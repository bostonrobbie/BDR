# Playbook: Inbound Leads Sequence

## ⛔ SEND APPROVAL RULE — READ FIRST
**NEVER send any email from this sequence without Rob's explicit "APPROVE SEND."**
Claude's role is to draft, personalize, and prepare. Rob reviews and approves every message before it goes out. No exceptions — not for inbound leads, not for "warm" leads, not even if the email looks obviously good. If Rob has not said "APPROVE SEND" for a specific message to a specific contact in this session, do not send it.

---

## When to Use
When Salesforce assigns a new inbound lead to Rob, or when auditing prior inbound lead assignments that haven't been enrolled yet.

---

## Sequence Details

| Field | Value |
|-------|-------|
| Sequence name | Inbound Leads - Rob Gorham |
| Sequence ID | `69b2ae589d6bd10017d4be89` |
| Emailer campaign ID | `69b2ae589d6bd10017d4be89` (same as sequence ID) |
| Send-from email account ID | `68e3b53ceaaf74001d36c206` (robert.gorham@testsigma.com) |
| Steps | 3 (all MANUAL email) |
| Cadence | Day 1 (Touch 1), Day 4 (Touch 2), Day 7 (Touch 3) |

All steps are manual email — Apollo creates tasks for Rob to review. Nothing auto-sends.

---

## Part 1: Identifying Inbound Leads

### Lead Source
Leads come via Salesforce assignment emails sent to rgorham369@gmail.com (Rob's work Gmail) from internal team members:
- Murshid Ahmed
- Varun Prasath
- Ullas CR
- Talari Aparna

### Gmail Search Query
To find all assignments:
```
from:(murshid OR varun OR ullas OR talari) subject:"has been assigned to you"
```
Or search for: `"has been assigned to you"` in Gmail MCP.

### What to Ignore
Salesforce also sends LinkedIn suggestion emails with "has been assigned." These are NOT inbound leads — they are automated LinkedIn profile matches. Skip any email that mentions LinkedIn profile suggestions or lacks a company name in the subject line.

Valid assignment format: `"Lead: [Name], [Company] has been assigned to you"`

---

## Part 2: Lead Qualification Decision Tree

Before enrolling any lead, evaluate in this order:

### Step 1 — DNC Check
Cross-reference CLAUDE.md Do Not Contact list. If name/company matches, SKIP. Do not enroll, do not contact.

### Step 2 — Active Deal Check
Check if the lead's company has an active deal thread. If yes (e.g., an AE is already engaged, demo already happened), do NOT cold-sequence the contact. Flag for Rob — they may need a warm intro or coordinated outreach instead.

Example: Pranati Thankala at Aetna/CVS Health was correctly skipped because Tyler Kapeller (AE) has an active demo thread there.

### Step 3 — Contact Exists in Apollo?
Search Apollo contacts by name and/or company domain.
- If found: note the contact ID, check ownership (see Part 3).
- If not found: the contact needs to be created manually in Apollo UI before enrollment is possible. Flag for Rob.

### Step 4 — Persona Quality
| Tier | Titles | Action |
|------|--------|--------|
| High | QA Manager, QA Lead, Director/VP QA, SDET Lead, Automation Lead | Enroll immediately |
| Medium | Sr. QA Engineer, QA Engineer, QA Analyst | Enroll, note lower priority |
| Low | SDE, generic Engineer (no QA focus), non-technical | Flag for Rob's decision — they may not be worth the sequence slot |
| Skip | C-Suite with no buyer intent signal | Skip unless Factor account |

### Step 5 — Geography
US-based leads are standard. India-based, Portugal-based, or other non-US leads should be flagged — enroll only if Rob confirms. Testsigma has global customers but outreach cadence is US-focused.

---

## Part 3: Enrollment Process

### Ownership Permission Blocking
Apollo frequently blocks enrollment for contacts owned by other team members, even when `contacts_without_ownership_permission: true` is set. This is a known Apollo limitation (also seen in B10 audit Mar 7).

**Symptom:** API returns error on `contacts_without_ownership_permission` flag even with override set.

**Resolution options:**
1. Rob enrolls the contact manually through Apollo UI
2. Rob asks the contact owner to reassign ownership in Apollo
3. Rob asks ops/admin to bulk-reassign inbound lead ownership

Joe Casale (Lexia Learning, Sr. Director QA) hit this issue on Mar 12. He's a high-priority contact — flag for Rob immediately when this occurs.

### API Enrollment Call
```
Tool: apollo_emailer_campaigns_add_contact_ids
Parameters:
  id: "69b2ae589d6bd10017d4be89"
  emailer_campaign_id: "69b2ae589d6bd10017d4be89"
  send_email_from_email_account_id: "68e3b53ceaaf74001d36c206"
  contact_ids: ["<id1>", "<id2>", ...]
  sequence_no_email: true
  contacts_without_ownership_permission: true
  sequence_active_in_other_campaigns: true
  contact_verification_skipped: true
```

Use `sequence_no_email: true` unless Rob explicitly says to send immediately. Default is enroll only.

---

## Part 4: Before Sending Touch 1

### ⛔ Approval Required — No Exceptions
**Do NOT send any Touch 1 email without Rob's explicit "APPROVE SEND" for that specific contact.** Claude drafts and prepares. Rob reads, approves, and authorizes. Even if the email looks great, do not send until Rob says so. This rule has no exceptions.

**NEVER send Touch 1 from a generic sequence template.** The sequence templates contain placeholder copy that must be personalized per contact before any email goes out.

### Personalization Requirements
Each Touch 1 email must include:
- Opening hook tied to their specific role/company/tech stack (not just merge tags)
- Relevant proof point (customer story from a similar vertical or use case)
- One clear CTA — default is "What day works for a quick call?"
- Word count: 75–99 words sweet spot (39.0% reply rate)

### Pre-Send Checklist (INC-012 Rules — CRITICAL)
Once Rob has granted APPROVE SEND, before clicking "Send Now" in Apollo:
1. **JS readback:** `document.querySelector('.ql-editor').innerText.trim().slice(0, 120)` — must match the approved draft
2. **Zoom screenshot** of the body area — present to Rob
3. **Wait for Rob's explicit "looks good" / "send it"** — this is a second, separate gate from content APPROVE SEND
4. **After send:** verify via Gmail MCP within 60 seconds that the correct body landed

APPROVE SEND (content approval) ≠ APPROVE CLICK (send-button approval). Both gates are required every time.
Never use Quill API injection (dangerouslyPasteHTML, setText, setContents) — this caused INC-012.

See `memory/incidents.md` → INC-012, Rules 12-A through 12-E for full detail.

---

## Part 5: Touch Cadence Rules

| Touch | Day | Action |
|-------|-----|--------|
| Touch 1 | Day 1 | Personalized email. **Rob must APPROVE SEND before anything goes out.** |
| Touch 2 | Day 4 | Follow-up. Reference T1 angle, add new proof point. **Rob must APPROVE SEND before anything goes out.** |
| Touch 3 | Day 7 | Breakup / final ask. Keep short. **Rob must APPROVE SEND before anything goes out.** |

### Skip Rules
If Rob (or another team member) already sent a manual email outside the sequence to a contact:
- Skip the next scheduled sequence touch.
- Mark the Apollo task as "finished" without sending.
- The following touch is the first eligible re-contact.

Example: Evely Perrella (Mar 12) — INC-012 wrong-body send occurred, Rob sent his own manual follow-up. Touch 2 (Day 4, ~Mar 16) is SKIPPED. Touch 3 (~Mar 19) is first eligible re-contact.

---

## Part 6: Logging & Tracking

After every enrollment session, update `memory/pipeline-state.md` with:
- Date of enrollment
- Table of all enrolled contacts (name, company, contact ID, step, sent/not sent)
- Blocked contacts and reason
- Not-enrollable contacts and reason
- Note on whether any emails were sent

If any emails were sent, also update `MASTER_SENT_LIST.csv` with the send record.

---

## Part 7: Ongoing Monitoring

### When a New Lead Arrives
New inbound lead assignment emails come to Gmail. Check Gmail MCP at the start of each session for any new assignments. Don't let them pile up — enroll within 1–2 days of assignment.

### Apollo Task Queue
Once contacts are enrolled, Apollo's task queue will show pending manual email tasks. Check the queue regularly. Work tasks in order, personalizing each email before sending.

### Evely Perrella Edge Case
Evely is at Step 2 in the sequence. Touch 2 task (~Mar 16) must be SKIPPED (marked finished without sending). Touch 3 (~Mar 19) requires fresh personalization and Rob's APPROVE SEND.

---

## Known Issues & Gotchas

| Issue | Mitigation |
|-------|-----------|
| Ownership permission blocking | Flag for Rob manual UI enrollment or ownership reassign |
| Generic sequence templates | ALWAYS personalize per contact before sending — never send template copy as-is |
| INC-012 wrong-body send risk | Follow 4-step pre-send protocol every time, no exceptions |
| Aetna/CVS Health active deal | Pranati Thankala and the AE thread — don't cold-sequence any Aetna contact without checking first |
| India/non-US leads | Flag for Rob decision before enrolling |
| Contact not in Apollo | Can't enroll via API — needs manual contact creation first |

---

*Created: 2026-03-12 (Session — inbound lead bulk enrollment)*
