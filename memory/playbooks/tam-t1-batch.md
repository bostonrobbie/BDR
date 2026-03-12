# Playbook: TAM T1 Batch (End-to-End)

## When to Use
Every day that new T1 outreach is needed. This is the primary daily workflow per the operating directive: "Maximize new T1 pipeline volume."

---

## Overview
Source contacts from TAM/Factor accounts, research them, draft personalized T1 emails, QA gate them, enroll in Apollo, and present for Rob's APPROVE SEND. Target: 25-50 new contacts enrolled per send day.

---

## Full Process (10 Steps)

### Step 1: Source Accounts
**Priority order:**
1. Factor accounts with buyer intent (38 accounts in `tam-accounts-mar26.csv` where ICP column = "Factor")
2. TAM accounts with ICP = HIGH (from the 312 TAM accounts)
3. TAM accounts with ICP = MEDIUM

**Reference file:** `tam-accounts-mar26.csv` — contains 350 accounts (312 TAM + 38 Factor) with domains, ICP scores, and coverage status.

**Check coverage:** Read `memory/target-accounts.md` to see which accounts already have contacts enrolled. Skip fully-covered accounts.

### Step 2: Find Contacts at Target Accounts

**Method 1 — Apollo People Search:**
```
Tool: apollo_mixed_people_api_search
Parameters:
  q_organization_domains_list: ["epicor.com"]
  person_titles: ["QA Manager", "QA Lead", "Director of QA", "VP Quality", "Test Manager", "SDET Lead", "Automation Lead"]
  person_seniorities: ["manager", "director", "vp"]
```
Note: This does NOT return emails. Use enrichment after finding people.

**Method 2 — Sales Navigator Deep Sweep (browser):**
Open Sales Nav > Lead filters > Company = target > Title keywords = "QA" OR "Quality" OR "Test" OR "SDET" > Seniority = Manager, Director, VP. See `sales-nav-deep-sweep.md` playbook for detailed browser steps.

**Method 3 — Apollo Contact Search (existing contacts):**
```
Tool: apollo_contacts_search
Parameters:
  q_keywords: "Epicor QA"
```
This searches contacts already in the team's Apollo database.

### Step 3: Dedup Every Contact

Before proceeding with ANY contact, run the full dedup. See `dedup-protocol.md` playbook for complete steps. Quick version:
1. Grep name against `MASTER_SENT_LIST.csv`
2. Check CLAUDE.md DNC list
3. Search Apollo contacts for existing records
4. Check current batch tracker for duplicates within the batch

### Step 4: Verify TAM Domain (MANDATORY — per INC-010)

Every contact's company email domain MUST appear in `tam-accounts-mar26.csv`. This is the Pre-Enrollment Domain Verification Gate from `sop-tam-outbound.md` Part 11.

Steps:
1. Extract the domain from the contact's email (e.g., `epicor.com` from `jlieberman@epicor.com`)
2. Grep that domain against `tam-accounts-mar26.csv`
3. If NOT found: do NOT include in the TAM Outbound batch. The contact is non-TAM.
4. If found: proceed.

### Step 5: Research Each Contact

**Standard targeting (1-2 contacts per company):**
- LinkedIn title and headline
- Company size and industry
- 1 specific pain hypothesis tied to their role

**Medium targeting (3-5 contacts per company):**
- All of the above, PLUS:
- Each contact gets a unique angle (no two emails at the same company should feel the same)
- Different proof points per contact
- Role-specific language (VP gets strategic framing, Manager gets tactical)

**High targeting (6+ contacts per company):**
- All of the above, PLUS:
- Product-area specific angles (e.g., YouTube Music vs YouTube TV)
- Engineering blog references if available
- Job posting signals

### Step 6: Draft T1 Emails

**Formula (from sop-tam-outbound.md Part 6):**
- Subject: `{First name}'s {role context} at {Company}` (SMYKM style)
- Body structure: HC1 intro (1 sentence) → Challenge hook (1-2 sentences) → Proof point with numbers (1 sentence) → CTA: "What day works to see how?" (1 sentence)
- Word count: 75-99 words (sweet spot per data-rules.md: 39.0% reply rate)
- Exactly 2 question marks in the body
- Must mention Testsigma by name
- Must include a named customer with specific numbers (e.g., "Hansard cut regression 8 to 5 weeks")
- No em dashes. Use commas. Minimize hyphens.

**Proof point rotation:** Track which proof point each contact gets. No two contacts at the same company should get the same proof point. Available proof points:
- Hansard: regression 8→5 weeks
- CRED: 90% regression coverage, 5x faster
- Medibuddy: 2,500 tests, 50% maintenance cut
- Cisco: 35% regression time reduction
- Fortune 100: 3x test coverage in 4 months
- Samsung: cross-platform coverage
See `memory/proof-points.md` for the full list with vertical matching.

### Step 7: QA Gate Every Email

**MQS (Message Quality Score) — must be >= 9/12:**

| # | Check | Points |
|---|-------|--------|
| 1 | Word count 75-99 | 1 |
| 2 | Exactly 2 question marks | 1 |
| 3 | SMYKM subject line | 1 |
| 4 | HC1 intro (shows you know them) | 1 |
| 5 | Specific challenge hook (not generic) | 1 |
| 6 | Named customer with numbers | 1 |
| 7 | Testsigma mentioned by name | 1 |
| 8 | "What day works" CTA | 1 |
| 9 | No em dashes | 1 |
| 10 | No placeholder text (e.g., [COMPANY], {name}) | 1 |
| 11 | Different proof point from same-company contacts | 1 |
| 12 | Tone is conversational, not scripted | 1 |

**Hard failures (instant reject):**
- Any placeholder text
- Word count over 120 or under 60
- Missing proof point
- Same proof point as another contact at same company
- Contact is on DNC list
- Contact's domain is not in TAM accounts list

### Step 8: Build Batch Tracker HTML

See `batch-tracker-html.md` playbook for the full template. Key elements:
- One card per contact with all fields populated
- Status badge (Draft Ready → Enrolled → T1 Sent → T2 Due)
- QA gate checklist per contact
- Proof point rotation tracker
- Backlog section for contacts that couldn't be included (no email, wrong domain, etc.)

### Step 9: Create Apollo Contacts + Enroll

See `apollo-enrollment.md` playbook for the full process. Key reminders:
- Max 5 contacts per enrollment API call
- Always use `run_dedupe: true` when creating contacts
- Always use `sequence_same_company_in_same_campaign: true`
- Verify TAM domain BEFORE enrollment (Step 4 above)
- Log everything in MASTER_SENT_LIST.csv immediately after enrollment

### Step 10: Present for APPROVE SEND

Tell Rob:
- How many contacts enrolled
- Which companies
- Link to the batch tracker HTML
- Any blockers (ownership issues, catchall domains, etc.)
- Wait for explicit "APPROVE SEND" before sending any emails

**After APPROVE SEND:**
- Open Apollo Tasks tab
- For each contact with a Step 1 task: paste subject and body from the tracker HTML
- Click Send Now
- Update tracker badges to "T1 Sent {date}"
- T2 is due Day 5-8 from send date

---

## Timing

| Step | Estimated Time |
|------|---------------|
| Source accounts | 5-10 min |
| Find contacts (Apollo) | 10-15 min per account |
| Find contacts (Sales Nav) | 15-20 min per account |
| Dedup | 2-3 min per contact |
| TAM domain verification | 1 min per contact |
| Research | 3-5 min per contact |
| Draft T1 | 3-5 min per contact |
| QA gate | 1-2 min per contact |
| Build tracker HTML | 15-20 min |
| Apollo enrollment | 5-10 min per batch of 5 |
| Total for 10 contacts | ~90-120 min |
| Total for 25 contacts | ~180-240 min |

---

## Common Mistakes (from incident log)

1. **INC-010:** Enrolling non-TAM contacts in TAM Outbound sequence. Always verify domain against tam-accounts-mar26.csv.
2. **INC-007:** Sending placeholder emails (Apollo template instead of custom draft). Always paste the custom draft from the tracker HTML before clicking Send.
3. **INC-001:** Sending Touch 2 before Day 4 of the sequence. Respect the cadence: T2 not before Day 4, T3 not before Day 9.
4. **Double-sends:** Contact already received outreach from another channel/batch. Always dedup against MASTER_SENT_LIST.csv.
5. **Same proof point at same company:** Two contacts at Fidelity both getting the Hansard story. Track proof points per company in the tracker HTML.

---

*Last updated: 2026-03-12 — consolidated from Sessions 4-27*
