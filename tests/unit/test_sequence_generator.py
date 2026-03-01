"""
Unit tests for the multi-touch sequence generator.
Tests cadence logic, proof point rotation, escalation, and tier-driven timing.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.agents.researcher import build_research_artifact
from src.agents.scorer import score_from_artifact
from src.agents.sequence_generator import (
    generate_sequence,
    get_cadence_schedule,
    CADENCE,
)


# ─── SAMPLE DATA ──────────────────────────────────────────────

CONTACT_HOT = {
    "first_name": "Sarah", "last_name": "Chen",
    "title": "Director of Quality Engineering", "seniority_level": "director",
    "company_name": "PayFlow", "linkedin_url": "https://linkedin.com/in/sarahchen",
    "email": "sarah.chen@payflow.com",
}
ACCOUNT_HOT = {
    "name": "PayFlow", "domain": "payflow.com", "industry": "FinTech",
    "employee_band": "201-500", "employee_count": 350,
    "buyer_intent": 1, "known_tools": '["Selenium", "Jenkins"]',
}

CONTACT_COLD = {
    "first_name": "Priya", "last_name": "Patel",
    "title": "Software Engineer", "seniority_level": "",
    "company_name": "",
}


def _build(contact, account=None):
    result = build_research_artifact(contact, account)
    artifact = result["artifact"]
    scoring = score_from_artifact(artifact)
    return artifact, scoring


# ─── TESTS ───────────────────────────────────────────────────

def test_hot_sequence_has_all_touches():
    """Hot prospect should get full 6-touch sequence."""
    artifact, scoring = _build(CONTACT_HOT, ACCOUNT_HOT)
    seq = generate_sequence(artifact, scoring, has_email=True)

    touch_nums = [t["touch_number"] for t in seq["touches"]]
    assert 1 in touch_nums, "Should have Touch 1"
    assert 2 in touch_nums, "Should have Touch 2 (call)"
    assert 3 in touch_nums, "Should have Touch 3 (followup)"
    assert 6 in touch_nums, "Should have Touch 6 (breakup)"
    assert len(seq["touches"]) >= 5, f"Hot should have 5+ touches: {touch_nums}"
    print("PASS: test_hot_sequence_has_all_touches")


def test_cold_sequence_is_minimal():
    """Cold prospect should get only 2 touches."""
    artifact, scoring = _build(CONTACT_COLD)
    seq = generate_sequence(artifact, scoring)

    touch_nums = [t["touch_number"] for t in seq["touches"]]
    assert len(seq["touches"]) == 2, f"Cold should have 2 touches: {touch_nums}"
    assert 1 in touch_nums and 6 in touch_nums
    print("PASS: test_cold_sequence_is_minimal")


def test_proof_points_rotate():
    """Different touches should use different proof points."""
    artifact, scoring = _build(CONTACT_HOT, ACCOUNT_HOT)
    seq = generate_sequence(artifact, scoring, has_email=True)

    pp_keys = [t["proof_point_key"] for t in seq["touches"] if t.get("proof_point_key")]
    unique_pps = set(pp_keys)
    assert len(unique_pps) >= 2, f"Should rotate proof points: {pp_keys}"
    print(f"PASS: test_proof_points_rotate ({len(unique_pps)} unique across {len(pp_keys)} touches)")


def test_touch_channels_correct():
    """Touches should use the right channels."""
    artifact, scoring = _build(CONTACT_HOT, ACCOUNT_HOT)
    seq = generate_sequence(artifact, scoring, has_email=True)

    for touch in seq["touches"]:
        if touch["touch_number"] in (1, 3, 6):
            assert touch["channel"] == "linkedin", f"Touch {touch['touch_number']} should be LinkedIn"
        elif touch["touch_number"] in (2, 4):
            assert touch["channel"] == "phone", f"Touch {touch['touch_number']} should be phone"
        elif touch["touch_number"] == 5:
            assert touch["channel"] == "email", f"Touch 5 should be email"
    print("PASS: test_touch_channels_correct")


def test_touch_types_correct():
    """Each touch should have the right type."""
    artifact, scoring = _build(CONTACT_HOT, ACCOUNT_HOT)
    seq = generate_sequence(artifact, scoring, has_email=True)

    for touch in seq["touches"]:
        if touch["touch_number"] == 1:
            assert touch["touch_type"] == "inmail"
        elif touch["touch_number"] in (2, 4):
            assert touch["touch_type"] == "call_snippet"
        elif touch["touch_number"] == 3:
            assert touch["touch_type"] == "inmail_followup"
        elif touch["touch_number"] == 5:
            assert touch["touch_type"] == "email"
        elif touch["touch_number"] == 6:
            assert touch["touch_type"] == "inmail_breakup"
    print("PASS: test_touch_types_correct")


def test_touch3_references_previous():
    """Touch 3 follow-up should reference previous outreach."""
    artifact, scoring = _build(CONTACT_HOT, ACCOUNT_HOT)
    seq = generate_sequence(artifact, scoring)

    touch3 = next((t for t in seq["touches"] if t["touch_number"] == 3), None)
    assert touch3 is not None, "Should have Touch 3"
    body_lower = touch3["body"].lower()
    assert any(word in body_lower for word in ["circling back", "following up", "follow up"]), \
        f"Touch 3 should reference previous outreach: {touch3['body'][:100]}"
    print("PASS: test_touch3_references_previous")


def test_touch5_acknowledges_channel_switch():
    """Touch 5 email should acknowledge the channel switch."""
    artifact, scoring = _build(CONTACT_HOT, ACCOUNT_HOT)
    seq = generate_sequence(artifact, scoring, has_email=True)

    touch5 = next((t for t in seq["touches"] if t["touch_number"] == 5), None)
    if touch5:
        body_lower = touch5["body"].lower()
        assert any(word in body_lower for word in ["email", "switching", "linkedin"]), \
            f"Touch 5 should acknowledge channel switch: {touch5['body'][:100]}"
    print("PASS: test_touch5_acknowledges_channel_switch")


def test_touch6_no_pitch():
    """Touch 6 breakup should not contain any pitch or proof points."""
    artifact, scoring = _build(CONTACT_HOT, ACCOUNT_HOT)
    seq = generate_sequence(artifact, scoring)

    touch6 = next((t for t in seq["touches"] if t["touch_number"] == 6), None)
    assert touch6 is not None, "Should have Touch 6"
    assert touch6["proof_point_key"] == "", "Breakup should have no proof point"
    body_lower = touch6["body"].lower()
    assert "testsigma" not in body_lower, "Breakup should not mention product"
    assert any(word in body_lower for word in ["close the loop", "closing the loop"]), \
        f"Breakup should reference closing the loop: {touch6['body'][:100]}"
    print("PASS: test_touch6_no_pitch")


def test_call_snippet_format():
    """Call snippets should have 3-line OPENER/PAIN/BRIDGE format."""
    artifact, scoring = _build(CONTACT_HOT, ACCOUNT_HOT)
    seq = generate_sequence(artifact, scoring)

    call = next((t for t in seq["touches"] if t["touch_type"] == "call_snippet"), None)
    assert call is not None, "Should have a call snippet"
    assert "OPENER:" in call["body"]
    assert "PAIN:" in call["body"]
    assert "BRIDGE:" in call["body"]
    print("PASS: test_call_snippet_format")


def test_no_em_dashes_in_sequence():
    """No touch in the sequence should contain em dashes."""
    artifact, scoring = _build(CONTACT_HOT, ACCOUNT_HOT)
    seq = generate_sequence(artifact, scoring, has_email=True)

    for touch in seq["touches"]:
        assert "\u2014" not in touch["body"], f"Touch {touch['touch_number']} has em dash"
        assert "\u2013" not in touch["body"], f"Touch {touch['touch_number']} has en dash"
    print("PASS: test_no_em_dashes_in_sequence")


def test_cadence_timing():
    """Cadence timing should match the tier config."""
    for tier, config in CADENCE.items():
        schedule = get_cadence_schedule(tier, "2026-03-01T00:00:00")
        assert len(schedule) == len(config["touches"]), \
            f"{tier} schedule length mismatch"
        for i, entry in enumerate(schedule):
            assert entry["day_offset"] == config["days_between"][i], \
                f"{tier} day offset mismatch at touch {entry['touch_number']}"
    print("PASS: test_cadence_timing")


def test_skip_touch5_without_email():
    """Touch 5 email should be skipped when prospect has no email."""
    artifact, scoring = _build(CONTACT_HOT, ACCOUNT_HOT)
    seq = generate_sequence(artifact, scoring, has_email=False)

    touch_nums = [t["touch_number"] for t in seq["touches"]]
    assert 5 not in touch_nums, f"Touch 5 should be skipped without email: {touch_nums}"
    print("PASS: test_skip_touch5_without_email")


def test_qa_runs_on_written_touches():
    """QA should run on written touches but not call snippets."""
    artifact, scoring = _build(CONTACT_HOT, ACCOUNT_HOT)
    seq = generate_sequence(artifact, scoring)

    qa_touch_nums = {q["touch_number"] for q in seq["qa_results"]}
    for touch in seq["touches"]:
        if touch["touch_type"] == "call_snippet":
            assert touch["touch_number"] not in qa_touch_nums, \
                f"Call snippet touch {touch['touch_number']} should not have QA"
        else:
            assert touch["touch_number"] in qa_touch_nums, \
                f"Written touch {touch['touch_number']} should have QA"
    print("PASS: test_qa_runs_on_written_touches")


def test_metadata_populated():
    """Sequence metadata should contain key info."""
    artifact, scoring = _build(CONTACT_HOT, ACCOUNT_HOT)
    seq = generate_sequence(artifact, scoring)

    meta = seq["metadata"]
    assert meta["prospect_name"] == "Sarah Chen"
    assert meta["company"] == "PayFlow"
    assert meta["scoring_tier"] in ("hot", "warm", "cool", "cold")
    assert meta["total_score"] > 0
    assert len(meta["proof_points_used"]) >= 1
    assert meta["generated_at"]

    cadence = seq["cadence"]
    assert cadence["tier"]
    assert cadence["total_touches"] > 0
    assert cadence["total_days"] > 0
    print("PASS: test_metadata_populated")


def test_tone_consistency():
    """All touches should use the requested tone."""
    artifact, scoring = _build(CONTACT_HOT, ACCOUNT_HOT)
    for tone in ["friendly", "direct", "curious"]:
        seq = generate_sequence(artifact, scoring, tone=tone)
        assert seq["metadata"]["tone"] == tone
    print("PASS: test_tone_consistency")


if __name__ == "__main__":
    test_hot_sequence_has_all_touches()
    test_cold_sequence_is_minimal()
    test_proof_points_rotate()
    test_touch_channels_correct()
    test_touch_types_correct()
    test_touch3_references_previous()
    test_touch5_acknowledges_channel_switch()
    test_touch6_no_pitch()
    test_call_snippet_format()
    test_no_em_dashes_in_sequence()
    test_cadence_timing()
    test_skip_touch5_without_email()
    test_qa_runs_on_written_touches()
    test_metadata_populated()
    test_tone_consistency()
    print("\n=== All 15 sequence generator tests passed ===")
