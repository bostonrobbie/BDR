# Batch QA Verification SOP

**Version:** 1.0
**Created:** 2026-03-01
**Owner:** Rob Gorham, BDR @ Testsigma
**Purpose:** Standalone, repeatable quality assurance process for every outreach batch before send approval. Run this after message drafting (Phase 5) and before batch assembly (Phase 7).

---

## How to Use This SOP

This document is designed to be run as a standalone verification process. It can be:
- Uploaded to Cowork as a skill or reference document
- Added to CLAUDE.md as an isolated section
- Committed to the repo as a repeatable workflow

**Trigger:** Run after every batch of prospect messages is drafted, before any messages are approved for send.

**Input:** HTML batch tracker file with prospect cards and messages (all 3 touches per prospect).

**Output:** QA-verified batch with all messages scoring MQS >= 9/12, zero Hard Constraint violations, and all structural checks passing.

---

## Phase 1: Pre-Audit Setup (2 min)

### 1.1 Load the Batch
- Open the batch HTML tracker file
- Confirm total prospect count matches expected batch size (typically 20-25)
- Extract all message data (Touch 1, Touch 2, Touch 3 per prospect)

### 1.2 Load Reference Data
- Confirm research data exists for every prospect (3 sources: LinkedIn, Apollo, Company External)
- Confirm each prospect has a defined theme sentence (Pre-Draft Step 1)
- Confirm proof point assignments exist for all 3 touches per prospect

### 1.3 Set Pass Threshold
- MQS >= 9/12 required for every individual touch
- Zero Hard Constraint violations across entire batch
- All 14 structural checks must pass

---

## Phase 2: Hard Constraint Scan (10 min)

Check EVERY message (all touches, all prospects) against these 10 Hard Constraints. Any single violation = automatic rewrite of that message.

| HC# | Constraint | Detection Method | Data Basis |
|-----|-----------|-----------------|------------|
| HC1 | No "I noticed" / "I saw" / "I see" | Text search for exact phrases | -13.4 pp differential |
| HC2 | No AI/ML/self-healing in first 2 sentences | Read first 2 sentences of each message. Flag: "AI," "ML," "machine learning," "self-healing," "auto-heal," "artificial intelligence" | -9.2 pp differential |
| HC3 | No messages over 120 words (body only, exclude signature) | Word count of message body | 150+ words = 21.2% reply rate |
| HC4 | No evening sends (after 6 PM) | Check send time recommendations | -44.4 pp difference |
| HC5 | No bullet-point or numbered-list feature dumps | Visual scan for bullets, numbered lists, feature lists | -2.2 pp differential |
| HC6 | No "would it be unreasonable" as sole CTA | Text search | 12.8% reply rate |
| HC7 | No phone-number asks | Text search for "number," "phone," "call me," "drop my #" | 5.0% reply rate |
| HC8 | No "reaching out" / "wanted to connect" | Text search | -2.4 pp differential |
| HC9 | No "I figure" / "would you like to share" / "enough about me" | Text search for exact phrases | -19.0 pp, -13.6 pp, -10.6 pp |
| HC10 | No 3+ question marks per message | Count "?" in each message | 3 Qs = 14.3% vs 2 Qs = 34.8% |

### HC Scan Output
For each violation found, log:
```
[HC#] [Prospect Name] [Touch #] — "[violating phrase]" — REWRITE REQUIRED
```

### HC Remediation
- HC1: Remove "I noticed/saw/see" and rewrite opener to lead with a QA situation question
- HC2: Move AI/ML mention to context paragraph (sentence 3+). Lead with outcome in first 2 sentences
- HC3: Cut to 80-110 words. Remove filler phrases, redundant context, or over-explained proof points
- HC5: Rewrite feature list as a single proof point sentence
- HC6/HC7: Replace with "what day works" CTA tied to proof point outcome
- HC8/HC9: Delete phrase and rewrite surrounding sentence
- HC10: Reduce to exactly 2 question marks for Touch 1, 1-2 for Touch 2/3

---

## Phase 3: MQS Scoring (15 min)

Score every message on 4 dimensions (1-3 each). Maximum = 12 per message.

### Dimension 1: Opener Clarity (1-3)

| Score | Criteria | Example |
|-------|----------|---------|
| 3 | Specific, insight-driven question about the prospect's situation. No "I noticed," no role-recap, no "reaching out." References something QA-relevant from research. | "Are flaky Selenium tests slowing your releases or just eating engineering time?" |
| 2 | Company-specific reference but generic frame. May include mild role reference. | "Directing QA at [Company]'s platform, what's harder right now?" |
| 1 | Opens with "I noticed," "Seeing that you're the [Title]," or "Are you looking for..." Template-visible. | "I saw you've been leading QA at [Company]..." |

### Dimension 2: CTA Confidence (1-3)

| Score | Criteria | Example |
|-------|----------|---------|
| 3 | "What day works" + direct tie to proof point outcome + prospect's specific situation. Close cannot be pasted into another message unchanged. | "If cutting regression from 8 to 5 weeks would help the OpenEdge schedule, what day works for a quick look at how Hansard did it?" |
| 2 | Uses "what day works" but weak tie to proof point (generic outcome, no prospect situation). | "What day works for a quick look at how they cut testing time?" |
| 1 | Generic close, open-ended question, no proof point tie, no meeting ask. | "Worth comparing notes?" / "Would exploring that be worth your time?" |

**CTA Scoring Checklist (all 3 must be YES for score of 3):**
- [ ] Contains "what day works" (or close variant)
- [ ] References the SPECIFIC outcome from the proof point (number, timeframe, or result)
- [ ] Connects that outcome to THIS prospect's specific situation (their product, event, constraint)

### Dimension 3: Personalization Density (1-3)

| Score | Criteria | Example |
|-------|----------|---------|
| 3 | References something only THIS person would recognize (specific project, company event, platform migration, QA hiring signal). | "With the Vega Discover integration expanding your test surface..." |
| 2 | References their company specifically but opener could apply to anyone in that role. | "Directing QA at Ally's digital banking platform..." |
| 1 | Only swaps name, title, company. Indistinguishable from a template. | "As a QA Manager, you probably deal with..." |

### Dimension 4: Friction (1-3, inverted: 3 = low friction)

| Score | Criteria |
|-------|----------|
| 3 | 80-110 words, one proof point, one CTA, exactly 2 questions (Touch 1), no bullet lists, 4+ paragraph breaks, max 1 hyphen in body |
| 2 | 110-120 words, may have 2 proof points, still readable, proper spacing |
| 1 | Over 120 words, bullet-point features, multiple CTAs, 3+ questions, wall-of-text, 2+ hyphens as dashes |

### MQS Computation
```
MQS = Opener + CTA + Personalization + Friction
Minimum to pass: 9/12
Target: 10-12/12
```

### MQS Output Format
For each prospect, log:
```
[Name] @ [Company]
  Touch 1: [O]/[C]/[P]/[F] = [Total]/12 [PASS/FAIL]
  Touch 2: [O]/[C]/[P]/[F] = [Total]/12 [PASS/FAIL]
  Touch 3: [O]/[C]/[P]/[F] = [Total]/12 [PASS/FAIL]
  Overall: [PASS/FAIL]
```

---

## Phase 4: Structural Checks (10 min)

These checks apply at the BATCH level, not individual message level.

### Check 1: Close Deduplication
- Extract the close (last 1-2 sentences) from every Touch 1 message in the batch
- No two closes may use the same sentence structure
- Closes must rotate across these 5 patterns:

| Pattern | Template |
|---------|----------|
| 1 | "If [outcome] would help [their situation], what day works for a quick look at how they did it?" |
| 2 | "What day works to see how [customer] [achieved outcome] while [solving their version of the problem]?" |
| 3 | "If [outcome] before [their event/deadline] sounds useful, what day works for a quick look?" |
| 4 | "What day works to compare how [customer] [achieved outcome] without [their constraint]?" |
| 5 | "If getting [specific number] back in your [their process] would help, what day works for a quick chat?" |

**Rotation rule:** For a 25-prospect batch, each pattern should be used 5 times. Assign patterns by prospect index: prospects 1-5 get Pattern 1, 6-10 get Pattern 2, etc.

**FAIL condition:** Any two prospects sharing structurally identical closes.

### Check 2: Proof Point Rotation
- For each prospect, verify Touch 1, Touch 2, and Touch 3 each use a DIFFERENT proof point
- No prospect should receive the same customer story or stat twice in their sequence

**Available proof points for rotation:**
| ID | Proof Point | Best Verticals |
|----|------------|----------------|
| PP1 | Hansard: regression 8wk to 5wk | Insurance, FinServ, long regression |
| PP2 | Medibuddy: 2,500 tests, 50% maintenance cut | Healthcare, mid-size scaling |
| PP3 | CRED: 90% regression automation, 5X faster | FinTech, high-velocity |
| PP4 | Sanofi: 3 days to 80 minutes | Pharma, compliance-heavy |
| PP5 | Fortune 100: 3X productivity | Enterprise VP-level |
| PP6 | Nagra DTV: 2,500 tests in 8 months, 4X faster | Media, API + UI |
| PP7 | Spendflo: 50% manual testing cut | SaaS, small teams |
| PP8 | 70% maintenance reduction vs Selenium | Teams on Selenium |
| PP9 | 90% maintenance reduction (self-healing) | Flaky test complaints |
| PP10 | Cisco: 35% regression reduction | Enterprise, large QA |
| PP11 | Meesho: 4X faster automation | E-commerce, rapid growth |
| PP12 | Freshworks: reduced flakiness at scale | SaaS, mid-to-large |

**FAIL condition:** Any prospect receiving the same proof point in more than one touch.

### Check 3: No Duplicate Messages
- Compare all messages in the batch for structural similarity
- Flag any two messages that share >60% identical phrasing (excluding names/companies)
- The "stitched template" test: if you can swap the prospect name/company and the message still makes sense for a different prospect, it's too generic

### Check 4: Word Count Compliance
| Touch | Minimum | Optimal | Maximum |
|-------|---------|---------|---------|
| Touch 1 | 80 | 95-110 | 120 |
| Touch 2 | 40 | 50-60 | 70 |
| Touch 3 | 60 | 70-85 | 100 |

**Count body words only.** Exclude signature line ("Rob Gorham" etc.).

### Check 5: Question Mark Count
- Touch 1: Exactly 2 question marks
- Touch 2: 1-2 question marks
- Touch 3: 1-2 question marks

### Check 6: Hyphen Audit
- Count hyphens used as mid-sentence dashes in each message body (exclude signature, exclude compound words like "self-healing")
- Maximum 1 hyphen-as-dash per message body
- Any message with 2+ hyphens as dashes: rewrite to replace with commas

### Check 7: Paragraph Spacing
- Every message must have at least 4 paragraph breaks (blank lines)
- Opener, context, proof point, and close must each be visually separate
- No paragraph exceeds 3 sentences
- Must be scannable on mobile

### Check 8: Phrase Toxicity Scan
Flag any message containing these toxic phrases:

| Phrase | Penalty |
|--------|---------|
| "I noticed" / "I saw" / "I see" | -13.4 pp (also HC1) |
| "flaky tests" (as hook) | -11.9 pp |
| "I figure" | -19.0 pp |
| "would you like to share" | -13.6 pp |
| "enough about me" | -10.6 pp |
| "CI/CD" | -5.1 pp |
| "low code" / "no code" (as feature lead) | -2.9 pp |
| "reaching out" | -2.4 pp |
| "300% faster" / multiplier claims | -12.4 pp vs reduction framing |

### Check 9: CTA Validation (Detailed)
Every close must satisfy ALL of these:
- [ ] Contains "what day works" (or close variant like "what day works to see," "what day works for a quick look")
- [ ] References SPECIFIC outcome from proof point (a number, timeframe, or named result)
- [ ] Connects that outcome to prospect's specific situation (their product, their event, their constraint)
- [ ] Is NOT a generic close that could go in any message
- [ ] Is NOT an open-ended question close (DATA: 14.0% vs "what day works" at 40.4%)

**Banned closes (automatic fail):**
- "Worth comparing notes?"
- "Worth a quick chat?"
- "Would exploring that be worth your time?"
- "Thought it would be worth connecting."
- Any close that works unchanged for a different prospect

### Check 10: Research Depth
- Every prospect must have research from all 3 sources: LinkedIn profile, Apollo enrichment, Company external
- Each research bullet should be tagged with which message element it feeds (opener, context, proof match, close)
- If any source is missing, the prospect cannot be included

### Check 11: Angle Rotation
- No prospect may receive the same angle (pain hook) in more than one touch
- Touch 1 angle, Touch 2 angle, and Touch 3 angle must each approach from a different direction
- Example: Touch 1 = maintenance pain, Touch 2 = coverage gaps, Touch 3 = release velocity

### Check 12: Evidence Check
- Every personalization claim in a message must have a corresponding research source
- If the opener references a platform migration, there must be a research note confirming that migration
- No fabricated or assumed claims

### Check 13: C2 Structure Compliance
- Every Touch 1 must have all 5 elements: subject line, opener, context, proof point, close
- No message should exhibit the "stitched template" anti-pattern:
  - Opener with 2+ disconnected company facts
  - Generic connector phrase ("That's the squeeze most teams feel")
  - Proof point that could go in any message
  - Generic close with no proof point tie-in

### Check 14: Batch-Level Diversity
- No more than 2 prospects from the same company
- Vertical diversity: no more than 8 from the same vertical
- Persona mix: verify Prospect Mix Ratio (10-12 Manager/Lead, 4-6 Director, 3-5 Architect, 2-3 Buyer Intent, max 2 VP)

---

## Phase 5: Remediation (20-40 min)

For any message failing MQS threshold or structural checks:

### 5.1 Prioritize Fixes by Impact
1. **Hard Constraint violations** — Fix first. These are automatic fails.
2. **CTA dimension (score 1/3)** — Most common failure driver. Rewrite close using the 3-question method from Pre-Draft Step 4.
3. **Personalization dimension (score 1/3)** — Rewrite opener to reference QA-relevant research specific to this person.
4. **Proof point reuse** — Reassign proof points so each touch uses a different one.
5. **Close deduplication** — Reassign close patterns using the 5-pattern rotation.
6. **Word count / friction** — Trim or expand to optimal range.

### 5.2 Close Rewrite Method
For every close scoring below 3/3, answer these 3 questions before rewriting:

1. **What specific outcome did the proof point achieve?**
   Example: "cut regression from 8 to 5 weeks"

2. **What is the prospect's version of that problem?**
   Example: "OpenEdge release schedule pressure"

3. **How do I connect #1 to #2 and end with 'what day works'?**
   Example: "If 3 fewer weeks of regression would help the OpenEdge schedule, what day works for a quick look at how they did it?"

### 5.3 Opener Rewrite Method
For openers scoring below 3/3:
- Start with a QA situation the prospect would recognize from research
- Ask a real question (not a rhetorical one)
- Do NOT start with products, company facts, or background
- Do NOT use "I noticed" or reference the prospect's profile directly

### 5.4 Re-Score After Fixes
After fixing all flagged messages, re-run the full MQS scoring (Phase 3) on every changed message. Confirm all now score >= 9/12.

---

## Phase 6: Final Verification (5 min)

### 6.1 Batch Summary Report
Generate a summary with:
```
BATCH [#] QA VERIFICATION REPORT
=================================
Date: [date]
Total Prospects: [N]
Total Touches Audited: [N x 3]

HARD CONSTRAINTS
  Violations found: [N]
  Violations fixed: [N]
  Remaining: 0 (required)

MQS SCORES
  Average MQS: [X]/12
  Lowest MQS: [X]/12
  Passes (>= 9): [N]/[N] (must be 100%)

DIMENSION AVERAGES
  Opener Clarity: [X]/3
  CTA Confidence: [X]/3
  Personalization: [X]/3
  Friction: [X]/3

STRUCTURAL CHECKS
  Close dedup: PASS/FAIL
  Proof point rotation: PASS/FAIL
  Word count compliance: PASS/FAIL
  Question mark count: PASS/FAIL
  Hyphen audit: PASS/FAIL
  Paragraph spacing: PASS/FAIL
  Phrase toxicity: PASS/FAIL
  C2 structure: PASS/FAIL

BATCH STATUS: READY FOR SEND / BLOCKED
```

### 6.2 Sign-Off Criteria
ALL of these must be true before marking batch as READY FOR SEND:
- [ ] 0 Hard Constraint violations
- [ ] 100% of messages score MQS >= 9/12
- [ ] All 14 structural checks pass
- [ ] Close patterns rotated across 5 patterns (no duplicates)
- [ ] Proof points unique per prospect per touch
- [ ] Research from 3 sources for every prospect
- [ ] Word counts within spec for all touches
- [ ] Exactly 2 question marks in every Touch 1

---

## Common Failure Patterns & Fixes

These are the most frequently observed failures across batches. Check for these first to save time.

### Pattern 1: Identical Closes (Batch 9 Finding)
**Symptom:** All or most Touch 1 closes use the same sentence structure.
**Root Cause:** Message generation used a single close template without rotation.
**Fix:** Assign close Pattern 1-5 explicitly to each prospect before drafting. For 25 prospects, 5 prospects per pattern.

### Pattern 2: Weak CTA (1/3 Score)
**Symptom:** Closes say "what day works" but don't name the customer or tie the specific outcome number to the prospect's situation.
**Root Cause:** Close was written generically without completing Pre-Draft Step 4.
**Fix:** For every close, answer the 3 questions (what outcome, what's their version, how to connect). The close must name or reference the proof point outcome AND the prospect's specific context.

### Pattern 3: Proof Point Reuse
**Symptom:** Touch 2 uses the same customer story as Touch 1.
**Root Cause:** Proof points weren't pre-assigned per touch before drafting.
**Fix:** Before writing any messages, create a proof point assignment table:
```
Prospect | Touch 1 PP | Touch 2 PP | Touch 3 PP
---------|-----------|-----------|----------
Sean T.  | Hansard   | CRED      | Sanofi
Parth V. | Sanofi    | Medibuddy | Hansard
...
```

### Pattern 4: HC2 Violation (AI in First 2 Sentences)
**Symptom:** Touch 2 messages often open with "One thing that helped [Customer] was AI test generation..."
**Root Cause:** Natural tendency to lead with the differentiator feature.
**Fix:** Lead with the OUTCOME in sentences 1-2. Move the mechanism (AI, NLP, self-healing) to sentence 3+.
- BAD: "One thing that helped Medibuddy was AI test generation from plain English..."
- GOOD: "One thing that helped Medibuddy was faster test creation. Because they could write tests in plain English instead of hand-coding, their team built 2,500 tests in 8 months."

### Pattern 5: Template-Visible Openers (1/3 Personalization)
**Symptom:** Openers swap name/title/company but could apply to anyone in that role.
**Root Cause:** Research wasn't deep enough or wasn't connected to the opener.
**Fix:** The opener must reference a QA-relevant signal from research that is specific to THIS person's situation (their product, their platform, their team's challenge).

---

## Continuous Improvement Loop

### After Every Batch Send
1. Track which messages got replies (positive, negative, referral)
2. Tag what triggered the reply (opener, pain hook, proof point, timing, referral)
3. Note the MQS score of messages that got replies vs. those that didn't
4. Note the personalization score (1-3) of messages that got replies

### After Every 3 Batches
1. Compare reply rates by MQS score range (9-10 vs 11-12)
2. Compare reply rates by personalization score (1 vs 2 vs 3)
3. Compare reply rates by close pattern (Pattern 1-5)
4. Compare reply rates by proof point used
5. Compare reply rates by opener style

### Update This SOP When
- A new failure pattern is discovered across 2+ batches (add to Common Failure Patterns)
- Reply rate data reveals a new toxic phrase or underperforming pattern (add to Phrase Toxicity Scan)
- A new proof point becomes available (add to proof point rotation table)
- A Hard Constraint is added or modified based on data (update HC table)
- The MQS threshold changes (update pass threshold)

### Version Log
| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-01 | Initial SOP created from Batch 9 QA audit findings |

---

## Quick Reference Card

**For daily use, check these 5 things on every batch:**

1. **Zero HC violations** — Run text search for all 10 HC patterns
2. **Every close ties proof point outcome to prospect situation + "what day works"** — Read every close manually
3. **No two closes structurally identical** — Compare all Touch 1 closes side by side
4. **Every touch uses a different proof point** — Check proof point assignments per prospect
5. **MQS >= 9/12 on every message** — Score all 4 dimensions, fix any below threshold

**If the batch passes all 5, it's ready for send approval.**
