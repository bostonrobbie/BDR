import json, re, os, csv

work_dir = r'C:\Users\User\Desktop\Work'
lines = []

# Current known emails
known = {
    'Andy Nelsen': 'anelsen@rightworks.com',
    'Eduardo Menezes': 'emenezes@fulgentgenetics.com',
    'Hibatullah Ahmed': 'hahmed@spscommerce.com',
    'Amir Aly': 'amir.aly@procore.com',
    'Jeff Barnes': 'jeff.barnes@digi.com',
    'Jose Moreno': 'jose.moreno@flywire.com',
    'Eyal Luxenburg': 'eyal.luxenburg@island.io',
    'Todd Willms': 'todd.willms@bynder.com',
    'Jason Ruan': 'jason.ruan@binance.com',
    'Thong Vu': 'thong.vu@hitachivantara.com',
    'Jennifer Ades': 'jennifer.ades@hitachivantara.com',
    'Lakshmi Maganthi': 'lakshmi.maganthi@netapp.com',
    'Adhiti Kannan': 'adhiti.kannan@iqvia.com',
    'Anand Kumar': 'anand.kumar@synechron.com',
    'Dan Knox': 'dknox@g2.com',
    'Peter Seliga': 'peter.seliga@medimpact.com',
    'Rick Colonello': 'rick.colonello@netapp.com',
    'Dena McEwan': 'dena.mcewan@iqvia.com',
    'Aline Cordier': 'aline.cordier@iqvia.com',
    'Anthony Oluoch': 'anthony.oluoch@medimpact.com',
    'Sandeep Shah': 'sandeep.shah@netapp.com',
    'Eileen Zheng': 'eileen.zheng@zelis.com',
    'Joyce Lee': 'joyce.lee@veeva.com',
    'Trent Walkup': 'trent.walkup@redsailtechnologies.com',
    'Dawn Coen': 'dcoen@opploans.com',
    'Prashanthi Nettem': 'pnettem@gtreasury.com',
    'Shalaka Munjal': 'smunjal@healthedge.com',
    'Vinayak Singh': 'visingh@pureinsurance.com',
    'Luis Sanchez': 'luis@drata.com',
    'Sachin Kumbhar': 'kumbhar@altair.com',
    'Kai Esbensen': 'kai.esbensen@granicus.com',
    'Jonathan Zarnosky': 'jonathan.zarnosky@freedompay.com',
    'Kia Duran': 'kduran@fleetio.com',
    'Kimberly Salerno': 'kimberly.salerno@instructure.com',
    'Vijaya Belthur': 'belthur@bessemer.com',
    'Ellen Puckett': 'ellen.puckett@invesco.com',
    'Julie Bozeman': 'julie.bozeman@color.com',
    'Patrick Southall': 'psouthall@goodrx.com',
    'Tom Bombara': 'tbombara@extremenetworks.com',
    'Thomas Lamontia': 'tom.lamontia@csgi.com',
    'Stu Naylor': 'snaylor@owlcyberdefense.com',
    'Joe Pember': 'joe.pember@riverbed.com',
    'Marc Jarvis': 'marc_jarvis@partech.com',
    'Sneha Prabhakar': 'sprabhakar@ariasystems.com',
    'Kamal Pokharel': 'kamal.pokharel@cedargate.com',
    'Tom Yang': 'tom.yang@versantmedia.com',  # DNC but keep for reference
}

with open(os.path.join(work_dir, 'emails_data.json'), 'r', encoding='utf-8') as f:
    contacts = json.load(f)

missing_contacts = [c for c in contacts if c['name'] not in known and not c['is_dnc']]
lines.append(f"Missing: {len(missing_contacts)}")
for m in missing_contacts:
    lines.append(f"  #{m['num']} {m['name']} @ {m['company']}")

email_pat = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,6}')
exclude = {'testsigma.com','testsigma.in','testsigma.net','testsigmaweb.com','testsigmatech.in','example.com','gmail.com','sentry.io'}

def scan_file_for_emails(filepath, source_name):
    if not os.path.exists(filepath):
        lines.append(f"NOT FOUND: {filepath}")
        return
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    before = len(known)
    # For each missing contact, find name and nearby email
    for c in missing_contacts:
        if c['name'] in known:
            continue
        name = c['name']
        # Try full name, first+last
        search_terms = [name]
        parts = name.split()
        if len(parts) >= 2:
            search_terms.append(f"{parts[0]}.*{parts[-1]}")  # regex

        for term in search_terms:
            try:
                idxs = [m.start() for m in re.finditer(re.escape(term) if '.' not in term else term, content, re.IGNORECASE)]
            except:
                idxs = []
            for idx in idxs[:3]:
                snippet = content[max(0, idx-200):idx+400]
                emails = [e for e in email_pat.findall(snippet) if e.split('@')[1].lower() not in exclude]
                if emails:
                    known[name] = emails[0]
                    lines.append(f"  {source_name}: {name} -> {emails[0]}")
                    break
            if name in known:
                break

    after = len(known)
    lines.append(f"{source_name}: +{after-before} new emails (total: {len(known)})")

# Scan relevant files
files_to_scan = [
    ('touch2_drafts_all_contacts_mar6.md', 'T2-mar6'),
    ('touch2_drafts_enhanced_mar9.md', 'T2-mar9'),
    ('hyper_personalized_touch1_emails.md', 'T1-hyper'),
    ('personalized_sequence_emails.md', 'personalized'),
    ('touch2_drafts_batch3_inmail.md', 'T2-batch3'),
    ('touch1_batch5_emails.md', 'T1-batch5'),
    ('touch1_batch6_emails.md', 'T1-batch6'),
    ('intent-email-sequences-2026-02-27.html', 'intent-html'),
    ('email_send_execution_plan.md', 'exec-plan'),
    ('sequence_status_report_mar6.md', 'seq-status'),
    ('email_sequence_performance_audit_mar7.md', 'audit-mar7'),
    ('touch1_emails_Q1_Tier1.md', 'T1-tier1'),
    ('touch1_emails_Q1_Tier1_v2.md', 'T1-tier1-v2'),
    ('research_tab.csv', 'research-csv'),
]

for fname, label in files_to_scan:
    scan_file_for_emails(os.path.join(work_dir, fname), label)

# Show all mapped (non-DNC) in final summary
lines.append(f"\n=== FINAL: {len(known)} emails total ===")
still_missing = [c for c in contacts if c['name'] not in known and not c['is_dnc']]
lines.append(f"Still missing: {len(still_missing)}")
for m in still_missing:
    lines.append(f"  #{m['num']} {m['name']} @ {m['company']}")

with open(os.path.join(work_dir, 'get_emails3_out.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print("DONE")
