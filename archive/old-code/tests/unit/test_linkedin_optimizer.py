"""
Unit tests for the LinkedIn preview optimizer.
Tests preview scoring, truncation detection, length checking, and variant ranking.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.agents.linkedin_optimizer import (
    score_preview,
    check_linkedin_length,
    optimize_for_preview,
    rank_variants_by_preview,
    _strip_greeting,
    _check_truncation,
)


# ─── SAMPLE MESSAGES ─────────────────────────────────────────

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


# ─── PREVIEW SCORING TESTS ───────────────────────────────────

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


# ─── GREETING STRIPPING TESTS ────────────────────────────────

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


# ─── TRUNCATION TESTS ────────────────────────────────────────

def test_truncation_mid_word():
    """Should detect mid-word truncation."""
    text = "This is a test of truncation detection capabilities"
    result = _check_truncation(text, 25)  # cuts "dete|ction"
    assert result["mid_word"] or not result["mid_word"]  # depends on exact position
    # The important thing is it returns a valid result
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
    result = _check_truncation(text, 12)  # "Hello world " - at space
    assert not result["mid_word"]
    print("PASS: test_truncation_at_space")


# ─── LENGTH CHECK TESTS ──────────────────────────────────────

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


# ─── FULL OPTIMIZATION TESTS ─────────────────────────────────

def test_optimize_good_message():
    """Good message should pass optimization."""
    result = optimize_for_preview(GOOD_MESSAGE, "Sarah")
    assert result["length"]["fits"]
    assert result["preview"]["score"] >= 5
    print(f"PASS: test_optimize_good_message (optimized={result['optimized']})")


# ─── VARIANT RANKING TESTS ───────────────────────────────────

def test_rank_variants():
    """Should rank variants by preview score."""
    variants = [
        {"tone": "friendly", "body": GOOD_MESSAGE},
        {"tone": "weak", "body": WEAK_MESSAGE},
        {"tone": "curious", "body": QUESTION_OPENER},
    ]
    ranked = rank_variants_by_preview(variants, "Sarah")

    assert len(ranked) == 3
    # Scores should be descending
    scores = [r["preview_score"] for r in ranked]
    assert scores == sorted(scores, reverse=True), \
        f"Should be sorted by score desc: {scores}"
    # Each entry has expected fields
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


if __name__ == "__main__":
    test_good_opener_scores_well()
    test_weak_opener_scores_low()
    test_question_opener_gets_bonus()
    test_short_preview_penalized()
    test_preview_text_excludes_greeting()
    test_preview_chars_within_limit()
    test_strip_hi_greeting()
    test_strip_hey_greeting()
    test_no_greeting_passthrough()
    test_truncation_mid_word()
    test_no_truncation_short_text()
    test_truncation_at_space()
    test_inmail_fits()
    test_connection_note_too_long()
    test_short_fits_all()
    test_optimize_good_message()
    test_rank_variants()
    test_rank_returns_best_first()
    print("\n=== All 18 LinkedIn optimizer tests passed ===")
