#!/usr/bin/env python3
"""
Backfill the SQLite database from existing pipeline state files.

Imports data from:
  - work/pipeline-state.json  → batches table
  - work/dnc-list.json        → contacts table (DNC records)
  - batch7-send-tracker.json  → contacts + accounts + touchpoints

This is a one-time script to bootstrap the DB with the 148 sends
that have been tracked in HTML/JSON files but never entered into the DB.

Run: python scripts/backfill_db.py
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.db.models import gen_id

DB_PATH = os.environ.get("OCC_DB_PATH", str(ROOT / "outreach.db"))

def get_backfill_db():
    """Get a DB connection with WAL mode (matching existing DB) and long timeout."""
    import sqlite3
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=30000")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def backfill_from_pipeline_state():
    """Create batch records from pipeline-state.json."""
    state_file = ROOT / "work" / "pipeline-state.json"
    if not state_file.exists():
        print("  Skipping: work/pipeline-state.json not found")
        return 0

    state = json.loads(state_file.read_text())
    conn = get_backfill_db()
    count = 0

    for batch_name, batch_data in state.get("active_batches", {}).items():
        batch_id = gen_id("bat")
        now = datetime.utcnow().isoformat()
        batch_num = batch_name.replace("batch_", "").replace("a", "").replace("b", "")

        try:
            batch_num_int = int(batch_num)
        except ValueError:
            batch_num_int = 0

        # Check if batch already exists
        existing = conn.execute(
            "SELECT id FROM batches WHERE batch_number=?", (batch_num_int,)
        ).fetchone()
        if existing:
            continue

        conn.execute("""
            INSERT INTO batches (id, batch_number, prospect_count, status,
                ab_variable, pre_brief, metrics, created_at)
            VALUES (?,?,?,?,?,?,?,?)
        """, (
            batch_id,
            batch_num_int,
            batch_data.get("prospects", 0),
            batch_data.get("status", "complete"),
            None,  # ab_variable
            json.dumps({"notes": batch_data.get("notes", "")}),
            json.dumps({"touch1_sent_dates": batch_data.get("touch1_sent_dates", [])}),
            now,
        ))
        count += 1
        print(f"  Created batch: {batch_name} ({batch_data.get('prospects', 0)} prospects)")

    conn.commit()
    conn.close()
    return count


def backfill_from_dnc_list():
    """Create DNC contact records from dnc-list.json."""
    dnc_file = ROOT / "work" / "dnc-list.json"
    if not dnc_file.exists():
        print("  Skipping: work/dnc-list.json not found")
        return 0

    dnc_data = json.loads(dnc_file.read_text())
    conn = get_backfill_db()
    count = 0
    now = datetime.utcnow().isoformat()

    for entry in dnc_data.get("contacts", []):
        name_parts = entry["name"].split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Check if already exists
        existing = conn.execute(
            "SELECT id FROM contacts WHERE first_name=? AND last_name=?",
            (first_name, last_name)
        ).fetchone()
        if existing:
            continue

        cid = gen_id("con")
        try:
            conn.execute("""
                INSERT INTO contacts (id, first_name, last_name, title,
                    do_not_contact, dnc_reason, status, source, created_at, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (
                cid, first_name, last_name, "Unknown",
                1, entry.get("reason", ""), "dnc", "dnc_backfill",
                now, now
            ))
            count += 1
            print(f"  Created DNC contact: {entry['name']} ({entry.get('company', 'unknown')})")
        except Exception as e:
            print(f"  Error creating DNC {entry['name']}: {e}")

    conn.commit()
    conn.close()
    return count


def backfill_from_batch7_tracker():
    """Import contacts from batch7-send-tracker.json if it exists."""
    tracker_file = ROOT / "batch7-send-tracker.json"
    if not tracker_file.exists():
        print("  Skipping: batch7-send-tracker.json not found")
        return 0

    tracker = json.loads(tracker_file.read_text())
    conn = get_backfill_db()
    count = 0
    now = datetime.utcnow().isoformat()

    prospects = tracker if isinstance(tracker, list) else tracker.get("prospects", [])

    for prospect in prospects:
        name = prospect.get("name", "")
        if not name:
            continue

        name_parts = name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Check if already exists
        existing = conn.execute(
            "SELECT id FROM contacts WHERE first_name=? AND last_name=?",
            (first_name, last_name)
        ).fetchone()
        if existing:
            continue

        company = prospect.get("company", "")

        # Create or find account (using same connection)
        acc_row = conn.execute(
            "SELECT id FROM accounts WHERE name=?", (company,)
        ).fetchone()
        if acc_row:
            account_id = acc_row["id"] if hasattr(acc_row, "keys") else acc_row[0]
        elif company:
            account_id = gen_id("acc")
            try:
                conn.execute("""
                    INSERT INTO accounts (id, name, domain, industry, created_at, updated_at)
                    VALUES (?,?,?,?,?,?)
                """, (account_id, company, prospect.get("domain", ""),
                      prospect.get("vertical", ""), now, now))
            except Exception:
                account_id = None
        else:
            account_id = None

        # Create contact (using same connection to avoid locking)
        cid = gen_id("con")
        linkedin_url = prospect.get("linkedin_url", prospect.get("salesNavUrl", ""))
        try:
            conn.execute("""
                INSERT INTO contacts (id, account_id, first_name, last_name, title,
                    persona_type, seniority_level, email, linkedin_url,
                    priority_score, status, source, created_at, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                cid, account_id, first_name, last_name,
                prospect.get("title", ""),
                prospect.get("persona_type", ""),
                prospect.get("seniority", ""),
                prospect.get("email", ""),
                linkedin_url if linkedin_url else None,
                prospect.get("priority_score", 3),
                prospect.get("status", "touch_1_sent"),
                "batch7_backfill",
                now, now
            ))
            count += 1
        except Exception as e:
            print(f"  Error creating {name}: {e}")

    conn.commit()
    conn.close()
    print(f"  Imported {count} contacts from batch7-send-tracker.json")
    return count


def print_db_stats():
    """Print current database record counts."""
    conn = get_backfill_db()
    print("\n--- Database Stats ---")
    for table in ["accounts", "contacts", "batches", "message_drafts", "touchpoints", "replies"]:
        try:
            row = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            print(f"  {table}: {row[0]}")
        except Exception:
            print(f"  {table}: (table not found)")
    conn.close()


def main():
    print("=== BDR Database Backfill ===\n")

    print("Before backfill:")
    print_db_stats()

    print("\n1. Backfilling batches from pipeline-state.json...")
    batch_count = backfill_from_pipeline_state()

    print("\n2. Backfilling DNC contacts from dnc-list.json...")
    dnc_count = backfill_from_dnc_list()

    print("\n3. Backfilling contacts from batch7-send-tracker.json...")
    b7_count = backfill_from_batch7_tracker()

    print(f"\n--- Summary ---")
    print(f"  Batches created: {batch_count}")
    print(f"  DNC contacts created: {dnc_count}")
    print(f"  Batch 7 contacts imported: {b7_count}")

    print("\nAfter backfill:")
    print_db_stats()

    print("\nBackfill complete. Run 'python scripts/backfill_db.py' again to import more data.")
    print("For HTML tracker imports, extend this script with HTML parsing for each batch file.")


if __name__ == "__main__":
    main()
