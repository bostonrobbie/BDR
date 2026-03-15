# BDR Outreach Command Center - Architecture Map

**Generated:** 2026-02-22 | **Author:** Claude Code Audit

---

## System Overview

```
 REMOTE PC (Browser)                    VERCEL CLOUD                         SERVER PC (Rob's Desktop)
+---------------------+          +-------------------------+          +------------------------------+
|                     |          |                         |          |                              |
|  Vercel Dashboard   | <------> |  FastAPI Serverless     | <------> |  SQLite (outreach.db)       |
|  (React SPA)        |   HTTPS  |  api/index.py           |   Blob   |  950KB, 60+ tables          |
|  public/index.html  |          |  217 routes             |   Sync   |                              |
|  9,858 lines        |          |  /tmp/outreach.db       |          +------------------------------+
|                     |          |  (serverless copy)      |          |                              |
+--------|------------+          +-----------|-------------+          |  Ollama (qwen2.5:7b)        |
         |                                   |                        |  localhost:11434             |
         | Gateway calls (LLM)               |                        |                              |
         |                                   |                        +--------|---------------------+
         v                                   |                                 |
+---------------------+                      |                        +--------|---------------------+
|  Cloudflare Tunnel  | <----- quick mode ---+                        |  OCC Gateway (FastAPI)      |
|  *.trycloudflare.com|                                               |  port 8765, 78 routes       |
|  (temporary URL)    | --------- QUIC/H2 tunnel ------------------> |  src/api/app.py             |
+---------------------+                                               |  + watchdog + tunnel mgr    |
                                                                      +------------------------------+
```

## Two Repos, One System

| Repo | Path | Purpose | Deployment |
|------|------|---------|------------|
| **BDR** | `~/BDR` | Dashboard + Vercel API | Vercel serverless (`bdr-outreach.vercel.app`) |
| **occ-bdr** | `~/occ-bdr` | Local LLM gateway + server | Local uvicorn + Cloudflare tunnel |

## Request Flow

### 1. Dashboard Page Load
```
Browser -> Vercel CDN -> public/index.html (static React SPA)
```

### 2. API Calls (CRUD, analytics)
```
Browser -> Vercel -> api/index.py -> /tmp/outreach.db (SQLite)
```
The Vercel function copies a seed DB from `api/data/outreach_seed.db` on cold start, then applies schema migrations. Data persists via Vercel Blob (`/api/state/blob-save`).

### 3. LLM Calls (enhance, research, write)
```
Browser JS -> _gatewayCall() -> Cloudflare Tunnel URL -> occ-bdr FastAPI -> Ollama -> qwen2.5:7b
```
The gateway URL and key are stored in:
- **Vercel DB:** `gateway_config` table (via `/api/gateway/config`)
- **Browser:** `localStorage` keys `occ_gateway_url` and `occ_gateway_key`

### 4. Database Persistence (Vercel)
```
Vercel /tmp/outreach.db -> /api/state/blob-save -> Vercel Blob Storage
Cold start -> /api/state/blob-restore -> /tmp/outreach.db
```

## Key Services & Ports

| Service | Host | Port | Purpose |
|---------|------|------|---------|
| Vercel Dashboard | `bdr-outreach.vercel.app` | 443 | Frontend + API |
| OCC Gateway | `localhost` | 8765 | LLM relay + local CRUD |
| Ollama | `localhost` | 11434 | Local LLM inference |
| Cloudflare Tunnel | `*.trycloudflare.com` | 443 | Proxies to :8765 |
| Cloudflare Metrics | `localhost` | 20241 | Tunnel health metrics |

## Environment Variables

### BDR (Vercel) - `.env.local`
| Var | Purpose | Current |
|-----|---------|---------|
| `OCC_DB_PATH` | SQLite path | `/tmp/outreach.db` (auto-set) |
| `VERCEL_OIDC_TOKEN` | Vercel auth | Set in Vercel env |

### occ-bdr (Server) - `.env`
| Var | Purpose | Current |
|-----|---------|---------|
| `OCC_GATEWAY_PORT` | Gateway listen port | `8765` |
| `OCC_GATEWAY_KEY` | Auth header value | `occ-rob-2026-gateway` |
| `OLLAMA_URL` | Ollama endpoint | `http://localhost:11434` |
| `OLLAMA_MODEL` | Model for LLM calls | `qwen2.5:7b` |
| `OCC_DB_PATH` | SQLite path | `outreach.db` |

## Database Schema

### BDR (Vercel) - 60+ tables, 950KB
Core tables with data: `accounts` (48), `contacts` (49), `message_drafts` (250), `research_snapshots` (102), `batches` (1), `workflow_definitions` (7)

### occ-bdr (Server) - 17 tables, 225KB
Mostly empty - intended as local working copy. Only `contacts` (1) has data.

## Authentication

- **No user auth** - This is a single-user local-first tool
- **Gateway auth:** `x-occ-key` header required for LLM endpoints
- **Vercel:** Public by default (Vercel Deployment Protection available)

## LLM Integration

### Tier 1: Rule-based enhancement (no LLM needed)
- `POST /api/messages/{id}/enhance` - Applies regex fixes, em-dash removal, word count checks
- Works offline, instant response

### Tier 2: LLM-powered enhancement (requires gateway)
- `POST /api/drafts/{id}/enhance` - Full rewrite using research data + proof points
- Template-based rewrite engine on Vercel side
- `POST /llm/enhance` (gateway) - Direct Ollama call for deep rewriting
- `POST /llm/research` (gateway) - Research generation via Ollama
- `POST /llm/write` (gateway) - Message drafting via Ollama

### Agent Swarm (10 agents, defined in `src/agents/`)
Prospector, Researcher, Signal Scanner, Message Writer, Sequencer, Call Prep, Reply Triage, Quality Gate, Pre-Brief, Insights

## Frontend Architecture

Single HTML file (`public/index.html`, 9,858 lines) with:
- React via CDN (no build step)
- Chart.js for analytics
- 12+ page views (nav-driven SPA)
- Dark theme (Indigo accent `#6366f1`)
- `_gatewayCall()` function for LLM operations
- `api()` helper for Vercel backend calls

## Dashboard Pages
1. **Home** - Command center with stats, action queue, pipeline snapshot
2. **Pipeline** - Prospect table with filters and detail panel
3. **LinkedIn Workspace** - Batch manager, prospect cards, editor
4. **Email Workspace** - Email queue, draft composer
5. **Calls Workspace** - Call queue, snippets, outcomes
6. **Accounts & Contacts** - CRM management
7. **Research & Signals** - Buyer intent, research snapshots
8. **Drafts & Sequences** - Message library, versioning
9. **Experiments** - A/B test config and results
10. **Intelligence** - Analytics: reply rates, funnel, attribution
11. **Agent Logs** - Run history, QA flags
12. **Settings** - SOPs, templates, LLM Gateway config
