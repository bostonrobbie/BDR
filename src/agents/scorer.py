"""
Outreach Command Center - Scoring Engines
ICP scoring (0-12) and Priority scoring (1-5) for contacts.
Feature-based scoring (0-100) from ResearchArtifact with explanation objects.
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.db import models


# ─── SCORING CONFIG LOADER ────────────────────────────────────

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../../config/scoring_weights.json")
_cached_config = None


def load_scoring_config(path: str = None) -> dict:
    """Load scoring weights from config file. Cached after first load."""
    global _cached_config
    if _cached_config is not None and path is None:
        return _cached_config
    config_path = path or _CONFIG_PATH
    try:
        with open(config_path, "r") as f:
            _cached_config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        _cached_config = _default_config()
    return _cached_config


def _default_config() -> dict:
    """Fallback config if file is missing."""
    return {
        "features": {
            "title_seniority": {"max_points": 20, "tiers": {"primary_qa_leader": 20, "secondary_eng_leader": 14, "influencer_ic": 8, "adjacent_role": 4, "no_match": 0}},
            "function_match": {"max_points": 15, "tiers": {"qa_testing": 15, "engineering": 10, "devops_platform": 7, "product": 4, "other": 0}},
            "company_size_fit": {"max_points": 10, "bands": {"201-500": 10, "501-1000": 10, "1001-5000": 8, "51-200": 6, "5001-10000": 6, "10001-50000": 4, "1-50": 2, "50000+": 2}},
            "industry_fit": {"max_points": 10, "tiers": {"primary": 10, "secondary": 6, "tertiary": 3, "no_match": 0}},
            "pain_confidence": {"max_points": 20, "scoring": {"has_competitor_tool": 8, "has_pain_hypothesis_high_conf": 6, "has_pain_hypothesis_medium_conf": 3, "has_hiring_signal": 4, "has_tech_stack_evidence": 4}},
            "intent_signal": {"max_points": 15, "scoring": {"buyer_intent_flag": 8, "recently_hired": 5, "funding_event": 4, "digital_transformation": 5, "hiring_qa": 4, "compliance_trigger": 3}},
            "data_quality": {"max_points": 10, "scoring": {"has_email": 2, "has_linkedin_url": 2, "has_company_research": 2, "has_person_research": 2, "has_title": 1, "has_company_name": 1}},
        },
        "thresholds": {"hot": 70, "warm": 45, "cool": 25, "cold": 0},
    }


# ─── FEATURE-BASED SCORING (0-100) FROM RESEARCH ARTIFACT ─────

def score_from_artifact(artifact: dict, config: dict = None) -> dict:
    """Score a prospect from their ResearchArtifact. Deterministic and explainable.

    Args:
        artifact: A ResearchArtifact dict.
        config: Scoring config (loaded from file if None).

    Returns:
        ScoringResult: {total_score, tier, feature_scores, feature_weights,
                       reasons, missing_data}
    """
    config = config or load_scoring_config()
    features_cfg = config.get("features", {})
    thresholds = config.get("thresholds", {"hot": 70, "warm": 45, "cool": 25, "cold": 0})

    feature_scores = {}
    feature_weights = {}
    reasons = []
    missing_data = []

    prospect = artifact.get("prospect", {})
    company = artifact.get("company", {})
    signals = artifact.get("signals", {})
    pains = artifact.get("pains", {})
    personalization = artifact.get("personalization", {})

    # 1. Title / Seniority (0-20)
    ts_cfg = features_cfg.get("title_seniority", {})
    ts_max = ts_cfg.get("max_points", 20)
    feature_weights["title_seniority"] = ts_max
    title = prospect.get("title", "").lower()
    seniority = prospect.get("seniority", "").lower()

    primary_titles = ts_cfg.get("primary_titles", [])
    secondary_titles = ts_cfg.get("secondary_titles", [])
    influencer_titles = ts_cfg.get("influencer_titles", [])
    adjacent_titles = ts_cfg.get("adjacent_titles", [])
    tiers = ts_cfg.get("tiers", {})

    title_normalized = title.replace(" of ", " ").replace("  ", " ").strip()
    ts_score = tiers.get("no_match", 0)
    matched_tier = "no_match"

    for t in primary_titles:
        t_norm = t.replace(" of ", " ").replace("  ", " ").strip()
        if t in title or t_norm in title_normalized:
            ts_score = tiers.get("primary_qa_leader", 20)
            matched_tier = "primary_qa_leader"
            break
    if matched_tier == "no_match":
        for t in secondary_titles:
            t_norm = t.replace(" of ", " ").replace("  ", " ").strip()
            if t in title or t_norm in title_normalized:
                ts_score = tiers.get("secondary_eng_leader", 14)
                matched_tier = "secondary_eng_leader"
                break
    if matched_tier == "no_match":
        for t in influencer_titles:
            if t in title:
                ts_score = tiers.get("influencer_ic", 8)
                matched_tier = "influencer_ic"
                break
    if matched_tier == "no_match":
        for t in adjacent_titles:
            if t in title:
                ts_score = tiers.get("adjacent_role", 4)
                matched_tier = "adjacent_role"
                break

    feature_scores["title_seniority"] = ts_score
    if ts_score > 0:
        reasons.append(f"Title '{prospect.get('title', '')}' matches {matched_tier} tier ({ts_score}/{ts_max})")
    else:
        reasons.append(f"Title '{prospect.get('title', '')}' does not match ICP title list (0/{ts_max})")
    if not title:
        missing_data.append("prospect.title is empty")

    # 2. Function Match (0-15)
    fm_cfg = features_cfg.get("function_match", {})
    fm_max = fm_cfg.get("max_points", 15)
    feature_weights["function_match"] = fm_max
    function = prospect.get("function", "").lower()
    fm_tiers = fm_cfg.get("tiers", {})

    qa_kw = fm_cfg.get("qa_keywords", ["qa", "quality", "test", "sdet", "automation"])
    eng_kw = fm_cfg.get("engineering_keywords", ["engineering", "software", "development", "cto"])
    devops_kw = fm_cfg.get("devops_keywords", ["devops", "platform", "infrastructure", "sre"])
    product_kw = fm_cfg.get("product_keywords", ["product", "program"])

    if any(kw in function or kw in title for kw in qa_kw):
        fm_score = fm_tiers.get("qa_testing", 15)
        reasons.append(f"Function matches QA/Testing ({fm_score}/{fm_max})")
    elif any(kw in function or kw in title for kw in eng_kw):
        fm_score = fm_tiers.get("engineering", 10)
        reasons.append(f"Function matches Engineering ({fm_score}/{fm_max})")
    elif any(kw in function or kw in title for kw in devops_kw):
        fm_score = fm_tiers.get("devops_platform", 7)
        reasons.append(f"Function matches DevOps/Platform ({fm_score}/{fm_max})")
    elif any(kw in function or kw in title for kw in product_kw):
        fm_score = fm_tiers.get("product", 4)
        reasons.append(f"Function matches Product ({fm_score}/{fm_max})")
    else:
        fm_score = fm_tiers.get("other", 0)
        reasons.append(f"Function '{function}' not in ICP (0/{fm_max})")
    feature_scores["function_match"] = fm_score

    # 3. Company Size Fit (0-10)
    cs_cfg = features_cfg.get("company_size_fit", {})
    cs_max = cs_cfg.get("max_points", 10)
    feature_weights["company_size_fit"] = cs_max
    size_band = company.get("size_band", "")
    bands_map = cs_cfg.get("bands", {})
    cs_score = bands_map.get(size_band, 0)
    feature_scores["company_size_fit"] = cs_score
    if cs_score > 0:
        reasons.append(f"Company size '{size_band}' scores {cs_score}/{cs_max}")
    elif size_band:
        reasons.append(f"Company size '{size_band}' outside sweet spot (0/{cs_max})")
    else:
        missing_data.append("company.size_band is empty")

    # 4. Industry Fit (0-10)
    ind_cfg = features_cfg.get("industry_fit", {})
    ind_max = ind_cfg.get("max_points", 10)
    feature_weights["industry_fit"] = ind_max
    industry = company.get("industry", "").lower()
    ind_tiers = ind_cfg.get("tiers", {})

    primary_verts = ind_cfg.get("primary_verticals", [])
    secondary_verts = ind_cfg.get("secondary_verticals", [])
    tertiary_verts = ind_cfg.get("tertiary_verticals", [])

    ind_score = ind_tiers.get("no_match", 0)
    if any(v in industry for v in primary_verts):
        ind_score = ind_tiers.get("primary", 10)
        reasons.append(f"Industry '{company.get('industry', '')}' is primary vertical ({ind_score}/{ind_max})")
    elif any(v in industry for v in secondary_verts):
        ind_score = ind_tiers.get("secondary", 6)
        reasons.append(f"Industry '{company.get('industry', '')}' is secondary vertical ({ind_score}/{ind_max})")
    elif any(v in industry for v in tertiary_verts):
        ind_score = ind_tiers.get("tertiary", 3)
        reasons.append(f"Industry '{company.get('industry', '')}' is tertiary vertical ({ind_score}/{ind_max})")
    else:
        reasons.append(f"Industry '{company.get('industry', '')}' not in ICP verticals (0/{ind_max})")
    if not industry:
        missing_data.append("company.industry is empty")
    feature_scores["industry_fit"] = ind_score

    # 5. Pain Confidence (0-20)
    pc_cfg = features_cfg.get("pain_confidence", {})
    pc_max = pc_cfg.get("max_points", 20)
    feature_weights["pain_confidence"] = pc_max
    pc_scoring = pc_cfg.get("scoring", {})
    pc_score = 0

    tech_stack = signals.get("tech_stack", [])
    competitor_tools = {"selenium", "cypress", "playwright", "tosca", "katalon", "testim", "mabl"}
    has_competitor = False
    for item in tech_stack:
        val = item.get("value", "") if isinstance(item, dict) else str(item)
        if val.lower() in competitor_tools:
            has_competitor = True
            break

    if has_competitor:
        pc_score += pc_scoring.get("has_competitor_tool", 8)
        reasons.append(f"Uses competitor tool (+{pc_scoring.get('has_competitor_tool', 8)} pain confidence)")

    if tech_stack:
        pc_score += pc_scoring.get("has_tech_stack_evidence", 4)

    hypothesized = pains.get("hypothesized_pains", [])
    high_conf_pain = any(p.get("confidence", 0) > 0.7 for p in hypothesized)
    med_conf_pain = any(0.4 <= p.get("confidence", 0) <= 0.7 for p in hypothesized)
    if high_conf_pain:
        pc_score += pc_scoring.get("has_pain_hypothesis_high_conf", 6)
        reasons.append(f"High-confidence pain hypothesis (+{pc_scoring.get('has_pain_hypothesis_high_conf', 6)})")
    elif med_conf_pain:
        pc_score += pc_scoring.get("has_pain_hypothesis_medium_conf", 3)
        reasons.append(f"Medium-confidence pain hypothesis (+{pc_scoring.get('has_pain_hypothesis_medium_conf', 3)})")

    # Check for hiring signal in triggers
    triggers = signals.get("triggers", [])
    has_hiring = any("hiring" in (t.get("value", "") if isinstance(t, dict) else str(t)).lower()
                     for t in triggers)
    if has_hiring:
        pc_score += pc_scoring.get("has_hiring_signal", 4)

    pc_score = min(pc_score, pc_max)
    feature_scores["pain_confidence"] = pc_score
    if not hypothesized:
        missing_data.append("No pain hypotheses available")

    # 6. Intent Signal (0-15)
    is_cfg = features_cfg.get("intent_signal", {})
    is_max = is_cfg.get("max_points", 15)
    feature_weights["intent_signal"] = is_max
    is_scoring = is_cfg.get("scoring", {})
    is_score = 0

    intent_signals = signals.get("intent_signals", [])
    for sig in intent_signals:
        val = sig.get("value", "") if isinstance(sig, dict) else str(sig)
        val_lower = val.lower()
        if "buyer intent" in val_lower:
            is_score += is_scoring.get("buyer_intent_flag", 8)
            reasons.append(f"Buyer intent flag detected (+{is_scoring.get('buyer_intent_flag', 8)})")
        if "recently" in val_lower or "new to role" in val_lower:
            is_score += is_scoring.get("recently_hired", 5)
            reasons.append(f"Recently hired signal (+{is_scoring.get('recently_hired', 5)})")

    for trig in triggers:
        val = trig.get("value", "") if isinstance(trig, dict) else str(trig)
        val_lower = val.lower()
        if "funding" in val_lower:
            is_score += is_scoring.get("funding_event", 4)
            reasons.append(f"Funding event trigger (+{is_scoring.get('funding_event', 4)})")
        if "digital transformation" in val_lower:
            is_score += is_scoring.get("digital_transformation", 5)
        if "compliance" in val_lower:
            is_score += is_scoring.get("compliance_trigger", 3)

    is_score = min(is_score, is_max)
    feature_scores["intent_signal"] = is_score
    if not intent_signals and not triggers:
        missing_data.append("No intent signals or triggers detected")

    # 7. Data Quality (0-10)
    dq_cfg = features_cfg.get("data_quality", {})
    dq_max = dq_cfg.get("max_points", 10)
    feature_weights["data_quality"] = dq_max
    dq_scoring = dq_cfg.get("scoring", {})
    dq_score = 0

    meta = artifact.get("metadata", {})
    data_sources = meta.get("data_sources", [])

    if prospect.get("linkedin_url"):
        dq_score += dq_scoring.get("has_linkedin_url", 2)
    else:
        missing_data.append("prospect.linkedin_url is empty")
    if prospect.get("title"):
        dq_score += dq_scoring.get("has_title", 1)
    if prospect.get("company_name"):
        dq_score += dq_scoring.get("has_company_name", 1)

    # Check data sources for research presence
    if any("company research" in ds for ds in data_sources):
        dq_score += dq_scoring.get("has_company_research", 2)
    else:
        missing_data.append("No company research available")
    if any("person research" in ds for ds in data_sources):
        dq_score += dq_scoring.get("has_person_research", 2)
    else:
        missing_data.append("No person research available")

    # Check if email exists in personalization hooks or prospect
    hooks = personalization.get("hooks", [])
    # We don't have email directly in artifact, but we can check if it was a data source
    # Email is checked at pipeline level, so give the points if we have good data
    if dq_score >= 4:  # If we have at least title + company + some research
        dq_score = min(dq_score, dq_max)

    feature_scores["data_quality"] = min(dq_score, dq_max)

    # ── Total ──
    total = sum(feature_scores.values())

    # Determine tier
    if total >= thresholds.get("hot", 70):
        tier = "hot"
    elif total >= thresholds.get("warm", 45):
        tier = "warm"
    elif total >= thresholds.get("cool", 25):
        tier = "cool"
    else:
        tier = "cold"

    return {
        "total_score": total,
        "max_possible": sum(feature_weights.values()),
        "tier": tier,
        "feature_scores": feature_scores,
        "feature_weights": feature_weights,
        "reasons": reasons,
        "missing_data": missing_data,
    }


# ─── ICP SCORING (0-12) — LEGACY ─────────────────────────────────

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
