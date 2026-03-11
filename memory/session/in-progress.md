# In-Progress Checkpoint

**Status: CLEAR**
*Last cleared: 2026-03-11 (Session 15 — Crash-recovery infrastructure built)*

---

No task currently in progress. Safe to start any new task from `work-queue.md`.

---

## Purpose

This file is the **crash-recovery mechanism** for this BDR workflow.

| Event | Action |
|-------|--------|
| Task START | Claude writes ACTIVE block below + commits immediately |
| Each sub-step done | Claude checks off step + commits ("Checkpoint: …") |
| Task END (normal) | Claude sets Status → CLEAR + commits |
| Session START | Claude reads this file — CLEAR = normal; ACTIVE = crash |

If you open this file at the start of a session and see **Status: ACTIVE**, a prior session crashed mid-task. Follow the Crash Recovery Protocol below.

---

## Crash Recovery Protocol (for Claude)

1. **Stop.** Do NOT start a new task.
2. Tell Rob: *"I found an interrupted task from the last session. [Task name] was in progress. [N of M] steps were completed. The last safe checkpoint was: [step description]. Shall I resume from step [N+1], or restart the task from scratch?"*
3. Wait for Rob to confirm: resume or restart.
4. If **resuming**: begin at the step marked `← NEXT`. Check that files listed in "Files in progress" actually exist on disk before assuming their contents.
5. If **restarting**: set Status → CLEAR, commit, then claim the task fresh from work-queue.md.
6. **Never redo completed steps** — verify files exist first; if they do, trust the checkpoint.

---

## Mid-Session Commit Triggers (mandatory — see AGENTS.md)

These events require an immediate `git add -A && git commit` even in the middle of a session:

- Any new file created in `/Work/` (HTML tracker, draft MD, SOP update, etc.)
- After each group of 5 contacts drafted in a batch task
- After any `MASTER_SENT_LIST.csv` update
- After any `memory/` file update (pipeline-state.md, warm-leads.md, etc.)
- After each sub-step is checked off in this file

Commit message format:
- Mid-session: `Checkpoint: [TASK-XXX] — [step name] (step N/M)`
- Session-end: `Session [date]: [1-line summary]`

---

## Template

When starting a multi-step task, **replace this entire file's content** with the block below (fill in the blanks):

```
# In-Progress Checkpoint

**Status: ACTIVE**
*Started: [YYYY-MM-DD] Session [N]*

---

## Task: [TASK-XXX] — [Task name]

**What I'm doing:** [One sentence]

## Steps

- [x] Step 1: [description] ✅ [time/commit]
- [x] Step 2: [description] ✅ [time/commit]
- [ ] **Step 3: [description] ← NEXT**
- [ ] Step 4: [description]
- [ ] Step 5: Clear this file + update handoff.md + work-queue.md

## Files in progress

| File | Location | Current state |
|------|----------|---------------|
| [filename.html] | /Work/ | Exists. [N]/[M] contacts added. |
| [other file] | /Work/memory/ | In progress — [description] |

## Last commit

`[hash]` — "Checkpoint: [TASK-XXX] — step [N/M]"

## Resume instructions

**Start from:** Step [N+1]
**Specifically:** [Exact instruction — e.g., "Draft T2 for Seth Drummond (#4). T1 used Hansard proof point. Next proof point: CRED."]
**Do NOT redo:** Steps 1–[N] (files already exist on disk)
**Critical context:** [Any facts next session needs — e.g., proof point rotation rules, Apollo task IDs, open decisions]
```

---

*File created: 2026-03-11 (Session 15 — crash-recovery infrastructure)*
*See AGENTS.md for full protocol rules*
