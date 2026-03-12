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

9. Search Gmail MCP for replies to robert.gorham@testsigma.com (warm leads jump the queue):
   ```
   Tool: gmail_search_messages
   q: "to:robert.gorham@testsigma.com is:unread"
   maxResults: 10
   ```
10. Check `memory/warm-leads.md` for any overdue follow-ups.
11. If warm leads found: tell Rob immediately and prioritize response.

### Phase 6: Claim a Task

12. Review `memory/session/work-queue.md` for available tasks (status: UNCLAIMED).
13. Pick the highest-priority unclaimed task that doesn't conflict with other active sessions.
14. Or ask Rob what to work on.
15. Update your active session registration with the claimed task_id and companies_claimed.
16. Update work-queue.md task status to IN_PROGRESS.

### Phase 7: Read Relevant Playbooks (SELECTIVE — not all)

17. Read ONLY the playbooks mapped to your claimed task. Do NOT read all playbooks — this wastes context budget.
   - TAM T1 batch work → `tam-t1-batch.md` + `apollo-enrollment.md` + `dedup-protocol.md`
   - T2 follow-up drafting → `t2-followup.md` + `qa-gate.md`
   - Apollo sends → `apollo-task-queue-sends.md`
   - Bounce/error recovery → `error-recovery.md`
   - If unsure which playbooks apply → read `_index.md` (index only, ~30 lines) then pick

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
[ ] Gmail warm lead check
[ ] Claim task + update registration
[ ] Read relevant playbooks
[ ] Report to Rob
```
