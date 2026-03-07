#!/usr/bin/env python3
"""
Show current batch status and what's due.

Usage:
    python scripts/batch_status.py
"""

import os
import csv
import json
import glob
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK_DIR = os.path.join(PROJECT_ROOT, "work")
BATCHES_DIR = os.path.join(PROJECT_ROOT, "batches")
REPLY_LOG = os.path.join(WORK_DIR, "reply-log.csv")
RESULTS_FILE = os.path.join(WORK_DIR, "results.json")


def count_replies():
    """Count replies from log."""
    if not os.path.exists(REPLY_LOG):
        return 0, {}

    counts = {"positive": 0, "polite": 0, "negative": 0, "referral": 0, "meeting_booked": 0, "other": 0}
    total = 0

    with open(REPLY_LOG, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("prospect_name"):
                continue
            total += 1
            intent = row.get("reply_intent", "other")
            if intent in counts:
                counts[intent] += 1
            else:
                counts["other"] += 1

    return total, counts


def count_batches():
    """Count batch directories and files."""
    batch_dirs = sorted(glob.glob(os.path.join(BATCHES_DIR, "batch-*")))
    html_files = glob.glob(os.path.join(BATCHES_DIR, "**/*.html"), recursive=True)
    seq_files = glob.glob(os.path.join(BATCHES_DIR, "email-sequences/*.md"))
    return len(batch_dirs), len(html_files), len(seq_files)


def count_work_files():
    """Count files in work directory."""
    prospect_csvs = glob.glob(os.path.join(WORK_DIR, "batch-*-prospects.csv"))
    outreach_mds = glob.glob(os.path.join(WORK_DIR, "batch-*-outreach.md"))
    prebriefs = glob.glob(os.path.join(WORK_DIR, "pre-brief-*.md"))
    prep_cards = glob.glob(os.path.join(WORK_DIR, "meeting-prep", "*.md"))
    return len(prospect_csvs), len(outreach_mds), len(prebriefs), len(prep_cards)


def count_memory():
    """Count memory layer entries."""
    mem_root = os.path.join(PROJECT_ROOT, "memory")
    competitors = len(glob.glob(os.path.join(mem_root, "competitors", "*.md")))
    wins = len([f for f in glob.glob(os.path.join(mem_root, "wins", "*.md")) if "_template" not in f])
    losses = len([f for f in glob.glob(os.path.join(mem_root, "losses", "*.md")) if "_template" not in f])
    calls = len([f for f in glob.glob(os.path.join(mem_root, "call-notes", "*.md")) if "_template" not in f])
    return competitors, wins, losses, calls


def main():
    print("=" * 50)
    print(f"BDR STATUS - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    print()

    # Batches
    batch_dirs, html_count, seq_count = count_batches()
    print(f"Batches: {batch_dirs} total")
    print(f"  HTML deliverables: {html_count}")
    print(f"  Email sequences: {seq_count}")
    print()

    # Work directory
    prospects, outreach, prebriefs, prep_cards = count_work_files()
    print(f"Work directory:")
    print(f"  Prospect lists: {prospects}")
    print(f"  Outreach drafts: {outreach}")
    print(f"  Pre-briefs: {prebriefs}")
    print(f"  Meeting prep cards: {prep_cards}")
    print()

    # Replies
    total_replies, reply_counts = count_replies()
    print(f"Replies: {total_replies} total")
    if total_replies > 0:
        for intent, count in sorted(reply_counts.items(), key=lambda x: -x[1]):
            if count > 0:
                print(f"  {intent}: {count}")
    print()

    # Memory
    competitors, wins, losses, calls = count_memory()
    print(f"Memory layer:")
    print(f"  Battle cards: {competitors}")
    print(f"  Win reports: {wins}")
    print(f"  Loss reports: {losses}")
    print(f"  Call notes: {calls}")
    print()

    # Results summary
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            results = json.load(f)
        last = results.get("last_updated", "never")
        print(f"Results last updated: {last}")
    else:
        print("Results file: not created yet")

    print()
    print("Quick actions:")
    print("  python scripts/pre_brief.py          # Generate pre-brief")
    print("  python scripts/score_message.py       # Score a message")
    print("  python scripts/batch_status.py        # This report")


if __name__ == "__main__":
    main()
