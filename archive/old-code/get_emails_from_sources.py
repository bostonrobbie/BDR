import json
import re
import os
import csv

work_dir = r'C:\Users\User\Desktop\Work'
lines = []

# Load our contact list
with open(os.path.join(work_dir, 'emails_data.json'), 'r', encoding='utf-8') as f:
    contacts = json.load(f)

name_email_map = {
    'Andy Nelsen': 'anelsen@rightworks.com',
    'Eduardo Menezes': 'emenezes@fulgentgenetics.com',
    'Hibatullah Ahmed': 'hahmed@spscommerce.com',
    'Amir Aly': 'amir.aly@procore.com',
}

def try_match(name, email, note=''):
    """Try to match name to one of our contacts."""
    for c in contacts:
        cn = c['name'].lower()
        nn = name.lower().strip()
        if cn == nn or cn in nn or nn in cn:
            if c['name'] not in name_email_map:
                name_email_map[c['name']] = email
                lines.append(f"  MATCHED [{note}]: {c['name']} -> {email}")
            return True
    return False

# ---- Source 1: Apollo contacts export TSV ----
tsv_path = os.path.join(work_dir, 'apollo-contacts-export-2026-02-27.tsv')
if os.path.exists(tsv_path):
    with open(tsv_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
        content = f.read()
    lines.append(f"\n=== Apollo TSV ({len(content)} chars) ===")
    # Show first line (headers)
    first_line = content.split('\n')[0]
    lines.append(f"Headers: {first_line[:300]}")
    reader = csv.DictReader(content.splitlines(), delimiter='\t')
    rows = list(reader)
    lines.append(f"Rows: {len(rows)}")
    for row in rows:
        # Find name and email fields
        name = row.get('Name', row.get('Full Name', row.get('Contact Name', '')))
        email = row.get('Email', row.get('Email Address', row.get('Work Email', '')))
        if name and email and '@' in email:
            try_match(name, email, 'apollo-tsv')
    lines.append(f"After Apollo TSV: {len(name_email_map)} emails mapped")

# ---- Source 2: email_outreach_tracker.csv ----
tracker_path = os.path.join(work_dir, 'email_outreach_tracker.csv')
if os.path.exists(tracker_path):
    with open(tracker_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
        content = f.read()
    lines.append(f"\n=== email_outreach_tracker.csv ({len(content)} chars) ===")
    first_line = content.split('\n')[0]
    lines.append(f"Headers: {first_line[:400]}")
    reader = csv.DictReader(content.splitlines())
    rows = list(reader)
    lines.append(f"Rows: {len(rows)}")
    for row in rows:
        name = row.get('Name', row.get('Contact Name', row.get('Full Name', '')))
        email = (row.get('Email', '') or row.get('Email Address', '') or 
                 row.get('Work Email', '') or row.get('email', ''))
        if name and email and '@' in email:
            try_match(name, email, 'tracker-csv')
    lines.append(f"After tracker CSV: {len(name_email_map)} emails mapped")

# ---- Source 3: contacts_list.json ----
cj_path = os.path.join(work_dir, 'contacts_list.json')
if os.path.exists(cj_path):
    with open(cj_path, 'r', encoding='utf-8', errors='ignore') as f:
        cj = json.load(f)
    lines.append(f"\n=== contacts_list.json ===")
    lines.append(f"Type: {type(cj).__name__}, Length: {len(cj) if isinstance(cj, list) else 'dict'}")
    if isinstance(cj, list):
        for item in cj:
            if isinstance(item, dict):
                name = item.get('name', item.get('full_name', item.get('Name', '')))
                email = item.get('email', item.get('Email', item.get('email_address', '')))
                if name and email and '@' in email:
                    try_match(name, email, 'contacts-json')
    lines.append(f"After contacts_list.json: {len(name_email_map)} emails mapped")

# ---- Source 4: BATCH_5A_PROSPECTS.csv ----
b5a_path = os.path.join(work_dir, 'BATCH_5A_PROSPECTS.csv')
if os.path.exists(b5a_path):
    with open(b5a_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
        content = f.read()
    lines.append(f"\n=== BATCH_5A_PROSPECTS.csv ===")
    first_line = content.split('\n')[0]
    lines.append(f"Headers: {first_line[:300]}")
    reader = csv.DictReader(content.splitlines())
    rows = list(reader)
    lines.append(f"Rows: {len(rows)}")
    for row in rows:
        name = next((v for k,v in row.items() if 'name' in k.lower() and v), '')
        email = next((v for k,v in row.items() if 'email' in k.lower() and v and '@' in v), '')
        if name and email:
            try_match(name, email, 'batch5a-csv')
    lines.append(f"After batch5a CSV: {len(name_email_map)} emails mapped")

# ---- Source 5: touch2_drafts_all_contacts_mar6.md (look for "To:" or email patterns) ----
t2_path = os.path.join(work_dir, 'touch2_drafts_all_contacts_mar6.md')
if os.path.exists(t2_path):
    with open(t2_path, 'r', encoding='utf-8', errors='ignore') as f:
        t2content = f.read()
    lines.append(f"\n=== touch2_drafts_all_contacts_mar6.md ({len(t2content)} chars) ===")
    # Look for "To: email@domain.com" or "Email: " patterns
    email_pat = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,6}')
    exclude = {'testsigma.com','testsigma.in','testsigma.net','testsigmaweb.com','testsigmatech.in','example.com','gmail.com'}
    # Find "To: " or "email:" lines
    for line in t2content.splitlines():
        ll = line.lower()
        if ('to:' in ll or 'email:' in ll) and '@' in line:
            emails_found = [e for e in email_pat.findall(line) if e.split('@')[1].lower() not in exclude]
            if emails_found:
                lines.append(f"  Email line: {line.strip()[:100]}")
    # Also try looking for name near email in blocks
    blocks = re.split(r'\n#+\s+', t2content)
    for block in blocks[:5]:
        emails_found = [e for e in email_pat.findall(block) if e.split('@')[1].lower() not in exclude]
        if emails_found:
            lines.append(f"  Block emails: {emails_found[:3]}")
    lines.append(f"After touch2 mar6: {len(name_email_map)} emails mapped")

# ---- Summary ----
lines.append(f"\n=== FINAL SUMMARY ===")
lines.append(f"Total mapped: {len(name_email_map)}")
missing = [c for c in contacts if c['name'] not in name_email_map and not c['is_dnc']]
lines.append(f"Still missing: {len(missing)}")
for m in missing[:30]:
    lines.append(f"  #{m['num']} {m['name']} @ {m['company']}")

with open(os.path.join(work_dir, 'get_emails_out.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print("DONE")
