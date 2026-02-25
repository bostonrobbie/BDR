"""
Unit tests for ResearchArtifact schema, builder, and validator.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.agents.researcher import (
    build_empty_artifact,
    build_research_artifact,
    validate_research_artifact,
    make_evidence,
    make_pain_hypothesis,
    make_hook,
    DEFAULT_MUST_NOT_CLAIM,
)


# ─── SAMPLE PROSPECTS ──────────────────────────────────────────

SAMPLE_CONTACTS = [
    {
        "first_name": "Sarah",
        "last_name": "Chen",
        "title": "Director of Quality Engineering",
        "seniority_level": "director",
        "company_name": "PayFlow",
        "linkedin_url": "https://linkedin.com/in/sarahchen",
        "email": "sarah.chen@payflow.com",
    },
    {
        "first_name": "Mike",
        "last_name": "Torres",
        "title": "VP of Engineering",
        "seniority_level": "vp",
        "company_name": "HealthBridge",
        "linkedin_url": "",
        "email": "",
    },
    {
        "first_name": "Priya",
        "last_name": "Patel",
        "title": "Software Engineer",
        "seniority_level": "",
        "company_name": "",
        "linkedin_url": "",
    },
]

SAMPLE_ACCOUNTS = [
    {
        "name": "PayFlow",
        "domain": "payflow.com",
        "industry": "FinTech",
        "employee_band": "201-500",
        "employee_count": 350,
        "hq_location": "San Francisco, CA",
        "buyer_intent": 1,
        "known_tools": '["Selenium", "Jenkins"]',
    },
    {
        "name": "HealthBridge",
        "domain": "healthbridge.io",
        "industry": "Healthcare",
        "employee_band": "501-1000",
        "employee_count": 800,
        "hq_location": "Boston, MA",
        "buyer_intent": 0,
        "known_tools": "[]",
    },
    None,  # No account for Priya
]


def test_empty_artifact_structure():
    """Empty artifact should have all required sections."""
    a = build_empty_artifact()
    assert "prospect" in a
    assert "company" in a
    assert "signals" in a
    assert "icp_fit" in a
    assert "pains" in a
    assert "personalization" in a
    assert "constraints" in a
    assert "metadata" in a
    assert len(a["constraints"]["must_not_claim"]) >= 3
    print("PASS: test_empty_artifact_structure")


def test_build_artifact_from_strong_prospect():
    """Sarah Chen: Director QA at FinTech with Selenium - should be strong."""
    result = build_research_artifact(
        SAMPLE_CONTACTS[0], SAMPLE_ACCOUNTS[0],
        person_research={"headline": "QA Leader | Test Automation Advocate"},
    )
    artifact = result["artifact"]
    validation = result["validation"]

    # Prospect fields populated
    assert artifact["prospect"]["full_name"] == "Sarah Chen"
    assert artifact["prospect"]["title"] == "Director of Quality Engineering"
    assert artifact["prospect"]["seniority"] == "director"
    assert artifact["prospect"]["function"] == "QA/Testing"
    assert artifact["prospect"]["company_name"] == "PayFlow"

    # Company fields
    assert artifact["company"]["industry"] == "FinTech"
    assert artifact["company"]["size_band"] == "201-500"

    # Tech stack (evidence-tagged)
    tech = artifact["signals"]["tech_stack"]
    assert len(tech) >= 1
    assert all(isinstance(t, dict) and "evidence" in t for t in tech)
    tool_names = [t["value"].lower() for t in tech]
    assert "selenium" in tool_names

    # Intent signals (buyer intent flag)
    assert any("buyer intent" in s.get("value", "").lower()
               for s in artifact["signals"]["intent_signals"])

    # Pain hypotheses
    assert len(artifact["pains"]["hypothesized_pains"]) >= 1
    # Selenium pain should be high confidence
    selenium_pain = next(
        (p for p in artifact["pains"]["hypothesized_pains"]
         if "selenium" in p.get("pain", "").lower()),
        None
    )
    assert selenium_pain is not None, "Should have Selenium maintenance pain"
    assert selenium_pain["confidence"] >= 0.7
    assert "unknown" not in selenium_pain["evidence"]

    # Hooks
    assert len(artifact["personalization"]["hooks"]) >= 2
    # All hooks should have evidence
    for hook in artifact["personalization"]["hooks"]:
        assert hook.get("evidence_field"), f"Hook '{hook.get('hook', '')}' missing evidence"

    # ICP fit
    assert "Strong" in artifact["icp_fit"]["fit_summary"] or "Moderate" in artifact["icp_fit"]["fit_summary"]
    assert len(artifact["icp_fit"]["fit_reasons"]) >= 2

    # Constraints
    assert len(artifact["constraints"]["must_not_claim"]) >= 3

    # Validation should pass
    assert validation["valid"], f"Validation errors: {validation['errors']}"

    print("PASS: test_build_artifact_from_strong_prospect")


def test_build_artifact_missing_data():
    """Priya Patel: Software Engineer with no account - should be weak but valid."""
    result = build_research_artifact(SAMPLE_CONTACTS[2], None)
    artifact = result["artifact"]
    validation = result["validation"]

    assert artifact["prospect"]["full_name"] == "Priya Patel"
    assert artifact["prospect"]["function"] == "Engineering"
    assert artifact["prospect"]["seniority"] == "individual"

    # Should still have constraints
    assert len(artifact["constraints"]["must_not_claim"]) >= 3

    # Should have disqualifiers
    assert len(artifact["icp_fit"]["disqualifiers"]) >= 1

    # Should have at least a fallback pain
    assert len(artifact["pains"]["hypothesized_pains"]) >= 1

    # Validation should still pass (evidence rules are about what IS present)
    assert validation["valid"], f"Validation errors: {validation['errors']}"

    print("PASS: test_build_artifact_missing_data")


def test_build_artifact_healthcare_vp():
    """Mike Torres: VP Eng at Healthcare - secondary ICP."""
    result = build_research_artifact(SAMPLE_CONTACTS[1], SAMPLE_ACCOUNTS[1])
    artifact = result["artifact"]

    assert artifact["prospect"]["function"] == "Engineering"
    assert artifact["prospect"]["seniority"] == "vp"
    assert artifact["company"]["industry"] == "Healthcare"

    # Should have healthcare-related pain
    pain_texts = [p["pain"].lower() for p in artifact["pains"]["hypothesized_pains"]]
    assert any("compliance" in p or "regulated" in p for p in pain_texts), \
        f"Expected compliance pain for healthcare, got: {pain_texts}"

    print("PASS: test_build_artifact_healthcare_vp")


def test_validation_rejects_unevidenced_hooks():
    """Artifact with hooks lacking evidence should fail validation."""
    artifact = build_empty_artifact()
    artifact["prospect"]["full_name"] = "Test User"
    artifact["personalization"]["hooks"] = [
        {"hook": "Saw your great post", "evidence_field": ""},  # No evidence!
    ]
    result = validate_research_artifact(artifact)
    assert not result["valid"], "Should reject hooks without evidence"
    assert any("evidence" in e["message"].lower() for e in result["errors"])
    print("PASS: test_validation_rejects_unevidenced_hooks")


def test_validation_rejects_high_confidence_without_evidence():
    """Pain with confidence > 0.7 and no evidence should fail."""
    artifact = build_empty_artifact()
    artifact["prospect"]["full_name"] = "Test User"
    artifact["pains"]["hypothesized_pains"] = [
        {"pain": "They definitely have flaky tests", "confidence": 0.9,
         "evidence": "unknown - hypothesis only"},
    ]
    result = validate_research_artifact(artifact)
    assert not result["valid"], "Should reject high-confidence pain without evidence"
    print("PASS: test_validation_rejects_high_confidence_without_evidence")


def test_validation_rejects_untyped_tech_stack():
    """Tech stack items as plain strings should fail."""
    artifact = build_empty_artifact()
    artifact["prospect"]["full_name"] = "Test User"
    artifact["signals"]["tech_stack"] = ["Selenium"]  # Should be {value, evidence}
    result = validate_research_artifact(artifact)
    assert not result["valid"], "Should reject plain string tech stack"
    print("PASS: test_validation_rejects_untyped_tech_stack")


def test_validation_rejects_empty_must_not_claim():
    """Empty must_not_claim should fail."""
    artifact = build_empty_artifact()
    artifact["prospect"]["full_name"] = "Test User"
    artifact["constraints"]["must_not_claim"] = []
    result = validate_research_artifact(artifact)
    assert not result["valid"], "Should reject empty must_not_claim"
    print("PASS: test_validation_rejects_empty_must_not_claim")


def test_evidence_helpers():
    """Test the make_evidence, make_pain_hypothesis, make_hook helpers."""
    ev = make_evidence("Selenium", "from CRM field: known_tools")
    assert ev["value"] == "Selenium"
    assert ev["evidence"] == "from CRM field: known_tools"

    pain = make_pain_hypothesis("Flaky tests", 0.6, "from CRM field: title")
    assert pain["confidence"] == 0.6
    assert pain["evidence"] == "from CRM field: title"

    # Confidence clamping
    pain2 = make_pain_hypothesis("test", 1.5, "test")
    assert pain2["confidence"] == 1.0
    pain3 = make_pain_hypothesis("test", -0.3, "test")
    assert pain3["confidence"] == 0.0

    hook = make_hook("Role as QA Director", "from CRM field: title")
    assert hook["hook"] == "Role as QA Director"
    assert hook["evidence_field"] == "from CRM field: title"

    print("PASS: test_evidence_helpers")


def test_research_quality_score():
    """Research quality should be higher when more fields are filled."""
    result_full = build_research_artifact(SAMPLE_CONTACTS[0], SAMPLE_ACCOUNTS[0],
                                           person_research={"headline": "QA Leader"})
    result_empty = build_research_artifact(SAMPLE_CONTACTS[2], None)

    q_full = result_full["artifact"]["metadata"]["research_quality_score"]
    q_empty = result_empty["artifact"]["metadata"]["research_quality_score"]
    assert q_full > q_empty, f"Full ({q_full}) should score higher than empty ({q_empty})"
    print(f"PASS: test_research_quality_score (full={q_full}, empty={q_empty})")


if __name__ == "__main__":
    test_empty_artifact_structure()
    test_build_artifact_from_strong_prospect()
    test_build_artifact_missing_data()
    test_build_artifact_healthcare_vp()
    test_validation_rejects_unevidenced_hooks()
    test_validation_rejects_high_confidence_without_evidence()
    test_validation_rejects_untyped_tech_stack()
    test_validation_rejects_empty_must_not_claim()
    test_evidence_helpers()
    test_research_quality_score()
    print("\n=== All 10 research artifact tests passed ===")
