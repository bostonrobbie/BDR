# Memory

## Me
Rob Gorham, BDR at Testsigma. I reach out to QA/testing leaders to book meetings and drive pipeline for our agentic AI test automation platform.

## Company
**Testsigma** — Agentic AI-powered unified test automation platform. Write tests in plain English, AI creates/runs/heals them. Web, mobile, API, desktop, Salesforce, SAP. Founded 2019, HQ San Francisco, ~196 employees. $12.8M total funding (Series A led by MassMutual Ventures).

## People
| Who | Role |
|-----|------|
| **Rukmangada Kandyala** | CEO & Founder, Testsigma |
| **Pratheep Velicherla** | Co-founder |
| **Rajesh Reddy** | Co-founder |
| **Vikram Chaitanya** | Co-founder |

## Key Product Terms
| Term | Meaning |
|------|---------|
| **Atto** | AI coworker — suite of agents (Generator, Sprint Planner, Runner, Analyzer, Healer, Optimizer) |
| **Atto 2.0** | Nov 2025 release — intent-based self-healing, coverage discovery, risk analysis |
| **NLP** | Natural Language Programming — write tests in plain English |
| **Copilot** | GenAI assistant that generates tests from prompts, Figma, Jira, screenshots |
| **Self-healing** | AI auto-fixes broken locators/tests when UI changes (90% maintenance reduction) |

## Core Value Props (3 Pain Hooks)
1. **Flaky/brittle tests** → AI self-healing. Story: Hansard cut regression 8→5 weeks
2. **Too much time creating/running tests** → Plain English + parallel execution. Story: Medibuddy 2,500 tests, 50% maintenance cut
3. **Can't scale coverage** → NLP + AI agent + cross-browser. Story: CRED 90% regression coverage, 5x faster

## Target Personas
| Title | Priority | Why |
|-------|----------|-----|
| QA Manager / QA Lead | Primary | Feels pain daily, authority to evaluate |
| Director/VP of QA | Primary | Strategic, has budget |
| Software Eng Manager | Secondary | Owns QA at companies w/o dedicated QA dept |
| VP Engineering / CTO | Secondary | Budget holder, strategic champion |
| Senior SDET / Automation Lead | Influencer | Technical champion, validates in trial |

## Top Verticals
SaaS/Tech, FinTech, Retail/E-Commerce, Healthcare/Digital Health, Telecom, Pharma

## Key Customers
Cisco, Samsung, Honeywell, Bosch, Nokia, Nestle, KFC, DHL, Zeiss, Axel Springer, NTUC Fairprice, Oscar Health, Sanofi, Spendflo, Nagra DTV, American Psychological Association

## Preferences
- Conversational, consultative BDR style (not scripted)
- BANT + Techstack discovery framework
- Use customer stories matched to prospect pain
- Keep emails short (<150 words), one CTA, social proof

---

## Tool Stack & Access Rules
| Tool | Status | Notes |
|------|--------|-------|
| LinkedIn Sales Navigator | Primary | Browser automation for prospecting + InMail |
| Apollo | Connected (MCP) | Enrichment-first, not sequence-first. |
| Gmail | Connected (MCP) | **ALWAYS send from robert.gorham@testsigma.com. NEVER use rgorham369@gmail.com for work.** |
| Google Calendar | Connected (MCP) | Meeting scheduling |
| Google Drive | Connected (MCP) | File storage, batch trackers |
| Salesforce | SKIP | Too much 2FA. Use Apollo instead. |
| Slack | DO NOT CONNECT | Never interact with Slack in any way. |
| Chrome (Work/Blue) | Primary browser | **ALWAYS use the blue/work Testsigma Chrome profile.** |

### Hard Rule: Chrome Browser Selection
**ALWAYS use Rob's blue/work Chrome browser (Testsigma profile) for all Cowork browser automation tasks.**
- **Blue = Work (Testsigma)** — Use for ALL Cowork tasks
- **Red = Personal** — NEVER use for work tasks

### Hard Rule: Coworker Visibility
**NEVER take any action that would be visible to Rob's coworkers.** No Slack messages, no internal emails (unless explicitly asked), no actions revealing Claude is being used. Rob's use of AI tools is private. Claude drafts, Rob executes.

### Hard Rule: Company Data Protection
**NEVER modify, delete, alter, or overwrite any existing company data.** Read and enrich freely. Create new records freely. Modifying or deleting ANYTHING that already exists requires Rob's explicit approval. If uncertain, STOP and ask Rob.

### Hard Rule: Send Approval
**NEVER send any outreach message without Rob's explicit approval.** Claude drafts everything. Rob reviews, approves, and executes the send manually (copy/paste). The only exception is if Rob explicitly says "APPROVE SEND" for a specific message.

---

## Modular File Reference

This codebase uses modular files to keep context lean. Skills load only what they need.

### Live Operational State (read/write by skills)
| File | What It Contains | Updated By |
|------|-----------------|------------|
| `work/pipeline-state.json` | Send totals, credit count, batch statuses, warm leads, Apollo sequences | All skills after actions |
| `work/dnc-list.json` | Do Not Contact list (queryable) | `/reply-handle` |
| `work/follow-up-schedule.json` | Computed follow-up dates per batch | `/follow-up`, send sessions |
| `work/reply-log.csv` | Reply classifications and tags | `/reply-handle` |
| `work/results.json` | Aggregated analytics (reply rates by persona, vertical, proof point) | `/pre-brief` |

### Rules & SOPs (read-only, loaded by skills on demand)
| File | What It Contains | Loaded By |
|------|-----------------|-----------|
| `.claude/rules/outbound-intelligence.md` | Data-driven rules: HC1-HC10, SP1-SP10, MQS scoring, QA Gate, phrase intelligence, patterns | `/score-message`, `/write-batch` |
| `.claude/rules/message-structure.md` | C2 message structure, pre-draft steps, writing rules, proof points, research requirements, objections | `/write-batch`, `/follow-up` |
| `.claude/rules/safety.md` | Draft cadence enforcement, LinkedIn compliance, incident log | `/follow-up`, send sessions |
| `.claude/rules/sops.md` | LinkedIn send SOP, Apollo integration, warm lead SOP, daily workflow, cycle logging | Specific skills as needed |

### Config (read-only, used by Python agents)
| File | What It Contains |
|------|-----------------|
| `config/product_config.json` | Testsigma product info, value props, proof points, forbidden phrases |
| `config/scoring_weights.json` | Lead scoring weights (20 dimensions) |
| `config/vertical_pains.json` | Per-vertical pain library (10 verticals) |

### Knowledge Base
| Directory | Contents |
|-----------|---------|
| `memory/competitors/` | Battle cards (Selenium, Cypress, Playwright, TOSCA, etc.) |
| `memory/wins/` | Successful sequence patterns |
| `memory/losses/` | Failed sequence analysis |
| `memory/call-notes/` | Prospect call insights |
| `memory/context/` | Sales playbook, product knowledge |

### Python Backend
| Component | Purpose |
|-----------|---------|
| `src/agents/` | 24 agent modules (research, scoring, writing, QA, delivery) |
| `src/api/app.py` | FastAPI server (REST + SSE streaming) |
| `src/db/models.py` | SQLite database (15 tables: accounts, contacts, messages, batches, etc.) |
| `src/memory/` | Knowledge ingestion and retrieval |
| `scripts/score_message.py` | CLI: Score a message against QA rules |
| `scripts/pre_brief.py` | CLI: Generate "What's Working" summary |
| `scripts/run_pipeline.py` | CLI: End-to-end batch pipeline |

---

## 3-Touch Outreach Cadence (Quick Reference)

Every prospect gets a 3-touch sequence. No cold calls. Claude drafts, Rob sends.

| Touch | Day | Channel | Words | Key Rule |
|-------|-----|---------|-------|----------|
| 1 | Day 1 | LinkedIn InMail | 80-120 | Full C2 structure, 2 question marks, "what day works" CTA |
| 2 | Day 5 | LinkedIn InMail Follow-up | 40-70 | New angle/proof point, lighter close |
| 3 | Day 10 | Email (if available) | 60-100 | Fresh approach, different proof point |

**Cadence enforcement:** See `.claude/rules/safety.md` for date-gating rules. Touch 2 drafts cannot be created before Day 4. Touch 3 drafts cannot be created before Day 9.

---

## Available Skills

| Command | What It Does | Key Files Loaded |
|---------|-------------|-----------------|
| `/prospect` | Source and qualify new prospects | `message-structure.md` (mix ratio, scoring) |
| `/write-batch` | Research + draft all touches for a prospect list | `message-structure.md`, `outbound-intelligence.md` |
| `/follow-up` | Check due follow-ups and draft them | `follow-up-schedule.json`, `pipeline-state.json` |
| `/reply-handle` | Triage and respond to prospect replies | `outbound-intelligence.md` (reply patterns) |
| `/pre-brief` | Analyze past batches before building new one | `results.json`, `pipeline-state.json` |
| `/score-message` | Run QA gate on a draft message | `outbound-intelligence.md` (HC, MQS, QA Gate) |
| `/log-reply` | Record a reply and update the feedback loop | `reply-log.csv`, `results.json`, `pipeline-state.json` |
