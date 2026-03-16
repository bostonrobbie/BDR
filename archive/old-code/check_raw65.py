import re

with open(r'C:\Users\User\Desktop\Work\touch2_business_pressure_mar9.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find section #65
match = re.search(r'### #65\n(.*?)(?=\n### #66|\Z)', content, re.DOTALL)
if match:
    raw = match.group(0)
    with open(r'C:\Users\User\Desktop\Work\raw65_out.txt', 'w', encoding='utf-8') as f:
        f.write(raw[:2000])
else:
    with open(r'C:\Users\User\Desktop\Work\raw65_out.txt', 'w', encoding='utf-8') as f:
        f.write('NOT FOUND')
