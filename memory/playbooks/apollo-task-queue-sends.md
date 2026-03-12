# Playbook: Apollo Task Queue Sends

## When to Use
After contacts are enrolled in the TAM Outbound sequence and Rob has given APPROVE SEND. This is the process for executing the actual email sends through Apollo's manual task queue.

---

## Prerequisites
1. Contacts enrolled in TAM Outbound sequence (Step 1, active status)
2. Rob has given explicit APPROVE SEND for this batch
3. Batch tracker HTML file exists with all T1 email drafts (subject + body per contact)
4. You have browser access to Apollo (blue/work Chrome profile)

---

## Process

### Step 1: Open Apollo Tasks Tab
Navigate to Apollo > Tasks tab. Filter by:
- Sequence: "TAM Outbound - Rob Gorham"
- Status: Due / Overdue
- Type: Email (manual)

The tasks appear as a list of contacts with "Send Email" actions.

### Step 2: For Each Task
1. Click on the contact's task to open the email editor
2. Open the batch tracker HTML file in another tab
3. Find the matching contact card in the tracker
4. Copy the **Subject line** from the tracker → paste into Apollo's subject field
5. Copy the **Email body** from the tracker → paste into Apollo's body field
6. **QA CHECK before clicking Send:**
   - Subject has the contact's first name? Yes/No
   - Body mentions their company? Yes/No
   - Body has a specific proof point with numbers? Yes/No
   - No placeholder text like [COMPANY] or {name}? Yes/No
   - Word count looks right (75-99 for T1, 50-70 for T2)? Yes/No
7. Click **Send Now**
8. Apollo marks the task as complete and auto-advances the contact to Step 2

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
- T2 emails are shorter (50-70 words)
- T2 uses a DIFFERENT proof point from T1 (check tracker for T1 proof point)
- T2 uses an engagement question CTA (NOT "What day works")
- T2 subject: lighter tone, callback to T1 (e.g., "Quick follow-up" or "One more thought")

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

*Last updated: 2026-03-12 — consolidated from Sessions 11, 19-20, 22-24*
