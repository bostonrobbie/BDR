"""
Outreach Command Center - Scoring Engines
ICP scoring (0-12) and Priority scoring (1-5) for contacts.
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.db import models


# ─── ICP SCORING (0-12) ────────────────────────────────────────

ICP_TITLE_MAP = {
    # Primary (3 points) - QA-titled leaders
    "qa manager": 3, "qa lead": 3, "director of qa": 3, "head of qa": 3,
    "vp quality": 3, "vp quality engineering": 3, "sr director quality": 3,
    "director quality engineering": 3, "director of quality engineering": 3,
    "director of quality": 3, "head of quality": 3,
    "quality engineering manager": 3, "quality assurance": 3,
    # Secondary (2 points) - Engineering leaders
    "software eng manager": 2, "vp engineering": 2, "vp software engineering": 2,
    "cto": 2, "director of engineering": 2, "director engineering": 2,
    # Influencer (1 point) - Technical ICs
    "senior sdet": 1, "automation lead": 1, "qa architect": 1, "test architect": 1,
    "sdet lead": 1, "principal sdet": 1, "test lead": 1,
}

ICP_VERTICALS = {
    "saas": 2, "fintech": 2, "healthcare": 2, "digital health": 2,
    "retail": 1, "e-commerce": 1, "telecom": 1, "pharma": 1,
    "financial services": 2, "banking": 2, "insurance": 1,
}

ICP_SIZE_BANDS = {
    "51-200": 1, "201-500": 2, "501-1000": 2, "1001-5000": 2,
    "5001-10000": 1, "10001-50000": 1,
}


def compute_icp_score(contact: dict, account: dict) -> dict:
    """
    Compute ICP score (0-12) across 5 dimensions.

    Dimensions:
    - Title match (0-3)
    - Vertical match (0-2)
    - Company size fit (0-2)
    - Seniority fit (0-2)
    - Buyer intent bonus (0-3)
    """
    scores = {}

    # Title match (0-3)
    title_lower = (contact.get("title") or "").lower()
    # Normalize: strip "of", extra spaces for matching
    title_normalized = title_lower.replace(" of ", " ").replace("  ", " ").strip()
    title_score = 0
    for title_key, points in ICP_TITLE_MAP.items():
        key_normalized = title_key.replace(" of ", " ").replace("  ", " ").strip()
        if title_key in title_lower or key_normalized in title_normalized:
            title_score = max(title_score, points)
    scores["title_match"] = title_score

    # Vertical match (0-2)
    industry_lower = (account.get("industry") or "").lower()
    vertical_score = 0
    for vertical, points in ICP_VERTICALS.items():
        if vertical in industry_lower:
            vertical_score = max(vertical_score, points)
    scores["vertical_match"] = vertical_score

    # Company size fit (0-2)
    emp_band = account.get("employee_band", "")
    emp_count = account.get("employee_count", 0)
    size_score = ICP_SIZE_BANDS.get(emp_band, 0)
    if not size_score and emp_count:
        if 51 <= emp_count <= 200:
            size_score = 1
        elif 201 <= emp_count <= 10000:
            size_score = 2
        elif 10001 <= emp_count <= 50000:
            size_score = 1
    scores["company_size_fit"] = size_score

    # Seniority fit (0-2)
    seniority = (contact.get("seniority_level") or "").lower()
    if seniority in ("director", "vp", "c-suite", "head"):
        scores["seniority_fit"] = 2
    elif seniority in ("manager", "senior", "lead"):
        scores["seniority_fit"] = 1
    else:
        # Infer from title
        if any(s in title_lower for s in ["director", "vp", "head of", "chief"]):
            scores["seniority_fit"] = 2
        elif any(s in title_lower for s in ["manager", "lead", "senior", "sr"]):
            scores["seniority_fit"] = 1
        else:
            scores["seniority_fit"] = 0

    # Buyer intent bonus (0-3)
    buyer_intent = account.get("buyer_intent", 0)
    if buyer_intent:
        scores["buyer_intent_bonus"] = 3
    else:
        scores["buyer_intent_bonus"] = 0

    total = sum(scores.values())
    scores["total_score"] = total

    return scores


def score_icp_and_save(contact_id: str) -> dict:
    """Score ICP for a contact and save to icp_scores table."""
    contact = models.get_contact(contact_id)
    if not contact:
        return {"error": "Contact not found"}

    account = models.get_account(contact.get("account_id", "")) if contact.get("account_id") else {}
    scores = compute_icp_score(contact, account or {})

    # Save to icp_scores
    conn = models.get_db()
    icp_id = models.gen_id("icp")
    conn.execute("""
        INSERT INTO icp_scores (id, contact_id, title_match, vertical_match,
            company_size_fit, seniority_fit, software_qa_confirmed, buyer_intent_bonus,
            total_score, scored_at, scoring_version)
        VALUES (?,?,?,?,?,?,?,?,?,datetime('now'),'v1')
    """, (
        icp_id, contact_id, scores["title_match"], scores["vertical_match"],
        scores["company_size_fit"], scores["seniority_fit"], 1,
        scores["buyer_intent_bonus"], scores["total_score"]
    ))
    conn.commit()
    conn.close()

    # Also compute and save priority score
    priority = models.score_and_save(contact_id)

    return {
        "icp_score": scores,
        "priority_score": priority,
        "contact_id": contact_id
    }


def batch_score(contact_ids: list) -> list:
    """Score multiple contacts at once."""
    results = []
    for cid in contact_ids:
        result = score_icp_and_save(cid)
        results.append(result)
    return results


if __name__ == "__main__":
    # Test with sample data
    sample_contact = {
        "title": "Director of Quality Engineering",
        "seniority_level": "director"
    }
    sample_account = {
        "industry": "FinTech",
        "employee_count": 500,
        "employee_band": "201-500",
        "buyer_intent": 1
    }
    scores = compute_icp_score(sample_contact, sample_account)
    print(f"ICP Score: {scores['total_score']}/12")
    for k, v in scores.items():
        if k != "total_score":
            print(f"  {k}: {v}")
