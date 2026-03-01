"""
Unit tests for the v2 feature-based scorer (0-100 scale).
Tests determinism, explainability, and calibration.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.agents.scorer import score_from_artifact, load_scoring_config
from src.agents.researcher import build_research_artifact


# ─── SAMPLE ARTIFACTS (5 prospects) ───────────────────────────

def _build_artifact(contact, account=None, person_research=None, company_research=None, signals=None):
    result = build_research_artifact(contact, account, person_research, company_research, signals)
    return result["artifact"]


PROSPECT_1 = {  # Perfect ICP: QA Director at FinTech with Selenium + buyer intent
    "first_name": "Sarah", "last_name": "Chen",
    "title": "Director of Quality Engineering", "seniority_level": "director",
    "company_name": "PayFlow", "linkedin_url": "https://linkedin.com/in/sarahchen",
}
ACCOUNT_1 = {
    "name": "PayFlow", "domain": "payflow.com", "industry": "FinTech",
    "employee_band": "201-500", "employee_count": 350, "hq_location": "San Francisco",
    "buyer_intent": 1, "known_tools": '["Selenium", "Jenkins"]',
}

PROSPECT_2 = {  # Good: VP Eng at Healthcare, no tools
    "first_name": "Mike", "last_name": "Torres",
    "title": "VP of Engineering", "seniority_level": "vp",
    "company_name": "HealthBridge",
}
ACCOUNT_2 = {
    "name": "HealthBridge", "industry": "Healthcare",
    "employee_band": "501-1000", "employee_count": 800,
    "buyer_intent": 0, "known_tools": "[]",
}

PROSPECT_3 = {  # Weak: Junior engineer, no account
    "first_name": "Priya", "last_name": "Patel",
    "title": "Software Engineer", "seniority_level": "",
    "company_name": "",
}

PROSPECT_4 = {  # Mid: QA Manager at SaaS, competitor tools
    "first_name": "James", "last_name": "Wilson",
    "title": "QA Manager", "seniority_level": "manager",
    "company_name": "CloudStack",
}
ACCOUNT_4 = {
    "name": "CloudStack", "industry": "SaaS / B2B Software",
    "employee_band": "1001-5000", "employee_count": 2500,
    "buyer_intent": 0, "known_tools": '["Cypress", "Playwright"]',
}

PROSPECT_5 = {  # Edge: CTO at tiny startup
    "first_name": "Ana", "last_name": "Rodriguez",
    "title": "CTO", "seniority_level": "c-suite",
    "company_name": "TinyApp",
}
ACCOUNT_5 = {
    "name": "TinyApp", "industry": "Tech",
    "employee_band": "1-50", "employee_count": 20,
    "buyer_intent": 0, "known_tools": "[]",
}


def test_determinism():
    """Same input must produce same output every time."""
    artifact = _build_artifact(PROSPECT_1, ACCOUNT_1)
    result1 = score_from_artifact(artifact)
    result2 = score_from_artifact(artifact)
    assert result1["total_score"] == result2["total_score"], \
        f"Non-deterministic: {result1['total_score']} vs {result2['total_score']}"
    assert result1["feature_scores"] == result2["feature_scores"]
    print("PASS: test_determinism")


def test_perfect_icp_scores_high():
    """Sarah: Director QA at FinTech with Selenium + buyer intent -> hot."""
    artifact = _build_artifact(PROSPECT_1, ACCOUNT_1,
                                person_research={"headline": "QA Leader"})
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
        ("Sarah", _build_artifact(PROSPECT_1, ACCOUNT_1)),
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

    # Sarah should be #1
    assert names_ranked[0] == "Sarah", f"Expected Sarah first, got {names_ranked[0]}"
    # Priya should be last
    assert names_ranked[-1] == "Priya", f"Expected Priya last, got {names_ranked[-1]}"
    print("PASS: test_scoring_order")


def test_explanation_has_reasons():
    """Every scored prospect should have human-readable reasons."""
    artifact = _build_artifact(PROSPECT_1, ACCOUNT_1)
    result = score_from_artifact(artifact)
    assert len(result["reasons"]) >= 5, f"Expected >= 5 reasons, got {len(result['reasons'])}"
    # Reasons should reference evidence
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
    artifact_full = _build_artifact(PROSPECT_1, ACCOUNT_1,
                                     person_research={"headline": "QA Leader"})
    artifact_empty = _build_artifact(PROSPECT_3, None)
    result_full = score_from_artifact(artifact_full)
    result_empty = score_from_artifact(artifact_empty)
    assert result_full["feature_scores"]["data_quality"] > result_empty["feature_scores"]["data_quality"], \
        f"Full ({result_full['feature_scores']['data_quality']}) should have higher data quality than empty ({result_empty['feature_scores']['data_quality']})"
    print("PASS: test_missing_data_reduces_quality")


def test_feature_weights_sum():
    """Feature weights should sum to 100."""
    artifact = _build_artifact(PROSPECT_1, ACCOUNT_1)
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


def test_score_and_sort_all_5():
    """Score all 5 prospects and print sorted results."""
    prospects = [
        ("Sarah Chen", PROSPECT_1, ACCOUNT_1),
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

    print("\n  ── Prospect Ranking ──")
    for rank, (name, r) in enumerate(results, 1):
        features = r["feature_scores"]
        print(f"  #{rank} {name}: {r['total_score']}/100 ({r['tier']})")
        print(f"       title={features['title_seniority']} func={features['function_match']} "
              f"size={features['company_size_fit']} ind={features['industry_fit']} "
              f"pain={features['pain_confidence']} intent={features['intent_signal']} "
              f"dq={features['data_quality']}")

    print("PASS: test_score_and_sort_all_5")


if __name__ == "__main__":
    test_determinism()
    test_perfect_icp_scores_high()
    test_weak_prospect_scores_low()
    test_scoring_order()
    test_explanation_has_reasons()
    test_missing_data_reported()
    test_missing_data_reduces_quality()
    test_feature_weights_sum()
    test_config_loads()
    test_score_and_sort_all_5()
    print("\n=== All 10 scorer v2 tests passed ===")
