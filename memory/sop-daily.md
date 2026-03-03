# "Run the Daily" — Automated Daily Outreach Workflow

Trigger phrases: "run the daily", "daily run", "morning run", "start outreach", "run outreach"

## Phase 1: Intel Scan (~5 min)
1. Read CLAUDE.md for pipeline state, DNC, warm leads, credits
2. Read latest batch tracker files for send dates and statuses
3. Search Gmail for replies (to robert.gorham@testsigma.com)
4. Check Google Calendar for today's meetings
5. Calculate follow-up queue (Day 5 Touch 2, Day 10 Touch 3)
6. Check InMail credit budget
7. **Gmail Draft Audit (MANDATORY):** Cross-reference drafts against eligible dates. Flag orphans, premature, old-template, unscored drafts.

## Phase 2: Reply Processing (~10-20 min)
Skip if zero replies. Classify replies, draft responses per type, generate meeting prep if booked. Present for approval. Tag in tracker.

## Phase 3: Follow-Up Queue (~20-30 min)
Skip if no Day 5/10 prospects. Draft Touch 2 InMails (new angle, 40-70w) and Touch 3 Emails (fresh proof, 60-100w). Credit budget check. Present sorted by priority.

## Phase 4: New Pipeline (~60-90 min)
Gate: only if queue <10, credits >10, no unsent batches, not weekend/Monday.
Pre-Brief → Source 20-25 → Apollo enrich → 3-source research → C2 draft → QA Gate → Build HTML tracker.

## Phase 5: Daily Deliverable (~10 min)
Summary, log updates, tomorrow preview, numbered action items for Rob.

## Adaptive Logic
| Condition | Adaptation |
|-----------|------------|
| Credits < 5 | Skip new Touch 1s. Email + reply processing only. |
| Credits < 10 | Touch 2 only for Hot/Warm. |
| 5+ replies | Extend Phase 2, defer Phase 4. |
| No replies, light queue | Maximize Phase 4. |
| Monday | No sends. Research + batch build. |
| Thursday | Maximize send volume. |
| Weekend | Research only. No sends. |
| Warm lead reply | Process FIRST. |

## Weekly Targets
| Metric | Weekly | Monthly |
|--------|--------|---------|
| New Touch 1 | 20-25 | 80-100 |
| Touch 2 | 15-20 | 60-80 |
| Touch 3 | 10-15 | 40-60 |
| Replies | 5-7 | 20-30 |
| Meetings | 1-2 | 4-8 |

## Batch Sourcing Decision Framework (SOP D)
Claude follows this waterfall autonomously (never asks Rob which method):

### Tier 1: Buyer Intent (Highest)
Sales Nav Buyer Intent, website demo requests, webinar attendees (<48 hrs).

### Tier 2: Re-Engagement (High)
QA job postings, funding, leadership change, Testsigma feature release, product launch. Must be >60 days since last touch, new angle required.

### Tier 3: Saved Search Backfill (Standard)
Sales Nav saved searches, "Show X new results" filter, Prospect Mix Ratio.

### Tier 4: Specific Account Targeting
ONLY when Rob explicitly directs.

### Batch Size Calculation
MAX_BATCH = (CREDITS_REMAINING - FOLLOWUP_RESERVE - 5) / 1

### Prospect Mix Ratio (per 25-prospect batch)
- 10-12 QA Manager/Lead (26.8% reply rate)
- 4-6 Director/Head (26.0%)
- 3-5 Architect/Sr IC (39.3%)
- 2-3 Buyer Intent (any title)
- MAX 2 VP/CTO (only with Buyer Intent or QA scope)
- No more than 8 from same vertical
