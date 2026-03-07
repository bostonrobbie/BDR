#!/usr/bin/env python3
"""
BDR New Task — Add a task to the work queue without hand-editing JSON.

Usage:
    python3 scripts/new_task.py \
        --id TASK-009 \
        --title "Mon Mar 9 — Call blitz" \
        --priority HIGH \
        --due 2026-03-09 \
        --description "Call all B10 prospects who haven't replied to InMail." \
        --tags "calls,batch10"

    python3 scripts/new_task.py --list      # Show current task list
    python3 scripts/new_task.py --complete TASK-009  # Mark a task done
    python3 scripts/new_task.py --block TASK-009 --reason "Waiting for Nav credits"

Automatically:
    - Validates the task ID format and uniqueness
    - Adds to work-queue.json
    - Regenerates work-queue.md to stay in sync
    - Appends event to event-log.jsonl
    - Commits (but does NOT push — do that when closing the session)
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ─── PATHS ─────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent
SESSION_DIR = REPO_ROOT / "memory" / "session"
WORK_QUEUE_JSON = SESSION_DIR / "work-queue.json"
WORK_QUEUE_MD = SESSION_DIR / "work-queue.md"
EVENT_LOG = SESSION_DIR / "event-log.jsonl"

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load_json(path):
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def append_event(event):
    with open(EVENT_LOG, "a") as f:
        f.write(json.dumps(event) + "\n")

def run_git(args):
    result = subprocess.run(
        ["git"] + args,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def c(text, code):
    codes = {"red": "31", "green": "32", "yellow": "33", "cyan": "36", "bold": "1", "dim": "2"}
    return f"\033[{codes.get(code, '0')}m{text}\033[0m"

def priority_sort_key(task):
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    return (order.get(task.get("priority", "LOW"), 3), task.get("due") or "9999")

def regenerate_md(queue):
    """Regenerate work-queue.md from work-queue.json to keep them in sync."""
    active = queue.get("active", [])
    completed = queue.get("completed", [])
    ts = queue.get("_meta", {}).get("last_updated", now_iso())[:10]

    in_prog = [t for t in active if t.get("status") == "in_progress"]
    pending = sorted([t for t in active if t.get("status") == "pending"], key=priority_sort_key)
    blocked = [t for t in active if t.get("status") == "blocked"]

    lines = [
        f"# Work Queue",
        f"",
        f"**Last updated:** {ts}  ",
        f"**Source of truth:** `memory/session/work-queue.json` (this file is auto-generated)",
        f"",
        f"---",
        f"",
    ]

    if in_prog:
        lines += ["## 🔵 In Progress", ""]
        for t in in_prog:
            claimer = t.get("claimed_by", "?")
            lines.append(f"### {t['id']} — {t['title']}")
            lines.append(f"- **Status:** IN PROGRESS → claimed by `{claimer}` at `{t.get('claimed_at', '?')}`")
            lines.append(f"- **Priority:** {t.get('priority', '?')}  |  **Due:** {t.get('due', 'TBD')}")
            if t.get("description"):
                lines.append(f"- **Description:** {t['description']}")
            if t.get("ref_files"):
                lines.append(f"- **Ref files:** {', '.join(t['ref_files'])}")
            lines.append("")

    if pending:
        lines += ["## 🟡 Pending", ""]
        lines.append("| ID | Priority | Due | Title |")
        lines.append("|-----|----------|-----|-------|")
        for t in pending:
            lines.append(f"| {t['id']} | {t.get('priority','?')} | {t.get('due','—')} | {t['title']} |")
        lines.append("")
        for t in pending:
            lines.append(f"### {t['id']} — {t['title']}")
            lines.append(f"- **Priority:** {t.get('priority', '?')}  |  **Due:** {t.get('due', 'TBD')}")
            if t.get("description"):
                lines.append(f"- **Description:** {t['description']}")
            if t.get("prospects"):
                lines.append(f"- **Prospects:** {', '.join(t['prospects'])}")
            if t.get("ref_files"):
                lines.append(f"- **Ref files:** {', '.join(t['ref_files'])}")
            if t.get("tags"):
                lines.append(f"- **Tags:** {', '.join(t['tags'])}")
            lines.append("")

    if blocked:
        lines += ["## 🔴 Blocked", ""]
        for t in blocked:
            lines.append(f"### {t['id']} — {t['title']}")
            for b in t.get("blockers", []):
                lines.append(f"- ⚠ **BLOCKER:** {b}")
            lines.append("")

    if completed:
        lines += ["---", "## ✅ Completed", ""]
        lines.append("| ID | Title | Completed | By |")
        lines.append("|-----|-------|-----------|-----|")
        for t in sorted(completed, key=lambda x: x.get("completed_at", ""), reverse=True)[:10]:
            lines.append(f"| {t['id']} | {t['title']} | {t.get('completed_at','?')[:10]} | {t.get('completed_by','?')} |")
        lines.append("")

    lines.append("---")
    lines.append(f"*Auto-generated from work-queue.json. Do not edit manually.*")

    WORK_QUEUE_MD.write_text("\n".join(lines) + "\n")


def next_task_id(queue):
    """Suggest the next task ID based on existing IDs."""
    active = queue.get("active", [])
    completed = queue.get("completed", [])
    all_ids = [t["id"] for t in active + completed if t["id"].startswith("TASK-")]
    nums = []
    for tid in all_ids:
        try:
            nums.append(int(tid.split("-")[1]))
        except Exception:
            pass
    if not nums:
        return "TASK-009"
    return f"TASK-{max(nums)+1:03d}"

# ─── ACTIONS ───────────────────────────────────────────────────────────────────

def list_tasks(queue):
    active = queue.get("active", [])
    completed = queue.get("completed", [])
    print()
    print(c("Current task queue:", "bold"))
    print()
    in_prog = [t for t in active if t.get("status") == "in_progress"]
    pending = sorted([t for t in active if t.get("status") == "pending"], key=priority_sort_key)
    blocked = [t for t in active if t.get("status") == "blocked"]

    if in_prog:
        print(c("  In Progress:", "green"))
        for t in in_prog:
            print(f"  ▶ {c(t['id'], 'bold')} [{t.get('priority','?')}] {t['title']}  → {t.get('claimed_by','?')}")
    if pending:
        print(c("  Pending:", "yellow"))
        for t in pending:
            pri_color = {"HIGH": "yellow", "CRITICAL": "red", "MEDIUM": "cyan", "LOW": "dim"}.get(t.get("priority","MEDIUM"), "dim")
            print(f"  ○ {c(t['id'], 'bold')} [{c(t.get('priority','?'), pri_color)}] {t['title']}")
    if blocked:
        print(c("  Blocked:", "red"))
        for t in blocked:
            print(f"  ✗ {c(t['id'], 'bold')} {t['title']}")
    print()
    print(c(f"  {len(completed)} completed tasks (use --show-completed to see them)", "dim"))
    print()


def add_task(args, queue):
    task_id = args.id
    ts = now_iso()

    # Validate ID format
    if not task_id.startswith("TASK-") and not task_id.startswith("TASK-C"):
        print(c(f"⚠ ID should be TASK-XXX format (e.g. TASK-009). Got: {task_id}", "yellow"))
        suggested = next_task_id(queue)
        print(c(f"  Suggested next ID: {suggested}", "cyan"))

    # Check uniqueness
    all_tasks = queue.get("active", []) + queue.get("completed", [])
    for t in all_tasks:
        if t["id"] == task_id:
            print(c(f"✗ Task {task_id} already exists! Use a different ID.", "red"))
            print(f"  Existing: {t['title']} [{t.get('status','?')}]")
            sys.exit(1)

    # Build task
    new_task = {
        "id": task_id,
        "title": args.title,
        "status": "pending",
        "priority": args.priority.upper(),
        "due": args.due,
        "claimed_by": None,
        "claimed_at": None,
        "description": args.description or "",
        "prospects": [p.strip() for p in args.prospects.split(",")] if args.prospects else [],
        "blockers": [],
        "ref_files": [f.strip() for f in args.ref_files.split(",")] if args.ref_files else [],
        "tags": [t.strip() for t in args.tags.split(",")] if args.tags else [],
        "added_at": ts,
        "added_by": args.agent or "manual"
    }

    queue.setdefault("active", []).append(new_task)
    queue.setdefault("_meta", {})["last_updated"] = ts
    save_json(WORK_QUEUE_JSON, queue)
    regenerate_md(queue)

    append_event({
        "ts": ts,
        "agent": args.agent or "manual",
        "machine": os.uname().nodename,
        "event_type": "task_added",
        "task_id": task_id,
        "summary": f"Added {task_id}: {args.title} [{args.priority}]",
        "files_changed": []
    })

    print()
    print(c(f"✓ Task {task_id} added to work-queue.json and work-queue.md", "green"))
    print(f"  Title: {args.title}")
    print(f"  Priority: {args.priority.upper()}  |  Due: {args.due or 'TBD'}")
    print()
    print(c("  Note: Task is local only. It will be pushed on your next git commit.", "dim"))
    print()


def complete_task(task_id, agent, queue):
    ts = now_iso()
    active = queue.get("active", [])
    for i, t in enumerate(active):
        if t["id"] == task_id:
            t["status"] = "done"
            t["completed_at"] = ts
            t["completed_by"] = agent or "manual"
            queue.setdefault("completed", []).append(t)
            active.pop(i)
            queue["active"] = active
            queue["_meta"]["last_updated"] = ts
            save_json(WORK_QUEUE_JSON, queue)
            regenerate_md(queue)
            append_event({
                "ts": ts, "agent": agent or "manual",
                "machine": os.uname().nodename,
                "event_type": "task_completed",
                "task_id": task_id,
                "summary": f"Marked {task_id} done: {t['title']}",
                "files_changed": []
            })
            print(c(f"✓ {task_id} marked complete.", "green"))
            return
    print(c(f"✗ Task {task_id} not found in active tasks.", "red"))
    sys.exit(1)


def block_task(task_id, reason, agent, queue):
    ts = now_iso()
    for t in queue.get("active", []):
        if t["id"] == task_id:
            t["status"] = "blocked"
            t.setdefault("blockers", []).append(reason)
            t["claimed_by"] = None
            t["claimed_at"] = None
            queue["_meta"]["last_updated"] = ts
            save_json(WORK_QUEUE_JSON, queue)
            regenerate_md(queue)
            append_event({
                "ts": ts, "agent": agent or "manual",
                "machine": os.uname().nodename,
                "event_type": "task_blocked",
                "task_id": task_id,
                "summary": f"Blocked {task_id}: {reason}",
                "files_changed": []
            })
            print(c(f"✓ {task_id} marked blocked: {reason}", "yellow"))
            return
    print(c(f"✗ Task {task_id} not found.", "red"))
    sys.exit(1)

# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BDR New Task — manage the work queue")
    parser.add_argument("--id", help="Task ID (e.g. TASK-009)")
    parser.add_argument("--title", help="Task title")
    parser.add_argument("--priority", default="MEDIUM", choices=["CRITICAL", "HIGH", "MEDIUM", "LOW"])
    parser.add_argument("--due", help="Due date (YYYY-MM-DD)")
    parser.add_argument("--description", help="Full task description")
    parser.add_argument("--prospects", help="Comma-separated prospect names")
    parser.add_argument("--ref-files", help="Comma-separated reference file paths")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--agent", help="Agent adding this task (for logging)")
    parser.add_argument("--list", action="store_true", help="List all tasks and exit")
    parser.add_argument("--show-completed", action="store_true", help="Include completed tasks in list")
    parser.add_argument("--complete", metavar="TASK_ID", help="Mark a task as complete")
    parser.add_argument("--block", metavar="TASK_ID", help="Mark a task as blocked")
    parser.add_argument("--reason", help="Reason for blocking (use with --block)")
    parser.add_argument("--suggest-id", action="store_true", help="Suggest the next task ID and exit")
    args = parser.parse_args()

    queue = load_json(WORK_QUEUE_JSON)

    if args.suggest_id:
        print(f"Suggested next task ID: {c(next_task_id(queue), 'cyan')}")
        return

    if args.list or args.show_completed:
        list_tasks(queue)
        return

    if args.complete:
        complete_task(args.complete, args.agent, queue)
        return

    if args.block:
        if not args.reason:
            print(c("✗ --reason is required when using --block", "red"))
            sys.exit(1)
        block_task(args.block, args.reason, args.agent, queue)
        return

    # Default: add a new task
    if not args.id or not args.title:
        parser.print_help()
        print()
        print(c(f"  Suggested next ID: {next_task_id(queue)}", "cyan"))
        sys.exit(1)

    add_task(args, queue)


if __name__ == "__main__":
    main()
