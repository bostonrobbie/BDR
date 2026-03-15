# BDR Operational Safety Checklist

## Purpose
This checklist is run at the start of every Cowork session that involves outreach operations (drafting, sending, Apollo enrollment, Gmail operations). It catches errors before they reach prospects.

---

## Pre-Session Checklist (Run EVERY time before touching outreach)

### 1. Gmail Draft Audit
- [ ] Search Gmail drafts from all testsigma.com accounts
- [ ] For each draft found, verify:
  - [ ] Prospect exists in a batch tracker (no orphans)
  - [ ] Draft date is >= TOUCH_ELIGIBLE_DATE for that touch
  - [ ] Draft uses C2 message structure
  - [ ] Draft has passed QA Gate (MQS >= 9/12)
  - [ ] Draft subject follows naming convention: [READY]/[HOLD]/[SENT] + name + touch + date
- [ ] Flag and hold-tag any non-compliant drafts
- [ ] Report findings before proceeding

### 2. Cadence Integrity Check
- [ ] Read all active batch trackers
- [ ] Verify no prospect has a pending touch before their TOUCH_ELIGIBLE_DATE
- [ ] Verify no prospect has a missing touch (e.g., Touch 3 without Touch 2 sent)
- [ ] Flag any cadence violations

### 3. DNC List Check
- [ ] Read current DNC list from CLAUDE.md
- [ ] Verify no prospect in today's work queue is on the DNC list
- [ ] For any new prospects, check LinkedIn.com messaging history for prior hostile interactions

### 4. Credit Budget Check
- [ ] Check InMail credits remaining
- [ ] If < 10 credits: only Touch 2 for Hot/Warm prospects, email for rest
- [ ] If < 5 credits: no new Touch 1 InMails, focus on email and reply processing
- [ ] Report credit count

### 5. Template Version Check
- [ ] Confirm all message templates in use are C2 (current standard)
- [ ] Verify no C1 or pre-C2 templates are being referenced
- [ ] Check that all messages have the required elements: subject, opener question, context, proof point, "what day works" close

---

## Pre-Draft Checklist (Run before creating ANY draft)

### For Each Prospect:
- [ ] Prospect exists in a batch tracker with a unique ID
- [ ] `touch1_sent_date` is populated (confirms Touch 1 was sent)
- [ ] Today's date >= `touch[N]_eligible_date` for the touch being drafted
- [ ] Previous touch is confirmed SENT (no skipping)
- [ ] Research from all 3 sources logged (LinkedIn, Apollo, Company external)
- [ ] Proof point is DIFFERENT from previous touches
- [ ] Message passes QA Gate (14 checks, MQS >= 9/12)
- [ ] No HC violations (scan all 10 Hard Constraints)
- [ ] Close ties proof point outcome to prospect's situation + "what day works"
- [ ] Word count within range (Touch 1: 80-120, Touch 2: 40-70, Touch 3: 60-100)

---

## Pre-Send Checklist (Run before ANY send — InMail or Email)

### Identity Verification:
- [ ] Name on profile/email matches tracker exactly
- [ ] Title matches (note any changes)
- [ ] Company matches
- [ ] No "Messaged:" indicator in Sales Navigator (for InMail)
- [ ] LinkedIn.com messaging search shows no prior conversation
- [ ] Not on DNC list
- [ ] Not a known person / past coworker (Module A1)

### Content Verification:
- [ ] Message uses C2 structure
- [ ] MQS >= 9/12
- [ ] No HC violations
- [ ] Exactly 2 question marks (Touch 1) or 1-2 (Touch 2-3)
- [ ] Close is specific to this prospect (not generic)
- [ ] No placeholders remain ([Name], [Company], etc.)
- [ ] Proper paragraph spacing (4+ breaks for Touch 1)

### Cadence Verification:
- [ ] This is the correct touch number for this prospect
- [ ] Previous touch was sent and confirmed
- [ ] Today >= send date for this touch
- [ ] No out-of-sequence touches

### Approval:
- [ ] Rob has reviewed the message
- [ ] Rob has replied APPROVE SEND (for InMail sends)
- [ ] Or Rob has confirmed "send" for email batches

---

## Post-Send Checklist (Run after EACH send)

- [ ] Update tracker: status, dateSent, channel, conversationUrl
- [ ] Calculate and populate next touch eligible/send dates
- [ ] Verify send in Sales Navigator inbox (InMail) or Gmail sent folder (email)
- [ ] Log to cycle log if active session
- [ ] Check for any LinkedIn warnings or unusual behavior

---

## Weekly Review Checklist (Run once per week, ideally Monday)

- [ ] Count total sends by channel (InMail, Email) for the week
- [ ] Check reply rate trend (any decline signals deliverability issues)
- [ ] Review all batch trackers for orphan prospects or missing data
- [ ] Check InMail credit consumption rate vs remaining credits
- [ ] Audit any Gmail drafts that have been sitting > 3 days
- [ ] Verify DNC list is current
- [ ] Check for any prospects with overdue follow-ups (missed cadence)
- [ ] Review incident log for any new entries needed
- [ ] Update EXECUTION-STATUS.md with weekly metrics

---

## Error Escalation Protocol

| Error Type | Severity | Action |
|-----------|----------|--------|
| Premature draft/send (wrong touch order) | HIGH | STOP immediately. Log incident. Do not proceed until corrective action is documented. |
| Orphan prospect (no tracker entry) | HIGH | STOP. Add to tracker. Research before any further action. |
| HC violation in sent message | MEDIUM | Log. Cannot recall. Note for future template improvements. |
| Wrong prospect (identity mismatch) | CRITICAL | STOP. If sent, notify Rob immediately. May need apology message. |
| DNC contact messaged | CRITICAL | STOP. Log incident. If sent, flag for Rob — may need damage control. |
| LinkedIn warning/restriction | HIGH | STOP all LinkedIn activity. Follow Recovery Protocol in CLAUDE.md. |
| InMail credits exhausted | MEDIUM | Switch to email-only for remaining touches. Log credit depletion date. |
