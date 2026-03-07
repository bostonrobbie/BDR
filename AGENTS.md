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

## Startup Protocol (EVERY session, EVERY agent — no exceptions)

### Step 1 — Pull latest from remote
```bash
cd /sessions/<your-session-id>/mnt/Work
git pull origin main
```

### Step 2 — Read orientation files IN THIS ORDER
1. `AGENTS.md` (this file)
2. `CLAUDE.md` — Rob's full memory, preferences, all hard rules
3. `memory/session/handoff.md` — what the last agent left, what's in progress RIGHT NOW
4. `memory/session/work-queue.md` — available tasks, what's claimed

### Step 3 — Claim your task before starting
Before starting ANY work item in work-queue.md:
- Find the task
- Change its status to `IN_PROGRESS`
- Add your agent identifier and a timestamp
- Commit immediately: `git add memory/session/work-queue.md && git commit -m "chore: claim [task-id]" && git push origin main`

This prevents two agents from doing the same work simultaneously.

### Step 4 — Load task-specific memory
See the Reference Files table in `CLAUDE.md` for which memory files to read per task type.

---

## End-of-Session Protocol (EVERY session, EVERY agent — no exceptions)

### Step 1 — Update work-queue.md
- Mark your task(s) `DONE` with a brief completion note
- Add any newly discovered tasks as `PENDING`

### Step 2 — Overwrite handoff.md with current state
Replace the Current State section with what you know right now:
- What you did this session
- What's in progress or partially complete
- Top 3 priorities for the next agent
- Any blockers, flags, or anomalies

### Step 3 — Prepend a new entry to session-log.md
```
## [DATE] — [AGENT-ID] — [SESSION TITLE]
**Completed:** [what was done]
**Changed files:** [list]
**Key decisions:** [any important calls made]
**Pending:** [what's left]
```

### Step 4 — Update CLAUDE.md pipeline stats if numbers changed
Key stats to keep current: total prospects contacted, emails sent, InMail credits, CSV row count.

### Step 5 — Commit and push
```bash
git add -A
git commit -m "Update [DATE]: [brief summary]"
git push origin main
```
If push fails (no GitHub credentials in VM): tell Rob to run `git push origin main` from his terminal. The commit is made locally — do not re-commit.

---

## Conflict Prevention Rules

1. **Always pull before working.** Never start on a stale copy.
2. **Always claim tasks before working.** If a task is `IN_PROGRESS` with another agent's claim, skip it.
3. **MASTER_SENT_LIST.csv: append only.** Never delete or modify existing rows.
4. **pipeline-state.md and CLAUDE.md are high-collision files.** Pull, edit, commit, push as fast as possible.
5. **Never overwrite tracker files.** Always read first, then append or update.
6. **Merge conflicts: stop and tell Rob.** Never force-resolve without human review.

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
If git push fails (HTTPS credentials not available in VM): commit is already made locally. Tell Rob to run `git push origin main` from his own terminal.

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
| `memory/session/work-queue.md` | Any agent. Claim before starting, mark done when finished. |
| `memory/incidents.md` | Any agent. **Append only.** |
| `memory/warm-leads.md` | Any agent. Update status, don't delete rows. |
| `batches/` | Any agent. Add new files. Don't edit existing batch files. |
| `logs/` | Any agent. Append only. |

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
| Task queue | `memory/session/work-queue.md` |
| Session startup/closing checklist | `memory/session/session-manager.md` |
| Agent role split + command contract | `memory/codex-cowork-operating-protocol.md` |
| Pipeline state + send log | `memory/pipeline-state.md` |
| Draft safety + incidents | `memory/incidents.md` |
| SOPs | `memory/sop-*.md` |
