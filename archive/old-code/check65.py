import json
with open(r'C:\Users\User\Desktop\Work\emails_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
e = data[64]
with open(r'C:\Users\User\Desktop\Work\e65_out.txt', 'w', encoding='utf-8') as f:
    f.write(json.dumps(e, indent=2))
