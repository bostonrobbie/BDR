# Skill: Post-Send Verifier

**Trigger:** Runs weekdays at 12:00 PM and 5:30 PM. Also callable on-demand after any send session.
**Purpose:** After Rob executes Apollo sends, this skill verifies that the emails actually landed in Gmail Sent. Catches silent Apollo failures, wrong-body sends, or missed sends before the next day's work begins.
**Output:** Appends a `## POST-SEND VERIFICATION` section to `memory/session/messages.md`.

---

## What This Skill Does

1. Reads the most recent `batch{N}_sends.json` file(s) to find who was approved to receive sends today
2. Checks `memory/pipeline-state.md` for any sends logged in today's session
3. Searches Gmail Sent for outbound emails from `robert.gorham@testsigma.com` sent today
4. Cross-matches expected vs. confirmed sends
5. Flags any discrepancies for Rob's review

---

## Phase 1: Determine Expected Sends

**Step 1a: Find today's batch sends JSON**

Look in `Work/` for any `batch{N}_sends.json` files modified today:
```bash
find /sessions/epic-laughing-ptolemy/mnt/Work/ -name "batch*_sends.json" -newer [today_midnight]
```

For each file found, extract:
- Contact name
- Company
- Subject line
- Approved send date (if present in JSON)

**Step 1b: Cross-check pipeline-state.md**

Read `memory/pipeline-state.md`.

Look for any entries from today marked as "sent" or "APPROVED SEND executed." Extract names + batch numbers.

**If no sends JSON found and no pipeline-state entries:** Write "No sends detected today" and exit cleanly. This is expected on non-send days.

---

## Phase 2: Gmail Sent Search

Use `gmail_search_messages` with query:
```
from:robert.gorham@testsigma.com after:[today] in:sent
```

**Note:** If Gmail MCP is connected to `rgorham369@gmail.com` (personal) rather than the work account, this search may return 0 results. In that case, note the limitation and skip to Phase 4 (manual verification prompt).

For each result returned:
- Extract: recipient email, subject line, send timestamp
- Note any threads (replies) that might be mixed in

---

## Phase 3: Cross-Match

Compare expected sends (Phase 1) against confirmed sends (Phase 2):

**Match logic:**
- Match by subject line substring (first 40 chars) OR by recipient domain
- Partial matches count — flag for review if only domain matches, not exact name

**Build three lists:**

| Status | Definition |
|--------|-----------|
| ✅ CONFIRMED | Contact found in both expected list and Gmail Sent |
| ⚠️ UNCONFIRMED | Contact in expected list but NOT found in Gmail Sent |
| ❓ UNEXPECTED | Email found in Gmail Sent but NOT in expected list |

---

## Phase 4: Anomaly Classification

For any UNCONFIRMED sends, attempt to classify:

| Cause | Signal | Recommended Action |
|-------|--------|-------------------|
| Send not executed yet | Batch JSON exists but pipeline-state has no "sent" entry | No action — send may be pending |
| Apollo silent failure | Pipeline-state says sent but no Gmail match | Re-queue the send, flag INC |
| Wrong Gmail account | Gmail MCP on personal account | Manual check required — Rob to verify in work Gmail |
| Gmail delay | Send timestamp within last 15 min | Re-run verifier in 15 min |
| Apollo scheduled (not immediate) | Subject to checking | Flag for Rob |

---

## Phase 5: Write to messages.md

Append the following to `memory/session/messages.md`:

```markdown
---
## POST-SEND VERIFICATION — [DATE] [TIME]

**Expected sends today:** [N]
**Confirmed in Gmail:** [N]
**Unconfirmed:** [N]
**Unexpected:** [N]

### ✅ Confirmed Sends ([N])
| Name | Company | Subject | Sent At |
|------|---------|---------|---------|

### ⚠️ UNCONFIRMED — Review Required ([N])
| Name | Company | Subject | Issue |
|------|---------|---------|-------|
| [Name] | [Co] | [Subject] | [Classification] |

### ❓ Unexpected Sends ([N])
| Recipient | Subject | Sent At | Note |
|-----------|---------|---------|------|

---
[All sends confirmed — no action needed.] OR [ACTION REQUIRED: [N] sends unconfirmed. See above.]
```

---

## Phase 6: Update pipeline-state.md (if discrepancy found)

If any UNCONFIRMED or UNEXPECTED sends are found:
- Add a note to `memory/pipeline-state.md` under today's date:
  ```
  ⚠️ POST-SEND VERIFICATION FLAG [DATE]: [N] unconfirmed sends — see messages.md for detail
  ```
- Do NOT modify any other pipeline-state entries

---

## Hard Rules

- NEVER re-send anything — this is a read-and-verify skill only
- If Gmail MCP returns an auth error or 0 results on work account search, clearly note "Gmail MCP may be connected to personal account — manual verification required" — do not assume sends failed
- If no batch JSON and no pipeline-state sends entry for today, write "No sends detected today — nothing to verify" and exit. This is normal on non-send days
- Do not read or surface email body content in the report — subject lines and recipient names only
- Run at 12 PM catches morning send sessions. Run at 5:30 PM catches afternoon sessions and serves as end-of-day final check

---

## Scheduled Task Config

```
Name: post-send-verifier
Schedule: Weekdays at 12:00 PM and 5:30 PM
Cron (noon): 0 12 * * 1-5
Cron (EOD): 30 17 * * 1-5
```

**Implementation note:** Register as two separate scheduled tasks — `post-send-verifier-noon` and `post-send-verifier-eod` — since each cron handles one time slot.

---

## Self-Improvement Loop

This skill maintains its own run log and learned-patterns file. Full protocol: `skills/_shared/learning-loop.md`

### Before Each Run
1. Read `skills/post-send-verifier/learned-patterns.md` if it exists — apply any documented calibration adjustments
2. Count entries in `skills/post-send-verifier/run-log.md` to determine current run number

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
3. Overwrite `skills/post-send-verifier/learned-patterns.md` with updated findings
4. If a pattern appears in 4+ of 5 runs: write a `## SKILL UPDATE PROPOSAL — post-send-verifier` entry to `memory/session/messages.md` for Rob's review

**Hard rule:** Never modify SKILL.md directly. Only propose updates via messages.md and wait for Rob's explicit approval.
