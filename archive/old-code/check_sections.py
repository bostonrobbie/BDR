import re

with open(r'C:\Users\User\Desktop\Work\touch2_business_pressure_mar9.md', 'r', encoding='utf-8') as f:
    content = f.read()

content_clean = re.sub(r'\n## Special Handling Summary.*', '', content, flags=re.DOTALL)
sections = re.split(r'\n### #(\d+)', content_clean)

nums = []
for i in range(1, len(sections), 2):
    nums.append(int(sections[i]))

out = [f'Total sections: {len(nums)}', f'Numbers: {nums}', '', 'Last 5 sections names:']
for i in range(1, len(sections), 2):
    num = int(sections[i])
    if num >= 60:
        body = sections[i+1]
        lines = [l for l in body.strip().split('\n') if l.strip()]
        name_line = lines[0] if lines else 'N/A'
        out.append(f'  #{num}: {name_line[:80]}')

with open(r'C:\Users\User\Desktop\Work\sections_out.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
