# Analytics Engine — TAM Outbound Performance Review

## Description
Aggregates reply rates and conversion data across all TAM Outbound batches (495+ contacts as of Mar 12, 2026 in MASTER_SENT_LIST.csv), then slices by persona, vertical, touch number, proof point, word count, and CTA. Compares Testsigma campaign results against the mabl-era baselines in `memory/data-rules.md`. Generates the Pre-Brief that feeds directly into the next TAM T1 Batch workflow session.

## Trigger
- Scheduled: Mondays at 9am (taskId: `analytics-engine`)
- Run before starting a new batch: "run analytics", "pre-brief for next batch", "what's working?"
- Run after accumulating 3+ new batches since last review
- Run on-demand: "which proof point is best?", "show me persona breakdown", "how are we doing vs baseline?"

## ⛔ APPROVE SEND RULE
This skill is READ-ONLY analytics. It does NOT draft emails or take any outreach action. All recommendations generated here feed into the next TAM T1 Batch workflow (`skills/tam-t1-batch/SKILL.md`), where Rob's explicit APPROVE SEND is still required before any sends.

---

## Baselines (mabl-era, `memory/data-rules.md`)

These are the benchmarks every Testsigma metric is compared against. Grounded in 1,326 LinkedIn conversations (381 replies, 28.7% overall).

| Dimension | Baseline | Source |
|-----------|----------|--------|
| Overall reply rate | 28.7% | 1,326 conversations |
| QA Manager/Lead | 26.8% | mabl data |
| Director of QA | 26.0% | mabl data |
| SDET/Architect/Automation Lead | 39.3% | mabl data — highest tier |
| VP Engineering | 11.9% | mabl data — low, only target with intent |
| C-Level | 9.1% | mabl data — avoid |
| 75-99 word messages | 39.0% | n=775 |
| 100-124 word messages | 27.5% | dropping off |
| 150+ word messages | 21.2% | never for T1 |
| "What day works?" CTA | 40.4% | n=782 — default CTA |
| Thursday sends | 42.1% | best day |
| Tuesday/Friday sends | 29.6% | acceptable |
| Monday sends | 22.9% | worst — avoid T1 |
| Lunch slot (12-1 PM) | 56.5% | n=423 — best time |
| Positive reply rate | 11.3% | meetings/interest |
| Referral reply rate | 8.2% | warm hand-off |

---

## Step 1: Pull Volume Data from MASTER_SENT_LIST.csv

```bash
cd /Work

# Total sends (current state: 495 rows as of Mar 12, 2026)
total=$(tail -n +2 MASTER_SENT_LIST.csv | wc -l)
echo "Total sends: $total"

# Sends per batch (column 2 = batch name)
echo "--- By Batch ---"
awk -F',' 'NR>1 {print $2}' MASTER_SENT_LIST.csv | sort | uniq -c | sort -rn

# Sends per channel (column 4 = channel: Email/LinkedIn InMail/LinkedIn Connection)
echo "--- By Channel ---"
awk -F',' 'NR>1 {print $4}' MASTER_SENT_LIST.csv | sort | uniq -c | sort -rn

# Sends per date (column 3 = send date)
echo "--- By Send Date ---"
awk -F',' 'NR>1 {print $3}' MASTER_SENT_LIST.csv | sort | uniq -c | sort -rn

# Sends per day of week
echo "--- By Day of Week ---"
awk -F',' 'NR>1 {print $3}' MASTER_SENT_LIST.csv | while read d; do date -d "$d" +%A 2>/dev/null; done | sort | uniq -c | sort -rn
```

Known batches as of Mar 12, 2026:
- Batch 1: ~50 contacts, Feb 23, LinkedIn Connection
- Batches 2-5B: ~200 contacts, Feb-Mar, mixed LinkedIn InMail/Connection
- TAM Outbound batches Mar 12: ~40 contacts Email (enrolled in sequence `69afff8dc8897c0019b78c7e`)
- Inbound Leads Mar 12: ~15 contacts Email
- Wave 6 B1/B2: LinkedIn InMail, Mar sessions

---

## Step 2: Pull Reply Data from Gmail

```
Tool: gmail_search_messages
q: "to:robert.gorham@testsigma.com"
maxResults: 200
```

For each reply thread:
```
Tool: gmail_read_thread
threadId: {id}
```

Extract: sender name + email domain, reply date, reply type (positive/referral/timing/tool/decline/OOO/bounce).

Cross-reference each sender's domain against MASTER_SENT_LIST.csv to:
- Identify which batch/touch triggered the reply
- Determine persona (title from MASTER_SENT_LIST or Apollo)
- Determine vertical (industry from company domain)
- Determine proof point used in that T1 (from batch tracker HTML)

**Active warm leads to include (from `memory/warm-leads.md`):**
- Namita Jain (OverDrive) — T1_SENT Feb 27, webinar engagement — counts as P0 interest signal
- Pallavi Sheshadri (Origami Risk) — replied to premature T3 (INC-001), follow-up Mar 2 — T1_REPLIED
- Evely Perrella (Aetna/CVS Health) — inbound, T1 correction sent Mar 12 (INC-012)

---

## Step 3: Parse Batch Tracker HTMLs

Batch trackers are in `/Work/` named `tamob-batch-*.html` (e.g., `tamob-batch-mar12-1.html`).

For each batch tracker, extract per-contact:
- Title (persona classification)
- Company + vertical
- Proof point used (Hansard / CRED / Medibuddy / Cisco / Sanofi / Fortune 100)
- Subject line (SMYKM format)
- Word count from QA gate
- MQS score (should be ≥9/12 to have been enrolled)
- Email status (verified / catchall / unverified)
- Any override flags used

```bash
# List all batch trackers
ls /Work/tamob-batch-*.html 2>/dev/null | sort

# Count contacts per tracker (rough via tr count)
for f in /Work/tamob-batch-*.html; do
  count=$(grep -c "apollo-id" "$f" 2>/dev/null || echo "?")
  echo "$f: $count contacts"
done
```

---

## Step 4: Compute Metrics

For each dimension, calculate: sends (n), replies, reply rate, delta vs baseline.

**Minimum sample size for conclusions: n≥20 sends.** Flag anything below as "(low confidence)."

### Tier 1: Volume (weekly tracking)

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| New contacts enrolled | 25-50/week | {compute} | |
| T1 email sends | 25-50/week | {compute} | |
| Total replies | >28.7% of sends | {compute} | |
| Positive replies | >11.3% of sends | {compute} | |
| Meetings booked | >5% of sends | {compute} | |

### Tier 2: Persona Breakdown

| Title | Sends (n) | Replies | Rate | vs Baseline | Delta |
|-------|-----------|---------|------|-------------|-------|
| QA Manager/Lead | | | | 26.8% | |
| Director of QA / VP QA | | | | 26.0% | |
| SDET / Automation Lead | | | | 39.3% | |
| VP Engineering | | | | 11.9% | |
| Software Eng Manager | | | | ~20% | |

Flag if Testsigma data diverges >5pp from baseline — update `memory/data-rules.md` when n≥50 per persona.

### Tier 3: Proof Point Breakdown

These are the 6 proof points in rotation (see `memory/proof-points.md`):

| Customer Story | Sends (n) | Replies | Rate | Best Vertical Match | Notes |
|---------------|-----------|---------|------|---------------------|-------|
| Hansard (8→5 weeks) | | | | Insurance/FinServ | compliance angle |
| CRED (90% coverage, 5x faster) | | | | FinTech/SaaS | scale angle |
| Medibuddy (2,500 tests, 50% cut) | | | | HealthTech | maintenance angle |
| Cisco (35% regression reduction) | | | | Enterprise | enterprise credibility |
| Sanofi (3 days → 80 min) | | | | Pharma/Compliance | speed angle |
| Fortune 100 (3x in 4 months) | | | | Enterprise | scale+speed combo |

Flag over-rotation: if any one proof point is used >40% of sends, recommend diversifying.

### Tier 4: Message Length

| Word Count | Sends (n) | Replies | Rate | vs Baseline |
|------------|-----------|---------|------|-------------|
| 75-85 words | | | | vs 39.0% |
| 86-99 words | | | | vs 39.0% |
| 100-119 words | | | | vs 27.5% |
| 120+ words | | | | vs 21.2% — flag any |

### Tier 5: Account Type

| Type | Sends (n) | Replies | Rate | Meetings |
|------|-----------|---------|------|----------|
| Factor (intent signal) | | | | |
| TAM HIGH | | | | |
| TAM MEDIUM | | | | |

Factor accounts are highest priority (intent verified). If Factor reply rate isn't beating TAM HIGH, investigate account selection or proof point mismatch.

### Tier 6: Vertical

| Industry | Sends (n) | Replies | Rate | Notes |
|----------|-----------|---------|------|-------|
| FinTech | | | | |
| SaaS/Tech | | | | |
| Healthcare/Digital Health | | | | |
| Retail/E-Commerce | | | | |
| Enterprise/Manufacturing | | | | |
| Insurance/FinServ | | | | Hansard angle |

### Tier 7: Email Status (catchall flag)

Wave 6 B2 finding: 8/12 companies had catchall domains — emails look valid but aren't verified. Cross-reference against known catchall domains from batch trackers.

| Email Status | Sends (n) | Bounces | Bounce Rate |
|--------------|-----------|---------|-------------|
| Verified | | | |
| Catchall | | | flag if >15% |
| Unverified | | | |

---

## Step 5: Generate Pre-Brief for Next Batch

This is the 5-line summary that Rob reviews before the TAM T1 Batch session starts (per `memory/playbooks/tam-t1-batch.md` Step 2):

```
PRE-BRIEF — {date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. BEST PERSONA: {title} — {N}% reply rate (n={N}) vs {N}% baseline
   → Prioritize this title in next batch
   → [or: INCONCLUSIVE — need n≥20 for {title}]

2. BEST PROOF POINT: {customer story} — {N}% when used (n={N})
   → Lead with this in opener/challenge hook
   → [or: rotate Hansard/CRED/Medibuddy evenly — no winner yet]

3. BEST VERTICAL: {industry} — {N}% (n={N})
   → TAM accounts in this vertical: check tam-accounts-mar26.csv
   → [or: insufficient sample — SaaS/FinTech tied at {N}%]

4. PATTERN: {strongest positive pattern}
   → e.g., "75-85 word messages outperforming 86-99 by 6pp (n=47 vs n=23)"
   → [or: no significant pattern yet — need more batches]

5. STOP DOING: {one underperforming dimension}
   → e.g., "VP Engineering at non-Factor accounts — 8.3% (n=24), well below 11.9% baseline"
   → [or: no clear outlier yet]

ANOMALIES:
  • {anything that diverges >5pp from baseline — explain if possible}
  • {any proof point performing unexpectedly}
  • {any catchall domain cluster causing phantom opens}
```

---

## Step 6: Update `memory/data-rules.md` (when warranted)

Only update baselines when Testsigma data meets confidence thresholds:
- Persona rates: n≥50 sends to that title
- Proof point rates: n≥30 sends with that story
- Day/time rates: n≥100 sends in that slot

When updating, add a comment: `# Updated {date} based on Testsigma data (n={N})`

Never delete the original mabl-era baselines — move them to a "Historical Baselines" section.

---

## Output Format

### Quick Chat Summary:
```
ANALYTICS SNAPSHOT — {date range}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VOLUME: {N} total sends | {N} replies ({N}%) | {N} meetings
vs BASELINE: 28.7% overall (mabl-era)

PERSONA LEADERS:
  📈 SDET/Automation: {N}% (n={N}) — {vs 39.3% baseline}
  📈 QA Manager: {N}% (n={N}) — {vs 26.8% baseline}
  📉 VP Eng: {N}% (n={N}) — {vs 11.9% baseline — only use w/ intent}

PROOF POINT WINNERS:
  🏆 {story}: {N}% (n={N})
  ⚠️  {story}: {N}% (n={N}, low confidence)

NEXT BATCH ACTIONS:
  1. {highest-confidence recommendation}
  2. {second recommendation}
  3. {one thing to stop or reduce}

PRE-BRIEF ready for copy-paste into next TAM T1 Batch session. ↑
```

### Full HTML Report (on-demand):
Generate `/Work/analytics-report-{date}.html` with all tier tables and delta charts.

---

## Scheduled Task Config
```
taskId: analytics-engine
cronExpression: "0 9 * * 1"
description: "Weekly TAM Outbound performance review — Mondays 9am"
```

---

## Integration Points
- Reads: `MASTER_SENT_LIST.csv`, all `tamob-batch-*.html` trackers, `memory/warm-leads.md`, `memory/contact-lifecycle.md`, `memory/data-rules.md`
- Uses: Gmail MCP (reply data), Apollo MCP (sequence metrics if needed)
- Outputs: Pre-Brief for next batch, quick chat summary, optional HTML report
- Feeds into: `skills/tam-t1-batch/SKILL.md` Step 2 (Pre-Brief), `memory/data-rules.md` updates
- Does NOT: Send anything, draft anything, modify DNC list, or enroll contacts

*Source: `memory/data-rules.md` (mabl-era baselines) + `memory/playbooks/tam-t1-batch.md` (Pre-Brief format) + `memory/scoring-feedback.md`*
*Last updated: 2026-03-12 (Session 30 rewrite — grounded in real TAM Outbound data)*

---

## Self-Improvement Loop

This skill maintains its own run log and learned-patterns file. Full protocol: `skills/_shared/learning-loop.md`

### Before Each Run
1. Read `skills/analytics-engine/learned-patterns.md` if it exists — apply any documented calibration adjustments
2. Count entries in `skills/analytics-engine/run-log.md` to determine current run number

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
3. Overwrite `skills/analytics-engine/learned-patterns.md` with updated findings
4. If a pattern appears in 4+ of 5 runs: write a `## SKILL UPDATE PROPOSAL — analytics-engine` entry to `memory/session/messages.md` for Rob's review

**Hard rule:** Never modify SKILL.md directly. Only propose updates via messages.md and wait for Rob's explicit approval.
