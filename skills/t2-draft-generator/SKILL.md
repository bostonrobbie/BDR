# T2 Batch Draft Generator — Skill

## ⚠️ STATUS: LOCKED — DO NOT USE

**This skill is a stub. It is NOT ready for production use.**

The T2 email formula has not been finalized. Until Rob and Claude lock the T2 formula (word count structure, proof point rotation logic, CTA phrasing, opener conventions, threading behavior), this skill must not be used to generate T2 drafts at scale.

**When this skill becomes active:**
- After the T2 formula session (expected: before Batch 8/9 T2 window, ~Mar 18-21)
- The formula will be documented in `memory/playbooks/t2-followup.md`
- This stub will be updated with the finalized logic
- The LOCKED status header will be removed

**For now:** T2 drafts must be written manually per `memory/playbooks/t2-followup.md`.

---

## Description (Planned)

When unlocked, this skill will:
- Take a completed `batch{N}_sends.json` (T1 content) as input
- For each contact, generate a T2 draft using the finalized T2 formula
- Auto-select a different proof point than the one used in T1 (rotation logic TBD)
- Apply correct word count, CTA phrasing, and threading
- Run draft-qa scoring on each draft (MQS >= 9/12 required)
- Output a `batch{N}_t2_drafts.json` and corresponding HTML tracker section
- Generate a review summary for Rob to approve/modify before Gate 1

This would compress what is currently a multi-session manual drafting effort into a single review session.

---

## Inputs (Planned)

| Input | Source | Notes |
|-------|--------|-------|
| `batch{N}_sends.json` | Created by `skills/batch-json-builder/SKILL.md` | T1 content (subject, body, company, first name) |
| `memory/proof-points.md` | Memory file | Proof point library for rotation |
| `memory/playbooks/t2-followup.md` | Playbook | T2 formula (PENDING FINALIZATION) |
| `memory/target-accounts.md` | Memory file | Company intel for personalization |

---

## Open Questions Before Unlocking

These must be answered and locked in the T2 formula session:

1. **Opener convention:** Do T2s open with a direct reference to T1 ("I sent you a note last week about...")? Or drop straight into the new angle like T1 does (no greeting, no callback)?

2. **Proof point rotation:** If T1 used Medibuddy (maintenance reduction), does T2 always use a different vertical? Or same vertical, different stat? What's the selection logic?

3. **Threading in Apollo:** Does T2 subject always use "Re: [T1 subject]"? Or a fresh subject line? Apollo can thread or send standalone.

4. **CTA phrasing:** The playbook says "Would 15 minutes make sense to walk through how [Customer] made that shift?" — is this fixed or should it be personalized?

5. **Body length:** 140-190 words is documented in the playbook. Is this verified and locked, or still evolving?

6. **Banned phrases:** "Circling back", "Following up", "Just checking in" are banned. What else?

7. **Personalization depth:** Does each T2 need new company-specific context, or is the proof point + CTA the main variable?

---

## Placeholder Process (for reference when unlocking)

```
Phase 1: Load T1 data from batch{N}_sends.json
Phase 2: For each contact:
  a. Parse company name, first name, T1 proof point used
  b. Select a different proof point from proof-points.md (rotation TBD)
  c. Apply T2 formula structure (opener → new angle → proof point → CTA)
  d. Write draft to output array
  e. Auto-score via draft-qa (MQS >= 9/12 required)
Phase 3: Write batch{N}_t2_drafts.json
Phase 4: Generate HTML summary for Rob review
Phase 5: Gate 1 — Rob reviews and approves content
Phase 6: Hand off to skills/apollo-send/SKILL.md
```

---

## T2 Formula Reference (partial — PENDING FINALIZATION)

Currently documented in `memory/playbooks/t2-followup.md`. Known elements as of 2026-03-14:

| Element | Current Value | Locked? |
|---------|--------------|---------|
| Word count | 140-190 words | Tentative |
| CTA | 15-minute meeting ask | Tentative |
| Subject | "Re: [T1 subject]" | TBD |
| Opener | TBD | ❌ Not locked |
| Proof point selection | Different from T1 | TBD logic |
| Banned phrases | Circling back, Following up, One more angle worth adding | Tentative |

---

*Created: 2026-03-14 (Session 37). Stub only — NOT production-ready. Unlock after T2 formula finalization session. Update "Tracker Formats Known" equivalent table after first production run.*

---

## Self-Improvement Loop

This skill maintains its own run log and learned-patterns file. Full protocol: `skills/_shared/learning-loop.md`

### Before Each Run
1. Read `skills/t2-draft-generator/learned-patterns.md` if it exists — apply any documented calibration adjustments
2. Count entries in `skills/t2-draft-generator/run-log.md` to determine current run number

### After Every Run — Append to run-log.md
```
### Run #[N] — [YYYY-MM-DD HH:MM]
- **Result:** [1-2 sentence summary]
- **Key metrics:** [skill-specific counts per _shared/learning-loop.md]
- **Anomalies:** [anything unexpected]
- **Adjustments made this run:** [any deviations from SKILL.md]
- **Output quality:** [Accurate / Mostly accurate / Needs calibration / Failed]
```

### Every 5th Run — Pattern Review
1. Read last 5 run-log.md entries
2. Extract recurring patterns, consistent edge cases, metric drift
3. Overwrite `skills/t2-draft-generator/learned-patterns.md` with updated findings
4. If a pattern appears in 4+ of 5 runs: write a `## SKILL UPDATE PROPOSAL — t2-draft-generator` entry to `memory/session/messages.md` for Rob's review

**Hard rule:** Never modify SKILL.md directly. Only propose updates via messages.md and wait for Rob's explicit approval.
