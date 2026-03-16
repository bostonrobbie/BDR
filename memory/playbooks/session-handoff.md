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

### Step 2: Update handoff.md (MOST CRITICAL STEP)
This is the pipeline state snapshot that every new session reads on startup. **Session 30 audit found handoff.md 4+ sessions stale. This step is the #1 cause of information loss between sessions.**

**What to update:**
- `Last Updated` header line: session number, date, 1-line summary
- Add a NEW SECTION for any wave/batch work you did (with full contact table: Name, Company, Apollo ID, Email, Status)
- Update any existing sections if their status changed (e.g., T1 sends completed, T2 due dates)
- Update the "Next session" guidance at the bottom of the file
- If you enrolled contacts, the new section MUST include: sequence ID, send-from account, T2 due date, any override flags used, any blocked/skipped contacts with reasons

**Self-check:** Read back the section you just added. Could a brand-new session execute the T2 follow-ups for these contacts with ONLY the information in handoff.md? If not, add more detail.

**What NOT to do:**
- Don't delete old wave sections (they're historical reference)
- Don't rewrite the whole file (just update/append relevant sections)
- Don't skip this step even if you're running low on context. Handoff.md is more important than session-log.md.

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

1. **Updating only the header of handoff.md:** The header is a summary. The BODY needs the detailed wave/batch section too. Don't forget the body. This is the #1 most common mistake.
2. **Not adding new tasks to work-queue.md:** If your work created follow-up tasks (T2 due, sends pending), add them as new TASK entries.
3. **Forgetting to clear in-progress.md:** Leaves the file in ACTIVE state, which triggers crash recovery for the next session.
4. **Not releasing file locks:** Check `.locks/` directory and delete any lock files you created.
5. **Skipping session-log.md:** The log is the only chronological record. Don't skip it even if the session was short.
6. **Not registering in active sessions directory:** Session 30 audit found zero registration for concurrent sessions. Create `memory/session/active/{N}.json` BEFORE doing any work. This is STEP 10 of startup, not optional.
7. **Using non-standard batch names in MASTER_SENT_LIST.csv:** Never use abbreviations like "B7" or "W6B1". Use the full standard format from `playbooks/dedup-protocol.md` (e.g., "TAM Outbound Batch 7 Mar12").
8. **DONE message count mismatch:** Always run `wc -l MASTER_SENT_LIST.csv` right before writing a DONE/CLAIM message. State the EXACT row count you just verified, not what you think it should be.
9. **Messages.md timestamp wrong:** Use `date -u +%Y-%m-%dT%H:%M:%SZ` to get the real current time. Don't estimate or use a timestamp from earlier in your session.
10. **Skipping handoff.md entirely:** If you're running low on context, handoff.md > session-log.md > work-queue.md. Prioritize in that order. A session that updates handoff.md but skips session-log.md is better than one that does neither.

---

## Parallel Session Handoff

If multiple sessions are running simultaneously:
1. Each session handles its own handoff independently
2. Use file locks for handoff.md and work-queue.md (only one session writes at a time)
3. Session-log.md is append-only, so simultaneous appends are generally safe (but use a lock for safety)
4. Leave a `[DONE]` message in messages.md summarizing what you did

---

*Last updated: 2026-03-12 (Session 30 audit) — added 5 new common mistakes from audit, strengthened Step 2 with self-check, added priority order for context-constrained sessions*
