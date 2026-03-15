import json, re, sys

files = {
    'Batch 6 unsent': r'C:\Users\User\BDR\outreach-batch6-unsent.html',
    'Batch 7 unsent': r'C:\Users\User\BDR\archive\old-batches\outreach-batch7-unsent.html',
    'Batch 8 unsent': r'C:\Users\User\BDR\outreach-batch8-unsent.html',
    'Batch 8 Desktop': r'C:\Users\User\Desktop\Work\prospect-outreach-batch8-20260302.html',
    'Batch 9': r'C:\Users\User\BDR\prospect-outreach-9-2026-03-01.html',
}

all_prospects = {}
for label, filepath in files.items():
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'(?:const\s+)?prospects(?:Data)?\s*=\s*(\[.*?\]);', content, re.DOTALL)
        if match:
            prospects = json.loads(match.group(1))
            print(f'{label}: {len(prospects)} prospects')
            for p in prospects:
                name = p.get('name','?')
                key = name.strip().lower()
                title = p.get('title','?')
                company = p.get('company','?')
                email_status = p.get('email_status', '?')
                if key not in all_prospects:
                    all_prospects[key] = {'name': name, 'title': title, 'company': company, 'email_status': email_status, 'batches': [label]}
                else:
                    all_prospects[key]['batches'].append(label)
        else:
            print(f'{label}: No prospectsData found, trying regex...')
            names = re.findall(r'"name":\s*"([^"]+)"', content)
            titles_found = re.findall(r'"title":\s*"([^"]+)"', content)
            companies_found = re.findall(r'"company":\s*"([^"]+)"', content)
            email_statuses = re.findall(r'"email_status":\s*"([^"]+)"', content)
            print(f'  Found {len(names)} names via regex')
            for i, n in enumerate(names):
                key = n.strip().lower()
                t = titles_found[i] if i < len(titles_found) else '?'
                c = companies_found[i] if i < len(companies_found) else '?'
                es = email_statuses[i] if i < len(email_statuses) else '?'
                if key not in all_prospects:
                    all_prospects[key] = {'name': n, 'title': t, 'company': c, 'email_status': es, 'batches': [label]}
                else:
                    all_prospects[key]['batches'].append(label)
    except Exception as e:
        print(f'{label}: ERROR - {e}')

print(f'\nTotal unique prospects: {len(all_prospects)}')
print()
verified = [p for p in all_prospects.values() if p['email_status'] == 'verified']
unverified = [p for p in all_prospects.values() if p['email_status'] != 'verified']
print(f'Verified email: {len(verified)}')
print(f'Other status: {len(unverified)}')
print()
for key in sorted(all_prospects.keys()):
    p = all_prospects[key]
    batches_str = ', '.join(p['batches'])
    print(f"{p['name']}|{p['title']}|{p['company']}|{p['email_status']}|{batches_str}")
