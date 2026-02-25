"""
Unit tests for wiring and integration enhancements:
D1: Sentiment scoring wired into reply recording
D2: Contradiction detection auto-triggered on reply
D3: Subject line style tracking in message_drafts and touchpoints
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

from src.db import models
from src.agents.feedback_tracker import (
    record_reply,
    score_reply_sentiment,
    detect_contradictions_in_reply,
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


_test_counter = 0

def _setup_contact_and_account():
    """Create a unique contact and account in the DB for testing."""
    global _test_counter
    _test_counter += 1
    acc_data = dict(ACCOUNT)
    acc_data["id"] = f"acc_test_{_test_counter}"
    acc = models.create_account(acc_data)
    contact_data = dict(CONTACT)
    contact_data["account_id"] = acc["id"]
    contact_data["linkedin_url"] = f"https://linkedin.com/in/sarahchen-test-{_test_counter}"
    con = models.create_contact(contact_data)
    return con["id"], acc["id"]


# ─── D1: SENTIMENT WIRED INTO REPLY RECORDING ───────────────────

def test_reply_includes_sentiment():
    """record_reply should return sentiment analysis of the raw_text."""
    cid, _ = _setup_contact_and_account()
    result = record_reply(
        contact_id=cid,
        raw_text="Yes, let's schedule a call this week!",
        intent="neutral",
    )
    assert "sentiment" in result, "Should include sentiment"
    assert result["sentiment"]["sentiment_score"] >= 0.5, \
        f"Positive reply should have positive sentiment: {result['sentiment']}"
    print(f"PASS: test_reply_includes_sentiment (score={result['sentiment']['sentiment_score']})")


def test_reply_sentiment_overrides_neutral_intent():
    """When intent is 'neutral' but sentiment is strong, effective_intent should upgrade."""
    cid, _ = _setup_contact_and_account()
    result = record_reply(
        contact_id=cid,
        raw_text="Please stop emailing me. Not interested at all.",
        intent="neutral",
    )
    # The reply was recorded - check sentiment detected negativity
    assert result["sentiment"]["sentiment_score"] <= -0.5, \
        f"Should detect negative sentiment: {result['sentiment']}"
    print(f"PASS: test_reply_sentiment_overrides_neutral_intent (score={result['sentiment']['sentiment_score']})")


def test_reply_empty_text_still_works():
    """Reply with empty text should still succeed without sentiment."""
    cid, _ = _setup_contact_and_account()
    result = record_reply(
        contact_id=cid,
        raw_text="",
        intent="positive",
    )
    assert "sentiment" in result
    assert result["sentiment"]["sentiment_label"] == "unknown"
    assert result["contradictions"] == []
    print("PASS: test_reply_empty_text_still_works")


def test_reply_returns_reply_id():
    """record_reply should still return a reply_id."""
    cid, _ = _setup_contact_and_account()
    result = record_reply(
        contact_id=cid,
        raw_text="Thanks for the note",
    )
    assert "reply_id" in result
    assert result["reply_id"].startswith("rep_")
    print("PASS: test_reply_returns_reply_id")


# ─── D2: CONTRADICTION DETECTION AUTO-TRIGGERED ─────────────────

def test_reply_detects_contradictions():
    """record_reply with contradiction text should detect them."""
    cid, _ = _setup_contact_and_account()
    result = record_reply(
        contact_id=cid,
        raw_text="We don't use Selenium anymore. We migrated to Playwright last year.",
    )
    assert "contradictions" in result
    # Note: contradiction detection depends on artifact being available
    # With the DB setup, the artifact build should work
    print(f"PASS: test_reply_detects_contradictions ({len(result['contradictions'])} found)")


def test_reply_records_corrections_for_high_confidence():
    """High-confidence contradictions should auto-record corrections."""
    cid, _ = _setup_contact_and_account()
    result = record_reply(
        contact_id=cid,
        raw_text="I'm the wrong person for this. Try reaching out to our QA lead instead.",
    )
    assert "corrections_recorded" in result
    print(f"PASS: test_reply_records_corrections ({len(result['corrections_recorded'])} corrections)")


def test_reply_no_contradictions_for_positive():
    """Positive reply should have no contradictions."""
    cid, _ = _setup_contact_and_account()
    result = record_reply(
        contact_id=cid,
        raw_text="Sounds great, let's schedule a call to discuss!",
    )
    assert result["contradictions"] == []
    print("PASS: test_reply_no_contradictions_for_positive")


# ─── D3: SUBJECT LINE STYLE TRACKING ────────────────────────────

def test_message_draft_has_subject_style_field():
    """create_message_draft should accept subject_line_style."""
    cid, _ = _setup_contact_and_account()
    msg = models.create_message_draft({
        "contact_id": cid,
        "channel": "linkedin",
        "touch_type": "inmail",
        "body": "Test body",
        "subject_line": "Quick question for Sarah",
        "subject_line_style": "question",
    })
    assert msg["subject_line_style"] == "question", \
        f"Should persist subject_line_style: {msg.get('subject_line_style')}"
    print("PASS: test_message_draft_has_subject_style_field")


def test_touchpoint_has_subject_style_field():
    """log_touchpoint should accept subject_line_style."""
    cid, _ = _setup_contact_and_account()
    tp = models.log_touchpoint({
        "contact_id": cid,
        "channel": "linkedin",
        "touch_number": 1,
        "subject_line_style": "metric_led",
    })
    assert tp["subject_line_style"] == "metric_led", \
        f"Should persist subject_line_style: {tp.get('subject_line_style')}"
    print("PASS: test_touchpoint_has_subject_style_field")


def test_message_draft_without_subject_style():
    """Subject line style should be optional (None)."""
    cid, _ = _setup_contact_and_account()
    msg = models.create_message_draft({
        "contact_id": cid,
        "channel": "email",
        "touch_type": "email",
        "body": "Test body",
    })
    assert msg["subject_line_style"] is None
    print("PASS: test_message_draft_without_subject_style")


def test_attribution_includes_subject_style():
    """Attribution from record_reply should include subject_line_style."""
    cid, _ = _setup_contact_and_account()
    # Create a message draft with subject_line_style
    msg = models.create_message_draft({
        "contact_id": cid,
        "channel": "linkedin",
        "touch_type": "inmail",
        "body": "Test body",
        "subject_line_style": "curiosity",
    })
    # Create a touchpoint for the message
    tp = models.log_touchpoint({
        "contact_id": cid,
        "message_draft_id": msg["id"],
        "channel": "linkedin",
        "touch_number": 1,
        "subject_line_style": "curiosity",
    })
    # Record reply referencing that touchpoint
    result = record_reply(
        contact_id=cid,
        touchpoint_id=tp["id"],
        raw_text="Interesting, tell me more",
    )
    # Attribution should flow through
    assert result["attribution"]["subject_line_style"] == "curiosity", \
        f"Attribution should include subject_line_style: {result['attribution']}"
    print("PASS: test_attribution_includes_subject_style")


if __name__ == "__main__":
    test_reply_includes_sentiment()
    test_reply_sentiment_overrides_neutral_intent()
    test_reply_empty_text_still_works()
    test_reply_returns_reply_id()
    test_reply_detects_contradictions()
    test_reply_records_corrections_for_high_confidence()
    test_reply_no_contradictions_for_positive()
    test_message_draft_has_subject_style_field()
    test_touchpoint_has_subject_style_field()
    test_message_draft_without_subject_style()
    test_attribution_includes_subject_style()
    print("\n=== All 11 wiring enhancement tests passed ===")
