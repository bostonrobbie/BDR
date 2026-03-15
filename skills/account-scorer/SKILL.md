# Dynamic Account Scorer

**Version:** 1.0 — Created Mar 15, 2026
**Last Updated:** Mar 15, 2026
**Owner:** Claude (scheduled + on-demand)
**Status:** Active

---

## Skill Header

| Field | Value |
|-------|-------|
| **Name** | Dynamic Account Scorer |
| **Trigger** | `score my accounts` \| `which accounts should I hit this week` \| `top accounts` \| Monday 6:25 AM schedule |
| **Schedule** | Mondays 6:25 AM (before auto-prospect-enroll 6:30 AM) + on-demand |
| **Execution Time** | ~3-5 minutes |
| **Output** | `memory/account-scores-[YYYY-MM-DD].md` + summary appended to `memory/session/messages.md` |
| **Downstream Consumers** | auto-prospect-enroll, morning-briefing, batch-builder |
| **Inputs** | tam-accounts-mar26.csv, MASTER_SENT_LIST.csv, memory/session/messages.md (trigger-monitor output), memory/warm-leads.md |
| **Depends On** | trigger-monitor (runs at 6:10 AM), warm-leads.md updated |

---

## Purpose

Re-score all 350 TAM+Factor accounts weekly using a weighted multi-signal model. Generate a ranked top-25 list so downstream skills (auto-prospect-enroll, morning-briefing) and Rob's manual work always target the highest-intent accounts first.

**Why:** Without dynamic scoring, Rob doesn't know which accounts are hot this week. Factor accounts (intent-flagged) are highest priority per operating directive, but trigger signals (QA hiring, funding, leadership changes) can elevate TAM accounts above pure Factor. Weekly re-scoring ensures focus shifts with the market.

---

## Phase 1 — Load Account Universe

### Step 1a: Load TAM Account Master

Read `/sessions/funny-nifty-dirac/mnt/Work/tam-accounts-mar26.csv` and extract:
- `company_name`
- `domain`
- `icp_tier` (HIGH, MEDIUM, or LOW)
- `factor_flag` (Y/N — intent signal from Factor data)
- `vertical` (SaaS, FinTech, HealthTech, Retail, Telecom, Pharma, Other)
- `employee_count` (numeric)

Expected: 350 rows (312 TAM + 38 Factor).

### Step 1b: Load Send History

Read `/sessions/funny-nifty-dirac/mnt/Work/MASTER_SENT_LIST.csv` and build a lookup table:
- Key: `company_name` (normalized)
- Value: `most_recent_send_date` (YYYY-MM-DD), `total_sends`, `bounce_count`, `bounce_rate`

### Step 1c: Build Lookups

**Recently Touched (< 30 days):**
- For each TAM account, check if `most_recent_send_date < 30 days ago`
- Mark as COOLING OFF (skip entirely from scoring)
- Log count in output

**Bounce Risk:**
- For each account, compute `bounce_rate = bounce_count / total_sends`
- If `bounce_rate > 0.5` (more than 50% bounced), mark as BOUNCE RISK
- These still score normally, but flag in output so Rob can review

**Warm Leads Bonus:**
- Read `memory/warm-leads.md`
- Extract contacts marked P0-P2 (active warm) by company name
- Note: these get +25 pts bonus in Phase 2

### Step 1d: Load Trigger Signals

Read `memory/session/messages.md` and extract any messages from trigger-monitor (runs 6:10 AM):
- Pattern: `[date] Trigger Monitor: [company_name] — QA hiring active` → company gets QA job bonus
- Pattern: `[date] Trigger Monitor: [company_name] — Series A-C funding` → company gets funding bonus
- Pattern: `[date] Trigger Monitor: [company_name] — New QA/Eng leader` → company gets leadership bonus
- Pattern: `[date] Trigger Monitor: [company_name] — New CI/CD/Cloud platform` → company gets tech bonus

Build trigger lookup: `company_name → [list of active trigger signals this week]`

---

## Phase 2 — Scoring Model (100 points total)

Each account receives a composite score based on:

### Base Score (0-75 points)

| Signal | Points | Logic |
|--------|--------|-------|
| **Factor account** (intent-flagged) | +40 | Y/N in `factor_flag` column |
| **ICP tier HIGH** | +20 | From `icp_tier` column; mutually exclusive with MEDIUM/LOW |
| **ICP tier MEDIUM** | +10 | From `icp_tier` column; mutually exclusive with HIGH/LOW |
| **ICP tier LOW** | +0 | Baseline; no points |
| **Vertical match** | +10 | Vertical ∈ {SaaS, FinTech, HealthTech, Retail, Telecom, Pharma} |
| **Employee count sweet spot** | +5 | 200 ≤ employee_count ≤ 2000 |

**Subtotal: Base Score**

### Trigger Bonus (0-60 points, cumulative)

Read trigger signals from Phase 1d. For each active trigger this week:

| Signal | Points | Logic |
|--------|--------|-------|
| **QA job posting active** | +20 | Company posting QA Manager, QA Lead, SDET, Automation Engineer role |
| **Recent funding (Series A-C)** | +15 | Funding round closed within last 90 days |
| **Leadership change** | +15 | New VP Eng, VP QA, Eng Manager, QA Manager in last 90 days |
| **Technology change** | +10 | New CI/CD platform (GitHub Actions, GitLab, Jenkins), new cloud (AWS→GCP migration), new test framework adoption |

All trigger bonuses are **cumulative** (account can score up to 60 trigger pts if all signals present).

**Subtotal: Trigger Bonus**

### Recency Adjustment (-15 to 0 points)

Check `most_recent_send_date` from MASTER_SENT_LIST:

| Recency | Adjustment | Logic |
|---------|------------|-------|
| **Last touch < 30 days** | SKIP ENTIRELY | Account in cooling-off window; do not score, do not include in output (log separately) |
| **Last touch 30-60 days** | -15 pts | Too recent; give Rob breathing room before re-engagement |
| **Last touch 60-90 days** | -5 pts | Mild recency penalty; Rob may re-touch if score is strong |
| **Last touch > 90 days** | 0 pts | Neutral; fair game |
| **No prior contact** | 0 pts | Neutral; fresh account |

### Warm Lead Bonus (+25 points, one-time)

If account appears in `memory/warm-leads.md` as P0-P2 (active warm lead):
- Add **+25 pts** bonus
- This represents prior positive engagement; high conversion signal

---

## Phase 3 — Rank and Segment

### Step 3a: Calculate Final Scores

For each non-cooling-off account:

```
final_score = base_score + trigger_bonus + recency_adjustment + (warm_lead_bonus if applicable else 0)
```

Clamp to [0, 160] range (theoretical max: 75 base + 60 trigger + 0 recency + 25 warm = 160).

### Step 3b: Rank Descending

Sort all scored accounts by `final_score DESC`.

### Step 3c: Segment Into Tiers

| Tier | Score Range | Count | Action |
|------|-------------|-------|--------|
| 🔥 TIER 1 — Immediate Priority | ≥ 50 | Top 10 | Target this week; feed to auto-prospect-enroll |
| 🎯 TIER 2 — Secondary | 30-49 | Next 15 | Target if bandwidth allows; queue for following week |
| 📋 TIER 3 — Backlog | < 30 | Remaining | Seasonal campaigns or future batches |

### Step 3d: Exclude & Log

Separately list:
- **Cooling Off (< 30 days):** Company name, last_touch_date, days_since_touch
- **Bounce Risk (> 50% bounce rate):** Company name, bounce_count, bounce_rate, recommendation (cold outreach risky; consider warm intro)

---

## Phase 4 — Generate Output File

### Step 4a: Create memory/account-scores-[YYYY-MM-DD].md

Header:
```markdown
# Account Scores — [YYYY-MM-DD]

**Generated:** [timestamp, e.g., 2026-03-15 06:25 AM]
**Model Version:** 1.0 — Weighted multi-signal scoring
**TAM Universe:** 350 accounts (312 TAM + 38 Factor)
**Scoring Date Range:** Trigger signals current as of trigger-monitor 6:10 AM run

---

## Scoring Model Summary

- **Base:** Factor flag (40 pts) + ICP tier (20/10/0 pts) + Vertical match (10 pts) + Employee count (5 pts)
- **Triggers:** QA hiring (+20) + Funding (+15) + Leadership (+15) + Tech change (+10)
- **Recency:** Last touch < 30 days SKIP | 30-60 days (-15) | 60-90 days (-5) | > 90 or no prior (0)
- **Warm Lead Bonus:** P0-P2 in warm-leads.md (+25)
- **Max Score:** 160 points

---

## TIER 1 — Top 10 (Immediate Priority)

| Rank | Company | Score | Factor | ICP | Vertical | Employees | Last Touch | Days Since | Trigger Signal | Warm Lead? | Recommended Action |
|------|---------|-------|--------|-----|----------|-----------|------------|------------|----------------|------------|-------------------|
| 1 | [Company A] | [score] | Y/N | HIGH/MEDIUM | SaaS | [count] | [date] | [N] | QA hiring + Funding | Y/N | Hit immediately; warm if possible |
| 2 | [Company B] | [score] | Y/N | HIGH/MEDIUM | FinTech | [count] | [date] | [N] | QA hiring | Y/N | Cold outreach; target QA Lead |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 10 | [Company J] | [score] | Y/N | HIGH/MEDIUM | Retail | [count] | [date] | [N] | Leadership change | Y/N | Gentle re-engage due to recency |

---

## TIER 2 — Next 15 (Secondary Priority)

| Rank | Company | Score | Factor | ICP | Vertical | Trigger Signal | Last Touch (days ago) | Action |
|------|---------|-------|--------|-----|----------|-----------------|----------------------|--------|
| 11 | [Company K] | [score] | Y/N | HIGH | Telecom | Funding | [N] | Queue for week of [date] |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 25 | [Company Y] | [score] | Y/N | MEDIUM | Pharma | None | [N] | Monitor for trigger signals |

---

## Accounts Cooling Off (< 30 days — Skipped)

| Company | Last Touch | Days Since | Notes |
|---------|------------|------------|-------|
| [Company X] | 2026-03-10 | 5 | Skip until 2026-04-09 |
| ... | ... | ... | ... |

**Total:** [N] accounts cooling off

---

## Bounce Risk Accounts (> 50% bounce rate — Flag Review)

| Company | Bounce Rate | Bounced/Total | Recommendation |
|---------|------------|---|--------------|
| [Company Z] | 75% (3/4) | 3 bounced | Consider warm intro instead of cold email |
| ... | ... | ... | ... |

**Total:** [N] accounts flagged

---

## Key Insight This Week

[One-sentence analysis, e.g., "QA hiring signals dominate tier 1 — 7 of top 10 have active postings. Recommend targeting QA Manager titles first this week."]

---

## Next Steps

1. **auto-prospect-enroll:** Will read TIER 1 list and prospect the top 10 accounts starting at 6:30 AM
2. **morning-briefing:** Will display top 3 accounts in Rob's 6:00 AM briefing
3. **Manual override:** Rob can request re-scoring on-demand with `score my accounts` command

---

## Metadata

- **Run Time:** [seconds]
- **Non-cooling accounts scored:** [N]
- **TIER 1 count:** [N]
- **TIER 2 count:** [N]
- **Factor accounts in TIER 1:** [N] of 38
- **Warm leads in TIER 1:** [N] of [total active warm]
- **Skill Version:** 1.0
```

### Step 4b: Append Summary to memory/session/messages.md

Append a single-line summary in the format:

```
[YYYY-MM-DD HH:MM] Account Scorer: Top account this week = [Company] (score: [score]). [N] Factor accounts active in TIER 1. [N] accounts cooling off (30-day window).
```

Example:
```
2026-03-15 06:25 Account Scorer: Top account this week = Acme FinTech (score: 125). 8 Factor accounts active in TIER 1. 12 accounts cooling off (30-day window).
```

---

## Phase 5 — Feed Into Downstream Skills

### Dependency Graph

```
account-scorer (6:25 AM)
    ↓
    Output: memory/account-scores-[YYYY-MM-DD].md
    ↓
    Consumed by:
    ├─→ auto-prospect-enroll (6:30 AM)
    │   Reads TIER 1 list, selects accounts to prospect this run
    ├─→ morning-briefing (displays top 3 in 6:00 AM summary)
    └─→ batch-dashboard (updates top-10 panel)
```

**Critical:** If account-scorer fails or runs late, auto-prospect-enroll will fall back to reading the PREVIOUS day's account-scores-[date].md (graceful degradation).

---

## Learning Loop Integration

Follow `skills/_shared/learning-loop.md`.

### What to Log

Each run, append to `skills/account-scorer/run-log.md`:

```markdown
## Run [N] — [YYYY-MM-DD HH:MM]

- Top account: [Company] (score: [score])
- TIER 1 count: [N]
- Factor accounts in TIER 1: [N]
- Accounts cooling off: [N]
- Bounce risk flags: [N]
- Trigger signal breakdown: [N] QA hiring, [N] funding, [N] leadership, [N] tech
- Run time: [Ns]
```

### Review Cycle (Every 5 Runs)

After every 5th run (typically ~5 weeks), review effectiveness:

1. **Read run-log.md** — note top accounts over last 5 weeks
2. **Query analytics.outreach.db** — for those top accounts, calculate:
   - Reply rate among TIER 1 accounts
   - Reply rate among TIER 2 accounts
   - Do Factor accounts outperform ICP-only accounts?
   - Do trigger signals correlate with replies?
3. **Update learned-patterns.md** with findings
4. **Adjust weights if clear pattern emerges:**
   - Example: "Factor accounts + trigger signal = 85% reply rate; Factor-only = 62%; increase trigger weights by 10%"
   - Example: "Leadership signals yield no reply lift; consider removing or deprioritizing"

Do NOT change weights without evidence across 5+ runs.

---

## Execution Steps (For Claude Automaton)

When triggered (`score my accounts` or Monday 6:25 AM):

1. Load tam-accounts-mar26.csv → extract all 350 accounts
2. Load MASTER_SENT_LIST.csv → build recency lookup
3. Load memory/session/messages.md → extract trigger-monitor signals
4. Load memory/warm-leads.md → identify P0-P2 companies
5. For each account:
   - Calculate base_score (Factor + ICP + Vertical + Employee count)
   - Apply trigger bonuses (QA hiring, funding, leadership, tech)
   - Apply recency adjustment
   - Apply warm_lead bonus if applicable
   - Clamp to [0, 160]
6. Rank all non-cooling accounts by score DESC
7. Segment: TIER 1 (top 10, score ≥ 50), TIER 2 (next 15, 30-49), TIER 3 (rest)
8. Generate memory/account-scores-[YYYY-MM-DD].md with full tables
9. Append 1-line summary to memory/session/messages.md
10. Log run to skills/account-scorer/run-log.md
11. Return: "Scored 350 accounts. TIER 1 = [N] accounts, led by [Company]. Output: memory/account-scores-[YYYY-MM-DD].md"

---

## Error Handling

| Error | Mitigation |
|-------|-----------|
| tam-accounts-mar26.csv missing | Fail with error; ask Rob for path |
| MASTER_SENT_LIST.csv missing | Warn; continue with no recency data (all accounts score normally) |
| memory/session/messages.md missing | Warn; continue with no trigger signals (base + recency only) |
| memory/warm-leads.md missing | Warn; continue with no warm lead bonus |
| trigger-monitor hasn't run yet (before 6:10 AM) | Graceful; use stale trigger signals from previous day's messages.md |
| Account domain not in MASTER_SENT_LIST | Treat as no prior contact (recency = 0 pts) |

---

## Performance Notes

- **Execution time:** 3-5 minutes for 350 accounts (Python/pandas recommended for speed)
- **File I/O:** 4 reads (tam-accounts, MASTER_SENT_LIST, messages.md, warm-leads.md), 2 writes (account-scores-[date].md, append to messages.md)
- **Bottleneck:** Large MASTER_SENT_LIST (597+ rows) lookup — use hashmap for O(1) lookups

---

## Success Criteria

✅ Output file created with all 350 accounts processed
✅ TIER 1 list contains top 10, all with score ≥ 50
✅ TIER 2 contains next 15, all with score 30-49
✅ Cooling-off accounts properly excluded and logged separately
✅ Summary appended to messages.md within 10 minutes of scheduled run
✅ Run logged to run-log.md
✅ File exists and is readable by downstream skills (auto-prospect-enroll, morning-briefing)

---

## Maintenance & Updates

**Schedule for refinement:**
- **Every 5 runs:** Review effectiveness (read run-log.md + analytics.outreach.db)
- **Monthly:** Refresh trigger signals from Factor data (coordinate with trigger-monitor skill)
- **Quarterly:** Audit ICP tier accuracy in tam-accounts-mar26.csv
- **As-needed:** Adjust weights based on learned-patterns.md findings

**Owner:** Claude (with Rob's oversight on weight tuning)

---

## Appendix — Scoring Example

**Account: Acme Corp**
- TAM account (not Factor): 0 pts
- ICP tier: HIGH → 20 pts
- Vertical: SaaS → 10 pts
- Employee count: 500 → 5 pts
- **Base Score:** 35 pts

**Triggers (from trigger-monitor output this week):**
- QA job posting (Automation Engineer) → +20 pts
- Recent funding (Series B, 45 days ago) → +15 pts
- **Trigger Bonus:** 35 pts

**Recency:**
- Last touch: 2026-02-15 (29 days ago) → SKIP (cooling off)

**Result:** Acme Corp does NOT appear in output; logged in "Cooling Off" section. Will re-score on 2026-03-16 (30 days).

---

**Account: TechStart Inc.**
- Factor account: 40 pts
- ICP tier: MEDIUM → 10 pts
- Vertical: FinTech → 10 pts
- Employee count: 250 → 5 pts
- **Base Score:** 65 pts

**Triggers:**
- QA job posting → +20 pts
- Leadership change (new VP QA, 60 days ago) → +15 pts
- **Trigger Bonus:** 35 pts

**Recency:**
- Last touch: 2026-02-01 (72 days ago) → 0 pts (no penalty)

**Warm Lead:**
- In warm-leads.md as P1 (active warm) → +25 pts

**Final Score:** 65 + 35 + 0 + 25 = **125 pts**
**Tier:** TIER 1 (≥ 50)
**Rank:** Likely top 3-5 depending on other accounts
**Action:** Hit immediately; reference warm relationship in outreach

---

## Related Skills

- **trigger-monitor:** Feeds trigger signals into messages.md; run at 6:10 AM (before account-scorer)
- **auto-prospect-enroll:** Consumes TIER 1 list; runs at 6:30 AM (after account-scorer)
- **morning-briefing:** Displays top 3 accounts; reads account-scores-[date].md
- **batch-dashboard:** Updates top-10 account panel; refreshed daily
- **learning-loop:** Shared framework for run logging and pattern detection

---

**End of SKILL.md**
