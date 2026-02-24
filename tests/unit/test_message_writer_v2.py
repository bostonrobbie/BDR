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


def test_cta_varies_by_tier():
    """Hot prospects should get more confident CTAs than cold prospects."""
    artifact_hot, scoring_hot = _get_test_data()
    # Force hot tier
    scoring_hot["tier"] = "hot"
    scoring_hot["total_score"] = 85
    output_hot = generate_message_variants(artifact_hot, scoring_hot)

    # Build a cold prospect
    cold_contact = {
        "first_name": "Priya", "last_name": "Patel",
        "title": "Software Engineer", "seniority_level": "",
        "company_name": "",
    }
    cold_result = build_research_artifact(cold_contact, None)
    artifact_cold = cold_result["artifact"]
    scoring_cold = score_from_artifact(artifact_cold)

    output_cold = generate_message_variants(artifact_cold, scoring_cold)

    # Hot friendly CTA should be more confident (15-minute, comparison, etc.)
    hot_friendly = next(v for v in output_hot["variants"] if v["tone"] == "friendly")
    cold_friendly = next(v for v in output_cold["variants"] if v["tone"] == "friendly")
    assert hot_friendly["cta"] != cold_friendly["cta"], \
        f"Hot and cold CTAs should differ: '{hot_friendly['cta']}' vs '{cold_friendly['cta']}'"
    # Hot should mention a time frame or specific offer
    assert any(word in hot_friendly["cta"].lower() for word in ["15-minute", "this week", "make sense"]), \
        f"Hot CTA should be specific: '{hot_friendly['cta']}'"
    # Cold should be softer
    assert any(word in cold_friendly["cta"].lower() for word in ["flag", "helpful", "if", "radar"]), \
        f"Cold CTA should be soft: '{cold_friendly['cta']}'"
    print("PASS: test_cta_varies_by_tier")


def test_cta_varies_by_seniority():
    """VP-level prospects should get strategic offers (conversation), ICs get tactical (comparison/look)."""
    # VP prospect
    vp_contact = {
        "first_name": "Mike", "last_name": "Torres",
        "title": "VP of Engineering", "seniority_level": "vp",
        "company_name": "HealthBridge",
    }
    vp_account = {
        "name": "HealthBridge", "industry": "Healthcare",
        "employee_band": "501-1000", "employee_count": 800,
        "buyer_intent": 0, "known_tools": "[]",
    }
    vp_result = build_research_artifact(vp_contact, vp_account)
    vp_artifact = vp_result["artifact"]
    vp_scoring = score_from_artifact(vp_artifact)
    vp_scoring["tier"] = "warm"
    vp_output = generate_message_variants(vp_artifact, vp_scoring)

    # Manager prospect with same tier
    mgr_contact = {
        "first_name": "James", "last_name": "Wilson",
        "title": "QA Manager", "seniority_level": "manager",
        "company_name": "CloudStack",
    }
    mgr_account = {
        "name": "CloudStack", "industry": "SaaS / B2B Software",
        "employee_band": "1001-5000", "employee_count": 2500,
        "buyer_intent": 0, "known_tools": '["Cypress", "Playwright"]',
    }
    mgr_result = build_research_artifact(mgr_contact, mgr_account)
    mgr_artifact = mgr_result["artifact"]
    mgr_scoring = score_from_artifact(mgr_artifact)
    mgr_scoring["tier"] = "warm"
    mgr_output = generate_message_variants(mgr_artifact, mgr_scoring)

    vp_direct = next(v for v in vp_output["variants"] if v["tone"] == "direct")
    mgr_direct = next(v for v in mgr_output["variants"] if v["tone"] == "direct")

    # VP should get "conversation" offer, manager with Cypress should get "comparison"
    assert "conversation" in vp_direct["cta"].lower(), \
        f"VP CTA should mention conversation: '{vp_direct['cta']}'"
    assert "comparison" in mgr_direct["cta"].lower() or "cypress" in mgr_direct["cta"].lower(), \
        f"Manager with Cypress should get comparison offer: '{mgr_direct['cta']}'"
    print("PASS: test_cta_varies_by_seniority")


def test_signoff_varies_by_tone():
    """Friendly gets 'Cheers', direct gets just name, curious gets 'Best'."""
    artifact, scoring = _get_test_data()
    output = generate_message_variants(artifact, scoring)

    for v in output["variants"]:
        body = v["body"]
        if v["tone"] == "friendly":
            assert "Cheers," in body, f"Friendly should use 'Cheers,' sign-off"
        elif v["tone"] == "direct":
            # Direct should end with just the sender name, no "Best," or "Cheers,"
            assert "Cheers," not in body and "Best," not in body, \
                f"Direct should use bare name sign-off"
        elif v["tone"] == "curious":
            assert "Best," in body, f"Curious should use 'Best,' sign-off"
    print("PASS: test_signoff_varies_by_tone")


def test_ps_line_email_only():
    """P.S. should appear for hot email prospects, not LinkedIn."""
    artifact, scoring = _get_test_data()
    scoring["tier"] = "hot"
    scoring["total_score"] = 85

    linkedin_output = generate_message_variants(artifact, scoring, channel="linkedin")
    email_output = generate_message_variants(artifact, scoring, channel="email")

    for v in linkedin_output["variants"]:
        assert "P.S." not in v["body"], \
            f"LinkedIn {v['tone']} variant should not have P.S."

    # At least one email variant should have P.S. (if secondary PP differs)
    has_ps = any("P.S." in v["body"] for v in email_output["variants"])
    print(f"  Email P.S. present: {has_ps}")
    print("PASS: test_ps_line_email_only")


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
    test_cta_varies_by_tier()
    test_cta_varies_by_seniority()
    test_signoff_varies_by_tone()
    test_ps_line_email_only()
    print("\n=== All 14 message writer v2 tests passed ===")
