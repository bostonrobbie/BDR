# Work Queue
## Last Updated: 2026-03-15 (Session 39 — Batch 10 enrollment complete. 15/18 enrolled. TASK-040 added: APPROVE SEND for 15 contacts. TASK-041 added: T2 drafts due Mar 20-23. 3 blocked contacts need Rob manual Apollo UI fix.)

## ⚡ SESSION START PROTOCOL (read every time)
Follow the 14-step startup in `AGENTS.md` (v2.0). Key steps:
1. `git pull origin main`
2. Read AGENTS.md → CLAUDE.md → handoff.md → this file → in-progress.md → messages.md
3. Crash check (in-progress.md Status = ACTIVE → crash recovery)
4. Parallel check (ls `memory/session/active/` → avoid conflicts)
5. Register in `memory/session/active/{session-number}.json`
6. Check Gmail MCP for replies to robert.gorham@testsigma.com — warm leads jump the queue
7. Check warm-leads.md for overdue follow-ups
8. Read relevant playbooks from `memory/playbooks/` before starting work
9. **Start the new TAM T1 batch — this is the first priority every day**
10. After T1 batch work is done: check Apollo Tasks tab for T2s due

Tasks are sorted by priority. Claim one task at a time by updating status to IN_PROGRESS.

---

## 🔴 CRITICAL — Do First

### TASK-040: APPROVE SEND — Batch 10 (15 contacts enrolled, Mar 15)
**Status:** UNCLAIMED — waiting for Rob's APPROVE SEND
**Priority:** P0 — contacts enrolled, T1 tasks will appear in Apollo Tasks tab
**Effort:** ~25 min (paste 15 drafts from tracker into Apollo)
**Output:** 15 T1 emails sent via Apollo Tasks tab

All 15 contacts enrolled in TAM Outbound Step 1 (sequence 69afff8dc8897c0019b78c7e). When Apollo surfaces the manual email tasks:
1. **FIRST:** Attach avani.vaidya@cvshealth.com to Avani Vaidya's contact in Apollo UI (ID: 6904a84eea986d00191ba7f1)
2. Open Apollo Tasks tab
3. For each contact: paste subject + body from `batches/active/tamob-batch-20260315-1.html`
4. JS readback verify + screenshot before each send (INC-012 protocol)
5. Send Now
6. After all sends: Python badge update pass on tracker HTML

**Contacts:** Avani Vaidya, Swapna Bitra, Tarun Sharma, Divya Paul (CVS Health) | Usman Khan, Mehul Savalia (Citizens Bank) | Minu Prabhakaran, Jacob Wyman, Roger Tonneman (DISH) | Shikha Jayant, Collins Chellaswamy, Brendan McCarthy (D&B) | Dawn McCartha (EmblemHealth) | Stacey Schmidt (Vertafore) | Praveen Gali (Safelite)

**APPROVE SEND required before any sends**

---

### TASK-040B: Manual Apollo Fix — 3 Blocked Contacts (Batch 10)
**Status:** UNCLAIMED — Rob must manually enroll in Apollo UI
**Priority:** P1 — 3 contacts have drafts ready but couldn't be enrolled via API
**Effort:** ~5 min in Apollo UI

3 contacts silently rejected by Apollo API (contacts: [], skipped_contact_ids: {}) despite all override flags. Go to Apollo > Contacts > search each > open their profile > manually add to TAM Outbound sequence:

| Name | Company | Apollo ID | Email |
|------|---------|-----------|-------|
| Amaresh Shukla | BlackRock | 6915e0d2b283e9000160ffb8 | amaresh.shukla@blackrock.com |
| Colin Dwyer | EmblemHealth | 68e69f9eb4d410000123700c | cdwyer@emblemhealth.com |
| Deepa Pabbathi | Vertafore | 5f886aa5ef18ce008c0b797f | dpabbathi@vertafore.com |

Email drafts for all 3 are in `batches/active/tamob-batch-20260315-1.html`. After manual enrollment, update badges from Blocked → Enrolled and add to sends.

---

### TASK-041: Draft T2 Emails — Batch 10 (15 contacts, due Mar 20-23)
**Status:** UNCLAIMED
**Priority:** P1 — T2 due Mar 20-23 (Day 5-8 from T1 send)
**Effort:** ~45 min
**Output:** T2 drafts added to `batches/active/tamob-batch-20260315-1.html` or separate T2 file

15 contacts from Batch 10. T2 tasks will appear in Apollo Tasks tab ~Mar 20.
**Formula:** sop-tam-outbound.md Part 7 (Deep-Dive v4) — 140-190 words, 4-part: (1) "I imagine" + deeper pain, (2) Testsigma pitch, (3) customer story with WHY, (4) 15-min CTA. BANNED: "Circling back" / "Following up." See `memory/playbooks/t2-followup.md`.
**Check T1 proof points:** `batches/active/tamob-batch-20260315-1.html` (proof point rotation table)
**APPROVE SEND required before any sends**

**Accounts:** CVS Health (4), Citizens Bank (2), DISH Network (3), D&B (3), EmblemHealth (1), Vertafore (1), Safelite (1)

---

### TASK-033: Call Back TELUS Contacts TODAY — 3 Missed Inbound Calls
**Status:** UNCLAIMED — Rob must call back
**Priority:** P0 — inbound calls from active prospects
**Date Added:** 2026-03-13 (reply-classifier scheduled run)

3 TELUS contacts called Rob's Apollo dialer and got no answer. Call back ASAP:

| Priority | Name | Title | Phone | Calls | When |
|----------|------|-------|-------|-------|------|
| 1st | Krystal Jackson-Lennon | Manager, Technology Strategy/SRE/Perf Eng | +1 416-906-2317 | ×4 | Mar 12 3:55-3:56 PM |
| 2nd | Mike Brown | Quality Assurance Manager | +1 604-999-8592 | ×2 | Mar 11 3:25-3:40 PM |
| 3rd | Rajesh Ranjan | Engineering Manager | +1 647-936-7954 | ×1 | Mar 11 3:00 PM |

**Talk track:** Performance engineering + test automation at scale. Krystal is SRE/performance focused — lead with flaky tests / performance test automation angle.
**After call:** Update warm-leads.md + contact-lifecycle.md with outcome. If positive: add MEETING_BOOKED row.
**Note:** All 3 from same TELUS account — coordinate messaging so they don't feel siloed. Consider telling each you're talking to their colleagues.

---

### TASK-034: Fix Bounce Cluster — EA, Humana, Mastercard, Others
**Status:** UNCLAIMED
**Priority:** P1 — multiple contacts unreachable
**Date Added:** 2026-03-13 (reply-classifier scheduled run)

Bounce summary from Mar 11-12 sends:

| Contact | Company | Email (bounced) | Action |
|---------|---------|-----------------|--------|
| Clifton Wilcox | EA | clifton@ea.com | Re-source via Sales Nav — @ea.com format invalid |
| Simon Crawford | EA | simon.crawford@ea.com | Re-source or skip |
| Divya Sathish | EA | divya.sathish@ea.com | Already flagged in TASK-021 |
| Jiadong Shen | EA | jiadong.shen@ea.com | Already flagged in TASK-021 |
| Janel Jolly | EA | janel.jolly@ea.com | Re-source |
| William Xie | EA | william.xie@ea.com | Re-source |
| Sabrina Perry | EverBank | sabrina.perry@everbank.com | SPAM BLOCKED (not a bounce) — EverBank blocks external senders. May need LinkedIn outreach instead. VP QA = high value. |
| Zahidh Zubair | Citizens Bank | zahidh.zubair@citizensaccess.com | Apollo shows @citizensaccess.com but bounce to @citizensbank.com — verify which domain |
| David Schraff | Cleveland Clinic | schraffd@ccf.org | Bounced — re-source or try alternate |
| salam6@humana.com | Humana | Bad format email | Skip — email pattern invalid |
| sgangyshetty@humana.com | Humana | Bad format | Skip |
| ahmet.cakar@humana.com | Humana | Bounced | Re-source |
| koushal.ram@mastercard.com | Mastercard | SMTP 550 | Already flagged — skip or re-source |
| kshchelkonogova@mastercard.com | Mastercard | SMTP 550 | Already flagged in TASK-021 (Ksenia Shchelkonogova) |
| r.soto@cash.app | Cash.App/Block | Bounced | Re-source |
| jessica.harris@onemainfinancial.com | OneMain Financial | Bounced | Re-source |
| mseal@draftkings.com | DraftKings | Bounced | Re-source |

**EA Note:** 6 EA bounces suggests @ea.com domain doesn't accept email at these addresses. May need Sales Nav InMail for EA contacts instead of email. Reference: Yu Jin + Maalika Tadinada (from Wave 2, yjin@ea.com/mtadinada@ea.com) — check if those bounced too.

**Sabrina Perry note:** VP QA at EverBank is high value but email is blocked at the network level. Recommend LinkedIn InMail as alternative channel.

---

### TASK-021: Enroll + Send Wave 4 T1 (48 contacts)
**Status:** ✅ DONE (2026-03-11, Sessions 22-25)
**Result:** 37/48 T1 emails sent (35 via Tasks tab + 2 auto-sent by Apollo). QA gate passed on every manual send.
**MASTER_SENT_LIST.csv:** 37 rows added (412 total). tamob-batch-20260311-2.html: 37 T1SentMar11, 2 Blocked, 9 Ready.

**11 no-task contacts — RESOLVED (Session 25):**
- ✅ Glen Hudson (Mastercard) — T1 auto-sent during enrollment (step 2). CSV + HTML updated.
- ✅ Sibghatullah Veedy (Mastercard) — T1 auto-sent during enrollment (step 2). CSV + HTML updated.
- ⛔ Ksenia Shchelkonogova (Mastercard) — email bounced (invalid). Skip permanently.
- ⚠️ Divya Sathish (EA) — enrolled, step 1 pending, email marked "invalid" — watch for bounce when task surfaces.
- ⏳ 8 others (Irina Baxter, Jiadong Shen, Simon Crawford, Adit Shah, Mohan Raj, Shilendra Sharma, Poonam Patil + Divya Sathish) — enrolled, Step 1 tasks queued in Apollo, will surface. Send normally when they appear.

**Still need Rob action:**
- 🚫 Valerie Jefferies (BCBS Illinois) — blocked: job change flag. Re-enrich or skip.
- 🚫 Yvonne Oliver (Mastercard) — blocked: ownership error. LinkedIn InMail alternative?

**Wave 4 T2 due:** Mar 19 (Day 8 from Mar 11 send) — add TASK-022 when ready to draft.

### TASK-023: Send Wave 5 Batch 4 T1 Emails (9 contacts — pending APPROVE SEND)
**Status:** UNCLAIMED — waiting for Rob's APPROVE SEND
**Priority:** P0 — contacts enrolled, T1 tasks will appear in Apollo Tasks tab
**Effort:** ~15 min (paste drafts from tracker into Apollo)
**Output:** 9 T1 emails sent via Apollo Tasks tab

All 9 contacts enrolled in TAM Outbound Step 1. When Apollo surfaces the manual email tasks:
1. Open Apollo Tasks tab
2. For each contact: paste subject + body from `tamob-batch-20260312-4.html`
3. Send Now
4. Update tracker HTML badges to "T1 Sent"
5. MASTER_SENT_LIST.csv already updated (420 rows)

**Contacts:** Jason Lieberman (Epicor), Les Stickney (Epicor), Holly Shubaly (BeyondTrust), Tony MacLean (BeyondTrust), Michael Sutherland (BeyondTrust), Theepa Balakrishnan (BeyondTrust), Alnis Cers (Northern Trust), Moiz Meer (Northern Trust), Padma Suresh (Northern Trust)

**APPROVE SEND required before any sends**

### TASK-025: Send Batch 5 T1 Emails (5 contacts — pending APPROVE SEND)
**Status:** UNCLAIMED — waiting for Rob's APPROVE SEND
**Priority:** P0 — contacts enrolled, T1 tasks will appear in Apollo Tasks tab
**Effort:** ~10 min (paste drafts from tracker into Apollo)
**Output:** 5 T1 emails sent via Apollo Tasks tab

5 contacts from Batch 5 enrolled in TAM Outbound Step 1. When Apollo surfaces the manual email tasks:
1. Open Apollo Tasks tab
2. For each contact: paste subject + body from `tamob-batch-20260312-4.html`
3. Send Now
4. Update tracker HTML badges to "T1 Sent"
5. Update MASTER_SENT_LIST.csv with send rows

**Contacts:** (from Infor/Zebra/Check Point/FactSet — see tamob-batch-20260312-4.html Batch 5 section)

**Yogesh Garg (Check Point):** NOT enrolled — ownership blocked. Rob must assign ownership in Apollo UI first. After ownership fixed, enroll + add to this send batch.

**APPROVE SEND required before any sends**

### TASK-026: TAM-Only Enforcement — Ongoing
**Status:** ✅ DONE (2026-03-12, Session 27) — SOPs updated, audit complete
**Priority:** P0 — compliance
**What was done:**
- Audited TAM Outbound sequence: CLEAN (no non-TAM contacts enrolled)
- Added Pre-Enrollment Domain Verification Gate to sop-tam-outbound.md Part 11
- Added Factor Account Prioritization to target-accounts.md
- Updated CLAUDE.md operating directive with TAM-ONLY RULE
- Logged INC-010 in incidents.md (5 non-TAM contacts caught before enrollment)
- Added Rule 8 (Pre-Enrollment Domain Verification) to incidents.md

### TASK-024: Draft T2 Emails — Wave 5 Batch 4 (9 contacts, due ~Mar 19-20)
**Status:** UNCLAIMED
**Priority:** P1 — T2 due ~Mar 19-20 (Day 5-8 from T1 send)
**Effort:** ~30 min
**Output:** T2 drafts added to `tamob-batch-20260312-4.html` or separate file

9 contacts from Wave 5 Batch 4. T2 tasks will appear in Apollo ~Day 5 from T1 send.
**Formula:** sop-tam-outbound.md Part 7 (Deep-Dive v4, locked Mar 12) — 140-190 words, 4-part: "I imagine" pain + Testsigma pitch + customer story + 15-min CTA. BANNED: "Circling back" / "Following up." See `memory/playbooks/t2-followup.md` for full formula + reference example.
**Check T1 proof points:** `tamob-batch-20260312-4.html` (9 contact T1 drafts)
**APPROVE SEND required before any sends**

### TASK-036: Draft T2 Emails — Batch 9 (44 contacts, due Mar 18-21)
**Status:** UNCLAIMED
**Priority:** P1 — T2 due Mar 18-21 (Day 5-8 from Mar 14 T1 send)
**Effort:** ~120 min (large batch, 14 accounts)
**Output:** `tamob-batch9-t2-drafts-mar18.html`

44 contacts sent T1 on Mar 14 (45 enrolled, Bret Wiener DNC skipped). T2 tasks will appear in Apollo Tasks tab ~Mar 18-19.
**Formula:** sop-tam-outbound.md Part 7 (Deep-Dive v4) — 140-190 words, 4-part: (1) "I imagine" + deeper pain, (2) Testsigma solution pitch, (3) customer story with WHY, (4) 15-min CTA. BANNED: "Circling back" / "Following up." See `memory/playbooks/t2-followup.md`.
**Check T1 proof points:** `tamob-batch-20260313-2.html` (45 contact T1 drafts — use different proof point per contact)
**Send via:** Apollo UI → INC-012 protocol
**APPROVE SEND required before any sends**

**Accounts:** SailPoint(4), Farmers Insurance(5), Bethesda Softworks(5), hims&hers(3), Rocket Software(5), Lemonade(1), Zimmer Biomet(2), Anaplan(6), Bungie(2), Celonis(2), Check Point(2), DraftKings(4), Zebra Technologies(4)

---

### TASK-035: Draft T2 Emails — Batch 8 (55 contacts, due Mar 18)
**Status:** UNCLAIMED
**Priority:** P1 — T2 due Mar 18 (Day 5 from Mar 13 T1 send)
**Effort:** ~120-180 min (large batch, 14 accounts)
**Output:** `tamob-batch8-t2-drafts-mar18.html`

55 contacts enrolled in TAM Outbound Mar 13. T1 sent Mar 13. T2 tasks will appear in Apollo Tasks tab ~Mar 17-18.
**Formula:** sop-tam-outbound.md Part 7 (Deep-Dive v4, locked Mar 12) — 140-190 words, 4-part: (1) "I imagine" + deeper pain, (2) Testsigma solution pitch, (3) customer story with WHY, (4) 15-min CTA. BANNED: "Circling back" / "Following up." See `memory/playbooks/t2-followup.md` for full formula + reference example.
**Check T1 proof points:** `tamob-batch-20260313-1.html` (55 contact T1 drafts — use different proof point per contact)
**Send via:** Apollo UI → INC-012 protocol (JS insertText body, subject correction, readback verify, Send Now)
**APPROVE SEND required before any sends**

**Accounts:** WatchGuard (7), Everbridge (7), Procore (2), Pluralsight (4), Sysdig (3), Yext (3), SingleStore (1), Evernorth (3), Couchbase (4), Pathlock (5), Tandem Diabetes Care (5), Jack Henry (4), BMO Financial Group (5), Point32Health (2)
**Note:** Monika Sharma (#15, Everbridge) was skipped — do NOT draft T2 for her.

---

### TASK-022: Draft T2 Emails — Wave 4 (35 contacts, due Mar 19)
**Status:** UNCLAIMED
**Priority:** P1 — T2 due Mar 19 (Day 8 from Mar 11 T1 send)
**Effort:** ~120 min (large batch, 19 companies)
**Output:** `tamob-wave4-t2-drafts-mar19.html`

35 contacts enrolled in TAM Outbound Mar 11. T2 tasks will appear in Apollo Tasks tab ~Mar 18-19.
When Apollo surfaces them → draft + send per t2-followup.md playbook.
**Formula:** sop-tam-outbound.md Part 7 (Deep-Dive v4, locked Mar 12) — 140-190 words, 4-part: "I imagine" pain + Testsigma pitch + customer story + 15-min CTA. BANNED: "Circling back" / "Following up." See `memory/playbooks/t2-followup.md` for full formula + reference example.
**Check T1 proof points:** `tamob-batch-20260311-2.html` (35 contact T1 drafts with subjects + bodies)
**Send via:** Apollo UI (Part 23 of sop-tam-outbound.md v3.1) → manually paste → Send Now
**APPROVE SEND required before any sends**


### TASK-001: Draft Touch 2 Emails for Original 9 Feb 27 Contacts
**Status:** DONE (2026-03-07)
**Priority:** P0 — 3 days overdue
**Effort:** ~45 min
**Output:** `touch2_drafts_feb27.md` ✅ CREATED

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
**Status:** DONE (2026-03-07)
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

### TASK-020: Draft T2 Emails — Wave 3 (35 contacts, due Mar 16)
**Status:** UNCLAIMED
**Priority:** P1 — T2 due Mar 16 (Day 5 from Mar 11 T1 send)
**Effort:** ~120 min (large batch, 7 accounts)
**Output:** `tamob-wave3-t2-drafts-mar16.html`

35 contacts enrolled in TAM Outbound Mar 11. T2 tasks will appear in Apollo Tasks tab ~Mar 15-16.
When Apollo surfaces them → draft + send per t2-followup.md playbook.
**Formula:** sop-tam-outbound.md Part 7 (Deep-Dive v4, locked Mar 12) — 140-190 words, 4-part: "I imagine" pain + Testsigma pitch + customer story + 15-min CTA. BANNED: "Circling back" / "Following up." See `memory/playbooks/t2-followup.md` for full formula + reference example.
**Check T1 proof points:** `tamob-batch-20260311-1.html` (35 contact T1 drafts with subjects + bodies)
**Send via:** Apollo UI (Part 23 of sop-tam-outbound.md v3.1) → manually paste → Send Now
**APPROVE SEND required before any sends**

---

### TASK-018: Remove Sucheth Ramgiri from TAM Outbound Sequence + Re-enrich Email
**Status:** UNCLAIMED
**Priority:** P1
**Effort:** ~10 min
Sucheth Ramgiri (Commvault) hard-bounced — sramgiri@commvault.com is invalid (SMTP 550 5.1.10). Both the original placeholder T1 and recovery email failed. Remove from Apollo TAM Outbound sequence. Re-enrich via Apollo/LinkedIn if Commvault is still worth pursuing.

---

### TASK-017: Draft T2 Emails — Wave 1 (23) + Wave 2 (13)
**Status:** 🔴 URGENT — Wave 1 T2 due Mar 12. Wave 2 T2 OVERDUE (due Mar 15, now Mar 11). Check Apollo Tasks tab immediately next session.
**Priority:** P0 — Wave 1 T2 tasks should now be visible in Apollo. Do FIRST next session.
**Effort:** ~90 min for Wave 1, ~50 min for Wave 2 (templates are similar, batch together)
**Output:** `tamob-wave1-t2-drafts-mar12.html` and `tamob-wave2-t2-drafts-mar11.html`

**When to do this:** Open Apollo Tasks tab → when T2 tasks appear as due, THEN draft + send.
**Formula:** sop-tam-outbound.md Part 7 (Deep-Dive v4, locked Mar 12) — 140-190 words, 4-part: (1) "I imagine" + deeper pain, (2) Testsigma solution pitch, (3) customer story with WHY, (4) 15-min CTA. BANNED: "Circling back" / "Following up" / "One more angle." See `memory/playbooks/t2-followup.md` for full formula + QA gate + reference example.
**Check T1 proof points:** tamob-wave1-draft-mar10.html / tamob-wave2-draft-mar10.html (no repeat per contact)
**Send via:** Apollo UI (Part 23 of sop-tam-outbound.md v3.1) → manually paste subject + body → Send Now → Apollo marks Done and auto-advances automatically
**APPROVE SEND required before any sends**

---

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

### TASK-019: Crash-Recovery Infrastructure
**Status:** DONE (2026-03-11, Session 15)
**Priority:** P0 — infrastructure, unblocks all future sessions
**Effort:** ~30 min
**Output:** `memory/session/in-progress.md` ✅ CREATED; `AGENTS.md` ✅ UPDATED

Built persistent crash-recovery system:
1. `memory/session/in-progress.md` — checkpoint file. Write ACTIVE at task start, check off steps mid-task, set CLEAR on task end. Includes template + crash recovery protocol.
2. `AGENTS.md` updated — Step 6 reads in-progress.md; full Crash Recovery Protocol section; Mid-Session Commit Protocol (mandatory commit after each file creation, every 5 contacts drafted, every memory/ file update).
3. `work-queue.md` TASK-017 updated to DEFERRED per Rob (T2 drafts tackled when Apollo surfaces them).

**Next session startup note:** AGENTS.md Step 6 now reads in-progress.md. If Status = ACTIVE on startup = crash was detected — follow crash recovery protocol before doing anything else.

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
| touch2_drafts_feb27.md | Mar 7 | 9 Touch 2 emails for Feb 27 contacts, all MQS 10-12/12 |
| touch2_drafts_batch3_inmail.md | Mar 7 | 4 Touch 2 InMails for INC-001 Batch 3 (Irfan, Katie, Rachana, Giang). MQS 11, 10, 12, 12. All READY TO SEND. |
| TAM Outbound - Rob Gorham sequence built | Mar 10 | Apollo ID: 69afff8dc8897c0019b78c7e. 7 steps all manual, Day 1/5/10/15/21/28/35. email→email→LI connect→call→call→call→breakup email. Ready for enrollment. |
| Tyler Referrals T1 — all 7 sent | Mar 10 (Session 8) | 6 emails (Gopi/Staples, Pranati/Aetna, Roy/Sandia, Devin/FCB, Jason B/FCB, Skie/FCB) + 1 InMail (Vernon Bryant/Tractor Supply). T2 due Mar 14. File: tyler-referrals-outreach-mar10.html |
| TASK-019: Crash-recovery infrastructure | Mar 11 (Session 15) | Created in-progress.md checkpoint system. Updated AGENTS.md with mid-session commit protocol + crash recovery startup rules. T2 sends for TAMOB Wave 1/2 deferred to natural Apollo task cadence per Rob. |
| TASK-026: TAM-Only Enforcement | Mar 12 (Session 27) | SOPs updated, audit complete, no non-TAM contacts in live sequence |
| TASK-031: Comprehensive Audit + SOP Hardening | Mar 12 (Session 31) | 8 audit findings, 5 files updated (AGENTS.md v2.1, dedup-protocol.md, session-handoff.md, tam-t1-batch SKILL.md, messages.md). Handoff.md brought current. |

---

### TASK-011: Prospect Wave 1 Factor Enterprise Accounts
**Status:** DONE (Mar 10, Sessions 4-7) — 23 enrolled, 4 on HOLD, T1 drafts PENDING in TASK-014
**Priority:** P1 — sequence is ready, accounts are identified
**Effort:** ~90 min
**Output:** `wave1-batch1-tracker-mar10.html` ✅ + 23 contacts enrolled in TAM Outbound

---

### TASK-012: Revise sop-outreach.md — Enterprise Email-Only T1 Formula
**Status:** DONE (Mar 10)
**Priority:** P2 — needed before Wave 1 T1 drafts are written
**Effort:** ~30 min
**Output:** New section in `memory/sop-outreach.md` ✅ ADDED

Added:
- Enterprise email-only T1 formula (HC1 intro, SMYKM subject, challenge-narrative structure, word limit 75-100)
- A+ research protocol (7-step research process for Fortune 500/enterprise contacts — job postings, engineering blog, recent news, Glassdoor signal)
- Research quality thresholds by account type

---

### TASK-013: Build TAM Outbound SOP / Skill
**Status:** DONE (Mar 10)
**Priority:** P1 — needed for Wave 1 execution and all future TAM waves
**Effort:** ~90 min
**Output:** `memory/sop-tam-outbound.md` ✅ CREATED

Built full end-to-end SOP covering:
- Wave architecture (Factor Wave 1 → Non-Factor Wave 2+)
- Account selection from tam-coverage-tracker.csv
- Contact identification via Apollo + Sales Nav
- Dedup protocol (MASTER_SENT_LIST + DNC + Apollo + Gmail)
- A+ research protocol (17 parts total)
- T1 decision tree (InMail vs. email)
- Enterprise email T1 formula
- T2 + breakup email rules
- Batch tracker format
- Apollo enrollment (TAM Outbound sequence)
- Follow-up loop
- Wave 1 current state (4/6 ready to send, 2 flagged)
- Proof point vertical matching table

---

### TASK-016: TAM Outbound Wave 2 — Enroll + Send T1 (16 contacts)
**Status:** DONE (Mar 10, Session 10)
**Priority:** P1 — drafts complete, ready to execute
**Effort:** ~60 min (Apollo enrollment + Apollo email sends)
**Output:** Wave 2 contacts enrolled in TAM Outbound; T1 sends logged in MASTER_SENT_LIST.csv

16 T1 email drafts complete in `tamob-wave2-draft-mar10.html`. All deduped clean. All QA-scored.

**Send order:** HIGH first → MED → LOW (skip HashiCorp if credits are tight)

| # | Name | Company | Email | Priority | MQS |
|---|------|---------|-------|----------|-----|
| 1 | Saeyed Shamlou | OneMain | saeyed.shamlou@omf.com | HIGH | 12/12 |
| 2 | Marcela Fetters | GEICO | mfetters@geico.com | HIGH | 11/12 |
| 3 | Chandni Jain | Checkr | chandni.jain@checkr.com | HIGH | 11/12 |
| 4 | Sarah Kneedler | Checkr | sarah.kneedler@checkr.com | HIGH | 11/12 |
| 5 | Richelle Paulsen | Cetera | richelle.paulsen@cetera.com | HIGH | 11/12 |
| 6 | Karen Teng | Mindbody | karen.teng@mindbodyonline.com | HIGH | 11/12 |
| 7 | Roberto Bouza | GEICO | rbouza@geico.com | MED | 10/12 |
| 8 | Sambhav Taneja | GEICO | sambhav_taneja@geico.com | MED | 10/12 |
| 9 | Krista Moroder | Checkr | krista.moroder@checkr.com | MED | 10/12 |
| 10 | Cristian Brotto | Checkr | cristian.brotto@checkr.com | MED | 10/12 |
| 11 | Yu Jin | EA | yjin@ea.com | MED | 10/12 |
| 12 | Maalika Tadinada | EA | mtadinada@ea.com | MED | 10/12 |
| 13 | Anton Aleksandrov | Cetera | anton.aleksandrov@cetera.com | MED | 10/12 |
| 14 | Henry Rose | Mindbody | henry.rose@mindbodyonline.com | MED | 10/12 |
| 15 | Bipin Bhoite | Mindbody | bipin.bhoite@mindbodyonline.com | MED | 10/12 |
| 16 | Shyamendra Singh | HashiCorp | shyamendra.singh@hashicorp.com | LOW | 9/12 |

**Steps after APPROVE SEND:**
1. Create Apollo contacts for any not yet in system
2. Enroll all 16 in TAM Outbound - Rob Gorham (69afff8dc8897c0019b78c7e) via robert.gorham@testsigma.com
3. Send T1 emails via Apollo UI (copy from tracker)
4. Log all 16 rows in MASTER_SENT_LIST.csv
5. Update tamob-wave2-draft-mar10.html: T1 Sent status + date
6. T2 due Day 5 from send date

---

### TASK-015: Tyler Referrals T2 — Draft + Send (7 contacts, due Mar 14)
**Status:** UNCLAIMED
**Priority:** P1 — T2 due Mar 14 (Day 5 from Mar 10 T1)
**Effort:** ~45 min
**Output:** Touch 2 drafts for all 7 Tyler Kapeller referral contacts

All 7 T1 messages sent Mar 10. T2 eligible starting Day 4 (Mar 14). Send on Mar 14 (Day 5).

| # | Name | Company | Channel | T1 Angle | T2 Notes |
|---|------|---------|---------|---------|---------|
| 1 | Gopi Subramaniam | Staples | Email (Apollo) | Re-engagement | Re-engage on $50K Park deal + POC done |
| 2 | Pranati Thankala | Aetna | Email (Apollo) | Re-engagement | Follow up on Dec demo |
| 3 | Roy Life | Sandia National Labs | Email (Apollo) | Re-engagement | New angle from T1 |
| 4 | Vernon Bryant | Tractor Supply | InMail (Sales Nav) | Seasonal retail regression | T2 InMail via Sales Nav (thread: 2-NTIwNTRkMWItYWU3Yy00Mjk1LWFkOTAtMzNmOTg4ZjU2M2ZjXzEwMA==). ⚠️ No email — InMail only. |
| 5 | Devin Griffin | First Citizens Bank | Email (Apollo) | FCB digital banking QA | |
| 6 | Jason Berube | First Citizens Bank | Email (Apollo) | FCB digital banking QA | |
| 7 | Skie Kagulire | First Citizens Bank | Email (Apollo) | FCB digital banking QA | |

**Rules:**
- T2 = 40-70 words, new angle, light reference back to T1
- Check batch tracker `tyler-referrals-outreach-mar10.html` for T1 content
- Use C2 formula (new proof point, tie-back, CTA)
- FCB same-company flag overridden (Tyler referral, Rob approved all 3)
- Send emails via Apollo UI (LinkedIn Outbound sequence). Vernon Bryant = InMail via Sales Nav.
- APPROVE SEND required before any sends

---

### TASK-014: Draft Wave 1 T1 + T2 Emails — Multi-Contact (6 accounts, 27 contacts)
**Status:** DONE (Mar 10, Sessions 9+11) — All 23 T1 emails sent. T2 drafts = TASK-017.
**Priority:** P0 — enrollment done, ready to draft NOW
**Effort:** ~180 min remaining (T1 + T2 drafts for 23 enrolled contacts)
**Output:** `wave1-batch1-tracker-mar10.html` with T1 + T2 drafts for all 23 contacts

**IMPORTANT:** Old wave1-prospecting-plan-mar9.html drafts are DEPRECATED. InMail drafts deleted. Start fresh email T1 drafts for all accounts. Multi-contact approach — ALL decision-makers in same batch.

**✅ Step A COMPLETE (Mar 10, Session 7):** `wave1-batch1-tracker-mar10.html` built with 27 contacts across 6 accounts.

**✅ Step B COMPLETE (Mar 10, Session 7):** 23 contacts enrolled in TAM Outbound - Rob Gorham (69afff8dc8897c0019b78c7e). 4 on HOLD (see below).

**Step A — Build batch tracker HTML first (before any drafts)** ✅ DONE
Create `wave1-batch1-tracker-mar10.html` with all 13 contacts, using the batch tracker format from sop-tam-outbound.md Part 9.

**Step B — Pre-flight checks before drafting** ✅ DONE
For each contact:
1. Check MASTER_SENT_LIST.csv — if name+company found, skip
2. Check DNC list in CLAUDE.md — if found, skip
3. Verify email status (✅ verified / ⚠️ extrapolated)

**Step C — Research + draft T1 for each contact**
Use the Contact Depth Rule from sop-tam-outbound.md Part 3:
- Fidelity (3 contacts) = Medium targeting — each gets unique role-scope angle + different proof point
- YouTube (3 contacts) = High targeting — each gets unique product-area angle
- Others (1-2 contacts) = Standard targeting

**Full contact list (27 contacts — 23 enrolled, 4 HOLD):**
| # | Name | Account | Email | Enrolled | Targeting | T1 Angle |
|---|------|---------|-------|----------|-----------|---------|
| 1 | Rick Brandt | Cboe Global Markets | rbrandt@cboe.com ✅ | ✅ | Standard | Finance/regression cycle |
| 2 | Maurice Saunders | Cboe Global Markets | msaunders@cboe.com ✅ | ✅ | Standard | Same account, different angle |
| 3 | Snezhana Ruseva | Cboe Global Markets | sruseva@cboe.com ✅ | ✅ | Standard | Same account, different angle |
| 4 | Seth Drummond | Fidelity | seth.drummond@fidelity.com ✅ | ✅ | Medium | Org-level — QA team productivity, Hansard |
| 5 | Nithya Arunkumar | Fidelity | n.arunkumar@fidelity.com ✅ | ✅ | Medium | Team-level — test creation/maintenance, CRED |
| 6 | Chris Pendergast | Fidelity | chris.pendergast@fidelity.com ✅ | ✅ | Medium | Fortune 100 3X story |
| 7 | Christopher Bilcz | Fidelity | christopher.bilcz@fmr.com ✅ | ✅ | Medium | VP tier, different angle |
| 8 | Eric Pearson | Fidelity | ep@fidelity.com ✅ | ✅ | Medium | VP tier, different angle |
| 9 | Richelle Lacamera | Fidelity | richelle.lacamera@fidelity.com ✅ | ✅ | Medium | Director tier |
| 10 | Sourabh Roy | Fidelity | sourabh.roy2@fmr.com ✅ | ✅ | Medium | Director tier |
| 11 | Padma Srikanth | Fidelity | padma.srikanth@fmr.com ✅ | ✅ | Medium | Director tier |
| 12 | Neeraj Tati | JPMorgan Chase | neeraj.tati@chase.com ✅ | ✅ | Medium | Engineering/CI angle |
| 13 | Rose Serao | JPMorgan Chase | rose.serao@chase.com ⚠️ extrapolated | 🚫 HOLD | Medium | Risk-based regression — verify email first |
| 14 | Justin Hutchinson | JPMorgan Chase | justin.hutchinson@jpmchase.com ✅ | 🚫 HOLD | Medium | Ops QA concern — confirm software QA |
| 15 | Nikki Urlaub | JPMorgan Chase | (unverified) | 🚫 HOLD | Medium | Ops QA concern — confirm software QA |
| 16 | Brahmaiah Vallabhaneni | Commvault | bvallabhaneni@commvault.com ✅ | ✅ | Medium | Enterprise productivity — Fortune 100 |
| 17 | Jennifer Drangstveit | Commvault | jennifer.drangstveit@cunamutual.com ✅ | ✅ | Medium | Different angle — Cisco 35% regression |
| 18 | Arun Amarendran | Commvault | aamarendran@commvault.com ✅ | ✅ | Medium | Automation lead angle |
| 19 | Prasad Alapati | Commvault | palapati@commvault.com ✅ | ✅ | Medium | Director tier |
| 20 | Sucheth Ramgiri | Commvault | sramgiri@commvault.com ✅ | ✅ | Medium | Manager tier |
| 21 | Chamath Guneratne | TruStage | chamath.guneratne@trustage.com ✅ | ✅ | Standard | Insurance/compliance — Hansard |
| 22 | Maggie Redden | TruStage | maggie.redden@cunamutual.com ✅ | ✅ | Standard | Different angle from Chamath |
| 23 | Jennifer Drangstveit | TruStage | jennifer.drangstveit@cunamutual.com ✅ | ✅ | Standard | Director tier |
| 24 | Shawn Woods | TruStage | (TBD) | 🚫 HOLD | Standard | Below Director threshold — Rob to decide |
| 25 | John Harding | YouTube | jharding@youtube.com ✅ catch-all | ✅ | High | Music platform — Nagra DTV |
| 26 | Des Keane | YouTube | des@google.com ✅ catch-all | ✅ job_change override | High | Infrastructure/reliability angle |
| 27 | Hrishikesh Aradhye | YouTube | hrishi@google.com ✅ catch-all | ✅ job_change override | High | Podcasts/Music subteam angle |

**HOLD contacts — Rob action required:**
- Rose Serao: Send or skip? Email extrapolated (rose.serao@chase.com pattern matches domain standard)
- Justin Hutchinson: Ops QA or software QA? Title "QA Lead" — confirm scope before enrolling
- Nikki Urlaub: Same ops QA concern
- Shawn Woods: Below Director threshold — include or skip?

**Step D — Build T2 drafts for same contacts**
After T1 drafts complete. Use Deep-Dive v4 formula (sop-tam-outbound.md Part 7): 140-190 words, 4 parts — "I imagine" pain + Testsigma pitch + customer story + 15-min CTA, different proof point from T1. Full playbook: `memory/playbooks/t2-followup.md`.

**Step E — Present BATCH SUMMARY block to Rob**
Format per sop-tam-outbound.md Part 10. Wait for "APPROVE SEND."

**Step F — Post-send (after Rob's APPROVE SEND)**
For each contact sent:
1. Enroll in TAM Outbound (ID: 69afff8dc8897c0019b78c7e) via Apollo — mark Step 1 complete
2. Log row in MASTER_SENT_LIST.csv: [Name, email, Company, Title, Email, Send Date, B_Wave1]
3. Update batch tracker HTML: Status → "T1 Sent [date]"
4. Update tam-coverage-tracker.csv: account status → "📤 In Sequence"

**Apollo task queue becomes the follow-up controller after enrollment.** Each enrolled contact auto-generates a Step 2 task for Day 5. Check Apollo daily for tasks due.

**T1 formula:** Enterprise Email T1 (HC1 intro, SMYKM subject, 75-100 words). sop-tam-outbound.md Part 6.
**T2 formula:** Deep-Dive v4 (140-190 words, "I imagine" pain + pitch + customer story + 15-min CTA). sop-tam-outbound.md Part 7. Full playbook: `memory/playbooks/t2-followup.md`.
**Enrollment email:** robert.gorham@testsigma.com (.com ONLY)

---

### TASK-015: TAM SOP Review + Sign-Off
**Status:** UNCLAIMED — Rob needs to review Draft v2
**Priority:** P1 — read before any Wave 1 sends
**Effort:** ~15 min (Rob reads)
**Output:** Rob confirms SOP is approved for use

Review TAM-Outbound-SOP-draft-v1.html (now Draft v2). Check:
- Section 2 persona rule (bigger company = higher)
- Section 7 T1 formula (HC1 intro + SMYKM)
- Section 7 T2 formula (unified email-first)
- Section 7 Breakup formula
- YouTube contact shortlist (John Harding as primary)
- Decisions Made section (4 decisions confirmed)

---

*Updated by Claude — 2026-03-10 (Session 7)*

### TASK-027: Send Wave 5B T1 Emails (5 contacts — pending APPROVE SEND)
**Status:** UNCLAIMED — waiting for Rob's APPROVE SEND
**Priority:** P0 — contacts enrolled, T1 tasks will appear in Apollo Tasks tab
**Effort:** ~10 min (paste drafts from tracker into Apollo)
**Output:** 5 T1 emails sent via Apollo Tasks tab

5 contacts from Wave 5B (account expansion sweep) enrolled in TAM Outbound Step 1. When Apollo surfaces the manual email tasks:
1. Open Apollo Tasks tab
2. For each contact: paste subject + body from `tamob-batch-20260312-5.html`
3. Send Now
4. Update tracker HTML badges to "T1 Sent"
5. MASTER_SENT_LIST.csv already updated (432 rows)

**Contacts:** Divyesh Jain (GEICO), Altaf Shariff (OneMain), Geo Sarria (EA), Clifton Wilcox (EA), Christie Burkhead (Humana)

**Donald Jackson (Chase):** NOT enrolled — ownership blocked. Rob must assign ownership in Apollo UI first. After ownership fixed, enroll + add to this send batch.

**APPROVE SEND required before any sends**

### TASK-028: Fix Apollo Ownership for Donald Jackson (Chase) + Yogesh Garg (Check Point)
**Status:** UNCLAIMED — requires Rob manual action in Apollo UI
**Priority:** P1 — blocking 2 contacts from enrollment
**Effort:** ~5 min
**What:** Both contacts get `contacts_without_ownership_permission` error during enrollment. Rob needs to:
1. Go to Apollo > Contacts > search each name
2. Assign ownership to Rob's account
3. Then re-enroll via API or manually add to TAM Outbound sequence

### TASK-032: Fix Non-Standard Batch Names in MASTER_SENT_LIST.csv
**Status:** UNCLAIMED
**Priority:** P3 — cosmetic but improves traceability
**Effort:** ~15 min
**Output:** Updated MASTER_SENT_LIST.csv

5 non-standard batch names from today's sessions need correction:
- "B6" (24 rows) → "TAM Outbound Batch 6 Mar12"
- "B7" (5 rows) → "TAM Outbound Batch 7 Mar12"
- "W6B1" (8 rows) → "TAM Outbound Wave 6 Batch 1 Mar12"
- "W6B2" (27 rows) → "TAM Outbound Wave 6 Batch 2 Mar12"
- "W5B-S29" (5 rows) → "TAM Outbound Batch 5B Mar12"

Use sed or awk to do bulk replace. Verify row count unchanged after edit.

### TASK-029: Sales Nav Deep Sweep — Backlog Contacts (5 no-email + HashiCorp)
**Status:** UNCLAIMED
**Priority:** P2 — expansion pipeline
**Effort:** ~45 min
**What:** Use Sales Navigator browser automation to find emails for:
- Partha Pattanaik (Humana, Dir QA) — no Apollo email
- David Macdonald (OneMain, VP/MD QE) — no Apollo email
- Graig Taylor (EA/Respawn, QA Dir) — no Apollo email
- Brent Kong (EA, Dir QE) — no Apollo email
- Jaideep Mukherjee (GEICO, QA Eng Mgr) — no Apollo email
- HashiCorp — 0 Apollo results for any QA titles, full Sales Nav sweep needed
- Brian Vanhoose + Marion Stewart (JPMorgan) — verify if software QA vs operations QA

**Method:** Sales Nav search + Apollo Chrome Extension import for contacts without emails. See `memory/playbooks/sales-nav-deep-sweep.md`.

### TASK-030: Enrich + Prospect New Untouched Accounts (BlackRock, CVS, Citizens, Bungie)
**Status:** UNCLAIMED
**Priority:** P2 — new account pipeline
**Effort:** ~60 min
**What:** Session 29 partially enriched contacts at these HIGH ICP accounts (not yet enrolled):
- BlackRock: 4 contacts identified (Darin Koenig, Gil Leong, Nate Sewell, Amaresh Shukla — all verified emails, catchall domain)
- CVS Health: 2 contacts (Erin Bixel, Avani Vaidya — verified, non-catchall)
- Citizens Bank: 3 contacts with obfuscated names (need enrichment by Apollo ID)
- Bungie: 4 contacts with obfuscated names (3 QA Directors + 1 Sr QA Manager)
Complete dedup, draft T1s, enroll in TAM Outbound.
