# File Locking Protocol
*Version: 1.1 — 2026-03-13 (stale threshold aligned to 45 min; added append-only safe zone)*

## Purpose
Prevents two concurrent sessions from writing to the same file simultaneously. Used for files that are NOT append-only (handoff.md, work-queue.md, in-progress.md) or for append-only files when multiple sessions are writing at once (MASTER_SENT_LIST.csv).

---

## How to Acquire a Lock

### Step 1: Check for existing lock
```bash
ls .locks/{filename}.lock 2>/dev/null
```

If a lock file exists, read it:
```bash
cat .locks/{filename}.lock
```

Check `acquired_at`. If it's more than **45 minutes** old → stale lock (see below). Otherwise, wait or pick a different file/task.

### Step 2: Create your lock file
```bash
echo '{
  "locked_by_session": {N},
  "acquired_at": "{ISO 8601 timestamp}",
  "purpose": "{1-line description of why you need this file}",
  "expected_duration_minutes": {N}
}' > .locks/{filename}.lock
```

### Step 3: Do your work

### Step 4: Release the lock
```bash
rm .locks/{filename}.lock
```

**Always release immediately after your write is complete.** Do not hold locks longer than needed.

---

## Stale Lock Detection

A lock is considered **stale** if:
- `acquired_at` is more than **45 minutes** old

*Rationale: Aligned with `active/_protocol.md` stale session threshold (also 45 min). Eliminates asymmetry where sessions were blocked by stale locks (30 min) even though their registration remained "active" (60 min). Both systems now use the same 45-minute window.*

When you detect a stale lock:
1. Read the lock file to see which session acquired it.
2. Check `memory/session/active/` — is that session still registered and active?
3. If the session appears crashed (no heartbeat in 45+ min): override the lock. Leave a message in `messages.md`:
   `[WARN] Overriding stale lock on {file} — Session {N}'s lock was {age} minutes old and session appears crashed.`
4. Proceed with your write, then release the lock immediately.

---

## Files That Use Locks

| File | Lock Needed? | Notes |
|------|-------------|-------|
| `memory/session/handoff.md` | Yes — exclusive | One session at a time |
| `memory/session/work-queue.md` | Yes — exclusive | One session at a time |
| `memory/session/in-progress.md` | Yes — exclusive | One session at a time |
| `memory/session/messages.md` | Yes — brief | Acquire → append single message → release immediately |
| `MASTER_SENT_LIST.csv` | Yes — brief | Acquire → append rows → verify row count → release |
| Batch tracker HTML files | Only if two sessions share the same tracker | Typically one session per tracker |
| `memory/warm-leads.md` | Yes — brief | Acquire → update → release |
| `memory/session/rob-availability.json` | Yes — brief | Acquire → update → release |
| `memory/session/.last-session-number` | Yes — brief | Read + increment + write atomically |

---

## Append-Only Safe Zone

These files can be appended to WITHOUT a lock if sessions are working on **different contacts/rows**:
- `MASTER_SENT_LIST.csv` — safe if sessions append different contact rows. Use lock anyway for safety.
- `memory/session/session-log.md` — append-only, but lock during write to prevent interleaved entries.

Rule: When in doubt, use a lock. A brief lock (acquire → append → release, under 30 seconds) adds minimal overhead.

---

## Quick Reference

```bash
# Acquire lock
echo '{"locked_by_session": N, "acquired_at": "ISO_TS", "purpose": "..."}' > .locks/FILENAME.lock

# Check if locked
ls .locks/FILENAME.lock

# Check lock age (seconds since acquired_at)
# Parse acquired_at field and compare to current time

# Release lock
rm .locks/FILENAME.lock
```
