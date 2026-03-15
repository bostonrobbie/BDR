# AGENTS.md — Multi-Agent Collaboration Protocol (v2.0)
## Rob Gorham BDR Second Brain — Testsigma

---

## Purpose

This file defines how multiple Claude agents (Cowork sessions, Claude Code, etc.) collaborate on Rob's BDR workflow simultaneously. Every new session reads this file first, then follows the startup sequence below.

**Version 2.0 changes (Mar 12, 2026):** Added parallel session safety (active session registry, file locking, message board), playbook knowledge system, and Cowork skill files.

---

## Cold Start Protocol (for new sessions with zero context)

**Use this FIRST if you're a brand-new Claude session that has never seen this repo before.** It's a fast 5-step checklist to understand what's happening without reading every file.

1. **Read CLAUDE.md** (2 min) — identity, rules, preferences, DNC list, tool stack. Everything needed to understand "who is Rob and what are his hard rules?"
2. **Read memory/session/handoff.md** (first 50 lines) — current pipeline state snapshot. What was happening in the last session? What batches are active? What's the T2 window?
3. **Read memory/session/in-progress.md** — crash check. If `Status: ACTIVE`, a prior session crashed mid-task. STOP and tell Rob: "Last session was working on [task]. Status is ACTIVE. Should I resume from step [N] or restart?"
4. **Read memory/session/messages.md** (last 5-10 messages only) — inter-session alerts. Other sessions may have left `[WARN]` or `[CONFLICT]` flags. Look for `WARN`, `CONFLICT`, or `ASK` tags.
5. **Read memory/session/work-queue.md** (CRITICAL and ⚡ UNCLAIMED tasks only) — what's pending? What can you claim?

**Then: You have enough context to tell Rob the current state and ask what to work on.**

You do NOT need to read every playbook, SOP, or skill file at startup. Load them on-demand as you claim a task. This keeps your context window clean and saves 30 minutes of reading.

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

**⚠️ REGISTRATION IS NON-NEGOTIABLE.** Session 30 audit found concurrent sessions operating without registration, causing untracked parallel writes to MASTER_SENT_LIST.csv and messages.md ordering issues. Registration MUST happen before any work begins.

**On start (STEP 10 — do not skip):**
1. Determine your session number: check session-log.md for the last session number and increment by 1
2. Create `memory/session/active/{session-number}.json` with:
   ```json
   {
     "session_number": N,
     "started_at": "ISO timestamp",
     "last_heartbeat": "ISO timestamp",
     "status": "active",
     "task": "description of what you're working on",
     "claimed_companies": ["Company1", "Company2"],
     "files_editing": ["MASTER_SENT_LIST.csv", "tamob-batch-*.html"],
     "agent_type": "cowork"
   }
   ```
3. If you cannot determine a session number, use the current Unix timestamp as a temporary ID

**During work:** Update `last_heartbeat` whenever you complete a major step (file write, API call batch, etc.).

**On finish:** Set status to "completed", add a `notes` field with summary. Do NOT delete the file until you've completed the full handoff protocol (Steps 1-9 below). Then delete.

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

**Message Board Rules (from Session 30 audit):**

1. **Timestamp must be CURRENT time when writing**, not when you started the task. Use `date -u +%Y-%m-%dT%H:%M:%SZ` to get the exact current time right before appending.
2. **New messages go at the TOP** of the Messages section (right below the `## Messages` divider). Read the first existing message and insert ABOVE it.
3. **Accuracy requirement for DONE/CLAIM messages:**
   - State exact number of MASTER_SENT_LIST rows added (not enrolled count)
   - State the current total row count of MASTER_SENT_LIST.csv (run `wc -l` right before writing)
   - State exact companies and contact count
   - If using enrollment overrides (finished_in_other, active_in_other, job_change), list which contacts needed them
4. **One message per major action.** Don't combine unrelated work into one message. If you did Batch 6 and Batch 7, write TWO messages.
5. **Never edit existing messages.** If you made an error, append a `[CORRECTION]` message referencing the wrong one.

---

## Crash Recovery Protocol

### What it is
`in-progress.md` is a live checkpoint file. Written at task START, updated after each sub-step. If a session crashes, the next session reads this file and can resume exactly where the last one left off.

### On crash detection (Status = ACTIVE)

1. **STOP IMMEDIATELY.** Do not start a new task. Do not proceed on the task listed in in-progress.md.

2. **Tell Rob with exact context.** Copy-paste this template and fill in the bracketed fields:
   ```
   The last session crashed or hung mid-task. Here's the state:

   Task: [copy Task Name from in-progress.md]
   Task ID: [TASK-###]
   Progress: [N] of [M] steps completed
   Last completed step: [copy last checked step]
   Last checkpoint: [copy "Resume Instructions" field]

   What was actually completed (verification):
   - Files created: [list files that exist on disk — run 'ls' to verify]
   - Rows added to MASTER_SENT_LIST: [run 'wc -l MASTER_SENT_LIST.csv' and compare to prior count in messages.md]
   - API enrollments: [check latest messages.md CLAIM/DONE entry for exact count]

   What was NOT completed:
   - [copy steps that are NOT checked off]

   I can resume from step [N+1], or we can restart fresh. Your call?
   ```

3. **Wait for Rob's explicit decision:** "Resume from step [N]" or "Start fresh" — do not guess.

4. **If resuming:**
   - Verify the files listed in "Files in progress" actually exist on disk: `ls -la [filename]`
   - If a file is missing, tell Rob and ask if you should recreate it or skip
   - Start at the next unchecked step. Do not redo completed steps.
   - Update your active session registration with the task and mark heartbeat

5. **If restarting:**
   - Set in-progress.md Status to CLEAR
   - Commit the change: `git add memory/session/in-progress.md && git commit -m "Crash recovery: restarting [TASK-###]"`
   - Claim the task fresh, starting from Step 1

6. **Never trust completion without verification.** Even if in-progress.md says "Step 5 completed," verify the output files exist and have the expected row counts.

### On task START
Before starting any task involving file creation or multiple API calls:
1. Open `in-progress.md` and set Status to ACTIVE
2. Fill in: Task ID, task name, step list, files to be created, target row counts
3. Commit immediately with message `Checkpoint: [TASK-XXX] — starting task`

### During a task (mid-session checkpoints)
After completing each sub-step:
1. Check off the step in `in-progress.md`: `- [x] Step N: [description]`
2. Update "Resume instructions" to point to the next step
3. If a file was created/modified, log the new row count or file size
4. Commit immediately: `Checkpoint: [TASK-XXX] — [Step N] complete`

### On task completion
1. Set `in-progress.md` Status to CLEAR
2. Update handoff.md + work-queue.md (see Handoff Protocol section below)
3. Commit: `Session [date]: [1-line summary]`

---

## State Verification Commands (Quick Health Check)

Use these one-liners to verify current system state without reading every file. Run these at session startup to understand what's been done and what's pending:

```bash
# How many contacts have been sent to total?
wc -l /sessions/funny-nifty-dirac/mnt/Work/MASTER_SENT_LIST.csv

# What batch trackers are currently active?
ls -lht /sessions/funny-nifty-dirac/mnt/Work/batches/active/ | grep "tamob-batch" | head -5

# How many T2 draft files are staged for approval?
ls /sessions/funny-nifty-dirac/mnt/Work/batches/t2-pending/ 2>/dev/null | wc -l

# What's the last session number and status?
tail -5 /sessions/funny-nifty-dirac/mnt/Work/memory/session/session-log.md

# Is there a crash recovery checkpoint?
grep "^## Status:" /sessions/funny-nifty-dirac/mnt/Work/memory/session/in-progress.md

# Any stale or active sessions running?
ls -la /sessions/funny-nifty-dirac/mnt/Work/memory/session/active/

# Recent inter-session messages (last 5)?
head -10 /sessions/funny-nifty-dirac/mnt/Work/memory/session/messages.md | grep "\[" | head -5

# How many contacts are in each active batch (sampler)?
for f in /sessions/funny-nifty-dirac/mnt/Work/batches/active/tamob-batch-*.html; do echo "$f: $(grep -c '<tr data-contact' "$f" 2>/dev/null || echo '?') contacts"; done
```

**Use these to:**
- Verify nothing is hanging mid-task (no stale active sessions > 2 hours old)
- See how many contacts have been sent to total
- Check if T2 drafts are pending approval
- Understand the current batch workload before claiming a task

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

At the END of every session, BEFORE stopping, Claude MUST complete ALL 9 steps. **No exceptions. No "I'll let the next session handle it."** Session 30 audit found handoff.md 4+ sessions stale because sessions skipped Step 2.

1. Clear `in-progress.md` Status to CLEAR (if a task was completed)
2. **Update `memory/session/handoff.md`** with current pipeline state — add a FULL section for any batch/wave work done this session (contact table, Apollo IDs, status, T2 due dates). Update the `Last Updated` header. **If you enrolled contacts, the handoff MUST include them.**
3. Update `memory/session/work-queue.md` — mark completed tasks DONE, add new ones
4. Append a session entry to `memory/session/session-log.md` (with contact table if applicable)
5. Set your active session registration to `status: "completed"`, then delete the file
6. Release all file locks in `.locks/`
7. Leave a `[DONE]` message in `memory/session/messages.md` summarizing your work (see Message Board Rules below for format)
8. Commit all changes: `git add -A && git commit -m "Session [date]: [1-line summary]"`
9. Remind Rob to `git push` from his terminal (Claude cannot push due to auth)

**Self-check before finishing:** Can the NEXT session read handoff.md and know exactly what you did without reading messages.md or session-log.md? If no, your handoff is incomplete. Go back to Step 2.

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

## What Lives Where — Quick Reference

New sessions: use this to locate critical files without reading CLAUDE.md folder structure section:

| What You Need | Where to Find It |
|---------------|------------------|
| **Current pipeline state** | `memory/session/handoff.md` (first 50 lines) — last 2-3 batches, T2 windows, critical issues |
| **Tasks to claim** | `memory/session/work-queue.md` — sorted by priority (CRITICAL, ⚡, 🔴, 🟡, 🟢) |
| **Crash recovery checkpoint** | `memory/session/in-progress.md` — if Status = ACTIVE, read crash recovery section above |
| **Active batch trackers** | `batches/active/` — HTML files show contact details, send status, T2 due dates |
| **T2 drafts awaiting approval** | `batches/t2-pending/` — hold until Rob says APPROVE SEND |
| **All contacts sent to (history)** | `MASTER_SENT_LIST.csv` (597 rows) — dedup check, batch lookup, contact status |
| **DNC list** | `CLAUDE.md` → "Do Not Contact List" table (8 people) |
| **Target accounts** | `tam-accounts-mar26.csv` — 312 TAM + 38 Factor accounts |
| **Completed batches** | `batches/archive/` (if exists) or `archive/old-outreach-html/` |
| **System health report** | `diagnostics/system-health-report.md` — weekly auto-generated, skill health + call analytics |
| **All playbooks** | `memory/playbooks/` — read only the playbook(s) mapped to your claimed task (see Playbook System table above) |
| **All skills** | `skills/` — repeatable workflows; for session startup use `skills/session-start/SKILL.md` |

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

### MASTER_SENT_LIST.csv Batch Name Standard

The `batch` column in MASTER_SENT_LIST.csv MUST use the full standard format. **Session 30 audit found 5 non-standard batch names (B6, B7, W6B1, W5B-S29) that are untraceable without external context.** Full standard documented in `playbooks/dedup-protocol.md`.

| Sequence | Format | Example |
|----------|--------|---------|
| TAM Outbound T1 | `TAM Outbound Batch {N} Mar{DD}` | `TAM Outbound Batch 7 Mar12` |
| TAM Outbound T2 | `TAM Outbound Batch {N} T2 Mar{DD}` | `TAM Outbound Batch 7 T2 Mar16` |
| Website Visitor | `WV Email Batch Mar{DD}` | `WV Email Batch Mar3` |
| Buyer Intent | `Buyer Intent Email T{N}` | `Buyer Intent Email T2` |
| Other | `{Descriptive Name} T{touch} Mar{DD}` | `Tyler Referrals T1 Mar10` |

**NEVER** use short forms like B7, W6B1, or W5B-S29.

---

## Git Status

- Remote: `https://github.com/bostonrobbie/bdr-work.git`
- Branch: `main`
- Claude cannot push (no GitHub auth in VM). Rob must `git push` from his terminal.
- Multiple unpushed commits may accumulate. This is normal.

---

*Last updated: 2026-03-12 (Session 30 — v2.1: Audit-driven fixes: mandatory session registration with JSON template, handoff.md enforcement with self-check, messages.md accuracy rules with timestamp/count verification, MASTER_SENT_LIST batch naming standard, legacy duplicate documentation)*
