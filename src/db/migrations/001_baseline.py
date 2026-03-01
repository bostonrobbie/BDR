"""
Migration 001: Baseline schema.

This migration is a no-op for existing databases that already have the v1+v2 schema.
It exists to establish a baseline version so future migrations can build on it.

For new databases, run init_db.py first, then the migration runner.
"""


def up(conn):
    """Baseline migration - verify core tables exist."""
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tables = {row[0] for row in cursor.fetchall()}

    required = {"accounts", "contacts", "message_drafts", "batches", "signals"}
    missing = required - tables

    if missing:
        raise RuntimeError(
            f"Baseline migration requires existing schema. Missing tables: {missing}. "
            f"Run 'python -m src.db.init_db' first."
        )
