# Skill: Warm Lead Re-Engagement Scanner

**Trigger:** Runs monthly on the 1st at 6:05 AM. Also callable on-demand.
**Purpose:** Surface contacts who replied with a timing/soft objection (P2) and whose re-engagement window has now passed. Prevents warm leads from going cold in the backlog.
**Output:** Appends a `## WARM LEAD RE-ENGAGEMENT` section to `memory/session/messages.md`.

---

## What This Skill Does

1. Reads `memory/warm-leads.md` — finds all P2 contacts with a `re_engage_after` date
2. Compares against today's date — flags anyone whose window has passed or is within 7 days
3. Cross-checks `MASTER_SENT_LIST.csv` — confirms last touch date and sequence stage
4. Checks DNC list in `CLAUDE.md` — removes any permanent skips
5. Writes a prioritized re-engagement report to `messages.md`

---

## Phase 1: Load Warm Leads

Read `memory/warm-leads.md` in full.

Extract all entries with:
- Status: `P2` (timing objection) or `P3` (nurture/low intent) that have a re-engage date
- Any entry with a `re_engage_after` or `follow_up_by` field

Build a working list: `{ name, company, title, reply_summary, re_engage_date, last_touch_date }`

---

## Phase 2: Date Filter

For each contact in the working list:

```
today = current date
days_until_reengagement = re_engage_date - today
```

**Bucket into three groups:**
- 🔴 **OVERDUE** — re_engage_date has already passed (> 0 days ago)
- 🟡 **DUE THIS WEEK** — re_engage_date is within 7 days
- 🔵 **UPCOMING** — re_engage_date is 8–30 days away (informational only, do not action)

Skip contacts with re_engage_date > 30 days out entirely — not relevant yet.

---

## Phase 3: MASTER_SENT_LIST Cross-Check

Read `MASTER_SENT_LIST.csv`.

For each contact in OVERDUE or DUE THIS WEEK buckets:
- Find their row(s) in MASTER_SENT_LIST
- Confirm last send date and sequence stage (T1, T2, T3, etc.)
- Flag if they have been sent a T2 or T3 (means they already went through the full sequence — re-engagement is a fresh T1, not a continuation)
- Flag if no row found in MASTER_SENT_LIST (data gap — note it)

---

## Phase 4: DNC Check

Cross-reference against the Do Not Contact list in `CLAUDE.md`:
- Remove any contact listed as "Skip permanently"
- Note any contact listed with a conditional re-engage window (e.g. "Re-engage after 60+ days with new trigger") — surface these separately with the original condition

---

## Phase 5: Classify Re-Engagement Approach

For each actionable contact, determine re-engagement type:

| Scenario | Approach |
|----------|----------|
| P2 timing ("reach out in Q2/after budget cycle") | Fresh T1 email with a new angle — do NOT reference prior sequence |
| P3 soft decline ("not the right time") | Fresh T1 only if a new trigger exists (product launch, job change, funding) — otherwise skip |
| Had a call / meeting | Flag for Rob's personal review — these are higher-touch |
| DNC with conditional window | Only surface if re_engage_date passed AND new trigger exists |

**If no meaningful trigger exists for a P3 contact:** list them under a "No Action Yet" section — do not recommend outreach.

---

## Phase 6: Write to messages.md

Append the following section to `memory/session/messages.md`:

```markdown
---
## WARM LEAD RE-ENGAGEMENT — [DATE]

**Run:** Monthly re-engagement scan
**Actionable contacts:** [N]

### 🔴 OVERDUE — Re-engage now

| Name | Company | Title | Last Touch | Re-Engage By | Original Reply | Recommended Approach |
|------|---------|-------|-----------|--------------|----------------|---------------------|
| [Name] | [Co] | [Title] | [Date] | [Date] | [1-line summary] | Fresh T1 — [angle] |

### 🟡 DUE THIS WEEK

| Name | Company | Title | Last Touch | Re-Engage By | Original Reply | Recommended Approach |
|------|---------|-------|-----------|--------------|----------------|---------------------|

### 🔵 UPCOMING (next 8–30 days, informational)

| Name | Company | Title | Re-Engage By |
|------|---------|-------|-------------|

### ⏸ No Action Yet (no trigger)

| Name | Company | Reason |
|------|---------|--------|

---
**Next scan:** [1st of next month]
```

---

## Hard Rules

- NEVER draft or send re-engagement outreach without Rob's explicit request
- NEVER remove contacts from warm-leads.md — read only
- If warm-leads.md does not have a `re_engage_after` field for a P2 contact, note it as a data gap and surface the contact anyway with "date unknown — review manually"
- If `memory/warm-leads.md` does not exist or is empty, write "No warm leads on file yet" and exit cleanly

---

## Scheduled Task Config

```
Name: warm-lead-reengagement
Schedule: Monthly, 1st of each month at 6:05 AM
Cron: 5 6 1 * *
```

---

## Self-Improvement Loop

This skill maintains its own run log and learned-patterns file. Full protocol: `skills/_shared/learning-loop.md`

### Before Each Run
1. Read `skills/warm-lead-reengagement/learned-patterns.md` if it exists — apply any documented calibration adjustments
2. Count entries in `skills/warm-lead-reengagement/run-log.md` to determine current run number

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
3. Overwrite `skills/warm-lead-reengagement/learned-patterns.md` with updated findings
4. If a pattern appears in 4+ of 5 runs: write a `## SKILL UPDATE PROPOSAL — warm-lead-reengagement` entry to `memory/session/messages.md` for Rob's review

**Hard rule:** Never modify SKILL.md directly. Only propose updates via messages.md and wait for Rob's explicit approval.
