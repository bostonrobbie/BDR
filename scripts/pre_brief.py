#!/usr/bin/env python3
"""
Generate a pre-brief by reading reply-log.csv and results.json.

Usage:
    python scripts/pre_brief.py                    # Generate pre-brief
    python scripts/pre_brief.py --update-results   # Update results.json from reply-log
"""

import sys
import os
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK_DIR = os.path.join(PROJECT_ROOT, "work")
REPLY_LOG = os.path.join(WORK_DIR, "reply-log.csv")
RESULTS_FILE = os.path.join(WORK_DIR, "results.json")


def read_reply_log():
    """Read reply-log.csv and return list of dicts."""
    if not os.path.exists(REPLY_LOG):
        return []

    rows = []
    with open(REPLY_LOG, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("prospect_name"):  # skip empty rows
                rows.append(row)
    return rows


def update_results(replies):
    """Update results.json from reply data."""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            results = json.load(f)
    else:
        results = {}

    results["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    results["total_replies"] = len(replies)

    # Count by persona
    by_persona = defaultdict(lambda: {"contacted": 0, "replied": 0, "meetings": 0})
    by_vertical = defaultdict(lambda: {"contacted": 0, "replied": 0, "meetings": 0})
    by_proof = defaultdict(lambda: {"used": 0, "replied": 0})
    by_pscore = defaultdict(lambda: {"contacted": 0, "replied": 0})
    by_tag = Counter()

    for r in replies:
        persona = r.get("persona_type", "unknown")
        vertical = r.get("vertical", "unknown")
        proof = r.get("proof_point_used", "unknown")
        pscore = r.get("personalization_score", "0")
        tag = r.get("reply_tag", "unknown")
        intent = r.get("reply_intent", "")

        by_persona[persona]["replied"] += 1
        if intent == "meeting_booked":
            by_persona[persona]["meetings"] += 1

        by_vertical[vertical]["replied"] += 1
        if intent == "meeting_booked":
            by_vertical[vertical]["meetings"] += 1

        by_proof[proof]["replied"] += 1
        by_pscore[pscore]["replied"] += 1
        by_tag[tag] += 1

    results["by_persona"] = {k: dict(v) for k, v in by_persona.items()}
    results["by_vertical"] = {k: dict(v) for k, v in by_vertical.items()}
    results["by_proof_point"] = {k: dict(v) for k, v in by_proof.items()}
    results["by_personalization_score"] = {k: dict(v) for k, v in by_pscore.items()}
    results["by_reply_tag"] = dict(by_tag)

    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    return results


def generate_pre_brief(results, replies):
    """Generate the 5-line pre-brief."""
    lines = []
    lines.append("=" * 50)
    lines.append("PRE-BRIEF: What's Working")
    lines.append("=" * 50)
    lines.append("")

    if not replies:
        lines.append("No reply data yet. Start logging replies in work/reply-log.csv")
        lines.append("to build the learning loop.")
        lines.append("")
        lines.append("Default assumptions from SOP:")
        lines.append("  1. Best persona: QA Directors (highest historical reply rate)")
        lines.append("  2. Best proof point: Match to vertical (no data yet on what's working)")
        lines.append("  3. Best vertical: FinTech and Healthcare (SOP defaults)")
        lines.append("  4. Best pattern: Question-led openers (+2.6 pp from LinkedIn analysis)")
        lines.append("  5. Stop doing: VP Eng at 50K+ companies (lowest expected reply rate)")
        return "\n".join(lines)

    # 1. Best persona
    persona_replies = results.get("by_persona", {})
    if persona_replies:
        best_persona = max(persona_replies.items(), key=lambda x: x[1].get("replied", 0))
        lines.append(f"1. Best persona: {best_persona[0]} ({best_persona[1].get('replied', 0)} replies)")
    else:
        lines.append("1. Best persona: Not enough data")

    # 2. Best proof point
    proof_replies = results.get("by_proof_point", {})
    if proof_replies:
        best_proof = max(proof_replies.items(), key=lambda x: x[1].get("replied", 0))
        lines.append(f"2. Best proof point: {best_proof[0]} ({best_proof[1].get('replied', 0)} replies)")
    else:
        lines.append("2. Best proof point: Not enough data")

    # 3. Best vertical
    vert_replies = results.get("by_vertical", {})
    if vert_replies:
        best_vert = max(vert_replies.items(), key=lambda x: x[1].get("replied", 0))
        lines.append(f"3. Best vertical: {best_vert[0]} ({best_vert[1].get('replied', 0)} replies)")
    else:
        lines.append("3. Best vertical: Not enough data")

    # 4. Best pattern
    tag_replies = results.get("by_reply_tag", {})
    if tag_replies:
        best_tag = max(tag_replies.items(), key=lambda x: x[1])
        lines.append(f"4. Best trigger: {best_tag[0]} ({best_tag[1]} replies tagged this way)")
    else:
        lines.append("4. Best pattern: Not enough data")

    # 5. Stop doing
    if persona_replies:
        worst = min(persona_replies.items(), key=lambda x: x[1].get("replied", 0))
        if worst[1].get("replied", 0) == 0:
            lines.append(f"5. Stop doing: {worst[0]} (0 replies)")
        else:
            lines.append("5. Stop doing: No clear signal yet (need more data)")
    else:
        lines.append("5. Stop doing: Not enough data")

    lines.append("")
    lines.append(f"Based on {len(replies)} total replies logged.")

    return "\n".join(lines)


def main():
    replies = read_reply_log()

    if len(sys.argv) > 1 and sys.argv[1] == "--update-results":
        results = update_results(replies)
        print(f"Updated results.json with {len(replies)} replies.")
        return

    # Always update results first
    results = update_results(replies)

    # Generate pre-brief
    brief = generate_pre_brief(results, replies)
    print(brief)

    # Save to file
    batch_num = results.get("batches_analyzed", 0) + 1
    brief_path = os.path.join(WORK_DIR, f"pre-brief-batch-{batch_num}.md")
    with open(brief_path, "w") as f:
        f.write(brief)
    print(f"\nSaved to {brief_path}")


if __name__ == "__main__":
    main()
