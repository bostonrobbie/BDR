# Active Session Registry — Protocol

## Purpose
Prevents multiple Cowork sessions from duplicating work, editing the same files, or prospecting the same companies simultaneously. Every running session maintains a live registration file in this directory.

---

## How It Works

### On Session Start
Every session creates a JSON file in this directory named `{session-number}.json`:

```json
{
  "session_id": 28,
  "started_at": "2026-03-12T15:30:00Z",
  "last_heartbeat": "2026-03-12T15:30:00Z",
  "task_id": "TASK-023",
  "task_description": "Send Wave 5 Batch 4 T1 emails",
  "companies_claimed": ["Epicor", "BeyondTrust", "Northern Trust"],
  "files_editing": ["tamob-batch-20260312-4.html", "MASTER_SENT_LIST.csv"],
  "status": "active",
  "agent_type": "cowork",
  "machine": "cowork-instance-1"
}
```

### During Session (Heartbeat)
Update `last_heartbeat` every time a major step completes (file write, API call batch, etc.). This lets other sessions detect stale registrations from crashed sessions.

### On Session End
Delete your registration file. If the session crashes, the file remains (this is intentional for crash detection).

### Before Starting Work
1. List all files in `memory/session/active/`
2. Read each one
3. Check for conflicts:
   - **Company overlap:** If another session has claimed a company you need, STOP and leave a message in `messages.md` asking them to coordinate, or pick a different company.
   - **File overlap:** If another session is editing a file you need, WAIT or work on something else. Check `.locks/` for formal file locks.
   - **Task overlap:** If another session is working the same TASK-ID, STOP. One of you picked it up without claiming it properly.
4. If no conflicts, proceed and register yourself.

---

## Stale Session Detection

A session is considered **stale** (likely crashed) if:
- `last_heartbeat` is more than **2 hours** old AND `status` is still `"active"`

When you detect a stale session:
1. Do NOT delete their registration file.
2. Leave a message in `messages.md`: `"Session {N} appears stale (last heartbeat: {time}). Proceeding with {your task} which may overlap with their claimed work on {companies/files}."`
3. Check `in-progress.md` for crash recovery state.
4. If the stale session's claimed companies/files overlap with yours, tell Rob and let him decide.

---

## Registration File Schema

```json
{
  "session_id": "(integer) — session number from session-log.md",
  "started_at": "(ISO 8601) — when session started",
  "last_heartbeat": "(ISO 8601) — last updated timestamp",
  "task_id": "(string) — TASK-XXX from work-queue.md, or 'ad-hoc' for Rob-directed work",
  "task_description": "(string) — 1-line description of what this session is doing",
  "companies_claimed": ["(array of strings) — company names this session is actively prospecting or drafting for"],
  "files_editing": ["(array of strings) — filenames (not full paths) this session is actively writing to"],
  "status": "(string) — 'active' | 'finishing' | 'crashed'",
  "agent_type": "(string) — 'cowork' | 'claude-code' | 'manual'",
  "machine": "(string) — identifier for which machine/instance this is"
}
```

**Required fields:** session_id, started_at, last_heartbeat, task_id, task_description, status
**Optional fields:** companies_claimed, files_editing, agent_type, machine

---

## Conflict Resolution Rules

1. **First-registered wins.** If two sessions try to claim the same company or file, the one with the earlier `started_at` has priority.
2. **Rob breaks ties.** If both sessions started at roughly the same time, ask Rob in chat.
3. **Read-only is always safe.** Multiple sessions can READ the same files simultaneously. Only WRITES need coordination.
4. **MASTER_SENT_LIST.csv is append-only.** Two sessions can append to it if they are working different contacts, but should use the file lock system for safety.
5. **handoff.md and work-queue.md** should only be written by ONE session at a time (the one finishing its task). Use file locks.

---

## Quick Reference

| Action | How |
|--------|-----|
| Register | Create `memory/session/active/{session-number}.json` |
| Heartbeat | Update `last_heartbeat` field in your JSON file |
| Check for conflicts | `ls memory/session/active/` then read each file |
| Finish | Delete your JSON file |
| Detect crash | Any file with `last_heartbeat` > 2 hours old |
| Claim a company | Add to `companies_claimed` array in your JSON |
| Claim a file | Add to `files_editing` array AND create a `.locks/` entry |
