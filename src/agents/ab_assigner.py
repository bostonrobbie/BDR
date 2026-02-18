"""
Outreach Command Center - A/B Assigner
Stratified split of prospects into A/B groups for testing one variable per batch.
"""

import json
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.db import models


# ─── A/B TEST VARIABLES ──────────────────────────────────────

AB_VARIABLES = {
    "pain_hook": {
        "A": "Flaky/brittle tests (maintenance angle)",
        "B": "Release velocity/speed angle"
    },
    "proof_point_style": {
        "A": "Named customer (Sanofi, CRED, Hansard)",
        "B": "Anonymous ('a Fortune 100 company')"
    },
    "opener_style": {
        "A": "Career-reference openers",
        "B": "Company-metric openers"
    },
    "ask_intensity": {
        "A": "Direct: 'Would 15 minutes make sense?'",
        "B": "Soft: 'Happy to share more if helpful'"
    },
    "message_length": {
        "A": "Tight (70-80 words)",
        "B": "Fuller (100-120 words)"
    },
}


def assign_ab_groups(
    contact_ids: list,
    variable: str,
    group_descriptions: dict = None,
    batch_id: str = None
) -> dict:
    """Assign contacts to A/B groups with stratified sampling.

    Stratifies by persona_type and vertical to ensure balanced groups.
    Each group gets roughly equal representation of QA vs VP Eng
    and equal vertical distribution.

    Returns dict mapping contact_id -> group ('A' or 'B').
    """
    if not group_descriptions:
        group_descriptions = AB_VARIABLES.get(variable, {"A": "Control", "B": "Variant"})

    # Load contacts for stratification
    contacts = []
    for cid in contact_ids:
        c = models.get_contact(cid)
        if c:
            contacts.append(c)

    # Sort by persona_type then vertical for even distribution
    contacts.sort(key=lambda c: (c.get("persona_type", ""), c.get("company_industry", "")))

    # Alternate assignment: A, B, A, B... within each stratum
    assignments = {}
    group_toggle = True  # True = A, False = B

    for c in contacts:
        group = "A" if group_toggle else "B"
        assignments[c["id"]] = group
        group_toggle = not group_toggle

    # Store assignments in batch_prospects
    if batch_id:
        conn = models.get_db()
        for contact_id, group in assignments.items():
            conn.execute(
                "UPDATE batch_prospects SET ab_group=? WHERE batch_id=? AND contact_id=?",
                (group, batch_id, contact_id)
            )
        conn.commit()
        conn.close()

    # Create experiment record
    if batch_id:
        models.create_experiment({
            "name": f"A/B Test: {variable}",
            "variable": variable,
            "group_a_desc": group_descriptions.get("A", "Control"),
            "group_b_desc": group_descriptions.get("B", "Variant"),
            "batches_included": [batch_id],
            "status": "active",
        })

    # Summary
    a_count = sum(1 for v in assignments.values() if v == "A")
    b_count = sum(1 for v in assignments.values() if v == "B")

    return {
        "variable": variable,
        "groups": group_descriptions,
        "assignments": assignments,
        "group_a_count": a_count,
        "group_b_count": b_count,
    }


def get_ab_group_for_contact(contact_id: str, batch_id: str) -> Optional[str]:
    """Get the A/B group assignment for a contact in a batch."""
    conn = models.get_db()
    row = conn.execute(
        "SELECT ab_group FROM batch_prospects WHERE batch_id=? AND contact_id=?",
        (batch_id, contact_id)
    ).fetchone()
    conn.close()
    return row["ab_group"] if row else None
