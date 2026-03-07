# Work Queue

> Task tracker for multi-agent coordination.
> **Before starting any task:** claim it by setting status to `IN_PROGRESS` and adding your agent ID.
> **After finishing:** mark `DONE` with a completion note.
> Keep completed tasks in the file for reference — move to the Archive section after 2 weeks.

---

## Active Tasks

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
**Status:** PENDING
**Priority:** HIGH
**Due:** Start drafting Mar 8-9, send Mar 11
**Description:** Build Touch 2 drafts for all B10 (Day 4+ Mar 11) and B11 (Day 4+ Mar 11) prospects with no reply. Must pass MQS >= 9/12 and QA Gate before presenting to Rob.
**Reference:** `memory/sop-outreach.md`, `memory/incidents.md` (cadence rules), `memory/session/session-manager.md`
**B10 prospects:** 9 sent Mar 6 — see outreach-batch10-sent-mar6.html
**B11 prospects:** Brad Askins (Trimble), Dan Heintzelman (Prevail Legal), Georgii Petrosian (AuditBoard), Madhu Nedunuri (IDB Bank)

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
**Status:** PENDING
**Priority:** MEDIUM
**Due:** Before Mar 11
**Description:** 5 of 9 original Buyer Intent cohort (Feb 27 batch) did NOT receive confirmed email T2 on Mar 6. Determine whether they got InMail T2 instead or if Touch 2 has not been sent.
**Contacts:** Jose Moreno, Tom Yang, Eyal Luxenburg, Jeff Barnes, Todd Willms, Jason Ruan
**Action:** Check Apollo sequence enrollment + LinkedIn for InMail threads. Report status.

---

### TASK-006 | Tom Goody + Mohan Guruswamy — enroll in LinkedIn Outbound Q1
**Status:** PENDING
**Priority:** LOW
**Due:** No hard deadline
**Description:** Both are enrolled in "Outbound Calls (tyler) Only" sequence (called but never spoken). Rob confirmed OK to also enroll in LinkedIn Outbound Q1.
**Apollo IDs:** Look up via Apollo contacts search.

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
