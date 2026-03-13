# Playbook: Apollo Enrollment

## When to Use
Whenever you need to create contacts in Apollo and enroll them in the TAM Outbound sequence (or any Apollo sequence).

---

## Sequence Details

| Field | Value |
|-------|-------|
| Sequence name | TAM Outbound - Rob Gorham |
| Sequence ID | `69afff8dc8897c0019b78c7e` |
| Emailer campaign ID | `69afff8dc8897c0019b78c7e` (same as sequence ID) |
| Send-from email account ID | `68e3b53ceaaf74001d36c206` (robert.gorham@testsigma.com) |
| Steps | 7 (all manual): email, email, LI connect, call, call, call, breakup email |
| Cadence | Day 1, 5, 10, 15, 21, 28, 35 |

---

## Step-by-Step Process

### 1. Create the Contact (if not already in Apollo)

```
Tool: apollo_contacts_create
Parameters:
  first_name: "Jason"
  last_name: "Lieberman"
  email: "jlieberman@epicor.com"
  title: "QA Manager"
  organization_name: "Epicor"
  present_raw_address: "Austin, TX"
  run_dedupe: true     ← CRITICAL: always true to prevent duplicates
```

**If the contact already exists:** Apollo returns the existing contact with `run_dedupe: true`. Check the response for `id` — you'll need it for enrollment. Also check `emailer_campaign_ids` — if the sequence ID is already there, they're already enrolled.

### 2. Verify the Contact Before Enrollment

Check the created/found contact for:
- `emailer_campaign_ids`: Must be empty (or not contain your target sequence). If it contains the sequence already, skip enrollment.
- `email_status`: "verified" is ideal. "extrapolated" works for catchall domains but note the risk.
- `email`: Confirm it matches what you expect. Apollo sometimes has stale data.

### 2b. Phase 2 Dedup — Re-Run Immediately Before This Call

Before calling `apollo_emailer_campaigns_add_contact_ids`, re-grep every contact name against MASTER_SENT_LIST:

```bash
for name in "Jason Lieberman" "Les Stickney" "Holly Shubaly"; do
  result=$(grep -i "$name" /Work/MASTER_SENT_LIST.csv)
  [ -n "$result" ] && echo "RACE CONFLICT — $name already logged, remove from batch" || echo "OK: $name"
done
```

**Why:** Another concurrent session may have enrolled the same contact between when you ran compliance gate (Phase 1) and when you're about to enroll. This check takes 5 seconds and prevents the most likely multi-session duplicate scenario.

If a contact is now found: remove them from `contact_ids`, post `[WARN]` in messages.md, continue with the rest.

### 3. Enroll in the Sequence

```
Tool: apollo_emailer_campaigns_add_contact_ids
Parameters:
  id: "69afff8dc8897c0019b78c7e"
  emailer_campaign_id: "69afff8dc8897c0019b78c7e"
  send_email_from_email_account_id: "68e3b53ceaaf74001d36c206"
  contact_ids: ["id1", "id2", "id3", "id4", "id5"]     ← MAX 5 per call
  sequence_same_company_in_same_campaign: true            ← allows multiple contacts per company
```

**HARD LIMIT: 5 contacts per enrollment API call.** If you have more than 5, batch them: 5 + 5 + remainder.

### 4. Verify Enrollment Succeeded

Check the API response for:
- `contacts`: Array of successfully enrolled contact objects
- `skipped_contact_ids`: Object mapping contact IDs to skip reasons. If non-empty, you have problems.

---

## Known Errors and Fixes

### Error: `contacts_active_in_other_campaigns`
**Cause:** Contact is enrolled in another Apollo sequence (even a dead/failed one).
**Fix:** Re-enroll with the override flag:
```
sequence_active_in_other_campaigns: true
```
**Real example:** Moiz Meer (Northern Trust) was in Shakeel's old sequence `6810e96760f685000de960d5` with status "failed" / "user_deleted". Apollo still treated it as "active." Adding the override flag in a separate API call fixed it (Session 26).

### Error: `contacts_without_ownership_permission`
**Cause:** The contact's `owner_id` in Apollo is null or belongs to another user, and your account doesn't have permission to enroll contacts you don't own.
**Fix:** This CANNOT be fixed via API. Rob must manually assign ownership in the Apollo UI:
1. Go to Apollo > Contacts > search for the contact
2. Click the contact to open their profile
3. Change "Owner" to Rob Gorham
4. Save
5. Then re-enroll via API
**Real example:** Yogesh Garg (Check Point) — `owner_id: null`, `creator_id: 655ecb6c164f6a00a3396e46` (not Rob). Permanently blocked until Rob manually reassigns ownership (Session 27).

### Error: `contacts_job_changed`
**Cause:** Apollo flagged the contact as having recently changed jobs.
**Fix:** Re-enroll with the override flag:
```
sequence_job_change: true
```
**Real example:** Des Keane and Hrishikesh Aradhye (YouTube) both required this override (Session 7).

### Error: `already_in_campaign`
**Cause:** Contact was already enrolled in this specific sequence (from a prior wave or manual enrollment).
**Fix:** No action needed. They're already enrolled. Confirm their step position and proceed.
**Real example:** L3Harris contacts L06-L09 (Stringer, Gates, Beloskur, Street) returned this in Wave 3 enrollment — they were pre-existing from Wave 1/2 (Session 18).

### Apollo Auto-Send Behavior
**Warning:** In rare cases, Apollo will auto-send the Step 1 email during enrollment instead of queuing a manual task. This happens unpredictably and cannot be prevented.
**Impact:** The contact skips straight to Step 2 without you pasting the custom T1 draft. They get Apollo's template (if one exists) or a blank send.
**Detection:** After enrollment, check the contact's `current_step_position`. If it's 2 instead of 1, Apollo auto-sent.
**Real examples:** Glen Hudson and Sibghatullah Veedy (Mastercard) both auto-sent during Wave 4 enrollment (Session 25). Both were updated in MASTER_SENT_LIST.csv and tracker HTML retroactively.
**Mitigation:** There is no reliable prevention. Monitor and update records if it happens. INC-009 documents this behavior.

---

## Pre-Enrollment Checklist (MANDATORY)

Before enrolling ANY contact:

1. **DEDUP:** Grep contact name against MASTER_SENT_LIST.csv. If found, STOP.
2. **DNC:** Check CLAUDE.md Do Not Contact list. If found, STOP.
3. **TAM verification:** Verify contact's company domain appears in `tam-accounts-mar26.csv`. If NOT found, do NOT enroll in TAM Outbound (per TAM-ONLY rule and INC-010).
4. **Email status:** Confirm email exists and is not marked "invalid" in Apollo.
5. **Existing sequence:** Check `emailer_campaign_ids` is empty or doesn't contain the target sequence.
6. **Same-company check:** If other contacts from the same company are already in the sequence, that's OK (use `sequence_same_company_in_same_campaign: true`), but note it for tracking.

---

## Post-Enrollment Checklist

After enrolling contacts:

1. **Log in MASTER_SENT_LIST.csv:** Add one row per contact (name, batch, date, channel, credits, file, norm).
2. **Update batch tracker HTML:** Set status badges to "Enrolled" or "T1 Pending".
3. **Update session-log.md:** Append enrollment details with Apollo contact IDs.
4. **Update handoff.md:** Add enrollment summary to relevant wave section.
5. **Leave message in messages.md:** `[CLAIM] Enrolled N contacts from {companies}. Do not re-prospect.`

---

---
*Version: 1.0 — 2026-03-12*
*Change log: v1.0 (Mar 12, 2026) — initial consolidation from Sessions 7, 18, 25, 26, 27*
*When updating: increment version, add change log entry with date and what changed.*
