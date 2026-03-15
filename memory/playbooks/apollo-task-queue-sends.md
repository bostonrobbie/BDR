# Playbook: Apollo Task Queue Sends

## When to Use
After contacts are enrolled in the TAM Outbound sequence and Rob has given APPROVE SEND. This is the process for executing the actual email sends through Apollo's manual task queue.

**Daily target:** 50-100 new contacts sent per session (25 minimum on light days). This is the primary pipeline-building activity each session.

---

## Prerequisites
1. Contacts enrolled in TAM Outbound sequence (Step 1, active status)
2. Rob has given explicit **APPROVE SEND** for this batch (content gate — required before touching Apollo)
3. Approved content accessible — either batch tracker HTML **or** a `batch{N}_sends.json` file (see Content Lookup below)
4. You have browser access to Apollo (blue/work Chrome profile)

## Content Lookup — batch_sends.json Pattern
For large batches (Batch 9+), a JSON file is the fastest way to retrieve approved body + subject per contact mid-send. Format: array of objects with `id`, `name`, `first`, `email`, `subject`, `body`.

**Python lookup (use this every send):**
```bash
python3 -c "import json; data=json.load(open('batch9_sends.json')); c=next(x for x in data if x['id']==N); print('SUBJECT:', c['subject']); print('BODY:'); print(c['body'])"
```
Replace `N` with the contact's integer ID. Run this BEFORE opening each task in Apollo.

---

## CRITICAL: Two-Gate Send Rule (INC-012)

**APPROVE SEND ≠ APPROVE CLICK.** These are two separate gates:
- **Gate 1 — Content approval:** Rob reviews drafts and says "APPROVE SEND" → content locked
- **Gate 2 — Send click approval:** Before every "Send Now" click, run readback verification + present screenshot → wait for Rob's "looks good" / "send it"

**NEVER use Quill API injection** (dangerouslyPasteHTML, setText, setContents). These methods disconnect from Apollo's send payload and have caused wrong-body sends 3 times (INC-007, INC-008, INC-012).

**Correct body insertion method:**
```javascript
const e = document.querySelector('.ql-editor');
e.focus();
document.execCommand('selectAll');
document.execCommand('insertText', false, `[body text here]`);
```

**Readback verification (run before every Send Now click):**
```javascript
document.querySelector('.ql-editor').innerText.trim().slice(0, 120)
```
Output must match the approved draft for that contact. If it doesn't match → STOP, do not click Send Now.

---

## Process

### Step 1: Open Apollo Tasks Tab
Navigate to Apollo > Tasks tab. Filter by:
- Sequence: "TAM Outbound - Rob Gorham"
- Status: Due / Overdue
- Type: Email (manual)

The tasks appear as a list of contacts with "Send Email" actions.

### Step 2: For Each Task — Full INC-012 Protocol

1. Click on the contact's task to open the email editor
2. Open the batch tracker HTML file in another tab
3. Find the matching contact card in the tracker (match by name)

**Step 2a — Subject correction (REQUIRED every task):**
Apollo pre-fills subjects as "Firstname's QA coverage at Company" from the sequence template. This is almost always wrong.
- Triple-click the subject field to select all
- Type the correct personalized subject from the tracker (e.g., "Sandip's integration coverage at Pathlock")
- Verify with JS: `document.querySelector('input[placeholder="Type a subject for your email"]').value`

**Step 2b — Body insertion + readback (one JS call, execCommand method only):**
```javascript
const body = `[approved body text — paste from batch_sends.json lookup]`;
const editor = document.querySelector('.ql-editor');
editor.focus();
document.execCommand('selectAll');
document.execCommand('insertText', false, body);
editor.innerText.trim().slice(0, 120);
```
The return value IS the readback — verify it matches the first 120 chars of the approved body. If it doesn't → STOP.

**Step 2c — INC-012 Readback Gate (MANDATORY before Send Now):**
The combined JS call above handles injection + readback in one step. The returned string must match the approved body opening. Present a full screenshot of subject + body area to verify visually before Send Now.

**Step 2d — QA CHECK checklist:**
- [ ] Subject has contact's first name and correct company/topic?
- [ ] Body mentions their company by name?
- [ ] Body has a specific proof point with numbers?
- [ ] No placeholder text ([COMPANY], {name}, etc.)?
- [ ] Word count correct (75-99 for T1, 50-70 for T2)?
- [ ] Readback matches approved draft?

**Step 2e — Send Now click:**
- Click the Send Now button (coordinate ~214, 777 in the compose panel, or find via screenshot)
- After clicking, Apollo returns to the task list URL

**Step 2f — Post-send verification (3 patterns — use whichever applies):**

**Pattern A — Clean confirm (cleanest):**
URL returns to task list + task count shows "0 of 0" = ✅ sent and no remaining tasks for this search.

**Pattern B — "Changes saved" toast + empty list:**
"Changes saved" green toast appears + Email tasks = 0 = ✅ sent. Most common for single-contact searches.

**Pattern C — Sticky "1-1 of 1" (MOST COMMON in large batches):**
URL returns to task list but count still shows "1-1 of 1" (does NOT update immediately).
**Do NOT resend.** Click back into the task and run:
```javascript
!!([...document.querySelectorAll('button')].find(b => b.innerText.includes('Task completed')))
```
`true` = task is complete ✅. Also look for "Task completed" greyed-out button at top of page and "Send Now" being disabled.

**Gmail MCP** is a fallback only — the above in-page checks are faster and more reliable. Use Gmail MCP only if all 3 patterns are ambiguous.

4. Contact's sequence advances to Step 2 in Apollo (happens server-side, not always visible immediately)

### Step 3: Update Tracker
**Do NOT update badge per-send during the session** — this is slow and error-prone mid-send flow.
Instead, do a single batch update at the end of the session using Python:

```python
# Replace all "Draft Ready" badges with "T1 Sent {date}" in one pass
content = content.replace(
    'status-badge status-draft">Draft Ready',
    'status-badge status-sent">T1 Sent Mar 14'
)
# Then for any DNC contacts: find their card section and replace with DNC badge
# Then for any Not Enrolled contacts: revert those back to "Not Enrolled"
# Final check: count badges to verify correct distribution
```

Full pattern in tamob-batch-20260313-2.html session notes. MASTER_SENT_LIST.csv should already have all rows from enrollment — verify `wc -l` matches expected count.

### Step 4: Verify All Sends
After completing all tasks:
1. Count how many you sent
2. Compare to how many were expected
3. If any tasks didn't appear, check the contact's sequence status via Apollo MCP:
```
Tool: apollo_contacts_search
Parameters:
  q_keywords: "{contact name}"
  per_page: 1
```
Check `contact_campaign_statuses` for `current_step_position` and `status`.

---

## Known Issues

### Sticky "1-1 of 1" after send — NORMAL BEHAVIOR (not an error)
**Cause:** Apollo's task list count does not always update immediately after a send. The URL returns to the task list but the count stays at "1-1 of 1" instead of dropping to "0 of 0".
**This is NOT a failed send.** It happens consistently across large batches.
**Fix:** Click back into the task → run `!!([...document.querySelectorAll('button')].find(b => b.innerText.includes('Task completed')))` → `true` confirms sent. Also check that "Send Now" is greyed out on the task page.
**DO NOT click Send Now again** — that would double-send.
**Example:** Confirmed in Batch 8 (55 contacts) and Batch 9 (44 contacts) — this is the standard behavior, not an exception. (Sessions 34, 37)

### Search field not updating after task completion
**Cause:** After completing a task, the URL may remain on the old task page when you try to search for the next contact. The search field is present but typing doesn't navigate.
**Fix:** Click the "Tasks" breadcrumb at the top left first to return to the clean task list, THEN search for the next contact. Never search from within a completed task page.

### Tasks not appearing in queue
**Cause:** Apollo has a delay between enrollment and task generation. Tasks can take 1-24 hours to surface.
**Fix:** Wait. Check back later in the session or next session. The contacts are enrolled, the tasks WILL appear.
**Example:** Wave 4 — 9 contacts had no tasks immediately after enrollment. All surfaced within 24 hours. (Session 24-25)

### Task shows but no email editor
**Cause:** The contact's email might be marked invalid or the sequence step configuration might have an issue.
**Fix:** Check the contact's email status in Apollo. If invalid, skip and note in tracker.

### Wrong email content after Send
**Cause:** You forgot to paste the custom draft, or pasted the wrong contact's email.
**Prevention:** QA CHECK in Step 2 above. Always verify first name + company match before clicking Send.
**Recovery:** Cannot unsend. Log the error and note in tracker.

---

## T2 Sends (Follow-Up)

Same process as T1, but:
- T2 tasks appear in Apollo at ~Day 5 from T1 send
- T2 emails are LONGER than T1: 140-190 words (Deep-Dive v4 formula per Part 7 of sop-tam-outbound.md)
- T2 uses a DIFFERENT proof point from T1 (check tracker for T1 proof point)
- T2 CTA is a 15-minute meeting ask ("Would 15 minutes make sense to walk through how [Customer] made that shift?") — NOT an engagement question
- T2 subject: "Re: [T1 subject]" when threading in Apollo
- BANNED in T2: "Circling back" / "Following up" / "One more angle worth adding"
- Full T2 formula: `memory/playbooks/t2-followup.md`

---

## Timing Reference

| Touch | When tasks appear | Word count | CTA style |
|-------|------------------|------------|-----------|
| T1 | 1-24 hours after enrollment | 75-99 | Engagement question ("What day works…") |
| T2 | Day 5 from T1 send | 140-190 | 15-min meeting ask ("Would 15 minutes make sense…") |
| T3 | Day 10 from T1 send | N/A (LI connect request) | Connection request |
| T4-T6 | Day 15, 21, 28 | N/A (phone calls) | Call script |
| T7 | Day 35 | 40-60 | Breakup email |

---

*Last updated: 2026-03-14 (Session 37) — batch_sends.json lookup pattern added. Sticky "1-1 of 1" documented as normal/expected behavior with JS Task completed check as primary verification. "Changes saved" toast + empty list added as Pattern B confirm. Per-send tracker update replaced with batch Python update at session end. T2 word count corrected to 140-190. Search field navigation bug documented. Gmail MCP demoted to fallback only. Prior: Session 34 — INC-012 protocol, subject correction, daily 50-100 target.*
