# Session Start — Parallel-Safe Startup Protocol

## Description
Run this at the beginning of every Cowork session. It handles git pull, reading all context files, checking for crashes, registering as an active session, checking for conflicts with other running sessions, and presenting Rob with current state. This replaces the old sequential startup and adds parallel-session safety.

## Trigger
Run at the START of every new session, before doing any other work.

## Steps

### Phase 1: Sync and Load Context

1. Attempt `git pull origin main` (may fail if no git creds in VM — note and continue)
2. Read these files IN ORDER:
   - `AGENTS.md` (collaboration protocol)
   - `CLAUDE.md` (full BDR SOP, memory, rules, DNC list)
   - `memory/session/handoff.md` (current pipeline state)
   - `memory/session/work-queue.md` (task queue)
   - `memory/session/in-progress.md` (crash checkpoint)
   - `memory/session/messages.md` (inter-session message board)

### Phase 2: Crash Detection

3. Check `memory/session/in-progress.md`:
   - If Status = **ACTIVE**: A previous session crashed mid-task.
     - STOP. Tell Rob: "The last session crashed mid-task. [Task name] was in progress. [N of M] steps completed. Resume from step [N+1], or restart?"
     - Wait for Rob's decision before proceeding.
   - If Status = **CLEAR**: No crash. Proceed normally.

### Phase 3: Active Session Check (Parallel Safety)

4. List all files in `memory/session/active/`:
   ```bash
   ls memory/session/active/*.json 2>/dev/null
   ```
5. For each file found, read it and check:
   - Is `last_heartbeat` less than 2 hours old? If yes, this session is LIVE.
   - What companies are they claiming? What files are they editing? What task are they on?
6. If any live sessions exist:
   - Note which companies and files are claimed
   - DO NOT work on any claimed company or edit any claimed file
   - Tell Rob: "Session {N} is currently active, working on {task} with {companies}. I'll pick something that doesn't conflict."

### Phase 4: Register This Session

7. Determine your session number: check the last entry in `memory/session/session-log.md` and increment by 1.
8. Create `memory/session/active/{session-number}.json`:
   ```json
   {
     "session_id": {N},
     "started_at": "{ISO timestamp}",
     "last_heartbeat": "{ISO timestamp}",
     "task_id": "pending",
     "task_description": "Starting up, awaiting task assignment",
     "companies_claimed": [],
     "files_editing": [],
     "status": "active",
     "agent_type": "cowork",
     "machine": "cowork-instance"
   }
   ```

### Phase 5: Check for Warm Leads and Urgent Items

9. **Run `skills/reply-classifier/SKILL.md`** — this handles the full Gmail check, classifies all replies, updates warm-leads.md, and surfaces priority items. It replaces the manual Gmail search below.

   Manual fallback (if reply-classifier unavailable): Search Gmail MCP:
   ```
   Tool: gmail_search_messages
   q: "to:robert.gorham@testsigma.com is:unread"
   maxResults: 10
   ```
10. Check `memory/warm-leads.md` for any overdue follow-ups.
11. If P0 warm leads found (positive reply or curiosity): tell Rob immediately, run `skills/reply-router/SKILL.md` to draft response, and prioritize above all other tasks.
12. Check `memory/contact-lifecycle.md` for any contacts with T2 due dates today.

### Phase 6: Claim a Task

12. Review `memory/session/work-queue.md` for available tasks (status: UNCLAIMED).
13. Pick the highest-priority unclaimed task that doesn't conflict with other active sessions.
14. Or ask Rob what to work on.
15. Update your active session registration with the claimed task_id and companies_claimed.
16. Update work-queue.md task status to IN_PROGRESS.

### Phase 7: Read Relevant Playbooks and Skills (SELECTIVE — not all)

17. Read ONLY the playbooks/skills mapped to your claimed task. Do NOT read all — this wastes context budget.

   **Playbooks:**
   - TAM T1 batch work → `tam-t1-batch.md` + `apollo-enrollment.md` + `dedup-protocol.md`
   - T2 follow-up drafting → `t2-followup.md` + `qa-gate.md`
   - Apollo sends → `apollo-task-queue-sends.md`
   - Bounce/error recovery → `error-recovery.md`
   - If unsure → read `_index.md` (index only, ~30 lines) then pick

   **New Skills (read instead of or alongside playbooks):**
   - Building a batch → `skills/enrichment-pipeline/SKILL.md` + `skills/compliance-gate/SKILL.md` + `skills/draft-qa/SKILL.md`
   - Handling replies → `skills/reply-router/SKILL.md`
   - Pipeline view → `skills/batch-dashboard/SKILL.md`
   - Account research → `skills/trigger-monitor/SKILL.md`
   - Closing session → `skills/handoff-auto/SKILL.md`
   - Apollo sends → `skills/apollo-send/SKILL.md` (replaces manual send flow — use after APPROVE SEND)
   - Pre-send JSON prep → `skills/batch-json-builder/SKILL.md` (run after APPROVE SEND, before apollo-send)
   - T2/T3 due dates → `skills/stage-monitor/SKILL.md` (or check scheduled output in messages.md)

**Context budget:** By this point you should have read 6-8 files. Add 1-3 playbooks max. Total startup reads should be 7-11 files. If you're reading more, you're loading too much.

### Phase 8: Report to Rob

18. Present current state:
   - What other sessions are running (if any)
   - What task you're claiming
   - Any warm leads or urgent items
   - Any crash recovery needed
   - Any messages from other sessions

---

## Error Handling

- **Git pull fails:** Note the error and continue. Not blocking.
- **Can't read a file:** Note which file is missing and tell Rob. May indicate repo corruption.
- **Stale session detected:** Follow the stale session protocol in `memory/session/active/_protocol.md`.
- **Multiple sessions want same task:** First-registered wins per the active session protocol.
- **Message board has urgent alerts:** Address them before claiming a new task.

---

## Quick Checklist (copy-paste for fast reference)

```
[ ] git pull
[ ] Read AGENTS.md, CLAUDE.md, handoff.md, work-queue.md, in-progress.md, messages.md
[ ] Crash check (in-progress.md Status)
[ ] Active session check (ls memory/session/active/)
[ ] Register in active/ directory
[ ] Run skills/reply-classifier/SKILL.md (full Gmail reply check + warm lead update)
[ ] Check contact-lifecycle.md for T2 due today
[ ] Claim task + update registration
[ ] Read relevant playbooks/skills (see Phase 7)
[ ] Report to Rob
```

---

## Self-Improvement Loop

This skill maintains its own run log and learned-patterns file. Full protocol: `skills/_shared/learning-loop.md`

### Before Each Run
1. Read `skills/session-start/learned-patterns.md` if it exists — apply any documented calibration adjustments
2. Count entries in `skills/session-start/run-log.md` to determine current run number

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
3. Overwrite `skills/session-start/learned-patterns.md` with updated findings
4. If a pattern appears in 4+ of 5 runs: write a `## SKILL UPDATE PROPOSAL — session-start` entry to `memory/session/messages.md` for Rob's review

**Hard rule:** Never modify SKILL.md directly. Only propose updates via messages.md and wait for Rob's explicit approval.
