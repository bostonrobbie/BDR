# BDR Outreach Command Center - Run Report

**Date:** 2026-02-22 | **Duration:** ~45 minutes | **Auditor:** Claude Code (Opus 4.6)

---

## Executive Summary

Full end-to-end audit of the BDR Outreach Command Center across both repos (`~/BDR` Vercel dashboard and `~/occ-bdr` local LLM gateway). **76 tests executed, all passing.** 7 bugs found and fixed. The system is **fully operational** and accessible from a remote PC.

---

## What Was Tested

### Phase 0: Architecture Recon
- Mapped both repos: `BDR` (Vercel, 221 API routes, 60+ DB tables) and `occ-bdr` (local gateway, 78 routes, 17 DB tables)
- Created `docs/ARCHITECTURE_MAP.md` documenting request flows, ports, env vars, and LLM integration
- Identified the two-tier architecture: Vercel for data/UI, local gateway for LLM via Cloudflare tunnel

### Phase 1: Environment Validation
- **Python 3.14** - confirmed
- **Ollama v0.15.6** - running with qwen2.5:7b (4.7GB) model
- **cloudflared v2025.8.1** - installed
- **Gateway** - started on port 8765, healthy with 17 DB tables
- **Cloudflare Tunnel** - quick mode, URL: `https://operating-translate-lonely-scientist.trycloudflare.com`
- **Vercel** - project `bdr-outreach` with 20 consecutive successful deployments

### Phase 2: API QA (32 endpoint tests)
- Tested every major API endpoint on Vercel
- Found 7 bugs (see BUG_LOG.md), all fixed
- All 30 final endpoint tests passing

### Phase 3-4: Enhancement and LLM Flow
- Tier 1 (rule-based) enhance: working - returns auto-fixes and tier 2 prompt
- Tier 2 (template-based) enhance: working - rewrites drafts using research, proof points, pain hooks
- LLM via tunnel: all 3 endpoints working (`/llm/enhance`, `/llm/research`, `/llm/write`)
- Response times: 3.5-5.1 seconds for LLM calls through tunnel

### Phase 5: Remote Access Validation
- Vercel dashboard loads remotely via `bdr-outreach.vercel.app`
- Gateway accessible via Cloudflare tunnel
- LLM operations work end-to-end from remote
- Gateway config saved to Vercel DB so settings persist

### Phase 6: Vercel Deployment
- Latest commit deployed automatically via GitHub push
- Build state: READY
- All 20 historical deployments: READY (zero failures)
- Routes: 221 active API routes

---

## What Passed

| Area | Count | Details |
|------|-------|---------|
| Infrastructure | 14/14 | Python, Ollama, cloudflared, gateway, tunnel, Vercel all healthy |
| Database | 9/9 | Both DBs intact, 48 accounts, 49 contacts, 250 drafts, 102 research snapshots |
| API Endpoints | 30/30 | All CRUD, analytics, intelligence, workflow, gateway endpoints working |
| Enhancement | 6/6 | Both tier 1 and tier 2 enhance produce correct output |
| LLM Gateway | 5/5 | All LLM endpoints respond through tunnel with auth |
| Remote Access | 5/5 | Dashboard, API, tunnel, LLM all accessible remotely |
| Vercel Deploy | 7/7 | Build succeeds, static + API routes work, DB seeds correctly |

---

## What Failed (and Was Fixed)

| Bug | Severity | Fix |
|-----|----------|-----|
| BUG-001: Channel filter ignored on /api/messages | HIGH | Added `channel` query param and SQL filter |
| BUG-002: Missing GET /api/messages/{id} | MEDIUM | Added single-message endpoint with joins |
| BUG-003: Missing /api/research-snapshots | MEDIUM | Added list endpoint with filters |
| BUG-004: Missing /api/contacts/{id}/research | MEDIUM | Added contact research endpoint |
| BUG-005: GET /api/drafts/{id} broken | MEDIUM | Rewrote to use message_drafts as primary source |
| BUG-006: Missing /api/drafts/{id}/versions | LOW | Added dedicated versions endpoint |
| BUG-007: Duplicate route /api/drafts/{id}/research | LOW | Renamed first instance to /research-compact |

---

## What Needs User Action

| Item | Action Required |
|------|----------------|
| **Gateway URL changes on restart** | Quick tunnel generates new URL each time. Options: (1) Update Settings > LLM Gateway after each restart, (2) Set up named tunnel with permanent URL via `server-install-tunnel.bat` |
| **Vercel Blob persistence** | Set `BLOB_READ_WRITE_TOKEN` env var in Vercel to enable auto-persist across cold starts |
| **Ollama update available** | v0.16.3 available (current: v0.15.6). Optional upgrade. |

---

## Changelog

### Commit: `3e4641f` (2026-02-22)
**Fix 7 API bugs: channel filter, missing endpoints, duplicate routes**

Files changed:
- `api/index.py` (+90 lines) - 4 new endpoints, 2 fixes, 1 dedup
- `docs/ARCHITECTURE_MAP.md` (new) - Full system architecture documentation
- `docs/BUG_LOG.md` (new) - Detailed bug log with reproduction steps and fixes

New endpoints added:
- `GET /api/messages/{message_id}` - Single message with contact/company context
- `GET /api/research-snapshots` - List research snapshots with filters
- `GET /api/contacts/{contact_id}/research` - Contact person + company research
- `GET /api/drafts/{draft_id}/versions` - Draft version history

Fixes applied:
- `/api/messages` now respects `?channel=` filter parameter
- `/api/drafts/{id}` now queries `message_drafts` table (not just `draft_versions`)
- Duplicate `/api/drafts/{id}/research` route renamed to `/research-compact`

---

## Evidence

### Vercel Deployment
- Deploy ID: `dpl_RStZqu8Fohyya6NtT4NKNzTqFv3h`
- State: READY
- URL: `https://bdr-outreach.vercel.app`
- Build triggered by push to `main` branch

### Gateway Health
```json
{"status":"healthy","tables":17,"db_path":"outreach.db"}
```

### LLM Status (via tunnel)
```json
{"gateway":"ok","ollama":{"status":"ok","model":"qwen2.5:7b","models_available":["qwen2.5:7b-32k","qwen2.5:7b","llama3:latest","qwen2.5:14b","nomic-embed-text:latest","gpt-oss:20b","qwen2.5:0.5b","qwen2.5vl:7b","gemma3:4b"]}}
```

### Enhancement Test
```
Draft md_3cc270f3c035 enhanced:
- Version: 1 -> 2
- Word count: 80
- Proof point: "50% manual testing cut, ROI in Q1"
- Research used: headline, company_products, pain_indicators
```

### Channel Filter Fix Verification
```
Before: /api/messages?channel=linkedin returned 250 (all channels)
After: /api/messages?channel=linkedin returns 245 (linkedin only)
```

### Tunnel URL
```
https://operating-translate-lonely-scientist.trycloudflare.com
```

### Gateway Config on Vercel
```json
{"configured":true,"gateway_url":"https://operating-translate-lonely-scientist.trycloudflare.com","has_key":true}
```
