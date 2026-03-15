# Apollo Sequence Performance Analysis + Improvement Plan
## BDR Outreach — March 6, 2026
### Prepared by Claude (Cowork) | Based on Apollo live data + email_outreach_tracker.csv audit

---

## EXECUTIVE SUMMARY

As of March 6, 2026, the Testsigma BDR outreach operation has enrolled **518 total contacts** across three sequences — but only **~90 Touch 1 emails have actually been sent**, and **zero InMails have been executed** in the largest sequence (Q1 Priority Accounts, 285 contacts). The campaign is structurally sound and well-personalized, but execution velocity is severely lagging. The biggest immediate opportunities are not sourcing new leads — they are completing the Touch 2 queue for 70 already-warmed contacts and activating the 285-contact LinkedIn InMail sequence that has been sitting idle.

**One active warm conversation exists (Pallavi Sheshadri, Origami Risk → now Ampersand)** — she replied three times and engaged substantively, then went cold when asked for a demo. She has since changed jobs. This represents the only confirmed engagement from all 2026 outreach.

The CSV engagement tracking is incomplete — the Opened?, Replied?, Positive Reply?, and Meeting Booked? columns have not been updated after sends. This creates a blind spot on true performance, but the Gmail audit confirms no other replies have come in from cold outreach beyond Pallavi.

---

## SECTION 1: SEQUENCE-BY-SEQUENCE BREAKDOWN

### 1A. Q1 Website Visitor — Tier 1 Intent (Email)
**Apollo ID:** `69a1b3564fa5fa001152eb66`

| Metric | Count | Notes |
|--------|-------|-------|
| Total contacts enrolled | 91 | All Enterprise |
| Touch 1 sent | 90 | 82 prior sends + 8 sent today (Mar 6) |
| At Step 2 — awaiting Touch 2 | 70 | **No Touch 2s sent to date** |
| Step 2 blocked ("Reply to thread" error) | 5 | Tom Yang DNC'd; 5 errors fixed today |
| Finished / Stopped | 6 | Various reasons (see status report) |
| Bounced | 1 | Kenny Liu (ModMed) — find replacement |
| NEW JOB flag | 1 | Pallavi Sheshadri → moved to Ampersand |

**Confirmed engagement:**
- **Pallavi Sheshadri (Origami Risk)** — replied 3x, engaged substantively (discussed 1600+ Playwright tests, cursor.ai, Playwright Agent). Rob asked for demo Mar 2 → no reply since → job change confirmed. Thread stalled.
- All other contacts: no confirmed replies in Gmail inbox audit.

**Estimated reply rate:** ~1.1% on Touch 1 (1 confirmed reply / 90 sends). Likely understated — some replies may have gone to Salesforce or been missed. However, the Gmail inbox audit found no other cold reply threads active.

**The core problem here:** 70 contacts received a personalized Touch 1 and have been waiting for a follow-up for 5–7 days. The Touch 2 queue has not been executed. In cold email, 50–70% of replies typically come on Touch 2 or later. Every day without Touch 2 is leaving responses on the table.

---

### 1B. Q1 Priority Accounts (LinkedIn InMail)
**Apollo ID:** `69a05801fdd140001d3fc014`

| Metric | Count | Notes |
|--------|-------|-------|
| Total contacts enrolled | 285 | All at Step 1 (InMail #1) |
| InMails actually sent | **0** | **Sequence has never been executed** |
| "New" at Step 1 | ~242 | No prior activity anywhere |
| "Attempted to Contact" at Step 1 | ~36 | Stage comes from prior sequences, NOT this one |
| Finished (stopped) | 3 | Rashad Fambro, Amir Aly, Vinayak Singh |

**This is the single biggest gap in the operation.** 285 qualified QA leaders are enrolled and waiting — not one has received an InMail. The sequence steps are: InMail #1 → InMail #2 → Manual email → Phone call. Nothing has started.

LinkedIn InMail benchmarks for personalized, targeted outreach typically show **15–30% open rates and 8–15% reply rates** — significantly higher than cold email. With 285 contacts, executing this queue is the highest-leverage activity available.

**Why it hasn't been executed:** The Apollo task queue requires opening each task individually in the browser (which links to the LinkedIn profile) and sending the InMail manually. This is time-intensive but has no shortcut. The SOP (Step 4) covers the process.

---

### 1C. Copy — AI Maturity Audit Campaign for QA
**Apollo ID:** `6909f6b00f9bb2001d599d5e`

| Metric | Count | Notes |
|--------|-------|-------|
| Total contacts enrolled | 142 | Status of most is unknown |
| Gmail emails sent (Mar 3) | 19 | Sent outside Apollo — logged in CSV |
| Apollo task backlog | ~255+ tasks | Includes tasks from this sequence |
| Outreach via Apollo task queue | Unknown | Full audit not yet run |

This sequence was discovered on March 6 via the Apollo task digest showing 255 overdue tasks. The 19 Mar 3 Gmail sends were to contacts in this sequence — sent outside Apollo, creating tracking gaps. A full contact-level audit (comparable to the Tier 1 audit done today) needs to be run.

**Note on the 19 Mar 3 Gmail sends:**
- All logged in email_outreach_tracker.csv with Apollo contact IDs
- No replies confirmed in Gmail inbox audit
- Apollo timeline notes still need to be added to each of the 19 contacts manually

---

## SECTION 2: CROSS-SEQUENCE PERFORMANCE METRICS (2026)

| Metric | Value | Benchmark |
|--------|-------|-----------|
| Total tracked 2026 sends | 77 | — |
| Touch 1 only (no Touch 2+ tracked) | 77 (100%) | — |
| Engagement data tracked in CSV | 0 | **Critical gap** |
| Confirmed email replies (from Gmail audit) | 1 (Pallavi) | 1–5% industry avg |
| Confirmed meetings booked from cold outreach | 0 | — |
| Confirmed bounces | 1 (Kenny Liu) | <2% acceptable |
| Dual-sequencing violations resolved today | 3 | — |

**Send clustering issue:** 47 sends occurred on a single day (Feb 28) and 10 on Feb 27. Sending 57 emails over 2 days from the same domain can trigger spam filters. Apollo's built-in send limits help mitigate this, but batching in smaller daily groups (10–15/day) is better practice.

---

## SECTION 3: EMAIL CONTENT ANALYSIS

### Subject Lines
The Tier 1 Intent Touch 1 emails use a consistent "Quick question, [First name]" subject line format (confirmed from Apollo sequence template and send history). This is a well-known pattern — it has the advantage of low friction and high open rates historically, but it has also become widely used and increasingly filtered.

**What's working structurally:**
- Personalization is Tier A across 100% of sends — each email references the prospect's specific company and tech stack
- Angles are highly specific (e.g., "Regression testing eating your sprints," "Testing across 5 billion transactions," "Platform migration: test coverage risk")
- CTA is consistently low-friction: "Quick call or overview" / "Quick call"

**What's not differentiated:**
- 75 of 77 sends use the same CTA type ("Quick call" variants)
- Zero A/B testing across subject lines, angles, or CTAs
- No variation between Enterprise-size companies vs. mid-market
- All contacts marked as Personalization Level "Tier A" — no framework for Tier B or C outreach when personalization bandwidth is lower

### The Pallavi Conversation (Lesson)
The one confirmed engagement from all 2026 outreach provides a useful signal:

- **What worked:** A highly personalized Touch 1 about QA automation for risk management platforms. Pallavi responded with genuine context about her stack and pain points.
- **What stalled it:** When Rob asked for a demo/intro, Pallavi went cold. This is a common pattern — the pivot from "exchange" to "commitment ask" (demo) is where many cold threads die. A softer next step (e.g., "Would it be useful to share a 2-min video of how this works?") may have kept the thread alive.
- **What happened after:** Pallavi changed jobs. The conversation ended not because of disinterest but timing.

**Takeaway:** The personalization approach is working well enough to get a real conversation. The conversion point (demo ask) needs testing.

---

## SECTION 4: KEY STRUCTURAL ISSUES

### Issue 1: Touch 2 Queue Not Executing (HIGH IMPACT)
70 contacts have received Touch 1 but no Touch 2. Industry data consistently shows that **50–70% of B2B cold email replies come on Touch 2 or later**. Letting 70 contacts sit untouched after receiving Touch 1 is the single most impactful problem to fix.

**Fix:** Execute Touch 2 for all 70 Step 2 contacts via Apollo task queue. Priority: oldest Touch 1 sends first (Feb 27 batch — now 7 days old).

### Issue 2: Q1 Priority Accounts Completely Idle (HIGH IMPACT)
285 LinkedIn-sourced QA leaders have been enrolled for weeks with zero outreach. LinkedIn InMail outperforms cold email in B2B SaaS by a significant margin, especially for director+ titles. This is the largest untapped asset in the operation.

**Fix:** Run the Apollo task queue for Priority Accounts. Aim for 10–20 InMails per day. The queue will open each LinkedIn profile automatically.

### Issue 3: Engagement Tracking Not Maintained (MEDIUM IMPACT — DATA)
The email_outreach_tracker.csv has columns for Opened?, Replied?, Positive Reply?, Meeting Booked?, and Outcome Notes — but none of these have been updated after any 2026 send. Without this data, it's impossible to measure true open/reply rates, identify which angles are performing, or calculate ROI on the outreach effort.

**Fix:** After each Apollo task queue session, update the tracker with opens/replies from Apollo's sequence analytics. Apollo shows per-contact email status (opened, clicked, replied). Takes 5–10 minutes after each batch.

### Issue 4: Gmail Sends Outside Apollo (MEDIUM IMPACT — TRACKING)
26 of 77 tracked sends (34%) were sent via Gmail compose, not Apollo's task queue. This creates tracking gaps: contacts appear stuck in sequences, opens/replies aren't logged in Apollo, and follow-up timing gets lost.

- 19 Mar 3 sends (AI Maturity Audit Campaign contacts)
- ~6 ad-hoc Feb 28 sends (Pallavi, Gunasekaran, Giang, etc.)
- 1 Jason Dudley Mar 4 warm inbound follow-up

**Fix:** All future sequence sends must go through Apollo task queue (the SOP now documents this as a non-negotiable rule). For past Gmail sends, add Apollo timeline notes per the SOP.

### Issue 5: AI Maturity Audit Campaign Unaudited (MEDIUM IMPACT)
142 contacts, 255+ overdue tasks, 19 Gmail sends already out — and no contact-level audit has been run. This is the same problem that existed with Priority Accounts at the start of today's session: contacts are enrolled but nothing has been executed.

**Fix:** Run a full stage/step audit of the AI Maturity Audit Campaign (same process as today's Tier 1 audit).

### Issue 6: 255-Task Backlog Creates Analysis Paralysis (MEDIUM IMPACT)
When 255 tasks are showing as overdue, it's psychologically difficult to know where to start. The prioritization framework in the SOP addresses this, but the sheer volume can lead to deferral.

**Fix:** Set a daily task execution quota (e.g., 15 email tasks + 10 InMail tasks per day). Use the SOP prioritization order: P0 live conversations → P1 Touch 1s → P2 Thread errors → P3 InMail queue.

---

## SECTION 5: IMPROVEMENT PLAN — PRIORITIZED ACTIONS

### IMMEDIATE (Next 3 days)

**1. Execute Touch 2 for all 70 pending Step 2 contacts in Tier 1 Intent**
- Where: Apollo task queue → filter by Step 2
- Priority order: Feb 27 batch (7 days since Touch 1) → Feb 28 batch (6 days)
- Note: 3 contacts need manual Gmail send + Apollo mark-complete (Hibatullah, Eduardo, Andy — drafts already in Gmail)
- Expected impact: If even 3–5% of the 70 contacts reply, that's 2–4 conversations from a single queue run

**2. Send 3 pending Gmail drafts + mark Step 2 complete in Apollo**
- Open Gmail Drafts → send "Following up, Hibatullah," "Following up, Eduardo," "Following up, Andy"
- Then in Apollo: navigate to each contact → Sequences tab → mark Step 2 task complete
- This is already set up and ready

**3. Add Apollo timeline notes to all 19 AI Maturity Audit Gmail sends (Mar 3)**
- Template: `"Email sent via Gmail Mar 3, 2026 — subject: [subject line] — sent outside Apollo task queue. Do not re-send Step 1 via Apollo for this contact."`
- Apollo contact IDs are all logged in email_outreach_tracker.csv

### SHORT TERM (This week)

**4. Start executing Q1 Priority Accounts InMail queue — 20/day goal**
- Open Apollo → Sequences → Q1 Priority Accounts → Task queue
- Each task opens the LinkedIn profile and provides the InMail template
- Target: 20 InMails/day = ~14 business days to work through the full 285 contacts
- Track in email_outreach_tracker.csv: Channel = "LinkedIn InMail"

**5. Run AI Maturity Audit Campaign contact audit**
- Navigate to Apollo → Sequences → Copy AI Maturity Audit Campaign for QA
- Pull stage/step breakdown (same format as today's Tier 1 audit)
- Check for dual-sequencing violations, error states, and which contacts have Step 2 pending
- Update sequence_status_report with findings

**6. Fix engagement tracking in email_outreach_tracker.csv**
- After each Apollo task queue session, open Apollo → Sequences → [Sequence] → Contacts
- For each sent contact, check "Opened?", "Replied?" in Apollo's sequence analytics
- Update the CSV columns accordingly
- Add Apollo's "email opened" date as a note if available

### MEDIUM TERM (Next 2–3 weeks)

**7. A/B test subject line variants in Touch 1**
- Current default: "Quick question, [First Name]"
- Test variant A: "[Company] + Testsigma" (company-first curiosity)
- Test variant B: A specific pain point as subject (e.g., "Regression debt at [Company]?")
- Evaluate: Run 20 sends with each variant over a 2-week period, compare open/reply rates

**8. A/B test CTA on Touch 2**
- Current: "Quick call or overview" (all Touch 2s use this)
- Test variant A: "Would a 2-min Loom of how this works for [Company's] stack be useful?"
- Test variant B: "One specific question about your regression coverage — do you have 2 min?"
- The Pallavi lesson suggests the soft "one question" CTA keeps the conversation going longer before the demo ask

**9. Stagger daily send volume**
- Current pattern: large batches on single days (47 sends Feb 28)
- Target: 10–15 sends/day, spread across 5 days
- This reduces spam filter risk, spreads reply volume, and makes follow-up manageable

**10. Stop Pallavi Sheshadri from Tier 1 Intent + find Origami Risk replacement**
- Stop Pallavi in sequence (she left the company)
- Identify new QA contact at Origami Risk as replacement
- Consider reaching out to Pallavi at Ampersand with a brief, contextual re-introduction

### TRACKING IMPROVEMENTS

**11. Update the SOP to require engagement tracking**
- Add Step 6B to the Daily Audit SOP: "Check Apollo sequence analytics for opened/replied status on all Touch 1 sends from the prior 7 days. Update email_outreach_tracker.csv."
- Add a weekly "performance snapshot" section to the sequence_status_report format

**12. Create a pipeline attribution note for Lexia Learning**
- Lexia Learning ($50K active trial, Trial Kickoff Mar 3, Trial Sync Mar 9) is the most significant near-term revenue in the pipeline
- Confirm in Salesforce whether this originated from cold outreach or inbound
- If from outreach: log it in the tracker as a Meeting Booked + mark the original send row

---

## SECTION 6: PERFORMANCE BENCHMARKS & TARGETS

| Metric | Current (Tracked) | Realistic Target (30 days) | Notes |
|--------|------------------|---------------------------|-------|
| Touch 1 reply rate (email) | ~1.1% | 2–4% | Industry avg 1–5%; Tier A personalization should be at upper end |
| Touch 2 reply rate | Not tracked | 3–5% | Touch 2 historically outperforms Touch 1 |
| LinkedIn InMail reply rate | Not started | 10–20% | Higher than email for director+ titles at targeted accounts |
| Meeting booked rate from cold outreach | 0 confirmed | 0.5–1% of sends | 1–2 meetings per 100 sends is realistic for Tier A |
| Active conversations (warm threads) | 1 (stalled) | 3–5 simultaneous | Target from Touch 2 execution + InMail queue |
| Daily task execution | Variable / low | 15 email + 10 InMail | Steady cadence beats batch sends |

---

## SECTION 7: WHAT'S WORKING — DON'T BREAK IT

1. **Qualification rigor** — The 9-point ICP checklist is being followed. Contact quality appears high (all Enterprise, correct titles, verified emails where possible).
2. **Personalization depth** — Every email references specific company context, industry-specific pain points, and credible data points (e.g., "13 billion transactions," "2000 integrations"). This is above-average for BDR outreach.
3. **Sequence structure** — The Tier 1 Intent multi-touch cadence (email → follow-up → follow-up) is well-designed. The problem is execution speed, not the design.
4. **Apollo as source of truth** — The SOP's Apollo-only rule is now documented and enforced. Today's audit confirmed the approach: when sends go outside Apollo, they become invisible.
5. **Daily audit rhythm** — Running the morning audit before any outreach prevents duplicate sends and catches errors before they compound.

---

## APPENDIX: DATA SOURCES

- `email_outreach_tracker.csv` — 77 rows of 2026 sends analyzed (Feb 27 – Mar 4)
- `sequence_status_report_mar6.md` (v5) — Live Apollo stage/step data as of March 6
- Gmail inbox audit (robert.gorham@testsigma.com) — scanned for prospect replies, Mar 6
- Gong pipeline digest — Lexia Learning $50K trial context
- Apollo sequence contacts pages (pulled via Chrome during morning audit session)
- `daily_sequence_audit_sop.md` — Process reference

---

*Analysis prepared: March 6, 2026 | Version 1.0*
*Next review: March 13, 2026 (after Touch 2 queue execution + first week of Priority Accounts InMails)*
