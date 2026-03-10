# AGENTS.md — Multi-Agent Collaboration Protocol
## Rob Gorham BDR Second Brain — Testsigma

---

## Purpose

This file defines how Claude agents collaborate on Rob's BDR workflow across sessions.
Every new session reads this file first, then CLAUDE.md, then handoff.md and work-queue.md.

---

## Agent Startup Sequence (MANDATORY — every session)

```
STEP 1: git pull origin main   (may fail if no creds — note and continue)
STEP 2: Read AGENTS.md         (this file)
STEP 3: Read CLAUDE.md         (full BDR SOP and memory)
STEP 4: Read memory/session/handoff.md   (current pipeline state)
STEP 5: Read memory/session/work-queue.md (available tasks)
STEP 6: Claim a task OR ask Rob what to work on
STEP 7: Report current state to Rob
```

---

## Session Files

| File | Purpose | Updated by |
|------|---------|------------|
| `AGENTS.md` | This protocol file | Rob or Claude when protocol changes |
| `CLAUDE.md` | Full BDR SOP, memory, rules | Rob or Claude after major decisions |
| `memory/session/handoff.md` | Current pipeline state snapshot | Claude at END of every session |
| `memory/session/work-queue.md` | Task queue with priorities | Claude at END of every session |
| `memory/session/session-log.md` | Running log of what each session did | Claude — append only |

---

## Handoff Protocol

At the END of every session, before stopping, Claude MUST:

1. Update `memory/session/handoff.md` with current pipeline state
2. Update `memory/session/work-queue.md` — mark completed tasks, add new ones
3. Append a session entry to `memory/session/session-log.md`
4. Commit all changes: `git add -A && git commit -m "Session [date]: [1-line summary]"`
5. Remind Rob to `git push` from his terminal (Claude cannot push due to auth)

---

## Task Claiming

When claiming a task from work-queue.md:
- Update the task status to `IN_PROGRESS` with the session timestamp
- Only claim ONE task at a time unless Rob asks for parallel work
- Update status to `DONE` when complete

---

## Hard Rules (inherited from CLAUDE.md)

- Never send any message without Rob's explicit APPROVE SEND
- Never use personal Gmail (rgorham369@gmail.com) for work
- Always use Blue/Work Chrome profile for browser automation
- Never modify existing company data without explicit approval
- Draft everything → Rob reviews → Rob executes

---

## File Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Batch trackers | `outreach-sent-[date]-batch[N].html` | `outreach-sent-feb26-batch3.html` |
| SOP documents | `[topic]-sop-[version].md` | `tier1-intent-sop-master.md` |
| Draft files | `[touch]_drafts_[batch].md` | `touch2_drafts_feb27.md` |
| Research | `company-research-[name].md` | `company-research-overdrive.md` |
| Cycle logs | `cycle-logs/[date]-[session].md` | `cycle-logs/2026-03-07-morning.md` |
| Session files | `memory/session/[name].md` | `memory/session/handoff.md` |

---

*Last updated: 2026-03-07*
