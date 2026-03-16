# LinkedIn Sales Navigator Live Send SOP

## Hard Rules
- NEVER click Send until Rob replies APPROVE SEND in chat
- If anything looks off, STOP and report with screenshot + fix suggestion
- One prospect at a time. Complete full workflow before next.
- NEVER finalize a new batch without running the pre-batch dedup check (see below)
- NEVER end a session without logging all sends in pipeline-state.md in the same session

## Pre-Batch Build Checklist (MANDATORY before any new batch is finalized)

Run these checks BEFORE prospects are added to a new batch tracker file. Do not build the batch first and check after.

### Step 0: Account Source Validation ⛔ (MANDATORY — runs before everything else)
Verify every prospect's company is in one of the two authorized account lists:
- **Factor Accounts** (38 accounts): `memory/target-accounts.md`
- **TAM Accounts** (312 accounts): `/Work/tam-accounts-mar26.csv`

If the company is NOT in either list: **remove immediately.** Do not continue checking that prospect. No exceptions without Rob's explicit written approval. This step runs before DNC, before dedup, before any other check — a prospect from an unauthorized company never gets further in the pipeline.

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

---

---

## Apollo Task Queue Send — TAM Outbound T1 (Sequence Step 1)

Use this procedure when sending T1 emails via the Apollo sequence task queue ("Send Now" flow). This is the standard method for all TAM Outbound Wave sends.

### Hard Rules (from INC-007 + INC-008 — NON-NEGOTIABLE)
- **NEVER use Quill setText() JS injection** for task queue sends. Use clipboard paste only.
- **ALWAYS run JS body verification** before clicking Send Now — every single send, no exceptions.
- **"Changes saved" toast does NOT confirm body was set.** It only confirms subject was saved.
- **ALWAYS zoom-screenshot the body area** after paste to visually confirm real content.
- The placeholder text is: `"Placeholder - replace with personalized email before sending."` — if you see these words anywhere, STOP.

### Step-by-Step Flow

**1. Load the wave3_drafts.json entry for the current contact**
Match by name/email. Confirm subject and body are loaded into working memory before opening Apollo.

**2. Open the task in Apollo**
Navigate to: `https://app.apollo.io/#/sequences/69afff8dc8897c0019b78c7e/tasks?emailerCampaignIds[]=69afff8dc8897c0019b78c7e&emailerStepId=69afffcc6dc86e000d692314&sortBy[]=task_due_at.asc`
Click the task row for the current contact.

**3. Edit subject line**
Triple-click the Subject field → type exact subject from wave3_drafts.json. Do not press Enter.

**4. Set clipboard and focus body**
```
// 1. Set Windows clipboard via MCP (before touching the body editor):
Clipboard.set(text = [full email body from wave3_drafts.json])
// 2. Click body editor to focus — use coordinate (1035, 540):
left_click at (1035, 540)
// 3. Wait 0.5s
// 4. Ctrl+A to select all existing content
key "ctrl+a"
// 5. Ctrl+V to paste
key "ctrl+v"
```

**5. ⛔ MANDATORY JS BODY VERIFICATION (runs before every Send Now — no exceptions)**
Execute this JavaScript:
```javascript
document.querySelector('.ql-editor').innerText.trim().slice(0, 80)
```
**Expected:** Starts with `Hi [FirstName],`
**Failure:** Contains `Placeholder` → STOP immediately. Do NOT click Send Now. Re-focus body and re-paste (try clicking at [1035, 480] instead). Verify again.

**6. Zoom-screenshot body area**
```
zoom region: [860, 380, 1215, 500]
```
Confirm: real personalized sentence is visible. NOT placeholder text. Log this as "body verified ✓".

**7. Send Now**
Only after Steps 5 AND 6 both confirm real content. Use `find "Send Now button"` → left_click ref.

**8. Confirm advance**
Apollo auto-advances to next task or shows success. Take a screenshot to confirm send completed.

**9. Log immediately**
Update batch tracker + session notes before moving to the next contact.

### Paragraph Spacing Standard (applies to all sent emails)
Every email body must have a blank line between each paragraph. No walls of text. This is verified as part of the zoom screenshot check in Step 6 — if paragraphs are visually crammed together, STOP and fix before sending.

### Verification Failure Protocol (before send)
If JS body check returns placeholder text:
1. Do NOT click Send Now under any circumstances
2. Close the task modal (press Escape or click X)
3. Re-open the task from the task list
4. Repeat Steps 3-6
5. If paste fails 3 times: STOP session, report to Rob with screenshot

---

## Placeholder Send Recovery Protocol (INC-007 / INC-008)

Use this if a placeholder email was already sent to a prospect. Confirmed via Gmail sent folder — body shows "Placeholder - replace with personalized email before sending."

### Recognition
- Check Gmail sent folder after every send session
- Placeholder body starts with: `"Placeholder - replace with personalized email before sending."`
- If found: STOP all further sends. Log the affected contacts immediately. Report to Rob.

### Recovery Email Template
Send as a **reply to the original placeholder thread** in Gmail (not a new email).

**Opener (always use this exact format — no variations):**
> [FirstName], I just sent my draft a few moments ago, I was trying to get ahead of my message before lunch. Here's what I actually meant to say:

**Body:** The full personalized email from wave3_drafts.json — BUT strip the leading "Hi [FirstName]," line since the opener already addresses them. Preserve all paragraph spacing (blank line between each paragraph).

**No em dashes anywhere.** Replace any em dash with a comma.

**Full recovery email structure:**
```
[FirstName], I just sent my draft a few moments ago, I was trying to get ahead
of my message before lunch. Here's what I actually meant to say:

[Paragraph 1 — problem/hook]

[Paragraph 2 — social proof]

[Paragraph 3 — reason for reaching out + CTA question]

Rob Gorham | Testsigma
We have yet to be properly introduced. I work with [persona descriptor] at [vertical] companies.
```

### Steps
1. Pull the correct body from `wave3_drafts.json` for the affected contact
2. Draft the recovery email using the template above
3. **Present to Rob for APPROVE SEND** — never send without explicit approval
4. After approval: open Gmail, find the original placeholder thread, reply with the recovery email
5. Screenshot the sent reply as confirmation
6. Update the batch tracker: mark as "T1 Sent [date] (recovery)" — T2 eligible date resets to +4 days from recovery send
7. Log in incidents.md under the relevant INC entry

---

## Gmail Sent Folder Monitor — Required During Every Email Send Session

Run this check at two points in every Apollo Task Queue send session:

### Check 1: Mid-session (after every 5 sends)
1. Open Gmail sent folder: search `in:sent newer_than:2h`
2. Scan the last 5 sent emails — preview text should show real personalized content
3. If ANY show "Placeholder - replace with personalized email before sending": **STOP ALL SENDS IMMEDIATELY**
4. Identify affected contacts, log them, and follow the Placeholder Send Recovery Protocol above
5. Fix the paste issue before resuming

### Check 2: End-of-session (mandatory — before closing Apollo)
1. Open Gmail sent folder: search `in:sent newer_than:4h`
2. Scan ALL emails sent in the session — preview text must show real content for every send
3. Log result in session notes: "Gmail sent audit: [N] sends verified clean" or flag any issues
4. If issues found: log immediately in incidents.md, draft recovery emails, present to Rob

### How to run the Gmail check efficiently
Use the Gmail MCP tool:
```
gmail_search_messages(q="in:sent newer_than:2h", maxResults=20)
```
Check the `snippet` field of each result — it shows the first ~100 chars of the email body. Real content will start with "Hi [Name]," — placeholder will show "Placeholder - replace with..."

**This check is non-negotiable.** Do not end a send session without completing Check 2.

---

## Apollo UI Manual Email Send (Touch 2)

Use this procedure when sending T2 emails via the Apollo contact page (not LinkedIn InMail). This is the standard method for B9/B10/B11 Touch 2 emails.

### Hard Rules
- ALWAYS send from **robert.gorham@testsigma.com** (not .net, not .in). Apollo's default is .net — you MUST change it every time.
- Subject and body are NEVER typed via keyboard into the compose panel — use the technical methods below (form_input for Subject, Quill API for body). Keyboard input goes to the wrong element.
- Compose panel closing after clicking Send Now = success indicator.

### Preflight (all 3 required before opening compose)
| Check | Criteria |
|-------|----------|
| Owner | Must show "Rob Gorham" in Record Details section |
| Sequence | Must be enrolled in "LinkedIn Outbound - Q1 Priority Accounts" with status Active |
| Email | Primary email must match the draft email |
If ANY fails: SKIP. Document the reason.

### Step-by-Step Flow

**1. Navigate to contact**
```
https://app.apollo.io/#/contacts/{contact_id}/sequences
```
Get contact_id from Apollo MCP: `apollo_contacts_search q_keywords="Name Company"`

**2. Preflight**
Verify Owner = Rob Gorham, sequence = LinkedIn Outbound - Q1 Priority Accounts (Active), email correct.

**3. Open compose**
Click the envelope icon in the top right toolbar. A "Write with AI" panel opens on the left, and a "Send email" panel opens on the right. If only "Write with AI" opens, click the tooltip button at ~(930, 58) to reveal the full compose panel.

**4. CRITICAL — Change From address**
Apollo's default From is `robert.gorham@testsigma.net`. You MUST change it:
- Click the From dropdown (at ~1113, 152)
- Select `robert.gorham@testsigma.com` (second option in the list)
- Confirm the From field and the email signature both show `@testsigma.com`

**5. Set Subject**
Use the `find` tool: `find "Subject field for email"` → get ref (e.g., ref_336).
Then: `form_input ref=ref_336 value="[subject line]"`
Do NOT click the subject field and type — keystrokes go to the wrong element.

**6. Set Body**
Use the Quill JS API (NOT typing or clipboard):
```javascript
const emailText = `[full email body text]`;
const editorEl = document.querySelector('.ql-editor');
const container = editorEl.closest('.ql-container');
const quill = container.__quill;
quill.setText(emailText);
quill.setSelection(quill.getLength(), 0);
'done';
```

**7. Verify before sending**
Take a screenshot. Confirm:
- From: robert.gorham@testsigma.com ✅
- To: correct prospect email ✅
- Subject: correct ✅
- Body: correct (all paragraphs, no truncation) ✅
- Signature: shows testsigma.com ✅

**8. Send Now**
Use `find "Send Now button"` → get ref. Then `left_click ref=ref_XXX`.
Confirm compose panel closes = email sent successfully.

**9. Post-send**
Log in pipeline-state.md Email Send History immediately. Do not defer.

### Common Errors & Fixes
| Issue | Fix |
|-------|-----|
| From shows .net after send | NEVER SEND — you must change it FIRST. If you notice after send, flag to Rob. |
| Keyboard input goes to AI panel | Do NOT type in Subject — use form_input with ref |
| "Write with AI" panel blocks compose | Click X on "Write with AI" or click "Send email" tooltip (~930, 58) |
| Contact not found via search | Search name only (drop company name) — company search often returns 0 results |
| Chrome extension disconnects | Use tabs_create_mcp → new tab → navigate apollo.io → switch_browser to reconnect |
| Page blank after navigate | Go to #/home first, then search |

## T3 LinkedIn Connection Request Send

Use this procedure when sending Touch 3 (Day 10 — LinkedIn connection request) for prospects in the LinkedIn Outbound - Q1 Priority Accounts sequence.

### Hard Rules
- Send Day 10 (±1 day) from T1 InMail date. Do NOT send T3 before Day 9.
- Never pitch in T3. Goal = get accepted (1st degree), not to close.
- Max 200-250 characters (under LinkedIn's 300-char hard limit).
- Do NOT reference T1/T2 messages explicitly ("I sent you an InMail" = awkward). A light topic callback is fine.
- Rob must give APPROVE SEND before any connection request is sent.

### Connection Note Templates (rotate to avoid repetition)
- "Hi [First], been following [Company]'s work in [relevant space] — thought it made sense to connect. Rob"
- "Hi [First], reached out about QA automation a couple weeks back. Either way, good to be connected. Rob"
- "Hi [First], [Company]'s [relevant initiative] caught my attention — would love to stay connected. Rob"
- "Hi [First], interested in what you're building at [Company] on the QA side. Happy to connect either way. Rob"

### Step-by-Step Send Procedure

**1. Navigate to prospect's LinkedIn profile**
Use the LinkedIn URL from the batch tracker (linkedin.com/in/...). Do NOT use Sales Navigator for this step — use standard LinkedIn.

**2. Check connection status**
Confirm they are still 2nd or 3rd degree (not already 1st degree from a prior connection). If already 1st degree: skip T3 (already connected), note as "Connected" in tracker.

**3. Click "Connect"**
Click the Connect button on their profile. If the button shows "Follow" instead: click the three-dot menu (•••) → "Connect."

**4. Add a note**
When the connection modal opens: click "Add a note" (do NOT click "Send without a note" — personalized notes have higher acceptance rates). Paste the approved connection note from the batch tracker. Confirm character count ≤ 250.

**5. Verify and send**
Screenshot the modal showing the note text before sending. Present to Rob with "Reply APPROVE SEND to send, or EDIT with changes."

**6. Post-send logging**
Update batch tracker: Status = T3 Sent, date sent. Log in pipeline-state.md. Note: once accepted, this contact becomes 1st degree — future DMs are FREE.

### Common Errors & Fixes
| Issue | Fix |
|-------|-----|
| "Connect" button missing | Check if already connected (1st degree). If 3rd degree with no mutual connections, may be limited. Note as "T3 blocked" and skip. |
| Can only "Follow" | Three-dot menu → Connect. If unavailable, prospect has restricted connections. Skip. |
| Character count > 250 | Trim note. Never exceed 250 chars (buffer under LinkedIn's 300 limit). |
| Note field doesn't appear | Click "Add a note" explicitly before typing. Do NOT send without note. |
| Profile not findable | Search by name on LinkedIn. If still not found, log as "T3 - profile unavailable." |

---

## Open Profile InMails (Free — No Credits Used)

Some LinkedIn users have "Open Profile" enabled (LinkedIn Premium subscribers who allow anyone to InMail them). These cost ZERO credits and have a separate, higher daily limit than credit InMails. This is one of the most underused volume levers in Sales Nav.

### How to Identify Open Profile Prospects

**In Sales Nav search:**
- Filter: "Premium LinkedIn member" checkbox (left panel under "Premium Filters")
- On individual profiles: look for the gold LinkedIn Premium badge (gold "in" icon) next to their name
- When you open the InMail composer for an Open Profile prospect: the composer will show "Send for free" or will NOT show "Use 1 of X credits" — that's the confirmation

**Not all Premium members have Open Profile enabled.** The composer is the only 100% reliable check — if it says free, it's free.

### Open Profile InMail Rules
- Daily target: **10-20 free InMails** (separate from the 8 credit InMails)
- Same message quality standards as credit InMails — same C2 structure, same MQS ≥ 9/12 requirement
- Same composer check (Module A2) required before sending
- Same APPROVE SEND rule — Rob must approve before any send
- Log separately in pipeline-state.md as "Open Profile InMail (free)" so credit tracking stays accurate

### Prioritizing Open Profiles in Batch Build
When building a batch, run two passes in Sales Nav:
1. **First pass:** Premium filter ON → fill Open Profile slots (these are free, so they don't affect credit budget)
2. **Second pass:** Premium filter OFF → fill remaining credit InMail slots from broader search

This maximizes the free sends before spending credits.

---

## Daily LinkedIn Activity Summary

| Activity | Daily Target | Credit Cost | Notes |
|----------|-------------|-------------|-------|
| Credit InMails | 8 | 1 per send | 2nd/3rd degree non-Open profiles |
| Open Profile InMails | 10-20 | FREE | Premium members with Open Profile enabled |
| Connection requests (with note) | 15 | FREE | T3 or net-new cold connect |
| Profile views | 50-100 | FREE | Generates inbound curiosity visits |
| Post comments/engagement | 5-10 | FREE | Pre-warm before InMail |
| **Total direct messages/day** | **~33-43** | | InMails + connection requests |
| **Total LinkedIn activities/day** | **~88-153** | | All of the above |

---

## LinkedIn Safety & Compliance
### Pacing Limits
| Activity | Daily Max | Weekly Max |
|----------|-----------|------------|
| Credit InMails | 8 | 20 |
| Open Profile InMails (free) | 20 | 80 |
| Profile views | 100 | 500 |
| Connection requests | 15 | 80 |
| Total direct messages | ~43 | ~180 |

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
