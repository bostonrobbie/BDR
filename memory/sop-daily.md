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

⛔ **AUTHORIZED ACCOUNT UNIVERSE — MANDATORY GATE (Effective Mar 9, 2026)**
ALL new prospects MUST come from one of two authorized account lists:
- **Factor Accounts** (38 accounts) — see `memory/target-accounts.md`
- **TAM Accounts — Oct 2025** (312 accounts) — see `/Work/tam-accounts-mar26.csv`
NO open Sales Navigator prospecting outside these lists is permitted. If a prospect's company is not in Factor or TAM, do NOT include them in any batch. This rule cannot be overridden without Rob's explicit written approval. When in doubt: check the list, don't guess.

Gate: only if queue <10, credits >10, no unsent batches, not weekend/Monday.
Pre-Brief → Source 20-25 (from Factor/TAM only) → Apollo enrich → 3-source research → C2 draft → QA Gate → Build HTML tracker.

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

### Tier 0: Named Accounts (THE ONLY AUTHORIZED SOURCE)
Rob's two assigned account lists. These are the only companies Claude is authorized to prospect into. No other accounts are permitted.
- **Factor Accounts (HOT):** 38 accounts (Rob's assigned accounts — Shakeel has departed, all Factor accounts are Rob's as of Mar 9, 2026). Check for unworked Director+ contacts first every session. Full roster: `memory/target-accounts.md`.
- **TAM Accounts (Oct 2025):** Rob's primary NAMER named account list (312 accounts). ICP contacts enriched by LDR team. File: `/Work/tam-accounts-mar26.csv`.
- **Manual Testers TAM:** Supplemental TAM, coordinate with AEs Tyler + Eshwar.
- **Farming Accounts:** Active customers. NOT cold outreach. Coordinate with AE/CSM first.

All Factor account details + enriched contact roster: `memory/target-accounts.md`

### Tier 1: Buyer Intent (High — within authorized accounts only)
Buyer intent signals (Sales Nav, demo requests, webinar attendees <48 hrs) are a PRIORITIZATION signal within the Factor/TAM universe. Only valid if the company is already in Factor or TAM. Does NOT authorize outreach to companies outside those lists.

### Tier 2: Re-Engagement (High — within authorized accounts only)
QA job postings, funding, leadership change, Testsigma feature release, product launch. Only valid for companies in Factor/TAM. Must be >60 days since last touch, new angle required.

### Tier 3: Saved Search Backfill — SUSPENDED
⛔ Open Sales Nav saved search prospecting (pulling net-new companies from broad searches) is SUSPENDED as of Mar 9, 2026. All prospecting must come from Tier 0 authorized accounts. Saved searches may be used to FIND CONTACTS within Factor/TAM companies, but cannot be used to source companies outside those lists.

### Tier 4: Specific Account Targeting
ONLY when Rob explicitly directs. Must still be within Factor/TAM unless Rob explicitly authorizes an exception in writing.

### Batch Size Calculation
```
CREDIT_INMAILS_TODAY = min(8, CREDITS_REMAINING - FOLLOWUP_RESERVE - 5)
OPEN_PROFILE_INMAILS_TODAY = 10-20  (free — do not subtract from credit budget)
CONNECTION_REQUESTS_TODAY = 15      (free)
TOTAL_BATCH = CREDIT_INMAILS_TODAY + OPEN_PROFILE_INMAILS_TODAY + CONNECTION_REQUESTS_TODAY
```
Always fill Open Profile slots first (Pass 1) before spending credits (Pass 2). See `sop-prospect.md` → Two-Pass Search Strategy.

### Daily LinkedIn Send Targets
| Type | Daily Target | Cost |
|------|-------------|------|
| Credit InMails | 8 | 1 credit each |
| Open Profile InMails | 10-20 | FREE |
| Connection requests | 15 | FREE |

### Prospect Mix Ratio (per 25-prospect batch)
- 10-12 QA Manager/Lead (26.8% reply rate)
- 4-6 Director/Head (26.0%)
- 3-5 Architect/Sr IC (39.3%)
- 2-3 Buyer Intent (any title)
- MAX 2 VP/CTO (only with Buyer Intent or QA scope)
- No more than 8 from same vertical
