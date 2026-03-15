# Email Sequence Performance Audit
## Q1 Website Visitor - Tier 1 Intent | Apollo ID: 69a1b3564fa5fa001152eb66
### Audit Date: March 7, 2026 | Prepared by Claude (Cowork)

---

## Executive Summary

The Q1 Website Visitor Tier 1 Intent sequence has enrolled 91 contacts across its lifetime. Of those, 90 have received Touch 1. But **zero Touch 2 emails have been sent** to the 70 contacts currently waiting at Step 2, and the sequence has produced exactly **one confirmed reply** from all 90 Touch 1 sends (1.1% reply rate).

This audit documents what the data shows, what the current template quality problems are, and what specific, numbered improvements would materially change performance. The recommendations are ordered by expected impact.

**State of the sequence as of March 6-7, 2026:**

| Metric | Value |
|--------|-------|
| Total enrolled contacts | 91 |
| Touch 1 sent | 90 |
| Touch 2 sent | **0** |
| Touch 3 sent | 0 |
| Confirmed replies (Gmail audit) | 1 (Pallavi Sheshadri) |
| Confirmed meetings booked | 0 |
| Confirmed hard bounces | 1 (Kenny Liu, ModMed) |
| Engagement tracking maintained | **No — zero opens/clicks logged** |
| Contacts currently stuck at Step 2 | 70 |

---

## Section 1: Execution Gaps (The Big Numbers Problem)

### 1.1 The Touch 2 Execution Gap

70 contacts received a personalized Touch 1 and then received nothing. This is the single largest performance problem in the sequence — not the template quality, not the targeting, not the subject line. The emails are not being sent.

**Why this matters by the numbers:** Industry benchmarks for B2B cold email consistently show that 50-70% of replies come from Touch 2 or later (Rob's own LinkedIn data from the mabl dataset confirms this: 53.7% of replies came by the 2nd message, and 31.1% required 3+ touches). A sequence where only Touch 1 has been executed is capturing at most 25-30% of the reply potential that exists in this list.

**Estimated impact of executing Touch 2 for all 70 pending contacts:**

Assuming a conservative 2-3% reply rate on Touch 2 (slightly higher than Touch 1 given follow-up data):
- Low estimate (2%): 1-2 additional replies
- Mid estimate (3%): 2 replies
- High estimate (5%): 3-4 replies

These are not big numbers in absolute terms. But against a baseline of 1 total reply from the entire campaign, adding 2-4 replies would represent a 200-400% improvement in reply volume.

**The Touch 2 backlog by send date (priority order):**

| Cohort | Touch 1 Sent (est.) | Days Since T1 (as of Mar 7) | Touch 2 Status | Priority |
|--------|--------------------|-----------------------------|----------------|----------|
| Feb 27 batch | Feb 27 | 8 days | NOT SENT | **Urgent** |
| Feb 28 batch | Feb 28 | 7 days | NOT SENT | **Urgent** |
| Earlier sends | Various | 10+ days | NOT SENT | High |

**Recommendation:** Execute Touch 2 for all 70 pending contacts via Apollo task queue before sourcing any new contacts. This is the highest-leverage action available today.

### 1.2 Touch 3 Execution Gap

Touch 3 has not been sent to anyone in the sequence through the proper Apollo task queue. The 9 website visitor outreach emails sent on Feb 27 (the original batch) were sent via Gmail outside of Apollo, not via the sequence. This means:

- Touch 2 cadence for those 9 contacts is disconnected from Apollo tracking
- Even if those 9 received a Touch 3, it wasn't logged as a sequence completion

For any contact where Touch 1 was sent more than 10 days ago and Touch 2 has also been sent, Touch 3 is now due.

---

## Section 2: Reply Rate Analysis

### 2.1 Confirmed Performance vs. Benchmarks

| Metric | Current (This Sequence) | Industry Benchmark | Gap |
|--------|------------------------|-------------------|-----|
| Touch 1 reply rate | ~1.1% (1 / 90) | 1-5% | At low end |
| Touch 2 reply rate | N/A (0 sent) | 2-5% | Unmeasured |
| Touch 3 reply rate | N/A (0 sent properly) | 1-3% | Unmeasured |
| Meeting rate from cold email | 0% | 0.5-1% per 100 sends | Behind |
| Bounce rate | 1.1% (1 / 90) | <2% acceptable | Within range |

**The 1.1% Touch 1 reply rate is not inherently a problem.** For cold email with Tier A personalization, 1-2% is a plausible outcome. The problem is that the sequence was never allowed to run its full course — only 1 of 3 planned touches has been executed.

### 2.2 The Single Reply Signal (Pallavi Sheshadri)

The one confirmed reply from all 2026 outreach in this sequence provides meaningful signal:

**What worked:**
- Touch 1 was highly specific to her role (QA automation for risk management platforms)
- She replied three times and shared genuine context about her testing stack (1600+ Playwright tests, cursor.ai usage, Playwright Agent evaluation)
- The personalization approach generated a real technical conversation, not a polite brush-off

**What didn't work:**
- When Rob asked for a demo on March 2, the conversation stopped
- The "demo ask" is the highest-friction conversion step in the BDR process — it's when prospects who were happy to exchange information have to make a commitment decision
- A softer bridge (e.g., "Would a 2-minute video of how this works be useful before we set up a call?") may have kept the conversation alive

**What happened after:**
- Pallavi changed jobs (moved from Origami Risk to Ampersand)
- The thread ended due to life circumstances, not disinterest

**Takeaway for future sequences:** The personalization approach is working. The conversion bridge (exchange → commitment) needs testing. The current CTA ("quick call") is functionally correct per the data, but timing matters — asking for the demo in the same message where they first show engagement may be too fast.

### 2.3 Engagement Tracking Failure

The most critical data problem in the entire operation: **zero engagement data has been logged in the tracking CSV for any send in this sequence.**

Apollo records opens, clicks, and replies at the contact level in the sequence analytics. This data exists but has not been pulled. Without this data:

- It is impossible to calculate true open rate (only possible reply rate)
- Subject line performance cannot be measured
- It is unknown which contacts opened Touch 1 but didn't reply (these are warm signals for Touch 2)
- A/B testing of any kind is impossible

**Estimated impact of missing engagement data:** The contacts who opened Touch 1 but didn't reply are the highest-probability Touch 2 converters. If 15-25% of sends generated an open (conservative for a Tier A personalization sequence), that is 13-22 contacts who saw the email and chose not to reply. Touch 2 should land differently for these contacts than for contacts where there was zero engagement.

**Recommendation:** Pull Apollo sequence analytics for all 90 Touch 1 sends before executing Touch 2. Prioritize Touch 2 sends to contacts who opened but didn't reply.

---

## Section 3: Template Quality Analysis

This section audits the current website_visitor_sequence_drafts.md templates (the "original" Touch 1-2-3 templates used for the 9 Feb 27 sends) against current SOP standards.

### 3.1 Touch 1 Template Audit

**Current Touch 1 (from website_visitor_sequence_drafts.md):**

> Subject: Quick question, {{first_name}}
>
> Hi {{first_name}},
>
> Noticed some folks at {{company}} have been exploring test automation solutions lately — figured it might be worth a quick intro.
>
> I'm Rob with Testsigma. We help engineering teams like yours cut test maintenance by up to 80% with AI-driven test automation that works across web, mobile, and API — all from a single platform.
>
> Would it be worth a 15-minute call to see if there's a fit? Happy to share a quick overview doc instead if that's easier.
>
> Best,
> Rob

**QA Gate Violations:**

| Violation | Category | Severity |
|-----------|----------|----------|
| "Noticed some folks" = HC1 violation ("I noticed" phrasing) | Hard Constraint | FAIL — auto-rewrite required |
| "AI-driven test automation" = HC2 violation (AI as headline feature) | Hard Constraint | FAIL — auto-rewrite required |
| "Would it be worth..." = weak CTA (not "what day works") | SP5 violation | Degrades performance ~26pp vs benchmark |
| "Happy to share a quick overview doc instead if that's easier" = easy-out line | Style rule | Removes commitment pressure, reduces reply rate |
| "We help engineering teams like yours" = generic value prop, not personalized | Personalization | Score 1 (light) |
| "single platform" = corporate phrasing | Plain Language Pass | Should be rewritten |
| "15-minute call" = undersells the meeting | Style rule | Use "quick call" or "quick look" |
| Word count check | ~96 words | PASS (within 80-120 range) |
| Question count | 1 question mark | FAIL — optimal is exactly 2 |

**MQS Score:**
- Opener Clarity: 1/3 (opens with HC1 violation)
- CTA Confidence: 1/3 (weak "would it be worth" + easy out)
- Personalization Density: 1/3 (only company name swapped)
- Friction: 2/3 (word count OK, but single paragraph, no spacing)
- **Total: 5/12 — MUST REWRITE (threshold is 9/12)**

**The Feb 27 sends used this template.** All 9 sends were structurally identical to each other. This means:
1. Zero differentiation across 9 sends (any recipient who talked to another person in the industry could compare notes)
2. All 9 carries HC1 and HC2 violations
3. None passed QA Gate

### 3.2 Touch 2 Template Audit

**Current Touch 2 (from website_visitor_sequence_drafts.md):**

> Subject: Re: Quick question, {{first_name}}
>
> Hi {{first_name}},
>
> Wanted to follow up quickly — I know {{company}} is scaling fast, and in my experience that usually means test suites are growing even faster.
>
> A few things we've been helping similar teams with:
> - Reducing flaky tests with AI-powered self-healing locators
> - Cutting regression cycles from hours to minutes
> - Letting QA teams author tests in plain English (no scripting required)
>
> If any of that resonates, I'd love to walk you through a quick demo. If not, no worries at all.
>
> Best,
> Rob

**QA Gate Violations:**

| Violation | Category | Severity |
|-----------|----------|----------|
| "Reducing flaky tests" — HC5 violation (bullet list) | Hard Constraint | FAIL |
| "flaky tests" = toxic phrase (-11.9pp vs baseline) | Phrase toxicity | FAIL |
| "AI-powered self-healing locators" = HC2 violation | Hard Constraint | FAIL |
| "If not, no worries at all" = easy-out close | Style rule | Removes commitment pressure |
| "I'd love to walk you through" = self-centered framing | Style rule | Reframe to prospect outcome |
| "A few things we've been helping similar teams with:" = feature dump | HC5 | FAIL |
| No proof point with specific numbers | Content standards | FAIL |
| No "what day works" CTA | SP5 | FAIL |
| 3 bullets = HC5 violation | Hard Constraint | FAIL |
| Word count | ~85 words | PASS |
| No named customer | Section 11 standards | FAIL |

**MQS Score:**
- Opener Clarity: 1/3 ("scaling fast" is generic)
- CTA Confidence: 1/3 (easy-out, no "what day works")
- Personalization Density: 1/3 (only company name)
- Friction: 1/3 (bullet list, no paragraph breaks)
- **Total: 4/12 — MUST REWRITE**

### 3.3 Touch 3 Template Audit

**Current Touch 3 (from website_visitor_sequence_drafts.md):**

> Subject: Should I close the loop?
>
> Hi {{first_name}},
>
> I don't want to be that person who keeps emailing, so I'll keep this short — if test automation isn't a priority for {{company}} right now, totally understood.
>
> But if it is and the timing just wasn't right, feel free to bookmark this: [link to Testsigma overview or case study]
>
> Either way, wishing you and the team a great quarter.
>
> Best,
> Rob

**QA Gate Violations:**

| Violation | Category | Severity |
|-----------|----------|----------|
| "I don't want to be that person who keeps emailing" = apologetic framing, easy-out | Style rule | Removes any remaining conversion pressure |
| "totally understood" = easy-out language | Style rule | Signals defeat before asking for anything |
| "feel free to bookmark this" = passive, low-commitment CTA | SP5 violation | No "what day works" |
| No proof point with numbers | Content standards | FAIL |
| Treats Touch 3 as a "goodbye email" rather than a conversion attempt | Framing issue | Full approach needs rethink |
| "wishing you and the team a great quarter" = low-value filler | Style rule | Cut |
| No named customer | Section 12 standards | FAIL |
| Subject "Should I close the loop?" | PASS — this is the correct subject for Touch 3 per Section 12 | |
| Word count | ~67 words | PASS |

**MQS Score:**
- Opener Clarity: 1/3 (apologetic framing signals low confidence)
- CTA Confidence: 1/3 (no "what day works," passive)
- Personalization Density: 1/3 (only company name)
- Friction: 2/3 (short enough, proper spacing)
- **Total: 5/12 — MUST REWRITE**

---

## Section 4: Send Pattern Analysis

### 4.1 Volume and Clustering

| Date | Sends | Notes |
|------|-------|-------|
| Pre-Feb 27 (earlier) | 82 | Enrolled over time, bulk from Feb 28 |
| Feb 27 | 8 (website visitor batch via Gmail) | Sent outside Apollo; HC violations |
| March 6 | 8 (8 remaining from March 6 audit) | Via Apollo task queue |

**The clustering problem:** 82 of 90 sends appear to have occurred as a bulk enrollment rather than a steady daily drip. Sending 40-50 emails in a single day from a domain that normally sends far fewer messages can:
1. Temporarily reduce inbox placement rate (spam filter pressure)
2. Concentrate reply volume in a single window (harder to manage)
3. Create artificial urgency that doesn't reflect a natural outreach pattern

**Recommendation:** For new enrollments, cap the daily send rate at 10-15 contacts per day via the Apollo sequence task queue. This is also better for managing follow-up volumes — 70 simultaneous Touch 2s is harder to handle than 10 per day.

### 4.2 Send Channel Compliance

Of the approximately 90 Touch 1 sends:
- ~8 sent via Gmail directly (the Feb 27 website visitor batch) — outside Apollo, creates tracking gap
- ~82 sent via Apollo task queue — correct channel

The 8 Gmail sends are invisible to Apollo's sequence analytics. This means:
- Open/click data is unavailable for those 8 contacts
- Apollo will still show them as "at Step 2" even though they've technically received Touch 1
- Touch 2 must be sent to them via Apollo task queue with a note that Touch 1 was manually sent via Gmail

**Recommendation:** Per the SOP (March 1, 2026 update), Apollo task queue is the mandatory send method. No future sends from this sequence should go through Gmail compose.

---

## Section 5: Subject Line Analysis

The sequence currently uses a single subject line: **"Quick question, {{first_name}}"**

**What the data says about "Quick question" style subjects:**

This is one of the most widely used cold email subject lines in B2B outreach. Its strengths and weaknesses are well-documented:

- **Historically strong open rates:** The curiosity-without-commitment format opens well
- **Overused and increasingly filtered:** When thousands of BDRs use the same subject line format, spam filters and prospect pattern recognition both flag it
- **Not differentiated:** Every person who receives a "Quick question, Rob" email from any BDR in any product category sees the same frame

**Observed impact:** No data available on open rates for this specific sequence (engagement tracking not maintained). However, the 1.1% reply rate is consistent with a subject line that opens adequately but where the email body does not convert.

**Testing recommendation:** A/B test two variants against the control:
- **Variant A (domain-specific):** "[Company] + Testsigma" — company-first curiosity frame
- **Variant B (problem-framed):** A specific pain point as subject (e.g., "Regression debt at [Company]?" or "Testing coverage after the migration?")

Test each variant across 20 sends, compare open-to-reply conversion. Note: open data requires Apollo engagement tracking to be maintained.

---

## Section 6: Targeting Quality Assessment

### 6.1 ICP Match

The 9-contact sample from website_visitor_sequence_drafts.md shows:

| Name | Title | Company | ICP Match | Notes |
|------|-------|---------|-----------|-------|
| Andy Nelsen | QA Architect | Rightworks | Strong | Architect persona = 39.3% reply rate benchmark |
| Jeff Barnes | Test Engineering Manager | Digi International | Strong | Manager persona = 26.8% benchmark |
| Eduardo Menezes | Sr QA Manager | Fulgent Genetics | Moderate | Healthcare/lab QA — may not be software QA |
| Jose Moreno | QA Architect | Flywire | Strong | FinTech + Architect = high priority |
| Eyal Luxenburg | SW Engineering Manager | Island | Moderate | Engineering Manager is secondary persona |
| Todd Willms | Director of Engineering | Bynder | Moderate | Director of Engineering = secondary persona |
| Jason Ruan | Director of Engineering | Binance | Strong | FinTech + Director = strong ICP |
| Tom Yang | Director of Engineering | Versant Media | Moderate | Media vertical; DNC'd (Tom Yang flagged) |
| Hibatullah Ahmed | Engineering Manager | SPS Commerce | Strong | Manager level, SaaS vertical |

**ICP quality assessment:** 5 of 9 are strong ICP matches. 3 are moderate (Engineering Manager / Director of Engineering with no explicit QA scope). 1 is flagged as DNC.

**Opportunity:** The website visitor signal is the strongest possible trigger for this sequence. These contacts visited testsigma.com — they already have some awareness. The personalization approach should lean harder into that signal ("noticed your team was exploring...") BUT without using HC1 phrasing ("I noticed"). See corrected framing in the rewrite recommendations below.

### 6.2 Deliverability Risk Flags

From the original sequence notes:
- **Jose Moreno (Flywire)** — catchall domain. Catchall domains accept all email regardless of whether the address exists, so deliverability is less certain.
- **Todd Willms (Bynder)** — catchall domain. Same risk.
- **Eyal Luxenburg (Island)** — Israel-based. Timezone consideration: sending from US business hours may land at off-hours for him.

---

## Section 7: Prioritized Improvement Plan

The improvements below are ordered by expected impact (highest first). All are actionable within the current week.

### Priority 1 — Execute Touch 2 for 70 pending contacts (IMMEDIATE, HIGH IMPACT)

Every day without Touch 2 is leaving the highest-reply-probability window on the table. The data says 53.7% of replies come by message 2. This is the single highest-leverage action.

**How:** Apollo task queue → Q1 Website Visitor - Tier 1 Intent → Step 2 tasks
**Target:** 15-20 per day until the backlog is cleared
**Draft requirement:** Touch 2 drafts must pass QA Gate (Section 11). The current Touch 2 template has 5+ HC violations and scores 4/12 on MQS. Do not use the current template for Touch 2.

### Priority 2 — Pull Apollo engagement data before sending Touch 2 (IMMEDIATE, HIGH IMPACT)

Apollo records opens and clicks at the contact level. Before sending Touch 2, pull the open/click status for all 70 pending contacts. Prioritize:
1. Contacts who opened and clicked (highest engagement)
2. Contacts who opened but didn't click
3. Contacts with no open (may have been buried or missed)

**How:** Apollo → Sequences → Q1 Website Visitor → Contacts tab → Check email status column

### Priority 3 — Rewrite all three touch templates to pass QA Gate (THIS WEEK, HIGH IMPACT)

All three current templates fail the QA Gate with scores of 4-5/12. The new SOP (Sections 11 and 12) defines the correct standards. New templates are needed before any further sends — Touch 2 sends using the current template will underperform.

**Template requirements:**
- Touch 1: MQS >= 9/12, exactly 2 question marks, 80-120 words, specific proof point with named customer, "what day works" close tied to proof point outcome
- Touch 2: 40-70 words, "One more thought, [First Name]," as opener, reply thread, different proof point than Touch 1, light close
- Touch 3: 40-60 words, "Should I close the loop?" subject, new thread, third different proof point, confident (not apologetic) close

**Note on the website visitor angle:** The HC1 rule ("I noticed") prohibits using the website visitor signal directly in the message body. The signal informs targeting and priority but should not appear in the email copy. The message should start with a QA situation the prospect would recognize — not by referencing that they visited the website.

### Priority 4 — Maintain engagement tracking going forward (THIS WEEK, MEDIUM IMPACT — DATA)

After each Apollo task queue session, spend 5-10 minutes pulling engagement data:
1. Apollo → Sequences → Q1 Website Visitor → Contacts
2. Check Opened?, Clicked?, Replied? columns for all contacts sent in the last 7 days
3. Update email_outreach_tracker.csv or batch tracker accordingly

This data is the only way to measure the sequence's true performance and run any meaningful A/B testing.

### Priority 5 — A/B test subject lines on next new-enrollment batch (SHORT TERM)

For the next batch of website visitor contacts enrolled in this sequence, split into two groups:
- Group A: "Quick question, {{first_name}}" (current control)
- Group B: Pain-framed subject (e.g., "Regression coverage at {{company}}?" or "Test coverage signal from {{company}}")

Run 20 sends per group. Compare open-to-reply conversion. Maintain Apollo engagement tracking during the test.

### Priority 6 — A/B test Touch 2 CTA (SHORT TERM)

The current Touch 2 CTA ("I'd love to walk you through a demo") is a known underperformer (self-centered framing, easy-out, no "what day works"). Two CTA variants to test:

- **Variant A:** "What day works to see how [Customer] [achieved outcome]?" (direct "what day works" per SP5)
- **Variant B:** "Would a 2-minute Loom of how this works for [Company's] stack be useful?" (softer, lower commitment — tests the Pallavi lesson about meeting ask timing)

### Priority 7 — Fix Kenny Liu bounce and identify replacement (SHORT TERM)

Kenny Liu (ModMed) is confirmed as a hard bounce. The slot should be filled:
1. Search Apollo for a current QA/Engineering contact at ModMed
2. Verify the email address format against other @modmed.com addresses
3. Enrich via Apollo person enrichment
4. Enroll in the sequence with the corrected contact

### Priority 8 — Add Apollo timeline notes for 8 Gmail sends (SHORT TERM)

The 8 contacts sent via Gmail on Feb 27 need manual Apollo notes added so the sequence tracking remains accurate:

Template: "Email sent via Gmail Feb 27, 2026 — subject: Quick question, [First Name] — sent outside Apollo task queue. Do not re-send Step 1 via Apollo for this contact."

---

## Section 8: Performance Targets (30-Day)

| Metric | Current | Target (30 Days) | How to Get There |
|--------|---------|-----------------|------------------|
| Touch 1 reply rate | ~1.1% | 2-3% | Rewritten templates + better proof point matching |
| Touch 2 reply rate | Unmeasured (0 sent) | 3-5% | Execute backlog + use compliant templates |
| Touch 3 reply rate | Unmeasured (0 sent) | 1-3% | Execute after Touch 2 completion |
| Total replies (active sequence) | 1 | 4-8 | Full 3-touch execution across 70+ contacts |
| Meetings booked from sequence | 0 | 1-2 | Follows from reply rate improvement |
| Engagement tracking coverage | 0% | 100% of sends | Pull Apollo analytics after each session |
| Template compliance (QA Gate) | 0% pass rate | 100% pass rate | Rewrite all three touches |
| Open rate (estimated) | Unknown | Establish baseline | Requires engagement tracking |

---

## Section 9: What Is Working — Do Not Change

1. **Website visitor targeting logic is correct.** These contacts showed intent by visiting testsigma.com. This is a higher-quality signal than cold outbound. The sequence structure (email-only, 3 touches) is appropriate for this intent level.

2. **The personalization approach (when used) generates real conversations.** Pallavi's engagement — three substantive replies about specific testing details — confirms that when the outreach is specific and relevant, prospects engage. The problem is not the concept; it is the template execution.

3. **The proof points in the knowledge base are strong.** Hansard, CRED, Sanofi, Medibuddy — these are all real, specific, credible outcomes. The issue is that the current templates either don't use them or use them incorrectly (as feature bullets rather than proof-tied closes).

4. **The Apollo sequence infrastructure is correct.** Three steps, the correct cadence timing, the correct send account (robert.gorham@testsigma.net). The mechanical setup is fine. The problem is execution speed and template quality.

5. **Subject line "Should I close the loop?" for Touch 3 is correct.** Per Section 12 of the SOP, this subject is the standard for Touch 3 across the sequence. Keep it.

---

## Appendix: Data Sources

- `email_outreach_tracker.csv` — 77 rows of 2026 sends; engagement fields empty
- `sequence_performance_analysis_mar6.md` — Live Apollo data as of March 6
- `website_visitor_sequence_drafts.md` — Original templates (all fail QA Gate)
- Gmail inbox audit (robert.gorham@testsigma.com) — 1 confirmed reply (Pallavi Sheshadri)
- CLAUDE.md outbound intelligence data — benchmarks and phrase-level performance data
- Tier1_Intent_Sequence_SOP_MASTER.md — SOP standards for QA Gate comparison

---

*Audit prepared: March 7, 2026*
*Next review: March 21, 2026 (after Touch 2 execution + 2 weeks of tracking data)*
