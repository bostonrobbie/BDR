# Playbook: Apollo Task Queue Sends

## When to Use
After contacts are enrolled in the TAM Outbound sequence and Rob has given APPROVE SEND. This is the process for executing the actual email sends through Apollo's manual task queue.

**Daily target:** 50-100 new contacts sent per session (25 minimum on light days). This is the primary pipeline-building activity each session.

---

## Prerequisites
1. Contacts enrolled in TAM Outbound sequence (Step 1, active status)
2. Rob has given explicit **APPROVE SEND** for this batch (content gate — required before touching Apollo)
3. Batch tracker HTML file exists with all T1 email drafts (subject + body per contact)
4. You have browser access to Apollo (blue/work Chrome profile)

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

**Step 2b — Body insertion (execCommand method only):**
```javascript
const e = document.querySelector('.ql-editor');
e.focus();
document.execCommand('selectAll');
document.execCommand('insertText', false, `[JS_BODY string from tracker/lookup.py]`);
```

**Step 2c — INC-012 Readback Gate (MANDATORY before Send Now):**
```javascript
document.querySelector('.ql-editor').innerText.trim().slice(0, 120)
```
Verify output matches the approved body for this contact. Present screenshot of body area to Rob.

**Step 2d — QA CHECK checklist:**
- [ ] Subject has contact's first name and correct company/topic?
- [ ] Body mentions their company by name?
- [ ] Body has a specific proof point with numbers?
- [ ] No placeholder text ([COMPANY], {name}, etc.)?
- [ ] Word count correct (75-99 for T1, 50-70 for T2)?
- [ ] Readback matches approved draft?

**Step 2e — Send Now click:**
- Find the Send Now button: `const btns = Array.from(document.querySelectorAll('button')); const sendNow = btns.find(b => b.textContent.trim() === 'Send Now');`
- Confirm `disabled=false` before clicking
- Click via ref (preferred) or coordinate
- Apollo auto-advances to next task — confirm by URL change and new contact header

**Step 2f — Post-send verification:**
- Check Gmail MCP within 60 seconds: `gmail_search_messages(q="subject:[key words] from:robert.gorham@testsigma.com")`
- If Gmail confirms sent: ✅ proceed to next task
- If Gmail shows nothing after 90s: flag and investigate before continuing

4. Apollo marks the task as complete and auto-advances the contact to Step 2

### Step 3: Update Tracker
After sending each email:
1. Update the contact's status badge in the tracker HTML: "Draft Ready" → "T1 Sent {date}"
2. If MASTER_SENT_LIST.csv hasn't been updated yet (it should be from enrollment), verify the row exists

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
| T1 | 1-24 hours after enrollment | 75-99 | "What day works to see how?" |
| T2 | Day 5 from T1 send | 50-70 | Engagement question |
| T3 | Day 10 from T1 send | N/A (LI connect request) | Connection request |
| T4-T6 | Day 15, 21, 28 | N/A (phone calls) | Call script |
| T7 | Day 35 | 40-60 | Breakup email |

---

*Last updated: 2026-03-13 (Session 34) — INC-012 mandatory two-gate protocol embedded as core send process. Subject correction pattern documented. Daily 50-100 target added. Consolidated from Sessions 11, 19-20, 22-24, 34.*
