# QA Rules and Scoring Reference

Source: 1,330 LinkedIn conversations (384 replies, 946 no-replies, 6,210 messages)

## Message Quality Score (MQS) - 12-Point System

Every outbound message is scored on 4 dimensions (1-3 each). Maximum = 12.

### Opener Clarity (1-3)
- 3 = Specific, insight-driven question about prospect's situation. No reaching_out, no role-recap.
- 2 = Company-specific reference but generic frame. May include mild role reference.
- 1 = Opens with "I'm reaching out" or "Seeing that you're the [Title]." Template-visible.

### CTA Confidence (1-3)
- 3 = Specific ask with time/action, tied to value angle. No easy outs.
- 2 = Asks a question but doesn't specify time or tie to value angle.
- 1 = Permission-style, vague, or puts work on prospect.

### Personalization Density (1-3)
- 3 = References something only THIS person would recognize (project, career move, company event).
- 2 = References their company specifically but opener could apply to anyone in that role.
- 1 = Only swaps name, title, company. Indistinguishable from template.

### Friction (1-3, inverted: 3=low friction)
- 3 = Under 100 words, one proof point, one CTA, no bullet lists, clean.
- 2 = 100-120 words, may have 2 proof points, still readable.
- 1 = Over 120 words, bullet-point features, multiple CTAs, wall-of-text.

### Thresholds
- 10-12 = Ready to send
- 7-9 = Acceptable but should be improved
- <7 = MUST be rewritten

## QA Gate (MANDATORY before batch presentation)

1. Rule violation scan: Check every message against all 7 Hard Constraints. Any violation = auto-rewrite.
2. Score computation: Compute MQS for every message. Show breakdown.
3. Threshold enforcement: Only messages scoring >=9/12 may be presented.
4. Structural dedup: No two messages in batch may be structurally identical.
5. Evidence check: Every personalization claim must have a research source.
6. Angle rotation check: No prospect may receive the same angle in more than one touch.

## Prospect Prioritization (Reply-Likelihood Model)

Prioritize based on "likelihood of reply given historical behavior," NOT theoretical ICP fit.

### Boost factors
- QA-titled leaders (Director/Head/VP of QA): highest reply rate
- Companies where Personalization Score 3 is achievable
- Companies in active transformation, acquisition, or scaling
- Buyer Intent signals from Sales Navigator

### Penalize factors
- Surface-level personalization only possible (Score 1)
- VP Eng at 50K+ companies with no QA-specific scope
- Prospects requiring >120 words to explain relevance

## Proof Point Rotation

Never use same proof point twice for same prospect across their sequence.

| Angle | Proof Points | Best Verticals |
|-------|-------------|----------------|
| Maintenance | Hansard 8wk to 5wk, 90% maintenance reduction, 70% vs Selenium | Insurance, FinServ, long regression |
| Velocity | CRED 90% coverage + 5x faster, Sanofi 3 days to 80 min | FinTech, fast-shipping teams |
| Scale/Coverage | Medibuddy 2,500 tests + 50% cut, Nagra DTV 2,500 in 8mo | Healthcare, media, mid-size |
| Productivity | Fortune 100 3X productivity, Spendflo 50% manual cut | Enterprise VP-level, SaaS startups |

## Observed Reply Patterns

| Type | % of Replies | Action |
|------|-------------|--------|
| Polite ("thanks") | 37.9% | Follow up with value. Not commitment. |
| Positive ("interested") | 22.8% | Book meeting immediately. Don't over-explain. |
| Negative ("not interested") | 9.4% | Log objection. May re-engage 60+ days. |
| Curiosity ("how", "tell me more") | 8.3% | Answer directly, then bridge to meeting. |
| Referral ("talk to [name]") | 7.4% | Reach out to referred person immediately. |
| Has tool ("we use [X]") | 2.3% | Objection handle: ask about gaps. |
| Timing ("not right now") | 2.1% | Set reminder. Re-engage per triggers. |

## Programmatic Scoring

Use `src/outbound_qa_engine.py` for automated scoring:
```python
from src.outbound_qa_engine import quick_score, run_qa_gate, compute_mqs
print(quick_score(message_text))  # Human-readable report
```

CLI: `python src/outbound_qa_engine.py demo` or `python src/outbound_qa_engine.py score-batch file.json`
