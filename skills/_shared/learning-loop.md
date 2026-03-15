# Shared: Self-Improvement Learning Loop

**Version:** 1.0 — Initialized Mar 14, 2026
**Purpose:** Standard protocol applied to ALL scheduled skills. Every skill maintains its own run log and learned-patterns file. Over time, each skill reads its own history, extracts patterns, and proposes improvements — becoming more accurate and calibrated with each run.

---

## The Core Idea

Every skill runs the same three-phase learning loop:

1. **Before running:** Read accumulated knowledge from prior runs (`learned-patterns.md`)
2. **After running:** Log what happened (`run-log.md`)
3. **Every 5th run:** Review the log, extract patterns, update knowledge, propose SKILL.md improvements

This means skills get smarter over time without Rob having to manually tune them. If something keeps going wrong or keeps working unusually well, the skill notices and proposes a fix.

---

## File Structure (per skill)

```
skills/[skill-name]/
  SKILL.md              ← Core instructions (Rob-approved, only updated with permission)
  run-log.md            ← Auto-appended after every run
  learned-patterns.md   ← Auto-updated every 5th run
```

---

## Standard Run-Log Entry Format

Append this after EVERY run (success or failure):

```markdown
### Run #[N] — [YYYY-MM-DD HH:MM]
- **Result:** [1-2 sentence summary of what was found/done]
- **Key metrics:** [skill-specific counts — see each skill's section below]
- **Anomalies:** [anything unexpected, edge cases, data gaps, tool errors]
- **Adjustments made this run:** [any real-time judgment calls that deviated from SKILL.md]
- **Output quality:** [Accurate / Mostly accurate / Needs calibration / Failed]
```

**If the run failed (tool error, missing file, etc.):**
```markdown
### Run #[N] — [YYYY-MM-DD HH:MM] ❌ FAILED
- **Error:** [what went wrong]
- **Impact:** [what was skipped or incomplete]
- **Recovery:** [what to do next run]
```

---

## Skill-Specific Key Metrics

Each skill logs these additional metrics in its run log entry:

### reply-classifier
```
- Emails scanned: [N]
- New replies found: [N]
- P0/P1 (warm): [N] | P2/P3 (objection): [N] | P4 (ghost): [N]
- New warm leads added to warm-leads.md: [N]
```

### stage-monitor
```
- T2 tasks due today/upcoming: [N contacts, batch list]
- T3 tasks due today/upcoming: [N contacts, batch list]
- Bounces detected: [N]
- Pipeline contacts active: [N]
```

### auto-prospect-enroll
```
- Accounts scanned: [N]
- Contacts found: [N]
- Compliance gate: [N passed / N failed — top fail reason]
- MQS gate: [N passed / N failed — avg score]
- Enrolled: [N]
- TAM health: [N uncontacted Factor/HIGH remaining]
```

### trigger-monitor
```
- Accounts scanned: [N]
- Triggers found: [N] — breakdown: [hiring/N, funding/N, leadership/N]
- HOT accounts flagged: [N]
```

### morning-briefing
```
- Overnight replies: [N]
- Calendar events today: [N prospect meetings]
- T2/T3 due: [N]
- Work queue items: [N pending]
```

### weekly-analytics
```
- Sends synced to DB: [N new rows]
- Reply rate this week: [%]
- Total pipeline: [N active contacts]
- DB write: [success/error]
```

### warm-lead-reengagement
```
- P2/P3 contacts scanned: [N]
- OVERDUE (re-engage now): [N]
- DUE THIS WEEK: [N]
- DNC filtered: [N]
```

### tam-freshness-check
```
- TAM accounts loaded: [N]
- Uncontacted remaining: [N]
- Net-new candidates found: [N] (HOT: [N], WARM: [N])
- Stale accounts flagged: [N]
- Apollo credits used: [N]
```

### post-send-verifier (noon + eod)
```
- Expected sends: [N]
- Confirmed in Gmail: [N]
- Unconfirmed: [N]
- Unexpected: [N]
```

### objection-trend-digest
```
- Replies processed: [N]
- Top objection: [type] ([N])
- Flags raised: [list or "none"]
- Recommendations generated: [N]
```

### batch-dashboard / analytics-engine
```
- Batches summarized: [N]
- Data freshness: [last send date in DB]
```

---

## Pattern Review Protocol (Every 5th Run)

### Step 1 — Read Last 5 Run Log Entries
Count total runs in `run-log.md`. If run N is a multiple of 5: trigger the pattern review.

### Step 2 — Extract Patterns
Look for:
- **Recurring anomalies:** Same edge case appearing 3+ times
- **Consistent adjustments:** Same judgment call made 3+ times (means SKILL.md needs updating)
- **Metric drift:** Key numbers consistently above or below expected benchmarks
- **Tool failures:** Same tool failing repeatedly (means the skill needs a fallback)
- **False positives:** Contacts/accounts surfaced that Rob consistently ignores (means criteria need tightening)

### Step 3 — Update learned-patterns.md

Overwrite (don't append) `learned-patterns.md` with the latest version:

```markdown
# Learned Patterns — [Skill Name]

**Last updated:** [DATE] after Run #[N]
**Runs analyzed:** [N total]

## Active Calibration Adjustments
(Apply these at the START of every run)
- [adjustment]: [why / when to apply]

## Known Edge Cases
- [scenario]: [how to handle]

## Consistent Findings
- [pattern]: [what it means]

## Metric Benchmarks (calibrated from actual runs)
- [metric]: expected [range], actual avg [X]

## Proposed SKILL.md Updates
(Pending Rob approval — do NOT apply without explicit OK)
- [date]: [proposed change] | Reason: [why] | Seen: [N/5 runs]
```

### Step 4 — Propose SKILL.md Updates (if warranted)

If a pattern appears in 4 or more of the last 5 runs, write a proposal to `memory/session/messages.md`:

```markdown
## SKILL UPDATE PROPOSAL — [skill-name] — [DATE]

**Trigger:** Pattern appeared in [N]/5 recent runs
**Proposed change:** [specific edit to SKILL.md]
**Reason:** [what kept happening and why this change would fix it]
**Confidence:** [High / Medium]
**Action:** Reply "approve skill update [skill-name]" to apply, or ignore to defer.
```

Rob reviews proposals at his discretion. Nothing changes in SKILL.md until Rob approves.

---

## Failure Recovery

If a skill fails mid-run:
1. Log the failure in `run-log.md` with `❌ FAILED` marker
2. Note the recovery action in the log
3. On next run: read the failure log entry first and attempt the recovery action before proceeding normally
4. After 3 consecutive failures: write a `## SKILL FAILURE ALERT — [skill-name]` to `memory/session/messages.md` for Rob

---

## Privacy / Safety Rules

- `run-log.md` and `learned-patterns.md` are internal skill memory only — never shared externally
- Never log email body content in run logs — subjects and counts only
- Never log prospect personal data beyond name + company in run logs
- If a learned pattern would cause the skill to take a new action type it wasn't originally designed for: flag as a SKILL UPDATE PROPOSAL instead of just doing it
