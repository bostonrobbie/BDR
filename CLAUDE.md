# Memory

## Multi-Agent Session System
This repo is worked on by multiple Claude agents. Full startup protocol (14 steps) is in `AGENTS.md` (v2.0). Read it first every session. End-of-session handoff protocol is in `memory/playbooks/session-handoff.md`.

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

### Apollo Send Safety (INC-007/008/012 — CRITICAL)
**NEVER use Quill API injection** (dangerouslyPasteHTML, setText, setContents) for Apollo email sends. Quill DOM is disconnected from Apollo's send payload. This has caused wrong-body sends THREE TIMES.
**Before EVERY "Send Now" click in Apollo:**
1. JS readback: `document.querySelector('.ql-editor').innerText.trim().slice(0, 120)` — must match approved draft
2. Zoom screenshot of body area — present to Rob
3. Wait for Rob's explicit "looks good" / "send it" (separate from content APPROVE SEND)
4. After send: verify via Gmail MCP within 60 seconds
**APPROVE SEND ≠ APPROVE CLICK.** Content approval and send-click are two separate gates.
Full rules: `memory/incidents.md` → INC-012, Rules 12-A through 12-E.

### Draft Safety (from INC-001)
- Touch 2 drafts: NOT before Day 4 of sequence
- Touch 3 drafts: NOT before Day 9 of sequence
- Every prospect MUST exist in a batch tracker BEFORE any draft is created
- All drafts must use C2 structure and pass QA Gate (MQS >= 9/12)
- See `memory/incidents.md` for full cadence enforcement rules

### TAM-Only Prospecting
Only prospect from TAM (312) + Factor (38) accounts. Verify every contact's company domain against `tam-accounts-mar26.csv` before enrollment. See `sop-tam-outbound.md` Part 11 for the pre-enrollment verification gate.

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
| Bret Wiener | Farmers Insurance | Prior meeting held. Stage = Connected, had [Archived Sequence] from earlier era. Skip permanently — do not re-enroll. | 2026-03-14 |

---

## Reference Files (read on-demand per task)

**Full SOP/playbook navigation:** `memory/README.md` — always start here if unsure which file to read.

| Task | File to Read |
|------|-------------|
| **Session startup** | `AGENTS.md` → `memory/session/handoff.md` → `memory/session/work-queue.md` → `memory/session/in-progress.md` → `memory/session/messages.md` |
| **Session closing** | `memory/playbooks/session-handoff.md` |
| **Parallel sessions** | `memory/session/active/_protocol.md`, `.locks/_protocol.md`, `memory/session/messages.md` |
| **All playbooks** | `memory/playbooks/_index.md` (index with use-when guidance for all 12 playbooks) |
| **Pipeline state** | `memory/session/handoff.md` (snapshot) + `memory/pipeline-state.md` (full log) |
| Daily workflow | `memory/sop-daily.md` |
| TAM outbound (end-to-end) | `memory/sop-tam-outbound.md` |
| Prospecting / batch build | `memory/sop-prospect.md` + `memory/playbooks/tam-t1-batch.md` |
| Draft LinkedIn outreach | `memory/sop-outreach.md` |
| Draft email outreach | `memory/sop-email.md` |
| Send InMails | `memory/sop-send.md` |
| Inbound Salesforce leads | `memory/playbooks/inbound-leads-sequence.md` |
| Enroll contacts in Apollo | `memory/playbooks/apollo-enrollment.md` |
| Send via Apollo task queue | `memory/playbooks/apollo-task-queue-sends.md` |
| Write T2 follow-ups | `memory/playbooks/t2-followup.md` |
| Pre-batch dedup | `MASTER_SENT_LIST.csv` + `memory/playbooks/dedup-protocol.md` |
| Post-call follow-up email | `memory/sop-post-call-followup.md` |
| Handle warm reply | `memory/warm-leads.md` |
| Data rules | `memory/data-rules.md` |
| Proof points | `memory/proof-points.md` |
| Apollo config | `memory/apollo-config.md` |
| Incidents | `memory/incidents.md` |
| Scoring/feedback | `memory/scoring-feedback.md` |
| Target accounts | `memory/target-accounts.md` |
| Email analytics | `memory/email-analytics-sop.md` |

**Cowork Skills** (repeatable workflows):

| Skill | Location | Use When |
|-------|----------|----------|
| Session Start | `skills/session-start/SKILL.md` | Every session startup |
| TAM T1 Batch | `skills/tam-t1-batch/SKILL.md` | Building new outreach batches |
| Apollo Enroll | `skills/apollo-enroll/SKILL.md` | Creating contacts + enrolling in sequences |
| Reply Classifier | `skills/reply-classifier/SKILL.md` | Check Gmail for new replies, classify, surface warm leads |
| Batch Dashboard | `skills/batch-dashboard/SKILL.md` | Consolidated pipeline view across all batches |
| Enrichment Pipeline | `skills/enrichment-pipeline/SKILL.md` | TAM verify + Apollo enrich + compliance in one flow |
| Trigger Monitor | `skills/trigger-monitor/SKILL.md` | Scan accounts for QA hiring, funding, leadership changes |
| Draft QA | `skills/draft-qa/SKILL.md` | Auto-score drafts against 12-point MQS rubric |
| Reply Router | `skills/reply-router/SKILL.md` | Match reply to objection doc, draft response |
| Lifecycle Tracker | `skills/lifecycle-tracker/SKILL.md` | Unified contact history from enrichment to outcome |
| Analytics Engine | `skills/analytics-engine/SKILL.md` | Reply rate analytics by persona, vertical, proof point |
| Handoff Auto | `skills/handoff-auto/SKILL.md` | Auto-generate session handoff docs at end of session |
| Compliance Gate | `skills/compliance-gate/SKILL.md` | 8-point safety check before any enrollment |
| **Apollo Send** | `skills/apollo-send/SKILL.md` | Execute Apollo task queue sends with INC-012 two-gate protocol |
| **Batch JSON Builder** | `skills/batch-json-builder/SKILL.md` | After APPROVE SEND: parse tracker HTML → generate batch{N}_sends.json |
| **Stage Monitor** | `skills/stage-monitor/SKILL.md` | Daily T2/T3 due-date check, bounce scan, warm lead surface |
| **T2 Draft Generator** | `skills/t2-draft-generator/SKILL.md` | ⚠️ LOCKED — stub only, pending T2 formula finalization |
| **Auto Prospect + Enroll** | `skills/auto-prospect-enroll/SKILL.md` | Full automated pipeline: account select → prospect → compliance gate → draft → MQS → enroll → sends.json |
| **Warm Lead Re-Engagement** | `skills/warm-lead-reengagement/SKILL.md` | Monthly scan of P2/P3 contacts whose re-engage window has passed — surfaces actionable contacts |
| **Post-Send Verifier** | `skills/post-send-verifier/SKILL.md` | Verifies Apollo sends landed in Gmail Sent — catches silent failures |
| **Objection Trend Digest** | `skills/objection-trend-digest/SKILL.md` | Weekly objection pattern analysis — surfaces rising/falling objection types and messaging recommendations |

**Scheduled Tasks** (all registered in Cowork Scheduled sidebar — none send anything):

| Task | Schedule | Purpose |
|------|----------|---------|
| morning-briefing | Weekdays 6:00 AM | Overnight replies + calendar + T2/T3 due + warm leads + work queue → writes to messages.md |
| trigger-monitor | Mon/Wed/Fri 6:10 AM | Scan Factor + TAM HIGH for QA hiring, funding, leadership changes |
| auto-prospect-enroll | Mon/Wed/Fri 6:30 AM | Auto-prospect TAM contacts, compliance + QA gate, enroll clean contacts, build sends.json |
| stage-monitor | Weekdays 6:20 AM | T2/T3 due-date check, bounce scan, pipeline snapshot |
| reply-classifier | Weekdays 9am,11am,1pm,3pm,5pm | Full Gmail reply scan, classify P0-P4, update warm-leads.md |
| weekly-analytics | Fridays 5:00 PM | Sync sends + replies + calls → compute metrics → refresh bdr-analytics-dashboard.html |
| warm-lead-reengagement | Monthly, 1st at 6:05 AM | P2/P3 re-engagement window scanner → writes to messages.md |
| post-send-verifier-noon | Weekdays 12:00 PM | Mid-day Gmail Sent verification for morning Apollo sends |
| post-send-verifier-eod | Weekdays 5:30 PM | End-of-day final verification for all day's Apollo sends |
| objection-trend-digest | Fridays 5:15 PM | Weekly reply objection tally — rising/falling patterns + messaging recommendations |

**Analytics Infrastructure** (initialized Mar 14, 2026):

| File | Purpose |
|------|---------|
| `analytics/outreach.db` | SQLite DB — outreach_sends, call_activity, weekly_summary, warm_leads_log tables |
| `bdr-analytics-dashboard.html` | Combined email + LinkedIn + call performance dashboard (regenerated weekly) |
| `memory/call-log.md` | Manual call activity log — Rob fills in dials/connects/meetings, weekly-analytics syncs to DB |

**New Data Files** (initialized Mar 12, 2026):

| File | Purpose |
|------|---------|
| `memory/contact-lifecycle.md` | Unified contact timeline from discovery to outcome |
| `Work/pipeline-dashboard.html` | Generated by batch-dashboard skill (regenerate on demand) |

**Rule:** Always read the relevant files BEFORE starting a task. Don't rely on cached knowledge from prior sessions.

---

## Preferences
- Conversational, consultative BDR style (not scripted)
- BANT + Techstack discovery framework
- Keep emails short (<150 words), one CTA, social proof
- NO em dashes. Use commas. Minimize hyphens.
- "What day works" as default CTA (40.4% reply rate)
- 75-99 words sweet spot for Touch 1 (39.0% reply rate)

## Current Operating Directive
**Maximize new T1 pipeline volume. Factor accounts (intent) are HIGHEST priority.** Start every session with a new TAM T1 batch. Prioritize Factor accounts first, then TAM ICP=HIGH, then Medium. T2s and follow-ups happen after T1 work. Target: 25-50 new contacts enrolled every send day.

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
