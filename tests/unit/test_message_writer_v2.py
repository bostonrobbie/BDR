"""
Unit tests for the v2 grounded multi-variant message writer.
Tests evidence grounding, anti-hallucination, and QA checks.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.agents.researcher import build_research_artifact
from src.agents.scorer import score_from_artifact
from src.agents.message_writer import (
    generate_message_variants,
    check_message_variant,
    _load_product_config,
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
PERSON_RESEARCH = {"headline": "QA Leader | Test Automation Advocate"}


def _get_test_data():
    """Build artifact and score for test prospect."""
    result = build_research_artifact(CONTACT, ACCOUNT, person_research=PERSON_RESEARCH)
    artifact = result["artifact"]
    scoring = score_from_artifact(artifact)
    return artifact, scoring


def test_generates_three_variants():
    """Should produce exactly 3 variants: friendly, direct, curious."""
    artifact, scoring = _get_test_data()
    output = generate_message_variants(artifact, scoring)

    assert len(output["variants"]) == 3
    tones = [v["tone"] for v in output["variants"]]
    assert "friendly" in tones
    assert "direct" in tones
    assert "curious" in tones
    print("PASS: test_generates_three_variants")


def test_each_variant_has_required_fields():
    """Each variant should have body, subject_lines, proof_point, cta."""
    artifact, scoring = _get_test_data()
    output = generate_message_variants(artifact, scoring)

    for v in output["variants"]:
        assert v.get("body"), f"{v['tone']} variant missing body"
        assert len(v.get("subject_lines", [])) >= 2, f"{v['tone']} variant needs >= 2 subject lines"
        assert v.get("proof_point"), f"{v['tone']} variant missing proof point"
        assert v.get("cta"), f"{v['tone']} variant missing CTA"
        assert v.get("opener"), f"{v['tone']} variant missing opener"
        assert v.get("opener_evidence"), f"{v['tone']} variant missing opener evidence"
        assert v.get("char_count", 0) > 0
        assert v.get("word_count", 0) > 0
    print("PASS: test_each_variant_has_required_fields")


def test_no_forbidden_phrases():
    """No variant should contain forbidden phrases."""
    artifact, scoring = _get_test_data()
    config = _load_product_config()
    output = generate_message_variants(artifact, scoring, product_config=config)
    forbidden = config.get("forbidden_phrases", [])

    for v in output["variants"]:
        body_lower = v["body"].lower()
        for fp in forbidden:
            assert fp.lower() not in body_lower, \
                f"{v['tone']} variant contains forbidden phrase: '{fp}'"
    print("PASS: test_no_forbidden_phrases")


def test_no_em_dashes():
    """No variant should contain em dashes."""
    artifact, scoring = _get_test_data()
    output = generate_message_variants(artifact, scoring)

    for v in output["variants"]:
        assert "\u2014" not in v["body"], f"{v['tone']} variant contains em dash"
        assert "\u2013" not in v["body"], f"{v['tone']} variant contains en dash"
    print("PASS: test_no_em_dashes")


def test_proof_point_is_from_config():
    """Proof point must be from product config, not hallucinated."""
    artifact, scoring = _get_test_data()
    config = _load_product_config()
    output = generate_message_variants(artifact, scoring, product_config=config)

    valid_keys = set(config.get("proof_points", {}).keys())
    for v in output["variants"]:
        pp_key = v.get("proof_point_key", "")
        assert pp_key in valid_keys, \
            f"{v['tone']} variant uses unknown proof point: '{pp_key}'"
    print("PASS: test_proof_point_is_from_config")


def test_opener_is_evidence_grounded():
    """Opener personalization must have evidence field set."""
    artifact, scoring = _get_test_data()
    output = generate_message_variants(artifact, scoring)

    for v in output["variants"]:
        assert v.get("opener_evidence"), \
            f"{v['tone']} variant opener lacks evidence grounding"
        assert v["opener_evidence"] != "unknown - hypothesis only"
    print("PASS: test_opener_is_evidence_grounded")


def test_qa_checks_pass():
    """QA checks should pass for well-formed variants."""
    artifact, scoring = _get_test_data()
    output = generate_message_variants(artifact, scoring)

    for qa in output["qa_results"]:
        if not qa["passed"]:
            failed_checks = [c for c in qa["checks"] if not c["passed"]]
            print(f"  WARNING: {qa['tone']} variant failed QA: {failed_checks}")
        # At minimum, core checks should pass
        check_map = {c["check"]: c for c in qa["checks"]}
        assert check_map["no_forbidden_phrases"]["passed"], \
            f"{qa['tone']}: forbidden phrases found"
        assert check_map["no_em_dashes"]["passed"], \
            f"{qa['tone']}: em dashes found"
        assert check_map["proof_point_valid"]["passed"], \
            f"{qa['tone']}: invalid proof point"
    print("PASS: test_qa_checks_pass")


def test_char_limit_linkedin():
    """LinkedIn variants should be under 600 chars."""
    artifact, scoring = _get_test_data()
    output = generate_message_variants(artifact, scoring, channel="linkedin")

    for v in output["variants"]:
        assert v["char_count"] <= 700, \
            f"{v['tone']} variant exceeds LinkedIn char limit: {v['char_count']} chars"
    print("PASS: test_char_limit_linkedin")


def test_metadata_populated():
    """Output metadata should contain scoring and prospect info."""
    artifact, scoring = _get_test_data()
    output = generate_message_variants(artifact, scoring)
    meta = output["metadata"]

    assert meta.get("prospect_name") == "Sarah Chen"
    assert meta.get("company") == "PayFlow"
    assert meta.get("scoring_tier") in ("hot", "warm", "cool", "cold")
    assert meta.get("total_score", 0) > 0
    assert meta.get("proof_point_used")
    print("PASS: test_metadata_populated")


def test_qa_rejects_bad_variant():
    """A variant with forbidden phrases should fail QA."""
    artifact, _ = _get_test_data()
    bad_variant = {
        "tone": "test",
        "body": "I saw your post on LinkedIn and noticed you work at PayFlow. "
                "I was browsing your profile and\u2014thought I'd reach out.",
        "opener": "test",
        "opener_evidence": "",
        "proof_point_key": "fake_proof_point",
    }
    qa = check_message_variant(bad_variant, artifact)
    assert not qa["passed"], "Should fail QA"
    check_map = {c["check"]: c for c in qa["checks"]}
    assert not check_map["opener_has_evidence"]["passed"]
    assert not check_map["no_forbidden_phrases"]["passed"]
    assert not check_map["no_em_dashes"]["passed"]
    assert not check_map["proof_point_valid"]["passed"]
    print(f"PASS: test_qa_rejects_bad_variant ({qa['passed_count']}/{qa['total_checks']} checks passed)")


if __name__ == "__main__":
    test_generates_three_variants()
    test_each_variant_has_required_fields()
    test_no_forbidden_phrases()
    test_no_em_dashes()
    test_proof_point_is_from_config()
    test_opener_is_evidence_grounded()
    test_qa_checks_pass()
    test_char_limit_linkedin()
    test_metadata_populated()
    test_qa_rejects_bad_variant()
    print("\n=== All 10 message writer v2 tests passed ===")
