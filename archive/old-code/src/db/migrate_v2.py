"""
Database migration v2: Email integration and agent swarm tables.

This migration adds:
- Email identity management (sender accounts)
- Suppression list and email events tracking
- Swarm orchestration and task tracking
- Quality scoring for multi-agent QA gate
- Feature flags for safe rollout
- Pacing rules for rate limiting

All tables use CREATE TABLE IF NOT EXISTS for idempotence.
Run with: python3 migrate_v2.py
"""

import logging
import sqlite3
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

DB_PATH = os.environ.get("OCC_DB_PATH", os.path.join(os.path.dirname(__file__), "../../outreach.db"))


def get_db_path():
    """Get database path, default to outreach.db in project root"""
    return os.environ.get("OCC_DB_PATH", DB_PATH)


def run_migration(db_path=None):
    """Run v2 migration on the database."""
    if db_path is None:
        db_path = get_db_path()
    
    logger.info(f"[migrate_v2] Starting migration on: {db_path}")
    
    if not os.path.exists(db_path):
        logger.error("[migrate_v2] Database {db_path} not found. Run init_db.py first.")
        return False
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # ─── EMAIL IDENTITIES ──────────────────────────────────────────
        logger.info("[migrate_v2] Creating email_identities table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS email_identities (
                id TEXT PRIMARY KEY,
                email_address TEXT NOT NULL UNIQUE,
                display_name TEXT,
                daily_send_limit INTEGER DEFAULT 25,
                warmup_phase INTEGER DEFAULT 1,
                warmup_daily_cap INTEGER DEFAULT 5,
                total_sent_today INTEGER DEFAULT 0,
                total_sent_all_time INTEGER DEFAULT 0,
                reputation_score REAL DEFAULT 100.0,
                is_active INTEGER DEFAULT 1,
                notes TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            )
        """)
        
        # ─── SUPPRESSION LIST ──────────────────────────────────────────
        logger.info("[migrate_v2] Creating suppression_list table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suppression_list (
                id TEXT PRIMARY KEY,
                email_address TEXT NOT NULL UNIQUE,
                reason TEXT NOT NULL,
                source TEXT,
                added_at TEXT DEFAULT (datetime('now'))
            )
        """)
        
        # ─── EMAIL EVENTS ─────────────────────────────────────────────
        logger.info("[migrate_v2] Creating email_events table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS email_events (
                id TEXT PRIMARY KEY,
                contact_id TEXT REFERENCES contacts(id),
                email_address TEXT,
                event_type TEXT NOT NULL,
                event_source TEXT DEFAULT 'manual',
                details TEXT,
                raw_data TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        
        # ─── DELIVERABILITY SNAPSHOTS ──────────────────────────────────
        logger.info("[migrate_v2] Creating deliverability_snapshots table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deliverability_snapshots (
                id TEXT PRIMARY KEY,
                identity_id TEXT REFERENCES email_identities(id),
                snapshot_date TEXT,
                emails_sent INTEGER DEFAULT 0,
                bounces INTEGER DEFAULT 0,
                replies_received INTEGER DEFAULT 0,
                opt_outs INTEGER DEFAULT 0,
                bounce_rate REAL DEFAULT 0.0,
                reply_rate REAL DEFAULT 0.0,
                notes TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        
        # ─── PACING RULES ─────────────────────────────────────────────
        logger.info("[migrate_v2] Creating pacing_rules table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacing_rules (
                id TEXT PRIMARY KEY,
                rule_name TEXT NOT NULL,
                channel TEXT NOT NULL,
                max_per_day INTEGER DEFAULT 25,
                max_per_hour INTEGER DEFAULT 5,
                min_interval_minutes INTEGER DEFAULT 15,
                ramp_enabled INTEGER DEFAULT 1,
                ramp_increment_per_week INTEGER DEFAULT 5,
                ramp_max INTEGER DEFAULT 50,
                cooldown_after_bounce INTEGER DEFAULT 1,
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        
        # ─── SWARM RUNS ───────────────────────────────────────────────
        logger.info("[migrate_v2] Creating swarm_runs table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS swarm_runs (
                id TEXT PRIMARY KEY,
                swarm_type TEXT NOT NULL,
                batch_id TEXT REFERENCES batches(id),
                config TEXT DEFAULT '{}',
                status TEXT DEFAULT 'pending',
                total_tasks INTEGER DEFAULT 0,
                completed_tasks INTEGER DEFAULT 0,
                failed_tasks INTEGER DEFAULT 0,
                started_at TEXT,
                completed_at TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        
        # ─── SWARM TASKS ──────────────────────────────────────────────
        logger.info("[migrate_v2] Creating swarm_tasks table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS swarm_tasks (
                id TEXT PRIMARY KEY,
                swarm_run_id TEXT REFERENCES swarm_runs(id),
                agent_name TEXT NOT NULL,
                task_type TEXT NOT NULL,
                contact_id TEXT REFERENCES contacts(id),
                input_data TEXT DEFAULT '{}',
                output_data TEXT DEFAULT '{}',
                status TEXT DEFAULT 'pending',
                retry_count INTEGER DEFAULT 0,
                max_retries INTEGER DEFAULT 2,
                dedupe_key TEXT,
                error_message TEXT,
                parent_task_id TEXT REFERENCES swarm_tasks(id),
                started_at TEXT,
                completed_at TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        
        # ─── QUALITY SCORES ───────────────────────────────────────────
        logger.info("[migrate_v2] Creating quality_scores table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quality_scores (
                id TEXT PRIMARY KEY,
                swarm_task_id TEXT REFERENCES swarm_tasks(id),
                message_draft_id TEXT REFERENCES message_drafts(id),
                grounding_score REAL DEFAULT 0.0,
                tone_score REAL DEFAULT 0.0,
                compliance_score REAL DEFAULT 0.0,
                hallucination_flags TEXT DEFAULT '[]',
                overall_pass INTEGER DEFAULT 0,
                reviewer_notes TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        
        # ─── FEATURE FLAGS ────────────────────────────────────────────
        logger.info("[migrate_v2] Creating feature_flags table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feature_flags (
                id TEXT PRIMARY KEY,
                flag_name TEXT NOT NULL UNIQUE,
                enabled INTEGER DEFAULT 0,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            )
        """)
        
        # ─── INDEXES ───────────────────────────────────────────────────
        logger.info("[migrate_v2] Creating indexes...")
        
        indexes = [
            ("idx_suppression_email", "suppression_list(email_address)"),
            ("idx_email_events_contact", "email_events(contact_id)"),
            ("idx_email_events_type", "email_events(event_type)"),
            ("idx_swarm_runs_batch", "swarm_runs(batch_id)"),
            ("idx_swarm_tasks_run", "swarm_tasks(swarm_run_id)"),
            ("idx_swarm_tasks_contact", "swarm_tasks(contact_id)"),
            ("idx_swarm_tasks_dedupe", "swarm_tasks(dedupe_key)"),
            ("idx_quality_scores_task", "quality_scores(swarm_task_id)"),
            ("idx_quality_scores_msg", "quality_scores(message_draft_id)"),
            ("idx_feature_flags_name", "feature_flags(flag_name)"),
        ]
        
        for idx_name, idx_def in indexes:
            cursor.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {idx_def}")
        
        # ─── SEED DEFAULT FEATURE FLAGS ────────────────────────────────
        logger.info("[migrate_v2] Seeding feature flags...")
        feature_flags = [
            ("ff_email", "email_channel", 1, "Enable email channel for outreach"),
            ("ff_swarm", "agent_swarm", 1, "Enable multi-agent swarm processing"),
            ("ff_pacing", "email_pacing", 1, "Enable email pacing and rate limiting"),
            ("ff_suppression", "suppression_check", 1, "Check suppression list before drafting"),
            ("ff_qc_gate", "qc_gate_blocking", 1, "Block ungrounded messages from approval"),
        ]
        
        for ff_id, flag_name, enabled, description in feature_flags:
            cursor.execute("""
                INSERT OR IGNORE INTO feature_flags (id, flag_name, enabled, description)
                VALUES (?,?,?,?)
            """, (ff_id, flag_name, enabled, description))
        
        # ─── SEED DEFAULT PACING RULE ─────────────────────────────────
        logger.info("[migrate_v2] Seeding pacing rules...")
        cursor.execute("""
            INSERT OR IGNORE INTO pacing_rules (id, rule_name, channel, max_per_day, 
                max_per_hour, min_interval_minutes, ramp_enabled, ramp_increment_per_week, ramp_max)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, ("pr_email_default", "Default Email Pacing", "email", 25, 5, 15, 1, 5, 50))
        
        conn.commit()
        logger.info("[migrate_v2] Migration completed successfully!")
        return True
        
    except Exception as e:
        logger.error("[migrate_v2] {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def verify_migration(db_path=None):
    """Verify all v2 tables and indexes were created."""
    if db_path is None:
        db_path = get_db_path()
    
    logger.info(f"\n[verify_migration] Checking: {db_path}")
    
    if not os.path.exists(db_path):
        logger.error("[verify_migration] Database not found")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check tables
        tables_to_check = [
            "email_identities",
            "suppression_list",
            "email_events",
            "deliverability_snapshots",
            "pacing_rules",
            "swarm_runs",
            "swarm_tasks",
            "quality_scores",
            "feature_flags",
        ]
        
        missing_tables = []
        for table_name in tables_to_check:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                          (table_name,))
            if not cursor.fetchone():
                missing_tables.append(table_name)
        
        if missing_tables:
            logger.error("[verify_migration] Missing tables: %s", missing_tables)
            return False
        else:
            logger.info(f"[verify_migration] OK: All {len(tables_to_check)} tables present")
        
        # Check feature flags seeded
        cursor.execute("SELECT COUNT(*) FROM feature_flags")
        ff_count = cursor.fetchone()[0]
        logger.info(f"[verify_migration] OK: {ff_count} feature flags seeded")
        
        # Check pacing rule seeded
        cursor.execute("SELECT COUNT(*) FROM pacing_rules")
        pr_count = cursor.fetchone()[0]
        logger.info(f"[verify_migration] OK: {pr_count} pacing rules seeded")
        
        logger.info("[verify_migration] All checks passed!")
        return True
        
    except Exception as e:
        logger.info(f"[verify_migration] ERROR: {e}")
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    success = run_migration()
    if success:
        verify_migration()
    exit(0 if success else 1)
