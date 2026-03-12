# File Locking Protocol

## Purpose
Prevents two sessions from writing to the same file at the same time, which would cause one session's changes to be silently overwritten by the other.

---

## How It Works

### To Lock a File
Before writing to any shared file, create a lock file at `.locks/{filename}.lock`:

```json
{
  "locked_by_session": 28,
  "locked_at": "2026-03-12T15:35:00Z",
  "file_path": "MASTER_SENT_LIST.csv",
  "reason": "Appending 9 new contact rows for Wave 5 Batch 4",
  "expected_duration_minutes": 5
}
```

### To Check a Lock
Before writing to ANY file in the list below, check if `.locks/{filename}.lock` exists:
- If it exists and `locked_at` is less than 30 minutes old: **WAIT.** Do not write to this file.
- If it exists and `locked_at` is more than 30 minutes old: The lock is **stale** (session probably crashed). You may delete it and create your own lock, but first leave a note in `messages.md`.
- If it does not exist: **Proceed.** Create your lock, do your write, then release.

### To Release a Lock
After finishing your write, DELETE the lock file. Do this immediately after the write completes, not at session end.

---

## Files That REQUIRE Locking

These shared files are written by multiple sessions and MUST be locked before writing:

| File | Lock file name | Why |
|------|---------------|-----|
| `MASTER_SENT_LIST.csv` | `MASTER_SENT_LIST.csv.lock` | Central dedup database, append-only but still needs coordination |
| `memory/session/handoff.md` | `handoff.md.lock` | Pipeline state, written at session end |
| `memory/session/work-queue.md` | `work-queue.md.lock` | Task queue, written when claiming/completing tasks |
| `memory/session/session-log.md` | `session-log.md.lock` | Append-only log, but simultaneous appends can corrupt |
| `memory/session/in-progress.md` | `in-progress.md.lock` | Crash recovery checkpoint |
| `memory/pipeline-state.md` | `pipeline-state.md.lock` | Full pipeline tracking |
| `memory/incidents.md` | `incidents.md.lock` | Incident log |
| `memory/session/messages.md` | `messages.md.lock` | Message board (short locks only for append) |
| Any `tamob-*.html` tracker | `{filename}.lock` | Batch trackers with status badges |

## Files That Do NOT Need Locking

These are safe for concurrent access:

| File | Why |
|------|-----|
| `CLAUDE.md` | Rarely written, only by Rob or after major decisions |
| `AGENTS.md` | Protocol file, only updated when protocol changes |
| All `memory/playbooks/*.md` | Reference docs, read-only during normal work |
| All `memory/sop-*.md` | SOPs, rarely updated mid-session |
| `memory/target-accounts.md` | Reference data, updated infrequently |
| `memory/session/active/*.json` | Each session owns its own file, no conflicts |

---

## Lock File Schema

```json
{
  "locked_by_session": "(integer) — session number holding the lock",
  "locked_at": "(ISO 8601) — when lock was acquired",
  "file_path": "(string) — the file being locked (relative to repo root)",
  "reason": "(string) — what write operation requires the lock",
  "expected_duration_minutes": "(integer) — estimated time to hold the lock"
}
```

---

## Stale Lock Handling

A lock is considered **stale** if `locked_at` is more than **30 minutes** old.

When you encounter a stale lock:
1. Check `memory/session/active/` to see if the locking session is still registered.
2. If the locking session is still active (recent heartbeat): The lock is NOT stale, the session is just slow. Wait or ask Rob.
3. If the locking session is stale/gone: Delete the lock file, leave a message in `messages.md`, create your own lock.

---

## Error Prevention

**Race condition on lock creation:** Two sessions checking the same file at the same time could both see "no lock" and both create one. To minimize this:
1. After creating your lock file, WAIT 2 seconds.
2. Read the lock file back.
3. If your session_id is in the file, you have the lock.
4. If a different session_id is there (they overwrote yours), back off and try again in 30 seconds.

**Forgetting to release:** If your session crashes, the lock stays. The 30-minute stale timeout handles this automatically. Next session will detect it and proceed.

**Nested locks:** If you need to write to multiple files, acquire all locks BEFORE starting any writes. Release them all AFTER all writes complete. This prevents deadlocks where Session A holds file 1 and needs file 2, while Session B holds file 2 and needs file 1.

---

## Quick Reference

| Action | Command |
|--------|---------|
| Check lock | `ls .locks/{filename}.lock` |
| Acquire lock | Create `.locks/{filename}.lock` with your session JSON |
| Release lock | Delete `.locks/{filename}.lock` |
| Stale threshold | 30 minutes from `locked_at` |
| Multiple files | Lock ALL first, write ALL, release ALL |
