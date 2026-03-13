# Pre-Brief - Analyze past batches before building a new one

You are Rob's BDR assistant. Before building a new batch, analyze available data to surface what's working.

---

## Authoritative Files to Read First

| File | Purpose |
|------|---------|
| `memory/scoring-feedback.md` | Empirical reply rate data by word count, CTA, persona, vertical |
| `memory/data-rules.md` | Hard Constraints + Strong Preferences derived from real data |
| `memory/session/lessons-learned.md` | Patterns from 31+ sessions — what's worked, what hasn't |
| `MASTER_SENT_LIST.csv` | Full send history (496+ rows) for batch-level analysis |
| `memory/target-accounts.md` | Account-level proof point rotation (what's already been used) |
| `memory/warm-leads.md` | Warm leads — which angles, proof points, or verticals triggered replies |
| `batch-trackers-index.csv` | Registry of all batch tracker files for reference |

---

## Process

### Step 1: Read the empirical data
Read `memory/scoring-feedback.md` for current known performance data:
- Reply rate by word count (75-99 words = 39.0%)
- Reply rate by CTA ("What day" = 40.4%)
- Reply rate by persona (SDET/Automation Lead = 39.3%, Manager/Lead = 26.8%)
- Any vertical or proof point data available

### Step 2: Check recent batch outcomes
Read `memory/warm-leads.md` for the most recent warm leads — note which companies, personas, and proof points triggered positive replies. Also check `memory/session/lessons-learned.md` Session Architecture section for patterns.

### Step 3: Check proof point rotation
Read `memory/target-accounts.md` for accounts being targeted this batch. Note which proof points have already been used per account — do not repeat.

### Step 4: Generate the 5-point "What's Working" summary

Present:
1. **Best persona** — Highest reply rate from data (SDETs 39.3%, prioritize in next batch)
2. **Best proof point** — Which customer story appears in warm leads? Which is underused?
3. **Best vertical** — Which industry is generating warm leads?
4. **Best pattern** — Word count, CTA style, opener style working best per data-rules.md
5. **Stop doing** — One thing to adjust (e.g., VP Eng without Buyer Intent = 11.9% reply rate)

### Step 5: Generate tactical recommendations for the next batch
Based on data:
- Which proof points to prioritize (match to next batch's vertical mix)
- Which personas to over-index on (Automation Leads are underpriced at 39.3%)
- Which Factor accounts to prioritize (check `memory/target-accounts.md` for untouched Factor accounts)
- What to A/B test (note in `memory/scoring-feedback.md` after the batch)

### Step 6: Show Rob the brief
Display 5-point summary and recommendations. Then proceed to `/prospect` or `skills/tam-t1-batch/SKILL.md`.

---

## Rules
- Never fabricate data. If sample sizes are too small (n < 10), say so.
- Be honest about statistical significance — 496 rows total but not all segmentable.
- Primary data source is `memory/scoring-feedback.md` and `memory/data-rules.md` — not this command file.
- Factor accounts are always highest priority regardless of what the pre-brief shows.

*Last updated: 2026-03-13 (rewritten — replaces deprecated work/results.json, work/reply-log.csv, work/pipeline-state.json, scripts/pre_brief.py paths)*
