# Apollo Enrollment — Skill

## Description
Creates contacts in Apollo and enrolls them in the TAM Outbound sequence. Handles all known edge cases: dedup, catchall domains, ownership errors, job change flags, contacts active in other campaigns, and Apollo's unpredictable auto-send behavior.

## Trigger
Use when you have a list of contacts ready to enroll in the TAM Outbound Apollo sequence. Usually called as part of the TAM T1 Batch workflow (Step 8).

## Prerequisites
- Read `memory/playbooks/apollo-enrollment.md` (full process with all error handling)
- **Run `skills/compliance-gate/SKILL.md` FIRST** — all 8 checks must pass before ANY contact is enrolled. This replaces the old 6-point dedup-protocol.md check and adds DNC, reply history, and cadence checks.
- All contacts must have passed the 8-point compliance gate
- All contacts must have TAM domain verification (domain in tam-accounts-mar26.csv)
- Batch tracker HTML must exist with contact details

## Key Parameters (from memory/apollo-config.md)

| Parameter | Value |
|-----------|-------|
| Sequence ID | `69afff8dc8897c0019b78c7e` |
| Emailer Campaign ID | `69afff8dc8897c0019b78c7e` |
| Send-from email account ID | `68e3b53ceaaf74001d36c206` |
| Send-from email address | robert.gorham@testsigma.com |
| Max contacts per API call | 5 |

## Process

### Step 1: Create Contacts (for those not already in Apollo)

For each contact NOT already in Apollo:
```
Tool: apollo_contacts_create
  first_name, last_name, email, title, organization_name, present_raw_address
  run_dedupe: true   ← ALWAYS
```

For contacts already in Apollo (found during dedup):
- Record their existing Apollo ID
- Check their `emailer_campaign_ids` — if already contains `69afff8dc8897c0019b78c7e`, skip enrollment

### Step 2: Batch Enrollment

Group contacts into batches of max 5. For each batch:
```
Tool: apollo_emailer_campaigns_add_contact_ids
  id: "69afff8dc8897c0019b78c7e"
  emailer_campaign_id: "69afff8dc8897c0019b78c7e"
  send_email_from_email_account_id: "68e3b53ceaaf74001d36c206"
  contact_ids: [up to 5 IDs]
  sequence_same_company_in_same_campaign: true
```

### Step 3: Handle Errors

Check response `skipped_contact_ids`. For each skip reason:

| Skip Reason | Action |
|-------------|--------|
| `contacts_active_in_other_campaigns` | Retry with `sequence_active_in_other_campaigns: true` in a SEPARATE call for just that contact |
| `contacts_without_ownership_permission` | CANNOT fix via API. Tell Rob to reassign ownership in Apollo UI manually. |
| `contacts_job_changed` | Retry with `sequence_job_change: true` |
| `already_in_campaign` | No action needed, already enrolled |

### Step 4: Verify Enrollment

For critical contacts, verify via:
```
Tool: apollo_contacts_search
  q_keywords: "{contact name}"
  per_page: 1
```
Check `emailer_campaign_ids` contains the sequence ID and `contact_campaign_statuses` shows `status: "active"`, `current_step_position: 1`.

### Step 5: Log

- Append rows to MASTER_SENT_LIST.csv: `name,batch,send_date,channel,credits,file,norm`
- Update batch tracker HTML badges: "Draft Ready" → "Enrolled"
- Append to session-log.md with all Apollo IDs
- Leave message in messages.md: `[CLAIM] Enrolled N contacts from {companies}`
- **Update `memory/contact-lifecycle.md`**: Add/update contact records with stage = ENROLLED, Apollo ID, and enrollment timestamp (per `skills/lifecycle-tracker/SKILL.md`)

## Error Handling
Full error catalog in `memory/playbooks/error-recovery.md` and `memory/playbooks/apollo-enrollment.md`.

## Watch For
- Apollo auto-send: After enrollment, check `current_step_position`. If 2 instead of 1, Apollo auto-sent the T1 email. Update records accordingly. (INC-009)
- Catchall domains: Note in tracker but proceed. See `memory/playbooks/catchall-domains.md`.
- Bounces: Monitor after send. If SMTP 550, remove from sequence and log.
