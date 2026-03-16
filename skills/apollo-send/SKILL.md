# Apollo Send — Skill

## Description
Executes the full Apollo task queue send loop for a batch, applying the INC-012 two-gate protocol on every contact. Runs preflight automatically; pauses at Gate 2 for Rob's per-send "send it" approval. Handles all 3 post-send verification patterns, all known Apollo edge cases, and runs end-of-session batch cleanup automatically.

This skill is the production execution engine for T1 sends. It replaced the ad-hoc send process starting Batch 9 (Session 37).

## Trigger
Use when:
- Rob has given **APPROVE SEND** (Gate 1) for a batch
- Contacts are enrolled in TAM Outbound sequence
- `batch{N}_sends.json` exists in `/sessions/epic-laughing-ptolemy/` (or can be generated via `skills/batch-json-builder/SKILL.md`)

## Prerequisites
- Gate 1 already granted: Rob has said "APPROVE SEND" for this batch
- `batch{N}_sends.json` file available (see Content Lookup below)
- Apollo Tasks tab accessible in blue/work Chrome profile
- Batch tracker HTML file identified (for post-session badge update)
- MASTER_SENT_LIST.csv accessible

---

## CRITICAL SAFETY RULES (INC-012 — NEVER skip)

1. **APPROVE SEND ≠ APPROVE CLICK.** Gate 1 (content approval) and Gate 2 (send click) are two separate gates. Gate 1 is given once at the start. Gate 2 is required before EVERY individual Send Now click.
2. **NEVER use Quill API injection** — no `dangerouslyPasteHTML`, `setText`, `setContents`. These disconnect from Apollo's send payload. Caused 3 wrong-body sends (INC-007, INC-008, INC-012). execCommand ONLY.
3. **Stage check before every send.** If Stage ≠ "New", STOP and ask Rob.
4. **Readback must match before Gate 2.** If the first 120 chars don't match the approved body, STOP. Do not click Send Now.
5. **DO NOT double-send.** Pattern C (sticky "1-1 of 1") is NORMAL — do not re-click Send Now. Verify with JS Task completed check instead.

---

## Phase 1: Setup

### Step 1.1 — Load the batch_sends.json
Confirm the JSON file exists and is valid:
```bash
python3 -c "import json; data=json.load(open('batch{N}_sends.json')); print(f'{len(data)} contacts loaded')"
```
If the file doesn't exist, run `skills/batch-json-builder/SKILL.md` first.

### Step 1.2 — Identify the send list
Determine which contacts still need to be sent (not yet sent this session). On session resume, check the session log to see who's already been completed this session.

### Step 1.3 — Open Apollo Tasks tab
Navigate to: Apollo > Tasks
- Filter: Sequence = "TAM Outbound - Rob Gorham"
- Filter: Status = Due / Overdue
- Filter: Type = Email (manual)

Take a screenshot of the task count to confirm how many tasks are queued.

### Step 1.4 — Initialize running log
Create a simple running list in memory:
```
Sent so far this session: 0
Remaining: {N}
```
Update this count after each confirmed send.

---

## Phase 2: Per-Contact Send Loop

Repeat Steps 2.1–2.8 for EACH contact. Go in order of the JSON file unless Rob specifies otherwise.

### Step 2.1 — Fetch contact content from JSON
```bash
python3 -c "import json; data=json.load(open('batch{N}_sends.json')); c=next(x for x in data if x['id']=={ID}); print('SUBJECT:', c['subject']); print('BODY:'); print(c['body'])"
```
Note the first name, subject line, and full approved body before touching Apollo.

### Step 2.2 — Search and open the task
- Click the Tasks breadcrumb to return to clean task list (ALWAYS do this — prevents search-field bug)
- Search for the contact by name in the Tasks search field
- Click their task to open the email editor

**Known issue:** If the search field doesn't respond to typing, you're still on the previous completed task page. Click the Tasks breadcrumb first, THEN search.

### Step 2.3 — Stage check (MANDATORY)
Verify the contact's Stage = "New" in the task panel.
- Stage = "New" → proceed
- Stage ≠ "New" → STOP. Tell Rob: "Stage check failed for [Name] — Stage shows [X]. Skip or investigate?"

Do not proceed past this check without confirmation.

### Step 2.4 — Fix the subject (REQUIRED every task)
Apollo always pre-fills a generic template subject ("Firstname's QA coverage at Company"). This is almost always wrong.
- Triple-click the subject field to select all
- Type the correct personalized subject from the JSON lookup
- Verify with JS:
```javascript
document.querySelector('input[placeholder="Type a subject for your email"]').value
```
Output must match the approved subject exactly.

### Step 2.5 — Inject body + readback (one JS call)
```javascript
const body = `[paste approved body from Step 2.1 — use backtick delimiters, preserve line breaks]`;
const editor = document.querySelector('.ql-editor');
editor.focus();
document.execCommand('selectAll');
document.execCommand('insertText', false, body);
editor.innerText.trim().slice(0, 120);
```
The return value is the readback. It **must** match the first 120 characters of the approved body. If it doesn't → STOP. Do not proceed.

**Important for multi-line bodies:** Use `\n` for line breaks within the backtick string, or paste the body as a single string. Do NOT split into multiple execCommand calls.

### Step 2.6 — QA Checklist (Gate 2 preflight)
Before presenting to Rob for Gate 2, verify all:
- [ ] Subject has contact's first name and correct company/topic?
- [ ] Body mentions their company by name?
- [ ] Body has a specific proof point with numbers?
- [ ] No placeholder text `[COMPANY]`, `{name}`, `[NAME]`, etc.?
- [ ] Word count correct (75-99 for T1)?
- [ ] Readback matches approved body opening?

If any check fails → fix it, re-run readback, then present.

### Step 2.7 — Gate 2: Present to Rob
Take a screenshot of the full compose panel (subject + body visible). Present:
- The readback string (first 120 chars)
- The screenshot

Say: **"[Name] at [Company] — readback matches. Subject: [subject]. Send it?"**

Wait for Rob's explicit "send it" / "looks good" / equivalent before clicking Send Now.

If Rob says anything other than approval (e.g., "hold on", "change the subject", "skip this one") → do NOT click Send Now. Address the issue first.

### Step 2.8 — Send + Verify (3 patterns)

Click Send Now. Then verify using whichever pattern applies:

**Pattern A — Clean confirm:**
URL returns to task list + count shows "0 of 0" → ✅ Sent. Move to next contact.

**Pattern B — "Changes saved" toast + empty list:**
Green "Changes saved" toast appears + email task count = 0 → ✅ Sent. Move to next contact.

**Pattern C — Sticky "1-1 of 1" (most common in large batches):**
Count stays at "1-1 of 1" after send — this is NORMAL, NOT a failed send. Do NOT click Send Now again.
- Click back into the task
- Run:
```javascript
!!([...document.querySelectorAll('button')].find(b => b.innerText.includes('Task completed')))
```
- `true` → ✅ Sent. Also confirm "Send Now" button is greyed out.
- `false` → something is wrong. Do NOT resend. Tell Rob.

**Gmail MCP fallback** (only if all 3 patterns are ambiguous):
```
Tool: gmail_search_messages
q: "from:robert.gorham@testsigma.com to:{contact_email} newer_than:5m"
```
Email present in Sent = confirmed send.

Update running count: "Sent so far: {N+1}"

---

## Phase 3: End-of-Session Cleanup

After all contacts in the batch have been sent (or you're stopping for the session):

### Step 3.1 — Final send count
State the total: "Completed {N} sends this session out of {total} in the batch."

If any contacts were skipped (stage issue, DNC, task not found), list them with reason.

### Step 3.2 — Batch tracker badge update (Python batch pass)
```python
import re
from pathlib import Path

tracker_path = "mnt/Work/{tracker_filename}.html"
content = Path(tracker_path).read_text()

# Replace all Draft Ready → T1 Sent {date}
content = content.replace(
    'status-badge status-draft">Draft Ready',
    f'status-badge status-sent">T1 Sent {send_date}'
)

# For DNC contacts: find their card section, replace only that badge
# For Not Enrolled contacts: find their card section, revert only that badge

# Verify distribution
from collections import Counter
badge_counts = Counter(re.findall(r'status-badge[^>]*>([^<]+)<', content))
print(badge_counts)
# Expected: {N_sent} × "T1 Sent {date}", {N_dnc} × "DNC - Skip", {N_not_enrolled} × "Not Enrolled"

Path(tracker_path).write_text(content)
```

Expected distribution must be: (total T1 sent) + (DNC) + (Not Enrolled) = total contacts in tracker.

### Step 3.3 — MASTER_SENT_LIST.csv verification
```bash
wc -l mnt/Work/MASTER_SENT_LIST.csv
```
Row count must match expected total (all prior sends + this batch's sends). If rows are missing, append the missing contacts now.

### Step 3.4 — Pipeline state update
Update `memory/pipeline-state.md`:
- New send date row: batch name, N sent, cumulative total
- Update "TAM Outbound unique contacts T1 sent" running total
- Update tracker table with new HTML file entry (if new batch)

### Step 3.5 — Handoff
Tell Rob:
- Total sent this session / batch total
- T2 window: Day 5 from today's send date (when T2 tasks appear in Apollo)
- Any skipped contacts and why
- MASTER_SENT_LIST row count

---

## Known Issues

| Issue | Description | Fix |
|-------|-------------|-----|
| Sticky "1-1 of 1" | Task count doesn't update after send | Normal — use JS Task completed check (Pattern C) |
| Search field unresponsive | Still on previous task page | Click Tasks breadcrumb → then search |
| Tasks not in queue | Apollo task generation delay (1-24h after enrollment) | Wait — contacts are enrolled, tasks will appear |
| Subject auto-populates wrong | Apollo always fills generic template subject | Triple-click + retype every time |
| Body too long for backtick | Very long bodies may need line-break handling | Use `\n` escaping or split into two consecutive execCommand calls |
| Wrong stage | Contact has been manually advanced or re-enrolled | Stop + ask Rob before sending |

---

## Timing Reference

| Batch | T1 Send Date | T2 Window (Day 5) | T3 Window (Day 10) |
|-------|-------------|-------------------|-------------------|
| Fill in at session time | | | |

---

*Created: 2026-03-14 (Session 37). Based on INC-012 protocol, Batch 8 (Session 34) and Batch 9 (Session 37) production runs. Prerequisite: `memory/playbooks/apollo-task-queue-sends.md` (reference) and `batch{N}_sends.json` (content source).*

---

## Self-Improvement Loop

This skill maintains its own run log and learned-patterns file. Full protocol: `skills/_shared/learning-loop.md`

### Before Each Run
1. Read `skills/apollo-send/learned-patterns.md` if it exists — apply any documented calibration adjustments
2. Count entries in `skills/apollo-send/run-log.md` to determine current run number

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
3. Overwrite `skills/apollo-send/learned-patterns.md` with updated findings
4. If a pattern appears in 4+ of 5 runs: write a `## SKILL UPDATE PROPOSAL — apollo-send` entry to `memory/session/messages.md` for Rob's review

**Hard rule:** Never modify SKILL.md directly. Only propose updates via messages.md and wait for Rob's explicit approval.
