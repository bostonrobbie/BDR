import re, json

with open(r'C:\Users\User\Desktop\Work\touch2_business_pressure_mar9.md', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'\n## Special Handling Summary.*', '', content, flags=re.DOTALL)
sections = re.split(r'\n### #(\d+)', content)

parsed = []
for i in range(1, len(sections), 2):
    num = int(sections[i])
    body = sections[i+1].strip()
    parsed.append((num, body))

contacts = []
for num, body in parsed:
    # Extract metadata line (first line)
    lines = body.split('\n')
    meta = lines[0] if lines else ''
    
    # Extract subject
    subj_match = re.search(r'\*\*Subject:\*\*\s*(.+)', body)
    subject = subj_match.group(1).strip() if subj_match else ''
    
    # Extract first name and company from meta
    # Format: -  Name @ Company\n...
    name_match = re.search(r'-\s+(.+?)\s+@\s+(.+?)(?:\n|$)', meta)
    if name_match:
        name = name_match.group(1).strip()
        company = name_match.group(2).strip()
    else:
        name = meta.strip('- ')
        company = ''
    
    # Check flags
    is_gmail = 'GMAIL-ONLY' in meta
    is_dnc = '"send": "dnc"' in body or 'DNC' in meta
    is_seqflag = 'SEQ' in meta or 'SEQUENCING' in meta
    
    # Extract T2 proof point
    proof_match = re.search(r'T2 Proof Point:\s*(.+?)(?:\n|$)', meta)
    proof = proof_match.group(1).strip() if proof_match else ''
    
    contacts.append({
        'num': num,
        'name': name,
        'company': company,
        'subject': subject,
        'is_gmail': is_gmail,
        'is_dnc': is_dnc,
        'is_seqflag': is_seqflag,
        'proof': proof
    })

# Summary
gmail_contacts = [c for c in contacts if c['is_gmail']]
dnc_contacts = [c for c in contacts if c['is_dnc']]
seqflag_contacts = [c for c in contacts if c['is_seqflag']]
apollo_contacts = [c for c in contacts if not c['is_gmail'] and not c['is_dnc']]

with open(r'C:\Users\User\Desktop\Work\contacts_list.json', 'w', encoding='utf-8') as f:
    json.dump(contacts, f, indent=2)

print(f"Total: {len(contacts)}")
print(f"Apollo (to send via task queue): {len(apollo_contacts)}")
print(f"Gmail-only: {len(gmail_contacts)}")
print(f"DNC (skip): {len(dnc_contacts)}")
print(f"Seq flag: {len(seqflag_contacts)}")
print()
print("GMAIL contacts:")
for c in gmail_contacts:
    print(f"  #{c['num']} {c['name']} @ {c['company']}")
print()
print("DNC contacts:")
for c in dnc_contacts:
    print(f"  #{c['num']} {c['name']} @ {c['company']}")
print()
print("SEQ FLAG contacts:")
for c in seqflag_contacts:
    print(f"  #{c['num']} {c['name']} @ {c['company']}")
print()
print("APOLLO contacts (first 20):")
for c in apollo_contacts[:20]:
    print(f"  #{c['num']} {c['name']} @ {c['company']}")
