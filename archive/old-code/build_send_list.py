import json
import re
import os

work_dir = r'C:\Users\User\Desktop\Work'
out_path = os.path.join(work_dir, 'build_send_list_out.txt')
lines = []

# Gmail-only emails already confirmed
gmail_emails = {
    'Andy Nelsen': 'anelsen@rightworks.com',
    'Eduardo Menezes': 'emenezes@fulgentgenetics.com',
    'Hibatullah Ahmed': 'hahmed@spscommerce.com',
    'Amir Aly': 'amir.aly@procore.com',
}

# Read emails_data.json
with open(os.path.join(work_dir, 'emails_data.json'), 'r', encoding='utf-8') as f:
    contacts = json.load(f)

lines.append(f"Total contacts loaded: {len(contacts)}")

name_email_map = dict(gmail_emails)

# Email regex - exclude Rob's own addresses and common non-prospect domains
email_pat = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,6}')
exclude_domains = {
    'testsigma.com', 'testsigma.in', 'testsigma.net', 'testsigmaweb.com', 'testsigmatech.in',
    'example.com', 'gmail.com', 'sentry.io', 'anthropic.com', 'w3.org', 'linkedin.com',
    'apollo.io', 'schemas.microsoft.com', 'openxmlformats.org',
}

# Try batch7 JSON first (structured)
b7_json = os.path.join(work_dir, 'batch7-send-tracker.json')
if os.path.exists(b7_json):
    with open(b7_json, 'r', encoding='utf-8') as f:
        b7 = json.load(f)
    lines.append(f"Batch7 JSON keys: {list(b7.keys())[:10] if isinstance(b7, dict) else 'LIST'}")
    # Traverse and find email fields
    def find_emails_in_obj(obj, depth=0):
        found = []
        if depth > 8:
            return found
        if isinstance(obj, dict):
            email_val = None
            name_val = None
            for k, v in obj.items():
                kl = k.lower()
                if kl in ('email', 'email_address', 'emailaddress'):
                    if isinstance(v, str) and '@' in v:
                        email_val = v
                if kl in ('name', 'full_name', 'fullname', 'contact_name'):
                    if isinstance(v, str):
                        name_val = v
            if email_val and name_val:
                found.append((name_val, email_val))
            for v in obj.values():
                found.extend(find_emails_in_obj(v, depth+1))
        elif isinstance(obj, list):
            for item in obj:
                found.extend(find_emails_in_obj(item, depth+1))
        return found

    b7_pairs = find_emails_in_obj(b7)
    lines.append(f"Batch7 JSON email pairs found: {len(b7_pairs)}")
    for name, email in b7_pairs[:5]:
        lines.append(f"  {name} -> {email}")
    for name, email in b7_pairs:
        # Try to match to our contact list
        for c in contacts:
            if c['name'].lower() in name.lower() or name.lower() in c['name'].lower():
                if c['name'] not in name_email_map:
                    name_email_map[c['name']] = email

lines.append(f"After batch7 JSON: {len(name_email_map)} emails mapped")

# Read HTML batch files
html_files = [
    'outreach-sent-feb26-batch3.html',
    'outreach-sent-feb27-batch5a.html',
    'outreach-sent-feb27-batch5b.html',
    'outreach-batch6-unsent.html',
    'batch7-send-tracker.html',
    'intent-outreach-pipeline-2026-02-26.html',
    'outreach-sent-feb13-batch1-v2.html',
    'outreach-batch2-v2-unsent.html',
]

for html_file in html_files:
    path = os.path.join(work_dir, html_file)
    if not os.path.exists(path):
        lines.append(f"NOT FOUND: {html_file}")
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    before = len(name_email_map)

    for c in contacts:
        if c['is_dnc']:
            continue
        name = c['name']
        if name in name_email_map:
            continue

        # Try full name first, then last name
        search_terms = [name]
        parts = name.split()
        if len(parts) >= 2:
            search_terms.append(parts[-1])  # last name

        found_email = None
        for term in search_terms:
            idx = content.find(term)
            if idx < 0:
                continue
            # Get context around the name
            snippet = content[max(0, idx - 400): idx + 600]
            candidates = [e for e in email_pat.findall(snippet)
                          if e.split('@')[1].lower() not in exclude_domains]
            if candidates:
                found_email = candidates[0]
                break

        if found_email:
            name_email_map[name] = found_email

    after = len(name_email_map)
    lines.append(f"{html_file}: +{after - before} emails (total: {after})")

# Build final send list
send_list = []
for c in contacts:
    email = name_email_map.get(c['name'], '')
    is_seqflag = c.get('is_seqflag', False)
    # Davor Milosevic #65 - seqflag not detected by JSON due to emoji bug
    if c['num'] == 65 or 'Davor' in c['name']:
        is_seqflag = True

    send_list.append({
        'num': c['num'],
        'name': c['name'],
        'first_name': c.get('first_name', c['name'].split()[0]),
        'company': c['company'],
        'email': email,
        'subject': c['subject'],
        'body': c['body'],
        'is_gmail': c['is_gmail'],
        'is_dnc': c['is_dnc'],
        'is_seqflag': is_seqflag,
        'found_email': bool(email),
        'category': ('DNC' if c['is_dnc'] else
                     'SEQFLAG' if is_seqflag else
                     'READY' if email else 'MISSING_EMAIL'),
    })

with open(os.path.join(work_dir, 'send_list.json'), 'w', encoding='utf-8') as f:
    json.dump(send_list, f, indent=2, ensure_ascii=False)

# Summary
ready = [s for s in send_list if s['category'] == 'READY']
missing = [s for s in send_list if s['category'] == 'MISSING_EMAIL']
dnc = [s for s in send_list if s['category'] == 'DNC']
seqflag = [s for s in send_list if s['category'] == 'SEQFLAG']

lines.append(f"\n=== SEND LIST SUMMARY ===")
lines.append(f"READY (have email): {len(ready)}")
lines.append(f"MISSING EMAIL: {len(missing)}")
lines.append(f"DNC (skip): {len(dnc)}")
lines.append(f"SEQFLAG (pending Rob decision): {len(seqflag)}")
lines.append(f"\nMISSING EMAIL contacts:")
for m in missing:
    lines.append(f"  #{m['num']} {m['name']} @ {m['company']}")
lines.append(f"\nFirst 10 READY contacts:")
for r in ready[:10]:
    lines.append(f"  #{r['num']} {r['name']} @ {r['company']} -> {r['email']}")

with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("DONE")
