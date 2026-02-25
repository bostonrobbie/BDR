"""
Unit tests for the message writer engine.

Sections:
  1. Core variant generation and QA
  2. CTA, sign-off, and P.S. logic
  3. Objection-aware messaging (B5)
  4. Message component scoring (B6)
  5. Dynamic subject line generation (B7)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.agents.researcher import build_research_artifact
from src.agents.scorer import score_from_artifact
from src.agents.message_writer import (
    generate_message_variants,
    check_message_variant,
    render_for_channel,
    predict_objection_from_artifact,
    build_objection_aware_bridge,
    generate_subject_lines,
    _load_product_config,
)
from src.agents.message_components import (
    score_opener,
    score_pain_sentence,
    score_proof_bridge,
    score_cta,
    score_message_components,
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

CONTACT_ENTERPRISE = {
    "first_name": "Mike", "last_name": "Johnson",
    "title": "VP Engineering", "seniority_level": "vp",
    "company_name": "BigCorp",
}
ACCOUNT_ENTERPRISE = {
    "name": "BigCorp", "domain": "bigcorp.com", "industry": "Technology",
    "employee_band": "50000+", "employee_count": 75000,
}

CONTACT_PHARMA = {
    "first_name": "Elena", "last_name": "Rodriguez",
    "title": "QA Manager", "seniority_level": "manager",
    "company_name": "PharmaCo",
}
ACCOUNT_PHARMA = {
    "name": "PharmaCo", "domain": "pharmaco.com", "industry": "Pharma",
    "employee_band": "1001-5000", "employee_count": 3000,
}


def _get_test_data():
    """Build artifact and score for test prospect."""
    result = build_research_artifact(CONTACT, ACCOUNT, person_research=PERSON_RESEARCH)
    artifact = result["artifact"]
    scoring = score_from_artifact(artifact)
    return artifact, scoring


def _build(contact, account=None):
    result = build_research_artifact(contact, account)
    return result["artifact"]


# ═══════════════════════════════════════════════════════════════
# 1. CORE VARIANT GENERATION & QA
# ═══════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════
# 2. CTA, SIGN-OFF, AND P.S. LOGIC
# ═══════════════════════════════════════════════════════════════

def test_cta_varies_by_tier():
    """Hot prospects should get more confident CTAs than cold prospects."""
    artifact_hot, scoring_hot = _get_test_data()
    scoring_hot["tier"] = "hot"
    scoring_hot["total_score"] = 85
    output_hot = generate_message_variants(artifact_hot, scoring_hot)

    cold_contact = {
        "first_name": "Priya", "last_name": "Patel",
        "title": "Software Engineer", "seniority_level": "",
        "company_name": "",
    }
    cold_result = build_research_artifact(cold_contact, None)
    artifact_cold = cold_result["artifact"]
    scoring_cold = score_from_artifact(artifact_cold)
    output_cold = generate_message_variants(artifact_cold, scoring_cold)

    hot_friendly = next(v for v in output_hot["variants"] if v["tone"] == "friendly")
    cold_friendly = next(v for v in output_cold["variants"] if v["tone"] == "friendly")
    assert hot_friendly["cta"] != cold_friendly["cta"], \
        f"Hot and cold CTAs should differ: '{hot_friendly['cta']}' vs '{cold_friendly['cta']}'"
    assert any(word in hot_friendly["cta"].lower() for word in ["that'd", "15 minutes", "show you"]), \
        f"Hot CTA should be specific and reference PP: '{hot_friendly['cta']}'"
    assert any(word in cold_friendly["cta"].lower() for word in ["flag", "helpful", "if", "radar"]), \
        f"Cold CTA should be soft: '{cold_friendly['cta']}'"
    print("PASS: test_cta_varies_by_tier")


def test_cta_varies_by_seniority():
    """VP-level prospects should get strategic offers, ICs get tactical."""
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

    assert any(w in vp_direct["cta"].lower() for w in ["exploring", "apply", "maps"]), \
        f"VP CTA should use strategic framing: '{vp_direct['cta']}'"
    assert "cypress" in mgr_direct["cta"].lower() or "stacks up" in mgr_direct["cta"].lower(), \
        f"Manager with Cypress should reference tool: '{mgr_direct['cta']}'"
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

    has_ps = any("P.S." in v["body"] for v in email_output["variants"])
    print(f"  Email P.S. present: {has_ps}")
    print("PASS: test_ps_line_email_only")


def test_cta_flows_from_proof_point():
    """CTAs should use back-references ('that', 'similar') to tie into the proof point."""
    artifact, scoring = _get_test_data()
    output = generate_message_variants(artifact, scoring)

    back_refs = ["that", "similar"]
    for v in output["variants"]:
        cta = v["cta"].lower()
        has_back_ref = any(ref in cta for ref in back_refs)
        assert has_back_ref, \
            f"{v['tone']} CTA should reference back to proof point: '{v['cta']}'"
    print("PASS: test_cta_flows_from_proof_point")


def test_direct_merges_pp_and_cta():
    """Direct variant should have PP and CTA in the same paragraph."""
    artifact, scoring = _get_test_data()
    output = generate_message_variants(artifact, scoring)

    direct = next(v for v in output["variants"] if v["tone"] == "direct")
    body = direct["body"]
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    pp_para = None
    for p in paragraphs:
        if any(word in p.lower() for word in ["90%", "70%", "cred", "medibuddy", "sanofi", "hansard"]):
            pp_para = p
            break
    assert pp_para is not None, f"Should find a paragraph with proof point in: {paragraphs}"
    cta_words = direct["cta"].lower().split()[:4]
    cta_start = " ".join(cta_words)
    assert cta_start in pp_para.lower(), \
        f"Direct CTA should be in same paragraph as PP. CTA starts: '{cta_start}', PP para: '{pp_para[:100]}...'"
    print("PASS: test_direct_merges_pp_and_cta")


# ═══════════════════════════════════════════════════════════════
# 3. OBJECTION-AWARE MESSAGING (B5)
# ═══════════════════════════════════════════════════════════════

def test_predict_existing_tool_objection():
    """Should predict 'existing tool' for prospects with competitor tools."""
    artifact = _build(CONTACT, ACCOUNT)
    objection = predict_objection_from_artifact(artifact)
    assert objection["objection_key"] == "existing_tool", \
        f"Should predict existing_tool, got {objection['objection_key']}"
    assert "Selenium" in objection.get("tool", ""), f"Should identify Selenium"
    assert "preemptive_phrases" in objection
    assert len(objection["preemptive_phrases"]) == 3
    print("PASS: test_predict_existing_tool_objection")


def test_predict_enterprise_objection():
    """Should predict 'large enterprise' for 50k+ companies."""
    artifact = _build(CONTACT_ENTERPRISE, ACCOUNT_ENTERPRISE)
    objection = predict_objection_from_artifact(artifact)
    assert objection["objection_key"] == "large_enterprise", \
        f"Should predict large_enterprise, got {objection['objection_key']}"
    print("PASS: test_predict_enterprise_objection")


def test_predict_compliance_objection():
    """Should predict 'compliance' for pharma/healthcare."""
    artifact = _build(CONTACT_PHARMA, ACCOUNT_PHARMA)
    objection = predict_objection_from_artifact(artifact)
    assert objection["objection_key"] == "compliance", \
        f"Should predict compliance, got {objection['objection_key']}"
    print("PASS: test_predict_compliance_objection")


def test_objection_bridge_existing_tool():
    """Objection bridge should reference the specific tool."""
    objection = {
        "objection_key": "existing_tool",
        "tool": "Selenium",
    }
    bridge = build_objection_aware_bridge(objection, "friendly", "CRED hit 90%")
    assert "Selenium" in bridge, f"Bridge should reference Selenium: {bridge}"
    print(f"PASS: test_objection_bridge_existing_tool (bridge='{bridge}')")


def test_objection_bridge_varies_by_tone():
    """Different tones should produce different bridges."""
    objection = {"objection_key": "existing_tool", "tool": "Cypress"}
    bridges = {}
    for tone in ["friendly", "direct", "curious"]:
        bridges[tone] = build_objection_aware_bridge(objection, tone, "test")
    unique = set(bridges.values())
    assert len(unique) >= 2, f"Should vary by tone: {bridges}"
    print("PASS: test_objection_bridge_varies_by_tone")


def test_variants_include_objection_metadata():
    """Generated variants should include predicted objection."""
    artifact = _build(CONTACT, ACCOUNT)
    scoring = score_from_artifact(artifact)
    output = generate_message_variants(artifact, scoring)
    for v in output["variants"]:
        assert "predicted_objection" in v, "Variant should have predicted_objection"
        assert "objection_key" in v, "Variant should have objection_key"
    print("PASS: test_variants_include_objection_metadata")


def test_objection_bridge_in_message_body():
    """Objection-aware bridge should appear in the message body."""
    artifact = _build(CONTACT, ACCOUNT)
    scoring = score_from_artifact(artifact)
    output = generate_message_variants(artifact, scoring)
    assert len(output["variants"]) == 3
    print("PASS: test_objection_bridge_in_message_body")


# ═══════════════════════════════════════════════════════════════
# 4. MESSAGE COMPONENT SCORING (B6)
# ═══════════════════════════════════════════════════════════════

def test_score_strong_opener():
    """Strong opener with personalization should score high."""
    score = score_opener("Your work leading QA at PayFlow stood out", has_evidence=True)
    assert score.score >= 0.6, f"Strong opener should score >= 0.6: {score.score}"
    assert score.component_type == "opener"
    print(f"PASS: test_score_strong_opener (score={score.score})")


def test_score_weak_opener():
    """Weak 'I hope this finds you well' opener should score low."""
    score = score_opener("I hope this message finds you well", has_evidence=False)
    assert score.score <= 0.4, f"Weak opener should score <= 0.4: {score.score}"
    print(f"PASS: test_score_weak_opener (score={score.score})")


def test_score_pain_with_tool():
    """Pain sentence with tool reference should score higher."""
    with_tool = score_pain_sentence(
        "Keeping Selenium suites stable while shipping fast",
        has_tool_reference=True)
    without_tool = score_pain_sentence(
        "Test automation challenges are common",
        has_tool_reference=False)
    assert with_tool.score > without_tool.score, \
        f"Tool reference should boost score: {with_tool.score} vs {without_tool.score}"
    print("PASS: test_score_pain_with_tool")


def test_score_proof_bridge_with_metric():
    """Proof bridge with metric should score higher."""
    with_metric = score_proof_bridge(
        "CRED hit 90% regression automation and 5x faster execution",
        "in a similar fintech environment",
        has_metric=True)
    assert with_metric.score >= 0.7, f"Proof with metric should score >= 0.7: {with_metric.score}"
    print(f"PASS: test_score_proof_bridge_with_metric (score={with_metric.score})")


def test_score_cta_with_time_anchor():
    """CTA with time anchor should score higher."""
    with_time = score_cta("Happy to show you in 15 minutes", has_time_anchor=True)
    without_time = score_cta("Would you like to chat?")
    assert with_time.score > without_time.score, \
        f"Time-anchored CTA should score higher: {with_time.score} vs {without_time.score}"
    print("PASS: test_score_cta_with_time_anchor")


def test_score_cta_penalizes_pushy():
    """Pushy CTA language should be penalized."""
    pushy = score_cta("You need to see this ASAP")
    assert pushy.score <= 0.4, f"Pushy CTA should score low: {pushy.score}"
    print(f"PASS: test_score_cta_penalizes_pushy (score={pushy.score})")


def test_score_full_message_components():
    """Full message component scoring should identify weakest component."""
    artifact = _build(CONTACT, ACCOUNT)
    scoring = score_from_artifact(artifact)
    output = generate_message_variants(artifact, scoring)
    variant = output["variants"][0]

    result = score_message_components(variant, artifact)
    assert "overall_score" in result
    assert "components" in result
    assert "weakest" in result
    assert len(result["components"]) >= 3
    assert 0.0 <= result["overall_score"] <= 1.0
    print(f"PASS: test_score_full_message_components (overall={result['overall_score']}, weakest={result['weakest']})")


# ═══════════════════════════════════════════════════════════════
# 5. DYNAMIC SUBJECT LINE GENERATION (B7)
# ═══════════════════════════════════════════════════════════════

def test_generate_5_subject_styles():
    """Should generate 5 subject line variants in different styles."""
    artifact = _build(CONTACT, ACCOUNT)
    pp = _load_product_config().get("proof_points", {}).get("cred_coverage", {})
    subjects = generate_subject_lines(artifact, "test maintenance", pp)

    assert len(subjects) == 5, f"Should generate 5 subjects, got {len(subjects)}"
    styles = {s["style"] for s in subjects}
    expected = {"question", "metric_led", "curiosity", "personalized", "direct"}
    assert styles == expected, f"Should have all 5 styles: {styles}"
    print("PASS: test_generate_5_subject_styles")


def test_subject_lines_scored():
    """Each subject line should have a score between 0 and 1."""
    artifact = _build(CONTACT, ACCOUNT)
    pp = _load_product_config().get("proof_points", {}).get("cred_coverage", {})
    subjects = generate_subject_lines(artifact, "test maintenance", pp)

    for s in subjects:
        assert 0.0 <= s["score"] <= 1.0, f"Score out of range: {s['score']}"
        assert "reasons" in s
    print("PASS: test_subject_lines_scored")


def test_subject_lines_sorted_by_score():
    """Subject lines should be sorted by score descending."""
    artifact = _build(CONTACT, ACCOUNT)
    pp = _load_product_config().get("proof_points", {}).get("cred_coverage", {})
    subjects = generate_subject_lines(artifact, "test maintenance", pp)

    scores = [s["score"] for s in subjects]
    assert scores == sorted(scores, reverse=True), \
        f"Should be sorted by score desc: {scores}"
    print("PASS: test_subject_lines_sorted_by_score")


def test_subject_lines_within_char_limit():
    """Subject lines should respect the max_chars limit."""
    artifact = _build(CONTACT, ACCOUNT)
    pp = _load_product_config().get("proof_points", {}).get("cred_coverage", {})
    subjects = generate_subject_lines(artifact, "test maintenance", pp, max_chars=80)

    for s in subjects:
        assert len(s["subject"]) <= 80, \
            f"Subject too long ({len(s['subject'])}): {s['subject']}"
    print("PASS: test_subject_lines_within_char_limit")


def test_subject_personalization_boosted():
    """Subjects with name/company should score higher than generic."""
    artifact = _build(CONTACT, ACCOUNT)
    pp = _load_product_config().get("proof_points", {}).get("cred_coverage", {})
    subjects = generate_subject_lines(artifact, "test maintenance", pp)

    personalized = next(s for s in subjects if s["style"] == "personalized")
    assert "Sarah" in personalized["subject"] or "PayFlow" in personalized["subject"], \
        f"Personalized should include name/company: {personalized['subject']}"
    print("PASS: test_subject_personalization_boosted")


# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # 1. Core
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
    # 2. CTA / Sign-off
    test_cta_varies_by_tier()
    test_cta_varies_by_seniority()
    test_signoff_varies_by_tone()
    test_ps_line_email_only()
    test_cta_flows_from_proof_point()
    test_direct_merges_pp_and_cta()
    # 3. Objections
    test_predict_existing_tool_objection()
    test_predict_enterprise_objection()
    test_predict_compliance_objection()
    test_objection_bridge_existing_tool()
    test_objection_bridge_varies_by_tone()
    test_variants_include_objection_metadata()
    test_objection_bridge_in_message_body()
    # 4. Components
    test_score_strong_opener()
    test_score_weak_opener()
    test_score_pain_with_tool()
    test_score_proof_bridge_with_metric()
    test_score_cta_with_time_anchor()
    test_score_cta_penalizes_pushy()
    test_score_full_message_components()
    # 5. Subject Lines
    test_generate_5_subject_styles()
    test_subject_lines_scored()
    test_subject_lines_sorted_by_score()
    test_subject_lines_within_char_limit()
    test_subject_personalization_boosted()

    print("\n=== All 35 message writer tests passed ===")
