import json

with open(r'C:\Users\User\Desktop\Work\emails_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

gmail = [e for e in data if e.get('is_gmail')]
dnc = [e for e in data if e.get('is_dnc')]
seq = [e for e in data if e.get('is_seqflag')]
apollo = [e for e in data if not e.get('is_gmail') and not e.get('is_dnc') and not e.get('is_seqflag')]

lines = []
lines.append(f'Total: {len(data)}')
lines.append(f'Apollo: {len(apollo)}')
lines.append(f'Gmail-only: {len(gmail)}')
lines.append(f'DNC: {len(dnc)}')
lines.append(f'SeqFlag: {len(seq)}')
lines.append('')
lines.append('Gmail contacts:')
for e in gmail:
    lines.append(f'  #{e["num"]} {e["name"]} @ {e["company"]}')
lines.append('')
lines.append('DNC contacts:')
for e in dnc:
    lines.append(f'  #{e["num"]} {e["name"]} @ {e["company"]}')
lines.append('')
lines.append('SeqFlag contacts:')
for e in seq:
    lines.append(f'  #{e["num"]} {e["name"]} @ {e["company"]}')
lines.append('')
lines.append('First 5 Apollo contacts:')
for e in apollo[:5]:
    lines.append(f'  #{e["num"]} {e["name"]} @ {e["company"]} | Subject: {e["subject"]}')
    lines.append(f'    Body (first 150 chars): {repr(e["body"][:150])}')
    lines.append('')

with open(r'C:\Users\User\Desktop\Work\check_data_out.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
