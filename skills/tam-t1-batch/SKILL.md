# TAM T1 Batch — Full Workflow Skill

## Description
End-to-end workflow for building a new batch of TAM Outbound T1 email outreach. Sources contacts from TAM/Factor accounts, researches them, drafts personalized T1 emails, runs QA gate, enrolls in Apollo, logs everything, and presents for Rob's APPROVE SEND.

## Trigger
Use when Rob says "build a new batch", "T1 batch", "prospect new contacts", "TAM outreach", or when the operating directive calls for new T1 pipeline volume.

## Prerequisites
> **Index-first rule:** Before loading any playbook, check `memory/playbooks/_index.md` first. It maps each task to the specific playbook file you need. This prevents loading full playbooks you don't need and saves context budget.

- Read `memory/playbooks/tam-t1-batch.md` for the full 10-step process
- Read `memory/playbooks/dedup-protocol.md` for the 6-point dedup check
- Read `memory/playbooks/apollo-enrollment.md` for enrollment gotchas
- Read `memory/playbooks/qa-gate.md` for the 12-point MQS system
- Read `memory/playbooks/batch-tracker-html.md` for the tracker template
- Check `memory/session/active/` for other sessions and avoid company conflicts
- Check `memory/session/messages.md` for any relevant alerts

## New Skills Available (use these — they replace manual steps)

| Step | Old Approach | New Skill |
|------|-------------|-----------|
| Steps 1-3 (source + dedup) | Manual TAM lookup + dedup-protocol.md | `skills/enrichment-pipeline/SKILL.md` — runs all at once |
| Step 3 (compliance) | 6-point dedup-protocol.md | `skills/compliance-gate/SKILL.md` — now 8 points |
| Step 6 (QA gate) | Manual 12-point checklist | `skills/draft-qa/SKILL.md` — automated scoring |
| Before Step 1 | No trigger research | `skills/trigger-monitor/SKILL.md` — find best accounts to prioritize |
| After Step 10 | Manual handoff | `skills/handoff-auto/SKILL.md` — auto-generates handoff docs |

## Parallel Safety
Before starting:
1. Register in `memory/session/active/{N}.json` with the companies you plan to prospect
2. Check that no other active session has claimed the same companies
3. Acquire file locks for `MASTER_SENT_LIST.csv` and any tracker files you'll create

## Step-by-Step

### 0. [NEW] Check Trigger Events First
Before sourcing accounts, run `skills/trigger-monitor/SKILL.md` to identify which accounts have fresh signals (QA hiring, funding, leadership changes). Accounts with triggers get prioritized — they produce better openers and higher reply rates.

### 1. Source Accounts
**Preferred:** Run `skills/enrichment-pipeline/SKILL.md` — it handles Steps 1-3 in one automated flow.
Manual fallback: Read `tam-accounts-mar26.csv` and `memory/target-accounts.md`. Priority: Factor > TAM HIGH > TAM MEDIUM.
Skip accounts already fully covered (check target-accounts.md for coverage status).

### 2. Find Contacts
**If using enrichment-pipeline skill:** Skip to Step 3 — enrichment-pipeline handles contact discovery.
Manual fallback: Use Apollo People Search or Sales Nav Deep Sweep (see `playbooks/sales-nav-deep-sweep.md`).
Target personas: QA Manager, QA Lead, Director of QA, VP Quality, Test Manager, SDET Lead, Automation Lead.

### 3. Dedup + Compliance Every Contact
**Preferred:** Run `skills/compliance-gate/SKILL.md` — runs all 8 checks automatically.
Manual fallback: Run ALL 6 checks from `playbooks/dedup-protocol.md`:
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
**Preferred:** Run `skills/draft-qa/SKILL.md` — auto-scores all drafts with both mechanical checks (7/12) and AI judgment (5/12). Outputs a pass/fail with specific fix suggestions.
Manual fallback: MQS >= 9/12 to pass. See `playbooks/qa-gate.md` for full 12-point checklist.
Hard fail on: placeholders, word count >120/<60, missing proof point, duplicate proof point at same company.

### 7. Build Batch Tracker HTML
Template in `playbooks/batch-tracker-html.md`. Name: `tamob-batch-{YYYYMMDD}-{N}.html`.
Include: contact cards, email drafts, QA gates, proof point rotation, backlog section.

### 8. Create Apollo Contacts + Enroll
See `playbooks/apollo-enrollment.md`. Max 5 per API call. Use `run_dedupe: true`.
Handle errors: ownership, job change, active-in-other-campaigns (all documented in playbook).

### 9. Log Everything (ALL sub-steps mandatory)

**a) MASTER_SENT_LIST.csv** — Add 1 row per contact.
- Use the FULL batch name standard: `TAM Outbound Batch {N} Mar{DD}` (NEVER "B7" or "W6B1")
- Run `wc -l MASTER_SENT_LIST.csv` BEFORE and AFTER appending. Verify: after_count = before_count + contacts_added
- Format: `name,batch,send_date,channel,credits,file,norm`

**b) handoff.md** — Add a NEW SECTION with:
- Full contact table (Name, Company, Apollo ID, Email, Status)
- Sequence ID, send-from account ID, T2 due date
- Any enrollment overrides used (finished_in_other, active_in_other, job_change) per contact
- Any blocked/skipped contacts with reasons and required Rob actions

**c) work-queue.md** — Add new tasks for:
- T1 sends pending APPROVE SEND (if enrollment-only, not auto-send)
- T2 follow-up drafts with due date

**d) session-log.md** — Append session entry with contact table

**e) messages.md** — Append `[CLAIM]` or `[DONE]` at the TOP of Messages section:
- Get real current time: `date -u +%Y-%m-%dT%H:%M:%SZ`
- Include: exact row count from step (a), companies, contact count, any overrides
- Format: `[{timestamp}] Session {N}: [DONE] Enrolled {N} contacts from {companies}. MASTER_SENT_LIST.csv now {total} rows ({previous}+{added}). Tracker: {filename}. Do not re-prospect these contacts.`

**f) Update heartbeat in active session registration

### 10. Present for APPROVE SEND
Tell Rob: contact count, companies, link to tracker HTML, any blockers.
Wait for explicit "APPROVE SEND" before any emails go out.

## Post-APPROVE SEND
See `playbooks/apollo-task-queue-sends.md` for the send execution process.

## Error Handling
See `playbooks/error-recovery.md` for all known errors and fixes.

## Session End
**Preferred:** Run `skills/handoff-auto/SKILL.md` — auto-generates all handoff docs (handoff.md, work-queue.md, session-log.md, in-progress.md) from session activity.
Manual fallback: Follow `playbooks/session-handoff.md`.
Delete your active session registration. Release file locks. Git commit.

## Pipeline Visibility
After this batch is enrolled and sent, update the dashboard:
Run `skills/batch-dashboard/SKILL.md` to regenerate `pipeline-dashboard.html` with the new batch included.
