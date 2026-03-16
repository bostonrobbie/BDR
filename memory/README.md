# Memory — BDR Operating Brain

This folder is the canonical, living knowledge base for Rob's outbound workflow. Every file here is actively used by Claude sessions. Read the relevant files before starting any task — don't rely on cached knowledge from prior sessions.

---

## Quick Navigation — "I need to..."

| Task | File(s) to Read |
|------|----------------|
| Start a session | `session/handoff.md` → `session/work-queue.md` → `session/in-progress.md` |
| Close a session | `playbooks/session-handoff.md` |
| Run the daily workflow | `sop-daily.md` |
| Build a new T1 outreach batch | `sop-prospect.md` + `playbooks/tam-t1-batch.md` |
| Draft LinkedIn outreach | `sop-outreach.md` |
| Draft email outreach | `sop-email.md` |
| Run the TAM outbound process end-to-end | `sop-tam-outbound.md` |
| Send InMails via Sales Navigator | `sop-send.md` |
| Handle inbound Salesforce-assigned leads | `playbooks/inbound-leads-sequence.md` |
| Enroll contacts in Apollo | `playbooks/apollo-enrollment.md` |
| Send via Apollo task queue | `playbooks/apollo-task-queue-sends.md` |
| Write T2 follow-ups | `playbooks/t2-followup.md` |
| Do pre-batch dedup | `playbooks/dedup-protocol.md` + `../MASTER_SENT_LIST.csv` |
| Handle a catchall email domain | `playbooks/catchall-domains.md` |
| Validate an email before sending (QA Gate) | `playbooks/qa-gate.md` |
| Find QA contacts at a target company | `playbooks/sales-nav-deep-sweep.md` |
| Recover from an error | `playbooks/error-recovery.md` |
| Build a batch tracker HTML | `playbooks/batch-tracker-html.md` |
| Handle a warm reply or inbound response | `warm-leads.md` |
| Write a post-call follow-up email | `sop-post-call-followup.md` |
| Check Apollo config, sequence IDs, credits | `apollo-config.md` |
| Review incidents and hard rule history | `incidents.md` |
| Check performance data / A-B test results | `scoring-feedback.md` |
| Look up proof points / customer stories | `proof-points.md` |
| View current send history + batch state | `pipeline-state.md` |
| Look up target accounts (TAM + Factor list) | `target-accounts.md` |
| Check data-backed send rules | `data-rules.md` |
| Analyze email performance | `email-analytics-sop.md` |

---

## SOPs (Standard Operating Procedures)

Full workflow guides. Read end-to-end before executing the corresponding task.

| File | Scope | Last Updated |
|------|-------|-------------|
| `sop-daily.md` | "Run the daily" — master daily workflow trigger. T1 priority, T2 batching, send windows. | Mar 12, 2026 |
| `sop-tam-outbound.md` | TAM Outbound end-to-end. The authoritative guide for all TAM account outreach. 26 parts. | Mar 11, 2026 |
| `sop-prospect.md` | Sales Nav batch build — authorized prospecting universe, search filters, ICP scoring. | Mar 2026 |
| `sop-outreach.md` | LinkedIn outreach only — message drafting, C2 structure, QA Gate for InMail. | Mar 2026 |
| `sop-email.md` | Email outreach only — drafting, personalization, Apollo sequence execution. | Mar 2026 |
| `sop-send.md` | LinkedIn Sales Navigator live send — pre-send checklist, INC-012 rules, approval gates. | Mar 2026 |
| `sop-post-call-followup.md` | Post-call follow-up email from Gong transcript. Created Mar 11. | Mar 11, 2026 |
| `email-analytics-sop.md` | Email performance analysis — open rate, reply rate, sequence audit. | Mar 2026 |

---

## Playbooks

Tactical guides for specific sub-tasks. Faster to read than SOPs. Focus on gotchas and edge cases from real production work.

See `playbooks/_index.md` for full descriptions and use-when guidance.

| Playbook | File | One-Line Summary |
|----------|------|-----------------|
| TAM T1 Batch | `playbooks/tam-t1-batch.md` | End-to-end daily T1 outreach batch — the primary daily workflow |
| Apollo Enrollment | `playbooks/apollo-enrollment.md` | Creating contacts and enrolling in Apollo sequences |
| Apollo Task Queue Sends | `playbooks/apollo-task-queue-sends.md` | Executing sends through Apollo's manual task queue |
| Inbound Leads Sequence | `playbooks/inbound-leads-sequence.md` | Identifying, qualifying, and sending to Salesforce-assigned inbound leads |
| T2 Follow-Up Drafting | `playbooks/t2-followup.md` | Writing Touch 2 follow-up emails |
| Dedup Protocol | `playbooks/dedup-protocol.md` | Safety check before every send — prevents double-contacts |
| QA Gate | `playbooks/qa-gate.md` | 14-point message validation checklist before any outreach |
| Sales Nav Deep Sweep | `playbooks/sales-nav-deep-sweep.md` | Finding QA contacts at target accounts via LinkedIn |
| Catchall Domain Handling | `playbooks/catchall-domains.md` | Handling unverifiable email domains |
| Batch Tracker HTML | `playbooks/batch-tracker-html.md` | Building and maintaining HTML batch tracker files |
| Error Recovery | `playbooks/error-recovery.md` | Catalog of every error hit across 30+ sessions, with fixes |
| Session Handoff | `playbooks/session-handoff.md` | End-of-session closing protocol |

---

## Reference Files

Always-on knowledge. Read on demand when relevant to current task.

| File | What It Contains |
|------|----------------|
| `pipeline-state.md` | Full send log, batch index, current contact statuses, skip rules |
| `warm-leads.md` | Active warm leads, reply handling notes, re-engagement rules |
| `incidents.md` | Incident log (INC-001 through INC-012). Hard rules derived from real mistakes. |
| `apollo-config.md` | All Apollo sequence IDs, email account ID, user ID, credit tracking |
| `data-rules.md` | Data-backed hard rules and constraints (from performance analysis) |
| `scoring-feedback.md` | A/B test results, reply rate data, message performance feedback |
| `proof-points.md` | Customer stories, stats, and proof points by vertical and pain type |
| `target-accounts.md` | TAM (312) + Factor (38) account list, ICP scores, do-not-contact flags |
| `glossary.md` | Key terms, acronyms, internal shorthand |
| `codex-cowork-operating-protocol.md` | Multi-agent session coordination rules |

---

## Supporting Folders

| Folder | What It Contains |
|--------|----------------|
| `session/` | Live session state: `handoff.md`, `work-queue.md`, `in-progress.md`, `messages.md`, `session-log.md` |
| `competitors/` | Battle cards per competitor tool (mabl, Katalon, Cypress, Selenium, etc.) |
| `context/` | Evergreen sales reference: personas, objection map, platform overview, proof points, voice rules |
| `ops/` | Channel-specific ops guides: email channel, LinkedIn + email SOP v4, prospecting checklist |
| `market-intel/` | Industry trends, analyst coverage |
| `call-notes/` | Post-call captures (template at `call-notes/_template.md`) |
| `wins/` | Win reports (template at `wins/_template.md`) |
| `losses/` | Loss reports (template at `losses/_template.md`) |
| `inbox/` | Inbound item staging area |
| `.audit/` | Audit processing queue |

---

## Hard Rules (enforced across all files)

1. **NEVER send without Rob's explicit APPROVE SEND.** No exceptions. Not for warm leads, not for obvious emails.
2. **NEVER modify or delete existing records** without Rob's per-item approval.
3. **Read the relevant SOP/playbook BEFORE starting a task.** Don't rely on cached knowledge.
4. **INC-012 send protocol** — JS readback + screenshot + Rob's "looks good" before every Apollo send click. See `incidents.md`.
5. **Dedup before every batch.** Check `MASTER_SENT_LIST.csv` + `playbooks/dedup-protocol.md`.

---

*Last updated: 2026-03-12 (Session 30)*
