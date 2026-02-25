"""
Unit tests for feedback and attribution enhancements:
C8: Full-funnel attribution chain
C9: Reply sentiment granularity (-1 to +1 scale)
C10: Research contradiction feedback loop
"""

import sys
import os
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

# Set up temp DB before importing modules that use it
_tmpdb = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["OCC_DB_PATH"] = _tmpdb.name
os.environ["OCC_JOURNAL_MODE"] = "DELETE"

from src.db.init_db import init_db
init_db(_tmpdb.name)

from src.agents.feedback_tracker import (
    score_reply_sentiment,
    detect_contradictions_in_reply,
    get_full_funnel_attribution,
    get_attribution_summary,
    record_research_correction,
    get_research_corrections,
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


# ─── C9: REPLY SENTIMENT TESTS ──────────────────────────────────

def test_strong_positive_sentiment():
    """'Let's schedule a call' should score very positive."""
    result = score_reply_sentiment("Yes, let's schedule a call this week!")
    assert result["sentiment_score"] >= 0.7, \
        f"Strong positive should score >= 0.7: {result['sentiment_score']}"
    assert result["sentiment_label"] == "very_positive"
    assert result["action"] == "schedule_meeting"
    print(f"PASS: test_strong_positive_sentiment (score={result['sentiment_score']})")


def test_mild_positive_sentiment():
    """'Tell me more' should score mildly positive."""
    result = score_reply_sentiment("Interesting, can you send me more info?")
    assert 0.2 <= result["sentiment_score"] <= 0.8, \
        f"Mild positive should be 0.2-0.8: {result['sentiment_score']}"
    assert result["action"] in ("send_more_info", "schedule_meeting")
    print(f"PASS: test_mild_positive_sentiment (score={result['sentiment_score']})")


def test_neutral_sentiment():
    """'Thanks, noted' should score neutral."""
    result = score_reply_sentiment("Thanks for reaching out, noted.")
    assert -0.3 <= result["sentiment_score"] <= 0.3, \
        f"Neutral should be near 0: {result['sentiment_score']}"
    print(f"PASS: test_neutral_sentiment (score={result['sentiment_score']})")


def test_mild_negative_sentiment():
    """'Not the right time' should score mildly negative."""
    result = score_reply_sentiment("Not the right time for us, maybe later.")
    assert result["sentiment_score"] <= -0.2, \
        f"Mild negative should be <= -0.2: {result['sentiment_score']}"
    assert result["action"] in ("pause_sequence", "follow_up_later")
    print(f"PASS: test_mild_negative_sentiment (score={result['sentiment_score']})")


def test_strong_negative_sentiment():
    """'Please stop contacting me' should score very negative."""
    result = score_reply_sentiment("Not interested. Please stop emailing me.")
    assert result["sentiment_score"] <= -0.7, \
        f"Strong negative should be <= -0.7: {result['sentiment_score']}"
    assert result["sentiment_label"] == "very_negative"
    assert result["action"] == "mark_dnc"
    print(f"PASS: test_strong_negative_sentiment (score={result['sentiment_score']})")


def test_referral_sentiment():
    """Referral should be detected as mildly positive."""
    result = score_reply_sentiment("I'm not the right person, but try reaching out to my colleague John.")
    assert result["sentiment_score"] >= 0.0, \
        f"Referral should be >= 0: {result['sentiment_score']}"
    assert result["suggested_intent"] in ("referral", "positive")
    print(f"PASS: test_referral_sentiment (score={result['sentiment_score']})")


def test_empty_reply_sentiment():
    """Empty reply should return unknown."""
    result = score_reply_sentiment("")
    assert result["sentiment_label"] == "unknown"
    assert result["action"] == "review_manually"
    print("PASS: test_empty_reply_sentiment")


def test_sentiment_with_existing_intent():
    """Should use existing intent as fallback when no keywords match."""
    result = score_reply_sentiment("Hmm ok", existing_intent="positive")
    # Even without matching keywords, should use the intent hint
    assert result["confidence"] <= 0.5, "Low confidence without keyword match"
    print(f"PASS: test_sentiment_with_existing_intent (score={result['sentiment_score']})")


def test_sentiment_confidence_scales():
    """More keywords matched should increase confidence."""
    short = score_reply_sentiment("Yes")
    long = score_reply_sentiment("Yes, let's schedule a call. I'm interested in learning more.")
    assert long["confidence"] >= short["confidence"], \
        f"Longer reply should have higher confidence: {long['confidence']} vs {short['confidence']}"
    print("PASS: test_sentiment_confidence_scales")


# ─── C10: RESEARCH CONTRADICTION TESTS ──────────────────────────

def test_detect_tool_negation():
    """'We don't use Selenium' should flag tech_stack contradiction."""
    artifact = _build_artifact()
    contradictions = detect_contradictions_in_reply(
        "Thanks for the note, but we don't use Selenium anymore. We migrated to Playwright.",
        artifact)
    assert len(contradictions) >= 1, f"Should detect contradiction: {contradictions}"
    tool_contradiction = next(
        (c for c in contradictions if c["field"] == "tech_stack"), None)
    assert tool_contradiction is not None, "Should have tech_stack contradiction"
    print(f"PASS: test_detect_tool_negation ({len(contradictions)} contradictions)")


def test_detect_tool_switch():
    """'We actually use Playwright' should flag different tool."""
    artifact = _build_artifact()
    contradictions = detect_contradictions_in_reply(
        "We're actually using Playwright, not Selenium.",
        artifact)
    has_switch = any(
        "playwright" in c.get("reply_suggests", "").lower()
        for c in contradictions)
    assert has_switch, f"Should detect tool switch: {contradictions}"
    print("PASS: test_detect_tool_switch")


def test_detect_wrong_person():
    """'Wrong person' should flag role_fit contradiction."""
    artifact = _build_artifact()
    contradictions = detect_contradictions_in_reply(
        "I'm the wrong person for this. Try reaching out to our QA lead instead.",
        artifact)
    role_contradiction = next(
        (c for c in contradictions if c["field"] == "role_fit"), None)
    assert role_contradiction is not None, "Should detect role_fit contradiction"
    print("PASS: test_detect_wrong_person")


def test_no_contradictions_positive_reply():
    """Positive reply without contradictions should return empty list."""
    artifact = _build_artifact()
    contradictions = detect_contradictions_in_reply(
        "Sounds interesting! Let's schedule a call to discuss.",
        artifact)
    assert len(contradictions) == 0, f"Should have no contradictions: {contradictions}"
    print("PASS: test_no_contradictions_positive_reply")


def test_contradiction_confidence():
    """Contradictions should have a confidence score."""
    artifact = _build_artifact()
    contradictions = detect_contradictions_in_reply(
        "We stopped using Selenium last year.",
        artifact)
    for c in contradictions:
        assert "confidence" in c
        assert 0 <= c["confidence"] <= 1.0
    print("PASS: test_contradiction_confidence")


# ─── C8: FULL-FUNNEL ATTRIBUTION TESTS ──────────────────────────

def test_attribution_summary_structure():
    """Attribution summary should have expected structure."""
    # This tests the function runs without error (no DB data needed)
    result = get_attribution_summary(days=90)
    assert "meeting_attribution" in result
    assert "total_meetings" in result
    assert "by_proof_point" in result["meeting_attribution"]
    assert "by_channel" in result["meeting_attribution"]
    assert "by_touch_number" in result["meeting_attribution"]
    print("PASS: test_attribution_summary_structure")


def test_full_funnel_chain_structure():
    """Full funnel chain should have expected structure."""
    # This returns empty chain for non-existent contact (graceful handling)
    result = get_full_funnel_attribution("nonexistent_contact")
    assert "contact_id" in result
    assert "chain" in result
    assert "outcome" in result
    assert "winning_attributes" in result
    assert result["outcome"] == "no_outcome"
    print("PASS: test_full_funnel_chain_structure")


if __name__ == "__main__":
    test_strong_positive_sentiment()
    test_mild_positive_sentiment()
    test_neutral_sentiment()
    test_mild_negative_sentiment()
    test_strong_negative_sentiment()
    test_referral_sentiment()
    test_empty_reply_sentiment()
    test_sentiment_with_existing_intent()
    test_sentiment_confidence_scales()
    test_detect_tool_negation()
    test_detect_tool_switch()
    test_detect_wrong_person()
    test_no_contradictions_positive_reply()
    test_contradiction_confidence()
    test_attribution_summary_structure()
    test_full_funnel_chain_structure()
    print("\n=== All 16 feedback enhancement tests passed ===")
