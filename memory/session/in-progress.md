# In-Progress — Crash Recovery Checkpoint

## Status: COMPLETE
## Session: 32-37
## Task ID: TASK-033 + TASK-036-ENROLL + TASK-036-SEND
## Task Name: TAM T1 Batch 9 — 56 drafted, 45 enrolled (Mar 13), 44/45 T1 SENT (Mar 14)
## Started: 2026-03-13
## Completed: 2026-03-14

## Objective
Source, dedup, enrich, and enroll up to 100 contacts from untouched high-ICP TAM/Factor accounts in the TAM Outbound - Rob Gorham sequence.

## Step List
- [x] Step 1: Read playbooks (SKILL.md, tam-t1-batch.md, dedup-protocol.md, apollo-enrollment.md)
- [x] Step 2: Identify target accounts (Factor + TAM HIGH not yet worked)
- [x] Step 3: Apollo People Search for all target accounts (20+ accounts)
- [x] Step 4: Dedup all candidates against MASTER_SENT_LIST.csv + DNC
- [x] Step 5: Enrich contacts via Apollo People Match (get emails)
- [x] Step 6: Create contacts in Apollo + enroll in batches of 5 — 56 contacts enrolled, confirmed via contacts_already_exists_in_current_campaign
- [x] Step 7: Build batch tracker HTML — tamob-batch-20260313-1.html
- [x] Step 8: Update MASTER_SENT_LIST.csv — 56 rows added, now 552 total
- [x] Step 9: Update handoff.md, messages.md — DONE. CLAIM posted. Handoff updated.

## Target Accounts (Priority Order)
### Factor (untouched):
- OSF HealthCare (osfhealthcare.org) — HIGH ICP, Signal Tier A
- Charles River Laboratories (criver.com) — Medium ICP
- Enterprise Mobility Inc (enterprisemobility.com) — Medium ICP
- Winsupply (winsupplyinc.com) — Medium ICP, Signal Tier A

### TAM HIGH (untouched):
- BMO (bmo.com) — Finance/Banking
- Farmers Insurance Exchange (farmers.com) — Insurance
- WatchGuard Technologies (watchguard.com) — Security
- Sysdig (sysdig.com) — Security
- Yext (yext.com) — SaaS
- SingleStore (singlestore.com) — Tech/DB
- Couchbase (couchbase.com) — Tech/DB
- Pathlock (pathlock.com) — Security
- AppLovin (applovin.com) — Mobile Tech
- Bethesda Softworks (bethesda.net) — Gaming
- Pluralsight (pluralsight.com) — EdTech
- Everbridge (everbridge.com) — SaaS
- Procore Technologies (procore.com) — SaaS (Construction)
- SailPoint (sailpoint.com) — Security/SaaS
- Jack Henry (jackhenry.com) — Fintech
- Point32Health (point32health.org) — Healthcare
- Evernorth Health Services (evernorth.com) — Healthcare
- hims & hers (hims.com) — Healthcare/DTC
- Zimmer Biomet (zimmerbiomet.com) — MedTech
- Tandem Diabetes Care (tandemdiabetes.com) — MedTech
- Saber Interactive (saber.games) — Gaming

## Files Being Created
- tamob-batch-20260313-1.html (batch tracker)
- MASTER_SENT_LIST.csv (appending rows)

## Resume Instructions
If crash: Start at Step 3 — Apollo People Search. All target accounts listed above.
If enrollment started: check which contacts already enrolled by reading messages.md CLAIM entry.

## Completion Notes — Batch 8 (Session 33)
- 56 contacts enrolled across 14 TAM HIGH accounts (tamob-batch-20260313-1.html)
- MASTER_SENT_LIST.csv: 552 rows total after Batch 8

## Completion Notes — Batch 9 (Session 35)
- 56 contacts drafted, 45 enrolled (11 dedup misses/other-campaign blocks)
- Accounts: SailPoint(4), Farmers(5), Bethesda(5), hims&hers(3), Rocket Software(5), Lemonade(1), Zimmer Biomet(2), Anaplan(6), Bungie(2), Celonis(2), Check Point(2), DraftKings(4), Zebra(4)
- MASTER_SENT_LIST.csv: 597 rows total (552 + 45)
- Sequence ID: 69afff8dc8897c0019b78c7e
- Send-from account ID: 68e3b53ceaaf74001d36c206
- Tracker: tamob-batch-20260313-2.html
- 11 excluded: Sandeep Enagala, Maria Mata, Abhishek Ravishankara, Elad Moshe, Swapna B, Jesse Ybarra, Jorge Dominguez, Bogdan Minciu, Brian Oppenheim, Tomer Weinberger, Doron Lehmann
- T2 due: Mar 18-21 (Day 5-8 from Mar 13 send)
