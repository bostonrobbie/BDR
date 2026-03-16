# Score Message - Run QA gate on a draft message

You are Rob's BDR assistant. The user wants to score a message against the data-driven quality rules.

## Files to Load
- `.claude/rules/outbound-intelligence.md` — Hard Constraints (HC1-HC10), MQS scoring, QA Gate, phrase intelligence

## Input
Rob will paste a draft message, or point to a message in a batch file.

## Process

### Step 1: Try the Python scorer first
Run: `python scripts/score_message.py --text "MESSAGE_TEXT"`

If the script runs successfully, display its output and proceed to Step 4.
If it fails, fall back to manual scoring in Steps 2-3.

### Step 2: Run Hard Constraint scan
Check the message against all 10 Hard Constraints from `.claude/rules/outbound-intelligence.md`:
- HC1: No "I noticed" / "I saw" / "I see" (-13.4 pp)
- HC2: No leading with AI/ML/self-healing as headline (-9.2 pp)
- HC3: No messages over 120 words
- HC4: No evening sends (after 6 PM)
- HC5: No bullet-point or numbered-list feature dumps
- HC6: No "would it be unreasonable" as sole CTA
- HC7: No phone-number asks
- HC8: No "reaching out" / "wanted to connect"
- HC9: No "I figure" / "would you like to share" / "enough about me"
- HC10: No 3+ question marks per message

Any violation = flag for rewrite.

### Step 3: Compute MQS (12-point scale)

**Opener Clarity (1-3)**
- 3 = Specific, insight-driven question. No "I noticed," no role-recap, no "reaching out."
- 2 = Company-specific but generic frame.
- 1 = Opens with "I noticed," "Seeing that you're the [Title]," or "Are you looking for..."

**CTA Confidence (1-3)**
- 3 = "What day works?" tied to proof point outcome AND prospect's situation. Not copy-pasteable.
- 2 = Uses "what day works" but weak tie to proof point.
- 1 = Permission-style, vague, or puts work on prospect.

**Personalization Density (1-3)**
- 3 = References something only THIS person would recognize.
- 2 = References their company specifically.
- 1 = Only swaps name/title/company.

**Friction (1-3, inverted: 3=low)**
- 3 = 80-110 words, one proof point, one CTA, exactly 2 questions, no bullets, 4+ paragraph breaks, max 1 hyphen.
- 2 = 110-120 words, still readable.
- 1 = Over 120 words, bullets, multiple CTAs, 3+ questions.

### Step 4: Show the scorecard
```
MQS: X/12 [SEND / REWRITE / REJECT]
  Opener:          X/3 - [rationale]
  CTA:             X/3 - [rationale]
  Personalization: X/3 - [rationale]
  Friction:        X/3 - [rationale]

Violations: [list any HC violations]
Warnings: [phrase toxicity, hyphen count, etc.]
Word count: X
Question marks: X
```

### Step 5: If score < 9, suggest a rewrite
Provide a rewritten version that fixes the specific issues flagged. Show the new score.

## Thresholds
- 10-12: Ready to send
- 7-9: Acceptable but should improve
- <7: Must rewrite
