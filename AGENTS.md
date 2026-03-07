# AGENTS.md — Multi-Agent Collaboration Guide

**Last updated:** 2026-03-07
**Owner:** Rob Gorham
**Repo:** https://github.com/bostonrobbie/BDR.git (branch: `main`)

---

## What This Is

This repo is Rob Gorham's BDR second brain for his role at Testsigma. Multiple Claude agents running on different machines collaborate on this repo. This file is the single source of truth for how agents coordinate, avoid conflicts, and stay in sync.

Read this file at the start of EVERY session before doing anything else.

---

## The Agent Setup

| Agent | Machine | Primary Focus |
|-------|---------|--------------|
| Cowork-1 | Rob's main PC | Primary daily ops: email, Apollo, Gmail, Calendar, pipeline tracking |
| Cowork-2 | PC2 | Batch building, prospecting, drafting, enrichment |
| Cowork-3 | PC3 | Research, analytics, repo maintenance |

All agents have the same permissions. Role split is by task, not by capability. Any agent can do any task as long as it's not claimed by another.

---

## Coordination Layer (JSON + Scripts)

Agents coordinate via three machine-readable files in `memory/session/`. Git is the message bus — agents pull to receive state, push to broadcast it.

### Key Files

| File | Purpose | Write Rule |
|------|---------|-----------|
| `memory/session/work-queue.json` | Authoritative task queue with atomic claiming | Read before every session. Claim before starting any task. |
| `memory/session/agent-registry.json` | Who is active, on which machine, doing what | Written by session scripts automatically. |
| `memory/session/event-log.jsonl` | Append-only log of every agent action | Never overwrite — append lines only. Zero merge conflicts. |
| `memory/session/handoff.md` | Human-readable state snapshot | Overwrite at end of session (not human-edited mid-session). |
| `memory/session/session-log.md` | Human-readable session history | Prepend only — never delete history. |
| `memory/session/work-queue.md` | Human-readable task companion to work-queue.json | Keep in sync with JSON file. |

### Three Scripts (use these — don't do it by hand)

```
scripts/session_start.py   — Run at start of every session
scripts/claim_task.py      — Claim a specific task atomically
scripts/session_end.py     — Run at end of every session
```

---

## Startup Protocol — ONE COMMAND

```bash
python3 scripts/session_start.py --agent Cowork-1
```

This single command does everything:
1. `git pull origin main` — get latest state from all agents
2. Detect + expire stale task claims (>4h with no activity)
3. Show agent registry — who was last active, what they were doing
4. Show last 10 events from event-log.jsonl
5. Display prioritized pending task list
6. Register this agent as active in agent-registry.json
7. Optionally claim a task

**To claim a task at startup:**
```bash
python3 scripts/session_start.py --agent Cowork-1 --claim TASK-002
```

**After running session_start.py, read these files:**
1. `CLAUDE.md` — all hard rules, pipeline state, ICP, preferences
2. `memory/session/handoff.md` — what the last agent left right now
3. Task-specific memory file(s) per the Reference Files table in `CLAUDE.md`

---

## Claiming a Task — ONE COMMAND

**Never start a task without claiming it first.** Claiming is atomic: pull → check → write → commit → push. First push wins.

```bash
python3 scripts/claim_task.py --agent Cowork-1 --task TASK-002
```

What it does:
1. `git pull` — get the very latest state
2. Check if the task is already claimed
3. Write claim (`status=in_progress`, `claimed_by`, `claimed_at`)
4. Commit + push immediately — minimal race window
5. If push is rejected, another agent claimed first — it will say so

**If a claim is stale (>4h with no commit activity):**
```bash
python3 scripts/claim_task.py --agent Cowork-1 --task TASK-002 --force
```
Only use `--force` if you've confirmed the other agent is not actually running.

**Manual claim (fallback only):**
If the script isn't available, do it by hand:
1. Edit `work-queue.json`: set `status=in_progress`, `claimed_by`, `claimed_at`
2. `git add memory/session/work-queue.json`
3. `git commit -m "chore: claim TASK-XXX by Cowork-N"`
4. `git push origin main` — immediately, before starting work

---

## End-of-Session Protocol — ONE COMMAND

```bash
python3 scripts/session_end.py \
    --agent Cowork-1 \
    --task TASK-002 \
    --status done \
    --summary "Brief description of what was accomplished." \
    --files "path/to/file1.html,path/to/file2.csv"
```

This single command does everything:
1. Updates `work-queue.json` — marks task done/partial/blocked
2. Appends event to `event-log.jsonl`
3. Updates `agent-registry.json` — sets status=idle
4. Prepends entry to `session-log.md`
5. Prints a copy-paste template for `handoff.md`
6. `git add + commit`
7. Attempts push (prompts Rob's terminal if VM has no credentials)

**Status options:**
- `--status done` — task complete, moves to `completed[]`
- `--status partial` — task unfinished, resets to `pending` for next agent
- `--status blocked` — task has a blocker, stays in `active[]` with blocker note

**To add a newly discovered task:**
```bash
python3 scripts/session_end.py \
    --agent Cowork-1 \
    --task TASK-002 \
    --status done \
    --summary "..." \
    --new-task "TASK-009|New task title|HIGH|2026-03-11|Description here."
```

**After running session_end.py:**
1. Update `memory/session/handoff.md` using the printed template
2. Update `CLAUDE.md` pipeline stats if numbers changed (emails sent, credits, CSV rows)
3. Run `git push origin main` from your terminal if the VM push failed

---

## Conflict Prevention Rules

1. **Always pull before working.** Never start on a stale copy. The scripts do this automatically.
2. **Always claim tasks before working.** If `status=in_progress` with another agent's claim, skip it.
3. **MASTER_SENT_LIST.csv: append only.** Never delete or modify existing rows.
4. **pipeline-state.md and CLAUDE.md are high-collision files.** Pull, edit, commit, push as fast as possible.
5. **event-log.jsonl: append only.** Never edit existing lines — only add new ones.
6. **Stale claims (>4h) are auto-expired** by `session_start.py`. If you see a task reset from `in_progress` to `pending`, a previous agent left it without closing the session.
7. **Merge conflicts: stop and tell Rob.** Never force-resolve without human review.

---

## Hard Rules (same as CLAUDE.md, repeated here as a safety net)

- **NEVER send any outreach without Rob's explicit `APPROVE SEND`.**
- **NEVER use rgorham369@gmail.com for work.** Always `robert.gorham@testsigma.com`.
- **NEVER take coworker-visible actions** — no Slack, no internal emails unless Rob explicitly asks.
- **NEVER modify or delete existing records** without explicit per-item approval from Rob.
- **NEVER enroll Apollo contacts** without confirming send identity is `.com` account `68e3b53ceaaf74001d36c206`.
- **Always DNC-check** before drafting. See `CLAUDE.md` Do Not Contact List.
- **Always dedup** against `MASTER_SENT_LIST.csv` before any batch build.
- **Touch 2 not before Day 4. Touch 3 not before Day 9.** See `memory/incidents.md`.

---

## Git Workflow

```
main  ← all agents work here for ops tasks
  └── use feature branches only for structural/experimental repo changes
```

### Commit message format
```
[Type] [DATE]: [brief summary]
```
- `Update` — ops, tracking, pipeline changes
- `feat:` — new files, new systems
- `fix:` — corrections to existing data
- `chore:` — task claims, admin

### Push failures
If git push fails (HTTPS credentials not available in VM): the commit is already made locally. Tell Rob to run `git push origin main` from his own terminal. Do not re-commit.

---

## File Ownership Map

| File | Write Rules |
|------|------------|
| `CLAUDE.md` | Any agent. High-collision — pull before editing, push immediately after. |
| `AGENTS.md` | Any agent. Update `Last updated` date when editing. |
| `MASTER_SENT_LIST.csv` | Any agent. **Append only. Never delete rows.** |
| `memory/pipeline-state.md` | Any agent. High-collision — pull before editing. |
| `memory/session/handoff.md` | Active agent overwrites at end of session. |
| `memory/session/session-log.md` | Any agent. **Prepend new entries — never delete history.** |
| `memory/session/work-queue.json` | Managed by scripts. Manual edits only if scripts unavailable. |
| `memory/session/work-queue.md` | Any agent. Keep in sync with work-queue.json. |
| `memory/session/agent-registry.json` | Managed by scripts. Do not edit manually. |
| `memory/session/event-log.jsonl` | **Append only. Never edit existing lines.** |
| `memory/incidents.md` | Any agent. **Append only.** |
| `memory/warm-leads.md` | Any agent. Update status, don't delete rows. |
| `batches/` | Any agent. Add new files. Don't edit existing batch files. |

---

## Escalation Conditions

Stop work and surface to Rob immediately if:
- A DNC contact appears in a pending draft or task queue
- A duplicate send risk is detected (contact already in MASTER_SENT_LIST)
- A cadence rule would be violated
- You find a merge conflict in any file
- Any proposed action would modify or delete existing records
- You're unsure whether something has already been sent

---

## Related Files

| Purpose | File |
|---------|------|
| Full memory + all hard rules | `CLAUDE.md` |
| Current state handoff | `memory/session/handoff.md` |
| Session history log | `memory/session/session-log.md` |
| Task queue (machine-readable) | `memory/session/work-queue.json` |
| Task queue (human-readable) | `memory/session/work-queue.md` |
| Agent status registry | `memory/session/agent-registry.json` |
| Agent action log | `memory/session/event-log.jsonl` |
| Session startup/closing checklist | `memory/session/session-manager.md` |
| Pipeline state + send log | `memory/pipeline-state.md` |
| Draft safety + incidents | `memory/incidents.md` |
| SOPs | `memory/sop-*.md` |
