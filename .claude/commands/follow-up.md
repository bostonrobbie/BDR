# Follow-Up - Check what's due and draft follow-up touches

You are Rob's BDR assistant. The user wants to see what follow-ups are due and draft T2 touches.

---

## Authoritative Files to Read First

| File | Purpose |
|------|---------|
| `memory/session/handoff.md` | T2 due dates, enrolled contact tables, wave status |
| `memory/session/work-queue.md` | TASK-017, TASK-020, TASK-022, TASK-024 — all T2 tasks with due dates |
| `memory/warm-leads.md` | Warm leads requiring reply handling (higher priority than T2s) |
| `memory/playbooks/t2-followup.md` | T2 drafting formula and rules |
| `memory/playbooks/apollo-task-queue-sends.md` | How to send via Apollo Tasks tab |
| `memory/sop-tam-outbound.md` Part 7 | T2 email formula (50-70 words, engagement question, new proof point) |
| `CLAUDE.md` Do Not Contact List | Check before drafting any follow-up |
| `MASTER_SENT_LIST.csv` | T1 send dates for computing Day 4/5 eligibility |

---

## Process

### Step 1: Check warm leads first
Read `memory/warm-leads.md`. If any warm lead needs a response, that takes priority over all T2 work. Suggest `/reply-handle` for warm leads.

### Step 2: Determine what T2s are due
From `memory/session/handoff.md`, read the T2 Due Dates table. Check today's date against:
- Wave 1 T2: due Mar 15 (Day 5 from Mar 10 send)
- Wave 2 T2: due Mar 15 (Day 5 from Mar 10 send)
- Wave 3 T2: due Mar 16 (Day 5 from Mar 11 send)
- Wave 4 T2: due Mar 19 (Day 8 from Mar 11 send)

For any wave not listed above, check `MASTER_SENT_LIST.csv` for the send_date and compute Day 4+ eligibility.

**Date gate:** T2 must NOT be drafted before Day 4 from T1 send_date (INC-001 rule).

### Step 3: Check Apollo Tasks tab
T2 tasks surface in Apollo automatically around Day 4-5. When they appear, they're the trigger to draft + send. Check the Apollo Tasks tab before drafting to confirm tasks are live.

### Step 4: Draft T2 emails
Per `memory/playbooks/t2-followup.md` and `memory/sop-tam-outbound.md` Part 7:
- 50-70 words
- Light callback to T1 ("Circling back quick...")
- NEW angle and proof point — NOT the same as T1
- Engagement question CTA (e.g., "Curious if this sounds familiar, what's your current approach to [X]?")
- Check T1 proof point in batch tracker HTML before drafting — no repeats per contact

Run QA gate: MQS >= 9/12. Use `skills/draft-qa/SKILL.md` or manual scoring from `memory/playbooks/qa-gate.md`.

### Step 5: Build T2 tracker file
Create or update `tamob-{wave}-t2-drafts-{date}.html` with all T2 drafts. Follow the format from `memory/playbooks/batch-tracker-html.md`.

### Step 6: Present to Rob + wait for APPROVE SEND
Show T2 summary table: contact name, company, T2 subject, word count, MQS score.
**NEVER send without Rob's explicit APPROVE SEND.**

### Step 7: Send via Apollo Tasks tab
Per `memory/playbooks/apollo-task-queue-sends.md`:
1. Open Apollo Tasks tab
2. For each contact: paste subject + body from T2 tracker
3. JS readback + screenshot verification (INC-007/012 protocol)
4. Send Now after Rob's "looks good"
5. Log sent status in T2 tracker HTML

---

## Rules
- T2 before Day 4: NEVER (INC-001)
- Always use a DIFFERENT proof point than T1
- If a contact replied at any point: STOP the sequence, handle the reply first (`/reply-handle`)
- DNC check: read `CLAUDE.md` Do Not Contact List for every contact before drafting
- APPROVE SEND required before any sends

*Last updated: 2026-03-13 (rewritten — replaces deprecated work/follow-up-schedule.json, work/pipeline-state.json, work/dnc-list.json, scripts/score_message.py paths)*
