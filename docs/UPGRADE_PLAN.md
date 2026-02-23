# Upgrade Plan: BDR Outreach Command Center

**Date:** 2026-02-23
**Scope:** Repo infrastructure, database schema, code quality, and security

---

## Executive Summary

After auditing the full codebase (24+ DB tables, ~1,600-line models.py, ~1,500-line app.py, 10 agents, 9,800-line SPA), here are the recommended upgrades organized by priority.

---

## 1. CRITICAL: Security Fixes

### 1a. SQL Injection in Dynamic Update Functions

**Files:** `src/db/models.py:86-93`, `models.py:172-180`, `models.py:1310-1318`, `models.py:1367-1378`

The `update_account`, `update_contact`, `update_swarm_run`, and `update_swarm_task` functions build SQL from dictionary keys using f-strings:

```python
fields = ", ".join(f"{k}=?" for k in data.keys())
conn.execute(f"UPDATE accounts SET {fields} WHERE id=?", values)
```

If an attacker controls the dict keys (which they can via the API's `PATCH /api/accounts/{id}` that accepts arbitrary `dict`), they can inject SQL column names or SQL fragments.

**Fix:** Whitelist allowed column names per table. Only accept known fields.

```python
ACCOUNT_FIELDS = {"name", "domain", "industry", "sub_industry", ...}

def update_account(account_id: str, data: dict) -> Optional[dict]:
    safe_data = {k: v for k, v in data.items() if k in ACCOUNT_FIELDS}
    ...
```

### 1b. CORS Wildcard in Production

**File:** `src/api/app.py:28-33`

```python
allow_origins=["*"]
```

This allows any website to make authenticated requests to the API. Should restrict to known origins (Vercel domain, localhost).

---

## 2. HIGH: Database Upgrades

### 2a. Add a Real Migration Framework

**Current state:** Hand-written `init_db.py` + `migrate_v2.py` with no version tracking or rollback. Schema drift risk between the two files.

**Recommendation:** Add [Alembic](https://alembic.sqlalchemy.org/) or a lightweight alternative like a migrations table:

```sql
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    applied_at TEXT DEFAULT (datetime('now'))
);
```

Each migration is a numbered Python file that checks `schema_migrations` before running. This gives you:
- Version tracking (know exactly what schema is deployed)
- Idempotent applies
- Rollback capability
- Audit trail

### 2b. Add CHECK Constraints for Enum Fields

The database has many enum-like fields with no validation. Any typo or bad value silently persists.

```sql
-- contacts.stage
ALTER TABLE contacts ADD CHECK (stage IN (
    'new', 'researched', 'drafted', 'touched', 'sequencing',
    'break_up_sent', 'replied', 'replied_positive', 'replied_negative',
    'referred', 'meeting_booked', 'meeting_held', 'opportunity',
    'dormant', 're_engaged', 'not_interested'
));

-- contacts.status
ALTER TABLE contacts ADD CHECK (status IN ('active', 'dormant', 'bounced', 'do_not_contact'));

-- message_drafts.channel
ALTER TABLE message_drafts ADD CHECK (channel IN ('linkedin', 'email', 'call'));

-- message_drafts.approval_status
ALTER TABLE message_drafts ADD CHECK (approval_status IN ('draft', 'pending', 'approved', 'rejected', 'sent', 'archived'));

-- opportunities.status
ALTER TABLE opportunities ADD CHECK (status IN (
    'meeting_booked', 'meeting_held', 'opportunity_created', 'disqualified', 'lost'
));
```

Note: SQLite only enforces CHECK on INSERT/UPDATE, and adding CHECK to existing tables requires recreation. Best to add these in a migration that recreates tables.

### 2c. Add Missing Indexes

```sql
-- Contacts by email (for suppression checks and lookups)
CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email);

-- Signals by contact (used in prep cards, action queue)
CREATE INDEX IF NOT EXISTS idx_signals_contact ON signals(contact_id);

-- Email events by email address (for bounce/suppression lookups)
CREATE INDEX IF NOT EXISTS idx_email_events_email ON email_events(email_address);

-- Touchpoints by channel + date (for daily pacing queries)
CREATE INDEX IF NOT EXISTS idx_touchpoints_channel_date ON touchpoints(channel, sent_at);

-- Replies by channel + date (for LinkedIn daily stats)
CREATE INDEX IF NOT EXISTS idx_replies_channel_date ON replies(channel, replied_at);

-- Contacts composite (common filter: active + stage + priority)
CREATE INDEX IF NOT EXISTS idx_contacts_active_pipeline ON contacts(status, stage, priority_score DESC);

-- Batch prospects unique constraint (prevent duplicate assignments)
CREATE UNIQUE INDEX IF NOT EXISTS idx_batch_prospects_unique ON batch_prospects(batch_id, contact_id);
```

### 2d. Add Connection Context Manager

Every DB function manually opens and closes connections, with no protection against exceptions leaving connections open.

```python
from contextlib import contextmanager

@contextmanager
def get_db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(f"PRAGMA journal_mode={os.environ.get('OCC_JOURNAL_MODE', 'WAL')}")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
    finally:
        conn.close()
```

Then use everywhere:
```python
def get_account(account_id: str) -> Optional[dict]:
    with get_db_conn() as conn:
        row = conn.execute("SELECT * FROM accounts WHERE id=?", (account_id,)).fetchone()
        return dict(row) if row else None
```

### 2e. Clean Up Unused Table: `icp_scores`

The `icp_scores` table is defined in the schema but the actual ICP scoring logic (`compute_priority_score` in `models.py:204-251`) writes directly to `contacts.priority_score` and `contacts.priority_factors`. Either:
- **Option A:** Remove `icp_scores` table (simplify)
- **Option B:** Use it properly - store detailed scoring history so you can track score changes over time

Recommendation: Option B - keep `icp_scores` as a scoring audit trail, and populate it from `score_and_save()`.

### 2f. Verify + Fix verify_db()

`init_db.py:362-367` checks for 15 tables, but the system now has 24+ tables (after migrate_v2). Update the verification to cover all tables.

### 2g. Vercel /tmp SQLite Persistence

The current blob-save/blob-restore approach for persisting SQLite on Vercel is fragile. Consider:
- **Turso** (SQLite-compatible edge database) - drop-in replacement with libSQL
- **Vercel Postgres** - if willing to migrate from SQLite
- **LiteFS/LiteStream** - replicated SQLite

This is the most impactful DB upgrade for production reliability.

---

## 3. HIGH: Code Quality & Structure

### 3a. Add `pyproject.toml` with Proper Dependencies

`requirements.txt` only lists `fastapi>=0.104.0` and `uvicorn>=0.24.0`. Missing:
- pydantic (implicit via fastapi but should be pinned)
- Any test dependencies (pytest)
- Development tools

```toml
[project]
name = "bdr-outreach"
version = "2.0.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio",
    "httpx",  # for FastAPI test client
    "ruff",
    "mypy",
]

[tool.ruff]
line-length = 120
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "UP"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### 3b. Fix Deprecated `datetime.utcnow()`

Used throughout `models.py` (lines 39, 101, 272, 337, 405, 442, 498, 519, 539, 569, etc.). Python 3.12 deprecated `datetime.utcnow()`.

**Fix:**
```python
from datetime import datetime, timezone
datetime.now(timezone.utc).isoformat()
```

### 3c. Fix Deprecated Pydantic `.dict()` → `.model_dump()`

**File:** `src/api/app.py:1184` and `1257`
```python
# Before (deprecated)
return models.create_email_identity(req.dict())
# After
return models.create_email_identity(req.model_dump())
```

### 3d. Eliminate `sys.path` Hacks

**Files:** `src/api/app.py:14`, `src/api/pipeline_runner.py:15`

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
```

Fix by making the project a proper package with `pyproject.toml` and installing it in editable mode (`pip install -e .`), or by using relative imports correctly.

### 3e. Consolidate DB_PATH Definition

DB_PATH is defined differently in three places:
- `models.py:14` → `../../outreach.db` relative to file
- `init_db.py:14` → `outreach.db` (cwd)
- `migrate_v2.py:23-31` → env var, then cwd, then script dir

All three should use a single source of truth.

### 3f. Organize Tests

Current state: 4 test files in root (`test_agentic.py`, `test_comprehensive.py`, `test_final_integration.py`, `test_pipeline.py`) plus `tests/` directory with 3 more files. The `tests/e2e/`, `tests/integration/`, and `tests/unit/` directories are mostly empty `.gitkeep` files.

**Recommendation:**
- Move all root test files into `tests/`
- Add `conftest.py` with shared fixtures (test DB setup/teardown)
- Add pytest configuration

---

## 4. MEDIUM: Architectural Improvements

### 4a. Break Up Monolithic `models.py` (1,630 lines)

Split into domain modules:
```
src/db/
├── connection.py       # get_db, get_db_conn context manager, DB_PATH
├── accounts.py         # Account CRUD
├── contacts.py         # Contact CRUD + scoring
├── messages.py         # Message draft CRUD
├── touchpoints.py      # Touchpoint + reply + followup logic
├── opportunities.py    # Opportunity CRUD
├── batches.py          # Batch + batch_prospects CRUD
├── experiments.py      # Experiment CRUD + results
├── agents.py           # Agent runs, swarm runs/tasks
├── email.py            # Email identities, suppression, events, pacing
├── linkedin.py         # LinkedIn stats, pacing, events
├── analytics.py        # Dashboard stats, intelligence, action queue
├── audit.py            # Audit log
└── __init__.py         # Re-exports for backwards compatibility
```

### 4b. Break Up Monolithic `app.py` (1,567 lines)

Use FastAPI routers:
```python
# src/api/routers/accounts.py
from fastapi import APIRouter
router = APIRouter(prefix="/api/accounts", tags=["accounts"])

@router.post("")
def create_account(account: AccountCreate):
    ...
```

Then in `app.py`:
```python
from src.api.routers import accounts, contacts, messages, ...
app.include_router(accounts.router)
```

### 4c. Add Request Validation on PATCH Endpoints

`PATCH /api/accounts/{account_id}` accepts raw `dict` with no validation. Should use a Pydantic model with allowed fields.

### 4d. Add Rate Limiting

No rate limiting on any endpoint. For a single-user tool this is low priority, but the Vercel deployment is publicly accessible.

---

## 5. MEDIUM: Testing & CI

### 5a. Add pytest Configuration & Fixtures

```python
# tests/conftest.py
import pytest
import os
import tempfile
from src.db.init_db import init_db
from src.db.migrate_v2 import run_migration

@pytest.fixture
def test_db(tmp_path):
    db_path = str(tmp_path / "test.db")
    os.environ["OCC_DB_PATH"] = db_path
    os.environ["OCC_JOURNAL_MODE"] = "DELETE"
    init_db(db_path)
    run_migration(db_path)
    yield db_path
    os.environ.pop("OCC_DB_PATH", None)
```

### 5b. Add GitHub Actions CI

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: pytest tests/ -v
```

### 5c. Add Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
      - id: ruff-format
```

---

## 6. LOW: Nice-to-Have Improvements

### 6a. Add Structured Logging

Replace `print()` statements in init_db.py and migrate_v2.py with Python `logging` module. Add request logging middleware to FastAPI.

### 6b. Add API Versioning

Current routes are `/api/...`. Consider `/api/v1/...` for future-proofing if the API will be consumed by multiple clients.

### 6c. Add OpenAPI Tags and Descriptions

FastAPI auto-generates docs at `/docs`. Adding proper tags and descriptions makes the API self-documenting:
```python
app = FastAPI(
    title="Outreach Command Center",
    version="2.0.0",
    description="BDR operations platform API",
)
```

### 6d. Add DB Backup Script

Simple script to copy the SQLite file with a timestamp:
```bash
cp outreach.db backups/outreach-$(date +%Y%m%d-%H%M%S).db
```

### 6e. Add Health Check for LLM Gateway

The `/api/health` endpoint only checks the local DB. Add a check for the Ollama/gateway connection status.

---

## Recommended Implementation Order

| Priority | Upgrade | Effort | Impact |
|----------|---------|--------|--------|
| 1 | SQL injection fix (1a) | Small | Critical |
| 2 | DB connection context manager (2d) | Small | High |
| 3 | Missing indexes (2c) | Small | High |
| 4 | CORS restriction (1b) | Small | High |
| 5 | Fix deprecated datetime/pydantic (3b, 3c) | Small | Medium |
| 6 | Add pyproject.toml (3a) | Small | Medium |
| 7 | Consolidate DB_PATH (3e) | Small | Medium |
| 8 | Migration framework (2a) | Medium | High |
| 9 | CHECK constraints (2b) | Medium | Medium |
| 10 | Organize tests + CI (5a, 5b) | Medium | High |
| 11 | Break up models.py (4a) | Medium | Medium |
| 12 | Break up app.py (4b) | Medium | Medium |
| 13 | Vercel DB persistence (2g) | Large | High |
| 14 | Validate PATCH inputs (4c) | Small | Medium |
| 15 | Structured logging (6a) | Small | Low |

---

## Database Schema Diff Summary

### New indexes to add:
- `idx_contacts_email`
- `idx_signals_contact`
- `idx_email_events_email`
- `idx_touchpoints_channel_date`
- `idx_replies_channel_date`
- `idx_contacts_active_pipeline`
- `idx_batch_prospects_unique` (UNIQUE)

### Tables to audit:
- `icp_scores` - unused, decide keep-or-drop
- `schema_migrations` - new table for migration tracking

### Fields to add CHECK constraints:
- `contacts.stage`
- `contacts.status`
- `message_drafts.channel`
- `message_drafts.approval_status`
- `opportunities.status`
- `touchpoints.channel`
- `replies.intent`
- `batches.status`
- `agent_runs.status`
