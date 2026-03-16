# Playbook: Error Recovery

## When to Use
When you encounter an error during any workflow. This playbook catalogs every error we've hit across 27 sessions, what caused it, and how to fix it.

---

## Apollo API Errors

### `contacts_active_in_other_campaigns`
**Where:** Enrollment API (`apollo_emailer_campaigns_add_contact_ids`)
**Cause:** Contact is in another Apollo sequence, even if that sequence is dead/failed/deleted.
**Fix:** Add `sequence_active_in_other_campaigns: true` to the enrollment call. Do this in a SEPARATE API call for just the affected contact(s), not the whole batch.
**Example:** Moiz Meer — old sequence `6810e96760f685000de960d5` with status "failed". Override worked. (Session 26)

### `contacts_without_ownership_permission`
**Where:** Enrollment API
**Cause:** Contact's `owner_id` is null or belongs to another team member.
**Fix:** CANNOT fix via API. Rob must manually reassign ownership in Apollo UI.
**Steps for Rob:** Apollo > Contacts > search contact > click to open > change Owner to Rob Gorham > Save.
**Example:** Yogesh Garg (Check Point) — `owner_id: null`. (Session 27)

### `contacts_job_changed`
**Where:** Enrollment API
**Cause:** Apollo detected the contact recently changed jobs.
**Fix:** Add `sequence_job_change: true` to the enrollment call.
**Example:** Des Keane, Hrishikesh Aradhye (YouTube). (Session 7)

### `already_in_campaign`
**Where:** Enrollment API
**Cause:** Contact is already in the target sequence.
**Fix:** No fix needed. This is informational. They're already enrolled. Verify their step position matches expectations.
**Example:** L3Harris contacts L06-L09. (Session 18)

### Apollo auto-send during enrollment
**Where:** After successful enrollment
**Cause:** Apollo sometimes auto-sends the Step 1 email during enrollment instead of creating a manual task. Unpredictable behavior.
**Detection:** Contact's `current_step_position` is 2 instead of 1 after enrollment.
**Impact:** They get Apollo's default template (or blank) instead of your custom draft.
**Fix:** Cannot undo. Update MASTER_SENT_LIST.csv and tracker HTML to reflect "T1 Sent (auto)" and move on.
**Example:** Glen Hudson, Sibghatullah Veedy (Mastercard). INC-009. (Session 25)

### Email bounce (SMTP 550)
**Where:** After sending via Apollo
**Cause:** Email address is invalid. Server permanently rejected it.
**Fix:** Remove contact from sequence. Re-enrich via Apollo/LinkedIn for a new email if the company is worth pursuing.
**Example:** Sucheth Ramgiri (Commvault) — sramgiri@commvault.com bounced. Both original and recovery email failed. (Sessions 11, 13)

### Email marked "invalid" in Apollo
**Where:** Apollo contact record, custom fields
**Cause:** Previous bounce or Apollo's email verification flagged the address.
**Detection:** Check `typed_custom_fields` for an "email_invalid" flag, or `email_true_status` for unusual values.
**Fix:** Skip the contact or re-enrich for a new email. Sending to a known-invalid address wastes sends and hurts sender score.
**Example:** Divya Sathish (EA) — email marked invalid in custom field, high bounce risk. (Session 25)

---

## Git Errors

### `index.lock` — Git lock file stuck
**Where:** Any git commit command
**Cause:** A previous git operation was interrupted (session crash, timeout), leaving a lock file.
**Error message:** `fatal: Unable to create '.git/index.lock': File exists.`
**Fix:** Rob must run from his terminal:
```bash
rm .git/index.lock
```
Then retry the git operation. Claude cannot delete this file from the VM.
**Example:** Session 26 — wave2 T2 drafts commit failed due to Windows filesystem index.lock.

### Cannot push (no GitHub auth)
**Where:** Any `git push` command
**Cause:** Claude's VM doesn't have GitHub credentials configured.
**Fix:** Not fixable from Claude's side. Rob must run `git push` from his terminal after each session. Claude should remind Rob at session end.
**Workaround:** Claude commits locally. Rob pushes. Multiple unpushed commits accumulate between pushes but this is fine.

---

## File System Errors

### File not found (uploaded file)
**Where:** Reading user-uploaded files
**Cause:** The file was uploaded in a previous session and the upload path has expired.
**Fix:** Ask Rob to re-upload the file, or check if a copy exists in `/sessions/practical-tender-pascal/mnt/Work/`.

### File too large for tool output
**Where:** Apollo API responses, large CSV reads
**Cause:** The response exceeds the MCP tool's output character limit.
**Fix:** Output is auto-saved to a temp file. Use bash/python to parse the temp file:
```bash
cat /path/to/saved/output.txt | python3 -c "import json,sys; data=json.load(sys.stdin); ..."
```

---

## Workflow Errors

### Double-send to same contact
**Where:** Sending outreach
**Cause:** Contact was already sent outreach via a different channel/batch and wasn't caught by dedup.
**Prevention:** Always run the full 6-point dedup (see `dedup-protocol.md`) before any send.
**Recovery:** Cannot unsend. Add contact to DNC or monitor list. Log as incident.
**Examples:** Chuck Smith (B1 + B5B), Rick Kowaleski, Christie Howard, Mohan Gummadi, Yassi Dastan.

### Non-TAM contact enrolled in TAM Outbound
**Where:** Enrollment step
**Cause:** Contact's company domain was not verified against tam-accounts-mar26.csv.
**Prevention:** Always run TAM domain verification (dedup-protocol.md Check 6) before enrollment.
**Recovery:** Remove contact from sequence using `apollo_emailer_campaigns_remove_or_stop_contact_ids`. Log as incident (INC-010 template).
**Example:** 5 contacts caught before enrollment in Session 27 (DocuSign, Bentley).

### Premature Touch 2/3 sent before cadence allows
**Where:** Follow-up drafting
**Cause:** Not checking the Touch 1 send date against the cadence rules.
**Prevention:** Touch 2 NOT before Day 4. Touch 3 NOT before Day 9. Always calculate from the T1 send date.
**Recovery:** Cannot unsend. Mark as "unplanned extra touch" in records and proceed with adjusted cadence.
**Example:** INC-001 — premature Touch 3 email sent to Batch 3 contacts on Feb 28.

---

## Incident Logging

When any error occurs that affects data quality or outreach integrity:
1. Check `memory/incidents.md` for the next incident number (INC-XXX)
2. Log the incident with: date, affected contacts, root cause, remediation, prevention rule
3. If a new prevention rule is needed, add it to the Rules section of incidents.md
4. Update relevant SOP files with the new safeguard

---

*Last updated: 2026-03-12 — consolidated from INC-001 through INC-010, Sessions 1-27*
