"""
Decay-aware re-scoring cron job (F9).

Periodically re-scores contacts whose signals have decayed past a threshold,
automatically downgrading their tier if the new score warrants it.

Usage:
    python scripts/rescore_stale.py                  # Default: rescore contacts with >20% decay
    python scripts/rescore_stale.py --threshold 0.3  # Custom decay threshold
    python scripts/rescore_stale.py --dry-run        # Preview changes without writing

Cron example (daily at 6 AM):
    0 6 * * * cd /path/to/BDR && python scripts/rescore_stale.py >> logs/rescore.log 2>&1
"""

import sys
import os
import argparse
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.db import models
from src.agents.researcher import build_research_artifact
from src.agents.scorer import score_from_artifact, compute_decay_factor, load_scoring_config


def find_stale_contacts(threshold: float = 0.2) -> list:
    """Find contacts whose signals have decayed enough to warrant re-scoring.

    A contact is "stale" if any of their scored signals has a decay factor
    below (1.0 - threshold). For example, threshold=0.2 means any signal
    that's lost more than 20% of its value triggers a re-score.

    Args:
        threshold: Minimum decay percentage to trigger re-scoring (0.0 to 1.0).

    Returns:
        List of {"contact_id": str, "oldest_signal_age_days": int,
                 "worst_decay_factor": float} dicts.
    """
    config = load_scoring_config()
    decay_config = config.get("signal_decay", {})
    half_lives = decay_config.get("half_lives", {})
    min_factor = decay_config.get("min_factor", 0.1)

    if not half_lives:
        return []

    conn = models.get_db()
    contacts = conn.execute("""
        SELECT DISTINCT c.id as contact_id, c.first_name, c.last_name,
               c.priority_score, c.stage
        FROM contacts c
        WHERE c.status = 'active'
        AND c.stage NOT IN ('replied_positive', 'meeting_booked', 'replied_negative')
    """).fetchall()

    stale = []
    now = datetime.utcnow()

    for contact in contacts:
        contact_id = contact["contact_id"]

        # Check signal ages
        signals = conn.execute("""
            SELECT signal_type, detected_at FROM signals
            WHERE contact_id = ? AND detected_at IS NOT NULL
        """, (contact_id,)).fetchall()

        worst_factor = 1.0
        oldest_age = 0

        for signal in signals:
            sig_type = signal["signal_type"]
            detected = signal["detected_at"]
            hl = half_lives.get(sig_type)
            if not hl or not detected:
                continue

            try:
                sig_date = datetime.fromisoformat(detected)
                age_days = (now - sig_date).days
                factor = compute_decay_factor(age_days, hl, min_factor)

                if factor < worst_factor:
                    worst_factor = factor
                if age_days > oldest_age:
                    oldest_age = age_days
            except (ValueError, TypeError):
                continue

        if worst_factor < (1.0 - threshold):
            stale.append({
                "contact_id": contact_id,
                "name": f"{contact['first_name']} {contact['last_name']}",
                "current_priority": contact["priority_score"],
                "stage": contact["stage"],
                "oldest_signal_age_days": oldest_age,
                "worst_decay_factor": round(worst_factor, 3),
            })

    conn.close()
    return stale


def rescore_contact(contact_id: str) -> dict:
    """Re-score a single contact using current decay factors.

    Builds a fresh research artifact and scores it, which will
    automatically apply signal decay at scoring time.

    Returns:
        {"contact_id": str, "old_tier": str, "new_tier": str,
         "old_score": int, "new_score": int, "tier_changed": bool}
    """
    contact = models.get_contact(contact_id)
    if not contact:
        return {"contact_id": contact_id, "error": "Contact not found"}

    account = models.get_account(contact.get("account_id", "")) if contact.get("account_id") else {}
    old_priority = contact.get("priority_score", 0)

    try:
        result = build_research_artifact(contact, account or {})
        artifact = result.get("artifact", {})
        scoring = score_from_artifact(artifact)

        new_score = scoring.get("total_score", 0)
        new_tier = scoring.get("tier", "cold")

        # Map tier to priority score for backward compatibility
        tier_to_priority = {"hot": 5, "warm": 4, "cool": 3, "cold": 2}
        new_priority = tier_to_priority.get(new_tier, 3)
        old_tier = "hot" if old_priority >= 5 else "warm" if old_priority >= 4 else "cool" if old_priority >= 3 else "cold"

        return {
            "contact_id": contact_id,
            "name": f"{contact.get('first_name', '')} {contact.get('last_name', '')}",
            "old_score": old_priority,
            "new_score": new_score,
            "old_tier": old_tier,
            "new_tier": new_tier,
            "new_priority": new_priority,
            "tier_changed": old_tier != new_tier,
            "decay_applied": scoring.get("decay_applied", []),
        }
    except Exception as e:
        return {"contact_id": contact_id, "error": str(e)}


def run_rescore(threshold: float = 0.2, dry_run: bool = False) -> dict:
    """Run the full re-scoring job.

    Args:
        threshold: Decay threshold to trigger re-scoring.
        dry_run: If True, compute new scores but don't update the database.

    Returns:
        Summary of the re-scoring run.
    """
    started = datetime.utcnow().isoformat()
    print(f"[rescore] Starting at {started}")
    print(f"[rescore] Threshold: {threshold}, Dry run: {dry_run}")

    stale = find_stale_contacts(threshold)
    print(f"[rescore] Found {len(stale)} stale contacts")

    results = []
    tier_downgrades = 0
    tier_upgrades = 0
    errors = 0

    for s in stale:
        result = rescore_contact(s["contact_id"])
        results.append(result)

        if result.get("error"):
            errors += 1
            print(f"  ERROR: {s['name']} - {result['error']}")
            continue

        changed = result.get("tier_changed", False)
        old_tier = result.get("old_tier", "")
        new_tier = result.get("new_tier", "")
        tier_order = {"hot": 4, "warm": 3, "cool": 2, "cold": 1}

        if changed and tier_order.get(new_tier, 0) < tier_order.get(old_tier, 0):
            tier_downgrades += 1
            label = "DOWNGRADE"
        elif changed and tier_order.get(new_tier, 0) > tier_order.get(old_tier, 0):
            tier_upgrades += 1
            label = "UPGRADE"
        else:
            label = "no change"

        print(f"  {s['name']}: {old_tier} -> {new_tier} ({label})")

        if not dry_run and changed:
            models.update_contact(s["contact_id"], {
                "priority_score": result["new_priority"],
            })

    completed = datetime.utcnow().isoformat()
    summary = {
        "started": started,
        "completed": completed,
        "threshold": threshold,
        "dry_run": dry_run,
        "total_stale": len(stale),
        "rescored": len(results) - errors,
        "tier_downgrades": tier_downgrades,
        "tier_upgrades": tier_upgrades,
        "errors": errors,
    }

    print(f"\n[rescore] Complete: {len(stale)} checked, "
          f"{tier_downgrades} downgrades, {tier_upgrades} upgrades, {errors} errors")

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Re-score contacts with decayed signals")
    parser.add_argument("--threshold", type=float, default=0.2,
                        help="Decay threshold to trigger re-scoring (default: 0.2)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes without writing to database")
    args = parser.parse_args()

    run_rescore(threshold=args.threshold, dry_run=args.dry_run)
