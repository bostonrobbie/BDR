# Daily Sequence Audit SOP
## BDR Outreach — Sequence Status Check
## Version: 1.1 | Created: March 6, 2026 | Last Updated: March 6, 2026

---

## PURPOSE

Run this process every morning (or start of BDR session) to get a clean, accurate picture of where each sequence stands before doing ANY outreach. Prevents duplicate sends, catches tracking gaps, and gives you a prioritized action list for the day.

**Estimated time:** 15–20 minutes with Claude in Cowork. Claude does 80% of the work.

---

## WHEN TO RUN

- **Every day before sending any emails or InMails**
- After any new batch of prospects is enrolled in a sequence
- After any Sales Navigator InMails are sent directly (to log them)
- After any bulk Sequence adds via Apollo API

---

## STEP 1: TELL CLAUDE TO READ THE REPO (1 min)

Say: *"Read the BDR repo and work folder for context"*

Claude will read:
- `workflow-notes.md` — rules, IDs, qualification checklist
- `sequence_status_report_[latest date].md` — last known status
- `prospect_master_tracker.md` — running prospect log
- `batch[N]_qualification_report.md` — latest batch report

This gives Claude the baseline before pulling live data.

---

## STEP 2: PULL LIVE SEQUENCE DATA FROM APOLLO (5 min)

Claude will navigate directly to each sequence's contacts page via Chrome:

| Sequence | Apollo URL |
|----------|-----------|
| Tier 1 Intent | `https://app.apollo.io/#/sequences/69a1b3564fa5fa001152eb66/contacts` |
| Q1 Priority Accounts | `https://app.apollo.io/#/sequences/69a05801fdd140001d3fc014/contacts` |
| AI Maturity Audit Campaign for QA | `https://app.apollo.io/#/sequences/6909f6b00f9bb2001d599d5e/contacts` |
| Q1 QA Outreach - US | *(navigate manually if needed)* |

For each sequence, Claude extracts:
- Total contacts
- Stage breakdown: New / Attempted to Contact / Connected / Finished / Bounced
- Step breakdown: How many at Step 1 vs Step 2 vs Step 3+
- Error contacts: "Reply to thread missing original sent email"
- NEW JOB flags (Apollo flags these automatically)
- Finished/Stopped contacts

**Critical distinction:**
- "New" at Step 1 = **outreach NOT sent** in this sequence
- "Attempted to Contact" at Step X = **NOT necessarily sent via this sequence** — stage can come from prior activity elsewhere
- "Active Step N" = currently at Step N, task is PENDING

---

## STEP 3: CHECK FOR DUAL-SEQUENCING VIOLATIONS (3 min)

Compare the contact lists across both active sequences.

Any contact appearing as **Active** in 2+ sequences simultaneously is a violation.

**How to check:**
- Claude cross-references the contact names from both sequence pages
- Flags any contact appearing in both Tier 1 Intent AND Q1 Priority Accounts (or any other active sequence) as "Active"

**Rule:** A contact can only be active in ONE sequence at a time.
- Exception: If one sequence is LinkedIn-only (Priority Accounts) and the other is email-only (Tier 1 Intent), this is a gray area but still not recommended — discuss with manager.

**How to fix:**
- Open the contact in Apollo
- Go to their Sequences tab
- Stop them from the LOWER priority sequence
- Default priority: Tier 1 Intent (email) > Q1 Priority Accounts (LinkedIn)

---

## STEP 4: CHECK SALES NAVIGATOR SENDS (2 min)

Any InMails sent DIRECTLY via LinkedIn Sales Navigator (not through Apollo tasks) create a tracking gap. If Rob sent any InMails outside of Apollo since the last audit:

1. List the contacts who were InMail'd via Sales Nav
2. In Apollo, go to each contact's profile
3. Add a **note** to their timeline: `"LinkedIn InMail sent via Sales Nav [DATE] — [subject/message summary]"`
4. Optionally: If the sequence step is a manual InMail task, open the task for that contact and click **Mark as Complete** (without sending) to advance the sequence

This keeps Apollo as the source of truth.

---

## STEP 5: CHECK GMAIL FOR ACTIVE REPLIES (2 min)

Any emails sent from `robert.gorham@testsigma.com` (Gmail, not Apollo) are not tracked in Apollo. Check Gmail for any replies from prospects that need follow-up.

Search in Gmail: `from:(@) after:[yesterday's date] in:inbox`

Log any active conversations in `prospect_master_tracker.md`.

---

## STEP 6: COMPILE THE DAY'S ACTION LIST (3 min)

Claude will generate a prioritized to-do list in this order:

| Priority | Task Type | Why |
|----------|-----------|-----|
| P0 | Fix dual-sequencing violations | Prevents spam/double outreach |
| P0 | Reply to active live conversations (e.g. Pallavi Sheshadri) | Hottest prospects go cold fast |
| P1 | Send Touch 1 to all "New / Step 1" contacts in Tier 1 Intent | Your primary email sequence |
| P2 | Fix "Reply to thread" errors (Step 2 blocked) | Contacts stalling out |
| P3 | Work Priority Accounts InMail task queue | LinkedIn outreach |
| P4 | Handle any NEW JOB flagged contacts | Stop them, find replacements |
| P5 | Inbound leads (e.g. Salesforce assignments) | Warm > cold |

---

## STEP 7: UPDATE TRACKER FILES (5 min)

After the audit, Claude updates:

1. **`sequence_status_report_[date].md`** — Overwrite with today's full findings
2. **`prospect_master_tracker.md`** — Add new contacts, update statuses for completed sends
3. **`email_outreach_tracker.csv`** — Log each send (date, contact, sequence, step, subject line, send type)

File naming convention: `sequence_status_report_MMMDD.md` (e.g. `sequence_status_report_mar6.md`)

---

## DAILY AUDIT CHECKLIST

Use this as a quick verbal checklist each morning:

```
□ Claude has read the BDR repo (workflow-notes, latest report, trackers)
□ Tier 1 Intent contacts page pulled — stage breakdown confirmed
□ Q1 Priority Accounts contacts page pulled — stage breakdown confirmed
□ AI Maturity Audit Campaign contacts page pulled — stage breakdown confirmed
□ Dual-sequencing violations checked and resolved (across all 3 sequences)
□ Sales Nav / Gmail sends from yesterday logged in Apollo (if any sent outside Apollo task queue)
□ Gmail checked for active replies
□ Engagement tracking updated in email_outreach_tracker.csv (Opened?, Replied?, Outcome Notes)
□ Today's prioritized action list generated
□ Tracker files updated
```

---

## KEY NUMBERS TO KNOW

### Tier 1 Intent Sequence
- **ID:** `69a1b3564fa5fa001152eb66`
- **Step 1:** Manual email (Touch 1) — must send via Apollo UI task queue
- **Step 2+:** Follow-up emails — same method
- **Expected send volume per week:** 5–15 new Touch 1s as new contacts added

### Q1 Priority Accounts Sequence
- **ID:** `69a05801fdd140001d3fc014`
- **Step 1:** Manual LinkedIn InMail — must complete via Apollo task queue (opens LinkedIn)
- **Step 2:** Manual LinkedIn InMail — same
- **Step 3:** Manual email — paste into Apollo UI
- **Step 4:** Phone call
- **Current status (March 6):** 285 contacts enrolled, **0 InMails sent** — task queue has never been executed
- **Expected send volume:** Target 10–20 InMails/day to work through 285-contact backlog

### Copy — AI Maturity Audit Campaign for QA Sequence
- **ID:** `6909f6b00f9bb2001d599d5e`
- **Step 1:** Email (personalized to QA/engineering pain points)
- **Current status (March 6):** 142 contacts, ~255 overdue tasks, 19 contacts emailed via Gmail outside Apollo (logged in CSV, Apollo notes pending)
- **Note:** Full contact-level audit not yet run — run same process as Tier 1 audit to get stage/step breakdown

---

## COMMON ISSUES AND FIXES

| Issue | What It Means | Fix |
|-------|--------------|-----|
| Contact is "New" at Step 1 | No outreach sent yet in this sequence | Send Touch 1 via Apollo task queue |
| "Reply to thread missing original sent email" | Apollo can't find the original email to thread the reply onto | Send Step 2 as fresh email; verify Step 1 was actually delivered |
| Contact is "Attempted to Contact" but at Step 1 | Their stage came from a DIFFERENT sequence or prior outreach | Check contact timeline in Apollo; if Step 1 was never sent in THIS sequence, send it |
| Contact appears in 2 active sequences | Dual-sequencing violation | Stop them from lower-priority sequence |
| "NEW JOB" flag on contact | Apollo detected a job change | Verify on LinkedIn; if confirmed, stop + find replacement |
| Sales Nav InMail not in Apollo | Sent outside of Apollo | Add note to Apollo contact; optionally mark task complete |
| Contact bounced | Email address invalid | Mark Unqualified; find replacement or alternate email |

---

## WORKFLOW RULES (Non-Negotiable)

1. **ALL sequence emails must be sent through Apollo UI task queue** (not Gmail compose, not Gmail API)
2. **ALL LinkedIn InMails for sequences should be sent through Apollo task queue** (which links to LinkedIn) — NOT directly via Sales Nav without logging
3. **No contact in more than one active sequence at a time**
4. **Check the 9-point qualification checklist before adding any new contact**
5. **Log every send in `email_outreach_tracker.csv`** (date, name, company, step, subject, send type)

---

## SOP REVISION LOG

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | March 6, 2026 | Initial SOP created after audit revealed Q1 Priority Accounts had 0 sends logged despite 285 contacts enrolled; Sales Nav/Apollo tracking gap identified |
| 1.1 | March 6, 2026 | AI Maturity Audit Campaign for QA added to sequence list (ID: 6909f6b00f9bb2001d599d5e, 142 contacts); KEY NUMBERS section updated; daily checklist updated to include AI Maturity Audit + engagement tracking step |

---

## APOLLO-ONLY RULE (Non-Negotiable)

**ALL sequence emails must go through Apollo UI task queue ONLY.**

- **No Gmail compose.** Emails sent from Gmail are not tracked in the sequence and contacts appear stuck.
- **No API direct send.** Use Apollo's browser UI task queue for all outreach.
- **No Sales Navigator direct send (without Apollo logging).** All LinkedIn InMails for sequences must go through Apollo's task queue, which links to LinkedIn. If you send via Sales Nav directly, you create a tracking gap.

**If any send happens outside Apollo:**
1. Immediately log it as a note on the Apollo contact record with date, platform (Gmail/Sales Nav), and message summary
2. Mark the step task as Complete manually in the sequence (to advance the contact to the next step)
3. Do NOT double-send via Apollo for that contact in that step

**Source of truth for all outreach is Apollo — period.** Every send, every step, every stage advancement must be visible in the Apollo sequence dashboard. No exceptions.

---

*This SOP is maintained in: `/Work/daily_sequence_audit_sop.md`*
*Master SOP cross-reference: `Tier1_Intent_Sequence_SOP_MASTER.md` and `outreach_email_sop.md`*
