import re

with open(r'C:\Users\User\Desktop\Work\touch2_business_pressure_mar9.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find using split method like build_viewer.py does
content_clean = re.sub(r'\n## Special Handling Summary.*', '', content, flags=re.DOTALL)
sections = re.split(r'\n### #(\d+)', content_clean)

out = []
for i in range(1, len(sections), 2):
    num = int(sections[i])
    if num == 65:
        body = sections[i+1]
        out.append(f'=== SECTION #65 ===')
        out.append(body[:1500])
        break

with open(r'C:\Users\User\Desktop\Work\raw65_out.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out) if out else 'NOT FOUND')
