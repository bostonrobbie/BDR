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

# ---- SOURCE 1: touch2_drafts_all_contacts_mar6.md ----
# Each section has: name header, **Email:** email@domain
t2_path = os.path.join(work_dir, 'touch2_drafts_all_contacts_mar6.md')
with open(t2_path, 'r', encoding='utf-8', errors='ignore') as f:
    t2 = f.read()

lines.append("=== Parsing touch2_drafts_all_contacts_mar6.md ===")
# Split into sections by ## or ### headers
sections = re.split(r'\n(?=##+ )', t2)
lines.append(f"  Sections found: {len(sections)}")
for sect in sections:
    # Try to find name: first heading line
    heading_match = re.match(r'##+ (.+)', sect.strip())
    email_match = re.search(r'\*\*Email:\*\*\s*([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,6})', sect)
    if not email_match:
        continue
    email = email_match.group(1)
    
    # Try to match name from heading to our contacts
    if heading_match:
        heading_name = heading_match.group(1).strip()
        # heading might be "1. Andy Nelsen @ Rightworks" or "Andy Nelsen" etc.
        heading_name = re.sub(r'^\d+\.\s*', '', heading_name)  # remove leading "1. "
        heading_name = re.split(r'\s+@\s+', heading_name)[0].strip()  # take before @
        for c in contacts:
            cn = c['name'].lower()
            hn = heading_name.lower()
            if cn == hn or cn in hn or hn in cn:
                if c['name'] not in name_email_map:
                    name_email_map[c['name']] = email
                    lines.append(f"  MATCH: {c['name']} -> {email}")
                break
        else:
            lines.append(f"  NO MATCH for heading '{heading_name}' email={email}")

lines.append(f"After touch2 mar6: {len(name_email_map)} emails mapped")

# ---- SOURCE 2: Apollo TSV ---- 
tsv_path = os.path.join(work_dir, 'apollo-contacts-export-2026-02-27.tsv')
with open(tsv_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
    tsv_content = f.read()

lines.append(f"\n=== Apollo TSV ===")
reader = csv.DictReader(tsv_content.splitlines(), delimiter='\t')
tsv_rows = list(reader)
lines.append(f"  Rows: {len(tsv_rows)}")
lines.append(f"  First few names: {[r.get('Name','') for r in tsv_rows[:5]]}")
for row in tsv_rows:
    name = row.get('Name', '').strip()
    email = row.get('Email', '').strip()
    if not name or not email or '@' not in email:
        continue
    for c in contacts:
        cn = c['name'].lower()
        nn = name.lower()
        # Try various matching strategies
        cn_parts = cn.split()
        nn_parts = nn.split()
        if cn == nn:
            matched = True
        elif cn_parts[0] == nn_parts[0] and cn_parts[-1] == nn_parts[-1]:
            matched = True
        elif nn in cn or cn in nn:
            matched = True
        else:
            matched = False
        if matched and c['name'] not in name_email_map:
            name_email_map[c['name']] = email
            lines.append(f"  TSV MATCH: {c['name']} -> {email} (from '{name}')")
            break

lines.append(f"After Apollo TSV: {len(name_email_map)} emails mapped")

# ---- SOURCE 3: contacts_list.json ----
cj_path = os.path.join(work_dir, 'contacts_list.json')
with open(cj_path, 'r', encoding='utf-8', errors='ignore') as f:
    cj = json.load(f)
lines.append(f"\n=== contacts_list.json ({len(cj)} items) ===")
if cj:
    lines.append(f"  First item keys: {list(cj[0].keys()) if isinstance(cj[0], dict) else 'not dict'}")
    if isinstance(cj[0], dict):
        lines.append(f"  First item: {json.dumps(cj[0])[:300]}")
for item in cj:
    if not isinstance(item, dict):
        continue
    # Try all possible field names
    name = ''
    email = ''
    for k, v in item.items():
        kl = k.lower()
        if not name and any(x in kl for x in ['name', 'contact', 'full']):
            if isinstance(v, str) and len(v) > 1:
                name = v
        if not email and 'email' in kl:
            if isinstance(v, str) and '@' in v:
                email = v
    if not email:
        # look for email value anywhere
        for k, v in item.items():
            if isinstance(v, str) and '@' in v and 'testsigma' not in v.lower():
                email = v
                break
    if name and email:
        for c in contacts:
            if c['name'].lower() in name.lower() or name.lower() in c['name'].lower():
                if c['name'] not in name_email_map:
                    name_email_map[c['name']] = email
                    lines.append(f"  CJ MATCH: {c['name']} -> {email}")
                break

lines.append(f"After contacts_list.json: {len(name_email_map)} emails mapped")

# ---- SOURCE 4: BATCH_5A_PROSPECTS.csv (has Email column) ----
b5_path = os.path.join(work_dir, 'BATCH_5A_PROSPECTS.csv')
with open(b5_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
    b5content = f.read()
lines.append(f"\n=== BATCH_5A_PROSPECTS.csv ===")
reader = csv.DictReader(b5content.splitlines())
b5rows = list(reader)
lines.append(f"  Rows: {len(b5rows)}, Headers: {list(b5rows[0].keys()) if b5rows else []}")
for row in b5rows:
    name = row.get('Name', '').strip()
    email = row.get('Email', '').strip()
    if not name or not email or '@' not in email:
        continue
    if 'testsigma' in email.lower():
        continue
    for c in contacts:
        if c['name'].lower() == name.lower() or name.lower() in c['name'].lower():
            if c['name'] not in name_email_map:
                name_email_map[c['name']] = email
                lines.append(f"  B5A MATCH: {c['name']} -> {email}")
            break

lines.append(f"After batch5a: {len(name_email_map)} emails mapped")

# ---- SOURCE 5: step3_c2_rewrites (Touch 3 drafts with emails) ----
s3_path = os.path.join(work_dir, 'step3_c2_rewrites_batch2_2026-03-07.md')
if os.path.exists(s3_path):
    with open(s3_path, 'r', encoding='utf-8', errors='ignore') as f:
        s3 = f.read()
    lines.append(f"\n=== step3_c2_rewrites ===")
    sections = re.split(r'\n(?=##+ )', s3)
    lines.append(f"  Sections: {len(sections)}")
    for sect in sections:
        heading_match = re.match(r'##+ (.+)', sect.strip())
        email_match = re.search(r'\*\*(?:To|Email):\*\*\s*([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,6})', sect)
        if not email_match:
            # Also check for bare email on a line
            email_match = re.search(r'(?:To|Email):\s*([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,6})', sect)
        if not email_match:
            continue
        email = email_match.group(1)
        if 'testsigma' in email.lower():
            continue
        if heading_match:
            heading_name = heading_match.group(1).strip()
            heading_name = re.sub(r'^\d+\.\s*', '', heading_name)
            heading_name = re.split(r'\s+[@(]', heading_name)[0].strip()
            for c in contacts:
                if c['name'].lower() in heading_name.lower() or heading_name.lower() in c['name'].lower():
                    if c['name'] not in name_email_map:
                        name_email_map[c['name']] = email
                        lines.append(f"  S3 MATCH: {c['name']} -> {email}")
                    break
    lines.append(f"After step3: {len(name_email_map)} emails mapped")

# ---- Final summary ----
lines.append(f"\n=== FINAL SUMMARY ===")
lines.append(f"Total emails found: {len(name_email_map)}")
missing = [c for c in contacts if c['name'] not in name_email_map and not c['is_dnc']]
lines.append(f"Still missing: {len(missing)}")
for m in missing:
    lines.append(f"  #{m['num']} {m['name']} @ {m['company']}")

lines.append(f"\n=== ALL MAPPED EMAILS ===")
for name, email in sorted(name_email_map.items()):
    lines.append(f"  {name} -> {email}")

with open(os.path.join(work_dir, 'get_emails2_out.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print("DONE")
