#!/usr/bin/env python3
"""
BDR Sync Queue — Regenerate work-queue.md from work-queue.json.

Usage:
    python3 scripts/sync_queue.py          # Sync and report
    python3 scripts/sync_queue.py --check  # Only check if in sync (exit 1 if not)
    python3 scripts/sync_queue.py --commit # Sync and commit the result

Run this whenever:
    - You've manually edited work-queue.json
    - You suspect work-queue.md is out of date
    - After any script that modifies work-queue.json (session_end, new_task, claim_task)
    - Before pushing to remote to ensure both files are current

Design: work-queue.json is the source of truth. work-queue.md is always
derived from it — never edit .md directly.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ─── PATHS ─────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent
SESSION_DIR = REPO_ROOT / "memory" / "session"
WORK_QUEUE_JSON = SESSION_DIR / "work-queue.json"
WORK_QUEUE_MD = SESSION_DIR / "work-queue.md"

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load_json(path):
    if not path.exists():
        print(f"✗ {path} not found.")
        sys.exit(1)
    with open(path) as f:
        return json.load(f)

def run_git(args):
    result = subprocess.run(["git"] + args, cwd=REPO_ROOT, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def c(text, code):
    codes = {"red": "31", "green": "32", "yellow": "33", "cyan": "36", "bold": "1", "dim": "2"}
    return f"\033[{codes.get(code, '0')}m{text}\033[0m"

def priority_sort_key(task):
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    return (order.get(task.get("priority", "LOW"), 3), task.get("due") or "9999")

def hours_ago(ts):
    if not ts:
        return float("inf")
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).total_seconds() / 3600
    except Exception:
        return float("inf")

# ─── MD GENERATOR ──────────────────────────────────────────────────────────────

def generate_md(queue):
    """Full regeneration of work-queue.md from work-queue.json."""
    active = queue.get("active", [])
    completed = queue.get("completed", [])
    meta = queue.get("_meta", {})
    ts = meta.get("last_updated", now_iso())[:10]
    stale_hours = meta.get("stale_claim_expiry_hours", 4)

    in_prog = [t for t in active if t.get("status") == "in_progress"]
    pending = sorted([t for t in active if t.get("status") == "pending"], key=priority_sort_key)
    blocked = [t for t in active if t.get("status") == "blocked"]

    lines = [
        "# Work Queue",
        "",
        f"**Last updated:** {ts}  ",
        "**Source of truth:** `memory/session/work-queue.json`  ",
        "**This file is auto-generated** by `scripts/sync_queue.py`. Do not edit manually.",
        f"**Stale claim threshold:** {stale_hours}h — expired claims auto-reset on `session_start.py`",
        "",
        "---",
        "",
    ]

    # Summary table
    lines += [
        "## Summary",
        "",
        f"| Status | Count |",
        f"|--------|-------|",
        f"| 🔵 In Progress | {len(in_prog)} |",
        f"| 🟡 Pending | {len(pending)} |",
        f"| 🔴 Blocked | {len(blocked)} |",
        f"| ✅ Completed | {len(completed)} |",
        "",
        "---",
        "",
    ]

    # In Progress
    if in_prog:
        lines += ["## 🔵 In Progress", ""]
        for t in in_prog:
            claimer = t.get("claimed_by", "?")
            claimed_at = t.get("claimed_at", "?")
            h = hours_ago(claimed_at)
            stale_flag = "  ⚠ **STALE**" if h > stale_hours else ""

            lines.append(f"### {t['id']} — {t['title']}")
            lines.append(f"")
            lines.append(f"| Field | Value |")
            lines.append(f"|-------|-------|")
            lines.append(f"| Status | IN PROGRESS{stale_flag} |")
            lines.append(f"| Claimed by | `{claimer}` |")
            lines.append(f"| Claimed at | `{claimed_at}` |")
            lines.append(f"| Priority | {t.get('priority','?')} |")
            lines.append(f"| Due | {t.get('due','TBD')} |")
            if t.get("description"):
                lines.append(f"| Description | {t['description']} |")
            lines.append("")

    # Pending
    if pending:
        lines += ["## 🟡 Pending", ""]

        # Quick reference table
        lines.append("| ID | Priority | Due | Title |")
        lines.append("|-----|----------|-----|-------|")
        for t in pending:
            lines.append(f"| `{t['id']}` | {t.get('priority','?')} | {t.get('due','—')} | {t['title']} |")
        lines.append("")

        # Detail cards
        for t in pending:
            lines.append(f"### {t['id']} — {t['title']}")
            lines.append("")
            lines.append(f"- **Priority:** {t.get('priority','?')}  |  **Due:** {t.get('due','TBD')}")
            if t.get("description"):
                lines.append(f"- **Description:** {t['description']}")
            if t.get("prospects"):
                lines.append(f"- **Prospects:** {', '.join(t['prospects'])}")
            if t.get("ref_files"):
                lines.append(f"- **Read first:** {', '.join(t['ref_files'])}")
            if t.get("tags"):
                lines.append(f"- **Tags:** `{'` `'.join(t['tags'])}`")
            if t.get("blockers"):
                for b in t["blockers"]:
                    lines.append(f"- ⚠ **BLOCKER:** {b}")
            lines.append("")

    # Blocked
    if blocked:
        lines += ["## 🔴 Blocked", ""]
        for t in blocked:
            lines.append(f"### {t['id']} — {t['title']}")
            lines.append("")
            lines.append(f"- **Priority:** {t.get('priority','?')}  |  **Due:** {t.get('due','TBD')}")
            for b in t.get("blockers", []):
                lines.append(f"- ⚠ **BLOCKER:** {b}")
            if t.get("description"):
                lines.append(f"- **Description:** {t['description']}")
            lines.append("")

    # Completed
    if completed:
        recent_completed = sorted(completed, key=lambda x: x.get("completed_at", ""), reverse=True)
        lines += ["---", "## ✅ Completed", ""]
        lines.append("| ID | Title | Completed | By |")
        lines.append("|-----|-------|-----------|-----|")
        for t in recent_completed[:20]:
            comp_date = (t.get("completed_at") or "?")[:10]
            lines.append(f"| `{t['id']}` | {t['title']} | {comp_date} | {t.get('completed_by','?')} |")
        if len(completed) > 20:
            lines.append(f"| ... | *{len(completed)-20} more in work-queue.json* | | |")
        lines.append("")

    lines += [
        "---",
        "",
        "*Auto-generated from `memory/session/work-queue.json`.*  ",
        "*To modify: edit the JSON file directly, or use `scripts/new_task.py`.*  ",
        "*To sync: run `python3 scripts/sync_queue.py`.*",
        "",
    ]

    return "\n".join(lines)

# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BDR Sync Queue — keep work-queue.md in sync with JSON")
    parser.add_argument("--check", action="store_true", help="Only check if in sync (exit 1 if not)")
    parser.add_argument("--commit", action="store_true", help="Commit after syncing")
    args = parser.parse_args()

    queue = load_json(WORK_QUEUE_JSON)
    new_md = generate_md(queue)

    if args.check:
        if WORK_QUEUE_MD.exists():
            current = WORK_QUEUE_MD.read_text()
            if current == new_md:
                print(c("✓ work-queue.md is in sync with work-queue.json.", "green"))
                sys.exit(0)
            else:
                print(c("✗ work-queue.md is OUT OF SYNC with work-queue.json.", "red"))
                print(c("  Run: python3 scripts/sync_queue.py", "yellow"))
                sys.exit(1)
        else:
            print(c("✗ work-queue.md does not exist. Run: python3 scripts/sync_queue.py", "red"))
            sys.exit(1)

    # Write the file
    WORK_QUEUE_MD.write_text(new_md)

    active = queue.get("active", [])
    completed = queue.get("completed", [])
    in_prog = [t for t in active if t.get("status") == "in_progress"]
    pending = [t for t in active if t.get("status") == "pending"]
    blocked = [t for t in active if t.get("status") == "blocked"]

    print()
    print(c("✓ work-queue.md regenerated.", "green"))
    print(f"  {len(in_prog)} in progress  |  {len(pending)} pending  |  {len(blocked)} blocked  |  {len(completed)} completed")
    print()

    if args.commit:
        run_git(["add",
                 str(WORK_QUEUE_JSON.relative_to(REPO_ROOT)),
                 str(WORK_QUEUE_MD.relative_to(REPO_ROOT))])
        ts = now_iso()[:10]
        code, out, err = run_git(["commit", "-m", f"chore: sync work-queue.md from JSON [{ts}]"])
        if code == 0:
            print(c("  ✓ Committed.", "green"))
        elif "nothing to commit" in out or "nothing to commit" in err:
            print(c("  ✓ Already up to date — nothing to commit.", "green"))
        else:
            print(c(f"  ⚠ Commit failed: {err}", "yellow"))
        print()


if __name__ == "__main__":
    main()
