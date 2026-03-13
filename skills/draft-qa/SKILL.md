# Draft QA — Message Quality Scoring (MQS)

## Description
Scores every T1 or T2 email draft against the 12-point MQS rubric from `memory/playbooks/qa-gate.md`. Catches mechanical failures automatically and evaluates the 5 subjective checks using the AI judgment criteria from `memory/data-rules.md`. Required before presenting any draft to Rob. T1 must score ≥9/12. T2 must score ≥7/9 (T2 variant).

## Trigger
- Called from `skills/tam-t1-batch/SKILL.md` (Step 7 — QA Gate Every Email)
- Run on-demand: "QA check this email", "score this draft", "run QA gate"
- Can batch-score all drafts in a tracker HTML file

## ⛔ APPROVE SEND RULE
This skill scores drafts. It does NOT send anything. Even if a draft scores 12/12, it does NOT go anywhere until Rob gives explicit "APPROVE SEND." Claude drafts, Rob approves, Rob sends via Apollo UI.

---

## T1 Email MQS — 12 Points (must score ≥9 to pass)

Run these checks against the subject line and body. Count word count using `wc -w` or by counting manually.

### Mechanical Checks (7 points — automated)

**Check 1 — Word count (1 pt)**
T1 target: 75-99 words (sweet spot per data-rules.md: 39.0% reply rate)
Hard fail: <60 or >120 words

```python
word_count = len(body.split())
# 75-99: PASS (1 pt)
# 60-74 or 100-120: marginal (0 pts but not hard fail)
# <60 or >120: HARD FAIL
```

**Check 2 — Exactly 2 question marks (1 pt)**
Count `?` in body. Must be exactly 2.
- 3+ question marks: drops reply rate from 34.8% to 14.3% (data-rules.md HC10)
- 0-1 question marks: no CTA or no engagement hook

**Check 3 — SMYKM subject line (1 pt)**
Format: `{First name}'s {role context} at {Company}`
- ✅ "Rachel's QA team at Fidelity"
- ✅ "Seth's automation work at Northern Trust"
- ❌ "Quick question" — generic, instant fail
Check: first_name.lower() in subject.lower() AND company.lower() in subject.lower()

**Check 6 — Named customer with specific numbers (1 pt)**
Must mention a real Testsigma customer AND a specific metric. Both required.

Known customers to check for:
- hansard → "8 to 5 weeks" or "regression window"
- cred → "90%" or "5x"
- medibuddy → "2,500 tests" or "50%"
- cisco → "35%"
- sanofi → "3 days to 80 minutes" or "80 min"
- samsung, oscar health, ntuc, bosch, nokia, honeywell, dhl, zeiss, nestle

Hard fail: no named customer at all.

**Check 7 — Testsigma mentioned by name (1 pt)**
The word "Testsigma" must appear in the body. Not "our platform" or "we" — the actual brand name.

**Check 9 — No em dashes (1 pt)**
Search for `—` (em dash) and `–` (en dash). Must be zero. Use commas instead.

**Check 10 — No placeholder text (1 pt)**
Search for: `[`, `]`, `{`, `}`, `COMPANY`, `FIRSTNAME`, `LASTNAME`, `NAME`, `TITLE`
Hard fail: any placeholder found. This has caused wrong-body sends (INC-007, INC-012).

### AI Judgment Checks (5 points — contextual evaluation)

**Check 4 — HC1 intro (1 pt)**
First sentence must reference the prospect's specific role, team, or responsibility. NOT generic.
- ✅ "Managing QA across Fidelity's trading platforms is its own category of pressure."
- ✅ "Leading automation at a company that deploys to 50 states is different from a startup."
- ❌ "I came across your profile on LinkedIn." (-13.4 pp per data-rules.md HC1)
- ❌ "I noticed your team recently..." (banned per sop-email.md)
Hard constraint: any form of "I noticed" / "I saw" / "I see" = HARD FAIL

**Check 5 — Specific challenge hook (1 pt)**
Must reference a real challenge specific to their company/role/industry. Not generic.
- ✅ "With Fidelity's trading infrastructure, a test environment failure during a trading window isn't just an inconvenience."
- ❌ "Many QA teams struggle with test coverage." — generic, no specificity

**Check 8 — "What day works" CTA (1 pt)**
Default CTA has 40.4% reply rate. Must end with a variant of "What day works to see how?"
- ✅ "What day works to see how?" (canonical)
- ✅ "What day works this week to see how Testsigma handles that?" (tied to proof point)
- ❌ "Would it be worth a quick call?" (banned)
- ❌ "Worth comparing notes?" (banned per data-rules.md)
- ❌ "Would exploring that be worth your time?" (banned)

**Check 11 — Proof point rotation (1 pt)**
Different proof point from every other contact at the same company in this batch AND across all past batches (check `memory/playbooks/qa-gate.md` rotation tracker).
Hard fail: same customer story as another contact at same company.

Available proof points and best verticals:
- Hansard (8→5 weeks regression): Insurance, FinServ, compliance-heavy
- CRED (90% coverage, 5x faster): FinTech, scale challenges
- Medibuddy (2,500 tests, 50% cut): HealthTech, growing codebases
- Cisco (35% regression reduction): Enterprise, platform, hardware-software
- Sanofi (3 days→80 min): Enterprise, pharma, large orgs
- Fortune 100 (3x coverage in 4 months): Enterprise, any industry

**Check 12 — Conversational tone (1 pt)**
Read it aloud. Does it sound like a real person or a template?
- ✅ Short sentences. Natural rhythm. One idea per sentence.
- ❌ Buzzwords: "CI/CD" (-23.6 pp), "low code" (-25.8 pp), "flaky tests" (-16.8 pp)
- ❌ Corporate patterns: "reaching out" (-2.4 pp), "wanted to connect" (-2.4 pp)
- ❌ AI tells: "I figure" (9.8%), "enough about me" (18.2%)

### Hard Fails (instant reject, score irrelevant)
- Any placeholder text (Check 10)
- Word count <60 or >120 (Check 1)
- No named customer at all (Check 6)
- Same proof point as another contact at same company (Check 11)
- "I noticed" / "I saw" opener (Check 4 HC1)
- Contact is on DNC list (run compliance-gate first)
- Contact's domain not in TAM accounts list (run compliance-gate first)

---

## T2 Email QA — 9 Points (must score ≥7 to pass)

T2 uses the Variant A locked formula from `memory/sop-email.md` (locked Mar 9, 2026). Score these 9 checks:

1. **Word count 60-90 words** (1 pt)
2. **Part 1 present: concrete company fact** — not an industry generalization, not a quality/emotion word (1 pt)
3. **Part 2 present: "I'd imagine..." empathy bridge** — connects the company fact to their QA pressure (1 pt)
4. **Part 3 present: LinkedIn callback naming specific T1 topic** — NOT "following up," NOT generic "about test automation" (1 pt)
5. **Part 4 present: customer story + tie-back** — customer name + result + "Reminded me of..." (1 pt)
6. **Part 5 present: engagement CTA tied to Part 1 tension** — NOT a meeting ask, NOT "What day works?" (1 pt)
7. **Different proof point from T1** — required rotation (1 pt)
8. **No em dashes, no "following up," no "circling back"** (1 pt)
9. **No testsigma.com URL in body** (removed from T2 per sop-email.md) (1 pt)

Hard fails for T2:
- CTA is a meeting ask ("What day works?" is banned in T2 — save for T3 or after engagement)
- LinkedIn callback does not name the specific T1 topic
- Opening is an industry generalization instead of a company-specific fact
- Same customer story as T1

---

## Python QA Script (Run on Bash for T1 mechanical checks)

```python
import re

def qa_check_t1(subject, body, first_name, company, proof_points_at_company=[]):
    score = 0
    hard_fails = []
    notes = []

    # Word count
    words = len(body.split())
    if 75 <= words <= 99:
        score += 1
        notes.append(f"✅ Word count: {words} (optimal)")
    elif 60 <= words <= 120:
        notes.append(f"⚠️ Word count: {words} (acceptable but not optimal — target 75-99)")
    else:
        hard_fails.append(f"❌ Word count: {words} — HARD FAIL (<60 or >120)")

    # Question marks
    qmarks = body.count('?')
    if qmarks == 2:
        score += 1
        notes.append(f"✅ Question marks: {qmarks}")
    else:
        notes.append(f"❌ Question marks: {qmarks} (must be exactly 2)")

    # SMYKM subject
    if first_name.lower() in subject.lower() and company.lower() in subject.lower():
        score += 1
        notes.append(f"✅ Subject: SMYKM format confirmed")
    else:
        notes.append(f"❌ Subject: missing first name or company — '{subject}'")

    # Named customer with numbers
    customers = ['hansard', 'cred', 'medibuddy', 'cisco', 'samsung', 'oscar health',
                 'sanofi', 'bosch', 'nokia', 'honeywell', 'dhl', 'zeiss', 'nestle',
                 'fortune 100', 'ntuc']
    found = [c for c in customers if c in body.lower()]
    has_nums = bool(re.search(r'\d+[%x]|\d+\s*(to|→|weeks|min|days)', body))
    if found and has_nums:
        score += 1
        notes.append(f"✅ Proof point: {found[0]} with numbers")
    elif found:
        notes.append(f"⚠️ Proof point: {found[0]} found but no specific numbers")
    else:
        hard_fails.append(f"❌ No named customer — HARD FAIL")

    # Testsigma mentioned
    if 'testsigma' in body.lower():
        score += 1
        notes.append(f"✅ Testsigma: mentioned")
    else:
        notes.append(f"❌ Testsigma: NOT mentioned")

    # No em dashes
    if '—' not in body and '–' not in body:
        score += 1
        notes.append(f"✅ No em dashes")
    else:
        notes.append(f"❌ Em dash or en dash found — remove")

    # No placeholders
    placeholders = re.findall(r'\[.*?\]|\{.*?\}|COMPANY|FIRSTNAME|LASTNAME', body)
    if not placeholders:
        score += 1
        notes.append(f"✅ No placeholders")
    else:
        hard_fails.append(f"❌ Placeholders found: {placeholders} — HARD FAIL")

    # HC1 check (banned openers)
    if re.search(r'\b(i noticed|i saw|i see|i came across)\b', body.lower()):
        hard_fails.append(f"❌ Banned opener (HC1) — HARD FAIL")
    else:
        notes.append(f"✅ No banned openers")

    return {'score': score, 'max_mechanical': 7, 'hard_fails': hard_fails, 'notes': notes}
```

---

## Output Format

```
QA GATE: Seth Drummond @ Northern Trust (T1)
Subject: "Seth's automation work at Northern Trust"
Body: 87 words

MECHANICAL (7/7):
  ✅ Word count: 87 words (optimal)
  ✅ Question marks: 2
  ✅ Subject: SMYKM format
  ✅ Proof point: Hansard with numbers (8 to 5 weeks)
  ✅ Testsigma: mentioned
  ✅ No em dashes
  ✅ No placeholders

AI JUDGMENT (4/5):
  ✅ HC1 intro: References Northern Trust's trading infrastructure specifically
  ✅ Challenge hook: Trading window failure framing — specific to their environment
  ✅ CTA: "What day works to see how?" — clean
  ✅ Proof rotation: Hansard (unique at Northern Trust)
  ⚠️ Tone: "CI/CD" found — consider replacing with "automation pipeline" (-23.6 pp)

HARD CONSTRAINTS: All clear

MQS: 11/12 ✅ PASS (threshold: 9/12)

RECOMMENDATION: Replace "CI/CD" before presenting to Rob.
```

---

## Integration Points
- Called by: `skills/tam-t1-batch/SKILL.md` Step 7
- References: `memory/playbooks/qa-gate.md` (full MQS), `memory/data-rules.md` (HC1-HC10, toxic phrases), `memory/sop-email.md` (T2 Variant A formula)
- Outputs: Pass/fail per draft + QA gate section for batch tracker HTML cards

*Source: `memory/playbooks/qa-gate.md` + `memory/data-rules.md` + `memory/sop-email.md`*
*Last updated: 2026-03-12 (Session 30)*
