# Auto Prospect + Enroll — Skill

## Description
Fully automated TAM Outbound batch builder. Runs the complete pipeline from account selection through enrollment without human intervention — provided every contact passes all compliance and quality gates. Produces a batch tracker HTML, a `batch{N}_sends.json`, and a messages.md summary ready for Rob's APPROVE SEND.

**What it automates:** Account selection → contact discovery → enrichment → 8-point compliance gate → T1 draft → MQS scoring → Apollo enrollment → tracker HTML → sends.json → notification.

**What it does NOT automate:** The actual email sends. Those always require Rob's explicit "APPROVE SEND" and per-send Gate 2 approval via `skills/apollo-send/SKILL.md`.

## Trigger
- Scheduled: Mon/Wed/Fri 6:30 AM (taskId: `auto-prospect-enroll`)
- Manual: "run auto batch", "prospect and enroll batch", "build me a batch automatically"

## ⛔ HARD RULES — READ FIRST
1. **NEVER send emails.** Enrollment creates tasks. Tasks require APPROVE SEND separately.
2. **Zero tolerance on compliance.** Any contact that fails ANY of the 8 checks is skipped entirely. No exceptions, no overrides without Rob in session.
3. **MQS ≥ 9/12 required.** Any draft scoring below 9 is discarded — contact is NOT enrolled.
4. **TAM domain check is mandatory.** If a domain is not in `tam-accounts-mar26.csv`, skip. Period.
5. **DNC list always current.** Read CLAUDE.md at the start of every run for the latest DNC entries.
6. **Daily cap: 35 contacts max.** Do not enroll more than 35 contacts per automated run. Quality > volume.
7. **TAM health gate.** If fewer than 50 uncontacted Factor + HIGH contacts remain in the TAM, pause the run and flag to Rob instead of prospecting from Medium.

---

## Phase 1: Setup and Account Selection

### Step 1.1 — Read context files
Read these files to load current state:
- `CLAUDE.md` — DNC list (always read fresh)
- `memory/pipeline-state.md` — current batch number, last batch date
- `memory/session/messages.md` — check for trigger-monitor output from today (HOT accounts)

### Step 1.2 — Determine next batch number
Check pipeline-state.md for the last batch number. Increment by 1. Set batch name:
`TAM Outbound Batch {N} {Mon/Tue/Wed format}`

### Step 1.3 — TAM health check
```python
import csv, subprocess

# Count uncontacted Factor + HIGH accounts
master_contacts = set()
with open('MASTER_SENT_LIST.csv') as f:
    for row in csv.DictReader(f):
        domain = row['norm'].split('@')[-1] if '@' in row['norm'] else ''
        master_contacts.add(row['norm'].lower())

# Read TAM file and find uncontacted HIGH/Factor accounts
uncontacted_high = []
with open('tam-accounts-mar26.csv') as f:
    for row in csv.DictReader(f):
        if row.get('ICP', '').upper() in ['FACTOR', 'HIGH']:
            # Check if we've contacted anyone at this domain
            domain = row.get('domain', '').lower()
            # Count contacts at this domain in MASTER_SENT_LIST
            result = subprocess.run(['grep', '-ci', domain, 'MASTER_SENT_LIST.csv'],
                                  capture_output=True, text=True)
            count = int(result.stdout.strip()) if result.returncode == 0 else 0
            if count < 3:  # fewer than 3 contacts reached at this account
                uncontacted_high.append(row)

print(f"Uncontacted Factor/HIGH accounts: {len(uncontacted_high)}")
# If < 50: pause and flag to Rob
```

If fewer than 50 uncontacted Factor/HIGH accounts: write to messages.md:
`[AUTO-BATCH WARNING] TAM health low — only {N} uncontacted Factor/HIGH accounts remain. Pausing auto-batch. Rob: expand TAM or approve Medium tier?`
Then STOP. Do not proceed to prospecting.

### Step 1.4 — Select target accounts
Priority order:
1. **HOT accounts from trigger-monitor** (if messages.md has trigger output from today or yesterday)
2. **Factor accounts** (38 total) not yet contacted or with fewer than 2 contacts reached
3. **TAM HIGH** accounts — sorted by last trigger date or funding recency
4. **TAM MEDIUM** — only if Factor + HIGH pool is thin (Rob approval required)

Select 6-8 target accounts per run (expect 4-6 qualifying contacts per account = 25-35 total).

---

## Phase 2: Contact Discovery

### Step 2.1 — Search Apollo for QA contacts at each account
For each target account, search Apollo for contacts by title priority:

**Priority 1 (target first):**
- QA Manager, QA Lead, Director of QA, VP Quality, Head of Quality, Head of QA, Director of Testing

**Priority 2 (secondary):**
- SDET, Test Automation Engineer, Automation Lead, Quality Engineer, Software Engineer in Test

**Priority 3 (only with clear intent signals):**
- VP Engineering, Software Engineering Manager, Director of Engineering

```
Tool: apollo_mixed_people_api_search
Parameters:
  q_organization_domains_list: ["{domain}"]
  person_titles: ["QA Manager", "QA Lead", "Director of QA", "SDET", "Test Automation Engineer",
                  "Automation Lead", "Quality Engineer", "VP Quality"]
  contact_email_status_v2: ["verified", "likely_to_engage"]
  per_page: 10
```

Target 3-5 contacts per account. Stop at 5 per account.

### Step 2.2 — Enrich each contact
For each contact found:
```
Tool: apollo_people_match
Parameters:
  first_name, last_name, organization_name, domain
```
Capture: email, title, LinkedIn URL, company description, estimated headcount, industry.

---

## Phase 3: Compliance Gate (all 8 checks per contact)

Run `skills/compliance-gate/SKILL.md` logic for each contact. Automated version:

```python
import csv, subprocess

def compliance_check(name, email, domain, dnc_list):
    results = {}

    # Check 1: MASTER_SENT_LIST
    result = subprocess.run(['grep', '-i', name.lower(), 'MASTER_SENT_LIST.csv'],
                          capture_output=True, text=True)
    results['master_list'] = 'BLOCKED' if result.stdout.strip() else 'CLEAR'

    # Check 2: DNC list (passed in from CLAUDE.md read)
    results['dnc'] = 'BLOCKED' if any(d.lower() in name.lower() for d in dnc_list) else 'CLEAR'

    # Check 6: TAM domain (most important hard gate)
    tam_result = subprocess.run(['grep', '-i', domain, 'tam-accounts-mar26.csv'],
                               capture_output=True, text=True)
    results['tam_domain'] = 'CLEAR' if tam_result.stdout.strip() else 'BLOCKED'

    verdict = 'CLEAR' if all(v == 'CLEAR' for v in results.values()) else 'BLOCKED'
    return verdict, results
```

Also run Check 3 (Apollo sequence check) via `apollo_contacts_search`.
Also run Check 5 (same-company count — flag if 5+ contacts already at that company).
Also run Check 7 (Gmail reply history from that domain).

**Verdict:** Any single BLOCKED = skip this contact entirely. Log the reason.

---

## Phase 4: T1 Draft Generation

For each contact that passed all compliance checks:

### Step 4.1 — Gather company context
Pull context needed for a specific, non-generic opener:
- Industry + company size (from Apollo enrichment)
- Any trigger signals from trigger-monitor output (job postings, funding, leadership change)
- If no triggers: use industry pressure angle (see below)

### Step 4.2 — Select proof point
Apply proof point rotation logic:
1. Check what proof point(s) other contacts at the same company are using (in this batch)
2. Check what proof points have been over-used recently (analytics/outreach.db — flag if >40% of last 30 sends used same story)
3. Match vertical to best proof point:

| Company Vertical | First Choice | Second Choice |
|-----------------|-------------|---------------|
| Insurance / FinServ | Hansard (compliance angle) | Cisco |
| FinTech | CRED (scale angle) | Hansard |
| Healthcare / Digital Health | Medibuddy (maintenance) | Sanofi |
| Pharma / Life Sciences | Sanofi (speed/compliance) | Medibuddy |
| SaaS / Tech | CRED (5x faster) | Fortune 100 |
| Enterprise / Manufacturing | Cisco (35% reduction) | Fortune 100 |
| Retail / E-Commerce | Medibuddy (maintenance) | CRED |

### Step 4.3 — Write the T1 draft
Apply the formula from `memory/sop-tam-outbound.md` Part 5:

**Structure:**
1. **Opener (1-2 sentences):** Company-specific challenge. No "I noticed." No "I saw." Reference their role + a real pressure specific to their company/industry/size.
2. **Bridge (1 sentence):** Connect the challenge to test automation as the root or amplifier.
3. **Proof point (2-3 sentences):** Named customer + specific stat + relevance tie-back.
4. **CTA (1 sentence):** "What day works to see how [Customer] made that shift?" or canonical "What day works to see how?"

**Word count:** 75-99 words (optimal). Do NOT exceed 99. Do NOT go below 75.

**Subject:** `{First}'s {role context} at {Company}` — SMYKM format.

**Banned phrases:** em dashes, "circling back", "following up", "wanted to connect", "reaching out", "I noticed", "I saw", "CI/CD", "low code", "flaky tests", "Would it be worth", "Worth comparing notes", "I figure", "enough about me"

**Proof point stats to use (exact phrasing):**
- Hansard: "cut their regression window from 8 to 5 weeks"
- CRED: "built 90% regression coverage and cut cycle time 5x"
- Medibuddy: "automated 2,500 tests and cut maintenance time in half"
- Cisco: "reduced regression failures by 35% in 90 days"
- Sanofi: "cut a 3-day compliance test cycle down to 80 minutes"
- Fortune 100: "tripled test coverage in 4 months without adding headcount"

### Step 4.4 — Run MQS scoring (automated)
Run the Python QA script from `skills/draft-qa/SKILL.md`:
- Must score ≥ 9/12
- Must pass all hard constraints (no placeholders, no banned openers, named customer required)

**If MQS < 9:** Do NOT enroll this contact. Log: "Draft failed QA for [Name] at [Company] — MQS {score}/12. Skipped."
**If MQS ≥ 9:** Proceed to enrollment.

---

## Phase 5: Enrollment

For all contacts with compliance CLEAR + MQS ≥ 9:

### Step 5.1 — Create Apollo contact (if not already in Apollo)
```
Tool: apollo_contacts_create
Parameters:
  first_name, last_name, email, title, organization_name
  run_dedupe: true  ← ALWAYS
```

### Step 5.2 — Batch enroll (max 5 per API call)
```
Tool: apollo_emailer_campaigns_add_contact_ids
Parameters:
  id: "69afff8dc8897c0019b78c7e"
  emailer_campaign_id: "69afff8dc8897c0019b78c7e"
  send_email_from_email_account_id: "68e3b53ceaaf74001d36c206"
  contact_ids: [up to 5 IDs]
  sequence_same_company_in_same_campaign: true
```

Handle skip reasons per `skills/apollo-enroll/SKILL.md` Step 3.

### Step 5.3 — Append to MASTER_SENT_LIST.csv
For each enrolled contact, append:
```
{name},{batch_name},{today_date},Email (Apollo TAM Outbound T1),0,{tracker_filename},{name_lowercase}
```

Verify row count: `wc -l MASTER_SENT_LIST.csv` — state exact count in report.

---

## Phase 6: Build Outputs

### Step 6.1 — Generate batch tracker HTML
Create `mnt/Work/tamob-batch-{YYYYMMDD}-auto.html` using the standard tracker format from prior batches (tamob-batch-20260313-2.html as reference). Include:
- One card per enrolled contact
- Status badge: "Enrolled — APPROVE SEND pending"
- Subject line, email body preview, MQS score, proof point used
- Company, title, Apollo ID

### Step 6.2 — Generate batch_sends.json
Create `/sessions/epic-laughing-ptolemy/batch{N}_sends.json`:
```json
[
  {
    "id": 1,
    "name": "Full Name",
    "first": "First",
    "email": "email@company.com",
    "subject": "First's QA work at Company",
    "body": "Full approved T1 body text..."
  }
]
```

### Step 6.3 — Update analytics DB
Add enrolled contacts to `analytics/outreach.db` outreach_sends table (channel_type = 'email', touch_number = 1).

---

## Phase 7: Notify Rob

Write to `memory/session/messages.md`:

```
[AUTO-BATCH {date} {time}] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ BATCH {N} READY — {N} contacts enrolled, {N} skipped

📋 ENROLLED ({N} contacts):
  • {Name} ({Title} @ {Company}) — MQS {score}/12 — Proof: {story}
  • [list all enrolled]

⛔ SKIPPED ({N} contacts):
  • {Name} ({Company}) — {reason: compliance check X / MQS {score}/12}

📊 STATS:
  • Accounts prospected: {N}
  • Contacts found: {N}
  • Passed compliance: {N}
  • Passed QA: {N} (enrolled)
  • Failed compliance: {N}
  • Failed QA: {N}

📁 FILES READY:
  • Tracker: tamob-batch-{YYYYMMDD}-auto.html
  • Sends JSON: batch{N}_sends.json
  • MASTER_SENT_LIST rows: {total}

⚡ NEXT STEP: Review enrolled contacts + draft content, then give APPROVE SEND to execute sends.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Quality Gates Summary

| Gate | Threshold | Failure action |
|------|-----------|---------------|
| Compliance: Check 1 (MASTER_SENT_LIST) | Not in list | Skip contact |
| Compliance: Check 2 (DNC) | Not in DNC | Skip contact |
| Compliance: Check 3 (Apollo sequence) | Not already enrolled | Skip or flag |
| Compliance: Check 6 (TAM domain) | Domain in tam-accounts-mar26.csv | Skip contact |
| Compliance: Check 7 (Gmail reply) | No prior negative reply | Skip contact |
| Draft QA: MQS score | ≥ 9/12 | Skip contact (do NOT enroll) |
| Draft QA: Hard constraints | All clear | Skip contact |
| Daily cap | ≤ 35 contacts | Stop enrolling when cap hit |
| TAM health | ≥ 50 uncontacted Factor/HIGH | Pause run if below threshold |

---

## What Requires Rob's Action After This Runs

1. **Review the batch report** in messages.md at session start
2. **Spot-check 3-5 drafted emails** from the tracker HTML — make sure tone and specificity feel right
3. **Give APPROVE SEND** for this batch when satisfied
4. **Execute sends** via `skills/apollo-send/SKILL.md` (using the auto-generated batch_sends.json)

The only thing this skill can NOT do autonomously is the actual send. Everything else is handled.

---

## Known Limitations

- **T1 draft quality** depends on available context. Contacts at accounts with no trigger signals (no job postings, no news) will have more generic openers. The MQS gate filters out the worst cases, but Rob should still spot-check.
- **Apollo credit usage:** ~2 credits per contact for enrichment. 35 contacts = ~70 credits per run. 3x/week = ~210 credits/week. Rob has ~6,800 credits as of Mar 14, so sustainable for 32 weeks.
- **New TAM accounts:** If tam-accounts-mar26.csv hasn't been updated, new intent accounts won't be reached. Refresh the TAM file manually as Factor signals come in.

---

*Created: 2026-03-14 (Session 37). Automates the full tam-t1-batch workflow through enrollment. Sends remain manual and require Rob's APPROVE SEND + Gate 2 approval per skills/apollo-send/SKILL.md. Prerequisite skills: compliance-gate, draft-qa, apollo-enroll.*

---

## Self-Improvement Loop

This skill maintains its own run log and learned-patterns file. Full protocol: `skills/_shared/learning-loop.md`

### Before Each Run
1. Read `skills/auto-prospect-enroll/learned-patterns.md` if it exists — apply any documented calibration adjustments
2. Count entries in `skills/auto-prospect-enroll/run-log.md` to determine current run number

### After Every Run — Append to run-log.md
```
### Run #[N] — [YYYY-MM-DD HH:MM]
- **Result:** [1-2 sentence summary]
- **Key metrics:** [skill-specific counts per _shared/learning-loop.md]
- **Anomalies:** [anything unexpected]
- **Adjustments made this run:** [any deviations from SKILL.md]
- **Output quality:** [Accurate / Mostly accurate / Needs calibration / Failed]
```

### Every 5th Run — Pattern Review
1. Read last 5 run-log.md entries
2. Extract recurring patterns, consistent edge cases, metric drift
3. Overwrite `skills/auto-prospect-enroll/learned-patterns.md` with updated findings
4. If a pattern appears in 4+ of 5 runs: write a `## SKILL UPDATE PROPOSAL — auto-prospect-enroll` entry to `memory/session/messages.md` for Rob's review

**Hard rule:** Never modify SKILL.md directly. Only propose updates via messages.md and wait for Rob's explicit approval.
