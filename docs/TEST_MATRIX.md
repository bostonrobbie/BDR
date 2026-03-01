# BDR Outreach Command Center - Test Matrix

**Audit Date:** 2026-02-22 | **Auditor:** Claude Code

---

## 1. INFRASTRUCTURE TESTS

| # | Component | Test | Expected | Actual | Status |
|---|-----------|------|----------|--------|--------|
| 1.1 | Python | Version check | 3.10+ | 3.14.0 | PASS |
| 1.2 | Ollama | Installed & running | Running | v0.15.6, PID 18104 | PASS |
| 1.3 | Ollama | qwen2.5:7b model available | Listed | Available (4.7GB) | PASS |
| 1.4 | Ollama | Test prompt response | Content returned | "OLLAMA_OK" in 7.9s | PASS |
| 1.5 | cloudflared | Installed | Present | v2025.8.1 | PASS |
| 1.6 | Gateway | Starts on port 8765 | Listening | Uvicorn running | PASS |
| 1.7 | Gateway | /api/health returns OK | 200 + healthy | `{"status":"healthy","tables":17}` | PASS |
| 1.8 | Gateway | /api/llm/status returns OK | Ollama connected | `{"gateway":"ok","ollama":{"status":"ok"}}` | PASS |
| 1.9 | Tunnel | Quick tunnel starts | URL generated | `operating-translate-lonely-scientist.trycloudflare.com` | PASS |
| 1.10 | Tunnel | Remote health check | 200 via tunnel | Healthy response via HTTPS | PASS |
| 1.11 | Vercel | Project exists | READY | `bdr-outreach` project READY | PASS |
| 1.12 | Vercel | Latest deploy succeeds | State=READY | `dpl_RStZqu8Fohyya6NtT4NKNzTqFv3h` READY | PASS |
| 1.13 | Vercel | /api/health live | 200 | 49 contacts, 48 accounts, 250 drafts | PASS |
| 1.14 | Vercel | Domain accessible | HTTPS loads | `bdr-outreach.vercel.app` serves HTML | PASS |

## 2. DATABASE TESTS

| # | Test | Expected | Actual | Status |
|---|------|----------|--------|--------|
| 2.1 | BDR DB exists | outreach.db present | 950KB, 60+ tables | PASS |
| 2.2 | Accounts populated | >0 rows | 48 accounts | PASS |
| 2.3 | Contacts populated | >0 rows | 49 contacts | PASS |
| 2.4 | Message drafts populated | >0 rows | 250 drafts | PASS |
| 2.5 | Research snapshots populated | >0 rows | 102 snapshots | PASS |
| 2.6 | Workflow definitions seeded | >0 rows | 7 workflows | PASS |
| 2.7 | Batch exists | >0 rows | 1 batch (imported) | PASS |
| 2.8 | Schema migrations applied | All tables present | 60+ tables created | PASS |
| 2.9 | occ-bdr DB exists | outreach.db present | 225KB, 17 tables | PASS |

## 3. API ENDPOINT TESTS (Vercel)

| # | Endpoint | Method | Expected | Status Code | Result | Status |
|---|----------|--------|----------|-------------|--------|--------|
| 3.1 | /api/health | GET | Healthy status | 200 | Tables + counts | PASS |
| 3.2 | /api/stats | GET | Dashboard metrics | 200 | 49 contacts, 250 drafts | PASS |
| 3.3 | /api/contacts | GET | Contact list | 200 | 49 contacts | PASS |
| 3.4 | /api/accounts | GET | Account list | 200 | 48 accounts | PASS |
| 3.5 | /api/messages | GET | Message list | 200 | 250 messages, 100/page | PASS |
| 3.6 | /api/messages?channel=linkedin | GET | LinkedIn only | 200 | 245 linkedin drafts | PASS (FIXED) |
| 3.7 | /api/messages/{id} | GET | Single message | 200 | Full message + contact | PASS (NEW) |
| 3.8 | /api/batches | GET | Batch list | 200 | 1 batch | PASS |
| 3.9 | /api/action-queue | GET | Action items | 200 | 10 items | PASS |
| 3.10 | /api/signals | GET | Signal list | 200 | Empty (expected) | PASS |
| 3.11 | /api/experiments | GET | Experiment list | 200 | Empty (expected) | PASS |
| 3.12 | /api/agent-runs | GET | Agent run logs | 200 | Empty (expected) | PASS |
| 3.13 | /api/opportunities | GET | Opportunities | 200 | Empty (expected) | PASS |
| 3.14 | /api/followups | GET | Follow-ups | 200 | Empty (expected) | PASS |
| 3.15 | /api/replies | GET | Reply list | 200 | 0 replies | PASS |
| 3.16 | /api/research-snapshots | GET | Research data | 200 | 102 snapshots | PASS (NEW) |
| 3.17 | /api/contacts/{id}/research | GET | Contact research | 200 | Person + company | PASS (NEW) |
| 3.18 | /api/pipeline-funnel | GET | Funnel metrics | 200 | new:49 | PASS |
| 3.19 | /api/reply-rates/persona | GET | Reply analytics | 200 | 3 personas | PASS |
| 3.20 | /api/workflows | GET | Workflow defs | 200 | 7 workflows | PASS |
| 3.21 | /api/intelligence/proof-points | GET | Proof points | 200 | 5 proof points | PASS |
| 3.22 | /api/intelligence/pain-hooks | GET | Pain hooks | 200 | 1 pain hook | PASS |
| 3.23 | /api/send-queue | GET | Send queue | 200 | 0 queued | PASS |
| 3.24 | /api/flows/runs | GET | Flow run history | 200 | Empty | PASS |
| 3.25 | /api/gateway/config | GET | Gateway config | 200 | URL + key configured | PASS |
| 3.26 | /api/gateway/status | GET | Gateway status | 200 | configured=true | PASS |
| 3.27 | /api/email/identities | GET | Email identities | 200 | Empty | PASS |
| 3.28 | /api/drafts/{id} | GET | Draft detail | 200 | Full draft + versions | PASS (FIXED) |
| 3.29 | /api/drafts/{id}/versions | GET | Version history | 200 | Versions array | PASS (NEW) |
| 3.30 | /api/drafts/{id}/research | GET | Draft research | 200 | Rich research data | PASS |

## 4. ENHANCEMENT FLOW TESTS

| # | Test | Expected | Actual | Status |
|---|------|----------|--------|--------|
| 4.1 | Tier 1 enhance (rule-based) | Status ready_for_review | Returns tier1 fixes + tier2 prompt | PASS |
| 4.2 | Full draft enhance | Status enhanced | Version incremented, body rewritten | PASS |
| 4.3 | Enhancement uses research | Research fields in output | headline, company_products, pain_indicators used | PASS |
| 4.4 | Enhancement uses proof points | Proof point selected | "50% manual testing cut, ROI in Q1" | PASS |
| 4.5 | Version saved on enhance | draft_versions entry | Pre-enhance body preserved | PASS |
| 4.6 | Enhanced status persisted | approval_status=enhanced | Stats show enhanced:6 | PASS |

## 5. LLM GATEWAY TESTS (via Cloudflare Tunnel)

| # | Test | Expected | Actual | Status |
|---|------|----------|--------|--------|
| 5.1 | /llm/enhance via tunnel | Enhanced text returned | 3.5s, coherent rewrite | PASS |
| 5.2 | /llm/research via tunnel | Research JSON returned | 5.0s, structured output | PASS |
| 5.3 | /llm/write via tunnel | Draft generated | 3.9s, 28 words | PASS |
| 5.4 | Auth required (x-occ-key) | 401 without key | Correct auth enforcement | PASS |
| 5.5 | Gateway config set on Vercel | gateway_url populated | URL + key saved | PASS |

## 6. REMOTE ACCESS TESTS

| # | Test | Expected | Actual | Status |
|---|------|----------|--------|--------|
| 6.1 | Dashboard loads via Vercel URL | HTML renders | 502KB HTML served | PASS |
| 6.2 | API accessible remotely | JSON responses | All endpoints return data | PASS |
| 6.3 | Tunnel accessible remotely | Gateway reachable | Health check passes | PASS |
| 6.4 | LLM reachable via tunnel | LLM responds | All 3 LLM endpoints work | PASS |
| 6.5 | Gateway config persists | Settings saved | Survives page refresh | PASS |

## 7. VERCEL DEPLOYMENT TESTS

| # | Test | Expected | Actual | Status |
|---|------|----------|--------|--------|
| 7.1 | Latest commit deploys | READY state | READY in ~60s | PASS |
| 7.2 | Build uses Python runtime | Lambda runtime | `python:1` | PASS |
| 7.3 | Static files served | /public/* accessible | Dashboard HTML loads | PASS |
| 7.4 | API routes work | /api/* forwarded | All 221 routes active | PASS |
| 7.5 | DB seed on cold start | Tables populated | 48 accounts, 49 contacts on fresh start | PASS |
| 7.6 | Schema migration on restore | New tables added | gateway_config etc. present | PASS |
| 7.7 | No deployment failures | All READY | 20/20 deployments READY | PASS |

---

## Summary

| Category | Total | Pass | Fail | Fixed |
|----------|-------|------|------|-------|
| Infrastructure | 14 | 14 | 0 | 0 |
| Database | 9 | 9 | 0 | 0 |
| API Endpoints | 30 | 30 | 0 | 7 fixed |
| Enhancement Flow | 6 | 6 | 0 | 0 |
| LLM Gateway | 5 | 5 | 0 | 0 |
| Remote Access | 5 | 5 | 0 | 0 |
| Vercel Deployment | 7 | 7 | 0 | 0 |
| **TOTAL** | **76** | **76** | **0** | **7** |

All 76 tests passing. 7 bugs found and fixed in this audit.
