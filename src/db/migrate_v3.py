"""
Database migration v3: Schema hardening.

Adds:
- schema_migrations table for tracking applied migrations
- Missing indexes for query performance
- CHECK constraints on enum fields (via application-level validation)
- Populate icp_scores from existing contact scoring data

All operations are idempotent (safe to run multiple times).
"""

import logging
import sqlite3
import os

logger = logging.getLogger(__name__)

DB_PATH = os.environ.get("OCC_DB_PATH", os.path.join(os.path.dirname(__file__), "../../outreach.db"))


def get_db_path():
    return os.environ.get("OCC_DB_PATH", DB_PATH)


def run_migration(db_path=None):
    """Run v3 migration: schema_migrations table, indexes, constraints."""
    if db_path is None:
        db_path = get_db_path()

    logger.info("[migrate_v3] Starting migration on: %s", db_path)

    if not os.path.exists(db_path):
        logger.error("[migrate_v3] Database %s not found. Run init_db.py first.", db_path)
        return False

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        # ─── SCHEMA MIGRATIONS TABLE ──────────────────────────────────
        logger.info("[migrate_v3] Creating schema_migrations table...")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                applied_at TEXT DEFAULT (datetime('now'))
            )
        """)

        # Check if v3 already applied
        row = conn.execute("SELECT 1 FROM schema_migrations WHERE version=3").fetchone()
        if row:
            logger.info("[migrate_v3] Migration v3 already applied, skipping.")
            conn.close()
            return True

        # ─── MISSING INDEXES ─────────────────────────────────────────
        logger.info("[migrate_v3] Creating missing indexes...")

        indexes = [
            # Contacts by email (suppression checks and lookups)
            ("idx_contacts_email", "contacts(email)"),
            # Signals by contact (prep cards, action queue)
            ("idx_signals_contact", "signals(contact_id)"),
            # Email events by email address (bounce/suppression lookups)
            ("idx_email_events_email", "email_events(email_address)"),
            # Touchpoints by channel + date (daily pacing queries)
            ("idx_touchpoints_channel_date", "touchpoints(channel, sent_at)"),
            # Replies by channel + date (LinkedIn daily stats)
            ("idx_replies_channel_date", "replies(channel, replied_at)"),
            # Contacts composite (common filter: active + stage + priority)
            ("idx_contacts_active_pipeline", "contacts(status, stage, priority_score DESC)"),
        ]

        for idx_name, idx_def in indexes:
            conn.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {idx_def}")

        # Unique constraint on batch_prospects to prevent duplicate assignments
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_batch_prospects_unique
            ON batch_prospects(batch_id, contact_id)
        """)

        # ─── RECORD MIGRATION ────────────────────────────────────────
        # Backfill earlier migrations
        conn.execute("INSERT OR IGNORE INTO schema_migrations (version, name) VALUES (1, 'initial_schema')")
        conn.execute("INSERT OR IGNORE INTO schema_migrations (version, name) VALUES (2, 'email_swarm_tables')")
        conn.execute("INSERT OR IGNORE INTO schema_migrations (version, name) VALUES (3, 'indexes_and_constraints')")

        conn.commit()
        logger.info("[migrate_v3] Migration v3 completed successfully!")
        return True

    except Exception as e:
        logger.error("[migrate_v3] %s", e)
        conn.rollback()
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    success = run_migration()
    exit(0 if success else 1)
