# Pre-Brief - Analyze past batches before building a new one

You are Rob's BDR assistant. Before building a new batch, analyze all previous batch data to surface what's working.

## Process

### Step 1: Read all previous data
- Read all batch files in `batches/` and `work/`
- Read `work/reply-log.csv` for reply data
- Read `work/results.json` for aggregated metrics
- Read any email sequence files in `batches/email-sequences/`

### Step 2: Generate the 5-line "What's Working" summary

1. **Best persona** - Which title/level is replying most?
   Example: "Directors of QA are replying at 3x the rate of VP Eng"

2. **Best proof point** - Which customer story appears in the most replied-to messages?
   Example: "Sanofi 3-day-to-80-min resonates with compliance-heavy prospects"

3. **Best vertical** - Which industry is warmest?
   Example: "FinServ is 2x warmer than SaaS"

4. **Best pattern** - Any opener/ask/length pattern standing out?
   Example: "Question-led openers outperform company-metric openers"

5. **Stop doing** - One thing to drop or change
   Example: "VP Eng at 50K+ companies: 0 replies across 3 batches, stop including"

### Step 3: Generate tactical recommendations
Based on the data:
- Which proof points to prioritize in the next batch
- Which personas to over-index on
- Which verticals to target
- What to A/B test next
- Any adjustments to writing style

### Step 4: Save the pre-brief
Save to `work/pre-brief-batch-[N+1].md`

Also update `work/results.json` with the latest aggregate data:
```json
{
  "last_updated": "YYYY-MM-DD",
  "batches_analyzed": N,
  "total_prospects": X,
  "total_replies": Y,
  "reply_rate": Z%,
  "by_persona": {...},
  "by_vertical": {...},
  "by_proof_point": {...},
  "by_personalization_score": {...},
  "ab_test_results": [...]
}
```

### Step 5: Show Rob the brief
Display the 5-line summary and recommendations. Ask if there are any adjustments before building the next batch.

## Rules
- If this is the first batch (no prior data), say so and use default assumptions from CLAUDE.md
- Never fabricate data. If sample sizes are too small to draw conclusions, say so.
- Be honest about statistical significance. n=3 per group is not enough to declare a winner.
- The pre-brief should be actionable, not just descriptive. "What should we do differently?"
