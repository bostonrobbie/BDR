"""
Database connection utilities.
Centralizes DB_PATH, get_db(), get_db_conn() context manager, and gen_id().
"""

import logging
import os
import sqlite3
import uuid
from contextlib import contextmanager
from typing import Optional

logger = logging.getLogger(__name__)

DB_PATH = os.environ.get("OCC_DB_PATH", os.path.join(os.path.dirname(__file__), "../../outreach.db"))


def get_db():
    """Get a database connection with row_factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    journal_mode = os.environ.get("OCC_JOURNAL_MODE", "WAL")
    conn.execute(f"PRAGMA journal_mode={journal_mode}")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def get_db_conn():
    """Context manager for database connections. Ensures connections are always closed."""
    conn = get_db()
    try:
        yield conn
    finally:
        conn.close()


def gen_id(prefix=""):
    """Generate a prefixed UUID."""
    short = uuid.uuid4().hex[:12]
    return f"{prefix}_{short}" if prefix else short


def _safe_update(table: str, record_id: str, data: dict, allowed_fields: set, id_column: str = "id") -> Optional[dict]:
    """Generic safe update that whitelists field names to prevent SQL injection."""
    safe_data = {k: v for k, v in data.items() if k in allowed_fields}
    if not safe_data:
        return None
    fields = ", ".join(f"{k}=?" for k in safe_data.keys())
    values = list(safe_data.values()) + [record_id]
    with get_db_conn() as conn:
        conn.execute(f"UPDATE {table} SET {fields} WHERE {id_column}=?", values)
        conn.commit()
        row = conn.execute(f"SELECT * FROM {table} WHERE {id_column}=?", (record_id,)).fetchone()
        return dict(row) if row else None
