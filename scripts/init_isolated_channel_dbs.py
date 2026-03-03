#!/usr/bin/env python3
"""Initialize isolated channel SQLite databases with the same schema.

Creates two DBs (email/linkedin) from a source schema database by copying DDL and
optionally data for shared reference tables.
"""
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

DEFAULT_SOURCE = Path("api/data/outreach_seed.db")
DEFAULT_EMAIL_DB = Path("api/data/outreach_email.db")
DEFAULT_LINKEDIN_DB = Path("api/data/outreach_linkedin.db")

# Tables that should be duplicated across both DBs to keep baseline context aligned.
SHARED_TABLES = {
    "accounts",
    "contacts",
    "feature_flags",
    "workflows",
}


def recreate_schema(src: sqlite3.Connection, dst: sqlite3.Connection) -> None:
    ddl_rows = src.execute(
        """
        SELECT sql FROM sqlite_master
        WHERE sql IS NOT NULL
          AND type IN ('table','index','trigger','view')
          AND name NOT LIKE 'sqlite_%'
        ORDER BY CASE type
            WHEN 'table' THEN 1
            WHEN 'index' THEN 2
            WHEN 'trigger' THEN 3
            WHEN 'view' THEN 4
            ELSE 5 END, name
        """
    ).fetchall()

    for (ddl,) in ddl_rows:
        try:
            dst.execute(ddl)
        except sqlite3.OperationalError as exc:
            # Skip duplicate index/view edge cases safely.
            if "already exists" not in str(exc).lower():
                raise


def copy_table_data(src: sqlite3.Connection, dst: sqlite3.Connection, table: str) -> None:
    cols = [r[1] for r in src.execute(f"PRAGMA table_info({table})").fetchall()]
    if not cols:
        return
    quoted_cols = ", ".join([f'"{c}"' for c in cols])
    rows = src.execute(f"SELECT {quoted_cols} FROM {table}").fetchall()
    if not rows:
        return
    placeholders = ", ".join(["?"] * len(cols))
    dst.executemany(
        f"INSERT INTO {table} ({quoted_cols}) VALUES ({placeholders})",
        rows,
    )


def init_channel_db(source_path: Path, target_path: Path, channel: str) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    if target_path.exists():
        target_path.unlink()

    with sqlite3.connect(source_path) as src, sqlite3.connect(target_path) as dst:
        src.row_factory = sqlite3.Row
        recreate_schema(src, dst)

        # Copy shared baseline tables to both DBs.
        for table in SHARED_TABLES:
            copy_table_data(src, dst, table)

        # Copy only channel-specific touch/message history for isolation.
        for table in ("message_drafts", "touchpoints", "activity_timeline", "workflow_runs", "replies"):
            existing = src.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)
            ).fetchone()
            if not existing:
                continue

            cols = [r[1] for r in src.execute(f"PRAGMA table_info({table})").fetchall()]
            if not cols:
                continue

            quoted_cols = ", ".join([f'"{c}"' for c in cols])
            has_channel = "channel" in cols
            query = f"SELECT {quoted_cols} FROM {table}"
            params = ()
            if has_channel:
                query += " WHERE channel = ?"
                params = (channel,)
            rows = src.execute(query, params).fetchall()
            if rows:
                placeholders = ", ".join(["?"] * len(cols))
                dst.executemany(
                    f"INSERT INTO {table} ({quoted_cols}) VALUES ({placeholders})", rows
                )

        dst.commit()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--email-db", type=Path, default=DEFAULT_EMAIL_DB)
    p.add_argument("--linkedin-db", type=Path, default=DEFAULT_LINKEDIN_DB)
    args = p.parse_args()

    if not args.source.exists():
        raise SystemExit(f"Source DB not found: {args.source}")

    init_channel_db(args.source, args.email_db, "email")
    init_channel_db(args.source, args.linkedin_db, "linkedin")

    print(f"Created email DB: {args.email_db}")
    print(f"Created linkedin DB: {args.linkedin_db}")


if __name__ == "__main__":
    main()
