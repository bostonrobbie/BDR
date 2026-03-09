# Work Queue

> Task tracker for multi-agent coordination.
> **Before starting any task:** claim it by setting status to `IN_PROGRESS` and adding your agent ID.
> **After finishing:** mark `DONE` with a completion note.
> Keep completed tasks in the file for reference — move to the Archive section after 2 weeks.

---

## Active Tasks

### TASK-012 | TAM prospecting — Wave 1 Factor accounts
**Status:** PENDING
**Priority:** HIGH
**Due:** This week (Mar 9+)
**Description:** Begin systematic prospecting into Factor account Wave 1. All 6 accounts need contacts sourced, enriched via Apollo, added to LinkedIn Outbound Q1 sequence. Verify TruStage prior outreach before including.
**Wave 1 accounts:** Chase, Cboe Global Markets, Commvault, Fidelity Investments, YouTube, TruStage (check first)
**Files:** `memory/target-accounts.md` (Wave 1 section), `tam-coverage-tracker.html`, `memory/sop-send.md`

---

### TASK-013 | Add company column to MASTER_SENT_LIST
**Status:** PENDING
**Priority:** MEDIUM (process improvement)
**Due:** Next batch send
**Description:** MASTER_SENT_LIST.csv currently has no company column, making account-level dedup against TAM impossible. Add "company" column to all future entries. Backfill for existing 228 entries where possible (lower priority).
**Impact:** Enables programmatic cross-reference — know exactly which TAM accounts already have contacts worked.

---

### TASK-010 | B9 Touch 2 sends (17 prospects) — ✅ DONE
**Status:** DONE (2026-03-09)
**Completed by:** Cowork-6 (Mar 9 send session)
**Result:** 16 of 17 B9 T2 emails sent via Apollo UI. (Kylie Summer + Yuliya A excluded — no emails. Georgii Petrosian counted as B11 not B9.) ⚠️ Sent from robert.gorham@testsigma.net (Apollo default — not caught until Draft 26). Rob aware. T3 due Mar 14.

---

### TASK-011 | B9/B10/B11 Touch 2 EMAIL drafts — ✅ DONE
**Status:** DONE (2026-03-09)
**Completed by:** Cowork-6 (Mar 9 send session)
**Result:** 25 of 28 T2 emails sent via Apollo UI. 3 skipped (preflight failures): Tim Wiseman/Upland wrong owner/sequence, Jason Poole/Vergent wrong owner, LP Guo/Moody's no sequences. ⚠️ Drafts 1-25 from robert.gorham@testsigma.net, Drafts 26-28 from .com. T3 due Mar 14. Full send log in pipeline-state.md Email Send History.
**Key fix this session:** Apollo From dropdown must be manually changed from .net to .com every time. SOP updated in memory/sop-send.md (Apollo UI Email Send section).

---

### TASK-009 | Touch 2 emails — WV Mar 3 batch + BI stragglers (25 total) ⬅ DO THIS FIRST
**Status:** IN_PROGRESS (email collection 7/19 done; 0 drafts written)
**Priority:** URGENT — all overdue or due today Mar 8
**Due:** Mar 8 (WV Mar 3 batch Day 4+), Buyer Intent batch overdue since Mar 3
**Description:** Draft and send 25 Touch 2 emails. 12 email addresses still missing — collect from Apollo first, then draft all 25.

**Sending mechanism:** ALL manual Gmail sends (robert.gorham@testsigma.com). Apollo cannot auto-generate — WV Mar 3 batch is enrolled in LinkedIn Outbound only, not the WV email sequence. Buyer Intent stragglers have failed/finished/missing Apollo contact records.

**Template:** EM-FU-1 (TEMPLATE_LIBRARY.md). Subject: "Re: Quick question, [First Name]". Max 70 words. Different proof point from T1 (T1 = Medibuddy 80% maintenance). "What day works" CTA. MQS ≥ 9/12.

**Emails already collected (7):**
| Name | Email | Company | Proof Point |
|------|-------|---------|-------------|
| Stephen Starnaud | stephen.starnaud@biberk.com | biBerk | Hansard 8→5wk |
| Kyung Kim | kkim@webmd.com | WebMD | Sanofi 3d→80min |
| Lyle Landry | lyle.landry@availity.com | Availity | Sanofi 3d→80min |
| Morya Moyal | mmoyal@hippo.com | Hippo | Hansard 8→5wk |
| Shivaleela Devarangadi | sdevarangadi@rxsense.com | RxSense | Sanofi 3d→80min |
| Jim Lenihan | jim.lenihan@waystar.com | Waystar | Sanofi 3d→80min |
| Konstantin Diachenko | kdiachenko@paymentus.com | Paymentus | CRED 90%+5x |

**Buyer Intent emails (already confirmed from website_visitor_sequence_drafts.md):**
| Name | Email | Company | Proof Point |
|------|-------|---------|-------------|
| Jose Moreno | jose.moreno@flywire.com | Flywire | CRED 90%+5x |
| Eyal Luxenburg | eyal.luxenburg@island.io | Island | Fortune 100 3X |
| Jeff Barnes | jeff.barnes@digi.com | Digi International | Spendflo 50% |
| Todd Willms | todd.willms@bynder.com | Bynder | Spendflo 50% |
| Tom Yang | tom.yang@versantmedia.com | Versant Media | Nagra DTV 2500 |
| Jason Ruan | jason.ruan@binance.com | Binance | CRED 90%+5x |

**Emails still needed — pull from Apollo (search by name+domain):**
| Name | Domain | Vertical | Proof Point |
|------|--------|----------|-------------|
| Courtney Corbin | vizientinc.com | Healthcare | Sanofi 3d→80min |
| Jason Schwichtenberg | webmd.net | Healthcare ⚠️double-channel | Sanofi 3d→80min |
| Geoffrey Juma | solera.com | InsurTech | Hansard 8→5wk |
| Olivia Pereiraclarke | sapiens.com | Insurance | Hansard 8→5wk |
| Nabil Ahmed | progyny.com | Healthcare | Sanofi 3d→80min |
| Sneha Bairappa | aamc.org | Healthcare | Sanofi 3d→80min |
| Jamie Kurt | vertafore.com | Insurance ⚠️double-channel | Hansard 8→5wk |
| Avijit Sur | solera.com | InsurTech | Hansard 8→5wk |
| Kerri McGee | sapiens.com | Insurance ⚠️double-channel | Hansard 8→5wk |
| Priya Khemani | getinsured.com | InsurTech | Hansard 8→5wk |
| Keith Schofield | fullsteam.com | FinTech | CRED 90%+5x |
| Emre Ozdemir | theocc.com | FinTech | CRED 90%+5x |

⚠️ **Nabil Ahmed:** May not be in Apollo. If not found, search Gmail sent folder for the Mar 3 email to progyny.com to get his exact address.
⚠️ **Double-channel contacts** (Schwichtenberg, McGee, Kurt): Still send Touch 2 email (per Rob's Mar 8 confirmation — send to all 19).

**Draft rules (non-negotiable):**
- No em dashes. No "I noticed/I saw." Reduction framing only (not "Nx faster").
- 1-2 question marks max. Max 70 words. Subject: "Re: Quick question, [First Name]"
- MQS ≥ 9/12. Present all drafts to Rob for review. NEVER SEND without "APPROVE SEND."

**Files:** `TEMPLATE_LIBRARY.md`, `memory/sop-outreach.md`, `memory/proof-points.md`, `memory/incidents.md`

---

### TASK-001 | Mon Mar 9 — B10 InMail sends
**Status:** PENDING
**Priority:** HIGH
**Due:** 2026-03-09
**Description:** 8 credit InMails queued for Batch 10. Confirm enrollment status first — some may be blocked by ownership in Apollo. Send only if enrollment confirmed and Rob approves.
**Prospects:** Sasa Lazarevic, Srikanth Sy, Sarah Ross, Niveditha Somasundaram, Stephen Burlingame, Dave Czoper, Crys Simonca, Christian Melville
**Blocked by:** Apollo ownership issues for Sasa Lazarevic + Christian Melville. Rob must resolve.
**Files:** `memory/pipeline-state.md` (B10 section), `MASTER_SENT_LIST.csv`

---

### TASK-002 | B10 + B11 Touch 2 drafts (due Mar 11)
**Status:** DONE (2026-03-08)
**Completed by:** Cowork-1 (Mar 8 session)
**Result:** All T2 drafts built in `linkedin-t2-drafts-mar8.html`. B10: 9 prospects (Tim Wiseman, Josh Thayer, Elena Lysenko, Jason Poole, Tom Goody, LP Guo, Francesco Leising, Chet West, Clint Parker). B11: 4 prospects (Brad Askins, Dan Heintzelman, Georgii Petrosian, Madhu Nedunuri). All use free thread continuation method (Sales Nav Inbox). **Rob reviews and sends via Sales Nav on/after Mar 11.**

---

### TASK-003 | B10 enrollment blockers
**Status:** PENDING
**Priority:** MEDIUM
**Due:** Before Mar 9 sends
**Description:** 7 B10 contacts not yet fully enrolled in LinkedIn Outbound Q1. 2 blocked by Apollo ownership (Sasa Lazarevic, Christian Melville). 5 not attempted (Kristyn Burke, Tim Hartgrave, Vince Delfini, Padmanaban Vadivelu, Ravi Nag).
**Action needed from Rob:** Reassign ownership for Lazarevic + Melville in Apollo, OR manually enroll via Apollo UI.
**Other 5:** Attempt enrollment via MCP, report back on result.

---

### TASK-004 | Namita Jain follow-up (OverDrive)
**Status:** PENDING
**Priority:** MEDIUM
**Due:** Overdue — was due ~Mar 4
**Description:** Touch 1 email sent Feb 27. No confirmed reply in Gmail. Check inbox first — if no reply, draft follow-up Touch 2. Must be Day 4+ from Feb 27 (it is — Day 9 as of Mar 7).
**Reference:** `memory/warm-leads.md`, `memory/sop-outreach.md`
**Important:** Check Gmail for any reply before drafting.

---

### TASK-005 | Buyer Intent Touch 2 gap — verify status
**Status:** DONE (2026-03-08)
**Completed by:** Cowork-1 (Mar 8 session)
**Result:**
- Jose Moreno (Flywire): WV sequence "manually finished" at Step 1. No T2 generated. → Manual Gmail send needed.
- Jason Ruan (Binance): WV sequence Step 2 FAILED — `thread_reply_original_email_missing`. Apollo can't find original T1 thread (sent via Gmail MCP, not Apollo). → Manual Gmail.
- Eyal Luxenburg (Island): Same failure as Ruan — Step 2 FAILED, `thread_reply_original_email_missing`. → Manual Gmail.
- Tom Yang: NOT IN APOLLO contacts. Correct company = Versant Media (not IQVIA from the audit file — different person). Email: tom.yang@versantmedia.com.
- Jeff Barnes: NOT IN APOLLO. Correct company = Digi International (not Mimecast). Email: jeff.barnes@digi.com.
- Todd Willms: NOT IN APOLLO. Correct company = Bynder. Email: todd.willms@bynder.com.
**All 6 folded into TASK-009 for manual Gmail T2 send.**

---

### TASK-006 | Tom Goody + Mohan Guruswamy — enroll in LinkedIn Outbound Q1
**Status:** DONE (2026-03-07/08)
**Completed by:** Cowork-1
**Result:** Apollo API confirmed BOTH are already enrolled in LinkedIn Outbound Q1 (sequence `69a05801fdd140001d3fc014`, status: active). Tom Goody is B10 sent Mar 6. Mohan Guruswamy is B9 sent Mar 3. No action needed.

---

### TASK-007 | Apollo WV sequence gap investigation
**Status:** PENDING
**Priority:** LOW
**Due:** No hard deadline
**Description:** Apollo UI shows "81 delivered" in Website Visitor sequence but only 28 WV emails confirmed via Gmail. Gap of ~53 is unresolved. Likely pre-campaign sends or different time window.
**Action:** Pull Apollo sequence stats via API and compare date ranges to Gmail sends.

---

### TASK-008 | Merge unmerged Claude branches (optional)
**Status:** PENDING
**Priority:** LOW
**Due:** No hard deadline
**Description:** Three Claude branches have unmerged content that may be useful:
- `claude/add-secondary-brain-layer` — voice-rules.md, gold-standards.md, sales-playbook.md, integrations.md, email-channel-ops.md, linkedin-email-sop-v4.md, prospecting-checklist.md
- `claude/consolidate-sessions-repo` — older restructure with knowledge/ folder
- `claude/plan-upgrades` — CI/CD, test suite, API rewrite (engineering-heavy, not urgent)
**Action:** Review add-secondary-brain-layer files, merge useful content into current memory/ structure. Skip consolidate and plan-upgrades unless Rob requests.

---

## Completed Tasks

### TASK-C001 | Email count reconciliation + audit (DONE 2026-03-07)
**Completed by:** Cowork-1
**Result:** Confirmed 49 outreach emails via Gmail audit. Updated pipeline-state.md, CLAUDE.md, MASTER_SENT_LIST.csv. Discovered 4 cross-channel double-contacts.

### TASK-C002 | Full Apollo audit (DONE 2026-03-07)
**Completed by:** Cowork-1
**Result:** Verified B10 (9 sent), B11 (4 sent), enrollment status for all batches. Audit report saved to audit-report-mar6.html. Pipeline state synced.

### TASK-C003 | Multi-agent collaboration system build (DONE 2026-03-07)
**Completed by:** Cowork-1
**Result:** Created AGENTS.md, handoff.md, session-log.md, work-queue.md, session-manager.md. Git committed (db17edb). Push needs Rob's terminal.

### TASK-C004 | Repo organize + commit (DONE 2026-03-07)
**Completed by:** Cowork-1
**Result:** 194 files staged and committed (db17edb). Push failed — requires Rob's terminal (`git push origin main`).
