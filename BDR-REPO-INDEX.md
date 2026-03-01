# Testsigma BDR Outreach Repository

**Owner:** Rob Gorham, BDR | **Last Updated:** March 1, 2026

This repository contains the complete BDR outreach system for Testsigma, including SOPs, playbooks, templates, intelligence reports, and batch trackers. Everything is designed for a repeatable daily workflow assisted by Cowork (Claude desktop automation).

---

## How to Use This Repo

**New to the system?** Read these in order:

1. `daily-prospecting-sop-v1.docx` — The daily step-by-step execution guide (start here)
2. `bdr-automation-pipeline-sop.docx` — The overall pipeline architecture and strategy
3. `TEMPLATE_LIBRARY.md` — All message templates with quality scores
4. `proof-point-reference-card.docx` — Quick lookup: pain type to customer story
5. `competitive-battlecards.docx` — What to say when prospects mention competitors

**During outreach sessions:** Keep these open:

- `qa-gate-checklist.docx` — 14-point message validation (printable)
- `proof-point-reference-card.docx` — Which story to use for which pain
- `objection-handling-playbook.docx` — Ready responses for every objection type

**When prospects reply:** Reference:

- `reply-handling-playbook.docx` — Classification, templates, warm lead SOP

---

## Core Documents (SOPs & Playbooks)

| File | What It Is |
|------|-----------|
| `daily-prospecting-sop-v1.docx` | Step-by-step daily execution guide: 7 phases from sourcing to send-ready batch (2-3 hours). Includes Sales Navigator saved search IDs, Apollo MCP commands, parallel research workflow, QA Gate automation, and daily iteration framework. |
| `bdr-automation-pipeline-sop.docx` | Overall pipeline architecture (v3.0). Covers the full system: C2 message structure, 3-touch sequence, research pipeline, batch assembly, send loop, tracking, and feedback loop. |
| `email-sequence-sop.docx` | Email-only sequence playbook for BDR-wide Apollo use. 5-touch 21-day cadence, template selection, Apollo configuration. |
| `email-sequence-sop.html` | Interactive HTML version of the email SOP with 8 tabs. |

## Reference Cards & Playbooks

| File | What It Is |
|------|-----------|
| `competitive-battlecards.docx` | 7 competitor battlecards (Selenium, Cypress, Playwright, Tricentis, Provar, AccelQ, Copado). Each has: overview, when you'll encounter them, Testsigma advantages, their strengths, exact objection response, and best proof point. Summary comparison table at the end. |
| `objection-handling-playbook.docx` | Consolidated objection responses from all sources. 5 categories: Tool/Competitor, Priority/Budget, Compliance/Security, Timing/Interest, plus the universal Acknowledge-Bridge-Ask framework. |
| `proof-point-reference-card.docx` | One-page quick reference. 3 tables: Master Proof Point Library (12 customer stories with stats and best verticals), Pain-to-Proof-Point Quick Lookup, and Stat Framing Rules (reduction vs. multiplier data). |
| `reply-handling-playbook.docx` | What to do when prospects respond. Reply classification (8 types with % breakdown), response templates, warm inbound lead SOP, meeting booking best practices, re-engagement triggers, and reply tagging system. |
| `qa-gate-checklist.docx` | Printable 14-point message validation checklist with pass/fail criteria and common failures. Includes MQS scoring reference (4 dimensions, 12-point scale). |

## Intelligence & Analytics

| File | What It Is |
|------|-----------|
| `outreach-intelligence-report.docx` | Deep analysis of 1,326 LinkedIn conversations. Hard constraints, strong preferences, timing optimization, word count curves, pattern differentials, phrase-level intelligence, persona reply rates. The data foundation for everything else. |
| `outreach-intelligence.html` | Interactive HTML version of the intelligence report. |
| `linkedin-outreach-analysis.docx` | LinkedIn-specific outreach analysis and channel performance. |
| `batch-performance-summary.docx` | Aggregate stats across all 8 batches (148 sends, Feb 13-28, 2026). Volume by batch, pipeline status, process metrics, key learnings, DNC list. |
| `testsigma-knowledge-bible.md` | Master Testsigma product knowledge: features, Atto AI agents, integrations, pricing, deployment options. Used as source material for message drafting. |

## Templates & Sequence Copy

| File | What It Is |
|------|-----------|
| `TEMPLATE_LIBRARY.md` | Master template library v2.0. All InMail and Email templates, MQS-validated (>= 9/12). Organized by pain hook (maintenance, velocity, coverage, migration, trigger event). |
| `apollo-sequence-step-copy.md` | Step-by-step copy guide for Apollo sequences. Template selection, personalization variables, rotation matrix. |

## Batch Trackers (Active)

| File | Batch | Status |
|------|-------|--------|
| `outreach-sent-feb13-batch1-v2.html` | Batch 1 (rebuild) | Complete |
| `outreach-sent-feb26-batch3.html` | Batch 3 (24 sent) | Complete |
| `outreach-sent-feb27-batch5a.html` | Batch 5A - FinServ (25 sent) | Complete |
| `outreach-sent-feb27-batch5b.html` | Batch 5B - Multi-vertical (23 sent) | Complete |
| `outreach-batch6-unsent.html` | Batch 6 (27 sent) | Complete |
| `batch7-send-tracker.html` | Batch 7 (41 sent) | Complete |
| `batch7-send-tracker.json` | Batch 7 structured data | Complete |
| `outreach-batch8-unsent.html` | Batch 8 (19 prospects, unsent) | Ready for Review |

## Operational Files

| File | What It Is |
|------|-----------|
| `CLAUDE.md` | Master configuration for Cowork sessions. All SOPs, rules, outreach intelligence, writing constraints, tool access, and memory in one file. This is the "brain" that powers each Cowork session. |
| `daily-work-log.html` | Interactive daily work log. Searchable, filterable by category and date range. Add entries manually or via Cowork. Export to Markdown, CSV, or JSON. Pre-loaded with all activity from Feb 13 onward. |
| `daily-outreach-workflow.html` | Visual reference for the "Run the Daily" workflow. 5-phase pipeline with adaptive logic, weekly rhythm, and velocity targets. |
| `daily-execution-guide-2026-02-26.html` | Daily outreach limits, 14-day send schedule, copy-paste workflow, safety guardrails. |
| `intent-outreach-pipeline-2026-02-26.html` | Intent-based outreach command center: transferred accounts, intent signals, lead assignments. |
| `EXECUTION-STATUS.md` | Current execution status tracker. |

## Account Research

| File | What It Is |
|------|-----------|
| `mastercard-account-map.html` | Mastercard account mapping and research. |
| `call-prep-joe-casale-lexia-2026-02-26.md` | Call prep for Joe Casale at Lexia Learning. |
| `moderna-qa-research-deep-dive.md` | Moderna QA team research and intel. |

## Archive

The `archive/` folder contains superseded batch tracker versions and intermediate files from earlier iterations. These are kept for reference but are not part of the active workflow.

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
                     QA Gate (14 checks)
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

## Key Metrics (as of Feb 28, 2026)

- **Total sends:** 148 across 8 batches
- **InMail credits remaining:** ~24
- **Message quality:** All messages MQS >= 9/12
- **Research sources per prospect:** 3 (LinkedIn, Apollo, Company)
- **Touch sequence:** 3-touch (2 InMail + 1 Email)
- **Target reply rate:** 28.7% (based on historical data)

---

*This index is maintained alongside the CLAUDE.md master configuration. Update both when adding new documents or changing workflows.*
