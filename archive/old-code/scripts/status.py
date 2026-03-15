#!/usr/bin/env python3
"""
BDR Status — Control tower dashboard for the multi-agent system.

Usage:
    python3 scripts/status.py              # Full status
    python3 scripts/status.py --brief      # One-line summary per section
    python3 scripts/status.py --events 20  # Show last N events (default: 8)
    python3 scripts/status.py --tasks      # Task list only
    python3 scripts/status.py --agents     # Agent registry only

Run this any time to see:
  - Which agents are active / idle / stale
  - Which tasks are claimed, pending, blocked
  - Last N events from the event log
  - Any stale claims or anomalies
  - Push state (are we ahead of remote?)
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
ANOMALY_LOG = SESSION_DIR / "anomaly-log.jsonl"

STALE_HOURS = 4

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def c(text, code):
    codes = {
        "red": "31", "green": "32", "yellow": "33", "blue": "34",
        "cyan": "36", "white": "37", "bold": "1", "dim": "2",
        "bg_red": "41", "bg_green": "42", "bg_yellow": "43"
    }
    return f"\033[{codes.get(code, '0')}m{text}\033[0m"

def load_json(path):
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)

def load_jsonl(path, limit=None):
    if not path.exists():
        return []
    lines = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    lines.append(json.loads(line))
                except Exception:
                    pass
    return lines[-limit:] if limit else lines

def hours_ago(ts):
    if not ts:
        return float("inf")
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        delta = datetime.now(timezone.utc) - dt
        return delta.total_seconds() / 3600
    except Exception:
        return float("inf")

def fmt_ago(ts):
    if not ts or ts == "never_seen":
        return c("never", "dim")
    h = hours_ago(ts)
    if h < 1/60:
        return c("just now", "green")
    elif h < 1:
        return c(f"{int(h*60)}m ago", "green")
    elif h < 4:
        return c(f"{h:.1f}h ago", "yellow")
    elif h < 24:
        return c(f"{h:.1f}h ago", "red")
    else:
        return c(f"{int(h/24)}d ago", "dim")

def run_git(args):
    result = subprocess.run(
        ["git"] + args,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def priority_sort_key(task):
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    return (order.get(task.get("priority", "LOW"), 3), task.get("due") or "9999")

# ─── SECTIONS ──────────────────────────────────────────────────────────────────

def print_header():
    _, branch, _ = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    _, commits_ahead, _ = run_git(["rev-list", "--count", "HEAD@{u}..HEAD"])
    ahead_str = ""
    if commits_ahead and commits_ahead != "0":
        ahead_str = c(f"  ↑ {commits_ahead} unpushed commit(s) — run: git push origin main", "yellow")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print()
    print(c("╔══════════════════════════════════════════════════════════╗", "bold"))
    print(c("║           BDR AGENT CONTROL TOWER                       ║", "bold"))
    print(c("╚══════════════════════════════════════════════════════════╝", "bold"))
    print(f"  {c(now, 'dim')}  branch: {c(branch, 'cyan')}{ahead_str}")
    print()


def print_agents(registry, brief=False):
    agents = registry.get("agents", {})
    stale_threshold = registry.get("_meta", {}).get("stale_threshold_hours", STALE_HOURS)

    print(c("── AGENTS ──────────────────────────────────────────────────", "bold"))

    if not agents:
        print(c("  No agents registered.", "dim"))
        print()
        return []

    stale_agents = []
    for agent_id, info in agents.items():
        last_seen = info.get("last_seen", "never_seen")
        status = info.get("status", "unknown")
        current_task = info.get("current_task") or "—"
        machine = info.get("machine", "?")
        h = hours_ago(last_seen)

        is_stale = h > stale_threshold
        if is_stale and status == "active":
            status = "STALE"
            stale_agents.append(agent_id)

        if status == "active":
            status_str = c("● ACTIVE", "green")
        elif status == "idle":
            status_str = c("○ idle  ", "dim")
        elif status == "STALE":
            status_str = c("⚠ STALE ", "yellow")
        else:
            status_str = c(f"? {status}", "dim")

        if brief:
            print(f"  {status_str}  {c(agent_id, 'bold')} ({machine}) — task: {current_task} — {fmt_ago(last_seen)}")
        else:
            print(f"  {status_str}  {c(agent_id, 'bold')}")
            print(f"          machine: {machine}  |  last seen: {fmt_ago(last_seen)}")
            print(f"          task: {c(current_task, 'cyan')}  |  sessions: {info.get('session_count', 0)}")
            if info.get("notes"):
                print(f"          notes: {c(info['notes'], 'dim')}")

    if stale_agents:
        print()
        print(c(f"  ⚠ Stale agents (>{stale_threshold}h): {', '.join(stale_agents)}", "yellow"))
        print(c("    session_start.py will auto-expire their claims.", "dim"))

    print()
    return stale_agents


def print_tasks(queue, brief=False):
    active = queue.get("active", [])
    completed = queue.get("completed", [])

    print(c("── TASKS ───────────────────────────────────────────────────", "bold"))

    if not active:
        print(c("  No active tasks.", "dim"))
        print()
        return

    # Sort: in_progress first, then by priority, then pending, then blocked
    in_prog = [t for t in active if t.get("status") == "in_progress"]
    pending = sorted([t for t in active if t.get("status") == "pending"], key=priority_sort_key)
    blocked = [t for t in active if t.get("status") == "blocked"]

    # In progress
    if in_prog:
        for t in in_prog:
            claimer = t.get("claimed_by", "?")
            claimed_at = t.get("claimed_at")
            h = hours_ago(claimed_at)
            stale_warn = c(" ⚠ STALE CLAIM", "yellow") if h > STALE_HOURS else ""

            print(f"  {c('▶ IN PROGRESS', 'green')}  {c(t['id'], 'bold')} — {t['title']}")
            if not brief:
                print(f"     claimed by: {c(claimer, 'cyan')} — {fmt_ago(claimed_at)}{stale_warn}")
                if t.get("due"):
                    print(f"     due: {t['due']}")

    # Pending
    if pending:
        if in_prog:
            print()
        print(c("  PENDING:", "bold"))
        for t in pending:
            pri = t.get("priority", "MEDIUM")
            pri_color = {"CRITICAL": "red", "HIGH": "yellow", "MEDIUM": "cyan", "LOW": "dim"}.get(pri, "dim")
            due = f"  due {t['due']}" if t.get("due") else ""
            print(f"  {c('○', 'dim')} {c(t['id'], 'bold')}  [{c(pri, pri_color)}]{due}  {t['title']}")
            if not brief and t.get("description"):
                desc = t["description"][:90]
                print(f"     {c(desc + ('...' if len(t['description']) > 90 else ''), 'dim')}")

    # Blocked
    if blocked:
        print()
        print(c("  BLOCKED:", "bold"))
        for t in blocked:
            print(f"  {c('✗', 'red')} {c(t['id'], 'bold')}  {t['title']}")
            if not brief:
                for b in t.get("blockers", []):
                    print(f"     {c('BLOCKER:', 'red')} {b}")

    print()
    print(c(f"  {len(in_prog)} in progress  |  {len(pending)} pending  |  {len(blocked)} blocked  |  {len(completed)} completed", "dim"))
    print()


def print_events(events, n=8, brief=False):
    print(c("── RECENT EVENTS ───────────────────────────────────────────", "bold"))

    if not events:
        print(c("  No events logged yet.", "dim"))
        print()
        return

    recent = events[-n:]

    event_icons = {
        "session_start": "▶",
        "session_end": "■",
        "task_claimed": "⚑",
        "task_completed": "✓",
        "task_partial": "↻",
        "task_blocked": "✗",
        "send_approved": "📤",
        "anomaly": "⚠",
        "error": "✗",
        "note": "·",
    }

    for ev in reversed(recent):
        ts = ev.get("ts", "?")
        agent = ev.get("agent", "?")
        event_type = ev.get("event_type", "note")
        summary = ev.get("summary", "")
        task_id = ev.get("task_id", "")

        icon = event_icons.get(event_type, "·")

        # Format timestamp
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            ts_fmt = dt.strftime("%m-%d %H:%M")
        except Exception:
            ts_fmt = ts[:16]

        task_str = f" [{c(task_id, 'cyan')}]" if task_id else ""

        if event_type == "anomaly":
            icon_str = c(icon, "red")
            summary_str = c(summary, "red")
        elif event_type in ("task_completed", "send_approved"):
            icon_str = c(icon, "green")
            summary_str = summary
        elif event_type == "task_claimed":
            icon_str = c(icon, "yellow")
            summary_str = summary
        else:
            icon_str = c(icon, "dim")
            summary_str = summary

        print(f"  {c(ts_fmt, 'dim')}  {icon_str} {c(agent, 'bold')}{task_str}  {summary_str}")

        if not brief and ev.get("files_changed"):
            files = ev["files_changed"]
            if files:
                print(f"           {c('files: ' + ', '.join(files[:3]) + ('...' if len(files) > 3 else ''), 'dim')}")

    print()


def print_anomalies(anomalies):
    if not anomalies:
        return

    recent = [a for a in anomalies if hours_ago(a.get("ts")) < 48]
    if not recent:
        return

    print(c("── ⚠ RECENT ANOMALIES (last 48h) ───────────────────────────", "red"))
    for a in recent[-5:]:
        ts = a.get("ts", "?")[:16]
        severity = a.get("severity", "WARN")
        atype = a.get("anomaly_type", "?")
        msg = a.get("message", "")
        sev_color = "red" if severity == "ERROR" else "yellow"
        print(f"  {c(severity, sev_color)}  {c(atype, 'bold')}  {msg}  {c(ts, 'dim')}")
    print()


def print_git_state():
    code, ahead, _ = run_git(["rev-list", "--count", "HEAD@{u}..HEAD"])
    if code == 0 and ahead and ahead != "0":
        print(c(f"  ⚠ {ahead} unpushed commit(s). Run: git push origin main", "yellow"))
        print()


def print_footer():
    print(c("── QUICK COMMANDS ──────────────────────────────────────────", "dim"))
    print(c("  Claim task:     python3 scripts/claim_task.py --agent <ID> --task <TASK-XXX>", "dim"))
    print(c("  Add task:       python3 scripts/new_task.py --id TASK-XXX --title '...' --priority HIGH", "dim"))
    print(c("  Health check:   python3 scripts/health_check.py", "dim"))
    print(c("  Pre-send check: python3 scripts/pre_send_check.py --name 'First Last' --company 'Co'", "dim"))
    print(c("  Close session:  python3 scripts/session_end.py --agent <ID> --task <TASK-XXX> --status done --summary '...'", "dim"))
    print()

# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BDR Control Tower — system status dashboard")
    parser.add_argument("--brief", action="store_true", help="Compact one-line-per-item output")
    parser.add_argument("--events", type=int, default=8, help="Number of recent events to show (default: 8)")
    parser.add_argument("--tasks", action="store_true", help="Show task list only")
    parser.add_argument("--agents", action="store_true", help="Show agent registry only")
    args = parser.parse_args()

    queue = load_json(WORK_QUEUE_JSON)
    registry = load_json(AGENT_REGISTRY)
    events = load_jsonl(EVENT_LOG)
    anomalies = load_jsonl(ANOMALY_LOG)

    if args.tasks:
        print_tasks(queue, brief=args.brief)
        return

    if args.agents:
        print_agents(registry, brief=args.brief)
        return

    print_header()
    print_agents(registry, brief=args.brief)
    print_tasks(queue, brief=args.brief)
    print_events(events, n=args.events, brief=args.brief)
    if anomalies:
        print_anomalies(anomalies)
    print_footer()


if __name__ == "__main__":
    main()
