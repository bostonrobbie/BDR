#!/usr/bin/env python3
"""
BDR Claim Task — Atomic task claiming for multi-agent coordination.

Usage:
    python3 scripts/claim_task.py --agent Cowork-1 --task TASK-002

What it does:
1. git pull (get latest state — critical before claiming)
2. Check if task is already claimed
3. Write claim (status=in_progress, claimed_by, claimed_at)
4. Commit + push immediately (minimize race window)
5. Confirm or report conflict

Design principle: the window between read and push is as small as possible.
If two agents claim simultaneously, git push will reject one — first push wins.
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

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

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

def hours_ago(ts: str) -> float:
    if not ts:
        return float("inf")
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).total_seconds() / 3600
    except Exception:
        return float("inf")

# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BDR Claim Task — atomic claiming")
    parser.add_argument("--agent", required=True, help="Agent identifier (e.g. Cowork-1)")
    parser.add_argument("--task", required=True, help="Task ID to claim (e.g. TASK-002)")
    parser.add_argument("--force", action="store_true",
                        help="Force-claim even if already claimed (use only if you know the other agent is dead)")
    parser.add_argument("--no-pull", action="store_true",
                        help="Skip git pull (dangerous — only for offline debugging)")
    args = parser.parse_args()

    agent_id = args.agent
    task_id = args.task
    ts = now_iso()

    print()
    print(color("=" * 60, "bold"))
    print(color("  BDR CLAIM TASK", "bold"))
    print(color(f"  Agent: {agent_id}  |  Task: {task_id}", "cyan"))
    print(color("=" * 60, "bold"))
    print()

    # ── Step 1: Pull latest state ────────────────────────────────────────────
    if not args.no_pull:
        print(color("▶ Pulling latest state from origin/main...", "bold"))
        code, out, err = run_git(["pull", "origin", "main"])
        if code == 0:
            if "Already up to date" in out:
                print(color("  ✓ Already up to date.", "green"))
            else:
                lines = [l for l in out.split("\n") if l.strip()]
                print(color(f"  ✓ Pulled. {len(lines)} line(s) updated.", "green"))
        else:
            print(color(f"  ⚠ Pull failed: {err}", "yellow"))
            print("  Continuing with local state — there may be a conflict on push.")
        print()
    else:
        print(color("⚠ Skipping pull (--no-pull). Race condition risk elevated.", "yellow"))
        print()

    # ── Step 2: Load and check task ──────────────────────────────────────────
    queue = load_json(WORK_QUEUE_JSON)
    active_tasks = queue.get("active", [])

    target_task = None
    task_index = None
    for i, task in enumerate(active_tasks):
        if task["id"] == task_id:
            target_task = task
            task_index = i
            break

    if target_task is None:
        # Check if it's in completed
        for task in queue.get("completed", []):
            if task["id"] == task_id:
                print(color(f"✗ {task_id} is already COMPLETED. Nothing to claim.", "red"))
                print(f"  Completed at: {task.get('completed_at', 'unknown')}")
                print(f"  By: {task.get('completed_by', 'unknown')}")
                sys.exit(1)
        print(color(f"✗ Task {task_id} not found in work-queue.json.", "red"))
        print("  Available tasks:")
        for t in active_tasks:
            status = t.get("status", "?")
            print(f"  → {t['id']} [{status}] {t['title']}")
        sys.exit(1)

    # ── Step 3: Check for existing claim ────────────────────────────────────
    current_status = target_task.get("status")
    current_claimer = target_task.get("claimed_by")
    claimed_at = target_task.get("claimed_at")

    if current_status == "in_progress" and current_claimer:
        age_h = hours_ago(claimed_at)
        print(color(f"⚠ {task_id} is already claimed.", "yellow"))
        print(f"  Claimed by: {color(current_claimer, 'cyan')}")
        print(f"  Claimed at: {claimed_at} ({age_h:.1f}h ago)")

        if age_h > 4:
            print(color("  ⚠ Claim is STALE (>4h). You may safely claim with --force.", "yellow"))
        else:
            print(color("  Claim is fresh. Do NOT claim unless you have confirmed the other agent is dead.", "red"))

        if not args.force:
            print()
            print(color("  Aborting. Use --force to override.", "bold"))
            sys.exit(1)
        else:
            print(color("  --force specified. Overriding claim.", "yellow"))
            print()

    elif current_status == "blocked":
        blockers = target_task.get("blockers", [])
        print(color(f"⚠ {task_id} is marked BLOCKED.", "yellow"))
        for b in blockers:
            print(color(f"  BLOCKER: {b}", "yellow"))
        print()
        print("  Proceeding with claim (resolve blocker before closing session).")

    # ── Step 4: Write the claim ──────────────────────────────────────────────
    # Do this as fast as possible to minimize the race window
    active_tasks[task_index]["status"] = "in_progress"
    active_tasks[task_index]["claimed_by"] = agent_id
    active_tasks[task_index]["claimed_at"] = ts

    queue["active"] = active_tasks
    queue["_meta"]["last_updated"] = ts
    save_json(WORK_QUEUE_JSON, queue)

    # Update agent registry
    registry = load_json(AGENT_REGISTRY)
    if "agents" not in registry:
        registry["agents"] = {}
    if agent_id not in registry["agents"]:
        registry["agents"][agent_id] = {}
    registry["agents"][agent_id].update({
        "last_seen": ts,
        "status": "active",
        "current_task": task_id
    })
    save_json(AGENT_REGISTRY, registry)

    # Log event
    append_event({
        "ts": ts,
        "agent": agent_id,
        "machine": os.uname().nodename,
        "event_type": "task_claimed",
        "task_id": task_id,
        "summary": f"Claimed {task_id}: {target_task['title']}",
        "files_changed": []
    })

    print(color(f"✓ Claim written for {task_id}: {target_task['title']}", "green"))
    print()

    # ── Step 5: Commit + Push immediately ───────────────────────────────────
    print(color("▶ Committing and pushing claim (minimize race window)...", "bold"))

    run_git(["add",
             str(WORK_QUEUE_JSON.relative_to(REPO_ROOT)),
             str(AGENT_REGISTRY.relative_to(REPO_ROOT)),
             str(EVENT_LOG.relative_to(REPO_ROOT))])

    commit_msg = f"chore: claim {task_id} by {agent_id} [{ts[:10]}]"
    code, out, err = run_git(["commit", "-m", commit_msg])

    if code != 0:
        if "nothing to commit" in out or "nothing to commit" in err:
            print(color("  ✓ Already committed.", "green"))
        else:
            print(color(f"  ⚠ Commit failed: {err}", "yellow"))
    else:
        print(color(f"  ✓ Committed: {commit_msg}", "green"))

    # Push
    code, out, err = run_git(["push", "origin", "main"])
    if code == 0:
        print(color("  ✓ Pushed to origin/main. Claim is now visible to all agents.", "green"))
    else:
        # Check if push was rejected (another agent claimed first)
        if "rejected" in err or "non-fast-forward" in err or "fetch first" in err:
            print(color("  ✗ PUSH REJECTED — another agent may have claimed first!", "red"))
            print(color("  → Pull, check work-queue.json, and retry if still available.", "yellow"))
            print()
            print("  To investigate:")
            print("    git pull origin main")
            print(f"    python3 scripts/claim_task.py --agent {agent_id} --task {task_id}")
            sys.exit(1)
        else:
            print(color("  ⚠ Push failed (no credentials in VM).", "yellow"))
            print(color("  → Run from your terminal to register claim with other agents:", "bold"))
            print(color("    git push origin main", "cyan"))

    # ── Final Summary ────────────────────────────────────────────────────────
    print()
    print(color("─" * 60, "bold"))
    print(color(f"  ✓ {task_id} claimed by {agent_id}", "green"))
    print()
    print(f"  Task: {target_task['title']}")
    print(f"  Priority: {target_task.get('priority', '?')}")
    print(f"  Due: {target_task.get('due') or 'no deadline'}")
    if target_task.get("description"):
        # Truncate long descriptions
        desc = target_task["description"]
        print(f"  Description: {desc[:120]}{'...' if len(desc) > 120 else ''}")
    if target_task.get("ref_files"):
        print(f"  Ref files: {', '.join(target_task['ref_files'])}")
    if target_task.get("blockers"):
        for b in target_task["blockers"]:
            print(color(f"  ⚠ BLOCKER: {b}", "yellow"))
    print()
    print(f"  When done: python3 scripts/session_end.py --agent {agent_id} --task {task_id} --summary '...'")
    print(color("─" * 60, "bold"))
    print()


if __name__ == "__main__":
    main()
