# "Run the Daily" — Automated Daily Outreach Workflow
## Version 2.0 — Updated Mar 12, 2026 (Rewritten for TAM Outbound email-first reality. LinkedIn InMail is secondary/suspended. Apollo task queue is the primary follow-up controller.)

Trigger phrases: "run the daily", "daily run", "morning run", "start outreach", "run outreach"

---

## Current Operating Mode (as of Mar 12, 2026)

**Primary channel:** TAM Outbound email via Apollo sequence (TAM Outbound - Rob Gorham, `69afff8dc8897c0019b78c7e`)
**Follow-up controller:** Apollo Tasks tab — all T2/T3 tasks surface here on their cadence days
**LinkedIn InMail:** ⛔ SUSPENDED — 4 credits remaining. Reserved for warm lead escalations only.
**Daily priority order:** Warm leads → Replies → Apollo Tasks (T2s) → New T1 batch (if capacity)

Active wave T2 schedule:
| Wave | T1 Sent | T2 Due | Contacts |
|------|---------|--------|----------|
| Wave 1 | Mar 10 | **Mar 15** (Day 5) | 23 |
| Wave 2 | Mar 10 | **Mar 15** (Day 5) | 16 |
| Wave 3 | Mar 11 | **Mar 16** (Day 5) | 35 |
| Wave 4 | Mar 11 | **Mar 19** (Day 8) | 37 confirmed sent |

---

## Phase 1: Session Startup + Intel Scan (~5 min)

1. `git pull origin main`
2. Read `memory/session/handoff.md` and `memory/session/work-queue.md` — get current state
3. Open Apollo → TAM Outbound - Rob Gorham → **Tasks tab** — count how many tasks are due today and in the next 2 days
4. Search Gmail MCP for replies to `robert.gorham@testsigma.com` — any new replies since last session
5. Check `memory/warm-leads.md` — any pending follow-ups overdue
6. Check Google Calendar for meetings today
7. Output a 5-line intel summary: tasks due, replies received, warm lead status, what phase to prioritize

---

## Phase 2: Warm Lead & Reply Processing (~10-20 min)

**Skip if zero replies and no warm lead follow-ups overdue.**

### Warm leads (HIGHEST PRIORITY — process before anything else)
- Check `memory/warm-leads.md` for any follow-up dates that have passed
- If overdue: draft follow-up immediately. Present to Rob. Wait for APPROVE SEND.
- A warm lead in limbo is a meeting lost.

### Reply classification
For each new reply to `robert.gorham@testsigma.com`:

| Type | Response |
|------|----------|
| Positive / Curious | Move to warm-leads.md. Draft same-day response. Present for approval. |
| Timing / Not now | Log. Draft a light "noted, I'll circle back" reply. Set 30-day re-engage reminder in work-queue. |
| Referral | Thank referrer same day. Research referred person. Draft outreach mentioning referrer. |
| Hard no | Add to DNC. Log in CLAUDE.md. No response needed. |
| Unsubscribe | Add to DNC. No further contact. |

When a meeting is booked: generate a prep card (Company snapshot, Prospect background, Pain hypothesis, Suggested discovery questions, Relevant proof points, Predicted objections).

---

## Phase 3: Apollo Task Queue — TAM Outbound T2s (~30-90 min)

**This is the core daily operation.** The Apollo task queue controls all follow-up for enrolled contacts. Check it every session.

### Steps
1. Open Apollo → TAM Outbound - Rob Gorham → Tasks tab
2. For each task due today (or overdue):
   a. Identify the contact and their company
   b. Pull their T2 draft from the batch tracker HTML (see T2 source files below)
   c. If no draft exists yet: draft T2 now per Part 7 of `sop-tam-outbound.md`
   d. Present to Rob — wait for **APPROVE SEND**
   e. Send via Apollo UI (Part 23 + Part 25 of `sop-tam-outbound.md`)
   f. After send: update batch tracker status → "T2 Sent [date]"
3. After all due tasks are processed: note any that are coming due in the next 48 hours

### T2 source files by wave
| Wave | T1 Tracker (for proof point reference) | T2 Tracker (build when drafts needed) |
|------|----------------------------------------|---------------------------------------|
| Wave 1 | `wave1-batch1-tracker-mar10.html` | `tamob-wave1-t2-mar15.html` (build by Mar 14) |
| Wave 2 | `tamob-wave2-draft-mar10.html` | `tamob-wave2-t2-mar15.html` (build by Mar 14) |
| Wave 3 | `tamob-batch-20260311-1.html` | `tamob-wave3-t2-mar16.html` (build by Mar 15) |
| Wave 4 | `tamob-batch-20260311-2.html` | `tamob-wave4-t2-mar19.html` (build by Mar 18) |

### T2 formula (from sop-tam-outbound.md Part 7)
- 50-70 words
- Light callback to T1 (1 sentence max — "Circling back on this...")
- New angle or new proof point — NOT a repeat of T1
- Engagement question CTA (NOT "what day works" — save that for T3/breakup)
- No em dashes, no placeholders, no company name misspelling
- **APPROVE SEND required before any sends**

### What to do if Apollo shows 0 tasks
Normal between step cycles (e.g., Day 2-4 between T1 and T2). Check if any waves are approaching their T2 date. If so, pre-build T2 drafts now so they're ready when tasks surface. Move to Phase 4.

---

## Phase 4: New TAM T1 Batch (~90-180 min)

**Only proceed if:** Apollo task queue has fewer than 5 overdue tasks, no T2 due in next 24 hours, and it's not Monday.

This is the new pipeline source. All new T1s come from `tam-accounts-mar26.csv` (312 accounts) or Factor accounts (`memory/target-accounts.md`). No other sourcing is authorized.

### Steps
1. Open `tam-accounts-mar26.csv` — filter for `icp=HIGH`, `status=Untouched`
2. Dedup against `MASTER_SENT_LIST.csv` and DNC list in CLAUDE.md
3. Source 15-20 accounts → research (sop-tam-outbound.md Part 5) → draft T1s (Part 6)
4. QA Gate: word count 75-100, SMYKM subject, real proof point, Testsigma mentioned, "What day works?" CTA
5. Build batch tracker HTML (sop-tam-outbound.md Part 9)
6. Present BATCH SUMMARY to Rob — wait for **APPROVE SEND**
7. Enroll in TAM Outbound via Apollo API (max 5 at a time)
8. Send Step 1 tasks via Apollo UI (Part 23)
9. Log all sends in MASTER_SENT_LIST.csv + update batch tracker

**Daily target:** 25-50 T1 sends when in active new-batch mode.
**Full SOP:** `memory/sop-tam-outbound.md`

---

## Phase 5: Legacy Follow-up (~15 min, situational)

**⛔ InMail SUSPENDED (4 credits remaining as of Mar 6). Only proceed if Rob explicitly authorizes credit spend.**

When credits allow (>10), check work-queue.md for:
- Overdue T2/T3 InMails from legacy batches (Batches 1-11)
- Tyler Referrals T2 (Vernon Bryant — InMail only, Sales Nav thread saved)
- Any warm lead escalation needing InMail

Send via Sales Nav. Log in MASTER_SENT_LIST.csv.

---

## Phase 6: Daily Wrap (~5-10 min)

1. Update `memory/session/session-log.md` — what was sent, what was drafted, any incidents
2. Update `memory/session/handoff.md` — current state, next due dates
3. Update `memory/session/work-queue.md` — mark completed tasks, add new ones
4. `git add -A && git commit -m "Session [N]: [brief description]"`
5. Remind Rob: `git push origin main`
6. Deliver summary to Rob: sends today, tasks due next session, any warm lead flags

---

## Adaptive Logic

| Condition | Adaptation |
|-----------|------------|
| Apollo has 10+ T2s due | Skip Phase 4. All focus on Phase 3. |
| Apollo has 0 tasks due + none in 48hr | Skip Phase 3. Maximize Phase 4 (new T1 batch). |
| 5+ replies received | Extend Phase 2. Defer Phase 4 until replies are processed. |
| Warm lead reply | Drop everything. Process FIRST. |
| Monday | No sends. Research + T2 draft prep only. |
| Thursday/Friday | Maximize send volume. |
| Weekend | Research only. No sends. |
| InMail credits < 5 | Phase 5 SUSPENDED. Apollo email only. |
| Wave T2 due in <48 hr and no drafts built | Build T2 drafts immediately (Phase 3 prep), even if no tasks yet. |

---

## Weekly Targets

| Metric | Weekly Target | Notes |
|--------|--------------|-------|
| TAM Outbound T2 sends | 20-40 | Big wave weeks (Mar 15-19) will be higher |
| TAM Outbound T1 sends | 25-50/day when batching | Continuous pipeline |
| Reply response time | Same day | No reply sits >24 hours |
| Meetings booked | 1-2 | Primary success metric |
| MASTER_SENT_LIST accuracy | 100% | Every send logged same session |

---

## Account Authorization Rules

⛔ **MANDATORY GATE — ALL new prospects must come from authorized lists only.**

| Source | Status |
|--------|--------|
| Factor Accounts (38 accounts) | ✅ Active — `memory/target-accounts.md` |
| TAM Accounts Oct 2025 (312 accounts) | ✅ Active — `/Work/tam-accounts-mar26.csv` |
| Open Sales Nav saved searches | ⛔ SUSPENDED Mar 9, 2026 |
| Re-engagement (Factor/TAM only, >60 days) | ✅ With new trigger event |
| Farming accounts | ❌ Coordinate with AE/CSM first. No cold outreach. |

If a prospect's company is not in Factor or TAM, do NOT include them. No exceptions without Rob's explicit written approval.
