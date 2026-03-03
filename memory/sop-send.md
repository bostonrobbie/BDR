# LinkedIn Sales Navigator Live Send SOP

## Hard Rules
- NEVER click Send until Rob replies APPROVE SEND in chat
- If anything looks off, STOP and report with screenshot + fix suggestion
- One prospect at a time. Complete full workflow before next.

## Inputs Required (from HTML tracker)
Full name, Title, Company, Sales Nav URL, LinkedIn URL (optional), Apollo ID/email, Message text, Subject line, Research notes.

## 10-Step Procedure

### Step 1: Load Prospect Record
Extract from HTML tracker. Confirm all required fields present. If missing, STOP and ask Rob.

### Step 2: Navigate to Sales Nav Profile
Open URL, wait for full load. Screenshot showing name, title, company, location.

### Step 3: Pre-Flight Identity Check
| Check | Criteria |
|-------|----------|
| Name match | Matches tracker (variants like middle initial OK) |
| Title match | Matches within reason (note promotions) |
| Company match | Matches (note changes) |
| Target fit | Role plausibly impacts QA/testing |
| InMail access | "Message" button available |
| No prior contact | No "Messaged:" or "Viewed:" indicator |
If ANY FAILS: STOP, output issue + screenshot + fix.

### Step 4: Open InMail Composer
Click "Message" button. Wait for modal. Enter subject line if field exists.

### Step 5: Compose Message
- Max 2-3 sentences per paragraph, 1 blank line between each
- No bullets unless 2 or fewer. No emojis.
- Under 600 characters when possible
- Paste message EXACTLY from tracker. Verify line breaks preserved.

### Step 6: Quality Check
- [ ] No placeholders remain
- [ ] Name/company spelling matches profile
- [ ] CTA present ("what day works")
- [ ] No extra spaces or jumbled text
- [ ] Exactly 2 question marks
- [ ] Subject line present (if field exists)

### Step 7: Present for Approval (NO SEND)
Show Rob: pre-flight results, discrepancies, final message, screenshot.
Say: "Reply APPROVE SEND to send, or reply EDIT with changes."
**STOP and wait.**

### Step 8: Send (Only After APPROVE SEND)
Click Send. Wait for confirmation UI. Screenshot confirming send.

### Step 9: Post-Send Logging
Update tracker: Status=Touch 1 Sent, dateSent, subjectUsed, conversationUrl, preFlightResult, nextStepDue (+5 days).

### Step 10: Close & Prepare Next
Close InMail window. Navigate back to search. Confirm: "Prospect #X complete. Ready for #[X+1]."

## Error Handling
| Issue | Action |
|-------|--------|
| Profile not found | STOP, ask for alternate URL |
| InMail not available | STOP, suggest connection request |
| Composer won't load | Refresh, retry once, then STOP |
| "Messaged" indicator | STOP, flag as already contacted |
| Title/company mismatch | Note change, present to Rob |
| Session expired | STOP, ask Rob to re-authenticate |

## LinkedIn Safety & Compliance
### Pacing Limits
| Activity | Daily Max | Weekly Max |
|----------|-----------|------------|
| InMails | 8 | 20 |
| Profile views | 100 | 500 |
| Connection requests | 15 | 80 |
| Total messages | 15 | 60 |

### Session Rules
- Space sends 2-3 min apart. 10-min break every 10 sends.
- Send 9 AM-5 PM only (12-1 PM ideal). Never back-to-back days at same time.
- If "unusual activity" warning: STOP, pause 72 hrs, reduce volume 50%.

### Known Person / Past Coworker Check (Module A1)
If 1st-degree connection: check shared history (mabl or any past employer). If real relationship: DO NOT CONTACT.

### Already Messaged Check (Module A2)
Check Sales Nav "Messaged:" indicator. Check InMail composer for existing thread. **CRITICAL: Also check linkedin.com/messaging search** (catches messages Sales Nav misses, especially from mabl era 2021-2023).
