# Stage Monitor — Skill

## Description
Scans all active TAM Outbound contacts in Apollo and cross-references T1 send dates to surface who is due for T2, T3, or subsequent touches today. Runs as a scheduled task (daily, Monday-Friday) and can also be triggered manually at session start. Outputs a prioritized "what's due today" block so Rob never has to mentally reconstruct the T2/T3 calendar.

## Trigger
- Automatically: runs daily Mon-Fri at 8:30 AM (scheduled task)
- Manually: run at session start when work-queue.md doesn't show clear T2/T3 due dates
- Manually: any time Rob asks "what T2s are due" or "what's coming up this week"

## Prerequisites
- Apollo MCP connected
- MASTER_SENT_LIST.csv accessible (source of truth for T1 send dates by batch)
- `memory/pipeline-state.md` accessible (batch T1 send dates)

---

## Touch Timing Reference

| Touch | Trigger | Apollo task appearance |
|-------|---------|----------------------|
| T1 | Enrollment | 1-24h after enrollment |
| T2 | Day 5 from T1 send | Apollo tasks appear ~Day 5 |
| T3 | Day 10 from T1 send | Apollo tasks appear ~Day 10 (LinkedIn connect) |
| T4 | Day 15 | Phone call queue |
| T7 | Day 35 | Breakup email |

---

## Process

### Step 1: Load Batch Timeline
Read `memory/pipeline-state.md` to get T1 send dates for all active batches.

Build a timeline table:
| Batch | T1 Send Date | T2 Due (Day 5) | T3 Due (Day 10) | Contacts |
|-------|-------------|----------------|-----------------|---------|
| Batch 8 | Mar 13, 2026 | Mar 18, 2026 | Mar 23, 2026 | 55 |
| Batch 9 | Mar 14, 2026 | Mar 19, 2026 | Mar 24, 2026 | 44 |
| [prior batches] | ... | ... | ... | ... |

### Step 2: Calculate What's Due Today

```python
from datetime import datetime, timedelta

today = datetime.today().date()

batches = [
    {"name": "Batch 8", "t1_date": "2026-03-13", "contacts": 55},
    {"name": "Batch 9", "t1_date": "2026-03-14", "contacts": 44},
    # add more batches as they're sent
]

due_today = []
due_this_week = []

for b in batches:
    t1 = datetime.strptime(b["t1_date"], "%Y-%m-%d").date()
    t2_due = t1 + timedelta(days=5)
    t3_due = t1 + timedelta(days=10)
    t7_due = t1 + timedelta(days=35)

    days_until_t2 = (t2_due - today).days
    days_until_t3 = (t3_due - today).days

    if days_until_t2 == 0:
        due_today.append(f"🔴 T2 DUE TODAY — {b['name']} ({b['contacts']} contacts)")
    elif 0 < days_until_t2 <= 3:
        due_this_week.append(f"🟡 T2 in {days_until_t2}d — {b['name']} ({b['contacts']} contacts, due {t2_due})")

    if days_until_t3 == 0:
        due_today.append(f"🔴 T3 DUE TODAY — {b['name']} (LinkedIn connects)")
    elif 0 < days_until_t3 <= 3:
        due_this_week.append(f"🟡 T3 in {days_until_t3}d — {b['name']} (LinkedIn connects due {t3_due})")

print("=== DUE TODAY ===")
for item in due_today: print(item)
print("\n=== DUE THIS WEEK ===")
for item in due_this_week: print(item)
```

### Step 3: Check Apollo for Stuck / Bounced Contacts

For each batch with T2/T3 due, do a quick scan for any contacts that may have:
- Bounced (email invalid)
- Opted out (unsubscribed)
- Been manually paused
- Replied (should be in warm-leads.md, but double-check)

```
Tool: apollo_contacts_search
Parameters:
  emailer_campaign_id: "69afff8dc8897c0019b78c7e"
  contact_campaign_statuses: ["bounced", "unsubscribed", "stopped"]
  per_page: 25
```

For any contacts found in stopped/bounced status: add to the "exceptions" list in the report.

### Step 4: Check for Warm Leads Not Yet Handled

Run a quick Gmail scan for any replies in the last 48 hours that haven't been classified:
```
Tool: gmail_search_messages
q: "to:robert.gorham@testsigma.com is:unread newer_than:2d"
maxResults: 10
```

Cross-reference with `memory/warm-leads.md`. Any unhandled positive replies are P0 — flag them at the top of the report.

### Step 5: Output the Daily Report

Format:
```
=== STAGE MONITOR — {today's date} ===

🚨 WARM LEADS (P0 — handle first):
  - [Name] at [Company]: [reply summary] — needs response

🔴 DUE TODAY:
  - T2: Batch 8 (55 contacts) — Apollo tasks should appear now
  - T2: Batch 9 (partial, 12 contacts) — check task queue

🟡 DUE THIS WEEK:
  - T2: Batch 9 (remaining) — due Mar 21
  - T3: Batch 7 — LinkedIn connects due Mar 17

⚠️ EXCEPTIONS (bounced/stopped since last check):
  - [Name] at [Company]: bounced — remove from tracker

📊 PIPELINE SNAPSHOT:
  - Active T1 contacts: {N}
  - Awaiting T2: {N}
  - Awaiting T3: {N}
  - Positive replies: {N}
  - Total T1 sent (all time): {N}
```

### Step 6: Write to messages.md (if scheduled run)

If this is an automated scheduled run, append the report to `memory/session/messages.md` so Rob sees it at session start:
```
[STAGE-MONITOR {date}] T2 due: Batch 8 (Mar 18), Batch 9 (Mar 19). No new bounces. [full report in work-queue.md]
```

Also update `memory/session/work-queue.md`: if T2 tasks are due today, mark TASK-03X status = READY_TO_SEND.

---

## When to Escalate to Rob

Escalate immediately (don't wait for session start) if:
- Any positive reply detected in Gmail (P0 warm lead)
- More than 5 contacts bounced in a single batch
- Any batch is past Day 7 with no T2 sent (falling behind cadence)

---

## Scheduled Task Configuration

This skill is designed to run as a scheduled task. The schedule entry in `.scheduled-tasks` should be:
```
Name: stage-monitor
Schedule: Weekdays 8:30 AM
Command: Read and execute skills/stage-monitor/SKILL.md
Purpose: Daily pipeline due-date check, warm lead scan, T2/T3 calendar
```

To register: use the `schedule` skill to create this task.

---

*Created: 2026-03-14 (Session 37). Replaces manual T2/T3 date tracking in handoff.md. Works alongside reply-classifier (which handles full Gmail scan — stage-monitor's Gmail check is a lightweight supplement, not a replacement).*

---

## Self-Improvement Loop

This skill maintains its own run log and learned-patterns file. Full protocol: `skills/_shared/learning-loop.md`

### Before Each Run
1. Read `skills/stage-monitor/learned-patterns.md` if it exists — apply any documented calibration adjustments
2. Count entries in `skills/stage-monitor/run-log.md` to determine current run number

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
3. Overwrite `skills/stage-monitor/learned-patterns.md` with updated findings
4. If a pattern appears in 4+ of 5 runs: write a `## SKILL UPDATE PROPOSAL — stage-monitor` entry to `memory/session/messages.md` for Rob's review

**Hard rule:** Never modify SKILL.md directly. Only propose updates via messages.md and wait for Rob's explicit approval.
