"""
Database Migration Runner - Sequential, versioned, idempotent schema migrations.

Tracks applied migrations in a schema_versions table. Each migration is a
numbered Python file in src/db/migrations/ that defines an up() function.

Usage:
    python -m src.db.migration_runner          # Apply pending migrations
    python -m src.db.migration_runner --status  # Show migration status
    python -m src.db.migration_runner --init    # Create schema_versions table only
"""

import argparse
import importlib
import os
import sqlite3
import sys
from datetime import datetime
from glob import glob

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "migrations")


def _get_db_path():
    try:
        from src.config import DB_PATH
        return DB_PATH
    except ImportError:
        return os.environ.get("OCC_DB_PATH", "outreach.db")


def _ensure_schema_versions(conn: sqlite3.Connection):
    """Create the schema_versions table if it doesn't exist."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_versions (
            version INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            applied_at TEXT NOT NULL,
            checksum TEXT
        )
    """)
    conn.commit()


def get_applied_versions(conn: sqlite3.Connection) -> set:
    """Get the set of already-applied migration version numbers."""
    _ensure_schema_versions(conn)
    rows = conn.execute("SELECT version FROM schema_versions ORDER BY version").fetchall()
    return {row[0] for row in rows}


def discover_migrations() -> list:
    """Find all migration files in the migrations directory.

    Returns list of (version, name, module_path) sorted by version.
    """
    pattern = os.path.join(MIGRATIONS_DIR, "[0-9]*.py")
    migrations = []

    for filepath in sorted(glob(pattern)):
        filename = os.path.basename(filepath)
        # Expected format: 001_description.py
        parts = filename.split("_", 1)
        if len(parts) < 2:
            continue
        try:
            version = int(parts[0])
        except ValueError:
            continue
        name = os.path.splitext(parts[1])[0]
        migrations.append((version, name, filepath))

    return sorted(migrations, key=lambda x: x[0])


def apply_migration(conn: sqlite3.Connection, version: int, name: str, filepath: str) -> bool:
    """Apply a single migration.

    The migration module must define an up(conn) function that takes a
    sqlite3.Connection and applies schema changes.

    Returns True if successful, False if failed.
    """
    module_name = f"migration_{version}"

    try:
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "up"):
            print(f"  ERROR: Migration {version}_{name} missing up() function")
            return False

        # Apply the migration
        module.up(conn)

        # Record it
        conn.execute(
            "INSERT INTO schema_versions (version, name, applied_at) VALUES (?, ?, ?)",
            (version, name, datetime.utcnow().isoformat())
        )
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"  ERROR applying migration {version}_{name}: {e}")
        return False


def run_migrations(db_path: str = None) -> dict:
    """Apply all pending migrations.

    Returns dict with counts and details.
    """
    path = db_path or _get_db_path()
    conn = sqlite3.connect(path)
    _ensure_schema_versions(conn)

    applied = get_applied_versions(conn)
    available = discover_migrations()

    pending = [(v, n, p) for v, n, p in available if v not in applied]

    result = {"applied": 0, "skipped": len(applied), "failed": 0, "errors": []}

    if not pending:
        print(f"Database is up to date ({len(applied)} migrations applied).")
        conn.close()
        return result

    print(f"Applying {len(pending)} pending migration(s)...")

    for version, name, filepath in pending:
        print(f"  [{version}] {name}...", end=" ")
        if apply_migration(conn, version, name, filepath):
            print("OK")
            result["applied"] += 1
        else:
            print("FAILED")
            result["failed"] += 1
            result["errors"].append(f"{version}_{name}")
            # Stop on first failure
            break

    conn.close()
    return result


def show_status(db_path: str = None):
    """Show migration status."""
    path = db_path or _get_db_path()

    if not os.path.exists(path):
        print(f"Database not found at {path}")
        return

    conn = sqlite3.connect(path)
    _ensure_schema_versions(conn)

    applied = get_applied_versions(conn)
    available = discover_migrations()

    print(f"Database: {path}")
    print(f"Applied: {len(applied)}")
    print(f"Available: {len(available)}")
    print()

    for version, name, _ in available:
        status = "applied" if version in applied else "PENDING"
        marker = "+" if version in applied else "-"
        print(f"  [{marker}] {version:03d}_{name} ({status})")

    # Check for applied migrations not in the filesystem
    available_versions = {v for v, _, _ in available}
    orphaned = applied - available_versions
    if orphaned:
        print(f"\n  Warning: {len(orphaned)} applied migration(s) not found in filesystem: {orphaned}")

    conn.close()


def main():
    parser = argparse.ArgumentParser(description="BDR Database Migration Runner")
    parser.add_argument("--status", action="store_true", help="Show migration status")
    parser.add_argument("--init", action="store_true", help="Initialize schema_versions table only")
    parser.add_argument("--db", type=str, help="Database path override")
    args = parser.parse_args()

    if args.status:
        show_status(args.db)
    elif args.init:
        path = args.db or _get_db_path()
        conn = sqlite3.connect(path)
        _ensure_schema_versions(conn)
        conn.close()
        print(f"schema_versions table created at {path}")
    else:
        result = run_migrations(args.db)
        if result["failed"]:
            sys.exit(1)


if __name__ == "__main__":
    main()
