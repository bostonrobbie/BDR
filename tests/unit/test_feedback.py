"""
Unit tests for the feedback tracker.

Sections:
  1. Core feedback recording and stats
  2. Reply sentiment scoring (C9)
  3. Research contradiction detection (C10)
  4. Full-funnel attribution (C8)
"""

import sys
import os
import sqlite3
import json
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

# Set up temp DB before importing modules that use it
_tmpdb = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["OCC_DB_PATH"] = _tmpdb.name
os.environ["OCC_JOURNAL_MODE"] = "DELETE"

from src.db.init_db import init_db, SCHEMA_SQL
init_db(_tmpdb.name)

from src.db import models
from src.agents.feedback_tracker import (
    record_reply,
    record_meeting,
    get_conversion_stats,
    get_winning_patterns,
    get_proof_point_preference,
    generate_feedback_report,
    score_reply_sentiment,
    detect_contradictions_in_reply,
    get_full_funnel_attribution,
    get_attribution_summary,
    record_research_correction,
    get_research_corrections,
    _safe_rate,
    _breakdown,
)
from src.agents.researcher import build_research_artifact
from datetime import datetime


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


# ─── SEED DATA ────────────────────────────────────────────────

def _seed_test_data():
    """Seed test database with realistic outreach data."""
    acc = models.create_account({
        "name": "TestCo", "industry": "FinTech",
        "employee_band": "201-500",
    })

    contacts = []
    for i in range(10):
        c = models.create_contact({
            "account_id": acc["id"],
            "first_name": f"Contact{i}",
            "last_name": f"Test{i}",
            "title": "QA Manager",
        })
        contacts.append(c)

    proof_points = ["cred_coverage", "hansard_regression", "medibuddy_scale",
                    "spendflo_roi", "selenium_maintenance"]
    conn = models.get_db()

    drafts = []
    for i, c in enumerate(contacts):
        pp = proof_points[i % len(proof_points)]
        draft_id = models.gen_id("msg")
        conn.execute("""
            INSERT INTO message_drafts (id, contact_id, channel, touch_number,
                touch_type, body, proof_point_used, pain_hook, opener_style,
                ask_style, ab_group, ab_variable, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,datetime('now'))
        """, (
            draft_id, c["id"], "linkedin", 1, "inmail",
            f"Test message body {i}", pp,
            "test maintenance", "career_reference",
            "15_min_compare",
            "A" if i < 5 else "B", "proof_point",
        ))
        drafts.append(draft_id)

    conn.commit()

    tp_ids = []
    for i, (c, draft_id) in enumerate(zip(contacts, drafts)):
        tp_id = models.gen_id("tp")
        conn.execute("""
            INSERT INTO touchpoints (id, contact_id, message_draft_id, channel,
                touch_number, sent_at, outcome, created_at)
            VALUES (?,?,?,?,?,datetime('now'),?,datetime('now'))
        """, (
            tp_id, c["id"], draft_id, "linkedin", 1, "sent",
        ))
        tp_ids.append(tp_id)

    conn.commit()
    conn.close()

    return {
        "account": acc,
        "contacts": contacts,
        "drafts": drafts,
        "touchpoints": tp_ids,
    }


_test_data = _seed_test_data()


# ═══════════════════════════════════════════════════════════════
# 1. CORE FEEDBACK RECORDING & STATS
# ═══════════════════════════════════════════════════════════════

def test_safe_rate():
    """Rate computation should handle zero denominators."""
    assert _safe_rate(5, 10) == 0.5
    assert _safe_rate(0, 10) == 0.0
    assert _safe_rate(5, 0) == 0.0
    assert _safe_rate(0, 0) == 0.0
    print("PASS: test_safe_rate")


def test_record_reply_basic():
    """Should record a reply and return attribution."""
    contact = _test_data["contacts"][0]
    tp_id = _test_data["touchpoints"][0]

    result = record_reply(
        contact_id=contact["id"],
        touchpoint_id=tp_id,
        channel="linkedin",
        intent="positive",
        reply_tag="interested",
        summary="Interested in a demo",
    )

    assert result["reply_id"], "Should return a reply_id"
    assert result["attribution"]["channel"] == "linkedin"
    assert result["attribution"]["touch_number"] == 1
    assert result["attribution"]["proof_point_used"] is not None
    print("PASS: test_record_reply_basic")


def test_record_reply_without_touchpoint():
    """Should handle reply without explicit touchpoint."""
    contact = _test_data["contacts"][1]

    result = record_reply(
        contact_id=contact["id"],
        channel="email",
        intent="neutral",
        summary="Auto-reply",
    )

    assert result["reply_id"]
    print("PASS: test_record_reply_without_touchpoint")


def test_record_multiple_replies():
    """Should handle multiple replies with different intents."""
    for i in range(2, 6):
        contact = _test_data["contacts"][i]
        tp_id = _test_data["touchpoints"][i]
        intent = "positive" if i % 2 == 0 else "negative"

        result = record_reply(
            contact_id=contact["id"],
            touchpoint_id=tp_id,
            intent=intent,
            reply_tag="interested" if intent == "positive" else "not_now",
            summary=f"Reply from contact {i}",
        )
        assert result["reply_id"]

    print("PASS: test_record_multiple_replies")


def test_record_meeting():
    """Should record a meeting with full attribution."""
    contact = _test_data["contacts"][0]
    tp_id = _test_data["touchpoints"][0]

    result = record_meeting(
        contact_id=contact["id"],
        trigger_touchpoint_id=tp_id,
        pipeline_value=25000.0,
        ae_name="Test AE",
        notes="Demo scheduled",
    )

    assert result["opportunity_id"]
    assert result["attribution"]["channel"] == "linkedin"
    assert result["attribution"]["proof_point_used"] is not None
    print("PASS: test_record_meeting")


def test_conversion_stats():
    """Should compute conversion stats from recorded data."""
    stats = get_conversion_stats(days=90)

    assert stats["totals"]["touches_sent"] == 10, \
        f"Should have 10 touches: {stats['totals']['touches_sent']}"
    assert stats["totals"]["replies_received"] > 0, \
        f"Should have replies: {stats['totals']['replies_received']}"
    assert stats["totals"]["meetings_booked"] >= 1, \
        f"Should have at least 1 meeting: {stats['totals']['meetings_booked']}"

    assert 0 <= stats["totals"]["reply_rate"] <= 1
    assert 0 <= stats["totals"]["positive_rate"] <= 1
    assert 0 <= stats["totals"]["meeting_rate"] <= 1

    print("PASS: test_conversion_stats")


def test_proof_point_breakdown():
    """Stats should break down by proof point."""
    stats = get_conversion_stats(days=90)
    by_pp = stats["by_proof_point"]

    assert len(by_pp) > 0, "Should have proof point breakdown"
    for pp_key, data in by_pp.items():
        assert "sent" in data
        assert "replied" in data
        assert "positive" in data
        assert "reply_rate" in data
        assert "positive_rate" in data
        assert data["sent"] > 0, f"'{pp_key}' should have at least 1 sent"

    print("PASS: test_proof_point_breakdown")


def test_channel_breakdown():
    """Stats should break down by channel."""
    stats = get_conversion_stats(days=90)
    by_ch = stats["by_channel"]

    assert "linkedin" in by_ch, f"Should have linkedin channel: {by_ch.keys()}"
    assert by_ch["linkedin"]["sent"] > 0
    print("PASS: test_channel_breakdown")


def test_winning_patterns():
    """Should identify winning patterns with sufficient data."""
    patterns = get_winning_patterns(min_sample_size=1, days=90)

    assert "recommendations" in patterns
    assert "sample_size" in patterns
    assert patterns["sample_size"] == 10
    assert patterns["confidence"] in ("high", "medium", "low")
    assert "stats" in patterns

    print("PASS: test_winning_patterns")


def test_proof_point_preference():
    """Should return a proof point preference when data exists."""
    pref = get_proof_point_preference(min_sample=1, days=90)
    print(f"  Proof point preference: {pref}")
    print("PASS: test_proof_point_preference")


def test_feedback_report():
    """Should generate a readable feedback report."""
    report = generate_feedback_report(days=90)

    assert "OUTREACH PERFORMANCE REPORT" in report
    assert "Total touches" in report
    assert "Replies" in report
    assert "Meetings booked" in report
    assert "PROOF POINT PERFORMANCE" in report
    assert "CHANNEL PERFORMANCE" in report

    print("PASS: test_feedback_report")


def test_empty_database_stats():
    """Stats should handle empty data gracefully."""
    stats = get_conversion_stats(days=0)

    assert stats["totals"]["touches_sent"] == 0
    assert stats["totals"]["reply_rate"] == 0.0
    assert stats["period_days"] == 0
    print("PASS: test_empty_database_stats")


def test_ab_group_breakdown():
    """Stats should break down by A/B group."""
    stats = get_conversion_stats(days=90)
    by_ab = stats["by_ab_group"]

    assert len(by_ab) >= 1, f"Should have A/B breakdown: {by_ab.keys()}"
    total_ab_sent = sum(d["sent"] for d in by_ab.values())
    assert total_ab_sent == 10, f"All touches should have AB group: {total_ab_sent}"
    print("PASS: test_ab_group_breakdown")


# ═══════════════════════════════════════════════════════════════
# 2. REPLY SENTIMENT SCORING (C9)
# ═══════════════════════════════════════════════════════════════

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
    assert result["confidence"] <= 0.5, "Low confidence without keyword match"
    print(f"PASS: test_sentiment_with_existing_intent (score={result['sentiment_score']})")


def test_sentiment_confidence_scales():
    """More keywords matched should increase confidence."""
    short = score_reply_sentiment("Yes")
    long = score_reply_sentiment("Yes, let's schedule a call. I'm interested in learning more.")
    assert long["confidence"] >= short["confidence"], \
        f"Longer reply should have higher confidence: {long['confidence']} vs {short['confidence']}"
    print("PASS: test_sentiment_confidence_scales")


# ═══════════════════════════════════════════════════════════════
# 3. RESEARCH CONTRADICTION DETECTION (C10)
# ═══════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════
# 4. FULL-FUNNEL ATTRIBUTION (C8)
# ═══════════════════════════════════════════════════════════════

def test_attribution_summary_structure():
    """Attribution summary should have expected structure."""
    result = get_attribution_summary(days=90)
    assert "meeting_attribution" in result
    assert "total_meetings" in result
    assert "by_proof_point" in result["meeting_attribution"]
    assert "by_channel" in result["meeting_attribution"]
    assert "by_touch_number" in result["meeting_attribution"]
    print("PASS: test_attribution_summary_structure")


def test_full_funnel_chain_structure():
    """Full funnel chain should have expected structure."""
    result = get_full_funnel_attribution("nonexistent_contact")
    assert "contact_id" in result
    assert "chain" in result
    assert "outcome" in result
    assert "winning_attributes" in result
    assert result["outcome"] == "no_outcome"
    print("PASS: test_full_funnel_chain_structure")


# ═══════════════════════════════════════════════════════════════

def _cleanup():
    """Clean up temp database."""
    try:
        os.unlink(_tmpdb.name)
    except Exception:
        pass


if __name__ == "__main__":
    try:
        # 1. Core
        test_safe_rate()
        test_record_reply_basic()
        test_record_reply_without_touchpoint()
        test_record_multiple_replies()
        test_record_meeting()
        test_conversion_stats()
        test_proof_point_breakdown()
        test_channel_breakdown()
        test_winning_patterns()
        test_proof_point_preference()
        test_feedback_report()
        test_empty_database_stats()
        test_ab_group_breakdown()
        # 2. Sentiment
        test_strong_positive_sentiment()
        test_mild_positive_sentiment()
        test_neutral_sentiment()
        test_mild_negative_sentiment()
        test_strong_negative_sentiment()
        test_referral_sentiment()
        test_empty_reply_sentiment()
        test_sentiment_with_existing_intent()
        test_sentiment_confidence_scales()
        # 3. Contradictions
        test_detect_tool_negation()
        test_detect_tool_switch()
        test_detect_wrong_person()
        test_no_contradictions_positive_reply()
        test_contradiction_confidence()
        # 4. Attribution
        test_attribution_summary_structure()
        test_full_funnel_chain_structure()

        print("\n=== All 29 feedback tests passed ===")
    finally:
        _cleanup()
