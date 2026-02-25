"""
Unit tests for the LLM polish pass.
Tests validation logic, element preservation, and graceful fallback.
No LLM required - tests the validation and extraction logic independently.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.agents.llm_polish import (
    _extract_preserved_elements,
    _validate_polish,
    _build_polish_prompt,
    polish_message,
)


# ─── SAMPLE DATA ──────────────────────────────────────────────

SAMPLE_BODY_FRIENDLY = """Hi Sarah,

Your work leading QA at PayFlow stood out. Keeping Selenium suites stable while shipping fast is a grind most FinTech teams know well - CRED hit 90% regression automation and 5x faster execution.

Happy to show you what that'd look like against your Selenium setup - 15 minutes, tops.

Cheers,
Rob Gorham"""

SAMPLE_BODY_WITH_PS = """Hi Sarah,

Your work leading QA at PayFlow stood out. Keeping Selenium suites stable while shipping fast is a grind most FinTech teams know well - CRED hit 90% regression automation and 5x faster execution.

Happy to show you what that'd look like against your Selenium setup - 15 minutes, tops.

Cheers,
Rob Gorham

P.S. Medibuddy automated 2,500 tests and cut maintenance 50% - happy to share the full story if relevant."""


def test_extract_preserved_elements():
    """Should extract metrics, customer refs, signoff, and P.S."""
    preserved = _extract_preserved_elements(SAMPLE_BODY_FRIENDLY)

    assert len(preserved["metrics"]) > 0, "Should find metrics like 90%, 5x"
    assert any("90%" in m for m in preserved["metrics"]), f"Should find 90%: {preserved['metrics']}"
    assert "CRED" in preserved["customer_refs"], f"Should find CRED: {preserved['customer_refs']}"
    assert "Rob Gorham" in preserved["signoff"], f"Signoff should contain Rob Gorham"
    assert preserved["ps_line"] == "", "No P.S. in this sample"
    print("PASS: test_extract_preserved_elements")


def test_extract_ps_line():
    """Should extract P.S. line when present."""
    preserved = _extract_preserved_elements(SAMPLE_BODY_WITH_PS)
    assert "P.S." in preserved["ps_line"], f"Should find P.S. line: {preserved['ps_line']}"
    assert "Medibuddy" in preserved["ps_line"]
    print("PASS: test_extract_ps_line")


def test_validate_polish_good():
    """Valid polish that preserves all elements should pass."""
    preserved = _extract_preserved_elements(SAMPLE_BODY_FRIENDLY)

    # Slightly reworded but preserves all elements
    polished = """Hi Sarah,

Your work in QA at PayFlow caught my eye. Keeping Selenium suites running smoothly while shipping fast is something most FinTech teams struggle with - CRED hit 90% regression automation and 5x faster execution.

Happy to show you what that'd look like against your Selenium setup - 15 minutes, tops.

Cheers,
Rob Gorham"""

    result = _validate_polish(SAMPLE_BODY_FRIENDLY, polished, preserved)
    assert result["valid"], f"Should be valid: {result['issues']}"
    print("PASS: test_validate_polish_good")


def test_validate_polish_missing_metric():
    """Polish that drops a metric should fail validation."""
    preserved = _extract_preserved_elements(SAMPLE_BODY_FRIENDLY)

    # Removed the 90% metric
    polished = """Hi Sarah,

Your work in QA at PayFlow caught my eye. Keeping Selenium suites running smoothly is tough - CRED had great results with regression automation.

Happy to show you what that'd look like - 15 minutes, tops.

Cheers,
Rob Gorham"""

    result = _validate_polish(SAMPLE_BODY_FRIENDLY, polished, preserved)
    assert not result["valid"], "Should fail when metric is missing"
    assert any("metric" in issue.lower() or "90%" in issue for issue in result["issues"]), \
        f"Should flag missing metric: {result['issues']}"
    print("PASS: test_validate_polish_missing_metric")


def test_validate_polish_missing_customer():
    """Polish that drops a customer reference should fail."""
    preserved = _extract_preserved_elements(SAMPLE_BODY_FRIENDLY)

    # Removed CRED reference
    polished = """Hi Sarah,

Your work leading QA at PayFlow stood out. Keeping Selenium suites stable while shipping fast is a grind - a fintech team hit 90% regression automation and 5x faster execution.

Happy to show you what that'd look like against your Selenium setup - 15 minutes, tops.

Cheers,
Rob Gorham"""

    result = _validate_polish(SAMPLE_BODY_FRIENDLY, polished, preserved)
    assert not result["valid"], "Should fail when customer ref is missing"
    assert any("CRED" in issue for issue in result["issues"])
    print("PASS: test_validate_polish_missing_customer")


def test_validate_polish_em_dash():
    """Polish that introduces em dashes should fail."""
    preserved = _extract_preserved_elements(SAMPLE_BODY_FRIENDLY)

    polished = SAMPLE_BODY_FRIENDLY.replace(" - ", " \u2014 ")  # Replace hyphens with em dashes

    result = _validate_polish(SAMPLE_BODY_FRIENDLY, polished, preserved)
    assert not result["valid"], "Should fail when em dashes introduced"
    assert any("dash" in issue.lower() for issue in result["issues"])
    print("PASS: test_validate_polish_em_dash")


def test_validate_polish_word_count_drift():
    """Polish that changes word count by more than 20% should fail."""
    preserved = _extract_preserved_elements(SAMPLE_BODY_FRIENDLY)

    # Much shorter version
    polished = "Hi Sarah, your QA work at PayFlow stood out. CRED hit 90% automation. Cheers, Rob Gorham"

    result = _validate_polish(SAMPLE_BODY_FRIENDLY, polished, preserved)
    assert not result["valid"], "Should fail when word count drifts too much"
    assert any("word count" in issue.lower() for issue in result["issues"])
    print("PASS: test_validate_polish_word_count_drift")


def test_validate_polish_signoff_changed():
    """Polish that changes the sign-off should fail."""
    preserved = _extract_preserved_elements(SAMPLE_BODY_FRIENDLY)

    polished = SAMPLE_BODY_FRIENDLY.replace("Rob Gorham", "Best regards, Robert")

    result = _validate_polish(SAMPLE_BODY_FRIENDLY, polished, preserved)
    assert not result["valid"], "Should fail when sign-off is changed"
    print("PASS: test_validate_polish_signoff_changed")


def test_build_polish_prompt():
    """Polish prompt should include the body and metadata."""
    prompt = _build_polish_prompt(
        SAMPLE_BODY_FRIENDLY, "friendly",
        {"prospect_name": "Sarah Chen", "company": "PayFlow"}
    )
    assert "friendly" in prompt.lower()
    assert "Sarah Chen" in prompt
    assert "PayFlow" in prompt
    assert SAMPLE_BODY_FRIENDLY in prompt
    print("PASS: test_build_polish_prompt")


def test_polish_message_fallback():
    """polish_message should fall back to original when LLM unavailable."""
    result = polish_message(
        body=SAMPLE_BODY_FRIENDLY,
        tone="friendly",
        metadata={"prospect_name": "Sarah Chen", "company": "PayFlow"},
    )
    # Without Ollama running, should fall back
    assert result["original"] == SAMPLE_BODY_FRIENDLY
    assert result["polished"] == SAMPLE_BODY_FRIENDLY  # Falls back to original
    assert result["was_polished"] is False
    assert result["fallback_reason"] is not None
    print("PASS: test_polish_message_fallback")


if __name__ == "__main__":
    test_extract_preserved_elements()
    test_extract_ps_line()
    test_validate_polish_good()
    test_validate_polish_missing_metric()
    test_validate_polish_missing_customer()
    test_validate_polish_em_dash()
    test_validate_polish_word_count_drift()
    test_validate_polish_signoff_changed()
    test_build_polish_prompt()
    test_polish_message_fallback()
    print("\n=== All 10 LLM polish tests passed ===")
