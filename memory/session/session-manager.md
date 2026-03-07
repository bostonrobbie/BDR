# Session Manager

> Detailed startup and closing checklist for every session.
> Read AGENTS.md first, then this file for the full session workflow.
> Last updated: 2026-03-07

---

## Session Startup Checklist

When a new session begins, do ALL of the following:

### 1. Pull and orient
```bash
cd /sessions/<your-session-id>/mnt/Work
git pull origin main
```
Then read in order:
- `AGENTS.md` — collaboration rules
- `CLAUDE.md` — full memory + hard rules
- `memory/session/handoff.md` — current state
- `memory/session/work-queue.md` — available tasks

### 2. Identify session type
Ask Rob what he's working on, or infer from his first message. Session types:

| Type | Trigger | Key Files to Load |
|------|---------|------------------|
| New Batch Build (LinkedIn) | "build a new batch" | sop-outreach.md, sop-send.md, MASTER_SENT_LIST.csv |
| Website Visitor Email Batch | "WV batch", "Apollo visitors" | sop-outreach.md, apollo-config.md, MASTER_SENT_LIST.csv |
| Touch 2/3 Drafts | "follow-up drafts", "touch 2" | sop-outreach.md, incidents.md (cadence), pipeline-state.md |
| Reply Handling | "[Name] replied" | warm-leads.md, sop-outreach.md |
| Daily Ops | "run the daily", "what's next" | sop-daily.md, pipeline-state.md, warm-leads.md |
| Research Only | "research [company/person]" | proof-points.md, data-rules.md |
| Analytics Review | "how are we doing", "what's working" | scoring-feedback.md, data-rules.md |
| Tracker Update | "update the tracker", "log these sends" | pipeline-state.md, MASTER_SENT_LIST.csv |
| Call Prep | "I'm calling...", "prep me for calls" | proof-points.md, warm-leads.md |

### 3. Check current state
- What batch are we on? Check pipeline-state.md.
- Any replies to handle? Check warm-leads.md and Gmail if needed.
- Any touch-ups due today? Check work-queue.md and pipeline-state.md follow-up schedule.
- Credit state: InMail credits (only 4 remaining as of Mar 6). Apollo leads (~6,879).

### 4. Claim your task in work-queue.md (if doing tracked work)

---

## Session Closing Checklist

Before ending ANY session — no exceptions:

- [ ] Update `memory/session/work-queue.md` (mark done, add new tasks)
- [ ] Overwrite `memory/session/handoff.md` with current state
- [ ] Prepend new entry to `memory/session/session-log.md`
- [ ] Update `CLAUDE.md` Pipeline Status if key numbers changed
- [ ] Update `memory/pipeline-state.md` if sends or status changes occurred
- [ ] Commit: `git add -A && git commit -m "Update [DATE]: [summary]"`
- [ ] Push (or tell Rob to push if VM has no credentials)

---

## Session Types — Full Workflows

### Type 1: New Batch Build (LinkedIn InMail)

1. Generate Pre-Brief from previous batch data (see Pre-Brief Template below)
2. Present Pre-Brief to Rob
3. Receive prospect list (from Rob's Sales Navigator export)
4. Preflight check: DNC, MASTER_SENT_LIST dedup, same-company collision
5. For each prospect: research company + person, score ICP fit (1-5), assign A/B group
6. Draft Touch 1 InMail: C1 framework, 70-100 words, one CTA, MQS target >= 9/12
7. QA Gate all messages (7 Hard Constraints from sop-outreach.md)
8. Generate HTML deliverable, save to `batches/`
9. Present to Rob for review — wait for `APPROVE SEND`
10. After approval: update MASTER_SENT_LIST.csv, pipeline-state.md, session log
11. Commit + push

### Type 2: Website Visitor Email Batch

1. Pull WV data from Apollo (or receive from Rob)
2. Qualify/filter: persona match, not already in MASTER_SENT_LIST
3. Research each company (2 sources)
4. Write Touch 1 emails: C2 framework, 75-99 words, one CTA, personalized subject
5. QA Gate all messages
6. Present to Rob — wait for `APPROVE SEND`
7. Enroll contacts in Apollo WV sequence using correct `.com` email account ID
8. Update MASTER_SENT_LIST.csv + pipeline-state.md
9. Commit + push

### Type 3: Touch 2/3 Drafts

1. Check cadence eligibility: Touch 2 = Day 4+, Touch 3 = Day 9+. See incidents.md.
2. Pull names from pipeline-state.md (no-reply list for target batch)
3. Verify no reply received (Gmail check if needed)
4. Draft each touch: reference Touch 1 pain point, different angle, short (40-70 words)
5. MQS score each draft
6. QA Gate
7. Present to Rob — wait for `APPROVE SEND`
8. After approval: update pipeline-state.md send dates
9. Commit + push

### Type 4: Reply Handling

1. Identify reply type: positive / curious / timing / referral / polite decline / hostile
2. Note what triggered the reply (opener, pain hook, proof point, timing)
3. If positive: draft response to book meeting. Update warm-leads.md as Active.
4. If referral: draft outreach to referred person (standard Touch 1 workflow)
5. If polite decline: add to DNC (60+ day re-engage flag), log in CLAUDE.md DNC list
6. If hostile: add to DNC permanently
7. Draft response per sop-outreach.md reply handling
8. Present to Rob — wait for approval before sending
9. Update warm-leads.md, pipeline-state.md, MASTER_SENT_LIST.csv (status column if applicable)

### Type 5: Daily Ops

1. Read sop-daily.md
2. Gmail scan: any new replies? Handle per Type 4.
3. Warm lead check: any warm-leads.md items overdue for follow-up?
4. Credit state: InMail credits? Apollo credits?
5. Touch due check: who is Day 4+ or Day 9+ with no reply?
6. Generate prioritized action list for Rob
7. Rob picks what to execute today

---

## Pre-Brief Template

Generated before every new batch build. Pulls from accumulated batch data.

```
## Pre-Brief: Batch [N] | [Date]

1. Best persona: [which title/level is replying most]
2. Best proof point: [which customer story is in most replied-to messages]
3. Best vertical: [which industry is warmest]
4. Best pattern: [any opener/length/CTA pattern standing out]
5. Stop doing: [one thing to drop based on data]

Data basis: [X] batches, [Y] prospects, [Z] replies tracked.
```

If no batch data available, use defaults from `memory/data-rules.md` and `memory/scoring-feedback.md`.

---

## Quick Reference: Key Numbers

| Metric | Value | Updated |
|--------|-------|---------|
| Total prospects contacted | 206 | 2026-03-07 |
| Emails sent (confirmed) | 49 | 2026-03-07 |
| InMail credits | 4 | 2026-03-06 |
| Apollo lead credits | ~6,879 | 2026-03-06 |
| MASTER_SENT_LIST rows | 278 | 2026-03-07 |
| LI Outbound Q1 enrolled | 316 | 2026-03-07 |
| Current batch number | 11 | 2026-03-07 |

---

## File Quick Reference

| What | Where |
|------|-------|
| Primary memory | `CLAUDE.md` |
| Collaboration rules | `AGENTS.md` |
| Current handoff | `memory/session/handoff.md` |
| Task queue | `memory/session/work-queue.md` |
| Session history | `memory/session/session-log.md` |
| Voice rules + do-nots | `memory/context/voice-rules.md` (if merged) |
| Gold standard messages | `memory/context/gold-standards.md` (if merged) |
| SOP: outreach drafting | `memory/sop-outreach.md` |
| SOP: sending InMails | `memory/sop-send.md` |
| SOP: daily workflow | `memory/sop-daily.md` |
| Pipeline state + send log | `memory/pipeline-state.md` |
| Incident + cadence rules | `memory/incidents.md` |
| Apollo config + sequences | `memory/apollo-config.md` |
| Proof points | `memory/proof-points.md` |
| Warm leads | `memory/warm-leads.md` |
| Data-backed rules | `memory/data-rules.md` |
| Master sent list | `MASTER_SENT_LIST.csv` |
