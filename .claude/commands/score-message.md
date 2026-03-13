# Score Message - Run QA gate on a draft message

You are Rob's BDR assistant. The user wants to score a message against the 12-point MQS rubric.

---

## Authoritative Files to Read First

| File | Purpose |
|------|---------|
| `memory/playbooks/qa-gate.md` | Full 12-point MQS rubric + HC1-HC10 Hard Constraints |
| `memory/data-rules.md` | Hard Constraints (HC1-HC10) + Strong Preferences with performance data |
| `skills/draft-qa/SKILL.md` | Automated batch scoring workflow (use for 5+ messages) |

---

## Input
Rob pastes a draft message. Or points to a message in a batch tracker HTML file.

---

## Process

### Step 1: Run the Draft QA skill (for batches)
If scoring 5+ messages at once, read `skills/draft-qa/SKILL.md` — it handles bulk scoring with pass/fail thresholds.

For a single message, score inline using the rubric below.

### Step 2: Hard Constraint scan (HC1-HC10)

Check against all 10 Hard Constraints from `memory/data-rules.md`:

| HC | Rule | Penalty |
|----|------|---------|
| HC1 | No "I noticed" / "I saw" / "I see" | -13.4 pp reply rate |
| HC2 | No leading with AI/ML/self-healing as headline | -9.2 pp |
| HC3 | No messages over 120 words | Auto-fail |
| HC4 | No evening sends after 6 PM | Timing rule |
| HC5 | No bullet-point or numbered-list feature dumps | Auto-fail |
| HC6 | No "would it be unreasonable" as sole CTA | Auto-fail |
| HC7 | No phone-number asks | Auto-fail |
| HC8 | No "reaching out" / "wanted to connect" | -7.1 pp |
| HC9 | No "I figure" / "would you like to share" / "enough about me" | Auto-fail |
| HC10 | No 3+ question marks per message | Auto-fail |

Any HC violation = flag for rewrite before scoring MQS.

### Step 3: Compute MQS (12-point scale)

**Opener Clarity (1-3)**
- 3 = Specific, insight-driven question. No "I noticed," no role-recap, no "reaching out."
- 2 = Company-specific but generic frame.
- 1 = Opens with "I noticed," role-at-company opener, or "Are you looking for..."

**CTA Confidence (1-3)**
- 3 = "What day works?" tied to proof point outcome AND prospect's situation. Not copy-pasteable.
- 2 = Uses "what day works" but weak tie to proof point.
- 1 = Permission-style, vague, or puts work on prospect.

**Personalization Density (1-3)**
- 3 = References something only THIS person would recognize.
- 2 = References their company specifically.
- 1 = Only swaps name/title/company.

**Friction (1-3, inverted: 3=low)**
- 3 = 75-99 words (39.0% reply rate), one proof point, one CTA, exactly 2 question marks, no bullets, short paragraphs, max 1 hyphen.
- 2 = 100-120 words, still readable.
- 1 = Over 120 words, bullets, multiple CTAs, 3+ question marks.

### Step 4: Show the scorecard

```
MQS: X/12 [SEND / REWRITE / REJECT]
  Opener:          X/3 — [rationale]
  CTA:             X/3 — [rationale]
  Personalization: X/3 — [rationale]
  Friction:        X/3 — [rationale]

HC violations: [list any]
Warnings: [hyphen count, word count, question marks]
Word count: X (target: 75-99)
Question marks: X (target: exactly 2)
```

### Step 5: If score < 9, provide a rewrite
Fix the specific flagged dimensions. Show the rewritten version and its new MQS score.

---

## Thresholds
| Score | Status |
|-------|--------|
| 10-12 | Ready to send |
| 9 | Pass (minimum) |
| 7-8 | Rewrite recommended |
| < 7 | Must rewrite |

*Last updated: 2026-03-13 (rewritten — replaces deprecated .claude/rules/outbound-intelligence.md and scripts/score_message.py paths)*
