# Outreach Email SOP: End-to-End Repeatable Process
## Covers: Tier 1 Intent + Priority Accounts + AI Maturity Audit Campaign Sequences
## Last Updated: March 6, 2026 (v4.1 — Touch 2 execution complete for 67 contacts; Gmail-only workflow documented; stale drafts deleted; tracker updated)

---

## OVERVIEW

This SOP documents the full process for creating, quality checking, and sending personalized outreach emails to prospects in Apollo sequences. The process is designed to be repeatable for any new batch of contacts added to either sequence. It covers two active sequences:

1. **Q1 Website Visitor - Tier 1 Intent** (intent-driven website visitors)
2. **Q1 Priority Accounts** (strategic account targets)

> **WRITING STYLE RULE (March 2, 2026):** Never use em dashes (the long dash character) in any outreach emails, SOPs, or written communications. Use commas, periods, parentheses, or restructure the sentence instead. This applies to all documents and email drafts produced under this SOP.

**Send Account:** robert.gorham@testsigma.com (Apollo email account ID: `68e3b53ceaaf74001d36c206`)
**Deprecated Send Account:** robert.gorham@testsigma.net (ID: `68f65bdf998c4c0015f3446a`) -- used for earlier batches, no longer the default

### Active Sequences

| Sequence | ID | Steps | Email Style | Status |
|----------|----|-------|-------------|--------|
| Q1 Website Visitor - Tier 1 Intent | `69a1b3564fa5fa001152eb66` | 3 touches, all MANUAL email | Template-based ("Quick question, [First Name]") | Active — Touch 2 COMPLETE (67 sent Mar 6, 2026). Contacts now at Step 3. |
| Q1 Priority Accounts | `69a05801fdd140001d3fc014` | Step 1-2 InMail, Step 3 email, Step 4 call | Case-study personalized, unique subject per contact | ⚠️ IDLE — 285 contacts, 0 InMails sent |
| Copy - AI Maturity Audit Campaign for QA | `6909f6b00f9bb2001d599d5e` | Email sequence | Personalized to QA/engineering pain points | ⚠️ NEEDS AUDIT — 142 contacts, ~255 tasks overdue |

> **⚠️ CORRECTION (March 6, 2026):** The 19 Priority Accounts emails previously recorded as "sent March 3" were actually sent to AI Maturity Audit Campaign contacts via Gmail (outside Apollo). Q1 Priority Accounts has had ZERO InMails sent. The March 3 Gmail sends are logged in email_outreach_tracker.csv and Apollo notes are pending.

> **CRITICAL PROCESS CHANGE (March 3, 2026):** All emails are now sent from **robert.gorham@testsigma.com**. The testsigma.net address was used for earlier batches but is no longer the default. When using the Apollo email composer, always select testsigma.com from the From dropdown.

> **⚠️ CRITICAL PROCESS CHANGE (March 3, 2026):** All emails are sent exclusively through Apollo UI. Two send methods are used depending on the sequence: (1) Apollo task queue for Tier 1 Intent, and (2) Apollo manual email composer for Priority Accounts. Gmail drafts and Gmail API sends are deprecated. Emails sent outside Apollo do not register in the sequence, break deliverability tracking, and create double-send risk. See Phase 4 below for both workflows.

---

## PHASE 1: IDENTIFY CONTACTS NEEDING TOUCH 1

### Step 1.1: Pull contacts from Apollo sequence
- Open the relevant Apollo sequence:
  - "Q1 Website Visitor - Tier 1 Intent" for intent-driven prospects
  - "Q1 Priority Accounts" for strategic account targets
- Filter contacts at the relevant step (those who have NOT yet received the current touch)
- Export or note: Name, Title, Company, Email, Contact ID, Owner

### Step 1.2: Check for already sent emails
- Search Apollo contact activity logs for recent sends
- For Tier 1: check for subject "Quick question" sends
- For Priority Accounts: check contact activity timeline for any recent emails
- Cross reference against the to-send list to identify any already sent
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

### Step 2.3: Draft personalized emails

Two email styles are used depending on the sequence:

**Style A: Tier 1 Intent (template-based)**
- Subject: "Quick question, [First Name]"
- Opens with website visitor intent signal
- Middle paragraph connects Testsigma value to their company/role
- Low-friction CTA (15 min call or overview doc)
- Sign off: "Best, Rob"
- 4-6 sentences

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

**Style B: Priority Accounts (case-study personalized)**
- Subject: Unique per contact, tied to their specific challenge (e.g., "Regression testing under compliance pressure", "QA scaling for 13 billion transactions")
- NO greeting line (starts directly with a question or challenge statement)
- Opens with a pain-point question specific to their company/role
- Middle: relevant Testsigma case study proof point (e.g., CRED 90% reduction, Hansard 8 weeks to 5, Medibuddy 40% reduction)
- CTA: "What day works to see how..." or similar
- Sign off: "Rob" (no "Best,")
- 4-5 short paragraphs, concise and direct

```
Subject: [Unique challenge-based subject]

[Pain-point question specific to their company/situation]

[Industry context: why this matters for their vertical]

[Case study proof point with specific metrics from Testsigma customer]

[CTA tied to the case study: "If [benefit] sounds useful, what day works for a quick look?"]

Rob
```

**Case Study Library for Priority Accounts:**

| Case Study | Key Metric | Best For |
|------------|-----------|----------|
| CRED | 90% reduction in regression test maintenance, 15+ hrs/week recovered | Large-scale platforms, high transaction volume |
| Hansard | Regression cycles cut from 8 weeks to 5 weeks, AI auto-healing | Compliance-heavy orgs, platform migrations |
| Medibuddy | 40% reduction in test maintenance | Healthcare, high integration count |
| Acko | Test cycle reduction across web + mobile | Insurance, multi-platform testing |

---

## PHASE 3: QUALITY CHECKS

### Step 3.1: Automated quality scan
Run all drafts through the following checks:

| Check | Rule (Tier 1 Intent) | Rule (Touch 2 / All Sequences) | Action if Fail |
|-------|----------------------|--------------------------------|----------------|
| Em dashes | ZERO em dashes (—) | ZERO em dashes (—) — major AI tell | Replace with comma, period, colon, or restructure sentence |
| Regular dashes | Hyphens only for hyphenated words (e.g., follow-up, multi-tenant) | Max 1-2 short hyphens (-) per email total; never use as sentence connectors | Remove or restructure sentence |
| Buzzwords | None of: synergy, leverage, cutting-edge, game-changer, revolutionary, disruptive, paradigm, holistic, robust, seamless, seamlessly, turnkey, best-in-class, world-class, next-gen, bleeding edge, innovative | Same list | Replace with plain language |
| Sentence flow | No awkward or AI-sounding phrasing; sentences must read naturally out loud | Read each sentence aloud test: if it sounds stiff or robotic, rewrite | Rewrite affected sentences |
| Subject line | Must be exactly "Quick question, [First Name]" for T1; "One more thought, [First Name]" for T2 | Unique, challenge-based for Priority Accounts | Fix to match style |
| Opening | Body must contain website visitor intent reference (T1) or brief re-engagement line (T2) | Must open with pain-point question or brief re-engagement | Fix opening |
| Proof point | N/A for T1 | T2 Template B must use named customer (Sanofi, UK Govt Procurement Service, or Spendflo) with specific metrics | Add named proof point |
| CTA | Low friction CTA (15 min call or overview doc) | "Worth a quick reply?" or equivalent low-friction ask | Add CTA |
| Signature | Must end with "Best, Rob" (T1) | Must end with "Cheers, Rob" (T2) | Fix signature |
| Length | 4-6 sentences in body (T1) | 3-4 short paragraphs, 4-8 lines total (T2) | Trim or expand |
| Title match | Target titles per ICP | Sr SDET is deprioritized (not decision-maker) | Flag for review |
| Ownership | Contact must be owned by Rob | Contact must be owned by Rob | SKIP send |

**Touch 2 Grammar + Formatting Standards (aligned with LinkedIn Sequence SOP):**
- **No em dashes (—) anywhere.** Use periods, commas, colons, or parentheses instead.
- **No excessive dashes.** Short hyphens (-) are only for hyphenated compound words. Do not use them as sentence connectors or to create em-dash-style pauses.
- **Smooth, natural wording.** Every sentence should read cleanly out loud. If it sounds stiff or AI-generated, rewrite it in plain conversational English.
- **Short sentences.** Prefer two clean sentences over one long compound sentence joined by a dash or comma splice.
- **No walls of text.** Each paragraph should be 1-2 sentences max. Blank line between each block.
- **No buzzwords.** Plain language only. Never use: synergy, leverage (verb), cutting-edge, game-changer, revolutionary, disruptive, paradigm, holistic, robust, seamless, turnkey, best-in-class, world-class, next-gen, bleeding edge, innovative.
- **No invented claims.** Every specific number or customer reference must be from the verified proof point library (Sanofi, UK Government Procurement Service, Spendflo).
- **No emojis.** Never in outreach emails.

**Em dash replacement guide:**
- "Following up — still think..." → "Following up. Still think..."
- "Out of the loop — wanted to share..." → "Out of the loop. Wanted to share..."
- "Question — or is X?" → "Question, or is X?"
- "Proof point — automating/cutting/enabling..." → "Proof point, automating/cutting/enabling..."
- "Tool — it's specifically for..." → "Tool. It's specifically for..."
- "Complex scenario — where X happens —" → "Complex scenario (where X happens)"

### Step 3.2: Manual spot check
- Read 5-10 random emails for tone, accuracy, and natural flow
- Verify company descriptions are accurate
- Confirm no copy paste errors between emails

### Step 3.3: Fix and re-scan
- Fix any failures identified in 3.1
- Re-run automated scan to confirm 100% pass rate
- Document pass rate in tracker

---

## PHASE 4: SEND VIA APOLLO UI

> **This phase replaces the previous Gmail draft workflow.** As of March 1, 2026, all sequence emails are sent through Apollo's UI only. Two methods exist depending on the sequence type.

### Step 4.1: Prepare email copy in a working doc
- Use Cowork/Claude output or manually written emails
- Save all email drafts in a markdown file (e.g., `batch8_touch1_drafts.md`) for reference
- Each email should include: recipient name, company, email, subject line, and body text
- For Priority Accounts, also include: vertical, priority score, and group designation

### Step 4.2A: Send via Apollo task queue (Tier 1 Intent)
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

### Step 4.2B: Send via Apollo manual email composer (Priority Accounts)
This method is used when contacts are in the Priority Accounts sequence and emails need to be sent outside the task queue (e.g., when tasks haven't appeared yet or for ad-hoc sends).

1. Navigate to each contact's profile page in Apollo
2. **Verify before sending:**
   - Contact is on the correct list (e.g., "Batch 8")
   - Contact is owned by Rob Gorham (owner_id check)
   - If owned by someone else, SKIP (e.g., Rian Musial was owned by Senthilkumar K and was skipped)
3. Click the **envelope icon** on the contact profile to open the email composer
4. **Switch the From address:**
   - Click the From dropdown arrow
   - Select **testsigma.com** (robert.gorham@testsigma.com)
   - This must be done for EVERY email; the composer defaults to testsigma.net
5. Close the "Write with AI" panel if it auto-opens (click the X)
6. Set the subject line and body from the working doc
7. Click **"Send Now"** to dispatch
8. Verify the email was sent (composer drawer closes, email appears in contact activity)

**Manual composer workflow notes:**
- The From dropdown must be changed every time; it does not remember your selection
- The "Write with AI" panel opens automatically and must be dismissed
- Always verify ownership before sending; Apollo will send the email even if someone else owns the contact, but this creates territory conflicts
- Catch-all email addresses should still be sent but monitored for bounces

### Step 4.3: Verify sends
- After completing a batch, check the sequence dashboard for updated step counts
- Confirm each contact has moved from their current step to the next
- Spot-check 2-3 contact activity logs to confirm delivery
- For Priority Accounts manual sends, verify the email appears in the contact's activity timeline

---

## PHASE 5: TRACK AND MONITOR

### Step 5.1: Update tracker
- Update prospect_master_tracker.md with send dates and method ("Apollo UI")
- Move contacts from "draft ready" to "sent" status
- Note any bounces or delivery failures
- Update email_outreach_tracker.csv: add a row for every send with Date, Prospect Name, Company, Title, Email, Account Type, Source, Sequence Name, Channel, Touch Number, Angle, CTA Type

### Step 5.1B: Update engagement tracking (NEW — March 6, 2026) ⚠️
**This step was previously skipped — the Opened?, Replied?, and Positive Reply? columns in email_outreach_tracker.csv were never updated after sends, creating a blind spot.**

After each send batch, and again 48–72 hours later:
1. Open Apollo → Sequences → [Sequence] → Contacts tab
2. For each recently-sent contact, check their Apollo activity timeline
3. If the email was opened: set `Opened? = Y` in the CSV
4. If the contact replied: set `Replied? = Y`, `Positive Reply? = Y/N`, and update `Outcome Notes`
5. If a meeting was booked: set `Meeting Booked? = Y`
6. If email bounced: set `Outcome Notes = "Bounced"` and update status in Apollo (Unqualified)

This takes 5–10 minutes per batch and is essential for measuring reply rates and identifying which angles and subject lines perform best.

### Step 5.2: Monitor deliverability
- Check Apollo's sequence dashboard for bounce/delivery metrics within 24 hours
- Pay special attention to catchall domains (see Master SOP Section 9 for full list)
- Document any delivery issues in the tracker

### Step 5.3: Clean up deprecated Gmail drafts
- If any Gmail drafts were previously created for contacts now sent via Apollo, DELETE those drafts to avoid confusion
- The 46 Gmail drafts created on March 1 are partially redundant (16 contacts already sent via Apollo task queue)
- **COMPLETED March 6, 2026:** All stale Touch 2 Gmail drafts deleted by Rob. This includes 3 old "Following up, [Name]" drafts (Andy/Eduardo/Hibatullah) and 3 em-dash-contaminated "One more thought" drafts created before the quality fix. All clear.

---

## PHASE 6: FOLLOW UP MANAGEMENT

### Step 6.1: Touch 2 — COMPLETED March 6, 2026

**Touch 2 is fully sent.** All 67 contacts received "One more thought, [First Name]" emails on March 6, 2026.

- 63 contacts: sent via Apollo task queue (auto-logged, sequence advanced to Step 3)
- 4 Gmail-only contacts (Andy Nelsen, Eduardo Menezes, Hibatullah Ahmed, Amir Aly): sent via Gmail Chrome UI, auto-logged by Apollo Gmail integration. Apollo Step 2 tasks intentionally left as "Not Sent" — marking as finished would have ended their entire sequence. Hibatullah, Eduardo, and Andy remain active in sequence (Touch 3 will auto-send). Amir Aly sequence is "Finished" (pre-existing Feb 28 error) — Touch 3 must be sent via Gmail manually when ready.
- Full draft set in: `touch2_drafts_all_contacts_mar6.md`
- Formula and QA verification: `touch2_formula_and_strategy_mar6.md`
- All 67 emails passed 10-point QA checklist (zero em dashes, correct signatures, named proof points)
- All stale Gmail drafts deleted
- Touch 2 rows added to email_outreach_tracker.csv for 4 Gmail-only sends
- Next action: Touch 3 (breakup email) will queue at Day 10 cadence. Monitor for replies in Apollo over 48-72 hrs.

### Step 6.2: Touch 3 (breakup)
- Touch 3 tasks appear at Day 10
- Use "Should I close the loop?" subject line
- Keep short and respectful

---

## FILE REFERENCE

| File | Sequence | Contents |
|------|----------|----------|
| prospect_master_tracker.md | Tier 1 | Master list of all contacts with status |
| personalized_sequence_emails.md | Tier 1 | 3-touch drafts for original 9 contacts |
| touch1_drafts_batch2.md | Tier 1 | Touch 1 drafts for Group A (13) + Group B (8) |
| touch1_drafts_batch2_groupC.md | Tier 1 | Touch 1 drafts for Group C (25) |
| website_visitor_sequence_drafts.md | Tier 1 | Original sequence template and prospect list |
| tier1_sequence_audit_report.md | Tier 1 | Sequence audit and contact ownership report |
| batch8_touch1_drafts.md | Priority Accts | 21 case-study personalized drafts for Batch 8 |
| email_outreach_tracker.csv | Both | Detailed outreach log with engagement data |

---

## QUICK REFERENCE: REPEATABLE CHECKLIST

For each new batch of contacts:

- [ ] Pull contacts from Apollo sequence (Tier 1 Intent or Priority Accounts)
- [ ] Run ALL 9 qualification checks (see Master SOP Section 3), including triple-sequence check, prior appointment check, 30-day cooldown check, AND ownership verification
- [ ] Identify and document exclusions (with reasons, including title mismatches like Sr SDET)
- [ ] Enrich contacts via Apollo API
- [ ] Research companies for personalization
- [ ] Draft personalized emails using the correct style (Style A for Tier 1, Style B for Priority Accounts)
- [ ] Run automated quality checks (em dashes, buzzwords, subject, CTA, signature, ownership)
- [ ] Fix any failures and re-scan until 100% pass
- [ ] Save final email copy in working doc (markdown file, e.g., `batchX_touch1_drafts.md`)
- [ ] **Send via Apollo UI:**
  - Tier 1 Intent: Apollo task queue (paste into task, click Complete)
  - Priority Accounts: Apollo manual email composer (envelope icon on contact profile)
- [ ] **Always select testsigma.com as the From address** (dropdown defaults to testsigma.net)
- [ ] Verify ownership before each send (skip if not owned by Rob)
- [ ] Verify sends in Apollo (sequence dashboard or contact activity timeline)
- [ ] Update tracker with send dates, method, and send account
- [ ] Monitor deliverability in Apollo (especially catchall domains)
- [ ] Prepare follow-up drafts per sequence cadence

---

## METRICS

### Tier 1 Intent Sequence (updated March 6, 2026)
- Total contacts in sequence: ~91
- Touch 1 emails sent (Feb 27): 9 (original batch via Gmail, pre-Apollo-UI standard)
- Touch 1 emails sent (Feb 28): 6 (pre-existing Gmail sends) + 13 (Apollo sequence)
- Touch 1 sent via Apollo task queue (Mar 1): 16 (personalized, sent from testsigma.net)
- Touch 1 Gmail drafts created (Mar 1): 46, DEPRECATED
- Quality check pass rate: 100% (46/46 after fixes)
- Contacts stopped (territory conflicts): 4 (Jose Moreno, Todd Willms, Jenny Li, Jeff Barnes)
- Contacts stopped (FAIL): 3 (Tim Wiseman, Mazie Roxx, Harsha Navaratne)
- Contacts flagged for CRITICAL removal: 5 (Andy Roth, Katie Hotard, Giang Hoang, Mark Freitag, Khalid Aziz)
- **Touch 2 sent (Mar 6, 2026): 67 contacts total**
  - 63 via Apollo task queue (auto-tracked, sequence advanced)
  - 4 via Gmail (Andy Nelsen, Eduardo Menezes, Hibatullah Ahmed, Amir Aly) — Thread Missing / Finished error states
  - 1 skipped (Tom Yang — DNC confirmed Mar 6 Apollo audit)
  - Templates used: A (question-led), B (Sanofi/UK Gov proof point), C (ultra-short for high-uniqueness tech)
  - QA: 100% pass rate (130 em dashes removed across full draft set before sends)
  - All Touch 2 rows added to email_outreach_tracker.csv
  - All stale Gmail drafts deleted (6 total: 3 "Following up" + 3 em-dash "One more thought" versions)

### Priority Accounts Sequence - CORRECTED Status (March 6, 2026)
- **⚠️ CORRECTION:** No InMails have been sent to Priority Accounts contacts via Apollo.
- Total contacts enrolled: 285 (all at Active Step 1 — InMail #1 never sent)
- "Batch 8" drafts created: 21 (March 3, case-study personalized emails)
- What actually happened March 3: Those 19 drafts were sent via Gmail to AI Maturity Audit Campaign contacts, NOT Priority Accounts contacts. They are now logged in email_outreach_tracker.csv.
- Priority Accounts InMail queue: 285 pending — execution has not started. See `sequence_performance_analysis_mar6.md` for prioritized action plan.
- Email style: Case-study personalized, unique subject lines (still correct for when InMails are sent)

**Batch 8 Full Send Log:**

| # | Contact | Company | Status | Subject |
|---|---------|---------|--------|---------|
| 1 | Lyle Landry | Availity | SENT | QA scaling for 13 billion transactions |
| 2 | Emre Ozdemir | OCC | SENT | Platform migration: test coverage risk |
| 3 | Keith Schofield | Fullsteam | SENT | Test debt across 100 portfolio products |
| 4 | Priya Khemani | GetInsured | SENT | ACA enrollment testing at deadline scale |
| 5 | Morya Moyal | Hippo Insurance | SENT | Regression coverage across claims + underwriting |
| 6 | Konstantin Diachenko | Paymentus | SENT | Regression validation: payment rails migration |
| 7 | Shivaleela Devarangadi | RxSense | SENT | Formulary engine: regression vs. release velocity |
| 8 | Kerri McGee | Sapiens | SENT | 4 platforms, 1 regression bottleneck |
| 9 | Avijit Sur | Solera | SENT | Regression testing across 7 product lines |
| 10 | Jamie Kurt | Vertafore | SENT | Insurance platform: regression vs. release cadence |
| 11 | Courtney Corbin | Vizient | SENT | Test maintenance across member integrations |
| 12 | Jim Lenihan | Waystar | SENT | Revenue cycle QA: compliance vs. velocity |
| 13 | Sneha Bairappa | AAMC | SENT | Test coverage across 3 major platform transitions |
| 14 | Nabil Ahmed | Progyny | SENT | HIPAA regression: coverage vs. compliance velocity |
| 15 | Olivia Pereiraclarke | Sapiens | SENT | Policy admin: regression across 4 platform migrations |
| 16 | Geoffrey Juma | Solera | SENT | Fleet QA: regression across telematics + claims |
| 17 | Jason Schwichtenberg | WebMD | SENT | Regression validation: time or accuracy |
| 18 | Kyung Kim | WebMD | SENT | Test coverage reality across 2,000 integrations |
| 19 | Stephen Starnaud | biBerk | SENT | Regression testing under compliance pressure |
| -- | Rian Musial | CCC | SKIPPED | Owned by Senthilkumar K, not Rob |

### Send Method Evolution (for reference)
| Date | Method | Sequence | Result |
|------|--------|----------|--------|
| Feb 27 | Gmail manual compose | Tier 1 | Worked but no Apollo tracking |
| Feb 28 | Gmail manual + Apollo add | Tier 1 | Partial tracking |
| Mar 1 AM | Gmail API drafts via Cowork | Tier 1 | Created 46 drafts, disconnected from Apollo tasks |
| Mar 1 PM | Apollo UI task queue | Tier 1 | Full tracking, proper sequence advancement |
| Mar 2 | Apollo manual composer | Priority Accts | 1 email (Brian Liu), sent from testsigma.net |
| **Mar 3** | **Apollo manual composer** | **Priority Accts** | **19 emails sent from testsigma.com. CURRENT STANDARD.** |
| **Mar 6** | **Apollo task queue (63) + Gmail UI (4)** | **Tier 1 — Touch 2** | **67 Touch 2 emails sent. 4 Gmail-only contacts handled via Chrome UI; auto-logged by Apollo Gmail integration. Step 2 tasks left as "Not Sent" — sequence preserved for Touch 3 auto-send (Amir Aly: sequence "Finished", Touch 3 via Gmail manually).** |
| **Going forward** | **Apollo UI (task queue or manual composer)** | **Both** | **Always send from testsigma.com** |
