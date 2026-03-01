"""
Migration 002: Add pipeline_errors table for tracking non-fatal errors.

Instead of silently swallowing exceptions, agents log errors here so they're
visible in the deliverable and can be investigated.
"""


def up(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pipeline_errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id TEXT REFERENCES batches(id),
            contact_id TEXT REFERENCES contacts(id),
            phase TEXT NOT NULL,
            agent_name TEXT,
            error_type TEXT,
            error_message TEXT,
            context TEXT DEFAULT '{}',
            severity TEXT DEFAULT 'warning',
            resolved INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_pipeline_errors_batch
        ON pipeline_errors(batch_id)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_pipeline_errors_severity
        ON pipeline_errors(severity, resolved)
    """)
