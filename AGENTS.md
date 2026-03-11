# AGENTS.md — Multi-Agent Collaboration Protocol
## Rob Gorham BDR Second Brain — Testsigma

---

## Purpose

This file defines how Claude agents collaborate on Rob's BDR workflow across sessions.
Every new session reads this file first, then CLAUDE.md, then the session files below.

---

## Agent Startup Sequence (MANDATORY — every session)

```
STEP 1: git pull origin main   (may fail if no creds — note and continue)
STEP 2: Read AGENTS.md         (this file)
STEP 3: Read CLAUDE.md         (full BDR SOP and memory)
STEP 4: Read memory/session/handoff.md     (current pipeline state)
STEP 5: Read memory/session/work-queue.md  (task queue)
STEP 6: Read memory/session/in-progress.md (crash check — see below)
STEP 7: Crash check: if in-progress.md Status = ACTIVE → crash recovery mode (see below)
         If Status = CLEAR → proceed normally
STEP 8: Claim a task OR ask Rob what to work on
STEP 9: Report current state to Rob
```

---

## Session Files

| File | Purpose | Updated by |
|------|---------|------------|
| `AGENTS.md` | This protocol file | Rob or Claude when protocol changes |
| `CLAUDE.md` | Full BDR SOP, memory, rules | Rob or Claude after major decisions |
| `memory/session/handoff.md` | Current pipeline state snapshot | Claude at END of every session |
| `memory/session/work-queue.md` | Task queue with priorities | Claude at END of every session |
| `memory/session/session-log.md` | Running log of what each session did | Claude — append only |
| `memory/session/in-progress.md` | **Crash-recovery checkpoint** | Claude — START and DURING tasks |

---

## Crash Recovery Protocol

### What it is
`in-progress.md` is a live checkpoint file that tracks mid-task progress. It gets written at the START of every major task and updated after each sub-step. If a session crashes unexpectedly, the next session reads this file and can resume exactly where the last one left off.

### On crash detection (Status = ACTIVE)
1. **Stop.** Do not start a new task.
2. Tell Rob: *"The last session crashed mid-task. [Task name] was in progress. [N of M] steps were completed. Last checkpoint: [description]. Resume from step [N+1], or restart?"*
3. Wait for Rob's decision.
4. **If resuming:** Start at the step marked `← NEXT`. Verify files listed in "Files in progress" actually exist on disk before trusting their contents.
5. **If restarting:** Set in-progress.md Status → CLEAR, commit, then claim the task fresh from work-queue.md.
6. **Never redo completed steps** — check files exist first; if they do, trust the checkpoint.

### On task START (Claude writes this)
Before starting any task that involves creating files or making multiple API calls:
1. Open `in-progress.md` and replace its content with the ACTIVE template (see in-progress.md)
2. Fill in: Task ID, task name, step list, files to be created
3. Commit immediately: `git add -A && git commit -m "Checkpoint: [TASK-XXX] — starting task"`

### During a task (mid-session checkpoints)
After completing each sub-step:
1. Check off the step in `in-progress.md` with a ✅ and the commit hash
2. Update "Files in progress" to show current file state
3. Update "Resume instructions" to point to the next step
4. Commit: `git add -A && git commit -m "Checkpoint: [TASK-XXX] — [step name] (step N/M)"`

### On task completion (normal)
1. Set `in-progress.md` Status → **CLEAR**
2. Update handoff.md + work-queue.md (mark task DONE)
3. Commit: `git add -A && git commit -m "Session [date]: [1-line summary]"`

---

## Mid-Session Commit Protocol (MANDATORY)

The following events each require an **immediate git commit** — do not wait until session end:

| Event | Commit message format |
|-------|----------------------|
| in-progress.md written (task start) | `Checkpoint: [TASK-XXX] — starting task` |
| Any new file created in /Work/ | `Checkpoint: [TASK-XXX] — [filename] created` |
| Every 5 contacts drafted in a batch | `Checkpoint: [TASK-XXX] — [N/M] contacts drafted` |
| MASTER_SENT_LIST.csv updated | `Checkpoint: [TASK-XXX] — MASTER_SENT_LIST +[N] rows` |
| Any memory/ file updated mid-task | `Checkpoint: [TASK-XXX] — [filename] updated` |
| Task completed (session end) | `Session [date]: [1-line summary]` |

**Why:** Sessions can crash at any time. Committing after each deliverable ensures the next session can pick up from a real on-disk state, not a lost in-memory one.

---

## Handoff Protocol

At the END of every session, before stopping, Claude MUST:

1. Set `memory/session/in-progress.md` Status → **CLEAR** (if a task was completed this session)
2. Update `memory/session/handoff.md` with current pipeline state
3. Update `memory/session/work-queue.md` — mark completed tasks, add new ones
4. Append a session entry to `memory/session/session-log.md`
5. Commit all changes: `git add -A && git commit -m "Session [date]: [1-line summary]"`
6. Remind Rob to `git push` from his terminal (Claude cannot push due to auth)

---

## Task Claiming

When claiming a task from work-queue.md:
- Update the task status to `IN_PROGRESS` with the session timestamp
- Only claim ONE task at a time unless Rob asks for parallel work
- Update status to `DONE` when complete
- Write `in-progress.md` BEFORE starting any file-creation or API work

---

## Hard Rules (inherited from CLAUDE.md)

- Never send any message without Rob's explicit APPROVE SEND
- Never use personal Gmail (rgorham369@gmail.com) for work
- Always use Blue/Work Chrome profile for browser automation
- Never modify existing company data without explicit approval
- Draft everything → Rob reviews → Rob executes

---

## File Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Batch trackers | `outreach-sent-[date]-batch[N].html` | `outreach-sent-feb26-batch3.html` |
| SOP documents | `[topic]-sop-[version].md` | `tier1-intent-sop-master.md` |
| Draft files | `[touch]_drafts_[batch].md` | `touch2_drafts_feb27.md` |
| Research | `company-research-[name].md` | `company-research-overdrive.md` |
| Cycle logs | `cycle-logs/[date]-[session].md` | `cycle-logs/2026-03-07-morning.md` |
| Session files | `memory/session/[name].md` | `memory/session/handoff.md` |

---

*Last updated: 2026-03-11 (Session 15 — Added crash-recovery / in-progress checkpoint system)*
