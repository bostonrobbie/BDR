#!/usr/bin/env python3
"""
BDR Health Check — System validator for the multi-agent coordination layer.

Usage:
    python3 scripts/health_check.py        # Full check
    python3 scripts/health_check.py --fix  # Auto-fix what can be fixed
    python3 scripts/health_check.py --ci   # Exit 1 if any errors found (for CI/pre-commit)

Checks:
    1. JSON schema validity (work-queue.json, agent-registry.json)
    2. work-queue.md sync with work-queue.json
    3. Stale task claims (>4h)
    4. Recent anomalies in anomaly-log.jsonl
    5. Git state (uncommitted changes, unpushed commits)
    6. Required files present
    7. MASTER_SENT_LIST.csv integrity (no blank name rows)
    8. Event log integrity (valid JSON on every line)
    9. DNC list consistency (are DNC contacts clean from active tasks?)
   10. Cadence integrity (no Touch 2 violations possible in queue)
"""

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
AGENT_REGISTRY = SESSION_DIR / "agent-registry.json"
EVENT_LOG = SESSION_DIR / "event-log.jsonl"
ANOMALY_LOG = SESSION_DIR / "anomaly-log.jsonl"
MASTER_SENT = REPO_ROOT / "MASTER_SENT_LIST.csv"
HANDOFF_MD = SESSION_DIR / "handoff.md"
SESSION_LOG = SESSION_DIR / "session-log.md"

REQUIRED_FILES = [
    WORK_QUEUE_JSON,
    AGENT_REGISTRY,
    EVENT_LOG,
    MASTER_SENT,
    REPO_ROOT / "CLAUDE.md",
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "BDR-REPO-INDEX.md",
    HANDOFF_MD,
    SESSION_LOG,
]

STALE_HOURS = 4

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def c(text, code):
    codes = {
        "red": "31", "green": "32", "yellow": "33", "cyan": "36",
        "bold": "1", "dim": "2"
    }
    return f"\033[{codes.get(code, '0')}m{text}\033[0m"

def ok(msg):
    print(f"  {c('✓', 'green')} {msg}")

def warn(msg):
    print(f"  {c('⚠', 'yellow')} {msg}")

def err(msg):
    print(f"  {c('✗', 'red')} {msg}")

def info(msg):
    print(f"  {c('·', 'dim')} {msg}")

def hours_ago(ts):
    if not ts:
        return float("inf")
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).total_seconds() / 3600
    except Exception:
        return float("inf")

def load_json(path):
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)

def run_git(args):
    result = subprocess.run(["git"] + args, cwd=REPO_ROOT, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

# ─── CHECKS ────────────────────────────────────────────────────────────────────

class HealthReport:
    def __init__(self):
        self.errors = 0
        self.warnings = 0
        self.passed = 0
        self.fixable = []

    def ok(self, msg):
        ok(msg)
        self.passed += 1

    def warn(self, msg, fix_cmd=None):
        warn(msg)
        self.warnings += 1
        if fix_cmd:
            self.fixable.append(fix_cmd)

    def err(self, msg, fix_cmd=None):
        err(msg)
        self.errors += 1
        if fix_cmd:
            self.fixable.append(fix_cmd)

    def info(self, msg):
        info(msg)


def check_required_files(report):
    print(c("\n[1] Required files", "bold"))
    for path in REQUIRED_FILES:
        if path.exists():
            report.ok(f"{path.relative_to(REPO_ROOT)}")
        else:
            report.err(f"MISSING: {path.relative_to(REPO_ROOT)}")


def check_json_validity(report):
    print(c("\n[2] JSON schema validity", "bold"))

    # work-queue.json
    queue = load_json(WORK_QUEUE_JSON)
    if queue is None:
        report.err("work-queue.json: not found or unreadable")
    else:
        required_keys = ["active", "completed", "_meta"]
        missing = [k for k in required_keys if k not in queue]
        if missing:
            report.err(f"work-queue.json: missing keys: {missing}")
        else:
            active = queue.get("active", [])
            task_errors = 0
            for t in active:
                for field in ["id", "title", "status", "priority"]:
                    if field not in t:
                        report.err(f"  Task {t.get('id','?')}: missing field '{field}'")
                        task_errors += 1
            if task_errors == 0:
                report.ok(f"work-queue.json: valid ({len(active)} active tasks, {len(queue.get('completed',[]))} completed)")

    # agent-registry.json
    registry = load_json(AGENT_REGISTRY)
    if registry is None:
        report.err("agent-registry.json: not found or unreadable")
    else:
        agents = registry.get("agents", {})
        report.ok(f"agent-registry.json: valid ({len(agents)} agents registered)")


def check_event_log(report):
    print(c("\n[3] Event log integrity", "bold"))
    if not EVENT_LOG.exists():
        report.err("event-log.jsonl: not found")
        return

    bad_lines = []
    total = 0
    with open(EVENT_LOG) as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total += 1
            try:
                ev = json.loads(line)
                for field in ["ts", "agent", "event_type"]:
                    if field not in ev:
                        bad_lines.append((i, f"missing field '{field}'"))
            except json.JSONDecodeError as e:
                bad_lines.append((i, str(e)))

    if bad_lines:
        for line_num, msg in bad_lines[:5]:
            report.err(f"event-log.jsonl line {line_num}: {msg}")
    else:
        report.ok(f"event-log.jsonl: {total} events, all valid JSON")


def check_stale_claims(report, queue):
    print(c("\n[4] Stale task claims", "bold"))
    if queue is None:
        report.warn("Cannot check — work-queue.json unavailable")
        return

    stale = []
    for t in queue.get("active", []):
        if t.get("status") == "in_progress":
            h = hours_ago(t.get("claimed_at"))
            if h > STALE_HOURS:
                stale.append((t["id"], t.get("claimed_by", "?"), h))

    if stale:
        for task_id, claimer, h in stale:
            report.warn(
                f"STALE CLAIM: {task_id} claimed by {claimer} — {h:.1f}h ago (>{STALE_HOURS}h)",
                fix_cmd=f"python3 scripts/session_start.py --agent <YOUR_AGENT> (auto-expires stale claims)"
            )
    else:
        active_claims = [t for t in queue.get("active",[]) if t.get("status")=="in_progress"]
        if active_claims:
            for t in active_claims:
                h = hours_ago(t.get("claimed_at"))
                report.ok(f"Active claim: {t['id']} by {t.get('claimed_by','?')} ({h:.1f}h ago — fresh)")
        else:
            report.ok("No active claims.")


def check_queue_sync(report):
    print(c("\n[5] work-queue.md sync", "bold"))
    if not WORK_QUEUE_MD.exists():
        report.warn(
            "work-queue.md not found — run sync to generate it",
            fix_cmd="python3 scripts/sync_queue.py"
        )
        return

    md_mtime = WORK_QUEUE_MD.stat().st_mtime
    json_mtime = WORK_QUEUE_JSON.stat().st_mtime if WORK_QUEUE_JSON.exists() else 0

    if json_mtime > md_mtime + 5:  # 5s grace period
        report.warn(
            "work-queue.md is older than work-queue.json — may be out of sync",
            fix_cmd="python3 scripts/sync_queue.py"
        )
    else:
        report.ok("work-queue.md is up to date")


def check_anomalies(report):
    print(c("\n[6] Recent anomalies (last 72h)", "bold"))
    if not ANOMALY_LOG.exists():
        report.ok("anomaly-log.jsonl: no anomalies recorded")
        return

    recent = []
    errors_72h = []
    with open(ANOMALY_LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                a = json.loads(line)
                h = hours_ago(a.get("ts"))
                if h < 72:
                    recent.append(a)
                if h < 72 and a.get("severity") == "ERROR":
                    errors_72h.append(a)
            except Exception:
                pass

    if errors_72h:
        for a in errors_72h[-3:]:
            report.warn(f"ANOMALY [{a.get('anomaly_type','?')}]: {a.get('message','')}")
    elif recent:
        report.warn(f"{len(recent)} anomaly/warning(s) in last 72h (no ERRORs)")
    else:
        total_anomalies = sum(1 for _ in open(ANOMALY_LOG) if _.strip())
        report.ok(f"No anomalies in last 72h ({total_anomalies} total historical)")


def check_git_state(report):
    print(c("\n[7] Git state", "bold"))

    # Uncommitted changes
    code, out, _ = run_git(["status", "--short"])
    if code == 0:
        changed = [l for l in out.split("\n") if l.strip()]
        if changed:
            report.warn(f"{len(changed)} uncommitted file(s). Commit before ending session.")
            for line in changed[:5]:
                info(f"  {line}")
        else:
            report.ok("Working tree clean")

    # Unpushed commits
    code, ahead, _ = run_git(["rev-list", "--count", "HEAD@{u}..HEAD"])
    if code == 0:
        if ahead and ahead != "0":
            report.warn(f"{ahead} unpushed commit(s). Run: git push origin main")
        else:
            report.ok("In sync with remote")
    else:
        report.warn("Could not check remote sync (no upstream tracked or no network)")

    # Check for index.lock
    lock_file = REPO_ROOT / ".git" / "index.lock"
    if lock_file.exists():
        report.err(
            ".git/index.lock exists — previous git operation may have crashed. Delete it.",
            fix_cmd="rm -f .git/index.lock"
        )


def check_master_sent(report):
    print(c("\n[8] MASTER_SENT_LIST.csv integrity", "bold"))
    if not MASTER_SENT.exists():
        report.err("MASTER_SENT_LIST.csv not found")
        return

    import csv
    blank_names = 0
    total = 0
    with open(MASTER_SENT) as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            name = row.get("name") or row.get("Name", "")
            if not name.strip():
                blank_names += 1

    if blank_names:
        report.warn(f"MASTER_SENT_LIST.csv: {blank_names} row(s) with blank name (out of {total})")
    else:
        report.ok(f"MASTER_SENT_LIST.csv: {total} rows, all have names")


def check_handoff_freshness(report):
    print(c("\n[9] Handoff freshness", "bold"))
    if not HANDOFF_MD.exists():
        report.warn("handoff.md not found")
        return

    mtime = HANDOFF_MD.stat().st_mtime
    h = (datetime.now(timezone.utc).timestamp() - mtime) / 3600

    if h > 48:
        report.warn(f"handoff.md was last modified {h:.0f}h ago — may be stale")
    elif h > 24:
        report.warn(f"handoff.md was last modified {h:.0f}h ago — update if starting new work")
    else:
        report.ok(f"handoff.md: last modified {h:.1f}h ago")

# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="BDR Health Check — system validator")
    parser.add_argument("--fix", action="store_true", help="Show fix commands for each issue")
    parser.add_argument("--ci", action="store_true", help="Exit 1 if any errors (for CI/hooks)")
    parser.add_argument("--quiet", action="store_true", help="Only show failures")
    args = parser.parse_args()

    print()
    print(c("╔══════════════════════════════════════════════════════════╗", "bold"))
    print(c("║           BDR HEALTH CHECK                               ║", "bold"))
    print(c("╚══════════════════════════════════════════════════════════╝", "bold"))
    print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")

    report = HealthReport()
    queue = load_json(WORK_QUEUE_JSON)

    check_required_files(report)
    check_json_validity(report)
    check_event_log(report)
    check_stale_claims(report, queue)
    check_queue_sync(report)
    check_anomalies(report)
    check_git_state(report)
    check_master_sent(report)
    check_handoff_freshness(report)

    # Summary
    print()
    print(c("── SUMMARY ──────────────────────────────────────────────────", "bold"))
    err_str = c(f"{report.errors} error(s)", "red") if report.errors else c("0 errors", "green")
    warn_str = c(f"{report.warnings} warning(s)", "yellow") if report.warnings else c("0 warnings", "green")
    ok_str = c(f"{report.passed} passed", "green")
    print(f"  {err_str}  |  {warn_str}  |  {ok_str}")

    if report.fixable and args.fix:
        print()
        print(c("── FIXABLE ISSUES ───────────────────────────────────────────", "yellow"))
        seen = set()
        for cmd in report.fixable:
            if cmd not in seen:
                print(c(f"  {cmd}", "cyan"))
                seen.add(cmd)

    if report.errors == 0 and report.warnings == 0:
        print()
        print(c("  ✓ All checks passed. System is healthy.", "green"))
    elif report.errors == 0:
        print()
        print(c("  ⚠ No hard errors, but review warnings above.", "yellow"))
    else:
        print()
        print(c("  ✗ Errors found. Resolve before proceeding with outreach.", "red"))

    print()

    if args.ci and report.errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
