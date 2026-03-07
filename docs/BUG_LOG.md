# BDR Outreach Command Center - Bug Log

**Audit Date:** 2026-02-22 | **Auditor:** Claude Code

---

## BUG-001: Channel filter ignored on /api/messages
- **Severity:** HIGH
- **Status:** FIXED
- **Endpoint:** `GET /api/messages?channel=linkedin`
- **Reproduction:** Call `/api/messages?channel=linkedin` -- returns all 250 messages (both linkedin and email)
- **Root Cause:** The `list_messages()` function at line 1640 did not accept or filter by `channel` query parameter
- **Fix:** Added `channel: str = None` parameter and SQL filter `AND m.channel=?`. Also fixed the `total` count to respect channel filter.
- **Diff:** `api/index.py` line 1640 - added channel param and two filter clauses
- **Verification:** Deploy and test `GET /api/messages?channel=linkedin` returns only linkedin drafts

## BUG-002: Missing GET /api/messages/{id} endpoint
- **Severity:** MEDIUM
- **Status:** FIXED
- **Endpoint:** `GET /api/messages/{message_id}`
- **Reproduction:** Call `/api/messages/msg_eb0496dd2f5e` -- returns 404
- **Root Cause:** No route handler defined for single message retrieval
- **Fix:** Added `get_message()` endpoint that joins contacts and accounts for full context
- **Diff:** `api/index.py` after line 1654 - new 10-line endpoint
- **Verification:** Deploy and test `GET /api/messages/{id}` returns full message with contact/company data

## BUG-003: Missing /api/research-snapshots endpoint
- **Severity:** MEDIUM
- **Status:** FIXED
- **Endpoint:** `GET /api/research-snapshots`
- **Reproduction:** Call `/api/research-snapshots` -- returns 404. Database has 102 research snapshots but no route serves them.
- **Root Cause:** No route handler defined
- **Fix:** Added `list_research_snapshots()` with contact_id, account_id, entity_type filters
- **Diff:** `api/index.py` before RESEARCH RUN ENDPOINTS section - new 12-line endpoint
- **Verification:** Deploy and test returns 102 snapshots

## BUG-004: Missing /api/contacts/{id}/research endpoint
- **Severity:** MEDIUM
- **Status:** FIXED
- **Endpoint:** `GET /api/contacts/{contact_id}/research`
- **Reproduction:** Call `/api/contacts/{id}/research` -- returns 404
- **Root Cause:** No route handler defined
- **Fix:** Added `get_contact_research()` that returns person + company research snapshots
- **Diff:** `api/index.py` after research-snapshots endpoint - new 15-line endpoint
- **Verification:** Deploy and test returns research for a contact

## BUG-005: GET /api/drafts/{id} returns 404 when no draft_versions exist
- **Severity:** MEDIUM
- **Status:** FIXED
- **Endpoint:** `GET /api/drafts/{draft_id}`
- **Reproduction:** Call `/api/drafts/{id}` for a draft that has never been enhanced -- returns 404 because it only checked `draft_versions` table
- **Root Cause:** The endpoint only queried `draft_versions` table, not `message_drafts` (the authoritative table)
- **Fix:** Rewrote to query `message_drafts` first with contact/account joins, then append version history from `draft_versions`
- **Diff:** `api/index.py` line 2072 - complete rewrite of get_draft()
- **Verification:** Deploy and test returns draft data even with no versions

## BUG-006: Missing /api/drafts/{id}/versions endpoint
- **Severity:** LOW
- **Status:** FIXED
- **Endpoint:** `GET /api/drafts/{draft_id}/versions`
- **Reproduction:** Call `/api/drafts/{id}/versions` -- returns 404
- **Root Cause:** No dedicated versions endpoint (was folded into `GET /api/drafts/{id}` which itself was broken)
- **Fix:** Added dedicated `get_draft_versions()` endpoint
- **Diff:** `api/index.py` after get_draft - new endpoint
- **Verification:** Deploy and test

## BUG-007: Duplicate route definition for /api/drafts/{id}/research
- **Severity:** LOW
- **Status:** FIXED
- **Root Cause:** Two `@app.get("/api/drafts/{draft_id}/research")` at lines 7099 and 7594
- **Fix:** Renamed first one to `/api/drafts/{draft_id}/research-compact`
- **Impact:** FastAPI used the last-defined route (the richer one), so no functional issue, but duplicate routes cause warnings

## BUG-008: Gateway not configured on Vercel dashboard
- **Severity:** HIGH
- **Status:** IDENTIFIED - Requires user action
- **Symptom:** `GET /api/gateway/config` returns empty gateway_url and gateway_key
- **Root Cause:** The tunnel URL changes every restart (quick mode) and is not auto-configured on Vercel
- **Impact:** Vercel dashboard cannot call LLM (Tier 2 enhance, research, write) from remote PC
- **Current Tunnel URL:** `https://operating-translate-lonely-scientist.trycloudflare.com`
- **Fix Options:**
  1. User manually sets gateway URL in Settings > LLM Gateway after each tunnel restart
  2. Add auto-registration: gateway pushes its URL to Vercel on startup
  3. Switch to named Cloudflare tunnel with permanent URL

## BUG-009: occ-bdr database mostly empty
- **Severity:** LOW
- **Status:** INFORMATIONAL
- **Symptom:** occ-bdr SQLite has 17 tables but only 1 contact, 0 messages
- **Root Cause:** The Vercel deployment has the real data (48 accounts, 49 contacts, 250 drafts). occ-bdr is the LLM gateway, not the primary data store.
- **Impact:** If the dashboard calls occ-bdr for CRUD (instead of its own Vercel API), data will be missing
- **Fix:** Not needed - the architecture correctly uses Vercel for data and occ-bdr only for LLM

## BUG-010: Missing /api/analytics/token-costs endpoint
- **Severity:** LOW
- **Status:** IDENTIFIED
- **Root Cause:** Not yet implemented
- **Impact:** Token cost analytics page won't load
