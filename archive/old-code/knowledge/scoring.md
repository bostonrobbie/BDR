# Scoring Systems

## Priority Scoring (per prospect, 1-5)

Determines the order Rob works prospects. Tracker sorted by priority descending.

**Scoring formula:**
| Factor | Points |
|--------|--------|
| Buyer Intent signal in Sales Navigator | +2 |
| QA-titled leader (Director/Head/VP of QA) | +1 |
| Company in top vertical (FinTech, SaaS, Healthcare) | +1 |
| Recently hired in role (<6 months) | +1 |
| Company in active digital transformation or migration | +1 |
| Company uses a known competitor tool (TOSCA, Katalon, Selenium, etc.) | +1 |
| VP Eng at 50K+ company (no QA-specific scope) | -1 |

**Priority tiers:**
- **5 (Hot):** Work first every morning. Call + InMail same day.
- **4 (Warm):** High priority. Start sequence within 24 hours.
- **3 (Standard):** Normal cadence. Start sequence within the batch cycle.
- **2 (Lower):** Fill out the batch but don't expect high conversion.
- **1 (Long shot):** Only include if batch needs volume. Skip if better options exist.

## Reply-Likelihood Model

Prioritize based on "likelihood of reply given historical behavior," NOT theoretical ICP fit.

**Boost factors:**
- QA-titled leaders: highest reply rate personas
- Companies where a Personalization Score 3 opener can be formed
- Companies in active transformation, acquisition, or scaling
- Buyer Intent signals from Sales Navigator

**Penalize factors:**
- Prospects where only surface-level personalization is possible (Score 1)
- VP Eng at 50K+ companies with no QA-specific scope
- Prospects requiring >120 words to explain relevance (high friction risk)

## Message Quality Score (MQS) - 12-Point System

Every outbound message scored on 4 dimensions (1-3 each). Maximum = 12.

**Dimension 1: Opener Clarity (1-3)**
- 3 = Specific, insight-driven question. No reaching_out, no role-recap.
- 2 = Company-specific reference but generic frame.
- 1 = Opens with "I'm reaching out" or "Seeing that you're the [Title]." Template-visible.

**Dimension 2: CTA Confidence (1-3)**
- 3 = Specific ask with time/action, tied to the value angle. No easy outs.
- 2 = Asks a question but doesn't specify time or tie to value angle.
- 1 = Permission-style, vague, or puts work on the prospect.

**Dimension 3: Personalization Density (1-3)**
- 3 = References something only THIS person would recognize.
- 2 = References their company specifically but opener could apply to anyone in that role.
- 1 = Only swaps name, title, company. Indistinguishable from a template.

**Dimension 4: Friction (1-3, inverted: 3=low friction)**
- 3 = Under 100 words, one proof point, one CTA, no bullets, clean.
- 2 = 100-120 words, may have 2 proof points, still readable.
- 1 = Over 120 words, bullet-point features, multiple CTAs, wall-of-text.

**Interpretation:**
- 10-12 = Ready to send
- 7-9 = Acceptable but should be improved
- <7 = MUST be rewritten

## Message Personalization Score (1-3)

| Score | Meaning | Example |
|-------|---------|---------|
| 3 | **Deep** - References something only THIS person would recognize | "The 'AI Quality Initiatives' part of your title stood out" |
| 2 | **Medium** - References their company but opener could apply to anyone there | "Directing QA at Ally's digital banking platform" |
| 1 | **Light** - Opener is mostly about company/industry, not the person | "QA teams in fintech often tell us..." |

Track per prospect. Compare reply rates by score level over time.

## QA Gate (MANDATORY before any batch is presented)

1. **Rule violation scan**: Check every message against all 7 Hard Constraints (see `data-insights.md`). Any violation = auto-rewrite.
2. **Score computation**: Compute MQS for every message. Show breakdown.
3. **Threshold enforcement**: Only messages scoring >=9/12 may be presented.
4. **Structural dedup**: No two messages in the batch may be structurally identical.
5. **Evidence check**: Every personalization claim must have a research source.
6. **Angle rotation check**: No prospect may receive the same angle in more than one touch.
