# Batch Dashboard — Pipeline Status Overview

## Description
Generates a consolidated HTML dashboard showing pipeline status across all TAM Outbound batches. Pulls from batch tracker HTML files, MASTER_SENT_LIST.csv (currently 495+ rows as of Mar 12, 2026), and `memory/warm-leads.md`. Shows reply rates, T2 due dates, warm leads, and contacts pending APPROVE SEND.

## Trigger
- Run on-demand: "show dashboard", "pipeline status", "where do we stand?", "batch overview"
- Run at session start (after checking replies)
- Run after completing a batch to update

## ⛔ APPROVE SEND RULE
This skill reads and reports. It does NOT draft or send anything. If the dashboard flags "T2 due" contacts, the next step is to run `skills/tam-t1-batch/SKILL.md` T2 drafting flow — with Rob's final APPROVE SEND before any sends.

---

## Step 1: Discover All Batch Files

```bash
cd /Work
ls tamob-batch-*.html outreach-sent-*.html 2>/dev/null | sort
```

Known file naming patterns (as of Mar 12):
- `tamob-batch-mar12-*.html` — TAM Outbound March 12 batches
- `outreach-sent-feb*.html` — February batches (Batches 1-8)
- Inbound: look in `/Work/` for inbound-related HTML files

For each batch file, extract using bash or Python:
- Batch name and date (from filename and title tag)
- Total contacts (count `.card` or contact divs)
- Status badges per contact (Draft Ready / Enrolled / T1 Sent / T2 Due / Bounced / Blocked)
- T2 due dates (T1 send date + 5-8 days per sequence)
- Proof point distribution

```bash
# Quick count from MASTER_SENT_LIST.csv
wc -l MASTER_SENT_LIST.csv
echo "Breakdown by batch:"
awk -F',' 'NR>1 {print $2}' MASTER_SENT_LIST.csv | sort | uniq -c | sort -rn | head -20
echo "Breakdown by channel:"
awk -F',' 'NR>1 {print $4}' MASTER_SENT_LIST.csv | sort | uniq -c | sort -rn
echo "Breakdown by date:"
awk -F',' 'NR>1 {print $3}' MASTER_SENT_LIST.csv | sort | uniq -c | sort -rn | head -20
```

---

## Step 2: Check Reply Status

```
Tool: gmail_search_messages
q: "to:robert.gorham@testsigma.com newer_than:14d"
maxResults: 50
```

Cross-reference reply sender domains against MASTER_SENT_LIST.csv to attribute replies to specific batches. Calculate per-batch reply rate.

---

## Step 3: Load Warm Leads from warm-leads.md

Read `memory/warm-leads.md` for active warm lead records. As of Mar 12:

**Active warm leads:**
- **Namita Jain (OverDrive)** — P1. T1 sent Feb 27 (coverage angle). Monitoring for reply.
- **Pallavi Sheshadri (Origami Risk)** — P2. Replied to premature T3 (INC-001). Rob sent follow-up Mar 2. Monitoring.
- **Evely Perrella (Aetna/CVS Health)** — P0 inbound. T1 sent Mar 12 (wrong body — INC-012). Rob sent correction via Gmail. Skip T2 (Rob already reached out). First re-contact eligible Mar 19.

---

## Step 4: Calculate T2 Due Dates

T2 is due Day 5-8 from T1 send date (TAM Outbound sequence Step 2 cadence). Calculate for all contacts where T1 is sent and T2 has not gone yet.

Per `memory/playbooks/tam-t1-batch.md`:
- T1 → T2: Day 5-8 (not before Day 4 — INC-001)
- T2 → T3: Day 10-15

Flag any contact where T2 is due within the next 2 days as "URGENT."

---

## Step 5: Generate Dashboard HTML

Save to `/Work/pipeline-dashboard.html`. Dark theme, readable at a glance.

Key sections:
1. **Top stats row**: Total contacts sent (from MASTER_SENT_LIST row count), overall reply rate (Gmail vs. sent count), active warm leads, meetings booked
2. **"Actions Needed Today" banner**: T2 emails due, warm leads needing response, contacts pending APPROVE SEND
3. **Batch performance table**: One row per batch — date, contacts, channel, sent, replies, rate, meetings, status
4. **Active warm leads**: Name, company, type, last touch, next step
5. **Upcoming T2 due dates**: Contact, company, T1 sent date, T2 due date, urgency
6. **Sequence stage funnel**: Enrolled → T1 Sent → T1 Reply → T2 Sent → Meeting
7. **Reply rate by persona and vertical**: Compare against mabl-era baselines from `memory/data-rules.md`

Dashboard template (dark theme):
```html
<!DOCTYPE html>
<html>
<head>
  <title>Pipeline Dashboard — {date}</title>
  <style>
    body { font-family: -apple-system, sans-serif; background: #0f172a; color: #e2e8f0; padding: 24px; }
    h1 { font-size: 24px; color: #f8fafc; margin-bottom: 4px; }
    .subtitle { color: #94a3b8; font-size: 13px; margin-bottom: 24px; }
    .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
    .card { background: #1e293b; border-radius: 12px; padding: 20px; }
    .card .val { font-size: 32px; font-weight: 700; color: #f8fafc; }
    .card .lbl { font-size: 13px; color: #94a3b8; margin-top: 4px; }
    .card .delta { font-size: 13px; margin-top: 8px; color: #4ade80; }
    .section { background: #1e293b; border-radius: 12px; padding: 20px; margin-bottom: 16px; }
    .section h2 { font-size: 15px; color: #f8fafc; margin-bottom: 16px; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th { text-align: left; padding: 8px 12px; color: #94a3b8; border-bottom: 1px solid #334155; }
    td { padding: 8px 12px; border-bottom: 1px solid #1e293b; }
    .banner { background: #1e293b; border-left: 4px solid #f59e0b; padding: 14px 18px; border-radius: 0 8px 8px 0; margin-bottom: 16px; }
    .banner h3 { color: #fbbf24; font-size: 13px; margin-bottom: 6px; }
    .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .warm { border: 1px solid #f59e0b; }
    .badge { padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }
    .p0 { background: #7c2d12; color: #fdba74; }
    .p1 { background: #713f12; color: #fde68a; }
    .urgent { background: #7f1d1d; color: #fca5a5; }
  </style>
</head>
<body>
<h1>TAM Outbound Pipeline Dashboard</h1>
<p class="subtitle">Generated: {date} {time} | {N} batches | MASTER_SENT_LIST: {row_count} rows</p>

<div class="grid">
  <div class="card"><div class="val">{total_sent}</div><div class="lbl">Total Contacts Sent</div><div class="delta">+{this_week} this week</div></div>
  <div class="card"><div class="val">{reply_rate}%</div><div class="lbl">Reply Rate</div><div class="delta">{replies} / {sends}</div></div>
  <div class="card"><div class="val">{warm_leads}</div><div class="lbl">Active Warm Leads</div></div>
  <div class="card"><div class="val">{meetings}</div><div class="lbl">Meetings Booked</div></div>
</div>

<div class="banner">
  <h3>Actions Needed</h3>
  <p>{t2_due} T2 emails due | {warm_responses} warm leads need response | {pending_send} contacts pending APPROVE SEND</p>
</div>

<!-- Batch Performance, Warm Leads, T2 Due, Funnel — populated from parsed data -->
</body>
</html>
```

---

## Step 6: Save and Present

```bash
# Save dashboard
# Output: /Work/pipeline-dashboard.html
```

Present link to Rob. Summarize in chat:
```
Pipeline as of Mar 12:
- 495 contacts in MASTER_SENT_LIST.csv across 10+ batches
- Active warm leads: Namita Jain (OverDrive, P1), Pallavi Sheshadri (Origami Risk, P2), Evely Perrella (Aetna, P0/INC-012)
- T2 due: [N] contacts from Mar 7-8 batches (Day 5-8 from T1)
- Actions: [list]
```

---

## Integration Points
- Called by: Session start, post-batch workflow, `skills/tam-t1-batch/SKILL.md` (pipeline visibility step)
- Reads: All `tamob-batch-*.html` files, `MASTER_SENT_LIST.csv`, `memory/warm-leads.md`, `memory/pipeline-state.md`, `memory/session/handoff.md`
- Uses: Gmail MCP (reply attribution)
- Outputs: `/Work/pipeline-dashboard.html`

*Source: `memory/playbooks/tam-t1-batch.md` + `memory/warm-leads.md` + `memory/playbooks/dedup-protocol.md`*
*Last updated: 2026-03-12 (Session 30)*

---

## Self-Improvement Loop

This skill maintains its own run log and learned-patterns file. Full protocol: `skills/_shared/learning-loop.md`

### Before Each Run
1. Read `skills/batch-dashboard/learned-patterns.md` if it exists — apply any documented calibration adjustments
2. Count entries in `skills/batch-dashboard/run-log.md` to determine current run number

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
3. Overwrite `skills/batch-dashboard/learned-patterns.md` with updated findings
4. If a pattern appears in 4+ of 5 runs: write a `## SKILL UPDATE PROPOSAL — batch-dashboard` entry to `memory/session/messages.md` for Rob's review

**Hard rule:** Never modify SKILL.md directly. Only propose updates via messages.md and wait for Rob's explicit approval.
