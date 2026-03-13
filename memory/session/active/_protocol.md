# Active Session Registry — Protocol
*Version: 1.1 — 2026-03-13 (aligned stale threshold to 45 min; added contacts_claimed; added awaiting_decision status)*

## Purpose
Prevents multiple Cowork sessions from duplicating work, editing the same files, or prospecting the same contacts simultaneously. Every running session maintains a live registration file in this directory.

---

## How It Works

### On Session Start
Every session creates a JSON file in this directory named `{session-number}.json`:

```json
{
  "session_id": 32,
  "started_at": "2026-03-13T14:00:00Z",
  "last_heartbeat": "2026-03-13T14:00:00Z",
  "task_id": "TASK-023",
  "task_description": "Send Wave 5 Batch 4 T1 emails",
  "contacts_claimed": [
    { "name": "Jason Lieberman", "company": "Epicor", "exclusive_until": "2026-03-13T16:00:00Z" },
    { "name": "Holly Shubaly", "company": "BeyondTrust", "exclusive_until": "2026-03-13T16:00:00Z" }
  ],
  "files_editing": ["tamob-batch-20260312-4.html", "MASTER_SENT_LIST.csv"],
  "status": "active",
  "awaiting_decision": null,
  "agent_type": "cowork",
  "machine": "cowork-instance-1"
}
```

### During Session (Heartbeat)
Update `last_heartbeat` every time a major step completes (file write, API call batch, etc.). This lets other sessions detect stale registrations from crashed sessions.

### When Blocked on Rob's Decision
If you're waiting for Rob (APPROVE SEND, warm lead priority, ownership conflict), update your status to `awaiting_decision` AND update `memory/session/rob-availability.json`:

```json
{
  "status": "awaiting_decision",
  "awaiting_decision": {
    "type": "warm_lead_priority",
    "context": "Seth Drummond @ Northern Trust replied positively — prioritize response or continue T1 batch?",
    "options": ["prioritize_warm_lead", "continue_batch"],
    "waiting_since": "2026-03-13T14:22:00Z"
  }
}
```

**Do NOT sit idle while waiting.** If Rob's decision isn't needed to start a different task, switch to a non-blocking task (T2 drafting, compliance gate checks, tracker updates) and note this in messages.md with `[IN_FLIGHT]`.

### On Session End
Delete your registration file. If the session crashes, the file remains (this is intentional for crash detection).

### Before Starting Work
1. List all files in `memory/session/active/`
2. Read each one
3. Check for conflicts:
   - **Contact overlap:** If another session has claimed a contact you need (check `contacts_claimed`), pick a different contact. Multiple contacts at the SAME company are fine as long as they're different people.
   - **File overlap:** If another session is editing a file you need, WAIT or work on something else. Check `.locks/` for formal file locks.
   - **Task overlap:** If another session is working the same TASK-ID, STOP. One of you picked it up without claiming it properly.
4. Check `memory/session/rob-availability.json` — if Rob is `busy`, pick a task that doesn't need immediate approval.
5. If no conflicts, proceed and register yourself.

---

## Stale Session Detection

A session is considered **stale** (likely crashed) if:
- `last_heartbeat` is more than **45 minutes** old AND `status` is still `"active"` or `"awaiting_decision"`

*Rationale: Aligned with `.locks/_protocol.md` stale lock threshold (also 45 min). Prior mismatch (60 min sessions vs. 30 min locks) caused asymmetric coordination — locks expired but contact claims stayed blocked for another 15 min. Now both use 45 min.*

When you detect a stale session:
1. Do NOT delete their registration file.
2. Leave a message in `messages.md`: `[WARN] Session {N} appears stale (last heartbeat: {time}). Proceeding with {your task} — may overlap with their claimed contacts: {list}.`
3. Check `in-progress.md` for crash recovery state.
4. If the stale session's claimed contacts/files overlap with yours, tell Rob and let him decide.

---

## Registration File Schema

```json
{
  "session_id": "(integer) — from memory/session/.last-session-number, incremented by 1",
  "started_at": "(ISO 8601) — when session started",
  "last_heartbeat": "(ISO 8601) — last updated timestamp",
  "task_id": "(string) — TASK-XXX from work-queue.md, or 'ad-hoc' for Rob-directed work",
  "task_description": "(string) — 1-line description of what this session is doing",
  "contacts_claimed": [
    {
      "name": "(string) — contact full name",
      "company": "(string) — company name",
      "exclusive_until": "(ISO 8601 or null) — null if work complete; timestamp if still in draft/enroll phase"
    }
  ],
  "files_editing": ["(array of strings) — filenames (not full paths) this session is actively writing to"],
  "status": "(string) — 'active' | 'finishing' | 'crashed' | 'awaiting_decision'",
  "awaiting_decision": {
    "type": "(string or null) — 'warm_lead_priority' | 'approve_send' | 'ownership_conflict'",
    "context": "(string) — 1-2 sentence description of what Rob needs to decide",
    "options": ["(array of strings) — choices for Rob"],
    "waiting_since": "(ISO 8601 or null)"
  },
  "agent_type": "(string) — 'cowork' | 'claude-code' | 'manual'",
  "machine": "(string) — identifier for which machine/instance this is"
}
```

**Required fields:** session_id, started_at, last_heartbeat, task_id, task_description, status
**Optional fields:** contacts_claimed, files_editing, agent_type, machine, awaiting_decision

---

## Conflict Resolution Rules

1. **Contact-level claims (not company-level).** Multiple sessions CAN work on different contacts at the same company simultaneously. Only block if the exact same person (name + company) is in another session's `contacts_claimed` with a future `exclusive_until`.
2. **First-registered wins for same contact.** If two sessions try to claim the exact same contact, the one with the earlier `started_at` has priority.
3. **Rob breaks ties.** If both sessions started at roughly the same time, ask Rob in chat.
4. **Read-only is always safe.** Multiple sessions can READ the same files simultaneously. Only WRITES need coordination.
5. **MASTER_SENT_LIST.csv is append-only.** Two sessions can append to it if they are working different contacts, but should use the file lock system for safety.
6. **handoff.md and work-queue.md** should only be written by ONE session at a time (the one finishing its task). Use file locks.
7. **Parallelization is encouraged.** T1 building + T2 drafting for old batches can run simultaneously. See `memory/session/active-batch-work.json` for parallel batch work coordination.

---

## Quick Reference

| Action | How |
|--------|-----|
| Register | Create `memory/session/active/{session-number}.json` |
| Get session number | Read `memory/session/.last-session-number`, increment by 1, update the file |
| Heartbeat | Update `last_heartbeat` field in your JSON file |
| Check for conflicts | `ls memory/session/active/` then read each file |
| Check Rob's availability | Read `memory/session/rob-availability.json` |
| Finish | Delete your JSON file |
| Detect crash | Any file with `last_heartbeat` > **45 minutes** old |
| Claim a contact | Add to `contacts_claimed` array with `exclusive_until` timestamp |
| Claim a file | Add to `files_editing` array AND create a `.locks/` entry |
| Block on Rob decision | Set status to `awaiting_decision` + update rob-availability.json + post [IN_FLIGHT] to messages.md |
