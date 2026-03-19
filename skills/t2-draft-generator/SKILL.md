# T2 Batch Draft Generator — Skill

## STATUS: ACTIVE (unlocked Mar 16, 2026)

Formula finalized in Session 42. T2 Reply + Piggyback v5 is locked and documented in:
- `memory/playbooks/t2-followup.md` (full playbook)
- `memory/sop-tam-outbound.md` Part 7 (canonical source)

---

## Description

This skill generates T2 draft emails for all contacts in a completed batch, using the finalized v5 formula. It takes T1 content as input, selects the correct rotation proof point, personalizes Para 1 and Para 2 to each contact's role and company, runs QA scoring, and outputs drafts for Rob's review before any send.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `batch{N}_sends.json` | `batches/sends-json/` | Yes — T1 content per contact |
| `memory/playbooks/t2-followup.md` | Playbook | Yes — formula |
| `memory/proof-points.md` | Memory | Yes — proof point library |
| LinkedIn/Apollo research | Research per contact | Yes — for Para 1 personalization |

---

## T2 Formula v5 — Quick Reference

### Structure (4 paragraphs, blank line between each)

**Para 1 — Greeting + re-engagement hook**
"Hi [First Name],

I know my last note wasn't specific enough to be worth your time. Looking at your [role/background] at [Company], I think this angle is a lot more relevant to what you're actually dealing with."

Must reference their specific role or responsibilities. Never just name the company.

**Para 2 — Personalized pain speculation**
Role/company-specific observation. "I imagine [specific consequence]." End with salvage clause.

Salvage clause options:
- "If I'm reading that wrong, correct me."
- "If that's not the right read, set me straight."
- "If I'm off on that, let me know."

**Para 3 — Customer proof point with bridge**
"It's the same [problem/tension/pressure] [Customer] was dealing with. [Metric]. [One insight beyond the headline]."

**Para 4 — CTA**
"If [specific pain echo], would 15 minutes give you a pretty clear picture of whether Testsigma is worth a look?"

---

## Hard Rules (fail the draft if violated)

- No em dashes (—) anywhere
- No "following up," "circling back," "reaching back out"
- "I imagine" must appear in Para 2 (not as opener)
- Salvage clause required in Para 2
- Bridge line required to open Para 3
- Closing sentence must end with question mark
- Blank line between every paragraph
- 155-180 words
- Different proof point from T1
- Para 1 must name role or specific responsibility

---

## Proof Point Rotation

| T1 Used | T2 Must Use |
|---------|------------|
| Hansard | CRED or MediBuddy |
| Fortune 100 / 3x productivity | Cisco or Hansard |
| Nagra DTV | CRED or MediBuddy |
| CRED | MediBuddy or Hansard |
| MediBuddy | Nagra DTV or Cisco |
| Sanofi | Hansard or CRED |

Vertical priority: Sanofi for healthcare/pharma, Nagra DTV for media/streaming, CRED for FinTech, Hansard for insurance/financial services.

Same-company rule: No two contacts at the same company get the same T2 proof point.

---

## QA Gate (minimum 10/12 to pass)

| # | Check |
|---|-------|
| 1 | Word count 155-180 |
| 2 | "Hi [First Name]," greeting |
| 3 | Para 1 references role or specific responsibility |
| 4 | "I imagine" in Para 2 |
| 5 | Salvage clause in Para 2 |
| 6 | Bridge line opens Para 3 |
| 7 | Named customer with specific metric |
| 8 | Different proof point from T1 |
| 9 | Closing sentence ends with question mark |
| 10 | No em dashes |
| 11 | No banned phrases |
| 12 | Blank line between paragraphs |

---

## Process

```
Phase 1: Load batch{N}_sends.json
Phase 2: For each contact:
  a. Parse first name, company, title, T1 proof point used
  b. Research role on LinkedIn/Apollo for Para 1 personalization
  c. Select T2 proof point via rotation table
  d. Write Para 1 (greeting + hook with role reference)
  e. Write Para 2 (pain speculation + "I imagine" + salvage clause)
  f. Write Para 3 (bridge line + proof point + insight)
  g. Write Para 4 (pain echo + question mark CTA)
  h. Count words (target 155-180)
  i. Score via QA gate (must pass 10/12)
Phase 3: Present all drafts to Rob for review
Phase 4: Wait for APPROVE SEND
Phase 5: Hand off to skills/apollo-send/SKILL.md (INC-012 two-gate protocol)
```

---

## Reference Example (validated Mar 16, 2026)

**Dawn McCartha — Testing Manager, EmblemHealth**
T1: Hansard / T2: Sanofi / 168 words / QA: 12/12

Hi Dawn,

I know my last note wasn't specific enough to be worth your time. Looking at your role managing testing at a health plan like EmblemHealth, I think this angle is a lot more relevant to what you're actually dealing with.

Testing at a health plan means you can't skip compliance workflows to save time. Member applications, claims, and benefits platforms all have to pass before anything ships, and I imagine that obligation is what keeps the cycle from getting shorter no matter how much pressure there is to release faster. If I'm reading that wrong, set me straight.

It's the same tension Sanofi was dealing with. They got their regression window from 3 days down to 80 minutes on Testsigma, not by cutting what gets tested, but by running those compliance workflows in parallel instead of one at a time. The manual patching work between releases stopped eating into sprint time too.

If that speed-versus-coverage tension is real for your team right now, would 15 minutes give you a pretty clear picture of whether Testsigma is worth a look?

Rob Gorham
Testsigma

---

## Self-Improvement Loop

This skill maintains its own run log and learned-patterns file. Full protocol: `skills/_shared/learning-loop.md`

### Before Each Run
1. Read `skills/t2-draft-generator/learned-patterns.md` if it exists — apply calibration adjustments
2. Count entries in `skills/t2-draft-generator/run-log.md` for current run number

### After Every Run — Append to run-log.md
```
### Run #[N] — [YYYY-MM-DD HH:MM]
- **Batch:** batch{N}
- **Contacts drafted:** [N]
- **QA pass rate:** [N/N]
- **Anomalies:** [anything unexpected]
- **Adjustments made this run:** [deviations from SKILL.md]
- **Output quality:** [Accurate / Mostly accurate / Needs calibration / Failed]
```

### Every 5th Run — Pattern Review
1. Read last 5 run-log entries
2. Extract recurring patterns, edge cases, metric drift
3. Overwrite `skills/t2-draft-generator/learned-patterns.md` with updated findings
4. If pattern appears in 4+ of 5 runs: write a SKILL UPDATE PROPOSAL to `memory/session/messages.md`

Hard rule: Never modify SKILL.md directly. Propose updates via messages.md and wait for Rob's explicit approval.

---

*Unlocked: 2026-03-16 (Session 42). Formula: Reply + Piggyback v5. Previous stub status removed. First production run: Batch 10 T2s (10 contacts, due Mar 21-24).*
