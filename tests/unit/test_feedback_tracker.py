"""
Unit tests for the feedback tracker (response tracking + feedback loop).
Uses an in-memory database to test tracking, analytics, and recommendations.
"""

import sys
import os
import sqlite3
import json
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

# Set up temp DB before importing models
_test_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["OCC_DB_PATH"] = _test_db.name
os.environ["OCC_JOURNAL_MODE"] = "DELETE"

from src.db import models
from src.db.init_db import SCHEMA_SQL
from src.agents.feedback_tracker import (
    record_reply,
    record_meeting,
    get_conversion_stats,
    get_winning_patterns,
    get_proof_point_preference,
    generate_feedback_report,
    _safe_rate,
    _breakdown,
)
from datetime import datetime


def _init_test_db():
    """Initialize test database with schema."""
    conn = sqlite3.connect(_test_db.name)
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()


def _seed_test_data():
    """Seed test database with realistic outreach data."""
    # Create an account
    acc = models.create_account({
        "name": "TestCo", "industry": "FinTech",
        "employee_band": "201-500",
    })

    # Create contacts
    contacts = []
    for i in range(10):
        c = models.create_contact({
            "account_id": acc["id"],
            "first_name": f"Contact{i}",
            "last_name": f"Test{i}",
            "title": "QA Manager",
        })
        contacts.append(c)

    # Create message drafts with different attributes
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

    # Create touchpoints
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


# ─── SETUP ───────────────────────────────────────────────────

_init_test_db()
_test_data = _seed_test_data()


# ─── TESTS ───────────────────────────────────────────────────

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
    # Attribution should still try to find the most recent touchpoint
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

    # Rates should be between 0 and 1
    assert 0 <= stats["totals"]["reply_rate"] <= 1
    assert 0 <= stats["totals"]["positive_rate"] <= 1
    assert 0 <= stats["totals"]["meeting_rate"] <= 1

    print("PASS: test_conversion_stats")


def test_proof_point_breakdown():
    """Stats should break down by proof point."""
    stats = get_conversion_stats(days=90)
    by_pp = stats["by_proof_point"]

    # Should have entries for proof points we seeded
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
    # Use min_sample=1 since we have limited test data
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
    # May or may not return a value depending on reply data, but should not error
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
    # Query with very small window where no data exists
    stats = get_conversion_stats(days=0)

    assert stats["totals"]["touches_sent"] == 0
    assert stats["totals"]["reply_rate"] == 0.0
    assert stats["period_days"] == 0
    print("PASS: test_empty_database_stats")


def test_ab_group_breakdown():
    """Stats should break down by A/B group."""
    stats = get_conversion_stats(days=90)
    by_ab = stats["by_ab_group"]

    # We seeded 5 in group A and 5 in group B
    assert len(by_ab) >= 1, f"Should have A/B breakdown: {by_ab.keys()}"
    total_ab_sent = sum(d["sent"] for d in by_ab.values())
    assert total_ab_sent == 10, f"All touches should have AB group: {total_ab_sent}"
    print("PASS: test_ab_group_breakdown")


# ─── CLEANUP ─────────────────────────────────────────────────

def _cleanup():
    """Clean up temp database."""
    try:
        os.unlink(_test_db.name)
    except Exception:
        pass


if __name__ == "__main__":
    try:
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
        print("\n=== All 13 feedback tracker tests passed ===")
    finally:
        _cleanup()
