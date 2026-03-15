import re, sys

with open(r'C:\Users\User\Desktop\Work\touch2_business_pressure_mar9.md', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'\n## Special Handling Summary.*', '', content, flags=re.DOTALL)
sections = re.split(r'\n### #(\d+)', content)

parsed = []
for i in range(1, len(sections), 2):
    num = int(sections[i])
    body = sections[i+1].strip()
    parsed.append((num, body))

out_lines = [f'Total parsed: {len(parsed)}\n']
for target in [1, 11, 22, 35, 50]:
    for num, body in parsed:
        if num == target:
            out_lines.append(f'=== #{num} ===\n{body[:2000]}\n\n')
            break

with open(r'C:\Users\User\Desktop\Work\samples_out.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

print("Done")
