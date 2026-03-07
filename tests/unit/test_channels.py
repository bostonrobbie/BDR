"""
Unit tests for channel rendering and LinkedIn optimization.

Sections:
  1. LinkedIn preview scoring
  2. Greeting stripping and truncation
  3. LinkedIn length checks
  4. Channel-specific rendering
  5. Feedback-informed proof point selection
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
from src.agents.linkedin_optimizer import (
    score_preview,
    check_linkedin_length,
    optimize_for_preview,
    rank_variants_by_preview,
    _strip_greeting,
    _check_truncation,
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


# ─── SAMPLE MESSAGES ──────────────────────────────────────────

GOOD_MESSAGE = """Hi Sarah,

Your work leading QA at PayFlow stood out. Keeping Selenium suites stable while shipping fast is a grind most FinTech teams know well - CRED hit 90% regression automation and 5x faster execution.

Happy to show you what that'd look like against your Selenium setup - 15 minutes, tops.

Cheers,
Rob Gorham"""

WEAK_MESSAGE = """Hi Sarah,

I hope this message finds you well. I wanted to reach out because I think our product might be interesting for your team.

We help companies with test automation. Would you like to chat?

Best,
Rob"""

QUESTION_OPENER = """Hi Mike,

Curious about how HealthBridge handles test automation at scale - how do you keep regression cycles short when compliance requires full coverage before every release?

Sanofi went from 3-day regression to 80 minutes. Worth exploring?

Best,
Rob Gorham"""

SHORT_MESSAGE = """Hi James,

Checking in.

Best,
Rob"""


# ═══════════════════════════════════════════════════════════════
# 1. LINKEDIN PREVIEW SCORING
# ═══════════════════════════════════════════════════════════════

def test_good_opener_scores_well():
    """A specific, personalized opener should score >= 6."""
    result = score_preview(GOOD_MESSAGE, "Sarah")
    assert result["score"] >= 6, f"Good opener should score >= 6, got {result['score']}"
    assert result["rating"] in ("good", "excellent")
    print(f"PASS: test_good_opener_scores_well (score={result['score']})")


def test_weak_opener_scores_low():
    """A generic 'hope this finds you well' opener should score low."""
    result = score_preview(WEAK_MESSAGE, "Sarah")
    assert result["score"] <= 5, f"Weak opener should score <= 5, got {result['score']}"
    assert len(result["issues"]) > 0, "Should flag issues"
    print(f"PASS: test_weak_opener_scores_low (score={result['score']}, issues={result['issues']})")


def test_question_opener_gets_bonus():
    """Question-based opener should get curiosity bonus."""
    result = score_preview(QUESTION_OPENER, "Mike")
    assert result["score"] >= 6, f"Question opener should score well: {result['score']}"
    print(f"PASS: test_question_opener_gets_bonus (score={result['score']})")


def test_short_preview_penalized():
    """Very short previews should be penalized."""
    result = score_preview(SHORT_MESSAGE, "James")
    assert result["score"] <= 5, f"Short preview should score low: {result['score']}"
    assert any("short" in issue.lower() for issue in result["issues"]), \
        f"Should flag shortness: {result['issues']}"
    print(f"PASS: test_short_preview_penalized (score={result['score']})")


def test_preview_text_excludes_greeting():
    """Preview text should start after 'Hi Name,' greeting."""
    result = score_preview(GOOD_MESSAGE, "Sarah")
    assert not result["preview_text"].lower().startswith("hi sarah"), \
        f"Preview should not start with greeting: {result['preview_text'][:30]}"
    print(f"PASS: test_preview_text_excludes_greeting (preview='{result['preview_text'][:50]}...')")


def test_preview_chars_within_limit():
    """Preview text should be <= 100 chars."""
    result = score_preview(GOOD_MESSAGE, "Sarah")
    assert result["preview_chars"] <= 100, \
        f"Preview should be <= 100 chars: {result['preview_chars']}"
    print(f"PASS: test_preview_chars_within_limit ({result['preview_chars']} chars)")


# ═══════════════════════════════════════════════════════════════
# 2. GREETING STRIPPING & TRUNCATION
# ═══════════════════════════════════════════════════════════════

def test_strip_hi_greeting():
    """Should strip 'Hi Name,' and blank line."""
    result = _strip_greeting("Hi Sarah,\n\nYour work leading QA...", "Sarah")
    assert result.startswith("Your work"), f"Should start with content: '{result[:30]}'"
    print("PASS: test_strip_hi_greeting")


def test_strip_hey_greeting():
    """Should strip 'Hey Name,' greeting."""
    result = _strip_greeting("Hey Mike,\n\nSomething here.", "Mike")
    assert result.startswith("Something"), f"Should start with content: '{result[:30]}'"
    print("PASS: test_strip_hey_greeting")


def test_no_greeting_passthrough():
    """Message without greeting should pass through."""
    content = "Your work at PayFlow stood out."
    result = _strip_greeting(content, "Sarah")
    assert result == content
    print("PASS: test_no_greeting_passthrough")


def test_truncation_mid_word():
    """Should detect mid-word truncation."""
    text = "This is a test of truncation detection capabilities"
    result = _check_truncation(text, 25)
    assert "mid_word" in result
    print("PASS: test_truncation_mid_word")


def test_no_truncation_short_text():
    """Short text should not trigger truncation."""
    result = _check_truncation("Short text.", 100)
    assert not result["mid_word"]
    assert not result["mid_sentence"]
    print("PASS: test_no_truncation_short_text")


def test_truncation_at_space():
    """Truncation at a space should not be mid-word."""
    text = "Hello world this is a test"
    result = _check_truncation(text, 12)
    assert not result["mid_word"]
    print("PASS: test_truncation_at_space")


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


# ═══════════════════════════════════════════════════════════════
# 3. LINKEDIN LENGTH CHECKS
# ═══════════════════════════════════════════════════════════════

def test_inmail_fits():
    """Standard message should fit InMail limit."""
    result = check_linkedin_length(GOOD_MESSAGE, "inmail")
    assert result["fits"], f"Should fit InMail: {result['char_count']}/{result['limit']}"
    assert result["over_by"] == 0
    print(f"PASS: test_inmail_fits ({result['char_count']}/{result['limit']})")


def test_connection_note_too_long():
    """Standard message should exceed connection note limit."""
    result = check_linkedin_length(GOOD_MESSAGE, "connection_note")
    assert not result["fits"], "Full message should not fit connection note"
    assert result["over_by"] > 0
    assert result["limit"] == 300
    print(f"PASS: test_connection_note_too_long (over by {result['over_by']})")


def test_short_fits_all():
    """Short message should fit all formats."""
    short = "Quick question about your QA setup."
    for msg_type in ["inmail", "connection_note", "inmessage"]:
        result = check_linkedin_length(short, msg_type)
        assert result["fits"], f"Short message should fit {msg_type}"
    print("PASS: test_short_fits_all")


def test_optimize_good_message():
    """Good message should pass optimization."""
    result = optimize_for_preview(GOOD_MESSAGE, "Sarah")
    assert result["length"]["fits"]
    assert result["preview"]["score"] >= 5
    print(f"PASS: test_optimize_good_message (optimized={result['optimized']})")


# ═══════════════════════════════════════════════════════════════
# 4. CHANNEL-SPECIFIC RENDERING
# ═══════════════════════════════════════════════════════════════

def test_linkedin_connection_strips_greeting():
    """Connection note should strip 'Hi Name,' greeting."""
    output, artifact = _get_test_output()
    variant = output["variants"][0]

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
    variant = output["variants"][0]

    adapted = render_for_channel(variant, "linkedin_message", artifact)
    body = adapted["body"]

    assert body.startswith("Hey Sarah,"), \
        f"LinkedIn message should start with 'Hey': {body[:30]}"
    assert adapted["subject_lines"] == [], "DM should have no subject lines"
    print("PASS: test_linkedin_message_casual_greeting")


def test_linkedin_message_no_ps():
    """LinkedIn DM should strip P.S. lines."""
    output, artifact = _get_test_output()
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


# ═══════════════════════════════════════════════════════════════
# 5. VARIANT RANKING & FEEDBACK-INFORMED SELECTION
# ═══════════════════════════════════════════════════════════════

def test_rank_variants():
    """Should rank variants by preview score."""
    variants = [
        {"tone": "friendly", "body": GOOD_MESSAGE},
        {"tone": "weak", "body": WEAK_MESSAGE},
        {"tone": "curious", "body": QUESTION_OPENER},
    ]
    ranked = rank_variants_by_preview(variants, "Sarah")

    assert len(ranked) == 3
    scores = [r["preview_score"] for r in ranked]
    assert scores == sorted(scores, reverse=True), \
        f"Should be sorted by score desc: {scores}"
    for r in ranked:
        assert "tone" in r
        assert "preview_score" in r
        assert "preview_text" in r
        assert "rating" in r
    print(f"PASS: test_rank_variants (scores={scores})")


def test_rank_returns_best_first():
    """The best variant should be ranked first."""
    variants = [
        {"tone": "friendly", "body": GOOD_MESSAGE},
        {"tone": "weak", "body": WEAK_MESSAGE},
    ]
    ranked = rank_variants_by_preview(variants, "Sarah")
    assert ranked[0]["tone"] == "friendly", \
        f"Good message should rank first, got: {ranked[0]['tone']}"
    print("PASS: test_rank_returns_best_first")


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
    exclude = all_keys[:-1]
    pp = _select_best_proof_point_with_feedback(artifact, config, exclude_keys=exclude)
    assert pp["key"] not in exclude, f"Should not return excluded key: {pp['key']}"
    print("PASS: test_feedback_proof_point_excludes")


def test_generate_variants_uses_feedback_selection():
    """generate_message_variants should use feedback-informed selection."""
    result = build_research_artifact(CONTACT, ACCOUNT)
    artifact = result["artifact"]
    scoring = score_from_artifact(artifact)

    output = generate_message_variants(artifact, scoring)
    assert len(output["variants"]) == 3
    for v in output["variants"]:
        assert v.get("proof_point_key"), f"Variant should have proof point key"
    print("PASS: test_generate_variants_uses_feedback_selection")


# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # 1. Preview Scoring
    test_good_opener_scores_well()
    test_weak_opener_scores_low()
    test_question_opener_gets_bonus()
    test_short_preview_penalized()
    test_preview_text_excludes_greeting()
    test_preview_chars_within_limit()
    # 2. Greeting / Truncation
    test_strip_hi_greeting()
    test_strip_hey_greeting()
    test_no_greeting_passthrough()
    test_truncation_mid_word()
    test_no_truncation_short_text()
    test_truncation_at_space()
    test_truncate_at_sentence()
    test_truncate_no_op_short()
    test_truncate_at_space()
    # 3. Length Checks
    test_inmail_fits()
    test_connection_note_too_long()
    test_short_fits_all()
    test_optimize_good_message()
    # 4. Channel Rendering
    test_linkedin_connection_strips_greeting()
    test_linkedin_connection_under_300_chars()
    test_linkedin_connection_no_subject()
    test_linkedin_message_casual_greeting()
    test_linkedin_message_no_ps()
    test_linkedin_inmail_has_subject()
    test_email_preserves_structure()
    test_channel_metadata_set()
    test_char_counts_updated()
    # 5. Ranking / Feedback
    test_rank_variants()
    test_rank_returns_best_first()
    test_feedback_proof_point_falls_back()
    test_feedback_proof_point_excludes()
    test_generate_variants_uses_feedback_selection()

    print("\n=== All 33 channel tests passed ===")
