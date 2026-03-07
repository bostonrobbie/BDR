#!/usr/bin/env python3
"""
BDR Session End — One-command session close for multi-agent coordination.

Usage:
    python3 scripts/session_end.py \
        --agent Cowork-1 \
        --task TASK-002 \
        --status done \
        --summary "Built Touch 2 drafts for B10 (9 people) and B11 (4 people). All pass MQS >= 9/12." \
        --files "batches/batch10-touch2.html,batches/batch11-touch2.html" \
        --new-task "TASK-009|B10 Touch 2 send|HIGH|2026-03-11|Rob to review and approve Touch 2 drafts before send."

What it does:
1. Update work-queue.json (mark task done or update status)
2. Append entry to event-log.jsonl
3. Update agent-registry.json (set status=idle)
4. Print handoff.md update template (copy-paste ready)
5. Prepend session-log.md entry
6. git add + commit
7. Remind about push
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
AGENT_REGISTRY = SESSION_DIR / "agent-registry.json"
EVENT_LOG = SESSION_DIR / "event-log.jsonl"
SESSION_LOG = SESSION_DIR / "session-log.md"

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def now_display() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)

def save_json(path: Path, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def append_event(event: dict):
    with open(EVENT_LOG, "a") as f:
        f.write(json.dumps(event) + "\n")

def prepend_to_file(path: Path, content: str):
    existing = path.read_text() if path.exists() else ""
    with open(path, "w") as f:
        f.write(content + "\n\n" + existing)

def run_git(args: list) -> tuple[int, str, str]:
    result = subprocess.run(
        ["git"] + args,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def color(text: str, code: str) -> str:
    codes = {"red": "31", "green": "32", "yellow": "33", "cyan": "36", "bold": "1"}
    c = codes.get(code, "0")
    return f"\033[{c}m{text}\033[0m"

# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BDR Session End")
    parser.add_argument("--agent", required=True, help="Agent identifier (e.g. Cowork-1)")
    parser.add_argument("--task", required=True, help="Task ID being closed (e.g. TASK-002)")
    parser.add_argument("--status", default="done", choices=["done", "partial", "blocked"],
                        help="Completion status: done | partial | blocked")
    parser.add_argument("--summary", required=True, help="What was accomplished this session")
    parser.add_argument("--files", default="", help="Comma-separated list of files changed")
    parser.add_argument("--new-task", default="",
                        help="Optional new task to add: 'ID|title|priority|due|description'")
    parser.add_argument("--next-priorities", default="",
                        help="Optional comma-separated task IDs for next agent's top priorities")
    parser.add_argument("--blockers", default="",
                        help="Any blockers or flags for next agent")
    parser.add_argument("--session-title", default=None,
                        help="Optional session title for session log")
    args = parser.parse_args()

    agent_id = args.agent
    task_id = args.task
    files_changed = [f.strip() for f in args.files.split(",") if f.strip()]
    ts = now_iso()

    print()
    print(color("=" * 60, "bold"))
    print(color("  BDR SESSION END", "bold"))
    print(color(f"  Agent: {agent_id}  |  Task: {task_id}  |  Status: {args.status}", "cyan"))
    print(color("=" * 60, "bold"))
    print()

    # ── Step 1: Update Work Queue ─────────────────────────────────────────────
    queue = load_json(WORK_QUEUE_JSON)
    active_tasks = queue.get("active", [])
    completed_tasks = queue.get("completed", [])

    task_found = False
    completed_task = None

    for i, task in enumerate(active_tasks):
        if task["id"] == task_id:
            task_found = True
            completed_task = task.copy()
            completed_task["status"] = args.status
            completed_task["completed_at"] = ts
            completed_task["completed_by"] = agent_id
            completed_task["result"] = args.summary

            if args.status == "done":
                # Move to completed
                completed_tasks.insert(0, completed_task)
                active_tasks.pop(i)
                print(color(f"✓ Marked {task_id} as DONE and moved to completed.", "green"))
            elif args.status == "partial":
                # Keep in active, reset claim
                task["status"] = "pending"
                task["claimed_by"] = None
                task["claimed_at"] = None
                task["description"] = task.get("description", "") + f"\n[PARTIAL {ts[:10]} by {agent_id}]: {args.summary}"
                print(color(f"✓ Marked {task_id} as PARTIAL. Reset to pending for next agent.", "yellow"))
            elif args.status == "blocked":
                task["status"] = "blocked"
                task["claimed_by"] = None
                task["claimed_at"] = None
                task["blockers"] = (task.get("blockers") or []) + [f"[{ts[:10]}] {args.blockers or args.summary}"]
                print(color(f"✓ Marked {task_id} as BLOCKED. Added blocker note.", "yellow"))
            break

    if not task_found:
        print(color(f"⚠ Task {task_id} not found in active queue. Logging event only.", "yellow"))

    # Add new task if provided
    if args.new_task:
        try:
            parts = args.new_task.split("|")
            new_task = {
                "id": parts[0].strip(),
                "title": parts[1].strip() if len(parts) > 1 else "Untitled",
                "status": "pending",
                "priority": parts[2].strip() if len(parts) > 2 else "MEDIUM",
                "due": parts[3].strip() if len(parts) > 3 else None,
                "claimed_by": None,
                "claimed_at": None,
                "description": parts[4].strip() if len(parts) > 4 else "",
                "prospects": [],
                "blockers": [],
                "ref_files": [],
                "tags": ["auto-added"]
            }
            active_tasks.append(new_task)
            print(color(f"✓ Added new task: {new_task['id']} — {new_task['title']}", "green"))
        except Exception as e:
            print(color(f"⚠ Could not parse --new-task: {e}", "yellow"))

    queue["active"] = active_tasks
    queue["completed"] = completed_tasks
    queue["_meta"]["last_updated"] = ts
    save_json(WORK_QUEUE_JSON, queue)

    # ── Step 2: Append to Event Log ───────────────────────────────────────────
    event = {
        "ts": ts,
        "agent": agent_id,
        "machine": os.uname().nodename,
        "event_type": "task_complete" if args.status == "done" else f"task_{args.status}",
        "task_id": task_id,
        "summary": args.summary,
        "files_changed": files_changed
    }
    if args.blockers:
        event["blockers"] = args.blockers
    append_event(event)
    print(color("✓ Appended to event-log.jsonl.", "green"))

    # ── Step 3: Update Agent Registry ────────────────────────────────────────
    registry = load_json(AGENT_REGISTRY)
    if "agents" not in registry:
        registry["agents"] = {}
    if agent_id not in registry["agents"]:
        registry["agents"][agent_id] = {}
    registry["agents"][agent_id].update({
        "last_seen": ts,
        "status": "idle",
        "current_task": None
    })
    save_json(AGENT_REGISTRY, registry)
    print(color("✓ Updated agent-registry.json (status: idle).", "green"))
    print()

    # ── Step 4: Session Log Entry ─────────────────────────────────────────────
    session_title = args.session_title or args.summary[:60]
    files_str = "\n".join(f"- `{f}`" for f in files_changed) if files_changed else "- (none listed)"
    blockers_str = args.blockers if args.blockers else "None"
    session_log_entry = f"""## {ts[:10]} — {agent_id} — {session_title}
**Completed:** {args.summary}
**Task:** {task_id} ({args.status})
**Changed files:**
{files_str}
**Blockers:** {blockers_str}"""

    prepend_to_file(SESSION_LOG, session_log_entry)
    print(color("✓ Prepended entry to session-log.md.", "green"))
    print()

    # ── Step 5: Print Handoff Template ────────────────────────────────────────
    next_priorities = args.next_priorities or "TASK-001, TASK-002"
    print(color("─" * 60, "bold"))
    print(color("  HANDOFF.MD UPDATE TEMPLATE", "bold"))
    print(color("  Copy this into memory/session/handoff.md:", "cyan"))
    print(color("─" * 60, "bold"))
    print()
    print(f"""## What Was Done This Session
{args.summary}

## Current State Snapshot
(Update with current numbers from CLAUDE.md)

## Top 3 Priorities for Next Agent
1. {next_priorities.split(',')[0].strip() if next_priorities else 'TASK-001'} — (describe)
2. {next_priorities.split(',')[1].strip() if len(next_priorities.split(',')) > 1 else 'TASK-002'} — (describe)
3. Continue from work-queue.json

## Blockers / Flags
{blockers_str}

## Files Changed This Session
{files_str}""")
    print()
    print(color("─" * 60, "bold"))

    # ── Step 6: Commit ────────────────────────────────────────────────────────
    print()
    print(color("▶ Staging and committing...", "bold"))

    files_to_stage = [
        str(WORK_QUEUE_JSON.relative_to(REPO_ROOT)),
        str(AGENT_REGISTRY.relative_to(REPO_ROOT)),
        str(EVENT_LOG.relative_to(REPO_ROOT)),
        str(SESSION_LOG.relative_to(REPO_ROOT)),
    ] + files_changed

    for f in files_to_stage:
        run_git(["add", f])

    # Stage any other modified files
    run_git(["add", "-u"])

    commit_msg = f"Update {ts[:10]}: {args.summary[:80]} [{agent_id}]"
    code, out, err = run_git(["commit", "-m", commit_msg])
    if code == 0:
        print(color(f"✓ Committed: {commit_msg[:60]}...", "green"))
    else:
        if "nothing to commit" in out or "nothing to commit" in err:
            print(color("✓ Nothing to commit (already clean).", "green"))
        else:
            print(color(f"⚠ Commit failed: {err}", "yellow"))

    # ── Step 7: Push Reminder ─────────────────────────────────────────────────
    print()
    code, out, err = run_git(["push", "origin", "main"])
    if code == 0:
        print(color("✓ Pushed to origin/main.", "green"))
    else:
        print(color("⚠ Push failed (no credentials in VM).", "yellow"))
        print(color("  → Run this from your terminal:", "bold"))
        print(color("    git push origin main", "cyan"))

    print()
    print(color("✓ Session closed. Good work.", "green"))
    print()


if __name__ == "__main__":
    main()
