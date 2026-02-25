"""
Unit tests for channel-specific rendering and feedback-informed proof point selection.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.agents.researcher import build_research_artifact
from src.agents.scorer import score_from_artifact
from src.agents.message_writer import (
    generate_message_variants,
    render_for_channel,
    _select_best_proof_point_with_feedback,
    _load_product_config,
    _truncate_cleanly,
)


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


def _get_test_output():
    """Build variants for testing."""
    result = build_research_artifact(CONTACT, ACCOUNT)
    artifact = result["artifact"]
    scoring = score_from_artifact(artifact)
    output = generate_message_variants(artifact, scoring)
    return output, artifact


# ─── CHANNEL RENDERING TESTS ─────────────────────────────────

def test_linkedin_connection_strips_greeting():
    """Connection note should strip 'Hi Name,' greeting."""
    output, artifact = _get_test_output()
    variant = output["variants"][0]  # friendly

    adapted = render_for_channel(variant, "linkedin_connection", artifact)
    body = adapted["body"]

    assert not body.lower().startswith("hi sarah"), \
        f"Connection note should not start with greeting: {body[:30]}"
    assert adapted["channel"] == "linkedin_connection"
    print("PASS: test_linkedin_connection_strips_greeting")


def test_linkedin_connection_under_300_chars():
    """Connection note should be under 300 characters."""
    output, artifact = _get_test_output()
    for variant in output["variants"]:
        adapted = render_for_channel(variant, "linkedin_connection", artifact)
        assert adapted["char_count"] <= 300, \
            f"{variant['tone']} connection note too long: {adapted['char_count']}/300"
    print("PASS: test_linkedin_connection_under_300_chars")


def test_linkedin_connection_no_subject():
    """Connection notes should have no subject lines."""
    output, artifact = _get_test_output()
    variant = output["variants"][0]

    adapted = render_for_channel(variant, "linkedin_connection", artifact)
    assert adapted["subject_lines"] == [], "Connection note should have no subject lines"
    print("PASS: test_linkedin_connection_no_subject")


def test_linkedin_message_casual_greeting():
    """LinkedIn DM should use 'Hey' instead of 'Hi'."""
    output, artifact = _get_test_output()
    variant = output["variants"][0]  # friendly

    adapted = render_for_channel(variant, "linkedin_message", artifact)
    body = adapted["body"]

    assert body.startswith("Hey Sarah,"), \
        f"LinkedIn message should start with 'Hey': {body[:30]}"
    assert adapted["subject_lines"] == [], "DM should have no subject lines"
    print("PASS: test_linkedin_message_casual_greeting")


def test_linkedin_message_no_ps():
    """LinkedIn DM should strip P.S. lines."""
    output, artifact = _get_test_output()
    # Generate email variant which has P.S.
    result = build_research_artifact(CONTACT, ACCOUNT)
    scoring = score_from_artifact(result["artifact"])
    scoring["tier"] = "hot"
    email_output = generate_message_variants(result["artifact"], scoring, channel="email")

    for variant in email_output["variants"]:
        adapted = render_for_channel(variant, "linkedin_message", result["artifact"])
        assert "P.S." not in adapted["body"], \
            f"LinkedIn DM should not have P.S.: {adapted['body'][-50:]}"
    print("PASS: test_linkedin_message_no_ps")


def test_linkedin_inmail_has_subject():
    """LinkedIn InMail should preserve subject lines."""
    output, artifact = _get_test_output()
    variant = output["variants"][0]

    adapted = render_for_channel(variant, "linkedin_inmail", artifact)
    assert len(adapted.get("subject_lines", [])) >= 2, "InMail should have subject lines"
    print("PASS: test_linkedin_inmail_has_subject")


def test_email_preserves_structure():
    """Email rendering should preserve full message structure."""
    output, artifact = _get_test_output()
    variant = output["variants"][0]

    adapted = render_for_channel(variant, "email", artifact)
    assert "Hi Sarah," in adapted["body"], "Email should keep greeting"
    assert len(adapted.get("subject_lines", [])) >= 2, "Email should have subject lines"
    print("PASS: test_email_preserves_structure")


def test_channel_metadata_set():
    """Each channel rendering should set channel_metadata."""
    output, artifact = _get_test_output()
    variant = output["variants"][0]

    for channel in ["linkedin_connection", "linkedin_message", "linkedin_inmail", "email"]:
        adapted = render_for_channel(variant, channel, artifact)
        assert "channel_metadata" in adapted, f"Missing channel_metadata for {channel}"
        assert "format" in adapted["channel_metadata"]
        assert "char_limit" in adapted["channel_metadata"]
    print("PASS: test_channel_metadata_set")


def test_char_counts_updated():
    """Char and word counts should be recalculated after channel adaptation."""
    output, artifact = _get_test_output()
    variant = output["variants"][0]

    adapted = render_for_channel(variant, "linkedin_connection", artifact)
    assert adapted["char_count"] == len(adapted["body"])
    assert adapted["word_count"] == len(adapted["body"].split())
    print("PASS: test_char_counts_updated")


# ─── TRUNCATION TESTS ────────────────────────────────────────

def test_truncate_at_sentence():
    """Should truncate at a sentence boundary."""
    text = "First sentence. Second sentence. Third sentence is longer and goes over."
    result = _truncate_cleanly(text, 40)
    assert result.endswith("."), f"Should end at sentence boundary: '{result}'"
    assert len(result) <= 40
    print("PASS: test_truncate_at_sentence")


def test_truncate_no_op_short():
    """Short text should not be truncated."""
    text = "Short."
    result = _truncate_cleanly(text, 100)
    assert result == text
    print("PASS: test_truncate_no_op_short")


def test_truncate_at_space():
    """If no sentence boundary, should truncate at word boundary."""
    text = "one two three four five six seven eight nine ten eleven twelve thirteen"
    result = _truncate_cleanly(text, 30)
    assert not result.endswith(" "), f"Should not end with space: '{result}'"
    assert len(result) <= 30
    print("PASS: test_truncate_at_space")


# ─── FEEDBACK-INFORMED PROOF POINT TESTS ─────────────────────

def test_feedback_proof_point_falls_back():
    """Without feedback data, should fall back to standard selection."""
    result = build_research_artifact(CONTACT, ACCOUNT)
    artifact = result["artifact"]
    config = _load_product_config()

    pp = _select_best_proof_point_with_feedback(artifact, config)
    assert pp is not None
    assert "key" in pp
    assert pp["key"] in config.get("proof_points", {})
    print(f"PASS: test_feedback_proof_point_falls_back (selected: {pp['key']})")


def test_feedback_proof_point_excludes():
    """Should respect exclude_keys even with feedback."""
    result = build_research_artifact(CONTACT, ACCOUNT)
    artifact = result["artifact"]
    config = _load_product_config()

    all_keys = list(config.get("proof_points", {}).keys())
    # Exclude all but one
    exclude = all_keys[:-1]
    pp = _select_best_proof_point_with_feedback(artifact, config, exclude_keys=exclude)
    assert pp["key"] not in exclude, f"Should not return excluded key: {pp['key']}"
    print("PASS: test_feedback_proof_point_excludes")


def test_generate_variants_uses_feedback_selection():
    """generate_message_variants should use feedback-informed selection."""
    result = build_research_artifact(CONTACT, ACCOUNT)
    artifact = result["artifact"]
    scoring = score_from_artifact(artifact)

    # This should work without errors - the feedback system gracefully
    # falls back when no DB data is available
    output = generate_message_variants(artifact, scoring)
    assert len(output["variants"]) == 3
    for v in output["variants"]:
        assert v.get("proof_point_key"), f"Variant should have proof point key"
    print("PASS: test_generate_variants_uses_feedback_selection")


if __name__ == "__main__":
    test_linkedin_connection_strips_greeting()
    test_linkedin_connection_under_300_chars()
    test_linkedin_connection_no_subject()
    test_linkedin_message_casual_greeting()
    test_linkedin_message_no_ps()
    test_linkedin_inmail_has_subject()
    test_email_preserves_structure()
    test_channel_metadata_set()
    test_char_counts_updated()
    test_truncate_at_sentence()
    test_truncate_no_op_short()
    test_truncate_at_space()
    test_feedback_proof_point_falls_back()
    test_feedback_proof_point_excludes()
    test_generate_variants_uses_feedback_selection()
    print("\n=== All 15 channel rendering + feedback tests passed ===")
