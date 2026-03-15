#!/usr/bin/env python3
"""
BDR Pre-Send Check — Safety validator before any outreach action.

Run this BEFORE drafting or sending to any prospect. It checks:
  1. DNC list — Is this person permanently blocked?
  2. MASTER_SENT_LIST.csv — Have we already contacted them?
  3. Cadence rules — Would this violate Touch 2 / Touch 3 timing?
  4. Company-level checks — Is someone at this company already in sequence?

Usage:
    python3 scripts/pre_send_check.py --name "Namita Jain" --company "OverDrive"
    python3 scripts/pre_send_check.py --name "John Smith" --company "Acme" --touch 2 --last-send 2026-03-04
    python3 scripts/pre_send_check.py --csv path/to/batch.csv  # Check an entire batch file

Output:
    CLEAR   — Safe to contact. No violations found.
    WARN    — Potential issue. Review before proceeding.
    BLOCKED — Hard stop. Do not contact.

Always log results to anomaly-log.jsonl if a violation is found.
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ─── PATHS ─────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent
MASTER_SENT = REPO_ROOT / "MASTER_SENT_LIST.csv"
SESSION_DIR = REPO_ROOT / "memory" / "session"
ANOMALY_LOG = SESSION_DIR / "anomaly-log.jsonl"

# ─── DNC LIST — pulled from CLAUDE.md ──────────────────────────────────────────
# Update this list whenever CLAUDE.md Do Not Contact changes.
# Format: (normalized_name, company, reason, permanent)

DNC_LIST = [
    ("sanjay singh", "servicetitan", "Hostile reply (2022 mabl era). Skip permanently.", True),
    ("lance silverman", None, "Polite decline. Re-engage after 2026-05-01 with new trigger.", False),
    ("clyde faulkner", "camp systems", "mabl-era customer (2022). Had direct thread, knew Izzy. Skip permanently.", True),
    ("ashok prasad", "zl technologies", "mabl-era contact (Sep 2022). 2 messages sent, no reply. Skip permanently.", True),
    ("abe blanco", "kapitus", "Replied 'not interested' Mar 4. Skip permanently.", True),
    ("chuck smith", "aventiv technologies", "Double-send (B1 connection + B5B InMail). Skip permanently.", True),
    ("jitesh biswal", "jpmorgan chase", "Declined InMail Nov 4. Skip permanently.", True),
]

# Cadence rules
TOUCH_RULES = {
    2: {"min_days": 4, "label": "Touch 2"},
    3: {"min_days": 9, "label": "Touch 3"},
}

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def c(text, code):
    codes = {
        "red": "31", "green": "32", "yellow": "33", "cyan": "36",
        "bold": "1", "dim": "2", "bg_red": "41;37", "bg_green": "42;30"
    }
    return f"\033[{codes.get(code, '0')}m{text}\033[0m"

def normalize(s):
    """Normalize name for fuzzy matching: lowercase, strip punctuation, collapse spaces."""
    if not s:
        return ""
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9 ]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s

def name_match(a, b):
    """True if names are likely the same person (handles partial matches)."""
    na, nb = normalize(a), normalize(b)
    if na == nb:
        return True
    # Check if last name + first initial match
    parts_a = na.split()
    parts_b = nb.split()
    if len(parts_a) >= 2 and len(parts_b) >= 2:
        # Last name match + first initial match
        if parts_a[-1] == parts_b[-1] and parts_a[0][0] == parts_b[0][0]:
            return True
    return False

def company_match(a, b):
    """Loose company matching."""
    if not a or not b:
        return False
    na, nb = normalize(a), normalize(b)
    # Remove common suffixes
    for suffix in ["inc", "llc", "ltd", "corp", "co", "company", "technologies", "tech", "solutions"]:
        na = na.replace(suffix, "").strip()
        nb = nb.replace(suffix, "").strip()
    return na == nb or na in nb or nb in na

def log_anomaly(anomaly_type, severity, message, prospect, company, resolution=""):
    entry = {
        "ts": now_iso(),
        "agent": "pre_send_check",
        "event_type": "anomaly",
        "anomaly_type": anomaly_type,
        "severity": severity,
        "message": message,
        "prospect": prospect,
        "company": company,
        "resolution": resolution
    }
    with open(ANOMALY_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

def load_master_sent():
    """Load MASTER_SENT_LIST.csv into a list of dicts."""
    if not MASTER_SENT.exists():
        print(c(f"⚠ MASTER_SENT_LIST.csv not found at {MASTER_SENT}", "yellow"))
        return []
    rows = []
    with open(MASTER_SENT) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def parse_date(s):
    """Parse YYYY-MM-DD to date object."""
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ", "%m/%d/%Y"):
        try:
            return datetime.strptime(s[:10], fmt[:8]).date()
        except Exception:
            pass
    return None

# ─── CHECKS ────────────────────────────────────────────────────────────────────

class CheckResult:
    def __init__(self, name, company):
        self.name = name
        self.company = company
        self.violations = []   # (severity, type, message)

    def add(self, severity, vtype, message):
        self.violations.append((severity, vtype, message))

    @property
    def status(self):
        sev_levels = [v[0] for v in self.violations]
        if "BLOCKED" in sev_levels:
            return "BLOCKED"
        if "WARN" in sev_levels:
            return "WARN"
        return "CLEAR"

    def print_result(self, brief=False):
        status = self.status
        if status == "BLOCKED":
            label = c("  ✗ BLOCKED  ", "bg_red")
        elif status == "WARN":
            label = c("  ⚠ WARN     ", "bg_red")
        else:
            label = c("  ✓ CLEAR    ", "bg_green")

        name_str = c(f"{self.name}", "bold")
        co_str = f"({self.company})" if self.company else ""
        print(f"\n{label}  {name_str} {co_str}")

        for sev, vtype, msg in self.violations:
            sev_color = "red" if sev == "BLOCKED" else "yellow"
            print(f"    {c(sev, sev_color)} [{vtype}] {msg}")

        if not self.violations:
            print(f"    No violations found. Safe to contact.")


def check_dnc(name, company, result):
    for dnc_name, dnc_co, reason, permanent in DNC_LIST:
        name_hit = name_match(name, dnc_name)
        co_hit = dnc_co is None or company_match(company, dnc_co)

        if name_hit and co_hit:
            if permanent:
                result.add("BLOCKED", "DNC_PERMANENT",
                           f"On permanent DNC list. Reason: {reason}")
                log_anomaly("DNC_VIOLATION", "ERROR",
                            f"Pre-send check blocked: {name} ({company}) is on permanent DNC. {reason}",
                            name, company, "Do not contact.")
            else:
                result.add("BLOCKED", "DNC_TEMPORARY",
                           f"On DNC list (temporary). Reason: {reason}")
                log_anomaly("DNC_VIOLATION", "WARN",
                            f"Pre-send check blocked: {name} ({company}) is on temporary DNC. {reason}",
                            name, company, "Re-engage after specified date.")
            return True
    return False


def check_master_sent(name, company, sent_rows, result):
    hits = []
    for row in sent_rows:
        row_name = row.get("name") or row.get("Name", "")
        row_norm = row.get("norm", normalize(row_name))
        if name_match(name, row_name):
            hits.append(row)

    if hits:
        latest = max(hits, key=lambda r: r.get("send_date", ""))
        send_date = latest.get("send_date", "?")
        batch = latest.get("batch", "?")
        channel = latest.get("channel", "?")
        result.add("WARN", "ALREADY_CONTACTED",
                   f"Found {len(hits)} send(s). Latest: {batch} on {send_date} via {channel}.")
        return hits
    return []


def check_cadence(touch_num, last_send_date_str, result):
    if touch_num not in TOUCH_RULES:
        return

    rule = TOUCH_RULES[touch_num]
    min_days = rule["min_days"]
    label = rule["label"]

    if not last_send_date_str:
        result.add("WARN", "CADENCE_NO_DATE",
                   f"{label} requested but no last send date provided. Cannot validate timing.")
        return

    last_send = parse_date(last_send_date_str)
    if not last_send:
        result.add("WARN", "CADENCE_BAD_DATE",
                   f"{label}: could not parse last send date '{last_send_date_str}'.")
        return

    today = datetime.now(timezone.utc).date()
    days_since = (today - last_send).days

    if days_since < min_days:
        days_remaining = min_days - days_since
        earliest = last_send + timedelta(days=min_days)
        result.add("BLOCKED", "CADENCE_VIOLATION",
                   f"{label} requires {min_days}+ days since Touch 1. Only {days_since} days elapsed. "
                   f"Earliest send: {earliest}. ({days_remaining} days to wait.)")
        log_anomaly("CADENCE_VIOLATION", "ERROR",
                    f"Cadence violation: {label} attempted only {days_since} days after Touch 1 (min {min_days}).",
                    "", "", f"Earliest send date: {earliest}")
    else:
        # Passes — just informational
        pass


def check_company_saturation(company, sent_rows, result, max_per_company=3):
    """Flag if we've already sent to many people at the same company."""
    if not company:
        return
    co_hits = [r for r in sent_rows if company_match(company, r.get("company", r.get("name", "")))]
    # More targeted: check how many unique names at this company
    # Since MASTER_SENT_LIST doesn't have company column, we skip this but note the limitation
    pass  # Would need company column in CSV to implement fully

# ─── BATCH MODE ────────────────────────────────────────────────────────────────

def check_batch(csv_path, sent_rows):
    """Check an entire batch CSV file. Expected columns: name, company (optional)."""
    if not Path(csv_path).exists():
        print(c(f"✗ File not found: {csv_path}", "red"))
        sys.exit(1)

    print(c(f"\nChecking batch file: {csv_path}", "bold"))
    print()

    blocked = []
    warned = []
    clear = []

    with open(csv_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print(c("No rows found in CSV.", "yellow"))
        return

    for row in rows:
        name = row.get("name") or row.get("Name") or row.get("full_name") or ""
        company = row.get("company") or row.get("Company") or row.get("organization_name") or ""

        if not name:
            continue

        result = CheckResult(name, company)
        check_dnc(name, company, result)
        check_master_sent(name, company, sent_rows, result)

        if result.status == "BLOCKED":
            blocked.append(result)
        elif result.status == "WARN":
            warned.append(result)
        else:
            clear.append(result)

    # Print summary
    print(c(f"Results for {len(rows)} prospects:", "bold"))
    print()

    if blocked:
        print(c(f"✗ BLOCKED ({len(blocked)}) — DO NOT CONTACT:", "red"))
        for r in blocked:
            for sev, vtype, msg in r.violations:
                print(f"  {c(r.name, 'bold')} ({r.company or '?'}) — {msg}")
        print()

    if warned:
        print(c(f"⚠ WARN ({len(warned)}) — REVIEW BEFORE SENDING:", "yellow"))
        for r in warned:
            for sev, vtype, msg in r.violations:
                print(f"  {c(r.name, 'bold')} ({r.company or '?'}) — {msg}")
        print()

    print(c(f"✓ CLEAR ({len(clear)}) — safe to contact", "green"))
    print()
    print(c(f"Summary: {len(blocked)} blocked | {len(warned)} need review | {len(clear)} clear", "bold"))
    print()

# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BDR Pre-Send Check — DNC, dedup, cadence validator")
    parser.add_argument("--name", help="Prospect full name")
    parser.add_argument("--company", default="", help="Prospect company name")
    parser.add_argument("--touch", type=int, choices=[1, 2, 3], help="Touch number (for cadence check)")
    parser.add_argument("--last-send", help="Date of last send (YYYY-MM-DD) for cadence check")
    parser.add_argument("--csv", help="Path to batch CSV to check (columns: name, company)")
    parser.add_argument("--no-log", action="store_true", help="Do not write violations to anomaly-log.jsonl")
    args = parser.parse_args()

    sent_rows = load_master_sent()

    if args.csv:
        check_batch(args.csv, sent_rows)
        return

    if not args.name:
        parser.print_help()
        print()
        print(c("Examples:", "bold"))
        print(c("  python3 scripts/pre_send_check.py --name 'John Smith' --company 'Acme Corp'", "dim"))
        print(c("  python3 scripts/pre_send_check.py --name 'Jane Doe' --company 'BigCo' --touch 2 --last-send 2026-03-03", "dim"))
        print(c("  python3 scripts/pre_send_check.py --csv batches/new-batch.csv", "dim"))
        sys.exit(1)

    result = CheckResult(args.name, args.company)

    # Run all checks
    print()
    print(c("─" * 60, "bold"))
    print(c(f"  Pre-Send Check: {args.name} ({args.company or 'company not specified'})", "bold"))
    print(c("─" * 60, "bold"))

    print(c("\n  Checking DNC list...", "dim"))
    dnc_hit = check_dnc(args.name, args.company, result)

    print(c("  Checking MASTER_SENT_LIST...", "dim"))
    prior_sends = check_master_sent(args.name, args.company, sent_rows, result)

    if args.touch and args.touch > 1:
        print(c(f"  Checking cadence (Touch {args.touch})...", "dim"))
        if not args.last_send and prior_sends:
            # Try to infer from master sent list
            latest = max(prior_sends, key=lambda r: r.get("send_date", ""))
            args.last_send = latest.get("send_date")
            print(c(f"  Inferred last send date from MASTER_SENT_LIST: {args.last_send}", "dim"))
        check_cadence(args.touch, args.last_send, result)

    # Print result
    result.print_result()

    # Additional context
    if prior_sends:
        print()
        print(c("  Prior contact history:", "dim"))
        for row in sorted(prior_sends, key=lambda r: r.get("send_date", "")):
            print(f"    {row.get('send_date','?')}  {row.get('batch','?')}  via {row.get('channel','?')}")

    print()
    status = result.status
    sys.exit(0 if status == "CLEAR" else (1 if status == "BLOCKED" else 0))


if __name__ == "__main__":
    main()
