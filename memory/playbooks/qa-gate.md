# Playbook: QA Gate

## When to Use
Before sending ANY outreach email. Every email must pass the QA gate. No exceptions.

---

## MQS (Message Quality Score) — 12 Point System

| # | Check | Points | How to Verify |
|---|-------|--------|---------------|
| 1 | Word count in range | 1 | T1: 75-99 words. T2: 50-70 words. Breakup: 40-60 words. Count with `wc -w` or manual count. |
| 2 | Exactly 2 question marks | 1 | Count `?` characters. Must be exactly 2 for T1. T2 can have 1-2. |
| 3 | SMYKM subject line | 1 | Format: `{First name}'s {role context} at {Company}`. Not generic like "Quick question". |
| 4 | HC1 intro (shows you know them) | 1 | First sentence references their specific role, team, or responsibility. NOT "I came across your profile." |
| 5 | Specific challenge hook | 1 | References a real challenge relevant to their role. NOT "many companies struggle with testing." |
| 6 | Named customer with numbers | 1 | Mentions a real Testsigma customer AND a specific metric. E.g., "Hansard cut regression 8 to 5 weeks." |
| 7 | Testsigma mentioned by name | 1 | The word "Testsigma" appears in the body. |
| 8 | "What day works" CTA (T1 only) | 1 | CTA ends with "What day works to see how?" or similar. T2 uses engagement question instead. |
| 9 | No em dashes | 1 | Search for `—` (em dash). Must be zero. Use commas instead. |
| 10 | No placeholder text | 1 | Search for `[`, `]`, `{`, `}`, `COMPANY`, `NAME`, `TITLE`. Must be zero. |
| 11 | Different proof point from same-company contacts | 1 | Check the proof point rotation tracker in the batch HTML. No two contacts at the same company get the same customer story. |
| 12 | Conversational tone | 1 | Read it aloud. Does it sound like a real person talking? Not robotic, not over-polished. |

**Pass threshold:** MQS >= 9/12
**Hard fail (instant reject, regardless of score):**
- Any placeholder text (Check 10 fails)
- Word count >120 or <60
- Missing proof point entirely
- Same proof point as another same-company contact
- Contact is on DNC list
- Contact's domain not in TAM accounts list

---

## Automated QA Script (Python)

For large batches, use the Python QA script. This checks the mechanical items (word count, question marks, em dashes, placeholders):

```python
import re

def qa_check(subject, body, company, first_name, proof_point_list_for_company):
    score = 0
    failures = []

    # Word count
    words = len(body.split())
    if 75 <= words <= 99:
        score += 1
    else:
        failures.append(f"Word count: {words} (target 75-99)")

    # Question marks
    qmarks = body.count('?')
    if qmarks == 2:
        score += 1
    else:
        failures.append(f"Question marks: {qmarks} (target 2)")

    # SMYKM subject
    if first_name.lower() in subject.lower() and company.lower() in subject.lower():
        score += 1
    else:
        failures.append(f"Subject missing name or company: '{subject}'")

    # Em dashes
    if '—' not in body and '–' not in body:
        score += 1
    else:
        failures.append("Em dash or en dash found")

    # Placeholders
    placeholder_pattern = r'\[.*?\]|\{.*?\}|COMPANY|FIRSTNAME|LASTNAME'
    if not re.search(placeholder_pattern, body):
        score += 1
    else:
        failures.append("Placeholder text found")

    # Testsigma mentioned
    if 'testsigma' in body.lower():
        score += 1
    else:
        failures.append("Testsigma not mentioned")

    # Named customer check (look for known customer names)
    customers = ['hansard', 'cred', 'medibuddy', 'cisco', 'samsung', 'oscar health',
                 'sanofi', 'bosch', 'nokia', 'honeywell', 'dhl', 'zeiss', 'nestle']
    has_customer = any(c in body.lower() for c in customers)
    if has_customer:
        score += 1
    else:
        failures.append("No named customer found")

    return {
        'score': score,
        'max': 12,
        'automated_checks': 7,
        'manual_checks_needed': 5,
        'failures': failures,
        'pass': score >= 9 and len([f for f in failures if 'Placeholder' in f]) == 0
    }
```

**Note:** The script catches 7 of 12 checks automatically. The remaining 5 (HC1 intro quality, challenge hook specificity, CTA phrasing, proof point rotation, conversational tone) require human/AI judgment.

---

## Proof Point Rotation Tracking

In the batch tracker HTML, maintain a table showing which proof point each contact got:

| Company | Contact | Proof Point | Customer | Numbers |
|---------|---------|------------|----------|---------|
| Fidelity | Seth Drummond | Regression speed | Hansard | 8→5 weeks |
| Fidelity | Nithya Arunkumar | Test coverage | CRED | 90% coverage, 5x faster |
| Fidelity | Chris Pendergast | Enterprise scale | Fortune 100 | 3x coverage in 4 months |

**Available proof points:**
1. Hansard: regression 8→5 weeks (Insurance/FinServ)
2. CRED: 90% regression coverage, 5x faster (FinTech)
3. Medibuddy: 2,500 tests, 50% maintenance cut (HealthTech)
4. Cisco: 35% regression time reduction (Enterprise/Tech)
5. Fortune 100: 3x test coverage in 4 months (Enterprise)
6. Samsung: cross-platform coverage (Hardware/Consumer Tech)
7. Oscar Health: compliance-critical test coverage (Healthcare)
8. NTUC Fairprice: retail regression (Retail)

**Vertical matching:** See `memory/proof-points.md` for the full matching table (which proof point works best for which industry).

---

## QA Gate in the Tracker HTML

Each contact card in the batch tracker should include a QA checklist:

```html
<div class="qa-gate">
  <h4>QA Gate</h4>
  <ul>
    <li>WC: 87 words</li>
    <li>QM: 2</li>
    <li>Subject: SMYKM</li>
    <li>Proof: Hansard (unique in company)</li>
    <li>MQS: 11/12</li>
    <li>Status: PASS</li>
  </ul>
</div>
```

---

---
*Version: 1.0 — 2026-03-12*
*Change log: v1.0 (Mar 12, 2026) — consolidated from Sessions 4-27, data-rules.md, sop-outreach.md*
*When updating: increment version, add change log entry with date and what changed.*
