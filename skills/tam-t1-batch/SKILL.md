# TAM T1 Batch — Full Workflow Skill

## Description
End-to-end workflow for building a new batch of TAM Outbound T1 email outreach. Sources contacts from TAM/Factor accounts, researches them, drafts personalized T1 emails, runs QA gate, enrolls in Apollo, logs everything, and presents for Rob's APPROVE SEND.

## Trigger
Use when Rob says "build a new batch", "T1 batch", "prospect new contacts", "TAM outreach", or when the operating directive calls for new T1 pipeline volume.

## Prerequisites
- Read `memory/playbooks/tam-t1-batch.md` for the full 10-step process
- Read `memory/playbooks/dedup-protocol.md` for the 6-point dedup check
- Read `memory/playbooks/apollo-enrollment.md` for enrollment gotchas
- Read `memory/playbooks/qa-gate.md` for the 12-point MQS system
- Read `memory/playbooks/batch-tracker-html.md` for the tracker template
- Check `memory/session/active/` for other sessions and avoid company conflicts
- Check `memory/session/messages.md` for any relevant alerts

## Parallel Safety
Before starting:
1. Register in `memory/session/active/{N}.json` with the companies you plan to prospect
2. Check that no other active session has claimed the same companies
3. Acquire file locks for `MASTER_SENT_LIST.csv` and any tracker files you'll create

## Step-by-Step

### 1. Source Accounts
Read `tam-accounts-mar26.csv` and `memory/target-accounts.md`. Priority: Factor > TAM HIGH > TAM MEDIUM.
Skip accounts already fully covered (check target-accounts.md for coverage status).

### 2. Find Contacts
Use Apollo People Search or Sales Nav Deep Sweep (see `playbooks/sales-nav-deep-sweep.md`).
Target personas: QA Manager, QA Lead, Director of QA, VP Quality, Test Manager, SDET Lead, Automation Lead.

### 3. Dedup Every Contact
Run ALL 6 checks from `playbooks/dedup-protocol.md`:
1. MASTER_SENT_LIST.csv grep
2. DNC list in CLAUDE.md
3. Apollo contacts search
4. Current batch duplicate check
5. Same-company awareness
6. TAM domain verification against tam-accounts-mar26.csv

### 4. Research Each Contact
Standard/Medium/High targeting based on contact density per company (see playbook).

### 5. Draft T1 Emails
Formula from sop-tam-outbound.md Part 6:
- Subject: `{First name}'s {role context} at {Company}`
- 75-99 words, 2 question marks, named customer with numbers, "What day works" CTA
- No em dashes, no placeholders, Testsigma mentioned by name

### 6. QA Gate Every Email
MQS >= 9/12 to pass. See `playbooks/qa-gate.md` for full 12-point checklist.
Hard fail on: placeholders, word count >120/<60, missing proof point, duplicate proof point at same company.

### 7. Build Batch Tracker HTML
Template in `playbooks/batch-tracker-html.md`. Name: `tamob-batch-{YYYYMMDD}-{N}.html`.
Include: contact cards, email drafts, QA gates, proof point rotation, backlog section.

### 8. Create Apollo Contacts + Enroll
See `playbooks/apollo-enrollment.md`. Max 5 per API call. Use `run_dedupe: true`.
Handle errors: ownership, job change, active-in-other-campaigns (all documented in playbook).

### 9. Log Everything
- Add rows to MASTER_SENT_LIST.csv (1 row per contact)
- Update session-log.md with enrollment details and Apollo IDs
- Update handoff.md with wave/batch section
- Add new tasks to work-queue.md (T1 sends pending APPROVE SEND, T2 due date)
- Leave message in messages.md: `[CLAIM] Enrolled N contacts from {companies}`
- Update heartbeat in active session registration

### 10. Present for APPROVE SEND
Tell Rob: contact count, companies, link to tracker HTML, any blockers.
Wait for explicit "APPROVE SEND" before any emails go out.

## Post-APPROVE SEND
See `playbooks/apollo-task-queue-sends.md` for the send execution process.

## Error Handling
See `playbooks/error-recovery.md` for all known errors and fixes.

## Session End
Follow `playbooks/session-handoff.md` for proper handoff.
Delete your active session registration. Release file locks. Git commit.
