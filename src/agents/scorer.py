"""
Outreach Command Center - Scoring Engines
ICP scoring (0-12) and Priority scoring (1-5) for contacts.
Feature-based scoring (0-100) from ResearchArtifact with explanation objects.
"""

import json
import math
import sys
import os
from datetime import datetime, timedelta

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


def compute_decay_factor(signal_age_days: float, half_life_days: float,
                          min_factor: float = 0.1) -> float:
    """Compute exponential decay factor for a signal based on its age.

    Uses half-life decay: factor = 0.5 ^ (age / half_life)
    A 90-day-old signal with a 90-day half-life contributes 50%.
    A 180-day-old signal with a 90-day half-life contributes 25%.

    Args:
        signal_age_days: How old the signal is in days.
        half_life_days: Number of days until the signal is worth 50%.
        min_factor: Floor so signals never fully vanish (default 0.1 = 10%).

    Returns:
        Float between min_factor and 1.0.
    """
    if half_life_days <= 0 or signal_age_days <= 0:
        return 1.0
    factor = math.pow(0.5, signal_age_days / half_life_days)
    return max(min_factor, round(factor, 4))


def get_signal_age_days(signal: dict, reference_date: str = None) -> float:
    """Get the age of a signal in days.

    Looks for 'detected_at', 'created_at', or 'timestamp' fields.
    Returns 0 if no date found (treats as fresh).
    """
    ref = datetime.utcnow()
    if reference_date:
        try:
            ref = datetime.fromisoformat(reference_date.replace("Z", "+00:00")).replace(tzinfo=None)
        except (ValueError, TypeError):
            pass

    for date_field in ("detected_at", "created_at", "timestamp"):
        date_str = signal.get(date_field, "")
        if date_str:
            try:
                sig_date = datetime.fromisoformat(date_str.replace("Z", "+00:00")).replace(tzinfo=None)
                return max(0, (ref - sig_date).total_seconds() / 86400)
            except (ValueError, TypeError):
                continue
    return 0  # No date found, treat as fresh


def apply_signal_decay(base_score: float, signal_type: str, signal: dict,
                        decay_config: dict = None, reference_date: str = None) -> tuple:
    """Apply decay to a signal's score contribution.

    Args:
        base_score: The raw score this signal would contribute.
        signal_type: Type key matching decay_config half_lives.
        signal: The signal dict (needs a date field for age calculation).
        decay_config: Decay config from scoring_weights.json.
        reference_date: Optional reference date (default: now).

    Returns:
        (decayed_score, decay_factor, age_days)
    """
    if not decay_config:
        return base_score, 1.0, 0

    half_lives = decay_config.get("half_lives", {})
    min_factor = decay_config.get("min_factor", 0.1)
    half_life = half_lives.get(signal_type, 0)

    if half_life <= 0:
        return base_score, 1.0, 0

    age_days = get_signal_age_days(signal, reference_date)
    if age_days <= 0:
        return base_score, 1.0, 0

    factor = compute_decay_factor(age_days, half_life, min_factor)
    return round(base_score * factor, 2), factor, round(age_days, 1)


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
    decay_config = config.get("signal_decay", None)

    feature_scores = {}
    feature_weights = {}
    reasons = []
    missing_data = []
    decay_applied = []

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

    # Pain specificity bonus: reward detailed, specific pains over generic ones
    pain_specificity = score_pain_specificity(hypothesized)
    if pain_specificity["specificity_bonus"] > 0:
        pc_score += pain_specificity["specificity_bonus"]
        reasons.append(f"Pain specificity bonus (+{pain_specificity['specificity_bonus']}, {pain_specificity['best_pain_label']})")

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
            raw = is_scoring.get("buyer_intent_flag", 8)
            decayed, factor, age = apply_signal_decay(raw, "buyer_intent_flag", sig if isinstance(sig, dict) else {}, decay_config)
            is_score += decayed
            reasons.append(f"Buyer intent flag detected (+{decayed})")
            if factor < 1.0:
                decay_applied.append({"signal": "buyer_intent_flag", "factor": factor, "age_days": age})
        if "recently" in val_lower or "new to role" in val_lower:
            raw = is_scoring.get("recently_hired", 5)
            decayed, factor, age = apply_signal_decay(raw, "recently_hired", sig if isinstance(sig, dict) else {}, decay_config)
            is_score += decayed
            reasons.append(f"Recently hired signal (+{decayed})")
            if factor < 1.0:
                decay_applied.append({"signal": "recently_hired", "factor": factor, "age_days": age})

    for trig in triggers:
        val = trig.get("value", "") if isinstance(trig, dict) else str(trig)
        val_lower = val.lower()
        if "funding" in val_lower:
            raw = is_scoring.get("funding_event", 4)
            decayed, factor, age = apply_signal_decay(raw, "funding_event", trig if isinstance(trig, dict) else {}, decay_config)
            is_score += decayed
            reasons.append(f"Funding event trigger (+{decayed})")
            if factor < 1.0:
                decay_applied.append({"signal": "funding_event", "factor": factor, "age_days": age})
        if "digital transformation" in val_lower:
            raw = is_scoring.get("digital_transformation", 5)
            decayed, factor, age = apply_signal_decay(raw, "digital_transformation", trig if isinstance(trig, dict) else {}, decay_config)
            is_score += decayed
            if factor < 1.0:
                decay_applied.append({"signal": "digital_transformation", "factor": factor, "age_days": age})
        if "compliance" in val_lower:
            raw = is_scoring.get("compliance_trigger", 3)
            decayed, factor, age = apply_signal_decay(raw, "compliance_trigger", trig if isinstance(trig, dict) else {}, decay_config)
            is_score += decayed
            if factor < 1.0:
                decay_applied.append({"signal": "compliance_trigger", "factor": factor, "age_days": age})

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
        "decay_applied": decay_applied,
    }


# ─── PAIN SPECIFICITY SCORING ────────────────────────────────────

# Specificity indicators: these signal the pain description is detailed
# and grounded, not a generic placeholder
SPECIFICITY_KEYWORDS = {
    "tool_names": ["selenium", "cypress", "playwright", "tosca", "katalon",
                   "testim", "mabl", "jenkins", "browserstack", "appium"],
    "team_context": ["ui layer", "api layer", "mobile", "regression suite",
                     "ci/cd", "pipeline", "sprint", "release cycle", "deploy"],
    "quantified": ["hours", "minutes", "days", "weeks", "%", "percent",
                   "x faster", "x slower"],
    "workflow": ["checkout", "payment", "onboarding", "compliance",
                 "policy", "claims", "enrollment", "billing"],
}


def score_pain_specificity(pains: list) -> dict:
    """Score pain hypotheses for specificity and depth.

    Generic: 'test maintenance overhead' -> 0 bonus
    Specific: 'Flaky Selenium tests in the payment checkout flow' -> +2 bonus

    Evaluates: tool name mentions, team/layer context, quantified terms,
    workflow-specific references, and evidence backing.

    Args:
        pains: List of pain hypothesis dicts with 'pain', 'confidence', 'evidence'.

    Returns:
        {"specificity_bonus": 0-3, "best_pain_label": str,
         "pain_scores": [...]}
    """
    if not pains:
        return {"specificity_bonus": 0, "best_pain_label": "none",
                "pain_scores": []}

    pain_scores = []
    for p in pains:
        pain_text = p.get("pain", "").lower()
        evidence = p.get("evidence", "").lower()
        confidence = p.get("confidence", 0)
        spec_score = 0
        indicators = []

        # Tool name specificity
        for tool in SPECIFICITY_KEYWORDS["tool_names"]:
            if tool in pain_text:
                spec_score += 1
                indicators.append(f"tool:{tool}")
                break

        # Team/layer context
        for ctx in SPECIFICITY_KEYWORDS["team_context"]:
            if ctx in pain_text:
                spec_score += 1
                indicators.append(f"context:{ctx}")
                break

        # Quantified impact
        for q in SPECIFICITY_KEYWORDS["quantified"]:
            if q in pain_text:
                spec_score += 1
                indicators.append(f"quantified:{q}")
                break

        # Workflow specificity
        for wf in SPECIFICITY_KEYWORDS["workflow"]:
            if wf in pain_text:
                spec_score += 1
                indicators.append(f"workflow:{wf}")
                break

        # Evidence-backed pains are more specific
        has_real_evidence = evidence and evidence != "unknown - hypothesis only"
        if has_real_evidence and confidence >= 0.7:
            spec_score += 1
            indicators.append("evidence_backed")

        pain_scores.append({
            "pain": p.get("pain", ""),
            "specificity_score": spec_score,
            "indicators": indicators,
        })

    # Best pain determines the bonus
    best = max(pain_scores, key=lambda x: x["specificity_score"])
    # Map specificity score to bonus: 3+ indicators = +3, 2 = +2, 1 = +1, 0 = 0
    bonus = min(3, best["specificity_score"])

    return {
        "specificity_bonus": bonus,
        "best_pain_label": best["pain"][:50] if best["pain"] else "generic",
        "pain_scores": pain_scores,
    }


# ─── SCORING WEIGHT A/B TESTING ──────────────────────────────────

def compare_weight_configs(artifacts: list, config_a: dict, config_b: dict,
                            labels: tuple = ("config_A", "config_B")) -> dict:
    """Compare two scoring weight configs by replaying artifacts through both.

    Takes a list of ResearchArtifacts and scores each with both configs.
    Returns tier distribution, score deltas, and which contacts switch tiers.

    Args:
        artifacts: List of ResearchArtifact dicts.
        config_a: First scoring config dict.
        config_b: Second scoring config dict.
        labels: Names for the two configs (for readability).

    Returns:
        {"summary": {...}, "tier_shifts": [...], "score_deltas": [...],
         "tier_distribution_a": {...}, "tier_distribution_b": {...}}
    """
    results_a = []
    results_b = []
    tier_shifts = []
    score_deltas = []

    for artifact in artifacts:
        score_a = score_from_artifact(artifact, config_a)
        score_b = score_from_artifact(artifact, config_b)
        results_a.append(score_a)
        results_b.append(score_b)

        name = artifact.get("prospect", {}).get("full_name", "unknown")
        delta = score_b["total_score"] - score_a["total_score"]
        score_deltas.append({
            "prospect": name,
            "score_a": score_a["total_score"],
            "score_b": score_b["total_score"],
            "delta": delta,
            "tier_a": score_a["tier"],
            "tier_b": score_b["tier"],
        })

        if score_a["tier"] != score_b["tier"]:
            tier_shifts.append({
                "prospect": name,
                "from_tier": score_a["tier"],
                "to_tier": score_b["tier"],
                "score_a": score_a["total_score"],
                "score_b": score_b["total_score"],
            })

    # Tier distributions
    dist_a = _tier_distribution(results_a)
    dist_b = _tier_distribution(results_b)

    # Score statistics
    scores_a = [r["total_score"] for r in results_a]
    scores_b = [r["total_score"] for r in results_b]

    return {
        "labels": labels,
        "contact_count": len(artifacts),
        "summary": {
            "mean_score_a": round(sum(scores_a) / max(len(scores_a), 1), 1),
            "mean_score_b": round(sum(scores_b) / max(len(scores_b), 1), 1),
            "mean_delta": round(sum(d["delta"] for d in score_deltas) / max(len(score_deltas), 1), 1),
            "tier_shift_count": len(tier_shifts),
            "tier_shift_pct": round(len(tier_shifts) / max(len(artifacts), 1) * 100, 1),
        },
        "tier_distribution_a": dist_a,
        "tier_distribution_b": dist_b,
        "tier_shifts": tier_shifts,
        "score_deltas": sorted(score_deltas, key=lambda d: abs(d["delta"]), reverse=True),
    }


def _tier_distribution(results: list) -> dict:
    """Count contacts per tier."""
    dist = {"hot": 0, "warm": 0, "cool": 0, "cold": 0}
    for r in results:
        tier = r.get("tier", "cold")
        dist[tier] = dist.get(tier, 0) + 1
    total = max(len(results), 1)
    return {
        tier: {"count": count, "pct": round(count / total * 100, 1)}
        for tier, count in dist.items()
    }


def score_sensitivity(artifact: dict, config: dict = None) -> dict:
    """Show how sensitive a score is to each feature.

    For each feature, shows: 'if this feature were maxed out, the score
    would increase by X and the tier would change to Y.'

    Args:
        artifact: A ResearchArtifact dict.
        config: Scoring config.

    Returns:
        {"current": {...}, "sensitivities": [...]}
    """
    config = config or load_scoring_config()
    baseline = score_from_artifact(artifact, config)
    features_cfg = config.get("features", {})

    sensitivities = []
    for feature_name, feature_cfg in features_cfg.items():
        max_pts = feature_cfg.get("max_points", 0)
        current = baseline["feature_scores"].get(feature_name, 0)
        gap = max_pts - current

        if gap > 0:
            # Score if this feature were maxed
            hypothetical_total = baseline["total_score"] + gap
            thresholds = config.get("thresholds", {"hot": 70, "warm": 45, "cool": 25})
            if hypothetical_total >= thresholds.get("hot", 70):
                hyp_tier = "hot"
            elif hypothetical_total >= thresholds.get("warm", 45):
                hyp_tier = "warm"
            elif hypothetical_total >= thresholds.get("cool", 25):
                hyp_tier = "cool"
            else:
                hyp_tier = "cold"

            sensitivities.append({
                "feature": feature_name,
                "current_score": current,
                "max_possible": max_pts,
                "gap": gap,
                "hypothetical_total": hypothetical_total,
                "hypothetical_tier": hyp_tier,
                "tier_would_change": hyp_tier != baseline["tier"],
            })

    sensitivities.sort(key=lambda s: s["gap"], reverse=True)

    return {
        "current": {
            "total_score": baseline["total_score"],
            "tier": baseline["tier"],
        },
        "sensitivities": sensitivities,
    }


# ─── ICP SCORING (0-12) — DEPRECATED ─────────────────────────────
# This scoring system is superseded by score_from_artifact() (0-100 scale).
# Kept only for backward compatibility with code that calls compute_icp_score().
# New code should use score_from_artifact() exclusively.

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
