import re

with open(r'C:\Users\User\Desktop\Work\touch2_business_pressure_mar9.md', 'r', encoding='utf-8') as f:
    content = f.read()

content_clean = re.sub(r'\n## Special Handling Summary.*', '', content, flags=re.DOTALL)
sections = re.split(r'\n### #(\d+)', content_clean)

for i in range(1, len(sections), 2):
    if int(sections[i]) == 65:
        raw = sections[i+1]
        with open(r'C:\Users\User\Desktop\Work\raw65_out.txt', 'w', encoding='utf-8') as f:
            f.write(raw)
        break
