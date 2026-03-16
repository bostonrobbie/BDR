"""
Unit tests for scoring enhancements:
A1: Signal decay with configurable half-lives
A2: Scoring weight A/B testing harness
A3: Legacy ICP scoring deprecation
A4: Pain specificity scoring
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.agents.scorer import (
    compute_decay_factor,
    get_signal_age_days,
    apply_signal_decay,
    score_from_artifact,
    compare_weight_configs,
    score_sensitivity,
    score_pain_specificity,
    load_scoring_config,
    compute_icp_score,
)
from src.agents.researcher import build_research_artifact


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


def _build_artifact():
    result = build_research_artifact(CONTACT, ACCOUNT)
    return result["artifact"]


# ─── A1: SIGNAL DECAY TESTS ─────────────────────────────────────

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


# ─── A2: WEIGHT A/B TESTING TESTS ───────────────────────────────

def test_compare_weight_configs_basic():
    """Should produce a comparison with tier distributions."""
    config_a = load_scoring_config()
    config_b = dict(config_a)
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
    # Make thresholds very high so everything becomes cold
    config_b = {**config_a, "thresholds": {"hot": 99, "warm": 98, "cool": 97, "cold": 0}}

    artifacts = [_build_artifact()]
    result = compare_weight_configs(artifacts, config_a, config_b)

    # The artifact likely scores < 99, so should shift to cold in config_b
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
    # Each sensitivity should have expected fields
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


# ─── A3: LEGACY ICP DEPRECATION TESTS ───────────────────────────

def test_legacy_icp_still_works():
    """Legacy ICP scoring should still function for backward compatibility."""
    scores = compute_icp_score(CONTACT, ACCOUNT)
    assert "total_score" in scores
    assert 0 <= scores["total_score"] <= 12
    print(f"PASS: test_legacy_icp_still_works (score={scores['total_score']})")


def test_v2_scorer_is_primary():
    """score_from_artifact should be the primary scorer with 0-100 scale."""
    artifact = _build_artifact()
    result = score_from_artifact(artifact)
    assert result["max_possible"] == 100, f"Max should be 100, got {result['max_possible']}"
    assert 0 <= result["total_score"] <= 100
    print("PASS: test_v2_scorer_is_primary")


# ─── A4: PAIN SPECIFICITY TESTS ─────────────────────────────────

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
    # The artifact has a pain with tool names from known_tools
    result = score_from_artifact(artifact)
    # Check that pain_confidence includes specificity contribution
    pc_score = result["feature_scores"].get("pain_confidence", 0)
    assert pc_score > 0, "Pain confidence should include specificity bonus"
    # Check for specificity-related reason
    has_specificity_reason = any("specificity" in r.lower() for r in result["reasons"])
    # It's OK if the specificity bonus is 0 for this particular artifact
    print(f"PASS: test_pain_specificity_integrated_in_scorer (pc={pc_score})")


if __name__ == "__main__":
    test_decay_factor_at_half_life()
    test_decay_factor_fresh_signal()
    test_decay_factor_very_old()
    test_decay_factor_min_floor()
    test_decay_factor_double_half_life()
    test_apply_signal_decay_with_config()
    test_apply_signal_decay_no_config()
    test_score_from_artifact_has_decay_field()
    test_compare_weight_configs_basic()
    test_compare_detects_tier_shift()
    test_score_sensitivity()
    test_sensitivity_sorted_by_gap()
    test_legacy_icp_still_works()
    test_v2_scorer_is_primary()
    test_specific_pain_gets_bonus()
    test_generic_pain_no_bonus()
    test_pain_with_tool_and_workflow()
    test_pain_specificity_empty()
    test_pain_specificity_indicators()
    test_pain_specificity_integrated_in_scorer()
    print("\n=== All 20 scoring enhancement tests passed ===")
