# Workflow Notes for Rob
## Last Updated: March 6, 2026 (v2.1 — daily audit SOP added; Q1 Priority Accounts tracking gap documented)

---

## 1. Apollo — General Rules

- **Always use Apollo UI for sending emails.** The Apollo API can enrich contacts, create contacts, add them to sequences, and search data — but actual email SENDS must happen through the Apollo UI task queue. This ensures deliverability tracking, sequence advancement, and proper logging.
- **Use the Apollo browser UI** when the API can't provide the needed data (e.g., per-sequence contact counts, draft statuses, detailed step-level info, website visitor data).
- Key sequence: **Q1 Website Visitor - Tier 1 Intent** (ID: `69a1b3564fa5fa001152eb66`)
- Send email account: `robert.gorham@testsigma.net` (ID: `68f65bdf998c4c0015f3446a`)
- Your Apollo user ID: `68e16f05978e5e000d10a621`

---

## 2. Email Sending — The Rules

### ONLY Apollo UI Task Queue (effective March 1, 2026)

**DO:**
- Send all sequence emails by pasting personalized copy into Apollo tasks and clicking Complete
- Use Cowork/Claude to write the email copy in advance (save to markdown files)
- Verify sends in the Apollo sequence dashboard after each batch

**DO NOT:**
- Send sequence emails from Gmail compose
- Create Gmail API drafts for sequence emails
- Send from robert.gorham@testsigma.com for sequence emails (use testsigma.net via Apollo)

**Why:** Gmail sends don't register in the Apollo sequence. Contacts appear stuck at their current step. Deliverability tracking (opens, clicks, bounces) only works for Apollo-sent emails. The Feb 27 - Mar 1 workflow evolution proved this conclusively.

---

## 3. Qualification Checks — The 9-Point Checklist

Every prospect MUST pass ALL checks before being added to a sequence. No exceptions.

1. **Not already in Tier 1 sequence** — check `emailer_campaign_ids`
2. **Not in any other active sequence** — check `contact_campaign_statuses`
3. **Not Salesforce-owned by another BDR** — check both `owner_id` (Apollo) AND `crm_owner_id` (Salesforce)
4. **Email is verified** — check `email_status`; flag catchall domains
5. **Not a duplicate contact** — check `owner_id` matches yours
6. **Person still at company** — check `employment_history` + LinkedIn headline
7. **Not triple-sequenced** — count ALL active sequences; if 2+ active, do not add
8. **No prior appointment/warm status** — check `inactive_reason` for "scheduled appointment", "interested", "talked on phone"
9. **30-day cooldown** — if any sequence finished within last 30 days, skip

### Additional Data Points to Check
- `email_source`: if "emailer_message_outbound", contact was previously emailed from Apollo
- `contact_stage_id`: if not "New" (e.g., "Connected", "Attempted to Contact"), contact has been worked
- Custom fields: "Outbound_BDR", "Senthil_TAM_Oct24th_Valid", "Factors_BDRs", "Starwest_Raghava" etc. indicate prior campaigns

---

## 4. Territory & Ownership Rules

- Check BOTH `owner_id` (Apollo) AND `crm_owner_id` (Salesforce) — they can be different
- If a contact has a different owner in both Apollo and Salesforce, this is a HARD territory conflict. Do NOT email.
- If the contact is Rob-owned in Apollo but Salesforce shows another owner, investigate before sending.
- If `owner_id` is NULL (orphaned contact), check Salesforce CRM owner before proceeding.
- Account-level ownership (different from contact ownership) can indicate shared territory — check but not necessarily a blocker.

---

## 5. Warm Lead Handling

- **"talked on phone"** = WARM lead. Do not send generic cold sequence. Get call notes first; personalize messaging to acknowledge prior conversation.
- **"scheduled appointment" / "interested"** = HOT lead. Do NOT cold-sequence. This person had a meeting with someone at Testsigma. Coordinate with the original BDR.
- **"Connected" contact stage** = Has been worked. Review history before adding to any cold sequence.
- Prior BDR contacts (check custom fields like "Outbound_BDR", "Factors_BDRs") = previously emailed by another team member. Check engagement data before re-engaging.

---

## 6. Catchall Domains

22 catchall domains identified as of March 2, 2026. These accept any email address, so delivery is uncertain and email verification gives a false "verified" result.

**Monitor bounce rates closely for:**
veeva.com, redsailtechnologies.com, opploans.com, goodrx.com, flywire.com, bynder.com, drata.com, g2.com, medimpact.com, freedompay.com, csgi.com, cedargate.com, iteris.com, quickbase.com, connectwise.com, modmed.com, opsecsecurityonline.com, crestron.com, epicgames.com, origamirisk.com, sapiens.com, webmd.com, webmd.net, solera.com, theocc.com, virtru.com, cyberark.com, together.ai, qualified.com, silvaco.com, meetmarigold.com

---

## 7. Job Changes

- Apollo does NOT auto-update when someone leaves a company. The contact record stays stale.
- Always verify LinkedIn headlines for Director+ titles, especially before sending.
- If a job change is confirmed: STOP the contact in the sequence, find a replacement QA/Engineering leader at the original (visitor) company.
- Real examples from March 1: Harsha Navaratne (Interactions LLC → SoundHound AI), Laura Riley (Origami Risk → Ampersand).

---

## 8. Cowork/Claude Best Practices

### What Claude Can Do via API
- Enrich contacts (single + bulk up to 10)
- Create contacts with deduplication (`run_dedupe: true`)
- Add contacts to sequences
- Stop/remove contacts from sequences
- Search contacts and sequences
- Run all 9 qualification checks
- Audit existing sequence contacts for risk
- Search Slack for team context on flagged contacts
- Write personalized emails following SOP guidelines
- Update tracker files

### What Claude Cannot Do
- Send emails through Apollo UI (requires human in the browser)
- Access Apollo Website Visitor data directly (requires browser UI)
- Access Apollo task queue to paste emails (requires browser UI)
- Change Salesforce records directly
- Make territory conflict decisions (requires human judgment and team coordination)

### Session Start Checklist
When opening a new Cowork session:
1. Tell Claude: "Read the Master SOP at Tier1_Intent_Sequence_SOP_MASTER.md"
2. Provide today's prospect list (or ask Claude to pull from Apollo)
3. Ask Claude to run qualification checks
4. Ask Claude to write personalized emails for CLEAN contacts
5. You send via Apollo UI task queue
6. Ask Claude to update trackers

---

## 9. Key Audit Findings (March 1, 2026)

### Audit 1: Full Sequence (68 contacts)
- 36 CLEAN, 29 FLAG, 3 FAIL
- 3 FAIL resolved: Tim Wiseman (duplicate sequences stopped), Mazie Roxx (triple-sequence stopped), Harsha Navaratne (job change — stopped)
- 4 HIGH-RISK territory conflicts STOPPED: Jose Moreno, Todd Willms, Jenny Li, Jeff Barnes
- 4 MEDIUM-RISK cleared via Slack cross-reference: Eileen Zheng, Amir Aly, Luis Sanchez, Joe Pember
- 19 catchall domains flagged

### Audit 2: Extended Engagement (25 contacts)
- 12 CLEAN, 4 MINOR, 4 MODERATE, 5 CRITICAL
- 5 CRITICAL pending removal: Andy Roth (scheduled appointment with another BDR), Katie Hotard (triple-sequenced), Giang Hoang (triple-sequenced), Mark Freitag (finished 7-step sequence 18 days ago), Khalid Aziz (prior outbound + SF contact+lead)
- 4 MODERATE to monitor: Scott Carruth (ABM/TAM), Yuehli Dewolf (dual-sequenced), Rashad Fambro (SF CRM), Felix Tanh (prior outbound)

---

## 10. File Reference

| File | Purpose | Status |
|------|---------|--------|
| `Tier1_Intent_Sequence_SOP_MASTER.md` | **Single source of truth** for the Tier 1 sequence | CURRENT (v3.0) |
| `outreach_email_sop.md` | End-to-end email creation and send process | CURRENT (v2.0) |
| `daily_prospecting_workflow.md` | Daily workflow with time estimates | CURRENT (v2.0) |
| `workflow-notes.md` | This file — quick reference knowledge base | CURRENT (v2.0) |
| `tier1_sequence_audit_report.md` | Full sequence audit report (68 contacts) | REFERENCE |
| `BDR/data/trackers/engagement_audit_mar1.md` | Extended engagement audit (25 contacts) | REFERENCE |
| `prospect_master_tracker.md` | Running tracker of all prospects | ACTIVE |
| `email_outreach_tracker.csv` | Detailed outreach log | ACTIVE |
| `email_send_execution_plan.md` | Feb 28 execution plan | **ARCHIVED** (superseded by Apollo UI workflow) |
| `hyper_personalized_touch1_emails.md` | Email drafts for original contacts | REFERENCE |
| `touch1_batch2.md` through `touch1_batch6.md` | Batch email drafts | REFERENCE |
| `personalized_sequence_emails.md` | 3-touch personalized drafts for original 9 | REFERENCE |
