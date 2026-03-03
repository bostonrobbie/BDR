#!/usr/bin/env python3
"""
Recompute work/results.json from work/reply-log.csv data.

Reads the reply log CSV and generates aggregate analytics for the pre-brief.
Run after each /log-reply to keep results current.

Usage: python scripts/update_results.py
"""
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPLY_LOG = ROOT / "work" / "reply-log.csv"
RESULTS_FILE = ROOT / "work" / "results.json"
PIPELINE_STATE = ROOT / "work" / "pipeline-state.json"


def load_replies():
    if not REPLY_LOG.exists():
        return []
    with open(REPLY_LOG, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def compute_results(replies):
    total_replies = len(replies)

    # Load total prospects from pipeline state
    total_prospects = 0
    if PIPELINE_STATE.exists():
        state = json.loads(PIPELINE_STATE.read_text())
        total_prospects = state.get("total_sends_all_time", 0)

    reply_rate = (total_replies / total_prospects * 100) if total_prospects > 0 else 0.0

    # Count meetings
    meetings = sum(1 for r in replies if r.get("next_action", "").lower().startswith("book"))

    # Breakdowns
    by_persona = Counter(r.get("persona_type", "unknown") for r in replies)
    by_vertical = Counter(r.get("vertical", "unknown") for r in replies)
    by_proof_point = Counter(r.get("proof_point_used", "unknown") for r in replies)
    by_reply_tag = Counter(r.get("reply_tag", "unknown") for r in replies)
    by_pscore = Counter(r.get("personalization_score", "unknown") for r in replies)
    by_intent = Counter(r.get("reply_intent", "unknown") for r in replies)

    # Generate insights (only if enough data)
    insights = {}

    if total_replies >= 5:
        # Best persona
        if by_persona:
            best_persona = by_persona.most_common(1)[0]
            insights["best_persona"] = f"{best_persona[0]} ({best_persona[1]} replies)"
        # Best proof point
        if by_proof_point:
            best_pp = by_proof_point.most_common(1)[0]
            insights["best_proof_point"] = f"{best_pp[0]} ({best_pp[1]} replies)"
        # Best vertical
        if by_vertical:
            best_vert = by_vertical.most_common(1)[0]
            insights["best_vertical"] = f"{best_vert[0]} ({best_vert[1]} replies)"
        # Best pattern (reply tag)
        if by_reply_tag:
            best_tag = by_reply_tag.most_common(1)[0]
            insights["best_pattern"] = f"Most replies triggered by: {best_tag[0]} ({best_tag[1]})"
        # Stop doing (lowest performer with enough data)
        if len(by_persona) >= 2:
            worst = by_persona.most_common()[-1]
            insights["stop_doing"] = f"Lowest reply persona: {worst[0]} ({worst[1]} replies)"
    else:
        for key in ["best_persona", "best_proof_point", "best_vertical", "best_pattern", "stop_doing"]:
            insights[key] = f"Not enough data yet ({total_replies} replies, need 5+)"

    # Positive reply breakdown
    positive_count = sum(1 for r in replies if r.get("reply_intent") in ("positive", "curiosity"))

    return {
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "batches_analyzed": len(set(r.get("batch_number", "") for r in replies if r.get("batch_number"))),
        "total_prospects_contacted": total_prospects,
        "total_replies": total_replies,
        "overall_reply_rate": round(reply_rate, 1),
        "positive_replies": positive_count,
        "meetings_booked": meetings,
        "by_persona": dict(by_persona),
        "by_vertical": dict(by_vertical),
        "by_proof_point": dict(by_proof_point),
        "by_personalization_score": dict(by_pscore),
        "by_reply_tag": dict(by_reply_tag),
        "by_intent": dict(by_intent),
        "ab_test_results": [],
        "insights": insights,
    }


def main():
    replies = load_replies()
    results = compute_results(replies)
    RESULTS_FILE.write_text(json.dumps(results, indent=2) + "\n")
    print(f"Results updated: {results['total_replies']} replies, "
          f"{results['overall_reply_rate']}% reply rate, "
          f"{results['meetings_booked']} meetings")

    if results["total_replies"] > 0 and results["insights"]:
        print("\nInsights:")
        for k, v in results["insights"].items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
