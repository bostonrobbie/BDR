# Testsigma BDR Outreach Repository

**Owner:** Rob Gorham, BDR | **Last Updated:** March 7, 2026

This repository contains the complete BDR outreach system for Testsigma, including SOPs, playbooks, templates, intelligence reports, and batch trackers. Everything is designed for a repeatable daily workflow assisted by Cowork (Claude desktop automation).

---

## Orientation: Where Everything Lives

| You need to... | Go to... |
|----------------|----------|
| Start a new session | `CLAUDE.md` → `AGENTS.md` → `memory/session/handoff.md` |
| See current pipeline state | `CLAUDE.md` header + `memory/pipeline-state.md` |
| Draft outreach | `TEMPLATE_LIBRARY.md` + `memory/sop-outreach.md` |
| Send InMails | `memory/sop-send.md` |
| Handle a reply | `reply-handling-playbook.docx` + `memory/warm-leads.md` |
| Check product/ICP | `testsigma-knowledge-bible.md` + `knowledge/` folder |
| Review reference playbooks | `sops/` folder |
| Find old batch data | `archive/batch-reports/` |

---

## Root-Level Active Files

### Core Ops

| File | What It Is |
|------|-----------|
| `CLAUDE.md` | Master config for every Cowork session. All rules, hard limits, pipeline state, ICP, tool access, and memory references. Start here. |
| `AGENTS.md` | Multi-agent collaboration rules. Read at session start so multiple Claude instances don't conflict. |
| `MASTER_SENT_LIST.csv` | Source of truth for all 278 prospects contacted. Cross-reference before every new batch build. |
| `OPERATIONAL-SAFETY-CHECKLIST.md` | Safety rules, send guardrails, and hard limits. Review before any batch send. |

### Active Batch Trackers (Mar 2026)

| File | Batch | Status |
|------|-------|--------|
| `outreach-batch10-sent-mar6.html` | Batch 10 (9 sent Mar 6) | Active — Touch 2 due Mar 11 |
| `outreach-batch11-draft-mar6.html` | Batch 11 (4 sent Mar 6) | Active — Touch 2 due Mar 11 |
| `outreach-batch10-draft-mar6.html` | Batch 10 draft version | Reference |
| `prospect-outreach-9-2026-03-03.html` | Batch 9 (sent Mar 3) | Complete |

### Intelligence & Analytics

| File | What It Is |
|------|-----------|
| `audit-report-mar6.html` | Full Mar 6–7 Apollo audit. B10/B11 status, enrollment blockers, credit state. |
| `bdr-intelligence-dashboard-2026-03-06.html` | Interactive pipeline dashboard. Prospect status, batch performance, reply tracking. |
| `daily-briefing-2026-03-06.html` | Mar 6 daily briefing. Most recent session reference. |
| `email-analytics-dashboard.html` | Email performance analytics across all sequences. |
| `testsigma-knowledge-bible.md` | Master Testsigma product knowledge: features, Atto AI agents, integrations, pricing. |

### Templates & Reference

| File | What It Is |
|------|-----------|
| `TEMPLATE_LIBRARY.md` | All InMail and Email templates, MQS-validated (≥9/12). Organized by pain hook. |
| `apollo-sequence-step-copy.md` | Step-by-step copy for Apollo sequences. Template selection + personalization variables. |
| `apollo-sequence-audit-mar3.md` | Apollo sequence audit results from Mar 3. Active sequence IDs and enrollment data. |
| `competitive-battlecards.docx` | 7 competitor battlecards with exact objection responses and best proof points. |
| `objection-handling-playbook.docx` | All objection responses. 5 categories + Acknowledge-Bridge-Ask framework. |
| `proof-point-reference-card.docx` | Quick lookup: pain type → customer story → stat. |
| `reply-handling-playbook.docx` | Reply classification, response templates, warm lead SOP, re-engagement triggers. |

### Trackers & Data

| File | What It Is |
|------|-----------|
| `Rob_Cold_Call_Tracker.xlsx` | Cold call tracking spreadsheet. Volume, connect rates, conversation notes. |
| `email-follow-up-candidates.csv` | Prospects flagged for email follow-up. |
| `weekly-prep-brief-2026-03-02.md` | Weekly prep brief from Mar 2. Reference for meeting/call context. |

### Infrastructure

| File | What It Is |
|------|-----------|
| `pyproject.toml` | Python project config. Dependencies, ruff lint, pytest settings. |
| `requirements.txt` | Minimal runtime requirements. |
| `Dockerfile` / `docker-compose.yml` | Container config for running the API locally. |
| `vercel.json` | Vercel deployment config for static assets. |

---

## Folder Structure

### `memory/` — Operational Brain
The living, per-session knowledge base. Always read relevant files here before starting any task.

| Path | What It Contains |
|------|-----------------|
| `memory/session/handoff.md` | Current state snapshot — read every session start |
| `memory/session/work-queue.md` | Active task queue with priorities |
| `memory/session/session-log.md` | Log of all sessions |
| `memory/pipeline-state.md` | Full send log, batch index, follow-up schedule |
| `memory/sop-outreach.md` | Message drafting rules, C2 structure, QA Gate |
| `memory/sop-send.md` | InMail send process, pre-batch dedup checklist |
| `memory/sop-daily.md` | Run-the-daily workflow |
| `memory/warm-leads.md` | Active warm leads and handling notes |
| `memory/incidents.md` | Incident log with cadence enforcement rules (INC-001–003) |
| `memory/apollo-config.md` | Apollo sequence IDs, email config, credit tracking |
| `memory/data-rules.md` | Data-backed rules and hard constraints |
| `memory/scoring-feedback.md` | A/B test results, feedback loops, performance data |
| `memory/proof-points.md` | Proof point matching and objection handling |

### `src/` — Application Code
FastAPI backend + agent layer. Not needed for day-to-day BDR work.

| Path | What It Contains |
|------|-----------------|
| `src/api/` | REST API: accounts, contacts, messages, email, LinkedIn, analytics |
| `src/agents/` | 20+ agent modules: scorer, message_writer, quality_gate, swarm_supervisor, etc. |
| `src/db/` | Database models + migrations (v1→v3) |
| `src/memory/` | Memory ingest, audit, classification, and loader |
| `src/config.py` | App-level configuration |

### `knowledge/` — Distilled Reference Docs
Clean, concise reference files for Claude sessions.

`company.md`, `icp.md`, `me.md`, `objections.md`, `outreach-rules.md`, `proof-points.md`, `scoring.md`, `sequences.md`, `workflows.md`, `data-insights.md`, `deliverable-format.md`

### `config/` — Scoring & Product Config (JSON)
Edit these to tune scoring without code changes.

| File | What It Contains |
|------|-----------------|
| `scoring_weights.json` | 7-dimension ICP scoring with thresholds and signal decay |
| `product_config.json` | Value props, proof points, customer stories by vertical |
| `vertical_pains.json` | Pain hypothesis library by industry |

### `sops/` — Standard Operating Procedures

| File | What It Is |
|------|-----------|
| `batch-qa-verification-sop.md` | Batch QA process — before every send |
| `batch-qa-verification-sop.docx` | Word version of batch QA SOP |
| `daily-prospecting-sop-v2.docx` | Daily execution guide: 7 phases, Sales Nav, Apollo, research, QA |
| `bdr-automation-pipeline-sop-v2.docx` | Full pipeline architecture (v2) |
| `email-sequence-sop.docx` | Email-only 5-touch 21-day cadence with Apollo config |
| `email-sequence-sop.html` | Interactive HTML version of email SOP |
| `linkedin-apollo-pipeline-sop.docx` | LinkedIn + Apollo combined pipeline SOP |
| `Rob_Prospecting_SOP.docx` | Comprehensive prospecting SOP |
| `Calls_Channel_SOP.docx` | Cold call channel SOP |
| `qa-gate-checklist.docx` | 14-point message validation checklist with MQS scoring |

### `plugins/` — Cowork Plugin Files
`.plugin` files for Cowork skills: `sales`, `marketing`, `finance`, `data`, `productivity`, `enterprise-search`.

### `tests/` — Test Suite
34 test files across unit and integration layers. CI runs on every push to `main` or `claude/*` via GitHub Actions (ruff lint + pytest).

### `batches/` — Raw Batch Data
Per-batch research and prospect data. `batches/email-sequences/` for Apollo sequence step copy.

### `scripts/` — Utility Scripts
Operational scripts: backfill, scoring, session startup, repo hygiene audit, LLM smoke test.
`scripts/archive/` — one-off fix scripts from earlier sessions.

### `data/` — Data Exports & Database
`outreach.db` (SQLite), LinkedIn exports, analysis outputs.

### `analytics/` — LinkedIn Analysis
LinkedIn conversation and performance analysis outputs.

### `archive/` — Historical Reference
Everything that's no longer active but kept for reference.

| Subfolder | Contents |
|-----------|---------|
| `archive/batch-reports/` | All batch analysis files, send trackers, prospect lists (B1–B9) |
| `archive/old-outreach-html/` | Superseded batch HTML trackers and .bak files |
| `archive/apollo-exports/` | Apollo data exports from Feb 2026 |
| `archive/research-intel/` | One-off research HTMLs (Mastercard, inbound leads, intent batches) |
| `archive/session-artifacts/` | Old summary docs, start-here files, completion notes |
| `archive/old-reports/` | Rob_* performance reports, outreach intelligence report |
| `archive/old-batches/` | Early batch HTML versions |
| `archive/json-data/` | Old JSON data exports |
| `archive/intermediate/` | Intermediate work files |

---

## System Architecture

```
Daily Workflow (2-3 hours per batch of 20-25 prospects):

Sales Navigator          Apollo MCP            Company Research
(saved searches)    →   (enrichment)      →   (3 parallel sources)
     ↓                       ↓                       ↓
Prospect List          Contact + Org Data       QA-Relevant Insights
     ↓                       ↓                       ↓
     └───────────→  Message Drafting (C2 Style)  ←───────┘
                            ↓
                     QA Gate (14 checks, MQS ≥9/12)
                            ↓
                     HTML Batch Tracker
                            ↓
                   Rob Reviews & Approves
                            ↓
                    Manual Send (12-1 PM)
                            ↓
                   Reply Handling & Tagging
                            ↓
                   Feedback → Next Batch
```

## Key Metrics (as of Mar 7, 2026)

- **Total unique prospects contacted:** 206
- **Emails sent (Gmail-confirmed):** 49
- **InMail credits remaining:** 4
- **Apollo lead credits:** ~6,879
- **LinkedIn Outbound Q1 enrolled:** 316
- **MASTER_SENT_LIST rows:** 278

---

*This index is maintained alongside `CLAUDE.md`. Update both when adding new documents or changing workflows.*
