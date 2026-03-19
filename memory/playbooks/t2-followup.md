# Playbook: T2 Follow-Up Drafting

## Version: v5 — Locked Mar 16, 2026
Previous version (v4) retired. Canonical source: `memory/sop-tam-outbound.md` Part 7.

---

## When to Use

When T2 tasks surface in Apollo's task queue, typically Day 5 after T1 was sent. Also use when manually calculating T2 due dates from MASTER_SENT_LIST.csv.

---

## Cadence Rules

| Touch | Earliest | Typical | Latest |
|-------|----------|---------|--------|
| T2 | Day 4 from T1 | Day 5 from T1 | Day 8 from T1 |

HARD RULE: Touch 2 NOT before Day 4. Violating this was INC-001.

---

## T2 Email Formula — Reply + Piggyback v5 (Locked Mar 16, 2026)

### Core Principle

T2 is a genuine reply to T1, not a second cold email. It acknowledges the first note, shows you actually researched the person, goes deeper on their specific pain, and asks for a concrete next step. The prospect should feel like you thought about them between sends.

### Format Rules

- 155-180 words
- Blank line between every paragraph
- "Hi [First Name]," greeting always opens
- Sign-off: Rob Gorham (line break) Testsigma
- Threading: send as reply to T1 thread
- No em dashes anywhere

---

### Structure (4 paragraphs, no exceptions)

---

**Para 1 — Greeting + re-engagement hook**

Open with "Hi [First Name],"

Then acknowledge you're back without using "following up" or "circling back." Signal that this note is more specific than the last one. Reference their actual role and what it means at their company.

Locked formula:
"I know my last note wasn't specific enough to be worth your time. Looking at your [role/background] at [Company], I think this angle is a lot more relevant to what you're actually dealing with."

Personalization rule: Must name their role or something specific about what they manage. Never reference only the company name.

---

**Para 2 — Personalized pain speculation**

Role/vertical/company-specific observation about what they are likely dealing with. Then "I imagine [specific operational consequence]." End with the salvage clause.

"I imagine" is mandatory in this paragraph. It is the engine of Para 2, not the email opener.

Salvage clause (pick one, end of paragraph):
- "If I'm reading that wrong, correct me."
- "If that's not the right read, set me straight."
- "If I'm off on that, let me know."
- "If that's not exactly right, set me straight."

Personalization depth: Name actual surfaces, products, workflows, or team dynamics specific to their company and role. The more specific, the better. Generic persona-level pain is a QA fail.

---

**Para 3 — Customer proof point with bridge**

Open with a bridge that connects Para 2's pain to the customer story. Never drop the customer story cold.

Bridge formula: "It's the same [problem / tension / pressure] [Customer] was dealing with."

Then: metric + one insight beyond the headline number that shows what actually changed for them.

Different proof point from T1. No exceptions.

---

**Para 4 — CTA**

Echo the specific pain from Para 2 (not generic language). Ask for 15 minutes framed as an evaluation.

CTA formula: "If [specific pain echo] is [real for your team / something you're working on], would 15 minutes give you a pretty clear picture of whether Testsigma is worth a look?"

HARD RULE: Closing sentence must end with a question mark.

---

### BANNED (hard fail)

- Em dashes (—) anywhere
- "Following up" / "Circling back" / "Reaching back out"
- "Different lens from my last note"
- "One more angle worth adding/sharing"
- "Thought this was worth adding"
- Any opener that apologizes for taking up space
- Closing without a question mark
- Intro that only names the company (must name role or responsibility)

---

### Proof Point Rotation

| T1 Used | T2 Must Use |
|---------|------------|
| Hansard (regression 8→5 weeks) | CRED or MediBuddy |
| Fortune 100 / 3x productivity | Cisco or Hansard |
| Nagra DTV (2,500 tests, 4x faster) | CRED or MediBuddy |
| CRED (90% coverage, 5x faster) | MediBuddy or Hansard |
| MediBuddy (50% maintenance cut) | Nagra DTV or Cisco |
| Sanofi (3 days → 80 min) | Hansard or CRED |

Vertical matching rule: If a same-vertical customer exists and was not the T1 proof point, prioritize it. Sanofi for healthcare/pharma, Nagra DTV for media/streaming, CRED for FinTech, Hansard for insurance.

Same-company rule: No two contacts at the same company get the same T2 proof point.

---

### QA Gate (pass threshold: 10/12)

| # | Check | Points |
|---|-------|--------|
| 1 | Word count 155-180 | 1 |
| 2 | "Hi [First Name]," greeting | 1 |
| 3 | Para 1 references role or specific responsibility | 1 |
| 4 | "I imagine" present in Para 2 | 1 |
| 5 | Salvage clause in Para 2 | 1 |
| 6 | Bridge line opens Para 3 | 1 |
| 7 | Named customer with specific metric | 1 |
| 8 | Different proof point from T1 | 1 |
| 9 | Closing sentence ends with question mark | 1 |
| 10 | No em dashes anywhere | 1 |
| 11 | No banned phrases | 1 |
| 12 | Blank line between every paragraph | 1 |

---

### Process

**Step 1: Identify T2s due**
Open Apollo task queue, filter TAM Outbound Step 2 tasks. Or calculate from MASTER_SENT_LIST: contacts with send_date 5-8 days ago.

**Step 2: Pull T1 content**
Open relevant batch tracker HTML or batch{N}_sends.json. For each contact: note T1 subject, body, proof point used, company, title, vertical.

**Step 3: Research the person**
Check LinkedIn for specific role details, responsibilities, team structure. Note anything that makes Para 1 and Para 2 more specific to this person.

**Step 4: Draft using v5 formula**
- Para 1: Greeting + re-engagement hook with role personalization
- Para 2: Pain speculation with "I imagine" + salvage clause
- Para 3: Bridge line + customer story + insight beyond the metric
- Para 4: Pain echo + 15-min question mark CTA

**Step 5: QA Gate**
Score each draft 0-12. Must pass 10/12 minimum before presenting.

**Step 6: Present for APPROVE SEND**
Show Rob all drafts. Wait for explicit APPROVE SEND before touching Apollo. Then use INC-012 two-gate protocol for every send.

---

### Reference Example (validated Mar 16, 2026 — Batch 10)

**Dawn McCartha — Testing Manager, EmblemHealth**
T1 angle: Regression cycle / Hansard
T2 proof point: Sanofi (healthcare vertical match)
Word count: 168

Hi Dawn,

I know my last note wasn't specific enough to be worth your time. Looking at your role managing testing at a health plan like EmblemHealth, I think this angle is a lot more relevant to what you're actually dealing with.

Testing at a health plan means you can't skip compliance workflows to save time. Member applications, claims, and benefits platforms all have to pass before anything ships, and I imagine that obligation is what keeps the cycle from getting shorter no matter how much pressure there is to release faster. If I'm reading that wrong, set me straight.

It's the same tension Sanofi was dealing with. They got their regression window from 3 days down to 80 minutes on Testsigma, not by cutting what gets tested, but by running those compliance workflows in parallel instead of one at a time. The manual patching work between releases stopped eating into sprint time too.

If that speed-versus-coverage tension is real for your team right now, would 15 minutes give you a pretty clear picture of whether Testsigma is worth a look?

Rob Gorham
Testsigma

---

### Batch Processing Tips

For batches with multiple contacts at the same company:
- Draft all same-company contacts together
- Ensure no two get the same T2 proof point
- Vary the Para 2 pain angle even if the vertical is the same

For large batches (10+ contacts):
- Process by company grouping
- QA score after every 5 drafts
- Commit to tracker after every 5 drafts (mid-session safety)

---

*Last updated: 2026-03-16 (Session 42) — FULL REWRITE to v5 Reply + Piggyback formula. Previous v4 had cold "I imagine" opener (no greeting, no re-engagement hook), no personalization requirement in Para 1, no bridge line requirement in Para 3, and no question mark rule on closing. All corrected in v5. Reference example updated to Dawn McCartha / EmblemHealth / Sanofi (replaces Rick Brandt / Cboe).*
