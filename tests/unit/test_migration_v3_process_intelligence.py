"""Migration 003 tests for process-intelligence tables."""

import os
import sqlite3
import tempfile

from src.db.init_db import init_db
from src.db.migration_runner import run_migrations


EXPECTED_TABLES = {
    "contact_action_plans",
    "qualification_checks",
    "research_evidence",
    "sequence_state",
    "message_strategies",
    "process_compliance_log",
}


def test_v3_migration_creates_process_intelligence_tables():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_v3.db")
        init_db(db_path)

        result = run_migrations(db_path)
        assert result["failed"] == 0

        conn = sqlite3.connect(db_path)
        tables = {
            r[0]
            for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        conn.close()

        missing = EXPECTED_TABLES - tables
        assert not missing, f"Missing v3 tables: {missing}"


def test_v3_migration_idempotent():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_v3_idem.db")
        init_db(db_path)

        first = run_migrations(db_path)
        second = run_migrations(db_path)

        assert first["failed"] == 0
        assert second["failed"] == 0
