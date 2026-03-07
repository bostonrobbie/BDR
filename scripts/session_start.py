#!/usr/bin/env python3
"""
BDR Session Start — One-command session initialization for multi-agent coordination.

Usage:
    python3 scripts/session_start.py --agent Cowork-1
    python3 scripts/session_start.py --agent Cowork-2 --machine PC2

What it does:
1. git pull (get latest state from all agents)
2. Detect stale task claims (> 4h with no activity)
3. Show agent registry (who was active, what they were doing)
4. Show recent event log (what happened since you last pulled)
5. Display prioritized pending task list
6. Register this agent as active
7. Optionally claim a task
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ─── PATHS ─────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent
SESSION_DIR = REPO_ROOT / "memory" / "session"
WORK_QUEUE_JSON = SESSION_DIR / "work-queue.json"
AGENT_REGISTRY = SESSION_DIR / "agent-registry.json"
EVENT_LOG = SESSION_DIR / "event-log.jsonl"
HANDOFF = SESSION_DIR / "handoff.md"

STALE_HOURS = 4
RECENT_EVENTS = 10  # how many recent events to display

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def parse_iso(ts: str) -> datetime:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None

def hours_ago(ts: str) -> float:
    """Return how many hours ago a timestamp was."""
    dt = parse_iso(ts)
    if not dt:
        return float("inf")
    delta = datetime.now(timezone.utc) - dt
    return delta.total_seconds() / 3600

def is_stale(ts: str) -> bool:
    return hours_ago(ts) > STALE_HOURS

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)

def save_json(path: Path, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    f.close()

def load_event_log(n: int = RECENT_EVENTS) -> list:
    if not EVENT_LOG.exists():
        return []
    events = []
    with open(EVENT_LOG) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except Exception:
                    pass
    return events[-n:]

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
    """ANSI color codes for terminal output."""
    codes = {"red": "31", "green": "32", "yellow": "33", "cyan": "36", "bold": "1", "reset": "0"}
    c = codes.get(code, "0")
    return f"\033[{c}m{text}\033[0m"

# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BDR Session Start")
    parser.add_argument("--agent", required=True, help="Agent identifier (e.g. Cowork-1)")
    parser.add_argument("--machine", default=None, help="Machine name (e.g. Rob-PC)")
    parser.add_argument("--no-pull", action="store_true", help="Skip git pull (for offline use)")
    parser.add_argument("--claim", default=None, help="Task ID to claim immediately (e.g. TASK-002)")
    args = parser.parse_args()

    agent_id = args.agent
    machine = args.machine or os.uname().nodename

    print()
    print(color("=" * 60, "bold"))
    print(color("  BDR SESSION START", "bold"))
    print(color(f"  Agent: {agent_id}  |  Machine: {machine}", "cyan"))
    print(color(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}", "cyan"))
    print(color("=" * 60, "bold"))
    print()

    # ── Step 1: Git Pull ──────────────────────────────────────────────────────
    if not args.no_pull:
        print(color("▶ Pulling latest from origin/main...", "bold"))
        code, out, err = run_git(["pull", "origin", "main"])
        if code == 0:
            lines = [l for l in out.split("\n") if l.strip()]
            if "Already up to date" in out:
                print(color("  ✓ Already up to date.", "green"))
            else:
                print(color(f"  ✓ Pulled. {len(lines)} line(s) of output.", "green"))
                for line in lines[:5]:
                    print(f"    {line}")
        else:
            print(color(f"  ⚠ Pull failed: {err}", "yellow"))
            print("    Continuing with local state. Fix pull before committing.")
        print()

    # ── Step 2: Agent Registry ────────────────────────────────────────────────
    registry = load_json(AGENT_REGISTRY)
    agents = registry.get("agents", {})
    active_agents = []
    stale_agents = []

    for aid, info in agents.items():
        if aid == agent_id:
            continue
        last_seen = info.get("last_seen")
        status = info.get("status", "unknown")
        task = info.get("current_task")
        if last_seen and not is_stale(last_seen) and status == "active":
            active_agents.append((aid, info))
        elif last_seen and not is_stale(last_seen):
            stale_agents.append((aid, info))

    if active_agents:
        print(color("⚠ ACTIVE AGENTS DETECTED", "yellow"))
        for aid, info in active_agents:
            ago = hours_ago(info.get("last_seen", ""))
            task = info.get("current_task") or "unknown task"
            print(color(f"  → {aid} ({info.get('machine','?')}) — working on {task} ({ago:.1f}h ago)", "yellow"))
        print("  Check work-queue.json before claiming tasks to avoid conflicts.")
        print()
    else:
        print(color("✓ No other agents currently active.", "green"))
        print()

    # ── Step 3: Recent Events ─────────────────────────────────────────────────
    events = load_event_log(RECENT_EVENTS)
    if events:
        print(color(f"▶ Recent Activity (last {len(events)} events):", "bold"))
        for e in reversed(events):  # newest first
            ts = e.get("ts", "")[:10]
            agent = e.get("agent", "?")
            etype = e.get("event_type", "?")
            summary = e.get("summary", "")
            tid = e.get("task_id") or ""
            tid_str = f" [{tid}]" if tid else ""
            print(f"  {ts}  {color(agent,'cyan')}  {etype}{tid_str}")
            print(f"         {summary}")
        print()
    else:
        print(color("  No events logged yet.", "yellow"))
        print()

    # ── Step 4: Work Queue ────────────────────────────────────────────────────
    queue = load_json(WORK_QUEUE_JSON)
    active_tasks = queue.get("active", [])

    # Expire stale claims
    stale_claims_cleared = []
    for task in active_tasks:
        if task.get("status") == "in_progress" and task.get("claimed_at"):
            if is_stale(task["claimed_at"]):
                stale_claims_cleared.append(task["id"])
                task["status"] = "pending"
                task["claimed_by"] = None
                task["claimed_at"] = None

    if stale_claims_cleared:
        save_json(WORK_QUEUE_JSON, queue)
        print(color(f"⚠ Expired stale claims on: {', '.join(stale_claims_cleared)}", "yellow"))
        print()

    # Display tasks by priority
    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, None: 3}
    pending = sorted(
        [t for t in active_tasks if t.get("status") == "pending"],
        key=lambda t: (priority_order.get(t.get("priority"), 3), t.get("due") or "9999")
    )
    in_progress = [t for t in active_tasks if t.get("status") == "in_progress"]

    if in_progress:
        print(color("▶ Tasks In Progress:", "bold"))
        for task in in_progress:
            claimed_by = task.get("claimed_by", "?")
            ago = hours_ago(task.get("claimed_at", ""))
            print(color(f"  [IN PROGRESS] {task['id']}: {task['title']}", "yellow"))
            print(f"    Claimed by {claimed_by} ({ago:.1f}h ago)")
        print()

    if pending:
        print(color("▶ Available Tasks (by priority):", "bold"))
        for task in pending:
            priority = task.get("priority", "?")
            due = task.get("due") or "no deadline"
            tid = task["id"]
            title = task["title"]
            blockers = task.get("blockers", [])
            pcolor = "red" if priority == "HIGH" else "yellow" if priority == "MEDIUM" else "reset"
            print(f"  {color(f'[{priority}]', pcolor)} {color(tid, 'cyan')} — {title}")
            print(f"    Due: {due}")
            if blockers:
                for b in blockers:
                    print(color(f"    ⚠ BLOCKER: {b}", "yellow"))
        print()
    else:
        print(color("  ✓ No pending tasks.", "green"))
        print()

    # ── Step 5: Register This Agent ───────────────────────────────────────────
    if "agents" not in registry:
        registry["agents"] = {}
    registry["agents"][agent_id] = {
        "machine": machine,
        "last_seen": now_iso(),
        "status": "active",
        "current_task": args.claim,
        "session_count": registry.get("agents", {}).get(agent_id, {}).get("session_count", 0) + 1,
        "notes": registry.get("agents", {}).get(agent_id, {}).get("notes", "")
    }
    save_json(AGENT_REGISTRY, registry)

    # Log session start event
    append_event({
        "ts": now_iso(),
        "agent": agent_id,
        "machine": machine,
        "event_type": "session_start",
        "task_id": args.claim,
        "summary": f"Session started. Claiming: {args.claim or 'none yet'}.",
        "files_changed": []
    })

    # ── Step 6: Claim Task if specified ───────────────────────────────────────
    if args.claim:
        task_found = False
        for task in active_tasks:
            if task["id"] == args.claim:
                task_found = True
                if task["status"] == "in_progress":
                    print(color(f"⚠ {args.claim} is already claimed by {task.get('claimed_by')}. Aborting claim.", "red"))
                    print("  Use scripts/claim_task.py if you believe the claim is stale.")
                else:
                    task["status"] = "in_progress"
                    task["claimed_by"] = agent_id
                    task["claimed_at"] = now_iso()
                    save_json(WORK_QUEUE_JSON, queue)
                    print(color(f"✓ Claimed {args.claim}: {task['title']}", "green"))
                    print("  → Committing claim now...")
                    run_git(["add", str(WORK_QUEUE_JSON.relative_to(REPO_ROOT)), str(AGENT_REGISTRY.relative_to(REPO_ROOT))])
                    run_git(["commit", "-m", f"chore: claim {args.claim} by {agent_id}"])
                    code, out, err = run_git(["push", "origin", "main"])
                    if code == 0:
                        print(color("  ✓ Claim pushed to remote.", "green"))
                    else:
                        print(color(f"  ⚠ Push failed — run `git push origin main` from your terminal.", "yellow"))
                break
        if not task_found:
            print(color(f"⚠ Task {args.claim} not found in work-queue.json.", "red"))
        print()

    # ── Final Summary ─────────────────────────────────────────────────────────
    print(color("─" * 60, "bold"))
    print(color("  READY. Key files to read before starting:", "bold"))
    print(f"  • {color('memory/session/handoff.md', 'cyan')} — what the last agent left")
    print(f"  • {color('CLAUDE.md', 'cyan')} — all hard rules and pipeline state")
    print()
    print("  To claim a task:  python3 scripts/claim_task.py --agent " + agent_id + " --task TASK-XXX")
    print("  To close session: python3 scripts/session_end.py --agent " + agent_id + " --task TASK-XXX --summary '...'")
    print(color("─" * 60, "bold"))
    print()


if __name__ == "__main__":
    main()
