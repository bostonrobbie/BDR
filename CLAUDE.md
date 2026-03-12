# Memory

## Multi-Agent Session System
This repo is worked on by multiple Claude agents across different machines. Full protocol: `AGENTS.md` (v2.0).

**Startup (14 steps — see AGENTS.md):**
1. `git pull origin main`
2. Read `AGENTS.md` (collaboration protocol)
3. Read `CLAUDE.md` (this file — SOP, memory, rules)
4. Read `memory/session/handoff.md` (pipeline state)
5. Read `memory/session/work-queue.md` (task queue)
6. Read `memory/session/in-progress.md` (crash checkpoint)
7. Read `memory/session/messages.md` (inter-session messages)
8. Crash check — if in-progress.md Status = ACTIVE → crash recovery
9. Parallel check — ls `memory/session/active/` → check for conflicts
10. Register in `memory/session/active/{session-number}.json`
11. Check Gmail MCP for replies to robert.gorham@testsigma.com
12. Claim a task (avoid conflicts with active sessions)
13. Read relevant playbooks from `memory/playbooks/`
14. Report current state to Rob

**End of EVERY session:** Follow `memory/playbooks/session-handoff.md` — update handoff.md + work-queue.md + session-log.md, deregister from active sessions, release locks, leave [DONE] message, commit.

---

## Me
Rob Gorham, BDR at Testsigma. I reach out to QA/testing leaders to book meetings and drive pipeline for our agentic AI test automation platform.

## Company
**Testsigma** — Agentic AI-powered unified test automation platform. Write tests in plain English, AI creates/runs/heals them. Web, mobile, API, desktop, Salesforce, SAP. Founded 2019, HQ San Francisco, ~196 employees. $12.8M total funding (Series A led by MassMutual Ventures).

## People
| Who | Role |
|-----|------|
| Rukmangada Kandyala | CEO & Founder |
| Pratheep Velicherla | Co-founder |
| Rajesh Reddy | Co-founder |
| Vikram Chaitanya | Co-founder |

## Key Product Terms
| Term | Meaning |
|------|---------|
| Atto | AI coworker — suite of agents (Generator, Sprint Planner, Runner, Analyzer, Healer, Optimizer) |
| Atto 2.0 | Nov 2025 release — intent-based self-healing, coverage discovery, risk analysis |
| NLP | Natural Language Programming — write tests in plain English |
| Copilot | GenAI assistant that generates tests from prompts, Figma, Jira, screenshots |
| Self-healing | AI auto-fixes broken locators/tests when UI changes (90% maintenance reduction) |

## Core Value Props
1. **Flaky/brittle tests** → AI self-healing. Story: Hansard cut regression 8→5 weeks
2. **Too much time creating/running tests** → Plain English + parallel execution. Story: Medibuddy 2,500 tests, 50% maintenance cut
3. **Can't scale coverage** → NLP + AI agent + cross-browser. Story: CRED 90% regression coverage, 5x faster

## Target Personas
| Title | Priority |
|-------|----------|
| QA Manager / QA Lead | Primary |
| Director/VP of QA | Primary |
| Software Eng Manager | Secondary |
| VP Engineering / CTO | Secondary (only with Buyer Intent) |
| Senior SDET / Automation Lead | Influencer (39.3% reply rate) |

## Top Verticals
SaaS/Tech, FinTech, Retail/E-Commerce, Healthcare/Digital Health, Telecom, Pharma

## Key Customers
Cisco, Samsung, Honeywell, Bosch, Nokia, Nestle, KFC, DHL, Zeiss, Axel Springer, NTUC Fairprice, Oscar Health, Sanofi, Spendflo, Nagra DTV, APA

---

## Tool Stack & Access Rules
| Tool | Status | Notes |
|------|--------|-------|
| LinkedIn Sales Navigator | Primary | Browser automation for prospecting + InMail |
| Apollo | Connected (MCP) | Enrichment-first. ~6,879 lead credits. |
| Gmail | Connected (MCP) | **Read/monitor only via MCP (replies, warm lead tracking). ALL outreach emails must be sent through Apollo UI using the robert.gorham@testsigma.com linked account — NOT directly via Gmail MCP. NEVER use rgorham369@gmail.com for work.** |
| Google Calendar | Connected (MCP) | Meeting scheduling |
| Google Drive | Connected (MCP) | File storage, batch trackers |
| Salesforce | SKIP | Too much 2FA. Use Apollo instead. |
| Slack | DO NOT CONNECT | Never take any visible action coworkers could see. |
| Chrome (Work/Blue) | Primary | **ALWAYS use blue/work Testsigma Chrome profile.** Never red/personal. |

---

## Hard Rules (NEVER violate)

### Chrome Browser
ALWAYS use Rob's blue/work Chrome browser (Testsigma profile). Never use red/personal for work tasks. Reuse tabs across sessions.

### Coworker Visibility
NEVER take any action visible to Rob's coworkers. No Slack messages, reactions, internal emails (unless Rob asks), or actions revealing Claude usage. Rob's AI use is private.

### Company Data Protection
NEVER modify, delete, alter, or overwrite existing company data. Read and enrich freely. Create new records freely. But modifying or deleting ANYTHING existing requires Rob's explicit per-item approval. If uncertain, STOP and ask.

### Send Approval
NEVER send any outreach without Rob's explicit "APPROVE SEND." Claude drafts, Rob reviews and executes. Exception: Rob explicitly says "APPROVE SEND" for a specific message.

### Draft Safety (from INC-001)
- Touch 2 drafts: NOT before Day 4 of sequence
- Touch 3 drafts: NOT before Day 9 of sequence
- Every prospect MUST exist in a batch tracker BEFORE any draft is created
- All drafts must use C2 structure and pass QA Gate (MQS >= 9/12)
- See `memory/incidents.md` for full cadence enforcement rules

---

## Do Not Contact List
| Name | Company | Reason | Date |
|------|---------|--------|------|
| Sanjay Singh | ServiceTitan | Hostile reply (2022 mabl era) | 2026-02-27 |
| Lance Silverman | Batch 5B | Polite decline. Re-engage after 60+ days with new trigger. | 2026-03-01 |
| Clyde Faulkner | CAMP Systems | mabl-era customer (2022). Had direct thread, knew Izzy. Skip permanently. | 2026-03-03 |
| Ashok Prasad | ZL Technologies | mabl-era contact (Sep 2022). 2 messages sent, no reply. Skip permanently. | 2026-03-03 |
| Abe Blanco | Kapitus | Replied "not interested" Mar 4. Batch 8 send. Skip permanently. | 2026-03-04 |
| Chuck Smith | Aventiv Technologies | Double-send (B1 connection + B5B InMail). Rob decision Mar 4. Skip permanently. | 2026-03-04 |
| Jitesh Biswal | JPMorgan Chase | Declined InMail Nov 4 (pre-campaign Oct 27 send). Skip permanently. | 2026-03-06 |

---

## Active Warm Leads
| Name | Company | Status | Last Action |
|------|---------|--------|-------------|
| Namita Jain | OverDrive | Monitoring for reply | Touch 1 email sent Feb 27. Follow-up due ~Mar 4. |
| Pallavi Sheshadri | Origami Risk | Warm reply | Rob replied Mar 2. Monitoring for response. |

→ Full details: `memory/warm-leads.md`

---

## Pipeline Status (Updated Mar 12 — post Batch 5 enrollment + audit)
| Metric | Value |
|--------|-------|
| Legacy batch prospects contacted (InMail/LI) | **206** (202 pre-Batch11 + 4 Batch 11 Mar 6) |
| TAM Outbound T1 sent (unique contacts) | **111** (Wave1: 23, Wave2: 16, Wave3: 35, Wave4: 37) + 9 Wave4 tasks pending + 5 Batch5 enrolled (pending T1) |
| MASTER_SENT_LIST.csv rows | **412** (updated Mar 11) |
| Total InMail sends (inc. double-sends) | 198 tracked + 17 untracked B9 + 9 Batch 10 + 4 Batch 11 = **228** |
| Total Emails sent | **~300+** — 74 pre-Mar10 + TAM Outbound Wave 1-4 (~135+ sends). See pipeline-state.md for detail. |
| InMail credits remaining | **4** (last updated Mar 6) |
| Batch 9 remaining | **2 to send** (Jyothi Kudithipudi, Axel Kerksiek — deferred) |
| Double-sends (cannot unsend) | Chuck Smith, Rick Kowaleski, Christie Howard, Mohan Gummadi, Yassi Dastan (Abe Blanco = DNC) |
| LinkedIn Outbound - Q1 Priority Accounts | **316 enrolled** (315 pre-Mar7 + 1 Gil Taub Mar 7) |
| TAM Outbound - Rob Gorham (69afff8dc8897c0019b78c7e) | **~130 enrolled** (Waves 1-4 + 5 Batch 5). 122 active, 10 bounced, 1 finished, 2 not sent. |
| Q1 QA Outreach - US | **RETIRED Mar 6** — 26 clean contacts migrated to LI Outbound, sequence archived |
| TAM Outbound bounces | Sucheth Ramgiri (Wave1 — SMTP 550), Ksenia Shchelkonogova (Wave4 — email invalid) |
| TAM Outbound T2 schedule | Wave1: **Mar 15** | Wave2: **Mar 15** | Wave3: **Mar 16** | Wave4: **Mar 19** |
| Yogesh Garg (Check Point) | Enrollment blocked — Apollo `contacts_without_ownership_permission` error. Needs manual ownership assignment in Apollo UI. |

**TAM Outbound wave files:**
- Wave1: `wave1-batch1-tracker-mar10.html` — Wave2: `tamob-wave2-draft-mar10.html`
- Wave3: `tamob-batch-20260311-1.html` — Wave4: `tamob-batch-20260311-2.html`
- Batch5: `tamob-batch-20260312-4.html` (13 drafted, 5 enrolled, 5 non-TAM removed, 2 phone-contact excluded, 1 ownership-blocked)

**Legacy batch notes:**
- Batch 9 duplicates removed: Jennifer Tune, Bhavani Neerathilingam, Sandy Paray (all in Batch 7 Feb 28)
- DNC violations (cannot unsend, monitor): Sanjay Singh + Lance Silverman sent in Batch 5B (Feb 27)
- Same-company flags: Saks Global (Batch 7), Greenway Health (Batches 7 + 9)
- Master sent list: `/Work/MASTER_SENT_LIST.csv` — cross-reference before every new batch build.

→ Full send log, batch index, follow-up schedule: `memory/pipeline-state.md`
→ Pre-batch dedup rules: `memory/sop-send.md` (Pre-Batch Build Checklist)
→ Incident log: `memory/incidents.md` (INC-001 through INC-008)
→ Full Mar 7 audit report: `/Work/audit-report-mar6.html`

---

## Reference Files (read on-demand when doing specific tasks)

| Task | File to Read |
|------|-------------|
| **Session startup (any task)** | `AGENTS.md` → `memory/session/handoff.md` → `memory/session/work-queue.md` → `memory/session/in-progress.md` → `memory/session/messages.md` |
| **Session closing (any task)** | `memory/playbooks/session-handoff.md` — update handoff.md, work-queue.md, session-log.md, deregister, commit |
| **Parallel session coordination** | `memory/session/active/_protocol.md` (session registry), `.locks/_protocol.md` (file locking), `memory/session/messages.md` (message board) |
| **New T1 batch** | `memory/playbooks/tam-t1-batch.md`, `memory/playbooks/apollo-enrollment.md`, `memory/playbooks/dedup-protocol.md`, `memory/playbooks/qa-gate.md`, `memory/playbooks/batch-tracker-html.md` |
| **T2 follow-ups** | `memory/playbooks/t2-followup.md`, `memory/playbooks/qa-gate.md` |
| **Apollo enrollment** | `memory/playbooks/apollo-enrollment.md`, `memory/playbooks/dedup-protocol.md` |
| **Apollo task queue sends** | `memory/playbooks/apollo-task-queue-sends.md` |
| **Sales Nav sourcing** | `memory/playbooks/sales-nav-deep-sweep.md` |
| **Error handling** | `memory/playbooks/error-recovery.md` |
| **Catchall domain decisions** | `memory/playbooks/catchall-domains.md` |
| **All playbooks (index)** | `memory/playbooks/_index.md` |
| Draft outreach messages | `memory/sop-outreach.md` |
| Send InMails via Sales Nav | `memory/sop-send.md` |
| Pre-batch dedup check | `MASTER_SENT_LIST.csv` + `memory/sop-send.md` Pre-Batch Checklist + `memory/playbooks/dedup-protocol.md` |
| Run the Daily workflow | `memory/sop-daily.md` |
| Check data-backed rules | `memory/data-rules.md` |
| Match proof points / objections | `memory/proof-points.md` |
| Check pipeline state / send log | `memory/pipeline-state.md` |
| Apollo sequences / email config | `memory/apollo-config.md` |
| Draft safety / incidents | `memory/incidents.md` |
| Warm lead handling | `memory/warm-leads.md` |
| Scoring, A/B, feedback loops | `memory/scoring-feedback.md` |
| Named accounts (TAM, Factors, Farming) | `memory/target-accounts.md` |

**Cowork Skills** (invoke as complete workflows):

| Skill | Location | Use When |
|-------|----------|----------|
| Session Start | `skills/session-start/SKILL.md` | Every session startup |
| TAM T1 Batch | `skills/tam-t1-batch/SKILL.md` | Building new outreach batches |
| Apollo Enroll | `skills/apollo-enroll/SKILL.md` | Creating contacts + enrolling in sequences |

**Rule:** Always read the relevant memory file(s) and playbooks BEFORE starting a task. Don't rely on cached knowledge from prior sessions.

---

## Preferences
- Conversational, consultative BDR style (not scripted)
- BANT + Techstack discovery framework
- Keep emails short (<150 words), one CTA, social proof
- NO em dashes. Use commas. Minimize hyphens.
- "What day works" as default CTA (40.4% reply rate)
- 75-99 words sweet spot for Touch 1 (39.0% reply rate)

## Current Operating Directive (Mar 12, 2026)
**Maximize new T1 pipeline volume. Factor accounts (intent) are HIGHEST priority.** Start every session with a new TAM T1 batch — source, research, draft, send. Prioritize untouched Factor accounts first, then TAM ICP=HIGH, then Medium. T2s and follow-up processing happen after T1 work is complete. Apollo handles the follow-up cadence automatically; the T1 pipeline requires active daily effort. Target: 25-50 new contacts enrolled every send day.

**⛔ TAM-ONLY RULE:** Only prospect from TAM (312) + Factor (38) accounts. Verify every contact's company domain against `tam-accounts-mar26.csv` before enrollment. See `sop-tam-outbound.md` Part 11 for the pre-enrollment verification gate.

## Google Drive Knowledge Base
| Document | ID |
|----------|-----|
| Objection Handling - Product | 1EDmrZO9ZK1rpYTMlZD1oL2DxtZIYrJY3UO9B_MRQkJU |
| Competitor Comparisons | 1yFYzrb1FdCOzI9FoVcN2MyfI_vfLOqGy-79SLgjJ0Kc |
| Persona Battle Cards | 1dqNe_q1RXuzXs4OD0TIEJwkplHk1UwabNQGIL3vpEOg |
| Simple Talk Tracks | 1lZhfvmxGfI12F64PCtejpHSdWOX_dI0gwr5MV3mGFgA |
| Trigger Event Playbook | 1e9DDmuOFtd9MgB1ol3MOJklzrq3vZn5oyevM6FAj_7I |
| Onboarding Assignment | 1JQ3_CgEAGgaL9H-geaLhXfkImIFcRNBQVaLVGZLz-bA |
| Objection Handling - AI | 1kGN-3bfmrFUclqIKCPky-eJ6ikqJYEBTApldxKiwCw4 |
| Objection Handling - Security | 1NAZqKAYKKLvJSo11kGxflqhvORW0BWXp0f7xGP1h0YQ |
| RFP Responses | 10l5kF9LtQwrax09BcOy_m3HhpjbXYdahSYliubiQvRQ |
| Full-Funnel BDR Scripts | 1yXGKZvy-7o78BxawYjng9H-F7DCBiQaudCZssgMlbjo |
| Salesforce Enablement v2 | 1bawvXns5ZSjWNvYkarikltH8aaNcUcSqw388Aks27CI |

## currentDate
Today's date is 2026-03-12.
