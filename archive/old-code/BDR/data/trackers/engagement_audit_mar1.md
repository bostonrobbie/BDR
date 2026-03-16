# Engagement Audit: 25 Tier 1 Intent Prospects
## Date: March 1, 2026
## Sequence: Q1 Website Visitor - Tier 1 Intent

---

## CRITICAL FLAGS — Recommend REMOVAL from sequence

### 1. Andy Roth — Director of QA Engineering @ Teaching Strategies
- **Risk: HIGHEST** — Had a scheduled appointment with another BDR
- In **4 sequences** total (3 finished/failed + our Tier 1)
- Previous sequence finished with reason: **"scheduled appointment / interested"** (BDR: Meimozhi Vendhan, meimozhi.vendhan@testsigma.com)
- Another sequence failed with "contact_stage_safeguard" (BDR: Raghava Surya)
- Contact stage: **Connected** (not New)
- Has Salesforce contact ID + lead ID
- Last activity: Jan 12, 2026
- Custom fields: "SEP 2025 Starwest US Event", "Starwest_Raghava_Full Attendees_Valid"
- Original source: salesforce_lead
- **Action: REMOVE immediately. This person had an appointment with Testsigma and is a warm/active contact managed by another BDR.**

### 2. Katie Hotard — Director of QA @ Lucid Software
- **Risk: HIGH** — Triple-sequenced across 3 active campaigns
- Active in sequence `699f4089628b940011da7fb7` (added Feb 25, from testsigma.in)
- Active in sequence `69a05801fdd140001d3fc014` (added Feb 28, from testsigma.net)
- Active in our Tier 1 sequence
- **Action: REMOVE from Tier 1. Already being emailed from 2 other sequences — risk of spam/unsubscribe.**

### 3. Giang Hoang — Director of QA @ Employee Navigator
- **Risk: HIGH** — Triple-sequenced (same pattern as Katie Hotard)
- Active in sequence `699f4089628b940011da7fb7` (added Feb 25, from testsigma.in)
- Active in sequence `69a05801fdd140001d3fc014` (added Feb 28, from testsigma.net)
- Active in our Tier 1 sequence
- **Action: REMOVE from Tier 1. Already being emailed from 2 other sequences.**

### 4. Mark Freitag — Director, Quality Engineering @ Alarm.com
- **Risk: HIGH** — Just finished another full sequence 18 days ago
- In 2 sequences: finished `69454e7438f1f80011693c5c` (completed all 7 steps, BDR: Raghava Surya via testsigma.in, finished Feb 11) + our Tier 1
- Has Salesforce contact ID (`003OX00000ZjdaZYAR`) + account ID
- Contact stage: `5e6be7ced287310106f43b93` (Attempted to Contact — not New)
- Last activity: Feb 11, 2026
- Created Dec 2023 from Salesforce by another user
- Has campaign custom field tags
- Account owned by another user (`6893092ef4354b0011be4014`)
- Catchall domain
- **Action: REMOVE. He just went through an entire 7-step sequence that ended 18 days ago. Re-sequencing immediately is aggressive and risks spam complaints.**

### 5. Khalid Aziz — Director of Test Automation @ Keeper Security
- **Risk: HIGH** — In Salesforce with prior outbound email activity
- Has Salesforce contact ID (`003OX00000GfuReYAJ`) + lead ID (`00QOX00000INrin2AD`)
- email_source: **"emailer_message_outbound"** (previously emailed from Apollo)
- Last activity: Nov 19, 2024
- Created Apr 2024 by another team member via search
- Has 2 label_ids and campaign custom field tags
- Account stage is non-default (existing CRM account)
- Has direct dial + valid mobile number
- **Action: REMOVE. Already in Salesforce as contact + lead, was previously emailed by the team. Another BDR may own this relationship.**

---

## MODERATE FLAGS — Recommend REVIEW before continuing

### 6. Scott Carruth — Director of QA @ Abrigo
- Has Salesforce contact ID (`003OX00000MGG7PYAX`) + account Salesforce ID
- Created Feb 2025 from LinkedIn by another user
- Custom fields: "19thFeb_MM_TAM_Batch1", "#ABM_2025", "TAM_BD_Jan2025"
- Was part of ABM/TAM campaigns in Jan-Feb 2025
- No last_activity_date, no prior sequence history
- **Action: MONITOR. Was in ABM/TAM campaigns but no sequence activity detected. Check with the TAM team if this account is being actively worked.**

### 7. Yuehli Dewolf — Senior Director, QA @ Vertafore
- In 2 active sequences: `6904f70577baa100190e4858` (added Feb 23) + our Tier 1
- Account has Salesforce ID (`001OX00000KV9UTYA1`)
- Account has multiple labels and last_activity_date
- **Action: MONITOR. Dual-sequenced but second sequence may be from a different motion. Verify the other sequence isn't also from your team.**

### 8. Rashad Fambro — Director, QA @ MedeAnalytics
- Has Salesforce contact ID (`003OX00000WouKmYAJ`) + account ID
- Created Nov 2025 from salesforce_contact by another user
- Custom fields: "#AIDriveSales" campaign tag + other tags
- No last_activity_date, only in Tier 1 sequence
- Account in Salesforce, owned by another user
- **Action: MONITOR. In Salesforce CRM but no sequence history or activity. Check if this account has an active AE or deal in Salesforce.**

### 9. Felix Tanh — Director, Quality Engineering @ Cofense
- Pre-existing contact from Aug 2023, created from LinkedIn by another user
- email_source: **"emailer_message_outbound"** (was previously emailed)
- Last activity: Apr 22, 2024
- Only in our Tier 1 sequence now
- **Action: LOW RISK but note the prior outbound. Old activity (2024), probably safe to continue but monitor for bounces/unsubscribes.**

---

## MINOR FLAGS — OK to continue, just noting pre-existing contacts

### 10. Kunal Patel — Sr. Director of QA @ aPriori Technologies
- Pre-existing from Aug 2023, created from LinkedIn by another user
- Last activity: Apr 22, 2024
- Only in Tier 1. No Salesforce. Catchall domain.
- **Action: Continue. Old contact, no concerning signals.**

### 11. Jennifer Bieg — SVP, QA @ RealPage
- Pre-existing from Aug 2021 (email_import)
- Last activity: Apr 13, 2020 (very old)
- Account has Salesforce ID
- Only in Tier 1
- **Action: Continue. Very old import, no recent engagement. Account Salesforce link may be from account-level CRM sync, not active deal.**

### 12. Alexander Tuaev — Director of QA @ Convoso
- Pre-existing from Apr 2024, created by another user via search
- Has label_ids and linked account
- No Salesforce. No last_activity_date. Only in Tier 1.
- **Action: Continue. Pre-existing but clean otherwise.**

### 13. Jennifer Marinas — Director of QA @ ETAP Software
- Pre-existing from Jul 2023, created from LinkedIn by another user
- Has label_ids and linked account
- No Salesforce. No last_activity_date. Only in Tier 1.
- **Action: Continue. Pre-existing but clean otherwise.**

---

## CLEAN — No prior engagement detected (12 prospects)

| # | Name | Company | Notes |
|---|------|---------|-------|
| 1 | Kenny Liu | ModMed | Created Mar 1 by us, no history |
| 2 | Tracy Grooms | Buildertrend | Created Feb 27 by us, no history |
| 3 | Amol Patil | ConnectWise | Created Mar 1 by us, catchall domain |
| 4 | Dave Cantrell | Solifi | Created Mar 1 by us, no history |
| 5 | Julia Yeh | Tempus AI | Created Mar 1 by us, no history |
| 6 | Ashutosh Singh | Acquia | Created Mar 1 by us, no history |
| 7 | Karen Motyka | Quickbase | Created Mar 1 by us, catchall domain |
| 8 | Pankaj Batra | ButterflyMX | Created Mar 1 by us, no history |
| 9 | Mark Nguyen | Aerospike | Created Mar 1 by us, no history |
| 10 | Jeremy Jensen | Awardco | Created Mar 1 by us, no history |
| 11 | Ryan Kennedy | Suvoda | Created Mar 1 by us, no history |
| 12 | Manu Jain | Iteris | Created Mar 1 by us, catchall domain |

---

## SUMMARY

| Category | Count | Names |
|----------|-------|-------|
| CRITICAL — Remove | 5 | Andy Roth, Katie Hotard, Giang Hoang, Mark Freitag, Khalid Aziz |
| MODERATE — Review | 4 | Scott Carruth, Yuehli Dewolf, Rashad Fambro, Felix Tanh |
| MINOR — Continue | 4 | Kunal Patel, Jennifer Bieg, Alexander Tuaev, Jennifer Marinas |
| CLEAN | 12 | Kenny, Tracy, Amol, Dave, Julia, Ashutosh, Karen, Pankaj, Mark N., Jeremy, Ryan, Manu |

**Gmail check:** No prior email conversations found in your inbox for any prospect.
**Slack check:** No specific deal mentions or client references found for any flagged company/person.

**Note:** The Gmail and Slack checks only cover YOUR inbox and public Slack channels. The Apollo data shows prior outbound emails were sent by OTHER BDRs (Meimozhi Vendhan, Raghava Surya) from different email accounts (testsigma.in, testsigmatech.in). Those conversations would be in their inboxes, not yours.

---

## RECOMMENDED NEXT STEPS

1. **Immediately remove 5 critical prospects** from the Tier 1 sequence to avoid spam risk and stepping on other BDRs' relationships
2. **Check with Raghava Surya** about Mark Freitag (Alarm.com) — he just completed Raghava's sequence 18 days ago
3. **Check with Meimozhi Vendhan** about Andy Roth (Teaching Strategies) — she had a scheduled appointment with him
4. **Find 5 replacement prospects** to maintain the 25-target count
5. **For moderate flags**, verify in Salesforce whether there are active deals or AE ownership before continuing
