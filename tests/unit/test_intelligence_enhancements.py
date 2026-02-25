"""
Unit tests for intelligence enhancements:
F7: Per-vertical pain library
F8: Sequence-aware messaging
F9: Decay-aware re-scoring
F10: LLM-assisted pain refinement
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

from src.agents.researcher import build_research_artifact, get_vertical_pains, _load_vertical_pains
from src.agents.scorer import score_from_artifact
from src.agents.message_writer import generate_message_variants, _load_product_config
from src.agents.feedback_tracker import refine_pains_from_reply, _extract_signals_from_reply, _rule_based_pain_refinement
from scripts.rescore_stale import find_stale_contacts, rescore_contact


# ─── SAMPLE DATA ──────────────────────────────────────────────

CONTACT_FINTECH = {
    "first_name": "Sarah", "last_name": "Chen",
    "title": "Director of Quality Engineering", "seniority_level": "director",
    "company_name": "PayFlow", "linkedin_url": "https://linkedin.com/in/sarahchen-vpl",
}
ACCOUNT_FINTECH = {
    "name": "PayFlow", "domain": "payflow.com", "industry": "FinTech",
    "employee_band": "201-500", "employee_count": 350,
    "buyer_intent": 1, "known_tools": '["Selenium", "Jenkins"]',
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

CONTACT_SAAS = {
    "first_name": "Alex", "last_name": "Kim",
    "title": "VP Engineering", "seniority_level": "vp",
    "company_name": "CloudStack",
}
ACCOUNT_SAAS = {
    "name": "CloudStack", "domain": "cloudstack.io", "industry": "SaaS",
    "employee_band": "201-500", "employee_count": 300,
    "known_tools": '["Cypress"]',
}


def _build(contact, account=None):
    result = build_research_artifact(contact, account)
    return result["artifact"]


# ─── F7: PER-VERTICAL PAIN LIBRARY TESTS ────────────────────────

def test_vertical_pains_config_loads():
    """Vertical pain config should load with all expected verticals."""
    config = _load_vertical_pains()
    assert "verticals" in config
    assert len(config["verticals"]) >= 5, \
        f"Should have at least 5 verticals: {list(config['verticals'].keys())}"
    print(f"PASS: test_vertical_pains_config_loads ({len(config['verticals'])} verticals)")


def test_get_fintech_pains():
    """FinTech vertical should return relevant pains."""
    pains = get_vertical_pains("FinTech")
    assert len(pains) >= 2, f"FinTech should have pains: {pains}"
    assert any("payment" in p["pain"].lower() or "financial" in p["pain"].lower()
               for p in pains), "Should include payment/financial pain"
    for p in pains:
        assert "evidence" in p
        assert p["confidence"] > 0
    print(f"PASS: test_get_fintech_pains ({len(pains)} pains)")


def test_get_pharma_pains():
    """Pharma vertical should return compliance-focused pains."""
    pains = get_vertical_pains("Pharma")
    assert len(pains) >= 2
    assert any("gxp" in p["pain"].lower() or "compliance" in p["pain"].lower()
               or "validation" in p["pain"].lower()
               for p in pains), "Should include compliance/validation pain"
    print(f"PASS: test_get_pharma_pains ({len(pains)} pains)")


def test_vertical_pains_case_insensitive():
    """Should work with different case variants."""
    pains_upper = get_vertical_pains("FINTECH")
    pains_lower = get_vertical_pains("fintech")
    assert len(pains_upper) == len(pains_lower), \
        "Case should not matter for vertical lookup"
    print("PASS: test_vertical_pains_case_insensitive")


def test_unknown_vertical_returns_empty():
    """Unknown vertical should return empty list."""
    pains = get_vertical_pains("SpaceExploration")
    assert pains == []
    print("PASS: test_unknown_vertical_returns_empty")


def test_tool_overlap_boosts_confidence():
    """Known tools matching vertical's typical tools should boost confidence."""
    pains_with_tools = get_vertical_pains("FinTech", known_tools=["Selenium"])
    pains_without = get_vertical_pains("FinTech", known_tools=[])
    # With matching tools should have higher confidence
    if pains_with_tools and pains_without:
        assert pains_with_tools[0]["confidence"] > pains_without[0]["confidence"], \
            f"Tool overlap should boost: {pains_with_tools[0]['confidence']} vs {pains_without[0]['confidence']}"
    print("PASS: test_tool_overlap_boosts_confidence")


def test_vertical_pains_integrated_in_artifact():
    """Research artifact should include vertical pains from the library."""
    artifact = _build(CONTACT_FINTECH, ACCOUNT_FINTECH)
    pains = artifact.get("pains", {}).get("hypothesized_pains", [])
    # Should have both CRM-derived and vertical-library pains
    has_vertical_pain = any("vertical pain library" in p.get("evidence", "")
                            for p in pains)
    assert has_vertical_pain, \
        f"Should include vertical library pains: {[p.get('evidence', '') for p in pains]}"
    print(f"PASS: test_vertical_pains_integrated_in_artifact ({len(pains)} total pains)")


def test_vertical_pains_no_duplicates():
    """Vertical pains should not duplicate existing CRM-derived pains."""
    artifact = _build(CONTACT_FINTECH, ACCOUNT_FINTECH)
    pains = artifact.get("pains", {}).get("hypothesized_pains", [])
    pain_texts = [p["pain"].lower() for p in pains]
    unique_texts = set(pain_texts)
    assert len(pain_texts) == len(unique_texts), \
        f"Should not have duplicate pains: {pain_texts}"
    print("PASS: test_vertical_pains_no_duplicates")


# ─── F8: SEQUENCE-AWARE MESSAGING TESTS ──────────────────────────

def test_touch1_full_structure():
    """Touch 1 should have full 6-element message structure."""
    artifact = _build(CONTACT_FINTECH, ACCOUNT_FINTECH)
    scoring = score_from_artifact(artifact)
    output = generate_message_variants(artifact, scoring, touch_number=1)
    for v in output["variants"]:
        assert v["touch_number"] == 1
        assert "Hi " in v["body"], "Touch 1 should have greeting"
        assert len(v["body"].split()) >= 40, \
            f"Touch 1 should be substantial: {len(v['body'].split())} words"
    print("PASS: test_touch1_full_structure")


def test_touch3_followup_shorter():
    """Touch 3 should be a shorter follow-up."""
    artifact = _build(CONTACT_FINTECH, ACCOUNT_FINTECH)
    scoring = score_from_artifact(artifact)
    output_t1 = generate_message_variants(artifact, scoring, touch_number=1)
    output_t3 = generate_message_variants(artifact, scoring, touch_number=3)
    for i, v3 in enumerate(output_t3["variants"]):
        v1 = output_t1["variants"][i]
        assert v3["touch_number"] == 3
        assert v3["word_count"] < v1["word_count"], \
            f"Touch 3 should be shorter than touch 1: {v3['word_count']} vs {v1['word_count']}"
    print("PASS: test_touch3_followup_shorter")


def test_touch3_references_followup():
    """Touch 3 subjects should reference follow-up."""
    artifact = _build(CONTACT_FINTECH, ACCOUNT_FINTECH)
    scoring = score_from_artifact(artifact)
    output = generate_message_variants(artifact, scoring, touch_number=3)
    for v in output["variants"]:
        has_followup = any("follow" in s.lower() or "circling" in s.lower()
                           for s in v["subject_lines"])
        assert has_followup, f"Touch 3 subjects should reference follow-up: {v['subject_lines']}"
    print("PASS: test_touch3_references_followup")


def test_touch5_different_angle():
    """Touch 5 body should differ from touch 3."""
    artifact = _build(CONTACT_FINTECH, ACCOUNT_FINTECH)
    scoring = score_from_artifact(artifact)
    output_t3 = generate_message_variants(artifact, scoring, touch_number=3)
    output_t5 = generate_message_variants(artifact, scoring, touch_number=5)
    for i in range(len(output_t3["variants"])):
        assert output_t3["variants"][i]["body"] != output_t5["variants"][i]["body"], \
            "Touch 5 should differ from touch 3"
    print("PASS: test_touch5_different_angle")


def test_touch6_breakup_no_pitch():
    """Touch 6 should be a break-up with no pitch or proof points."""
    artifact = _build(CONTACT_FINTECH, ACCOUNT_FINTECH)
    scoring = score_from_artifact(artifact)
    output = generate_message_variants(artifact, scoring, touch_number=6)
    for v in output["variants"]:
        body_lower = v["body"].lower()
        assert v["touch_number"] == 6
        assert "closing" in body_lower or "close the loop" in body_lower or \
               "last" in body_lower or "pest" in body_lower, \
            f"Touch 6 should be a close-out: {v['body'][:100]}"
        assert len(v["body"].split()) <= 80, \
            f"Touch 6 should be short: {len(v['body'].split())} words"
    print("PASS: test_touch6_breakup_no_pitch")


def test_touch6_subjects_close_out():
    """Touch 6 subjects should indicate closing."""
    artifact = _build(CONTACT_FINTECH, ACCOUNT_FINTECH)
    scoring = score_from_artifact(artifact)
    output = generate_message_variants(artifact, scoring, touch_number=6)
    for v in output["variants"]:
        has_close = any("clos" in s.lower() or "last" in s.lower() or "all good" in s.lower()
                        for s in v["subject_lines"])
        assert has_close, f"Touch 6 subjects should indicate closing: {v['subject_lines']}"
    print("PASS: test_touch6_subjects_close_out")


def test_metadata_includes_touch_number():
    """Output metadata should include touch_number."""
    artifact = _build(CONTACT_FINTECH, ACCOUNT_FINTECH)
    scoring = score_from_artifact(artifact)
    output = generate_message_variants(artifact, scoring, touch_number=3)
    assert output["metadata"]["touch_number"] == 3, \
        f"Metadata should include touch_number: {output['metadata']}"
    print("PASS: test_metadata_includes_touch_number")


# ─── F9: DECAY-AWARE RE-SCORING TESTS ────────────────────────────

def test_find_stale_contacts_returns_list():
    """find_stale_contacts should return a list (possibly empty with fresh DB)."""
    stale = find_stale_contacts(threshold=0.2)
    assert isinstance(stale, list)
    print(f"PASS: test_find_stale_contacts_returns_list ({len(stale)} stale)")


def test_find_stale_contacts_with_zero_threshold():
    """Threshold of 0 should flag every contact with any signal."""
    stale = find_stale_contacts(threshold=0.0)
    assert isinstance(stale, list)
    print(f"PASS: test_find_stale_contacts_with_zero_threshold ({len(stale)} stale)")


def test_rescore_nonexistent_contact():
    """Re-scoring a nonexistent contact should return error."""
    result = rescore_contact("nonexistent_contact_12345")
    assert "error" in result, f"Should have error: {result}"
    print("PASS: test_rescore_nonexistent_contact")


# ─── F10: LLM-ASSISTED PAIN REFINEMENT TESTS ─────────────────────

def test_extract_signals_tool_mentions():
    """Should extract tool mentions from reply text."""
    signals = _extract_signals_from_reply("we use selenium and jenkins for our ci pipeline")
    tool_signals = [s for s in signals if s["type"] == "test_tool"]
    assert len(tool_signals) >= 1, f"Should detect tool: {signals}"
    ci_signals = [s for s in signals if s["type"] == "ci_tool"]
    assert len(ci_signals) >= 1, f"Should detect CI tool: {signals}"
    print(f"PASS: test_extract_signals_tool_mentions ({len(signals)} signals)")


def test_extract_signals_pain_indicators():
    """Should extract pain indicators from reply text."""
    signals = _extract_signals_from_reply("our tests are flaky and maintenance is killing us")
    pain_signals = [s for s in signals if s["type"] == "pain_signal"]
    assert len(pain_signals) >= 2, f"Should detect pain signals: {signals}"
    pain_values = {s["value"] for s in pain_signals}
    assert "flaky_tests" in pain_values, "Should detect flaky tests"
    assert "maintenance_overhead" in pain_values, "Should detect maintenance"
    print(f"PASS: test_extract_signals_pain_indicators ({len(pain_signals)} pain signals)")


def test_extract_signals_empty_text():
    """Empty text should return no signals."""
    signals = _extract_signals_from_reply("")
    assert signals == []
    print("PASS: test_extract_signals_empty_text")


def test_rule_based_refinement_confirms_pain():
    """Reply mentioning maintenance should boost maintenance pain confidence."""
    original = [
        {"pain": "Test maintenance overhead", "confidence": 0.5,
         "evidence": "from CRM"},
    ]
    refined = _rule_based_pain_refinement(
        original,
        "yeah maintenance is a huge problem for us",
        [{"type": "pain_signal", "value": "maintenance_overhead", "source": "reply"}]
    )
    assert refined[0]["confidence"] > original[0]["confidence"], \
        f"Confirmed pain should have higher confidence: {refined[0]['confidence']}"
    assert "confirmed" in refined[0]["evidence"].lower(), \
        "Evidence should note confirmation"
    print(f"PASS: test_rule_based_refinement_confirms_pain (conf: {original[0]['confidence']} -> {refined[0]['confidence']})")


def test_rule_based_refinement_adds_new_pain():
    """Reply revealing new pain should add it to the list."""
    original = [
        {"pain": "Test maintenance overhead", "confidence": 0.5,
         "evidence": "from CRM"},
    ]
    refined = _rule_based_pain_refinement(
        original,
        "actually our biggest issue is flaky tests breaking ci",
        [{"type": "pain_signal", "value": "flaky_tests", "source": "reply"}]
    )
    assert len(refined) > len(original), \
        f"Should add new pain: {len(refined)} vs {len(original)}"
    new_pains = [p for p in refined if "flaky" in p["pain"].lower()]
    assert len(new_pains) >= 1, "Should add flaky test pain"
    print(f"PASS: test_rule_based_refinement_adds_new_pain ({len(refined)} pains)")


def test_refine_pains_full_flow():
    """Full pain refinement flow should work end-to-end."""
    artifact = _build(CONTACT_FINTECH, ACCOUNT_FINTECH)
    result = refine_pains_from_reply(
        contact_id="test_contact",
        reply_text="Yeah maintenance of Selenium is killing us. Also coverage gaps are a big concern.",
        artifact=artifact,
        use_llm=False,
    )
    assert "original_pains" in result
    assert "refined_pains" in result
    assert "new_signals" in result
    assert result["llm_used"] == False
    assert len(result["new_signals"]) >= 1, f"Should extract signals: {result['new_signals']}"
    print(f"PASS: test_refine_pains_full_flow ({len(result['new_signals'])} signals, {len(result['refined_pains'])} refined pains)")


def test_refine_pains_empty_reply():
    """Empty reply should return empty results."""
    result = refine_pains_from_reply(
        contact_id="test",
        reply_text="",
    )
    assert result["original_pains"] == []
    assert result["refined_pains"] == []
    assert result["new_signals"] == []
    print("PASS: test_refine_pains_empty_reply")


def test_refine_pains_no_llm_fallback():
    """When use_llm is True but LLM unavailable, should fall back to rules."""
    artifact = _build(CONTACT_FINTECH, ACCOUNT_FINTECH)
    result = refine_pains_from_reply(
        contact_id="test",
        reply_text="We have major flaky test problems",
        artifact=artifact,
        use_llm=True,  # LLM not available in test, should fallback
    )
    assert result["llm_used"] == False, "Should fall back when LLM unavailable"
    assert len(result["refined_pains"]) >= 1
    print("PASS: test_refine_pains_no_llm_fallback")


if __name__ == "__main__":
    test_vertical_pains_config_loads()
    test_get_fintech_pains()
    test_get_pharma_pains()
    test_vertical_pains_case_insensitive()
    test_unknown_vertical_returns_empty()
    test_tool_overlap_boosts_confidence()
    test_vertical_pains_integrated_in_artifact()
    test_vertical_pains_no_duplicates()
    test_touch1_full_structure()
    test_touch3_followup_shorter()
    test_touch3_references_followup()
    test_touch5_different_angle()
    test_touch6_breakup_no_pitch()
    test_touch6_subjects_close_out()
    test_metadata_includes_touch_number()
    test_find_stale_contacts_returns_list()
    test_find_stale_contacts_with_zero_threshold()
    test_rescore_nonexistent_contact()
    test_extract_signals_tool_mentions()
    test_extract_signals_pain_indicators()
    test_extract_signals_empty_text()
    test_rule_based_refinement_confirms_pain()
    test_rule_based_refinement_adds_new_pain()
    test_refine_pains_full_flow()
    test_refine_pains_empty_reply()
    test_refine_pains_no_llm_fallback()
    print("\n=== All 26 intelligence enhancement tests passed ===")
