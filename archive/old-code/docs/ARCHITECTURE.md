# Outreach Command Center - Architecture Document

## System Overview

The Outreach Command Center (OCC) is a local-first, browser-based BDR operations platform that consolidates LinkedIn, Email, and Calls into a single dashboard. It uses an agent swarm architecture where specialized AI agents handle research, drafting, quality control, and analysis, while Rob manually executes all outreach.

### What It Does
- Researches prospects and companies using structured extraction
- Drafts personalized, human-sounding outreach for all channels
- Tracks every touchpoint, reply, and outcome in a SQLite database
- Learns from accumulated data to improve over time
- Manages follow-up sequences and call prep
- Runs A/B experiments on messaging variables
- Generates analytics and pre-briefs before each batch

### What It Does NOT Do
- Send messages or emails (Rob copies, pastes, and sends manually)
- Log into platforms autonomously
- Make financial transactions
- Violate any platform terms of service

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | React (single HTML via CDN) | No build step, opens in any browser |
| Backend API | Python FastAPI | Lightweight, async, easy to extend |
| Database | SQLite | Zero config, file-based, portable |
| Agent Engine | Claude via Cowork | Research, drafting, analysis |
| Browser Bridge | Claude in Chrome MCP | Reads Sales Navigator pages |

## Core Design Principles

1. **Human in the Loop** - Claude researches and drafts. Rob reviews, edits, and sends.
2. **Opportunity Focused** - Every metric traces to opportunities created, not vanity counts.
3. **Sounds Like Rob** - No em dashes, no feature dumps, warm and specific.
4. **Compounding Intelligence** - Every touchpoint feeds the learning loop.
5. **Token Efficient** - Cache company profiles, reuse research, version message blocks.
6. **Local First** - Everything runs on Rob's machine.

## Pages and Navigation

| Page | Purpose |
|------|---------|
| Home | Daily cockpit: action queue, pipeline snapshot, pre-brief, hot prospects, reply queue |
| Pipeline | Unified prospect table with filters, sorting, right-side detail panel |
| LinkedIn Workspace | Primary prospecting: batch manager, prospect cards, research panel, message editor |
| Email Workspace | Email queue, draft composer, thread view, follow-up calendar |
| Calls Workspace | Call queue, 3-line snippets, outcome buttons, post-call notes |
| Accounts & Contacts | CRM-lite: account and contact management, research history |
| Research & Signals | Buyer intent signals, job postings, funding, leadership changes |
| Drafts & Sequences | Message library, sequence management, template versioning |
| Experiments | A/B test configuration, results, experiment history |
| Intelligence | Analytics dashboard: reply rates, funnel conversion, attribution |
| Agent Logs | Run history, QA flags, token usage, error tracking |
| Settings | SOPs, templates, voice rules, qualification criteria |

## Agent Swarm Architecture

See [AGENT_SWARM.md](./AGENT_SWARM.md) for the full agent design.

## Data Model

See [DATA_MODEL.md](./DATA_MODEL.md) for the complete database schema.
