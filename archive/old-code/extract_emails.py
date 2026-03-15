import re, json

with open(r'C:\Users\User\Desktop\Work\touch2_business_pressure_mar9.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Strip footer
content = re.sub(r'\n## Special Handling Summary.*', '', content, flags=re.DOTALL)

# Split into sections
sections = re.split(r'\n### #(\d+)', content)

emails = []
for i in range(1, len(sections), 2):
    num = int(sections[i])
    body = sections[i+1]
    
    # First non-empty lines (metadata)
    lines = [l for l in body.strip().split('\n') if l.strip()]
    meta_lines = lines[:3]  # first 3 lines usually have metadata
    meta_block = '\n'.join(meta_lines)
    
    # Detect flags
    is_gmail = 'GMAIL-ONLY' in meta_block or 'GMAIL' in meta_block.upper()
    is_dnc = '"send": "dnc"' in body or 'DNC' in meta_block.upper()
    is_seqflag = 'SEQUENCING' in meta_block.upper() or 'SEQ' in meta_block.upper()
    
    # Extract subject
    subj_match = re.search(r'\*\*Subject:\*\*\s*(.+)', body)
    subject = subj_match.group(1).strip() if subj_match else ''
    
    # Extract email body (everything from name line to end, excluding subject line markers)
    # Find the "Name," salutation
    body_clean = body.strip()
    
    # Try to extract just the email body (from first name greeting to "Rob")
    # Pattern: find first occurrence of a first name followed by comma
    name_match = re.search(r'\n([A-Z][a-z]+,)\n', body_clean)
    if name_match:
        body_start = body_clean.find(name_match.group(0))
        # Extract from name to end
        email_body_raw = body_clean[body_start:].strip()
        # Remove any trailing markdown
        # Stop at "---" separator
        sep_idx = email_body_raw.find('\n---')
        if sep_idx > 0:
            email_body_raw = email_body_raw[:sep_idx].strip()
        email_body = email_body_raw
    else:
        email_body = ''
    
    # Extract name and company from meta
    name_match2 = re.search(r'-\s+(.+?)\s+@\s+(.+?)(?:\n|$)', meta_block)
    if name_match2:
        name = name_match2.group(1).strip()
        company = name_match2.group(2).strip()
    else:
        name = f'Contact #{num}'
        company = ''
    
    # Get first name for salutation check
    first_name = name.split()[0] if name else ''
    
    emails.append({
        'num': num,
        'name': name,
        'first_name': first_name,
        'company': company,
        'subject': subject,
        'body': email_body,
        'is_gmail': is_gmail,
        'is_dnc': is_dnc,
        'is_seqflag': is_seqflag,
        'meta': meta_block[:200]
    })

# Save
with open(r'C:\Users\User\Desktop\Work\emails_data.json', 'w', encoding='utf-8') as f:
    json.dump(emails, f, indent=2, ensure_ascii=False)

# Print summary
gmail_list = [e for e in emails if e['is_gmail']]
dnc_list = [e for e in emails if e['is_dnc']]
seqflag_list = [e for e in emails if e['is_seqflag']]
apollo_list = [e for e in emails if not e['is_gmail'] and not e['is_dnc']]

print(f"Total: {len(emails)}")
print(f"Apollo: {len(apollo_list)}")
print(f"Gmail-only: {len(gmail_list)}")
print(f"DNC: {len(dnc_list)}")
print(f"SeqFlag: {len(seqflag_list)}")
print()
print("Gmail contacts:")
for e in gmail_list:
    print(f"  #{e['num']} {e['name']} @ {e['company']}")
print()
print("DNC contacts:")
for e in dnc_list:
    print(f"  #{e['num']} {e['name']} @ {e['company']}")
print()
print("SeqFlag contacts:")
for e in seqflag_list:
    print(f"  #{e['num']} {e['name']} @ {e['company']}")

# Sample email body for first apollo contact
apollo = [e for e in emails if not e['is_gmail'] and not e['is_dnc']]
if apollo:
    print(f"\nSample body for #{apollo[0]['num']} {apollo[0]['name']}:")
    print(repr(apollo[0]['body'][:500]))
    print(f"\nMeta for #{apollo[0]['num']}:")
    print(apollo[0]['meta'])
