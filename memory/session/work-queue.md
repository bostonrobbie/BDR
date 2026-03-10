# Work Queue
## Last Updated: 2026-03-10

## ⚡ SESSION START PROTOCOL (read every time)
1. `git pull origin main`
2. Read this file + handoff.md
3. Open Apollo → TAM Outbound - Rob Gorham → Tasks tab → check what's due today
4. Cross-reference batch tracker HTML for draft content
5. Continue from there. Do NOT re-research anything already in the tracker.

Tasks are sorted by priority. Claim one task at a time by updating status to IN_PROGRESS.

---

## 🔴 CRITICAL — Do First

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
| touch2_drafts_feb27.md | Mar 7 | 9 Touch 2 emails for Feb 27 contacts, all MQS 10-12/12 |
| touch2_drafts_batch3_inmail.md | Mar 7 | 4 Touch 2 InMails for INC-001 Batch 3 (Irfan, Katie, Rachana, Giang). MQS 11, 10, 12, 12. All READY TO SEND. |
| TAM Outbound - Rob Gorham sequence built | Mar 10 | Apollo ID: 69afff8dc8897c0019b78c7e. 7 steps all manual, Day 1/5/10/15/21/28/35. email→email→LI connect→call→call→call→breakup email. Ready for enrollment. |

---

### TASK-011: Prospect Wave 1 Factor Enterprise Accounts
**Status:** IN PROGRESS (Mar 10 — SOP built, drafts ready, awaiting APPROVE SEND)
**Priority:** P1 — sequence is ready, accounts are identified
**Effort:** ~90 min
**Output:** Batch tracker file for Wave 1 TAM prospects

Identify QA/testing leaders at Factor enterprise accounts and enroll in TAM Outbound - Rob Gorham (69afff8dc8897c0019b78c7e).

Priority accounts:
- JPMorgan Chase (Note: Jitesh Biswal = DNC — skip him)
- Cboe Global Markets
- Commvault
- TruStage
- Fidelity (confirm right contact)
- YouTube / Google (confirm right contact)

Rules:
- Use Apollo enrichment to find QA Manager/Director/Lead titles
- Dedup against MASTER_SENT_LIST.csv before enrolling
- Enrollment email: robert.gorham@testsigma.com (.com only)
- Create batch tracker BEFORE any drafts
- ALL messages need Rob's "APPROVE SEND" first

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

### TASK-014: Draft Wave 1 T1 + T2 Emails — Multi-Contact (6 accounts, 13 contacts)
**Status:** IN PROGRESS — SOPs updated Mar 10, ready to build batch tracker + drafts
**Priority:** P0 — ready to build NOW
**Effort:** ~180 min (13 contacts × ~10 min research + draft each)
**Output:** `wave1-batch1-tracker-mar10.html` with T1 + T2 drafts for all 13 contacts

**IMPORTANT:** Old wave1-prospecting-plan-mar9.html drafts are DEPRECATED. InMail drafts deleted. Start fresh email T1 drafts for all accounts. Multi-contact approach — ALL decision-makers in same batch.

**Step A — Build batch tracker HTML first (before any drafts)**
Create `wave1-batch1-tracker-mar10.html` with all 13 contacts, using the batch tracker format from sop-tam-outbound.md Part 9.

**Step B — Pre-flight checks before drafting**
For each contact:
1. Check MASTER_SENT_LIST.csv — if name+company found, skip
2. Check DNC list in CLAUDE.md — if found, skip
3. Verify email status (✅ verified / ⚠️ extrapolated)

**Step C — Research + draft T1 for each contact**
Use the Contact Depth Rule from sop-tam-outbound.md Part 3:
- Fidelity (3 contacts) = Medium targeting — each gets unique role-scope angle + different proof point
- YouTube (3 contacts) = High targeting — each gets unique product-area angle
- Others (1-2 contacts) = Standard targeting

**Full contact list with targeting instructions:**
| # | Name | Account | Email | Targeting Level | T1 Angle |
|---|------|---------|-------|-----------------|---------|
| 1 | Rick Brandt | Cboe Global Markets | rbrandt@cboe.com ✅ | Standard | Finance/regression cycle |
| 2 | Seth Drummond | Fidelity | seth.drummond@fidelity.com ✅ | Medium | Org-level — QA team productivity, Hansard |
| 3 | Nithya Arunkumar | Fidelity | n.arunkumar@fidelity.com ✅ | Medium | Team-level — test creation/maintenance, CRED |
| 4 | Chris Pendergast | Fidelity | chris.pendergast@fidelity.com ✅ | Medium | Different from Nithya — Fortune 100 3X story |
| 5 | Rose Serao | JPMorgan Chase | rose.serao@chase.com ⚠️ VERIFY FIRST | Medium | Risk-based regression at banking scale |
| 6 | Neeraj Tati | JPMorgan Chase | neeraj.tati@chase.com ✅ | Medium | Engineering/CI angle — different from Rose |
| 7 | Brahmaiah Vallabhaneni | Commvault | bvallabhaneni@commvault.com ✅ | Medium | Enterprise productivity — Fortune 100 |
| 8 | Jennifer Wang | Commvault | jenniferwang@commvault.com ✅ | Medium | Different angle — Cisco 35% regression |
| 9 | Chamath Guneratne | TruStage | chamath.guneratne@trustage.com ✅ | Standard | Insurance/compliance — Hansard |
| 10 | Maggie Redden | TruStage | maggie.redden@trustage.com ⚠️ VERIFY FIRST | Standard | Different angle from Chamath if verified |
| 11 | John Harding | YouTube | jharding@youtube.com ✅ catch-all | High | Music platform — Nagra DTV |
| 12 | Des Keane | YouTube | des@google.com ✅ | High | Infrastructure/reliability angle |
| 13 | Hrishikesh Aradhye | YouTube | hrishi@google.com ✅ | High | Podcasts/Music subteam angle |

**Step D — Build T2 drafts for same contacts**
After T1 drafts complete. Use unified email-first formula (sop-tam-outbound.md Part 7): 4 parts, 50-70 words, engagement question CTA, different proof point from T1.

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
**T2 formula:** Unified email-first (4 parts, 50-70 words, engagement question). sop-tam-outbound.md Part 7.
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

*Updated by Claude — 2026-03-10 (Session 5)*
