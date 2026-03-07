# Work Queue
## Last Updated: 2026-03-07

Tasks are sorted by priority. Claim one task at a time by updating status to IN_PROGRESS.

---

## 🔴 CRITICAL — Do First

### TASK-001: Draft Touch 2 Emails for Original 9 Feb 27 Contacts
**Status:** UNCLAIMED
**Priority:** P0 — 3 days overdue
**Effort:** ~45 min
**Output:** `touch2_drafts_feb27.md`

Draft Touch 2 follow-up emails for these 9 contacts (from the Q1 Website Visitor Tier 1 Intent sequence):
1. Andy Nelsen — QA Architect, Rightworks (anelsen@rightworks.com)
2. Jose Moreno — QA Architect, Flywire (jose.moreno@flywire.com)
3. Tom Yang — Director of Engineering, Versant Media (tom.yang@versantmedia.com)
4. Eyal Luxenburg — SW Engineering Manager, Island (eyal.luxenburg@island.io)
5. Hibatullah Ahmed — Engineering Manager, SPS Commerce (hahmed@spscommerce.com)
6. Jeff Barnes — Test Engineering Manager, Digi International (jeff.barnes@digi.com)
7. Eduardo Menezes — Sr QA Manager, Fulgent Genetics (emenezes@fulgentgenetics.com)
8. Todd Willms — Director of Engineering, Bynder (todd.willms@bynder.com)
9. Jason Ruan — Director of Engineering, Binance (jason.ruan@binance.com)

**Rules:**
- Touch 2 = 40-70 words, new angle, new proof point (NOT the same as Touch 1)
- Reference that you reached out before, but keep it light ("Circling back quick...")
- Close: lighter than Touch 1 but still ties to proof point outcome + "what day works"
- Follow C2 message structure and all HC rules
- QA Gate: MQS >= 9/12, no HC violations
- Check `personalized_sequence_emails.md` for what was used in Touch 1 for each person

---

### TASK-002: Draft Touch 2 InMails for INC-001 Batch 3 Contacts (4 people)
**Status:** UNCLAIMED
**Priority:** P0 — 2-3 days overdue
**Effort:** ~30 min
**Output:** `touch2_drafts_batch3_inmail.md`

These 4 contacts got a premature Touch 3 email on Feb 28 (INC-001). Per remediation plan, Touch 2 InMail proceeds as scheduled (treat premature email as an unplanned extra touch):
1. Irfan Syed — Progress Software (LinkedIn InMail, Touch 2)
2. Katie Barlow Hotard — Lucid Software (LinkedIn InMail, Touch 2)
3. Rachana Jagetia — Housecall Pro (LinkedIn InMail, Touch 2)
4. Giang Hoang — Employee Navigator (LinkedIn InMail, Touch 2)

**Reference:** Check `outreach-sent-feb26-batch3.html` for Touch 1 InMail content used for each.

---

### TASK-003: Gmail Draft Audit
**Status:** UNCLAIMED
**Priority:** P0 — compliance/safety
**Effort:** ~20 min
**Output:** Report in chat

Audit Gmail drafts from all testsigma.com accounts:
1. Verify the 46 Group A/B/C drafts still exist and are correctly named
2. Check for any orphan drafts (no tracker entry)
3. Check for any premature drafts (before eligible date)
4. Flag any drafts from the old 6 (Sergey, Mobin, Dino, Matthew, Joshua, Pete) — should have been deleted
5. Cross-reference the 16 Apollo Mar 1 sends — were their Gmail drafts deleted to avoid double-send?

---

## 🟡 HIGH — Do Soon

### TASK-004: Draft Touch 3 Emails for Batch 3 Contacts (24 people)
**Status:** UNCLAIMED
**Priority:** P1 — due TODAY (Mar 7) and tomorrow (Mar 8)
**Effort:** ~60 min
**Output:** `touch3_drafts_batch3.md`

Batch 3 Touch 1 was sent Feb 25-26. Touch 3 eligible Mar 6-7 (send Mar 7-8).
These are email Touch 3s — fresh approach, different proof point from both prior touches.
**Check:** `outreach-sent-feb26-batch3.html` for full prospect list and prior touch content.

---

### TASK-005: Draft Touch 2 Emails for 16 Apollo Mar 1 Sends
**Status:** UNCLAIMED
**Priority:** P1 — 1 day overdue
**Effort:** ~45 min
**Output:** `touch2_drafts_apollo_mar1.md`

These 16 contacts received Touch 1 from robert.gorham@testsigma.net on Mar 1 via Apollo task queue:
Scott Winzenread (DRB), Kunal Patel (aPriori), Jennifer Bieg (RealPage), Joel Brent (Kiddom), Alexander Tuaev (Convoso), Manu Jain (Iteris), Jennifer Marinas (ETAP), Rashad Fambro (MedeAnalytics), and 8 others from the Groups A/B/C list.

**Note:** Confirm which 16 were sent via Apollo before drafting — check Apollo task queue history or prospect_master_tracker.md notes.

---

### TASK-006: Send 46 Pending Gmail Drafts (Touch 1 — Groups A/B/C)
**Status:** UNCLAIMED (Rob must execute)
**Priority:** P1 — drafts have been sitting 6 days
**Effort:** Rob sends manually
**Output:** Update tracker with send dates

Rob needs to send the 46 Gmail drafts from Mar 1 (Groups A=13, B=8, C=25).
Before sending: confirm none of these contacts were already sent via Apollo (avoid double-send).
Drafts are in: `touch1_drafts_batch2.md` (A+B) and `touch1_drafts_batch2_groupC.md` (Group C).

---

### TASK-007: Draft Touch 2 Emails for Batch 9 Contacts (7 people)
**Status:** UNCLAIMED
**Priority:** P1 — 2 days overdue
**Effort:** ~20 min
**Output:** `touch2_drafts_batch9.md`

Batch 9 was sent Mar 2 via Apollo. Touch 2 due Mar 5 (2 days late).
These 7 contacts are in the Q1 Website Visitor sequence.
**Check:** `prospect_master_tracker.md` Section 6 or batch9 tracker for names.

---

## 🟢 NORMAL — Batch Prep

### TASK-008: Build Touch 2 Draft File for Batch 10 (53 contacts — due Mar 11)
**Status:** UNCLAIMED
**Priority:** P2 — eligible Mar 11, start prep Mar 10
**Effort:** ~120 min (large batch)
**Output:** `touch2_drafts_batch10.md`

53 contacts sent Touch 1 on Mar 7. Touch 2 eligible Mar 11 (Day 4), send Mar 12 (Day 5).
Do NOT start drafting until Mar 10 (per date-gating Rule 1 from CLAUDE.md).
**Reference:** `email_outreach_tracker.csv` rows 163-215 for all 53 contacts.

---

### TASK-009: New Outbound Batch (InMail) — When Credit Budget Allows
**Status:** UNCLAIMED
**Priority:** P3 — low credits (~24 remaining)
**Effort:** ~90 min
**Output:** New `outreach-sent-[date]-batch[N].html`

Only proceed when:
- Credits > 10
- Follow-up queue is light (< 10 overdue)
- Not a Monday

Source from Sales Navigator saved searches. Prospect Mix Ratio: 10-12 Manager/Lead, 4-6 Director, 3-5 Architect, 2-3 Buyer Intent, max 2 VP.

---

### TASK-010: Reply Inbox Scan
**Status:** UNCLAIMED
**Priority:** P2 — run at start of every "run the daily" session
**Effort:** ~10 min
**Output:** Reply summary in chat

Search Gmail for replies to robert.gorham@testsigma.com from all prospects.
Classify: Positive / Negative / Referral / Timing / Has Tool / Polite / Curiosity.
Draft responses per reply handling SOP (Section 13 of Tier1_Intent_Sequence_SOP_MASTER.md).

---

## ✅ COMPLETED

| Task | Completed | Notes |
|------|-----------|-------|
| Tier1_Intent_Sequence_SOP_MASTER.md Sections 11-13 | Mar 7 | Touch 2/3/Reply Handling |
| email_sequence_performance_audit_mar7.md | Mar 7 | 1.1% reply rate analysis |
| Batch 10 sends (53 contacts) | Mar 7 | Apollo task queue |
| email_outreach_tracker.csv update | Mar 7 | 215 rows through Batch 10 |
| prospect_master_tracker.md update | Mar 7 | All 121 contacts tracked |
| AGENTS.md created | Mar 7 | Multi-agent protocol |
| memory/session/handoff.md created | Mar 7 | Pipeline state snapshot |
| memory/session/work-queue.md created | Mar 7 | This file |

---

*Updated by Claude — 2026-03-07*
