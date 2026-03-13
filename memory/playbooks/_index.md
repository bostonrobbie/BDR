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
| T2 Follow-Up Drafting | `t2-followup.md` | Writing Touch 2 follow-up emails (see also: `skills/t2-draft/SKILL.md`) |
| Session Handoff | `session-handoff.md` | Properly closing a session and handing off to the next |
| Inbound Leads Sequence | `inbound-leads-sequence.md` | Identifying, qualifying, enrolling, and sending to inbound Salesforce-assigned leads |
| Warm Lead Escalation | `warm-lead-escalation.md` | When a prospect replies with interest — respond, draft follow-up, book meeting |
| Meeting Prep | `meeting-prep.md` | Generating a prep card when a meeting is booked |

---

## New Skills (added 2026-03-12)

10 new Cowork skills built to extend the workflow. Read these SKILL.md files directly — they are invokable as Cowork skills and follow the same format as playbooks:

| Skill | Location | Use When |
|-------|----------|----------|
| Reply Classifier | `skills/reply-classifier/SKILL.md` | Checking Gmail for replies — classifies by type, updates warm-leads.md |
| Batch Dashboard | `skills/batch-dashboard/SKILL.md` | Generating pipeline overview across all batches |
| Enrichment Pipeline | `skills/enrichment-pipeline/SKILL.md` | Pre-batch prep — TAM verify, enrich, dedup, compliance in one flow |
| Trigger Monitor | `skills/trigger-monitor/SKILL.md` | Scanning accounts for QA hiring, funding, leadership changes |
| Draft QA | `skills/draft-qa/SKILL.md` | Auto-scoring drafts against the 12-point MQS rubric |
| Reply Router | `skills/reply-router/SKILL.md` | Routing replies to the right objection doc and drafting responses |
| Lifecycle Tracker | `skills/lifecycle-tracker/SKILL.md` | Building and maintaining unified contact history |
| Analytics Engine | `skills/analytics-engine/SKILL.md` | Weekly performance analytics by persona, vertical, proof point |
| Handoff Auto | `skills/handoff-auto/SKILL.md` | Auto-generating session handoff docs at end of session |
| Compliance Gate | `skills/compliance-gate/SKILL.md` | 8-point safety check before any contact enrollment |
| T2 Draft | `skills/t2-draft/SKILL.md` | Draft T2 follow-up emails with cadence enforcement and QA gate |

---

## Skill Candidates (formalized)
All original candidates are now live skills:
1. `tam-t1-batch.md` ✅ `skills/tam-t1-batch/SKILL.md`
2. `apollo-enrollment.md` ✅ `skills/apollo-enroll/SKILL.md`
3. `dedup-protocol.md` ✅ Embedded in `skills/compliance-gate/SKILL.md`
4. `t2-followup.md` ✅ `skills/t2-draft/SKILL.md` (added Mar 13, 2026)

---

*Last updated: 2026-03-13 (Session 31 audit — 2 new playbooks: warm-lead-escalation, meeting-prep; 1 new skill: t2-draft; index updated to reflect all 14 playbooks + 14 skills)*
