# Trigger Monitor — Account Intelligence Alerts (Factor + TAM HIGH)

## Description
Scans Factor accounts (38) and TAM HIGH accounts for actionable trigger events: QA/SDET job postings, leadership changes, funding rounds, product launches. Surfaces the best "reason to reach out" before a batch starts, so every T1 opener is research-backed and timely. Scheduled Mon/Wed/Fri at 8am.

## Trigger
- Scheduled: Mon/Wed/Fri 8am (taskId: `trigger-monitor`)
- Run before starting a new batch: "check triggers", "any news on our accounts?", "scan Factor accounts"
- Run on-demand: "trigger check for [company]", "what's happening at [company]?"

## ⛔ APPROVE SEND RULE
This skill surfaces intelligence and suggests angles. It does NOT draft emails or send anything. Any outreach based on trigger data goes through the normal TAM T1 Batch workflow, with Rob's explicit APPROVE SEND required before any sends.

---

## Phase 1: Account Selection

**Scheduled run:** Check ALL 38 Factor accounts + top TAM HIGH accounts (not yet fully contacted)
**On-demand:** Check the specific companies requested
**Pre-batch:** Check the accounts you're about to add to the next batch

Load account lists:
```bash
cd /Work
# Factor accounts — ICP = Factor in tam-accounts-mar26.csv
grep -i "factor" tam-accounts-mar26.csv | head -50

# TAM HIGH accounts
grep -i "high" tam-accounts-mar26.csv | head -50
```

Cross-reference against MASTER_SENT_LIST.csv to see which accounts are already contacted:
```bash
awk -F',' 'NR>1 {print $1}' MASTER_SENT_LIST.csv | sort -u
```

---

## Phase 2: Job Posting Check (Apollo)

For each account, find the org ID then pull job postings:

```
Tool: apollo_mixed_companies_search
q_organization_domains_list: ["{domain}"]
per_page: 1
```

Get org ID from result, then:
```
Tool: apollo_organizations_job_postings
id: "{org_id}"
per_page: 100
```

**QA-relevant job titles to flag:**
- P0: "QA Manager", "QA Lead", "Director of QA", "VP Quality", "Head of Quality"
- P0: "SDET", "Test Automation Engineer", "Automation Lead", "Quality Engineer"
- P1: "Software Engineer in Test", "QA Analyst" (scale signal), "Test Engineer"
- P1: "Director of Engineering", "VP Engineering", "CTO" (leadership opening)
- P3 (context only): General "Software Engineer", "DevOps"

Multiple QA postings = strongest signal (team scaling, capacity problem).

---

## Phase 3: Company News (Web Search)

For Factor accounts and any account where we have active contacts:
```
Tool: WebSearch
query: "{company name} funding OR launch OR acquisition 2026"

Tool: WebSearch
query: "{company name} engineering OR quality OR testing 2026"
```

Extract:
- Funding announcements (amount, investors, date — relevant if within last 90 days)
- Product launches or major releases (relevant if within last 60 days)
- Acquisitions/mergers (inherited codebases = testing chaos)
- Leadership changes (new VP Eng / CTO / QA Director = 90-day evaluation window)

---

## Phase 4: Trigger Scoring

Score each account:

| Signal | Points |
|--------|--------|
| QA/SDET job posting (active) | +3 |
| Multiple QA postings (2+) | +2 additional |
| New QA/Eng leadership (last 90 days) | +3 |
| Funding round (last 90 days) | +2 |
| Product launch (last 60 days) | +2 |
| Acquisition/merger | +2 |
| Platform migration signal | +2 |
| Uses Selenium/Playwright (known pain point) | +1 |

**Tiers:**
- 5+ points: 🔥 HOT — Prioritize for next batch immediately
- 3-4 points: WARM — Strong candidate for next batch
- 1-2 points: NORMAL — Standard outreach priority
- 0 points: COLD — No current signals

---

## Phase 5: Match Trigger to Opener Angle

For each trigger, suggest the opening angle and proof point. Reference `memory/proof-points.md` for the full matching table.

**Trigger → Opener → Proof Point mapping:**

| Trigger | Opener angle | Best proof point |
|---------|-------------|-----------------|
| Hiring QA engineers | "Scaling the QA team usually means test volume is outpacing what the current process can handle..." | Medibuddy (50% maintenance cut) or CRED (90% coverage) |
| New VP Eng / CTO | "New engineering leadership usually means a tool audit in the first 90 days..." | Cisco (35% reduction) or Fortune 100 (3x in 4 months) |
| Funding raised | "When teams scale after a raise, testing usually becomes the bottleneck before anything else..." | CRED (5x faster) or Fortune 100 (3x coverage) |
| Product launch | "Major launches usually mean regression cycles that took weeks before the release..." | Hansard (8 to 5 weeks) |
| Acquisition/M&A | "Every acquisition brings in a codebase with its own test environment nobody outside that team fully understands..." | Medibuddy or Cisco |
| Compliance/regulatory | "Regulatory changes usually mean test coverage has to expand, and the window to do it doesn't..." | Hansard (FinServ/compliance angle) or Oscar Health |
| Using Selenium/Playwright | Reference competitor comparisons doc (`1yFYzrb1FdCOzI9FoVcN2MyfI_vfLOqGy-79SLgjJ0Kc`) for gap angle | Cisco or CRED |

---

## Output Format

```
TRIGGER REPORT — Mar 12, 2026 (Mon/Wed/Fri run)
Accounts scanned: 38 Factor + 20 TAM HIGH
Triggers found: 6 accounts with signals

🔥 HOT (Score 5+):
━━━━━━━━━━━━━━━━
EPICOR (epicor.com) — Score: 7 | Factor account
  📋 Hiring: 3 QA Engineers, 1 SDET Lead (posted last 2 weeks)
  💰 Series B: $80M closed Jan 2026
  Opener: "Scaling the QA team and closing a round at the same time usually means test volume is about to run ahead of capacity..."
  Proof point: CRED (90% coverage, 5x faster)
  Best contact: Jason Lieberman, QA Manager (in Apollo)
  TAM domain: ✅ epicor.com in tam-accounts-mar26.csv

NORTHERNTRUST (northerntrust.com) — Score: 5 | TAM HIGH
  👔 New Director of Quality Engineering hired (started Feb 2026)
  🔧 Currently using: Selenium, Jenkins
  Opener: "New QA leadership usually means a tool audit in the first 90 days..."
  Proof point: Hansard (8→5 weeks — FinServ, compliance angle)
  Best contact: Seth Drummond, Director QA (in Apollo — check for enrollment)

WARM (Score 3-4):
━━━━━━━━━━━━━━━━
BEYONDTRUST (beyondtrust.com) — Score: 3
  📋 Hiring 2 QA Analysts
  Note: Catchall domain (beyondtrust.com) — flag in tracker

COLD/NO SIGNALS (29 accounts):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[accounts with no current signals — normal outreach priority]

CREDIT USAGE: ~76 credits (38 accounts × job postings + search)
NEXT RUN: Wednesday Mar 14, 8am
```

---

## Scheduled Task Config
```
taskId: trigger-monitor
cronExpression: "0 8 * * 1,3,5"
description: "Scan Factor + TAM HIGH accounts for trigger events Mon/Wed/Fri 8am"
```

## Credit Usage Note
Apollo Org Search + Job Postings: ~2 credits per account. Full Factor scan (38 accounts) ≈ 76 credits. Check balance first: `apollo_users_api_profile` with `include_credit_usage: true`.

## Integration Points
- Feeds into: `skills/enrichment-pipeline/SKILL.md` (account prioritization)
- Feeds into: `skills/tam-t1-batch/SKILL.md` (opener angles for T1 drafts)
- Reads: `tam-accounts-mar26.csv`, `memory/target-accounts.md`, `MASTER_SENT_LIST.csv`
- References: `memory/proof-points.md`, Trigger Event Playbook (`1e9DDmuOFtd9MgB1ol3MOJklzrq3vZn5oyevM6FAj_7I`)
- Uses: Apollo Org Search, Job Postings MCPs + WebSearch

*Source: `memory/target-accounts.md` + `memory/proof-points.md` + trigger event patterns from Session 30*
*Last updated: 2026-03-12 (Session 30)*

---

## Self-Improvement Loop

This skill maintains its own run log and learned-patterns file. Full protocol: `skills/_shared/learning-loop.md`

### Before Each Run
1. Read `skills/trigger-monitor/learned-patterns.md` if it exists — apply any documented calibration adjustments
2. Count entries in `skills/trigger-monitor/run-log.md` to determine current run number

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
3. Overwrite `skills/trigger-monitor/learned-patterns.md` with updated findings
4. If a pattern appears in 4+ of 5 runs: write a `## SKILL UPDATE PROPOSAL — trigger-monitor` entry to `memory/session/messages.md` for Rob's review

**Hard rule:** Never modify SKILL.md directly. Only propose updates via messages.md and wait for Rob's explicit approval.
