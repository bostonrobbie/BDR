# System Diagnostics — Cross-Skill Health Monitor & Performance Analyzer

**Version:** 1.0 — Created Mar 15, 2026
**Schedule:** Sundays 6:00 AM (weekly) + on-demand
**Output:** Writes to `diagnostics/system-health-report.md` + appends to `memory/session/messages.md`

---

## Purpose

This skill is the meta-layer above all other skills. While individual skills monitor their own performance via the learning loop (`skills/_shared/learning-loop.md`), this skill looks ACROSS the whole system:

1. **Health Check** — Are all scheduled skills actually running? Any silent failures?
2. **Performance Correlation** — Do higher MQS scores produce higher reply rates? Which personas reply most? Which proof points land?
3. **Call Analytics** — Parse `memory/call-log.md`, compute connect rates, surface coaching insights
4. **Data Freshness** — Is the analytics DB up to date? Is MASTER_SENT_LIST accurate?
5. **System Recommendations** — What should change to improve outcomes?

---

## Trigger

Run this skill when:
- Rob asks for a "system health check" or "how is the system doing"
- It's Sunday morning (scheduled)
- After 5+ sessions without a diagnostic run (check `diagnostics/run-log.md` for last run date)
- After any incident (INC-*) to assess systemic impact

---

## Phase 1: Skill Run Log Audit

For each skill in `skills/`:
1. Check if `skills/{skill-name}/run-log.md` exists
2. Count total runs
3. Find the most recent run date
4. Check for any `❌ FAILED` entries in the last 5 runs
5. Check for any unresolved `SKILL FAILURE ALERT` entries

Build a table:
```
| Skill | Last Run | Total Runs | Recent Failures | Status |
|-------|----------|------------|-----------------|--------|
```

Flag any skill where:
- Last run > 3 days ago (for daily skills) → 🔴 STALE
- Last run > 7 days ago (for weekly skills) → 🔴 STALE
- 2+ failures in last 5 runs → 🟡 DEGRADED
- No run-log.md exists → ⚪ NEVER RUN

---

## Phase 2: Scheduled Task Health

Check each task in the Cowork Scheduled sidebar against its expected cadence:

| Task | Expected Cadence | Check |
|------|-----------------|-------|
| morning-briefing | Weekdays 6:00 AM | Last entry in messages.md from this task |
| reply-classifier | Weekdays 5x/day | Check warm-leads.md update timestamp |
| stage-monitor | Weekdays 6:20 AM | Check contact-lifecycle.md update timestamp |
| auto-prospect-enroll | Mon/Wed/Fri 6:30 AM | Check messages.md for [DONE] entries |
| trigger-monitor | Mon/Wed/Fri 6:10 AM | Check messages.md for trigger entries |
| weekly-analytics | Fridays 5:00 PM | Check analytics DB last write |
| post-send-verifier | Weekdays noon + 5:30 PM | Check messages.md |
| warm-lead-reengagement | Monthly 1st | Check warm-leads.md for reengagement entries |
| objection-trend-digest | Fridays 5:15 PM | Check analytics/reports/ for digest file |

Surface any tasks that appear to have stopped running or are producing no output.

---

## Phase 3: Performance Correlation Analysis

Read `analytics/outreach.db` using Python/SQLite. Run these queries:

### 3a. MQS Score vs Reply Rate
```sql
-- If MQS is stored in sends table:
SELECT
  CASE
    WHEN mqs_score >= 11 THEN 'High (11-12)'
    WHEN mqs_score >= 9 THEN 'Mid (9-10)'
    ELSE 'Low (<9)'
  END as mqs_band,
  COUNT(*) as sends,
  SUM(CASE WHEN replied = 1 THEN 1 ELSE 0 END) as replies,
  ROUND(100.0 * SUM(CASE WHEN replied = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) as reply_rate
FROM outreach_sends
GROUP BY mqs_band
```

### 3b. Persona Reply Rate
```sql
SELECT persona_title,
  COUNT(*) as sends,
  ROUND(100.0 * SUM(replied) / COUNT(*), 1) as reply_rate
FROM outreach_sends
GROUP BY persona_title
ORDER BY reply_rate DESC
```

### 3c. Proof Point Performance
```sql
SELECT proof_point_used,
  COUNT(*) as sends,
  ROUND(100.0 * SUM(replied) / COUNT(*), 1) as reply_rate
FROM outreach_sends
WHERE proof_point_used IS NOT NULL
GROUP BY proof_point_used
ORDER BY reply_rate DESC
```

### 3d. Vertical Performance
```sql
SELECT vertical,
  COUNT(*) as sends,
  ROUND(100.0 * SUM(replied) / COUNT(*), 1) as reply_rate
FROM outreach_sends
GROUP BY vertical
ORDER BY reply_rate DESC
```

### 3e. Bounce Rate by Domain Pattern
```sql
SELECT
  SUBSTR(email, INSTR(email,'@')+1) as domain,
  COUNT(*) as sends,
  SUM(bounced) as bounces,
  ROUND(100.0 * SUM(bounced) / COUNT(*), 1) as bounce_rate
FROM outreach_sends
GROUP BY domain
HAVING bounces >= 2
ORDER BY bounce_rate DESC
```

If the DB doesn't have the needed columns, note what's missing and recommend adding those fields to the weekly-analytics sync.

---

## Phase 4: Call Performance Analysis

Read `memory/call-log.md`. Parse all entries and compute:

1. **Connect Rate** = Connects / Dials (target: >15%)
2. **Meeting Rate** = Meetings Booked / Connects (target: >10%)
3. **Dials per Day** (average over last 30 days)
4. **Best calling time** — which hours/days have highest connect rates
5. **Call-to-pipeline ratio** — calls that directly attributed to a meeting booked

Format the call-log.md expected structure (for parsing):
```markdown
## [DATE]
- Dials: [N]
- Connects: [N]
- Meetings Booked: [N]
- Notes: [any key context]
```

If the call log is sparse or missing data, note: "Call log has [N] entries covering [date range]. [N] entries missing dials/connects. Recommend filling daily for accurate analytics."

Output call performance summary:
```
CALL PERFORMANCE (last 30 days)
  Total dials: [N]
  Total connects: [N]
  Connect rate: [%] ([vs 15% target])
  Meetings from calls: [N]
  Meeting rate: [%]
  Top time to call: [day/hour if determinable]
```

---

## Phase 5: Data Freshness Check

1. **MASTER_SENT_LIST.csv** — count rows, compare to last known count from handoff.md
2. **tam-accounts-mar26.csv** — confirm it exists and was last touched when expected
3. **analytics/outreach.db** — check `SELECT MAX(send_date) FROM outreach_sends` — should be within 7 days
4. **memory/warm-leads.md** — check last modification date — should be within 48 hours if active
5. **memory/session/handoff.md** — check `Last Updated` line — should be current session or yesterday

Flag anything stale.

---

## Phase 6: System Recommendations

Based on findings from all phases, generate 3-5 prioritized recommendations:

**Format:**
```
🔴 CRITICAL — [action needed, specific]
🟡 IMPROVE — [optimization, with expected impact]
🟢 INSIGHT — [data-backed finding to leverage]
```

Examples:
- 🔴 CRITICAL — `reply-classifier` has not run in 4 days. Check scheduled task status.
- 🟡 IMPROVE — FinTech contacts reply at 34% vs 18% overall. Prioritize FinTech accounts in next batch.
- 🟢 INSIGHT — MQS 11-12 drafts reply at 2.4x rate of MQS 9-10. The QA gate is working.

---

## Output

Write to `diagnostics/system-health-report.md`:

```markdown
# System Health Report — [DATE]
**Run #[N]** | Generated by: system-diagnostics skill

## Skill Health
[table from Phase 1]

## Scheduled Task Status
[findings from Phase 2]

## Performance Correlations
[tables from Phase 3]

## Call Performance
[summary from Phase 4]

## Data Freshness
[findings from Phase 5]

## Recommendations
[prioritized list from Phase 6]

---
*Next scheduled run: [date]*
```

Then append to `memory/session/messages.md`:
```
[timestamp] System Diagnostics: [INFO] Weekly health report complete.
[N] skills healthy, [N] stale, [N] degraded.
Top rec: [first critical/improve item].
Full report: diagnostics/system-health-report.md
```

---

## Self-Improvement Loop

Follows `skills/_shared/learning-loop.md`.

**Key metrics for run-log:**
```
- Skills audited: [N]
- Stale skills: [N]
- Degraded skills: [N]
- Correlations computed: [N]
- Call entries parsed: [N]
- Recommendations generated: [N]
- DB queries successful: [Y/N]
```

**Every 5th run:** Review if the DB queries are returning useful data. If columns are consistently NULL, propose adding them to the weekly-analytics sync via SKILL UPDATE PROPOSAL.

---

## Error Handling

- **DB not found / empty:** Note it, skip Phase 3, still run other phases
- **Call log sparse:** Run call analysis on available data, flag gaps
- **Skill run-log missing:** Mark as NEVER RUN in the health table
- **Messages.md write conflict:** Retry once after 5 seconds; if still locked, skip messages.md write (report is still written to diagnostics/)
