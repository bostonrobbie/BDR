"""
Unit tests for ICP scoring and priority scoring engines.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.agents.scorer import compute_icp_score
from src.db.models import compute_priority_score


def test_icp_perfect_score():
    """Director of QA at a mid-size fintech with buyer intent should score high."""
    contact = {"title": "Director of Quality Engineering", "seniority_level": "director"}
    account = {"industry": "FinTech", "employee_count": 500, "employee_band": "201-500", "buyer_intent": 1}
    scores = compute_icp_score(contact, account)
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
    assert scores["title_match"] == 2  # VP Engineering = secondary
    assert scores["vertical_match"] == 2  # SaaS
    assert scores["seniority_fit"] == 2  # VP
    assert scores["buyer_intent_bonus"] == 0
    assert 5 <= scores["total_score"] <= 8
    print("PASS: test_icp_mid_score")


def test_priority_hot():
    """Buyer intent + QA title + top vertical = priority 5."""
    contact = {"title": "Head of QA", "recently_hired": 0}
    account = {"buyer_intent": 1, "industry": "fintech", "employee_count": 1000, "known_tools": "[]"}
    result = compute_priority_score(contact, account)
    assert result["score"] == 4 or result["score"] == 5  # buyer(2) + qa(1) + vertical(1) = 4
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
    # Max everything
    contact = {"title": "Director of QA", "recently_hired": 1}
    account = {"buyer_intent": 1, "industry": "fintech", "employee_count": 500, "known_tools": '["Selenium"]'}
    result = compute_priority_score(contact, account)
    assert result["score"] <= 5, f"Score {result['score']} exceeds max 5"
    assert result["score"] >= 1, f"Score {result['score']} below min 1"
    print(f"PASS: test_priority_clamp (score={result['score']})")


if __name__ == "__main__":
    test_icp_perfect_score()
    test_icp_low_score()
    test_icp_mid_score()
    test_priority_hot()
    test_priority_penalty()
    test_priority_competitor_tool()
    test_priority_recently_hired()
    test_priority_clamp()
    print("\n=== All 8 scoring tests passed ===")
