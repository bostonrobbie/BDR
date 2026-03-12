# Playbook: Session Handoff

## When to Use
At the END of every session, before stopping. This ensures the next session (which may be on a different machine with no shared memory) can pick up seamlessly.

---

## Handoff Checklist (5 Steps, All Mandatory)

### Step 1: Clear In-Progress Checkpoint
If you had a task in progress:
1. Open `memory/session/in-progress.md`
2. Set Status to **CLEAR**
3. Update the "Last completed task" line with what you finished

If no task was in progress, skip this step.

### Step 2: Update handoff.md
This is the pipeline state snapshot that every new session reads on startup.

**What to update:**
- `Last Updated` header line: session number, date, 1-line summary
- Add a new section for any wave/batch work you did (with full contact table, Apollo IDs, status)
- Update any existing sections if their status changed (e.g., T1 sends completed, T2 due dates)
- Update the "Next session" guidance at the bottom of the file

**What NOT to do:**
- Don't delete old wave sections (they're historical reference)
- Don't rewrite the whole file (just update/append relevant sections)

### Step 3: Update work-queue.md
**What to update:**
- `Last Updated` header line: session number, date, 1-line summary
- Mark completed tasks as `✅ DONE` with date and session number
- Add new tasks discovered during your session (T2 drafts due, sends pending APPROVE SEND, etc.)
- Update status of in-progress tasks

**Task format for new tasks:**
```markdown
### TASK-{XXX}: {Short description}
**Status:** UNCLAIMED
**Priority:** P0/P1/P2/P3
**Effort:** ~{N} min
**Output:** {filename or "Report in chat"}

{Full description with all context the next session needs to execute this task without asking questions.}
```

### Step 4: Append to session-log.md
Add a new entry at the BOTTOM of the file:

```markdown
## Session {N} — {1-line title} ({date})

**Task:** {TASK-XXX or "ad-hoc"}
**Duration:** ~{N} min
**What was done:**
- {Bullet points of accomplishments}

**Files changed:**
- {List of files created or modified}

**Contacts enrolled:** {N} (if applicable)
| Name | Company | Apollo ID | Email | Status |
|------|---------|-----------|-------|--------|

**Notes:**
- {Any gotchas, decisions, or context the next session should know}

**Next:** {What the next session should do first}
```

### Step 5: Deregister from Active Sessions
If you created an active session registration file:
1. Delete `memory/session/active/{session-number}.json`
2. Release any file locks you hold in `.locks/`

### Step 6: Git Commit
```bash
git add -A && git commit -m "Session {date}: {1-line summary}"
```
Remind Rob to `git push` from his terminal.

---

## Common Mistakes

1. **Updating only the header of handoff.md:** The header is a summary. The BODY needs the detailed wave/batch section too. Don't forget the body.
2. **Not adding new tasks to work-queue.md:** If your work created follow-up tasks (T2 due, sends pending), add them as new TASK entries.
3. **Forgetting to clear in-progress.md:** Leaves the file in ACTIVE state, which triggers crash recovery for the next session.
4. **Not releasing file locks:** Check `.locks/` directory and delete any lock files you created.
5. **Skipping session-log.md:** The log is the only chronological record. Don't skip it even if the session was short.

---

## Parallel Session Handoff

If multiple sessions are running simultaneously:
1. Each session handles its own handoff independently
2. Use file locks for handoff.md and work-queue.md (only one session writes at a time)
3. Session-log.md is append-only, so simultaneous appends are generally safe (but use a lock for safety)
4. Leave a `[DONE]` message in messages.md summarizing what you did

---

*Last updated: 2026-03-12 — from AGENTS.md handoff protocol + 27 sessions of practice*
