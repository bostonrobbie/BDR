# Codex-Cowork Operating Protocol

Last updated: 2026-03-06
Owner: Rob Gorham

## 1) Role Split

Codex is internal intelligence and production control.
Cowork is external execution across connected systems.
Rob is final approver and operator of send authority.

Codex responsibilities:
- Read and enforce SOP rules from `memory/` and trackers in `C:\Users\rgorh\OneDrive\Desktop\Work`.
- Build targeting logic, drafts, QA gates, cadence checks, and send plans.
- Run mandatory preflight checks before any write action is proposed.
- Produce run plans, run logs, and post-run reports.

Cowork responsibilities:
- Execute external read and write actions in Apollo, Gmail, Sales Nav, Calendar, Drive.
- Return structured outputs with IDs, timestamps, and status per item.
- Follow Codex-provided execution checklist exactly.

Rob responsibilities:
- Confirm priorities and scope.
- Give explicit send approvals using exact phrase `APPROVE SEND`.
- Approve any update/delete to existing records on a named per-item basis.

## 2) Non-Negotiable Gates

1. No sends without `APPROVE SEND`.
2. No update/delete of existing records without explicit per-item approval.
3. DNC check is mandatory before every draft and send action.
4. Dedup against `MASTER_SENT_LIST.csv` is mandatory before draft creation.
5. Cadence enforcement is mandatory:
- Touch 2 not before Day 4.
- Touch 3 not before Day 9.
6. Every prospect must exist in a tracker before any draft is created.
7. Use work identity only, `robert.gorham@testsigma.com`.
8. No Slack or coworker-visible actions unless explicitly requested by Rob.

## 3) Critical System Flags

1. Apollo send identity risk:
- Apollo default sending account is `.net`, not `.com`.
- Every sequence enrollment must force `.com` account ID:
`send_email_from_email_account_id: "68e3b53ceaaf74001d36c206"`

2. Sales Nav profile risk:
- Sales Nav auth is browser-driven and not MCP-verifiable.
- Start of every send session must include manual confirmation of blue/work Chrome profile.

3. Credit checkpoints:
- Apollo credits were 6,790 on 2026-03-06.
- Sales Nav InMail credits were 23 last confirmed on 2026-03-04, refresh before send block.

## 4) Standard Command Contract

Use this format for fastest reliable runs:
`[ACTION TYPE]: [TARGET]. [KEY PARAMETERS]. [CONSTRAINTS/NOTES].`

Approved action types:
- `PREFLIGHT`
- `ENRICH`
- `DRAFT TOUCH 1`
- `DRAFT TOUCH 2`
- `DRAFT TOUCH 3`
- `DRY RUN`
- `FOLLOW-UP CHECK`
- `RETRY`
- `APPROVE SEND`

Examples:
- `PREFLIGHT: Batch 10 CSV. Check DNC, duplicates, cadence, same-company collisions. Return report only.`
- `DRAFT TOUCH 1: Jane Doe at Acme. Persona QA Manager. Pain flaky tests. Under 95 words. One CTA.`
- `DRY RUN: Touch 2 candidates from Batch 7 who are Day 4+ and no reply.`
- `APPROVE SEND: Draft ID abc123 to Jane Doe at Acme.`

## 5) Handoff Payload Schema

Every Codex-to-Cowork handoff should include:
- `run_id`
- `mode` (`read_only`, `dry_run`, `execute`)
- `action_type`
- `input_source` (file name, query, or named list)
- `gates` (dnc, dedup, cadence, same_company, send_approval)
- `constraints` (word count, CTA, persona, channel)
- `expected_outputs`
- `error_policy` (`continue_on_error: true`, itemized failures)

Every Cowork response should include:
- `run_id`
- `item_id`
- `prospect_name`
- `system`
- `action`
- `status` (`success`, `failed`, `skipped`)
- `reason`
- `system_record_id` (Apollo/Gmail/Sales Nav ID where available)
- `timestamp_et`
- `timestamp_iso`

## 6) Preflight Checklist (Required)

Before any draft creation, enrollment, or send:
1. DNC cross-reference from policy sources.
2. Dedup check vs `MASTER_SENT_LIST.csv` using LinkedIn URL first, then name/company fallback.
3. Cadence eligibility check based on send dates.
4. Tracker existence check, no orphan prospects.
5. Same-company collision flagging for manual decision.
6. Credit budget estimate and sufficiency check.
7. Channel availability check (InMail access, email validity).
8. `APPROVE SEND` gate status for any action that sends.

## 7) Execution States

- `READ_ONLY`: Gather, classify, and report. No writes.
- `DRY_RUN`: Build complete action plan and estimated impact. No writes.
- `EXECUTE_NON_SEND`: Allowed writes that do not send, for example create drafts, create new contacts, append logs.
- `EXECUTE_SEND`: Allowed only with explicit `APPROVE SEND` tied to listed items.

## 8) Daily Operating Sequence

1. Identity and environment check.
- Confirm blue/work Chrome profile for Sales Nav.
- Confirm Gmail identity is `robert.gorham@testsigma.com`.

2. Intel scan.
- Replies, warm leads, today calendar, credit state, draft audit, follow-up eligibility.

3. Preflight report.
- DNC, dedup, cadence, same-company, credit budget, anomalies.

4. Draft production.
- Build C2-compliant drafts with one CTA and MQS target.

5. Approval gate.
- Pause for explicit `APPROVE SEND` instruction.

6. Execution and logging.
- Execute approved items.
- Write JSON + CSV logs with run ID.
- Append outcomes to trackers without overwriting prior rows.

7. Post-run report.
- Succeeded, failed, skipped, credits used, next due actions.

## 9) Logging Standard

Run ID format:
`RUN_YYYYMMDD_HHMMSS`

Required artifacts per run:
- `logs\runs\<run_id>.json`
- `logs\runs\<run_id>.csv`
- Human-readable summary in chat

Retention:
- Persist in Work folder, no auto-expiration.
- Archive old logs periodically to reduce clutter.

## 10) Failure and Retry Rules

- Process sequentially, item by item.
- Continue after per-item failures unless blocked by policy.
- Never silently drop failed items.
- Retry via `RETRY: failures from <run_id>`.
- Stop or pause command takes effect between items.

## 11) Escalation Conditions

Pause and return to Rob immediately if:
- Identity mismatch risk appears.
- DNC ambiguity is unresolved.
- Prospect is likely duplicate with low-confidence match.
- Cadence date source is missing or contradictory.
- Any proposed action would modify existing records without explicit approval.

## 12) Quick Start Prompts

- `Run the daily in READ_ONLY, then give preflight + prioritized action list.`
- `Build Touch 2 drafts for all Day 4+ no-reply prospects, DRY_RUN only.`
- `Prepare Batch 10 preflight from [file], no drafts yet.`
- `Execute approved draft creation for listed names, do not send.`

