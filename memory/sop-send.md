# LinkedIn Sales Navigator Live Send SOP

## Hard Rules
- NEVER click Send until Rob replies APPROVE SEND in chat
- If anything looks off, STOP and report with screenshot + fix suggestion
- One prospect at a time. Complete full workflow before next.
- NEVER finalize a new batch without running the pre-batch dedup check (see below)
- NEVER end a session without logging all sends in pipeline-state.md in the same session

## Pre-Batch Build Checklist (MANDATORY before any new batch is finalized)

Run these checks BEFORE prospects are added to a new batch tracker file. Do not build the batch first and check after.

### Step A: DNC Cross-Reference
Read CLAUDE.md → Do Not Contact List. Remove any name that appears there. Zero tolerance.

### Step B: Master Sent List Dedup
Cross-reference every prospect name in the new batch against `/Work/MASTER_SENT_LIST.csv`.
- Fuzzy match: normalize names (strip parentheticals, credentials, middle names), then compare.
- Any match = flag immediately. Remove from batch unless Rob explicitly approves a second send.
- If MASTER_SENT_LIST.csv doesn't exist or is stale: re-run `/sessions/practical-brave-goldberg/build_master_list.py` to regenerate it.

### Step C: Same-Company Check
Scan the batch for multiple people at the same company. Flag any company with 2+ prospects. Default rule: 1 person per company per batch. Resolve conflicts autonomously using the priority tiebreaker in `sop-outreach.md` → Same-Company Conflict Resolution. Document all deferrals. Only escalate to Rob if priority scores are identical AND both are the same persona tier.

### Step D: Batch File Naming
Name ALL batch files with actual send date and status:
- `outreach-batchN-sent-MMMDD.html` (e.g. `outreach-batch10-sent-mar7.html`)
- `outreach-batchN-draft-MMMDD.html` for pre-send drafts
- NEVER label a file "unsent" if it might get sent later. Rename it the day it goes out.

### Step E: Update MASTER_SENT_LIST.csv
After every send session: re-run `build_master_list.py` so the CSV stays current. Do this BEFORE ending the session.

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
| No prior contact | Composer check = blank "New message" (see Module A2). No "Messaged:" indicator. |
If ANY FAILS: STOP, output issue + screenshot + fix.

### Step 4: Open InMail Composer
Click "Message" button. Wait for modal. **Confirm this is a fresh "New message" (composer check from Module A2 should have already cleared this).** Enter subject line if field exists.

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

### Step 9: Post-Send Logging (SAME SESSION — do not defer)
Update tracker: Status=Touch 1 Sent, dateSent, subjectUsed, conversationUrl, preFlightResult, nextStepDue (+5 days).
**Also update pipeline-state.md Master Send Log and credits remaining before ending the session.**
**Also re-run build_master_list.py to update MASTER_SENT_LIST.csv.**
If the session ends before logging is complete, the next session starts by catching up the log — not by sending more.

### Step 10: Close & Prepare Next
Close InMail window. Navigate back to search. Confirm: "Prospect #X complete. Ready for #[X+1]."

## Error Handling
| Issue | Action |
|-------|--------|
| Profile not found | STOP, ask for alternate URL |
| InMail not available | STOP, suggest connection request |
| Composer won't load | Refresh, retry once, then STOP |
| "Messaged" indicator | STOP, flag as already contacted |
| Composer shows existing thread | STOP, flag as DUPLICATE. Log in batch tracker. Skip prospect. |
| Prospect not on Sales Nav | Mark UNVERIFIABLE. Cannot composer-check. Route to email via Apollo instead. |
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

**Gold Standard: Composer Check (mandatory for every prospect)**
The ONLY 100% reliable dedup method is opening the InMail composer for the prospect on Sales Nav. If the composer shows a blank "New message" with an empty Subject field, the prospect is clean. If it loads an existing conversation thread, they've already been contacted. This takes ~10 seconds and catches duplicates that BOTH inbox searches miss.

**Why this matters (INC-002, discovered 2026-03-03):**
Three Batch 9 prospects (Jennifer Tune, Sandy Paray, Bhavani Neerathilingam) had prior InMail/DM threads that were invisible to Sales Nav inbox search AND linkedin.com/messaging search. The composer was the only thing that surfaced them. LinkedIn's messaging search index lags behind actual sends, especially for messages sent in the last 1-7 days.

**Full A2 procedure (in order):**
1. **Composer Check (REQUIRED):** Search prospect on Sales Nav, click message icon. If "New message" with blank Subject = CLEAN. If existing thread loads = DUPLICATE. Close composer.
2. **Sales Nav indicator:** Check for "Messaged:" badge on profile (supplementary, not sufficient alone).
3. **linkedin.com/messaging search:** Search prospect's first name. Catches mabl-era messages (2021-2023) and older DMs that predate Sales Nav tracking. Supplementary to composer check.

**If prospect is not findable on Sales Nav:** Mark as UNVERIFIABLE for InMail. Consider email via Apollo as alternative channel. Do NOT send InMail without completing the composer check.

**Rule: Never skip the composer check.** Inbox searches are supplementary only.
