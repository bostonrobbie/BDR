# Playbook: T2 Follow-Up Drafting

## When to Use
When T2 (Touch 2) tasks surface in Apollo's task queue, typically Day 5 after T1 was sent.

---

## Cadence Rules

| Touch | Earliest | Typical | Latest |
|-------|----------|---------|--------|
| T2 | Day 4 from T1 | Day 5 from T1 | Day 8 from T1 |

**HARD RULE:** Touch 2 NOT before Day 4 of the sequence. Violating this was INC-001.

---

## T2 Email Formula — Deep-Dive v4 (canonical source: sop-tam-outbound.md Part 7, Updated Mar 12)

### Structure (4 parts, 140-190 words total)

T2 is intentionally **longer than T1**. It goes deeper on pain, pitches the solution, and tells a customer story. Every word must earn its spot.

**Threading:** Send as a reply to the T1 thread when possible. Having T1 visible adds context and improves open rates.

**Tone:** Casual, direct, plain language. No enterprise-speak. Write like a real person, not a template.

---

**Part 1 — "I imagine" + deeper pain speculation (~2-3 sentences)**
Build directly on the T1 angle but go one level deeper. T1 named the problem; T2 describes what that problem actually FEELS like day-to-day for THIS person in THIS role at THIS company.
- Reference specific details from T1 (their tech stack, migration, team structure, company trigger)
- Speculate on the downstream consequences they're living with
- Make it specific enough that they think "yeah, that's exactly right"
- OPEN with "I imagine..." — this is the mandatory entry phrase

**Part 2 — Testsigma solution pitch (~2 sentences)**
NOT a generic pitch. Directly answer the specific pain from Part 1. Connect the feature to the pain so the "why" is obvious. Match the feature to the pain:
- Plain English tests (no framework lock-in) → use when pain is framework migration or dual-stack maintenance
- AI self-healing (auto-fixes locators) → use when pain is maintenance overhead or test brittleness
- NLP test creation → use when pain is test creation speed or coverage gaps
- Unified platform → use when pain is toolchain fragmentation

**Part 3 — Customer story (~2 sentences)**
Name a specific Testsigma customer that maps to their situation. Explain WHY this customer is relevant (similar industry, similar challenge, similar scale), give the outcome, and add one insight about what changed for them beyond the headline metric.

**Part 4 — Tie-back CTA (~1-2 sentences)**
Reference "what I mentioned last time" or the T1 topic explicitly. Then ask for **15 minutes** to walk through the customer story and see if it applies to their situation.

---

### CTA Phrasing (15-minute meeting ask — mandatory for T2)

- "Would 15 minutes make sense to walk through how [Customer] made that shift and see if it applies?"
- "Would 15 minutes be worth it to see how [Customer] handled [their exact problem] and whether there's a fit?"
- "If [pain from Part 1] is real for your team, would 15 minutes make sense to walk through what [Customer] did?"

**Note:** T2 CTA is a 15-minute meeting ask — NOT an engagement question. Engagement question CTAs belong to T1. Save "What day works" for T3 if needed.

---

### BANNED Phrases (non-negotiable, hard fail)

- "Circling back" / "Following up" / "Reaching back out"
- "Different lens from my last note"
- "One more angle worth adding/sharing"
- "Thought this was worth adding"
- Any bridge/opener that apologizes for taking up space
- No em dashes (—) anywhere

---

### Word Count: 140-190 words

- T2 is longer than T1 (75-100 words) by design
- Minimum 140 words — if under, expand Part 1 pain speculation or Part 3 customer story context
- Maximum 190 words — cut from Part 2 pitch if over

---

### Subject Line

- Reply format: "Re: [T1 subject]" — use when threading in Apollo
- Fresh subject (if not threaded): Same SMYKM personal format as T1 but with a different angle

---

## Process

### Step 1: Check which T2s are due
Open Apollo Tasks tab. Filter by sequence "TAM Outbound" and look for Step 2 tasks.

Or calculate from MASTER_SENT_LIST.csv:
- Find all contacts with send_date 5-8 days ago
- Those are due for T2

### Step 2: Pull T1 content for each contact
Open the relevant batch tracker HTML. For each contact due for T2:
- Read their T1 subject and body
- Note which proof point was used (MUST use a different one for T2)
- Note their company, title, trigger, tech stack, and any research notes

### Step 3: Draft T2 for each contact
Using the Deep-Dive v4 formula above:
- Write Part 1: "I imagine" + deeper day-to-day pain (reference T1 specifics)
- Write Part 2: Testsigma solution matched to that pain
- Write Part 3: Customer story with WHY they're relevant + metric + insight
- Write Part 4: T1 callback + 15-min CTA
- Keep to 140-190 words
- NO banned phrases — re-read before submitting

### Step 4: QA Gate the T2

| # | Check | Points |
|---|-------|--------|
| 1 | Word count 140-190 | 1 |
| 2 | "I imagine" opener in Part 1 | 1 |
| 3 | Different proof point from T1 | 1 |
| 4 | No banned phrases ("Circling back" etc.) | 1 |
| 5 | Named customer with specific metric | 1 |
| 6 | WHY customer story is relevant to them | 1 |
| 7 | 15-minute CTA (not engagement question) | 1 |
| 8 | No placeholder text | 1 |
| 9 | No em dashes | 1 |

**Pass threshold:** 7/9

### Step 5: Add to tracker or create T2 draft file
Either:
- Add T2 draft section to the existing batch tracker HTML (below each contact's T1 draft)
- Or create a separate T2 draft file: `tamob-t2-drafts-{date}.html`

### Step 6: Present for APPROVE SEND
Same as T1: show Rob the drafts, wait for APPROVE SEND, then send via Apollo task queue using INC-012 two-gate protocol.

---

## T2 Proof Point Rotation

**Rotation table (T1 used → T2 should use):**
- T1: Hansard (regression 8→5 weeks) → T2: CRED (90% coverage, 5x faster) or MediBuddy (50% maintenance cut)
- T1: Fortune 100 / 3x productivity → T2: Cisco (35% regression reduction) or Hansard
- T1: Nagra DTV (2,500 tests, 4x faster) → T2: CRED or MediBuddy
- T1: CRED → T2: Hansard or MediBuddy
- T1: MediBuddy → T2: CRED or Cisco

**Rule:** Different customer story, different metric, but relevant to the same industry if possible.

---

## Reference Example (validated Mar 12, 168 words)

**Rick Brandt — Director of QA, Cboe Global Markets**
T1 angle: Dual Selenium/Playwright migration, maintenance overhead, hiring for Playwright on clearing systems
T1 proof point: Hansard (8→5 week regression)

**T2:**

> Rick,
>
> I imagine running two frameworks at once at Cboe means your team is fighting two separate maintenance queues that never sync up. Locator breaks from the Selenium side don't line up with Playwright issues on the newer clearing systems, and your engineers are context-switching between both every sprint instead of building new coverage.
>
> That's exactly the kind of problem Testsigma was built for. Tests are written in plain English instead of framework-specific code, so there's no Selenium vs. Playwright split to maintain. And AI self-healing handles locator changes automatically, which is what keeps both queues from piling up.
>
> CRED, a financial platform dealing with a similar coverage-to-complexity ratio, hit 90% regression coverage 5x faster after switching to Testsigma. The big shift for them wasn't just speed, it was getting their team off the maintenance treadmill and back to building net-new tests.
>
> Between the dual-stack pressure I mentioned last time and the coverage demands that come with Cboe's product breadth, I think there's a real parallel to what CRED was facing. Would 15 minutes make sense to walk through how they made that shift and see if it applies?
>
> Rob Gorham
> Testsigma

---

## Batch Processing Tips

For large T2 batches (20+ contacts):
- Group by company first (all contacts at same company together)
- Ensure no company gets the same T2 proof point twice
- Process in order: highest-priority accounts first
- Commit after every 5 drafts (mid-session commit protocol)

---

*Last updated: 2026-03-13 (Session 34) — FULL REWRITE to match sop-tam-outbound.md Part 7 Deep-Dive v4. Previous version had critical formula errors: 50-70 word count (correct is 140-190), endorsed "Circling back" as good (it is BANNED), used engagement question CTA (correct is 15-minute meeting ask). All three errors corrected.*
