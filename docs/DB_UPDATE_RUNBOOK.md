# DB Update Runbook (Apollo + Local Channel DB)

## Purpose
Ensure every outreach action is recorded in both:
1. **Apollo** (sequence execution source of truth)
2. **Local channel DB** (internal analytics + audit)

This prevents sequence drift and reporting gaps.

## Channel Databases
- Email DB: `api/data/outreach_email.db`
- LinkedIn DB: `api/data/outreach_linkedin.db`

## Event → Required Updates

### 1) Draft Created
- Apollo: optional note/task comment if draft was prepared externally.
- Local DB:
  - upsert draft record
  - set state = `drafted`
  - append activity timeline event

### 2) Message Sent
- Apollo:
  - complete task/send action
  - verify contact progression or apply disposition
- Local DB:
  - upsert touch event with `channel`, `touch_number`, `state=sent`, `sent_at`
  - link to draft/message id
  - append activity timeline event

### 3) Reply Received
- Apollo:
  - tag/disposition contact
  - pause/stop sequence when needed
- Local DB:
  - insert reply row with intent/outcome
  - attribute to triggering touchpoint
  - update contact status/stage and timeline

### 4) Bounce/Failure
- Apollo:
  - mark failed/bounced and stop future sends as needed
- Local DB:
  - set touch/send state to `failed` or `bounced`
  - add suppression/do-not-contact indicator where applicable
  - append timeline event

### 5) Manual Stop / Disqualification
- Apollo:
  - stop sequence and add reason note
- Local DB:
  - set contact status to stopped/disqualified
  - write reason + timestamp + operator
  - append timeline event

## Minimum data keys to preserve
For every send/reply/failure action, preserve:
- contact id (+ email or linkedin_url)
- channel (`email` or `linkedin`)
- touch number
- message/draft id
- state
- timestamp
- operator/owner
- Apollo reference (task/sequence/disposition note)
- next action date

## End-of-Run Reconciliation
- Apollo sent count must match local DB sent touch count for the same window.
- Apollo stopped/paused contacts must match local DB status.
- Any mismatch must be logged as `sync_gap` and corrected before close.

## SOP Integration
- Email workflow: `memory/sop-email.md`
- LinkedIn workflow: `memory/sop-outreach.md`

Both SOPs require Apollo + local DB dual-update and reconciliation before run close.
