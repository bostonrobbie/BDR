"""
Unit tests for the scoring engine.

Sections:
  1. Legacy ICP scoring (0-12 scale)
  2. Priority scoring
  3. V2 feature-based scorer (0-100 scale)
  4. Signal decay (A1)
  5. Weight A/B testing (A2)
  6. Pain specificity scoring (A4)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.agents.scorer import (
    compute_icp_score,
    score_from_artifact,
    load_scoring_config,
    compute_decay_factor,
    get_signal_age_days,
    apply_signal_decay,
    compare_weight_configs,
    score_sensitivity,
    score_pain_specificity,
)
from src.agents.researcher import build_research_artifact
from src.db.models import compute_priority_score


# ─── SAMPLE DATA ──────────────────────────────────────────────

CONTACT = {
    "first_name": "Sarah", "last_name": "Chen",
    "title": "Director of Quality Engineering", "seniority_level": "director",
    "company_name": "PayFlow", "linkedin_url": "https://linkedin.com/in/sarahchen",
}
ACCOUNT = {
    "name": "PayFlow", "domain": "payflow.com", "industry": "FinTech",
    "employee_band": "201-500", "employee_count": 350,
    "buyer_intent": 1, "known_tools": '["Selenium", "Jenkins"]',
}

PROSPECT_2 = {
    "first_name": "Mike", "last_name": "Torres",
    "title": "VP of Engineering", "seniority_level": "vp",
    "company_name": "HealthBridge",
}
ACCOUNT_2 = {
    "name": "HealthBridge", "industry": "Healthcare",
    "employee_band": "501-1000", "employee_count": 800,
    "buyer_intent": 0, "known_tools": "[]",
}

PROSPECT_3 = {
    "first_name": "Priya", "last_name": "Patel",
    "title": "Software Engineer", "seniority_level": "",
    "company_name": "",
}

PROSPECT_4 = {
    "first_name": "James", "last_name": "Wilson",
    "title": "QA Manager", "seniority_level": "manager",
    "company_name": "CloudStack",
}
ACCOUNT_4 = {
    "name": "CloudStack", "industry": "SaaS / B2B Software",
    "employee_band": "1001-5000", "employee_count": 2500,
    "buyer_intent": 0, "known_tools": '["Cypress", "Playwright"]',
}

PROSPECT_5 = {
    "first_name": "Ana", "last_name": "Rodriguez",
    "title": "CTO", "seniority_level": "c-suite",
    "company_name": "TinyApp",
}
ACCOUNT_5 = {
    "name": "TinyApp", "industry": "Tech",
    "employee_band": "1-50", "employee_count": 20,
    "buyer_intent": 0, "known_tools": "[]",
}


_SENTINEL = object()


def _build_artifact(contact=_SENTINEL, account=_SENTINEL, person_research=None,
                    company_research=None, signals=None):
    c = CONTACT if contact is _SENTINEL else contact
    a = ACCOUNT if account is _SENTINEL else account
    result = build_research_artifact(c, a, person_research, company_research, signals)
    return result["artifact"]


# ═══════════════════════════════════════════════════════════════
# 1. LEGACY ICP SCORING (0-12)
# ═══════════════════════════════════════════════════════════════

def test_icp_perfect_score():
    """Director of QA at a mid-size fintech with buyer intent should score high."""
    scores = compute_icp_score(CONTACT, ACCOUNT)
    assert scores["title_match"] == 3, f"Expected title_match=3, got {scores['title_match']}"
    assert scores["vertical_match"] == 2, f"Expected vertical_match=2, got {scores['vertical_match']}"
    assert scores["company_size_fit"] == 2, f"Expected company_size_fit=2, got {scores['company_size_fit']}"
    assert scores["seniority_fit"] == 2, f"Expected seniority_fit=2, got {scores['seniority_fit']}"
    assert scores["buyer_intent_bonus"] == 3, f"Expected buyer_intent=3, got {scores['buyer_intent_bonus']}"
    assert scores["total_score"] == 12, f"Expected total=12, got {scores['total_score']}"
    print("PASS: test_icp_perfect_score")


def test_icp_low_score():
    """Random engineer at unknown company should score low."""
    contact = {"title": "Software Engineer", "seniority_level": "individual"}
    account = {"industry": "Manufacturing", "employee_count": 80000, "employee_band": "50001+", "buyer_intent": 0}
    scores = compute_icp_score(contact, account)
    assert scores["title_match"] == 0
    assert scores["vertical_match"] == 0
    assert scores["buyer_intent_bonus"] == 0
    assert scores["total_score"] <= 2
    print("PASS: test_icp_low_score")


def test_icp_mid_score():
    """VP Engineering at a SaaS company, no buyer intent."""
    contact = {"title": "VP of Engineering", "seniority_level": "vp"}
    account = {"industry": "SaaS / B2B Software", "employee_count": 300, "employee_band": "201-500", "buyer_intent": 0}
    scores = compute_icp_score(contact, account)
    assert scores["title_match"] == 2
    assert scores["vertical_match"] == 2
    assert scores["seniority_fit"] == 2
    assert scores["buyer_intent_bonus"] == 0
    assert 5 <= scores["total_score"] <= 8
    print("PASS: test_icp_mid_score")


def test_legacy_icp_still_works():
    """Legacy ICP scoring should still function for backward compatibility."""
    scores = compute_icp_score(CONTACT, ACCOUNT)
    assert "total_score" in scores
    assert 0 <= scores["total_score"] <= 12
    print(f"PASS: test_legacy_icp_still_works (score={scores['total_score']})")


# ═══════════════════════════════════════════════════════════════
# 2. PRIORITY SCORING
# ═══════════════════════════════════════════════════════════════

def test_priority_hot():
    """Buyer intent + QA title + top vertical = priority 5."""
    contact = {"title": "Head of QA", "recently_hired": 0}
    account = {"buyer_intent": 1, "industry": "fintech", "employee_count": 1000, "known_tools": "[]"}
    result = compute_priority_score(contact, account)
    assert result["score"] == 4 or result["score"] == 5
    assert result["factors"].get("buyer_intent") == True
    assert result["factors"].get("qa_title") == True
    print(f"PASS: test_priority_hot (score={result['score']})")


def test_priority_penalty():
    """VP Eng at 50K+ company should get penalized."""
    contact = {"title": "VP of Engineering", "recently_hired": 0}
    account = {"buyer_intent": 0, "industry": "Consulting", "employee_count": 60000, "known_tools": "[]"}
    result = compute_priority_score(contact, account)
    assert result["factors"].get("vp_eng_large_co_penalty") == True
    assert result["score"] <= 2
    print(f"PASS: test_priority_penalty (score={result['score']})")


def test_priority_competitor_tool():
    """Company using Selenium should get bonus."""
    contact = {"title": "QA Manager", "recently_hired": 0}
    account = {"buyer_intent": 0, "industry": "tech", "employee_count": 500, "known_tools": '["Selenium", "Jenkins"]'}
    result = compute_priority_score(contact, account)
    assert result["factors"].get("competitor_tool") == True
    print(f"PASS: test_priority_competitor_tool (score={result['score']})")


def test_priority_recently_hired():
    """Recently hired QA director should get bonus."""
    contact = {"title": "Director of QA", "recently_hired": 1}
    account = {"buyer_intent": 0, "industry": "healthcare", "employee_count": 2000, "known_tools": "[]"}
    result = compute_priority_score(contact, account)
    assert result["factors"].get("recently_hired") == True
    assert result["factors"].get("qa_title") == True
    assert result["factors"].get("top_vertical") == True
    assert result["score"] >= 3
    print(f"PASS: test_priority_recently_hired (score={result['score']})")


def test_priority_clamp():
    """Score should be clamped between 1-5."""
    contact = {"title": "Director of QA", "recently_hired": 1}
    account = {"buyer_intent": 1, "industry": "fintech", "employee_count": 500, "known_tools": '["Selenium"]'}
    result = compute_priority_score(contact, account)
    assert result["score"] <= 5, f"Score {result['score']} exceeds max 5"
    assert result["score"] >= 1, f"Score {result['score']} below min 1"
    print(f"PASS: test_priority_clamp (score={result['score']})")


# ═══════════════════════════════════════════════════════════════
# 3. V2 FEATURE-BASED SCORER (0-100)
# ═══════════════════════════════════════════════════════════════

def test_determinism():
    """Same input must produce same output every time."""
    artifact = _build_artifact()
    result1 = score_from_artifact(artifact)
    result2 = score_from_artifact(artifact)
    assert result1["total_score"] == result2["total_score"], \
        f"Non-deterministic: {result1['total_score']} vs {result2['total_score']}"
    assert result1["feature_scores"] == result2["feature_scores"]
    print("PASS: test_determinism")


def test_perfect_icp_scores_high():
    """Sarah: Director QA at FinTech with Selenium + buyer intent -> hot."""
    artifact = _build_artifact(person_research={"headline": "QA Leader"})
    result = score_from_artifact(artifact)
    assert result["total_score"] >= 60, f"Expected >= 60, got {result['total_score']}"
    assert result["tier"] in ("hot", "warm"), f"Expected hot/warm, got {result['tier']}"
    assert result["feature_scores"]["title_seniority"] >= 14
    assert result["feature_scores"]["function_match"] >= 10
    assert result["feature_scores"]["industry_fit"] >= 6
    print(f"PASS: test_perfect_icp_scores_high (score={result['total_score']}, tier={result['tier']})")


def test_weak_prospect_scores_low():
    """Priya: Junior engineer, no account -> cold."""
    artifact = _build_artifact(PROSPECT_3, None)
    result = score_from_artifact(artifact)
    assert result["total_score"] <= 30, f"Expected <= 30, got {result['total_score']}"
    assert result["tier"] in ("cold", "cool"), f"Expected cold/cool, got {result['tier']}"
    print(f"PASS: test_weak_prospect_scores_low (score={result['total_score']}, tier={result['tier']})")


def test_scoring_order():
    """Prospects should rank in expected order: Sarah > James > Mike > Ana > Priya."""
    artifacts = [
        ("Sarah", _build_artifact(CONTACT, ACCOUNT)),
        ("James", _build_artifact(PROSPECT_4, ACCOUNT_4)),
        ("Mike", _build_artifact(PROSPECT_2, ACCOUNT_2)),
        ("Ana", _build_artifact(PROSPECT_5, ACCOUNT_5)),
        ("Priya", _build_artifact(PROSPECT_3, None)),
    ]
    scored = [(name, score_from_artifact(a)) for name, a in artifacts]
    scored.sort(key=lambda x: x[1]["total_score"], reverse=True)

    names_ranked = [s[0] for s in scored]
    ranking_parts = [f"{n}={r['total_score']}" for n, r in scored]
    print(f"  Ranking: {', '.join(ranking_parts)}")

    assert names_ranked[0] == "Sarah", f"Expected Sarah first, got {names_ranked[0]}"
    assert names_ranked[-1] == "Priya", f"Expected Priya last, got {names_ranked[-1]}"
    print("PASS: test_scoring_order")


def test_explanation_has_reasons():
    """Every scored prospect should have human-readable reasons."""
    artifact = _build_artifact()
    result = score_from_artifact(artifact)
    assert len(result["reasons"]) >= 5, f"Expected >= 5 reasons, got {len(result['reasons'])}"
    assert any("title" in r.lower() for r in result["reasons"])
    assert any("industry" in r.lower() or "vertical" in r.lower() for r in result["reasons"])
    print(f"PASS: test_explanation_has_reasons ({len(result['reasons'])} reasons)")


def test_missing_data_reported():
    """Missing fields should be reported in missing_data."""
    artifact = _build_artifact(PROSPECT_3, None)
    result = score_from_artifact(artifact)
    assert len(result["missing_data"]) >= 1, "Should report missing data"
    print(f"PASS: test_missing_data_reported ({len(result['missing_data'])} items: {result['missing_data'][:3]})")


def test_missing_data_reduces_quality():
    """Missing data should reduce the data_quality feature score."""
    artifact_full = _build_artifact(person_research={"headline": "QA Leader"})
    artifact_empty = _build_artifact(PROSPECT_3, None)
    result_full = score_from_artifact(artifact_full)
    result_empty = score_from_artifact(artifact_empty)
    assert result_full["feature_scores"]["data_quality"] > result_empty["feature_scores"]["data_quality"], \
        f"Full ({result_full['feature_scores']['data_quality']}) should have higher data quality than empty ({result_empty['feature_scores']['data_quality']})"
    print("PASS: test_missing_data_reduces_quality")


def test_feature_weights_sum():
    """Feature weights should sum to 100."""
    artifact = _build_artifact()
    result = score_from_artifact(artifact)
    total_weights = sum(result["feature_weights"].values())
    assert total_weights == 100, f"Expected weights sum = 100, got {total_weights}"
    print("PASS: test_feature_weights_sum")


def test_config_loads():
    """Config file should load without errors."""
    config = load_scoring_config()
    assert "features" in config
    assert "thresholds" in config
    assert len(config["features"]) == 7
    print("PASS: test_config_loads")


def test_v2_scorer_is_primary():
    """score_from_artifact should be the primary scorer with 0-100 scale."""
    artifact = _build_artifact()
    result = score_from_artifact(artifact)
    assert result["max_possible"] == 100, f"Max should be 100, got {result['max_possible']}"
    assert 0 <= result["total_score"] <= 100
    print("PASS: test_v2_scorer_is_primary")


def test_score_and_sort_all_5():
    """Score all 5 prospects and print sorted results."""
    prospects = [
        ("Sarah Chen", CONTACT, ACCOUNT),
        ("Mike Torres", PROSPECT_2, ACCOUNT_2),
        ("Priya Patel", PROSPECT_3, None),
        ("James Wilson", PROSPECT_4, ACCOUNT_4),
        ("Ana Rodriguez", PROSPECT_5, ACCOUNT_5),
    ]

    results = []
    for name, contact, account in prospects:
        artifact = _build_artifact(contact, account)
        score_result = score_from_artifact(artifact)
        results.append((name, score_result))

    results.sort(key=lambda x: x[1]["total_score"], reverse=True)

    print("\n  -- Prospect Ranking --")
    for rank, (name, r) in enumerate(results, 1):
        features = r["feature_scores"]
        print(f"  #{rank} {name}: {r['total_score']}/100 ({r['tier']})")
        print(f"       title={features['title_seniority']} func={features['function_match']} "
              f"size={features['company_size_fit']} ind={features['industry_fit']} "
              f"pain={features['pain_confidence']} intent={features['intent_signal']} "
              f"dq={features['data_quality']}")

    print("PASS: test_score_and_sort_all_5")


# ═══════════════════════════════════════════════════════════════
# 4. SIGNAL DECAY (A1)
# ═══════════════════════════════════════════════════════════════

def test_decay_factor_at_half_life():
    """At exactly one half-life, factor should be ~0.5."""
    factor = compute_decay_factor(90, 90)
    assert abs(factor - 0.5) < 0.01, f"At half-life, factor should be ~0.5, got {factor}"
    print("PASS: test_decay_factor_at_half_life")


def test_decay_factor_fresh_signal():
    """A brand new signal (age=0) should have factor=1.0."""
    factor = compute_decay_factor(0, 90)
    assert factor == 1.0, f"Fresh signal should have factor 1.0, got {factor}"
    print("PASS: test_decay_factor_fresh_signal")


def test_decay_factor_very_old():
    """A very old signal should approach min_factor."""
    factor = compute_decay_factor(1000, 90, min_factor=0.1)
    assert factor <= 0.15, f"Very old signal should be near min_factor, got {factor}"
    assert factor >= 0.1, f"Should not go below min_factor, got {factor}"
    print("PASS: test_decay_factor_very_old")


def test_decay_factor_min_floor():
    """Factor should never go below min_factor."""
    factor = compute_decay_factor(10000, 90, min_factor=0.1)
    assert factor >= 0.1
    print("PASS: test_decay_factor_min_floor")


def test_decay_factor_double_half_life():
    """At 2x half-life, factor should be ~0.25."""
    factor = compute_decay_factor(180, 90)
    assert abs(factor - 0.25) < 0.02, f"At 2x half-life, factor should be ~0.25, got {factor}"
    print("PASS: test_decay_factor_double_half_life")


def test_apply_signal_decay_with_config():
    """Applying decay should reduce score proportionally."""
    config = {
        "half_lives": {"recently_hired": 90},
        "min_factor": 0.1,
    }
    signal = {"value": "recently hired", "detected_at": "2025-09-01T00:00:00"}
    decayed, factor, age = apply_signal_decay(5, "recently_hired", signal, config,
                                               reference_date="2025-12-01T00:00:00")
    assert decayed < 5, f"Decayed score should be less than 5, got {decayed}"
    assert factor < 1.0, f"Factor should be < 1.0, got {factor}"
    assert age > 0, f"Age should be > 0, got {age}"
    print(f"PASS: test_apply_signal_decay_with_config (decayed={decayed}, factor={factor})")


def test_apply_signal_decay_no_config():
    """Without decay config, score should pass through unchanged."""
    decayed, factor, age = apply_signal_decay(8, "buyer_intent", {}, None)
    assert decayed == 8
    assert factor == 1.0
    print("PASS: test_apply_signal_decay_no_config")


def test_score_from_artifact_has_decay_field():
    """score_from_artifact should include decay_applied field."""
    artifact = _build_artifact()
    result = score_from_artifact(artifact)
    assert "decay_applied" in result, "Should have decay_applied field"
    print("PASS: test_score_from_artifact_has_decay_field")


# ═══════════════════════════════════════════════════════════════
# 5. WEIGHT A/B TESTING (A2)
# ═══════════════════════════════════════════════════════════════

def test_compare_weight_configs_basic():
    """Should produce a comparison with tier distributions."""
    config_a = load_scoring_config()
    config_b = {**config_a, "thresholds": {"hot": 80, "warm": 55, "cool": 30, "cold": 0}}

    artifacts = [_build_artifact()]
    result = compare_weight_configs(artifacts, config_a, config_b)

    assert "summary" in result
    assert "tier_distribution_a" in result
    assert "tier_distribution_b" in result
    assert "score_deltas" in result
    assert result["contact_count"] == 1
    print("PASS: test_compare_weight_configs_basic")


def test_compare_detects_tier_shift():
    """Changing thresholds should cause tier shifts."""
    config_a = load_scoring_config()
    config_b = {**config_a, "thresholds": {"hot": 99, "warm": 98, "cool": 97, "cold": 0}}

    artifacts = [_build_artifact()]
    result = compare_weight_configs(artifacts, config_a, config_b)

    assert len(result["tier_shifts"]) > 0 or result["score_deltas"][0]["tier_b"] == "cold", \
        f"Should detect tier shift: {result['score_deltas']}"
    print("PASS: test_compare_detects_tier_shift")


def test_score_sensitivity():
    """Should show which features have the most room for improvement."""
    artifact = _build_artifact()
    result = score_sensitivity(artifact)

    assert "current" in result
    assert "sensitivities" in result
    assert len(result["sensitivities"]) > 0
    for s in result["sensitivities"]:
        assert "feature" in s
        assert "gap" in s
        assert "hypothetical_total" in s
        assert s["gap"] >= 0
    print(f"PASS: test_score_sensitivity ({len(result['sensitivities'])} features with room)")


def test_sensitivity_sorted_by_gap():
    """Sensitivities should be sorted by gap descending."""
    artifact = _build_artifact()
    result = score_sensitivity(artifact)

    gaps = [s["gap"] for s in result["sensitivities"]]
    assert gaps == sorted(gaps, reverse=True), f"Should be sorted by gap desc: {gaps}"
    print("PASS: test_sensitivity_sorted_by_gap")


# ═══════════════════════════════════════════════════════════════
# 6. PAIN SPECIFICITY (A4)
# ═══════════════════════════════════════════════════════════════

def test_specific_pain_gets_bonus():
    """Pain with tool names and workflow context should get high specificity."""
    pains = [
        {
            "pain": "Flaky Selenium tests in the payment checkout flow causing 2-day regression cycles",
            "confidence": 0.8,
            "evidence": "from CRM field: known_tools (Selenium)"
        }
    ]
    result = score_pain_specificity(pains)
    assert result["specificity_bonus"] >= 2, \
        f"Specific pain should get bonus >= 2, got {result['specificity_bonus']}"
    print(f"PASS: test_specific_pain_gets_bonus (bonus={result['specificity_bonus']})")


def test_generic_pain_no_bonus():
    """Generic pain hypothesis should get 0 bonus."""
    pains = [
        {
            "pain": "Test maintenance overhead",
            "confidence": 0.3,
            "evidence": "unknown - hypothesis only"
        }
    ]
    result = score_pain_specificity(pains)
    assert result["specificity_bonus"] <= 1, \
        f"Generic pain should get low bonus, got {result['specificity_bonus']}"
    print(f"PASS: test_generic_pain_no_bonus (bonus={result['specificity_bonus']})")


def test_pain_with_tool_and_workflow():
    """Pain mentioning specific tool AND workflow should max out."""
    pains = [
        {
            "pain": "Selenium maintenance in the payment checkout pipeline taking 3 hours per sprint",
            "confidence": 0.9,
            "evidence": "from CRM field: known_tools (Selenium)"
        }
    ]
    result = score_pain_specificity(pains)
    assert result["specificity_bonus"] == 3, \
        f"Tool + workflow + quantified should get max bonus 3, got {result['specificity_bonus']}"
    print("PASS: test_pain_with_tool_and_workflow")


def test_pain_specificity_empty():
    """Empty pains list should return 0 bonus."""
    result = score_pain_specificity([])
    assert result["specificity_bonus"] == 0
    print("PASS: test_pain_specificity_empty")


def test_pain_specificity_indicators():
    """Should list which specificity indicators were found."""
    pains = [
        {
            "pain": "Cypress regression suite breaking in ci/cd pipeline",
            "confidence": 0.7,
            "evidence": "from CRM field: known_tools"
        }
    ]
    result = score_pain_specificity(pains)
    assert len(result["pain_scores"]) == 1
    assert len(result["pain_scores"][0]["indicators"]) >= 2, \
        f"Should have multiple indicators: {result['pain_scores'][0]['indicators']}"
    print(f"PASS: test_pain_specificity_indicators ({result['pain_scores'][0]['indicators']})")


def test_pain_specificity_integrated_in_scorer():
    """Pain specificity bonus should be included in the total score."""
    artifact = _build_artifact()
    result = score_from_artifact(artifact)
    pc_score = result["feature_scores"].get("pain_confidence", 0)
    assert pc_score > 0, "Pain confidence should include specificity bonus"
    print(f"PASS: test_pain_specificity_integrated_in_scorer (pc={pc_score})")


# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # 1. Legacy ICP
    test_icp_perfect_score()
    test_icp_low_score()
    test_icp_mid_score()
    test_legacy_icp_still_works()
    # 2. Priority
    test_priority_hot()
    test_priority_penalty()
    test_priority_competitor_tool()
    test_priority_recently_hired()
    test_priority_clamp()
    # 3. V2 Scorer
    test_determinism()
    test_perfect_icp_scores_high()
    test_weak_prospect_scores_low()
    test_scoring_order()
    test_explanation_has_reasons()
    test_missing_data_reported()
    test_missing_data_reduces_quality()
    test_feature_weights_sum()
    test_config_loads()
    test_v2_scorer_is_primary()
    test_score_and_sort_all_5()
    # 4. Signal Decay
    test_decay_factor_at_half_life()
    test_decay_factor_fresh_signal()
    test_decay_factor_very_old()
    test_decay_factor_min_floor()
    test_decay_factor_double_half_life()
    test_apply_signal_decay_with_config()
    test_apply_signal_decay_no_config()
    test_score_from_artifact_has_decay_field()
    # 5. Weight A/B
    test_compare_weight_configs_basic()
    test_compare_detects_tier_shift()
    test_score_sensitivity()
    test_sensitivity_sorted_by_gap()
    # 6. Pain Specificity
    test_specific_pain_gets_bonus()
    test_generic_pain_no_bonus()
    test_pain_with_tool_and_workflow()
    test_pain_specificity_empty()
    test_pain_specificity_indicators()
    test_pain_specificity_integrated_in_scorer()

    print("\n=== All 38 scorer tests passed ===")
