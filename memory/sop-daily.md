# "Run the Daily" — Automated Daily Outreach Workflow
## Version 3.0 — Updated Mar 12, 2026 (T1 prospecting is the #1 daily priority. Maximize new contacts every session. T2s handled after new batch work is done, or batched at end of session.)

Trigger phrases: "run the daily", "daily run", "morning run", "start outreach", "run outreach"

---

## Operating Directive (as of Mar 12, 2026)

**The goal right now is maximum pipeline volume. Send as many T1s as possible every day.**

New TAM T1 batch work is the top daily priority — not T2s, not follow-up processing. Apollo's task queue handles the follow-up cadence automatically. What it cannot do is source and research new contacts. That requires human+Claude effort every day. Do that first.

T2s still get done — just after new T1 work is complete, or in whatever time remains.

**Primary channel:** TAM Outbound email via Apollo (`69afff8dc8897c0019b78c7e`)
**Daily T1 target:** 25-50 new contacts enrolled and sent
**LinkedIn InMail:** ⛔ Suspended — 4 credits remaining. Warm lead escalations only.

Active wave T2 schedule (handle after T1 work):
| Wave | T1 Sent | T2 Due | Contacts |
|------|---------|--------|----------|
| Wave 1 | Mar 10 | Mar 15 | 23 |
| Wave 2 | Mar 10 | Mar 15 | 16 |
| Wave 3 | Mar 11 | Mar 16 | 35 |
| Wave 4 | Mar 11 | Mar 19 | 37 |

---

## Phase 1: Session Startup (~5 min)

1. `git pull origin main`
2. Read `memory/session/handoff.md` + `memory/session/work-queue.md`
3. Search Gmail MCP for replies to `robert.gorham@testsigma.com` — flag any warm leads immediately
4. Check `memory/warm-leads.md` for overdue follow-ups
5. Quick Apollo Tasks tab check — note how many T2s are due (do NOT process yet — that's Phase 4)
6. Output: one-line summary of today's priority (e.g., "0 warm leads, 3 T2s due, clear for new batch")

---

## Phase 2: Warm Lead & Reply Processing (~10-20 min)

**Only skip if zero replies AND no warm lead follow-ups overdue.** Warm leads always jump the queue.

### Warm leads (PROCESS BEFORE ANYTHING ELSE)
Check `memory/warm-leads.md` for any follow-up dates that have passed. If overdue: draft response, present to Rob, wait for APPROVE SEND. A warm lead sitting cold is a meeting lost.

### Reply classification
| Reply type | Action |
|-----------|--------|
| Positive / Curious | Move to warm-leads.md. Draft same-day response. |
| Timing / Not now | Log. Draft light "noted, I'll circle back" reply. Set 30-day re-engage reminder in work-queue. |
| Referral | Thank referrer same day. Research referred person. Draft outreach mentioning referrer. |
| Hard no / Unsubscribe | Add to DNC. Log in CLAUDE.md. No response needed. |

When a meeting is booked: auto-generate prep card (Company snapshot, Prospect background, Pain hypothesis, Discovery questions, Proof points, Predicted objections).

---

## Phase 3: New TAM T1 Batch — TOP DAILY PRIORITY (~90-180 min)

**Do this before T2s. Every day. No exceptions except Monday (research only, no sends).**

This is where pipeline gets built. Apollo's task queue will handle T2/T3 follow-up on cadence — but it cannot source and research new contacts. That only happens here.

### Steps
1. Open `tam-accounts-mar26.csv` — filter `icp=HIGH`, `status=Untouched`, sort by employee count desc
2. Dedup against `MASTER_SENT_LIST.csv` + DNC list in CLAUDE.md
3. Source until you have ~50 clean contacts (see sop-tam-outbound.md Part 20 for full sourcing protocol)
4. Research accounts + contacts (Part 5 of sop-tam-outbound.md)
5. Draft T1 emails (Part 6) — SMYKM subject, 75-100 words, real proof point, "What day works?" CTA
6. QA Gate: run full MQS check — min 9/12
7. Build batch tracker HTML (Part 9)
8. Present BATCH SUMMARY to Rob — wait for **APPROVE SEND**
9. Enroll in TAM Outbound via API (max 5 at a time, Part 11)
10. Send Step 1 via Apollo UI (Part 23)
11. Log all sends in MASTER_SENT_LIST.csv + update batch tracker

**Full protocol:** `memory/sop-tam-outbound.md` — read it before starting if anything is unclear.

### When to skip Phase 3
- Monday only (no sends on Mondays — use the time for research + pre-building the next batch)
- Rob explicitly directs otherwise

### ICP=HIGH exhausted?
If `tam-accounts-mar26.csv` has no remaining ICP=HIGH Untouched accounts, move to ICP=Medium. Same process, same protocol.

---

## Phase 4: Apollo Task Queue — TAM Outbound T2s (~30-60 min, after Phase 3)

**Handle after T1 batch work is done, or in remaining session time.**

T2s matter — but Apollo surfaces them on a fixed cadence and they don't expire the same day. A T1 batch built today means 50 more people in the funnel. A T2 sent today means one follow-up that was already scheduled. Do the T1 work first.

### Steps
1. Open Apollo → TAM Outbound - Rob Gorham → Tasks tab
2. For each task due today:
   a. Identify contact, pull T2 draft from batch tracker HTML
   b. If no draft exists: draft T2 per Part 7 of sop-tam-outbound.md (50-70 words, new angle, engagement question CTA)
   c. Present to Rob — wait for **APPROVE SEND**
   d. Send via Apollo UI (Part 23 + Part 25 of sop-tam-outbound.md)
   e. Update batch tracker status → "T2 Sent [date]"
3. If T2 volume exceeds available time: send oldest wave first, log remainder as "T2 pending" in handoff.md

### T2 source files by wave
| Wave | T1 Tracker (proof point reference) | T2 Tracker (build before due date) |
|------|-------------------------------------|-------------------------------------|
| Wave 1 | `wave1-batch1-tracker-mar10.html` | `tamob-wave1-t2-mar15.html` |
| Wave 2 | `tamob-wave2-draft-mar10.html` | `tamob-wave2-t2-mar15.html` |
| Wave 3 | `tamob-batch-20260311-1.html` | `tamob-wave3-t2-mar16.html` |
| Wave 4 | `tamob-batch-20260311-2.html` | `tamob-wave4-t2-mar19.html` |

**T2 formula:** 50-70 words. Light callback to T1 (1 sentence). New angle + new proof point. Engagement question close (NOT "what day works" — save that for breakup). No em dashes. Full protocol: sop-tam-outbound.md Part 7.

---

## Phase 5: Legacy Follow-up (~15 min, situational)

**⛔ InMail SUSPENDED — 4 credits remaining. Do not spend without Rob's explicit go-ahead.**

When credits allow (>10): check work-queue for overdue T2/T3 InMails from legacy batches. Send via Sales Nav. Log in MASTER_SENT_LIST.csv.

---

## Phase 6: Daily Wrap (~5-10 min)

1. Update `memory/session/session-log.md` — sends, drafts, incidents
2. Update `memory/session/handoff.md` — current state, next due dates
3. Update `memory/session/work-queue.md` — mark completed tasks, add new ones
4. `git add -A && git commit -m "Session [N]: [brief description]"`
5. Remind Rob: `git push origin main`
6. Deliver summary to Rob: T1s sent today, T2s due next session, warm lead flags

---

## Adaptive Logic

| Condition | Adaptation |
|-----------|------------|
| Warm lead reply received | Process FIRST. Before Phase 3. Drop everything. |
| Monday | No sends. Research + pre-build next batch. |
| Phase 3 runs long (> 3 hrs) | Defer Phase 4 to next session. Log T2s pending in handoff.md. |
| T2 wave due tomorrow with zero drafts | Build T2 drafts in Phase 4 today even if tasks haven't surfaced yet. |
| ICP=HIGH fully exhausted | Shift to ICP=Medium in Phase 3. Same process. |
| Apollo has 20+ T2s overdue | Do T2s first in Phase 3 position, then new T1 batch after. |
| Thursday | Maximize send volume — go for full 50 T1 target. |
| InMail credits < 5 | Phase 5 suspended. Apollo email only. |

**The only situation that pushes T2s above new T1 work:** 20+ T2s overdue simultaneously. That won't happen under normal cadence. Under normal conditions, T1 always comes first.

---

## Weekly Targets

| Metric | Weekly Target | Notes |
|--------|--------------|-------|
| TAM Outbound T1 sends | 100-250 | 25-50/day × 4-5 send days |
| TAM Outbound T2 sends | 20-40 | Handled after T1 work each session |
| Reply response time | Same day | No warm lead sits >24 hours |
| Meetings booked | 1-2 | Primary success metric |
| MASTER_SENT_LIST accuracy | 100% | Every send logged same session |

---

## Account Authorization Rules

⛔ **MANDATORY — All new prospects must come from authorized lists only.**

| Source | Status |
|--------|--------|
| Factor Accounts (38 accounts) | ✅ Active — `memory/target-accounts.md` |
| TAM Accounts Oct 2025 (312 accounts) | ✅ Active — `/Work/tam-accounts-mar26.csv` |
| Open Sales Nav saved searches | ⛔ Suspended Mar 9, 2026 |
| Re-engagement (Factor/TAM only, >60 days, new trigger) | ✅ Active |
| Farming accounts | ❌ Coordinate with AE/CSM. No cold outreach. |

If a prospect's company is not in Factor or TAM, do NOT include them. No exceptions without Rob's explicit written approval in the session.
