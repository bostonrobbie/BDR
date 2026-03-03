# Outreach Email SOP: End-to-End Repeatable Process
## Q1 Website Visitor - Tier 1 Intent Sequence
## Last Updated: March 1, 2026 (v2.0 — Apollo UI send standard)

---

## OVERVIEW

This SOP documents the full process for creating, quality checking, and sending personalized Touch 1 outreach emails to prospects in the Q1 Website Visitor - Tier 1 Intent Apollo sequence. The process is designed to be repeatable for any new batch of contacts added to the sequence.

**Send Account:** robert.gorham@testsigma.net (Apollo — this is the ONLY approved send method)
**Sequence ID:** 69a1b3564fa5fa001152eb66
**Sequence Steps:** 3 touches, all MANUAL email tasks (no auto sends)

> **⚠️ CRITICAL PROCESS CHANGE (March 1, 2026):** All emails are now sent exclusively through the Apollo UI task queue. Gmail drafts and Gmail API sends have been deprecated. Emails sent outside Apollo do not register in the sequence, break deliverability tracking, and create double-send risk. See Phase 4 below for the updated workflow.

---

## PHASE 1: IDENTIFY CONTACTS NEEDING TOUCH 1

### Step 1.1: Pull contacts from Apollo sequence
- Open Apollo sequence "Q1 Website Visitor - Tier 1 Intent"
- Filter contacts at Step 1 (those who have NOT yet received Touch 1)
- Export or note: Name, Title, Company, Email, Contact ID

### Step 1.2: Check Gmail for already sent emails
- Search Gmail (robert.gorham@testsigma.com) for recent sends with subject "Quick question"
- Cross reference against the Step 1 list to identify any already sent
- Remove duplicates from the to-send list

### Step 1.3: Identify exclusions
- Remove contacts who have changed jobs (stale data)
- Remove contacts already in other active sequences
- Remove contacts with known deliverability issues
- Document all exclusions with reasons in the tracker

---

## PHASE 2: ENRICH AND PERSONALIZE

### Step 2.1: Enrich contacts via Apollo
- Use Apollo People Enrichment API for each contact
- Collect: Full name, current title, company, verified email, LinkedIn URL
- Note any catchall domains (monitor deliverability)
- Note any unverified emails (higher bounce risk)

### Step 2.2: Research companies
- For each unique company, gather a 1-2 sentence description focused on:
  - What the company does (product/service)
  - Why test automation matters for their specific domain
  - Any industry specific compliance, scale, or complexity factors
- This company context powers the personalized middle paragraph

### Step 2.3: Draft personalized Touch 1 emails
- Use the Touch 1 template below
- Personalize the middle paragraph for each contact's company and role
- Each email should be 4-6 sentences in the body

**Touch 1 Template:**

```
Subject: Quick question, [First Name]

Hi [First Name],

Noticed some folks at [Company] have been exploring test automation solutions
lately and figured it might be worth a quick intro.

I'm Rob with Testsigma. We help engineering teams cut test maintenance by up to
80% with AI powered test automation that works across web, mobile, and API from
a single platform. [1-2 sentences connecting Testsigma value to their specific
company/role/industry challenges.]

Would it be worth a 15 minute call to see if there's a fit? Happy to share a
quick overview doc instead if that's easier.

Best,
Rob
```

---

## PHASE 3: QUALITY CHECKS

### Step 3.1: Automated quality scan
Run all drafts through the following checks:

| Check | Rule | Action if Fail |
|-------|------|----------------|
| Em dashes | ZERO em dashes (—) in email body text | Replace with commas, periods, or restructure sentence |
| Buzzwords | None of: synergy, leverage, cutting-edge, game-changer, revolutionary, disruptive, paradigm, holistic, robust, seamless, seamlessly, turnkey, best-in-class, world-class, next-gen, bleeding edge, innovative | Replace with plain language |
| Subject line | Must be exactly "Quick question, [First Name]" | Fix to match template |
| Intent signal | Body must contain website visitor intent reference (e.g., "exploring test automation solutions") | Add intent signal opening |
| CTA | Must contain low friction CTA (15 min call or overview doc) | Add CTA |
| Signature | Must end with "Best, Rob" | Fix signature |
| Length | 4-6 sentences in body | Trim or expand |

### Step 3.2: Manual spot check
- Read 5-10 random emails for tone, accuracy, and natural flow
- Verify company descriptions are accurate
- Confirm no copy paste errors between emails

### Step 3.3: Fix and re-scan
- Fix any failures identified in 3.1
- Re-run automated scan to confirm 100% pass rate
- Document pass rate in tracker

---

## PHASE 4: SEND VIA APOLLO UI TASK QUEUE

> **This phase replaces the previous Gmail draft workflow.** As of March 1, 2026, all sequence emails are sent through Apollo's UI only.

### Step 4.1: Prepare email copy in a working doc
- Use Cowork/Claude output or manually written emails
- Save all email drafts in a markdown file (e.g., `touch1_drafts_batchX.md`) for reference
- Each email should include: recipient name, company, subject line, and body text

### Step 4.2: Send via Apollo task queue
1. Open Apollo UI > Sequences > "Q1 Website Visitor - Tier 1 Intent" > Tasks tab
2. For each prospect with a pending task (Touch 1, 2, or 3):
   a. Click on the prospect's task to open the email editor
   b. Replace the generic template with the personalized email from your working doc
   c. Verify the subject line matches the SOP format ("Quick question, [First Name]")
   d. Click "Complete" / Send to dispatch the email
3. Apollo will automatically:
   - Log the send under the contact's activity
   - Track opens, clicks, and bounces
   - Queue the next touch per the sequence cadence
   - Advance the contact to the next step

### Step 4.3: Verify sends
- After completing a batch, check the sequence dashboard for updated step counts
- Confirm each contact has moved from their current step to the next
- Spot-check 2-3 contact activity logs to confirm delivery

---

## PHASE 5: TRACK AND MONITOR

### Step 5.1: Update tracker
- Update prospect_master_tracker.md with send dates and method ("Apollo UI")
- Move contacts from "draft ready" to "sent" status
- Note any bounces or delivery failures

### Step 5.2: Monitor deliverability
- Check Apollo's sequence dashboard for bounce/delivery metrics within 24 hours
- Pay special attention to catchall domains (see Master SOP Section 9 for full list)
- Document any delivery issues in the tracker

### Step 5.3: Clean up deprecated Gmail drafts
- If any Gmail drafts were previously created for contacts now sent via Apollo, DELETE those drafts to avoid confusion
- The 46 Gmail drafts created on March 1 are partially redundant (16 contacts already sent via Apollo task queue)

---

## PHASE 6: FOLLOW UP MANAGEMENT

### Step 6.1: Touch 2 preparation
- Touch 2 tasks will appear in Apollo task queue per sequence cadence (Day 4)
- All steps are MANUAL, so no emails send without explicit action
- Personalized Touch 2 drafts exist in personalized_sequence_emails.md for the original 9 contacts
- Touch 2 drafts for the remaining contacts will need to be created following the same process

### Step 6.2: Touch 3 (breakup)
- Touch 3 tasks appear at Day 10
- Use "Should I close the loop?" subject line
- Keep short and respectful

---

## FILE REFERENCE

| File | Contents |
|------|----------|
| prospect_master_tracker.md | Master list of all contacts with status |
| personalized_sequence_emails.md | 3-touch drafts for original 9 contacts |
| touch1_drafts_batch2.md | Touch 1 drafts for Group A (13) + Group B (8) |
| touch1_drafts_batch2_groupC.md | Touch 1 drafts for Group C (25) |
| website_visitor_sequence_drafts.md | Original sequence template and prospect list |
| tier1_sequence_audit_report.md | Sequence audit and contact ownership report |

---

## QUICK REFERENCE: REPEATABLE CHECKLIST

For each new batch of contacts:

- [ ] Pull new Step 1 contacts from Apollo sequence
- [ ] Run ALL 9 qualification checks (see Master SOP Section 3) — including triple-sequence check, prior appointment check, and 30-day cooldown check
- [ ] Identify and document exclusions (with reasons)
- [ ] Enrich contacts via Apollo API
- [ ] Research companies for personalization
- [ ] Draft personalized Touch 1 emails using template
- [ ] Run automated quality checks (em dashes, buzzwords, subject, CTA, signature)
- [ ] Fix any failures and re-scan until 100% pass
- [ ] Save final email copy in working doc (markdown file)
- [ ] **Send via Apollo UI task queue** (paste personalized email into each task, click Complete)
- [ ] Verify sends in Apollo sequence dashboard
- [ ] Update tracker with send dates (note "Apollo UI" as send method)
- [ ] Monitor deliverability in Apollo (especially catchall domains)
- [ ] Prepare Touch 2 drafts for Day 4 follow up
- [ ] Delete any redundant Gmail drafts if they exist

---

## METRICS (as of March 1, 2026 EOD)

- Total contacts in sequence: ~80
- Touch 1 emails sent (Feb 27): 9 (original batch via Gmail — pre-Apollo-UI standard)
- Touch 1 emails sent (Feb 28): 6 (pre-existing Gmail sends — pre-Apollo-UI standard) + 13 (Apollo sequence)
- Touch 1 sent via Apollo task queue (Mar 1): 16 (personalized, sent from testsigma.net) ← **THIS IS THE CORRECT METHOD**
- Touch 1 Gmail drafts created (Mar 1): 46 — **DEPRECATED. Delete drafts for the 16 already sent via Apollo. Remaining drafts should be re-sent via Apollo UI, not Gmail.**
- Apollo task queue scan: 50 tasks total — 16 Step 1 sent, 34 Step 2 skipped
- Quality check pass rate: 100% (46/46 after fixes)
- Sequence opens: 3 unique
- Sequence replies: 0
- Catchall domains to monitor: G2, MedImpact, Flywire, Bynder, Iteris, + 14 more (see Master SOP)
- Contacts stopped (territory conflicts): 4 (Jose Moreno, Todd Willms, Jenny Li, Jeff Barnes)
- Contacts stopped (FAIL - duplicate sequences/job change): 3 (Tim Wiseman, Mazie Roxx, Harsha Navaratne)
- Contacts flagged for CRITICAL removal (engagement audit): 5 (Andy Roth, Katie Hotard, Giang Hoang, Mark Freitag, Khalid Aziz)

### Send Method Evolution (for reference)
| Date | Method | Result |
|------|--------|--------|
| Feb 27 | Gmail manual compose | Worked but no Apollo tracking |
| Feb 28 | Gmail manual + Apollo sequence add | Partial tracking |
| Mar 1 AM | Gmail API drafts via Cowork | Created 46 drafts but disconnected from Apollo tasks |
| Mar 1 PM | Apollo UI task queue | **CORRECT METHOD** — full tracking, proper sequence advancement |
| **Going forward** | **Apollo UI task queue ONLY** | **All future sends must use this method** |
