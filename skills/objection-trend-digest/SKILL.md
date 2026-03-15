# Skill: Objection Trend Digest

**Trigger:** Runs Fridays at 5:15 PM (after weekly-analytics at 5:00 PM). Also callable on-demand.
**Purpose:** Scan all classified replies from the current week and surface which objections appeared most frequently. Identifies emerging patterns across batches before they become systemic problems. Feeds into messaging strategy adjustments.
**Output:** Appends a `## OBJECTION TREND DIGEST` section to `memory/session/messages.md` and logs data to `analytics/outreach.db`.

---

## What This Skill Does

1. Reads `memory/warm-leads.md` for all new classifications from the past 7 days
2. Reads the reply-classifier run logs for this week
3. Tallies objections by type, persona, vertical, and batch
4. Compares against prior weeks to detect trends (rising, falling, new)
5. Surfaces actionable messaging recommendations
6. Writes to messages.md + updates the objections table in analytics DB

---

## Phase 1: Collect This Week's Replies

**Step 1a — Read warm-leads.md**

Read `memory/warm-leads.md`. Filter for entries with a date in the past 7 days (since last Friday).

Extract for each reply:
- Contact name, company, title, vertical
- Classification: P0, P1, P2, P3, P4
- Objection type (if P2/P3/P4): pricing, timing, competitor, not relevant, no response, already have solution, other
- Batch number
- Sequence stage when reply came (T1, T2, T3)

**Step 1b — Read reply-classifier run logs**

Check `skills/reply-classifier/run-log.md` for this week's run summaries. Pull any P-classification counts recorded there.

**Step 1c — Build this week's raw reply table**

```
{ name, company, title, vertical, batch, stage, classification, objection_type, date }
```

If fewer than 3 replies this week: note "Low reply volume this week — trend data may not be statistically meaningful" but still run.

---

## Phase 2: Tally and Categorize

**Objection Type Counts (this week):**

Count occurrences of each objection type across all P2/P3/P4 replies:

| Objection Type | Definition |
|---------------|-----------|
| Timing | "Reach out in Q3", "after budget cycle", "not now" |
| Competitor | "Using [tool]", "happy with current solution" |
| Pricing | "Too expensive", "need to check budget" |
| Not Relevant | "Not in QA", "wrong person", "we don't do this" |
| Already Have Solution | "We built in-house", "we use Selenium fine" |
| Positive Engage | P0/P1 — interested or meeting booked |
| Ghost / No Reply | P4 — no response at T2 or T3 stage |
| Other | Everything else |

**Breakdowns to compute:**
- By objection type (top 3 this week)
- By vertical (which verticals are objecting most)
- By persona (which titles are objecting most)
- By batch (any single batch driving disproportionate objections?)
- By sequence stage (are objections heavier at T1 vs T2 vs T3?)

---

## Phase 3: Week-over-Week Trend Detection

Read `skills/objection-trend-digest/run-log.md` for prior week entries. Extract prior week objection counts.

**Trend flags:**

| Signal | Threshold | Action |
|--------|-----------|--------|
| Rising objection type | +2 or more vs prior week | Flag as "📈 RISING" |
| Falling objection type | -2 or more vs prior week | Flag as "📉 FALLING" |
| New objection type | Appeared this week, not last | Flag as "🆕 NEW" |
| Dominant single type | >50% of all objections | Flag as "⚠️ CONCENTRATION" |
| Batch outlier | 1 batch has >40% of objections | Flag as "⚠️ BATCH ISSUE" |

**Benchmark context (from training data):**
- Timing objections: typically 30-40% of all objections — normal
- Competitor objections: typically 15-25% — investigate if >35%
- Not Relevant: should be <15% — if higher, ICP targeting may be off
- Positive Engage (P0/P1): target >10% of all replies

---

## Phase 4: Messaging Recommendations

For each flagged trend, generate a specific recommendation:

| Trend | Recommendation |
|-------|---------------|
| Timing rising | Adjust opener to acknowledge "budget cycles" — lead with ROI payback, not features |
| Competitor rising | Pull competitor comparison from Google Drive (ID: 1yFYzrb1FdCOzI9FoVcN2MyfI_vfLOqGy-79SLgjJ0Kc) — update T2 with competitive angle |
| Not Relevant rising | Review persona targeting — are recent batches hitting wrong titles? Flag for ICP audit |
| Already Have Solution rising | Lead with self-healing / maintenance reduction angle — speak to "improving what you have" |
| Positive Engage falling | Review recent T1 subjects and openings — may need refresh |
| Batch outlier | Review that batch's persona mix or company vertical — may have been off-ICP |

---

## Phase 5: Write to messages.md

Append the following to `memory/session/messages.md`:

```markdown
---
## OBJECTION TREND DIGEST — Week of [DATE]

**Replies classified this week:** [N]
**P0/P1 (warm/meeting):** [N] ([%])
**P2/P3 (objection):** [N] ([%])
**P4 (no reply/ghost):** [N] ([%])

### This Week's Objection Mix

| Objection Type | Count | % of Objections | vs Last Week |
|---------------|-------|-----------------|-------------|
| Timing | [N] | [%] | [📈/📉/➡️] |
| Competitor | [N] | [%] | [trend] |
| Not Relevant | [N] | [%] | [trend] |
| Already Have Solution | [N] | [%] | [trend] |
| Pricing | [N] | [%] | [trend] |
| Other | [N] | [%] | [trend] |

### ⚠️ Flags This Week
- [flag type]: [detail]

### 📊 Breakdown Insights
- **Top objecting vertical:** [vertical] ([N] replies)
- **Top objecting persona:** [title] ([N] replies)
- **Heaviest stage:** T[N] ([N] objections)
- **Batch outlier:** [batch or "none"]

### 💡 Messaging Recommendations
1. [Recommendation based on top trend]
2. [Recommendation based on second trend]
3. [Recommendation if applicable]

---
**Prior week comparison available in:** `skills/objection-trend-digest/run-log.md`
```

---

## Phase 6: Update Analytics DB

Using Python + sqlite3, insert a weekly summary row into `analytics/outreach.db`:

```sql
INSERT INTO weekly_summary (week_start, total_replies, p0_p1_count, p2_p3_count, p4_count,
    top_objection, top_objection_count, second_objection, second_objection_count,
    top_objecting_vertical, top_objecting_persona, notes)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
```

If the `weekly_summary` table doesn't have an objections breakdown column yet, add a `objection_json` TEXT column and store the full breakdown as JSON.

---

## Hard Rules

- Read only — never modify warm-leads.md or MASTER_SENT_LIST.csv
- Never recommend changing the T1 formula without flagging it as a proposal for Rob's review
- If warm-leads.md has no entries from this week: note "No replies classified this week" and exit cleanly
- Do NOT surface individual contact names in the trend summary — this is aggregate only
- Competitor mentions in replies: note the competitor name in the trend report (e.g., "Competitor: Tricentis x3, Katalon x1") — valuable intel

---

## Self-Improvement Loop

### Before Each Run
1. Read `skills/objection-trend-digest/learned-patterns.md` if it exists
2. Apply any documented calibration adjustments (e.g., adjusted objection type keywords, benchmark recalibration)
3. Count entries in `skills/objection-trend-digest/run-log.md` to determine run number

### After Every Run — Append to run-log.md
```
### Run #[N] — [DATE]
- **Replies processed:** [N total, breakdown by P-class]
- **Top objection this week:** [type] ([N])
- **Flags raised:** [list or "none"]
- **Recommendations generated:** [N]
- **Anomalies:** [anything unexpected]
- **Output quality:** [Accurate / Mostly accurate / Needs calibration]
```

### Every 5th Run — Pattern Review
1. Read last 5 entries in `skills/objection-trend-digest/run-log.md`
2. Identify which objection types appear consistently, which benchmarks need recalibration, which recommendations kept repeating
3. Update `skills/objection-trend-digest/learned-patterns.md`
4. If same recommendation appears 4+ of 5 weeks: write a `## SKILL UPDATE PROPOSAL — objection-trend-digest` entry to `memory/session/messages.md` for Rob's review

---

## Scheduled Task Config

```
Name: objection-trend-digest
Schedule: Fridays at 5:15 PM (after weekly-analytics)
Cron: 15 17 * * 5
```
