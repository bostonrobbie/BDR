# AGENTS.md — Multi-Agent Collaboration Protocol (v2.0)
## Rob Gorham BDR Second Brain — Testsigma

---

## Purpose

This file defines how multiple Claude agents (Cowork sessions, Claude Code, etc.) collaborate on Rob's BDR workflow simultaneously. Every new session reads this file first, then follows the startup sequence below.

**Version 2.0 changes (Mar 12, 2026):** Added parallel session safety (active session registry, file locking, message board), playbook knowledge system, and Cowork skill files.

---

## Agent Startup Sequence (MANDATORY — every session)

```
STEP 1:  git pull origin main           (may fail if no creds — note and continue)
STEP 2:  Read AGENTS.md                 (this file — the collaboration protocol)
STEP 3:  Read CLAUDE.md                 (full BDR SOP, memory, rules, DNC list)
STEP 4:  Read memory/session/handoff.md (current pipeline state)
STEP 5:  Read memory/session/work-queue.md (task queue with priorities)
STEP 6:  Read memory/session/in-progress.md (crash checkpoint)
STEP 7:  Read memory/session/messages.md (inter-session message board)
STEP 8:  Crash check — if in-progress.md Status = ACTIVE → crash recovery (see below)
STEP 9:  Parallel check — ls memory/session/active/ → read each .json file
         If other sessions are active, note their claimed companies/files/tasks
STEP 10: Register yourself in memory/session/active/{session-number}.json
STEP 11: Check Gmail MCP for replies to robert.gorham@testsigma.com (warm leads jump queue)
STEP 12: Claim a task (avoid conflicts with active sessions) OR ask Rob what to work on
STEP 13: Read ONLY the playbooks mapped to your claimed task (see Playbook System table below — do NOT read all playbooks)
STEP 14: Report current state to Rob
```

For the full detailed startup skill with error handling, see: `skills/session-start/SKILL.md`

---

## Infrastructure Overview

| System | Location | Purpose |
|--------|----------|---------|
| Active Session Registry | `memory/session/active/*.json` | Tracks which sessions are running and what they're working on |
| File Locking | `.locks/*.lock` | Prevents two sessions from writing to the same file simultaneously |
| Message Board | `memory/session/messages.md` | Append-only communication between concurrent sessions |
| Crash Recovery | `memory/session/in-progress.md` | Checkpoint file for mid-task crash recovery |
| Playbooks | `memory/playbooks/*.md` | Captured knowledge from all sessions — read before starting tasks |
| Skills | `skills/*/SKILL.md` | Repeatable workflow definitions for Cowork invocation |
| Handoff State | `memory/session/handoff.md` | Pipeline state snapshot updated at end of every session |
| Task Queue | `memory/session/work-queue.md` | Prioritized task list with claiming protocol |
| Session Log | `memory/session/session-log.md` | Chronological record of what every session did |

---

## Session Files

| File | Purpose | When to Update |
|------|---------|---------------|
| `AGENTS.md` | This protocol file | When protocol changes |
| `CLAUDE.md` | Full BDR SOP, memory, rules | After major decisions or DNC changes |
| `memory/session/handoff.md` | Pipeline state snapshot | END of every session |
| `memory/session/work-queue.md` | Task queue with priorities | When claiming/completing/adding tasks |
| `memory/session/session-log.md` | Chronological session log | END of every session (append only) |
| `memory/session/in-progress.md` | Crash-recovery checkpoint | START and DURING tasks |
| `memory/session/messages.md` | Inter-session messages | Whenever you need to communicate with other sessions |
| `memory/session/active/*.json` | Active session registration | START and END of session, heartbeat during |

---

## Parallel Session Protocol

### Active Session Registry

Every running session maintains a registration file in `memory/session/active/`. Full protocol: `memory/session/active/_protocol.md`.

**On start:** Create `memory/session/active/{session-number}.json` with your session ID, task, claimed companies, and files being edited.

**During work:** Update `last_heartbeat` whenever you complete a major step (file write, API call batch, etc.).

**On finish:** Delete your registration file and release all file locks.

**Conflict detection:** Before claiming any company or file, check all active registrations for overlap. First-registered wins. If conflict exists, pick different work or ask Rob.

**Stale detection:** If another session's `last_heartbeat` is more than 2 hours old and status is still "active", it likely crashed. Follow the stale session protocol in `_protocol.md`.

### File Locking

Before writing to any shared file, create a lock in `.locks/`. Full protocol: `.locks/_protocol.md`.

**Files that REQUIRE locking before writes:**
- `MASTER_SENT_LIST.csv`
- `memory/session/handoff.md`
- `memory/session/work-queue.md`
- `memory/session/session-log.md`
- `memory/session/in-progress.md`
- `memory/pipeline-state.md`
- `memory/incidents.md`
- `memory/session/messages.md`
- Any `tamob-*.html` tracker file

**Lock lifecycle:** Check for existing lock → Acquire lock → Write file → Release lock. Stale locks (>30 min) can be overridden.

**Multiple files:** Lock ALL needed files before starting writes. Release ALL after writes complete. This prevents deadlocks.

### Message Board

`memory/session/messages.md` is an append-only communication channel. Full format documented in the file itself.

**Use it for:**
- `[CLAIM]` — Announcing which companies/contacts you're working on
- `[DONE]` — Announcing completed work
- `[WARN]` — Flagging issues other sessions should know about
- `[CONFLICT]` — Reporting a conflict that needs Rob's resolution
- `[ASK]` — Asking other sessions for coordination
- `[INFO]` — General information sharing

**Check on startup.** Always read messages.md during startup (Step 7). Other sessions may have left alerts.

---

## Crash Recovery Protocol

### What it is
`in-progress.md` is a live checkpoint file. Written at task START, updated after each sub-step. If a session crashes, the next session reads this file and can resume exactly where the last one left off.

### On crash detection (Status = ACTIVE)
1. STOP. Do not start a new task.
2. Tell Rob: "The last session crashed mid-task. [Task name] was in progress. [N of M] steps completed. Last checkpoint: [description]. Resume from step [N+1], or restart?"
3. Wait for Rob's decision.
4. If resuming: Start at the step marked `next`. Verify files listed in "Files in progress" actually exist on disk before trusting their contents.
5. If restarting: Set in-progress.md Status to CLEAR, commit, then claim the task fresh.
6. Never redo completed steps — check files exist first; if they do, trust the checkpoint.

### On task START
Before starting any task involving file creation or multiple API calls:
1. Open `in-progress.md` and set Status to ACTIVE
2. Fill in: Task ID, task name, step list, files to be created
3. Commit immediately

### During a task (mid-session checkpoints)
After completing each sub-step:
1. Check off the step in `in-progress.md`
2. Update "Resume instructions" to point to the next step
3. Commit

### On task completion
1. Set `in-progress.md` Status to CLEAR
2. Update handoff.md + work-queue.md
3. Commit

---

## Mid-Session Commit Protocol (MANDATORY)

These events each require an immediate git commit — do not wait until session end:

| Event | Commit message format |
|-------|----------------------|
| in-progress.md written (task start) | `Checkpoint: [TASK-XXX] — starting task` |
| Any new file created in /Work/ | `Checkpoint: [TASK-XXX] — [filename] created` |
| Every 5 contacts drafted in a batch | `Checkpoint: [TASK-XXX] — [N/M] contacts drafted` |
| MASTER_SENT_LIST.csv updated | `Checkpoint: [TASK-XXX] — MASTER_SENT_LIST +[N] rows` |
| Any memory/ file updated mid-task | `Checkpoint: [TASK-XXX] — [filename] updated` |
| Task completed (session end) | `Session [date]: [1-line summary]` |

Sessions can crash at any time. Committing after each deliverable ensures the next session can pick up from a real on-disk state.

---

## Task Claiming

When claiming a task from work-queue.md:
1. Check `memory/session/active/` for other sessions on the same task — abort if claimed
2. Update the task status to `IN_PROGRESS` with session number and timestamp
3. Update your active session registration with the task_id
4. Only claim ONE task at a time unless Rob asks for parallel work
5. Update status to `DONE` when complete
6. Write `in-progress.md` BEFORE starting any file-creation or API work

---

## Task Sizing & Context Budget

Sessions have limited context windows. Hitting the limit causes compaction (loss of earlier context), which leads to repeated work and mistakes. Follow these rules to stay within budget.

**Task sizing guidelines:**

| Task Type | Target Size | Max Tool Calls | When to Checkpoint & Hand Off |
|-----------|-------------|----------------|-------------------------------|
| T1 batch (source + draft + enroll) | 8-12 contacts | ~60 | After enrollment. Don't add T2 drafts in same session. |
| T2 batch (draft only) | 15-20 contacts | ~40 | After QA gate pass. |
| Apollo sends (Tasks tab) | 15-20 sends | ~30 | After all sends confirmed. |
| Bounce cleanup / incident | 1 incident | ~25 | After MASTER_SENT_LIST + incidents.md updated. |
| Infrastructure / SOP work | 1 focused change | ~40 | After verification step. |

**Context budget rules:**

1. **Read selectively at startup.** Don't read every file. Read AGENTS.md + CLAUDE.md (auto-loaded) + handoff.md + work-queue.md + in-progress.md + messages.md. Then ONLY read the playbooks mapped to your claimed task (see Playbook System below).
2. **Never read a file you don't need.** If your task is bounce cleanup, don't read tam-t1-batch.md or qa-gate.md.
3. **If you've made 50+ tool calls, start wrapping up.** Checkpoint your progress, update handoff files, and hand off remaining work as a new task.
4. **If context gets compacted, don't re-read everything.** Trust in-progress.md for crash recovery. Read only the files needed to continue the current step.
5. **One task per session.** Don't chain tasks (e.g., "build batch then also do T2 drafts"). Complete one, hand off, let the next session pick up the other.
6. **Batch HTML trackers are large.** When reading trackers, read only the sections you need (use offset/limit). Don't read 500-line HTML files in full unless necessary.

---

## Handoff Protocol

At the END of every session, BEFORE stopping, Claude MUST:

1. Clear `in-progress.md` Status to CLEAR (if a task was completed)
2. Update `memory/session/handoff.md` with current pipeline state (FULL section, not just header)
3. Update `memory/session/work-queue.md` — mark completed tasks DONE, add new ones
4. Append a session entry to `memory/session/session-log.md` (with contact table if applicable)
5. Delete your active session registration: `memory/session/active/{session-number}.json`
6. Release all file locks in `.locks/`
7. Leave a `[DONE]` message in `memory/session/messages.md` summarizing your work
8. Commit all changes: `git add -A && git commit -m "Session [date]: [1-line summary]"`
9. Remind Rob to `git push` from his terminal (Claude cannot push due to auth)

Full handoff playbook: `memory/playbooks/session-handoff.md`

---

## Playbook System

All captured knowledge from production work lives in `memory/playbooks/`. Index: `memory/playbooks/_index.md`.

**Rule: Read the relevant playbook BEFORE starting a task.** Don't rediscover known gotchas.

| Task Type | Playbooks to Read |
|-----------|-------------------|
| New T1 batch | `tam-t1-batch.md`, `apollo-enrollment.md`, `dedup-protocol.md`, `qa-gate.md`, `batch-tracker-html.md` |
| T2 follow-ups | `t2-followup.md`, `qa-gate.md` |
| Apollo sends | `apollo-task-queue-sends.md` |
| Sales Nav sourcing | `sales-nav-deep-sweep.md` |
| Error handling | `error-recovery.md` |
| Session close | `session-handoff.md` |
| Catchall emails | `catchall-domains.md` |

**Contributing to playbooks:** If you discover a new gotcha, edge case, or process improvement during your session, UPDATE the relevant playbook. This is how we build institutional knowledge.

---

## Cowork Skills

Repeatable workflow definitions live in `skills/*/SKILL.md`. These are more structured than playbooks and designed to be invoked as complete workflows.

| Skill | Location | Use When |
|-------|----------|----------|
| Session Start | `skills/session-start/SKILL.md` | Every session startup |
| TAM T1 Batch | `skills/tam-t1-batch/SKILL.md` | Building new outreach batches |
| Apollo Enroll | `skills/apollo-enroll/SKILL.md` | Creating contacts + enrolling in sequences |

---

## Hard Rules (inherited from CLAUDE.md)

- Never send any message without Rob's explicit APPROVE SEND
- Never use personal Gmail (rgorham369@gmail.com) for work
- Always use Blue/Work Chrome profile for browser automation
- Never modify existing company data without explicit approval
- Draft everything, Rob reviews, Rob executes
- Never take any action visible to Rob's coworkers (no Slack, no internal emails unless asked)
- TAM-ONLY: Only prospect from TAM (312) + Factor (38) accounts

---

## File Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| TAM batch trackers | `tamob-batch-{YYYYMMDD}-{N}.html` | `tamob-batch-20260312-4.html` |
| Legacy batch trackers | `outreach-sent-{date}-batch{N}.html` | `outreach-sent-feb26-batch3.html` |
| T2 draft files | `tamob-wave{N}-t2-drafts-{date}.html` | `tamob-wave1-t2-drafts-mar12.html` |
| SOP documents | `memory/sop-{topic}.md` | `memory/sop-tam-outbound.md` |
| Playbooks | `memory/playbooks/{topic}.md` | `memory/playbooks/apollo-enrollment.md` |
| Skills | `skills/{skill-name}/SKILL.md` | `skills/tam-t1-batch/SKILL.md` |
| Active sessions | `memory/session/active/{N}.json` | `memory/session/active/28.json` |
| File locks | `.locks/{filename}.lock` | `.locks/MASTER_SENT_LIST.csv.lock` |
| Session files | `memory/session/{name}.md` | `memory/session/handoff.md` |

---

## Git Status

- Remote: `https://github.com/bostonrobbie/bdr-work.git`
- Branch: `main`
- Claude cannot push (no GitHub auth in VM). Rob must `git push` from his terminal.
- Multiple unpushed commits may accumulate. This is normal.

---

*Last updated: 2026-03-12 (Session 28 — v2.0: Parallel session protocol, file locking, message board, playbook system, Cowork skills)*
