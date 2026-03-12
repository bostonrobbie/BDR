# Playbooks — Knowledge Registry

## Purpose
Captured knowledge from real production work across 27+ sessions. Each playbook documents a specific workflow, including the gotchas and edge cases discovered through trial and error. New sessions should read relevant playbooks BEFORE starting a task instead of rediscovering these lessons.

## How to Use
1. Check this index for relevant playbooks before starting any task.
2. Read the full playbook file, not just the title.
3. If you discover a new gotcha or edge case during your session, UPDATE the relevant playbook (or create a new one).
4. Playbooks are living documents. Keep them current.

---

## Playbook Index

| Playbook | File | Use When |
|----------|------|----------|
| TAM T1 Batch (End-to-End) | `tam-t1-batch.md` | Building a new batch of T1 email outreach from scratch |
| Apollo Enrollment | `apollo-enrollment.md` | Creating contacts and enrolling them in Apollo sequences |
| Apollo Task Queue Sends | `apollo-task-queue-sends.md` | Sending emails through Apollo's manual task queue |
| Sales Nav Deep Sweep | `sales-nav-deep-sweep.md` | Finding QA contacts at target companies via LinkedIn Sales Navigator |
| Dedup Protocol | `dedup-protocol.md` | Checking contacts against all databases before outreach |
| Catchall Domains | `catchall-domains.md` | Handling companies with catchall email domains |
| QA Gate | `qa-gate.md` | Scoring and validating outreach emails before send |
| Error Recovery | `error-recovery.md` | Common Apollo/workflow errors and how to fix them |
| Batch Tracker HTML | `batch-tracker-html.md` | Building and maintaining HTML batch tracker files |
| T2 Follow-Up Drafting | `t2-followup.md` | Writing Touch 2 follow-up emails |
| Session Handoff | `session-handoff.md` | Properly closing a session and handing off to the next |

---

## Skill Candidates (for Cowork skill formalization)
These playbooks are stable enough to become formal Cowork skills:
1. `tam-t1-batch.md` — most-used workflow, highly repeatable
2. `apollo-enrollment.md` — specific API sequence, error-prone without guidance
3. `dedup-protocol.md` — safety-critical, must be consistent

---

*Last updated: 2026-03-12 (Session 28 — initial build from 27 sessions of accumulated knowledge)*
