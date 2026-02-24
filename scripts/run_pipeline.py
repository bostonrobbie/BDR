#!/usr/bin/env python3
"""
End-to-end pipeline: Research -> Score -> Write for sample prospects.
Runs entirely offline using local data. No LLM calls required.

Usage:
    python scripts/run_pipeline.py
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agents.researcher import build_research_artifact, validate_research_artifact
from src.agents.scorer import score_from_artifact
from src.agents.message_writer import generate_message_variants


# ─── SAMPLE PROSPECTS ──────────────────────────────────────────

PROSPECTS = [
    {
        "contact": {
            "first_name": "Sarah", "last_name": "Chen",
            "title": "Director of Quality Engineering", "seniority_level": "director",
            "company_name": "PayFlow", "linkedin_url": "https://linkedin.com/in/sarahchen",
            "email": "sarah.chen@payflow.com",
        },
        "account": {
            "name": "PayFlow", "domain": "payflow.com", "industry": "FinTech",
            "employee_band": "201-500", "employee_count": 350,
            "hq_location": "San Francisco, CA", "buyer_intent": 1,
            "known_tools": '["Selenium", "Jenkins"]',
        },
        "person_research": {"headline": "QA Leader | Test Automation Advocate"},
    },
    {
        "contact": {
            "first_name": "Mike", "last_name": "Torres",
            "title": "VP of Engineering", "seniority_level": "vp",
            "company_name": "HealthBridge",
        },
        "account": {
            "name": "HealthBridge", "domain": "healthbridge.io", "industry": "Healthcare",
            "employee_band": "501-1000", "employee_count": 800,
            "hq_location": "Boston, MA", "buyer_intent": 0, "known_tools": "[]",
        },
    },
    {
        "contact": {
            "first_name": "James", "last_name": "Wilson",
            "title": "QA Manager", "seniority_level": "manager",
            "company_name": "CloudStack",
        },
        "account": {
            "name": "CloudStack", "industry": "SaaS / B2B Software",
            "employee_band": "1001-5000", "employee_count": 2500,
            "buyer_intent": 0, "known_tools": '["Cypress", "Playwright"]',
        },
    },
]


def run_pipeline():
    """Run the full research -> score -> write pipeline for sample prospects."""
    print("=" * 70)
    print("BDR OUTREACH PIPELINE - End-to-End Run")
    print("=" * 70)

    results = []

    for i, prospect_data in enumerate(PROSPECTS, 1):
        contact = prospect_data["contact"]
        account = prospect_data.get("account")
        person_research = prospect_data.get("person_research")
        name = f"{contact['first_name']} {contact['last_name']}"

        print(f"\n{'─' * 70}")
        print(f"PROSPECT {i}/{len(PROSPECTS)}: {name}")
        print(f"  Title: {contact.get('title', 'N/A')}")
        print(f"  Company: {contact.get('company_name', 'N/A')}")
        print(f"{'─' * 70}")

        # ── Phase 1: Research ──
        print("\n  [1/3] RESEARCH...")
        research_result = build_research_artifact(
            contact, account, person_research=person_research)
        artifact = research_result["artifact"]
        validation = research_result["validation"]

        print(f"    ICP Fit: {artifact['icp_fit']['fit_summary']}")
        print(f"    Fit Reasons: {', '.join(artifact['icp_fit']['fit_reasons'][:3])}")
        print(f"    Pains: {len(artifact['pains']['hypothesized_pains'])} hypotheses")
        print(f"    Hooks: {len(artifact['personalization']['hooks'])} hooks")
        print(f"    Tech Stack: {[t['value'] for t in artifact['signals']['tech_stack']]}")
        print(f"    Validation: {'PASS' if validation['valid'] else 'FAIL'} "
              f"({validation['error_count']} errors, {validation['warning_count']} warnings)")
        if not validation["valid"]:
            for e in validation["errors"]:
                print(f"      ERROR: {e['field']}: {e['message']}")

        # ── Phase 2: Score ──
        print("\n  [2/3] SCORING...")
        scoring = score_from_artifact(artifact)

        print(f"    Total: {scoring['total_score']}/100 ({scoring['tier'].upper()})")
        for feat, score in scoring["feature_scores"].items():
            weight = scoring["feature_weights"].get(feat, "?")
            print(f"      {feat}: {score}/{weight}")
        if scoring["missing_data"]:
            print(f"    Missing: {', '.join(scoring['missing_data'][:3])}")

        # ── Phase 3: Write ──
        print("\n  [3/3] WRITING MESSAGES...")
        messages = generate_message_variants(artifact, scoring, channel="linkedin")

        for v in messages["variants"]:
            qa = next((q for q in messages["qa_results"] if q["tone"] == v["tone"]), {})
            qa_status = "PASS" if qa.get("passed") else "FAIL"
            print(f"\n    --- Variant: {v['tone'].upper()} (QA: {qa_status}) ---")
            print(f"    Subjects: {v['subject_lines']}")
            print(f"    Proof Point: {v['proof_point']}")
            print(f"    CTA: {v['cta']}")
            print(f"    Chars: {v['char_count']}, Words: {v['word_count']}")
            # Print body (indented)
            for line in v["body"].split("\n"):
                print(f"    | {line}")

        results.append({
            "name": name,
            "score": scoring["total_score"],
            "tier": scoring["tier"],
            "variants": len(messages["variants"]),
            "qa_passed": sum(1 for q in messages["qa_results"] if q["passed"]),
        })

    # ── Summary ──
    print(f"\n{'=' * 70}")
    print("PIPELINE SUMMARY")
    print(f"{'=' * 70}")
    results.sort(key=lambda x: x["score"], reverse=True)
    for r in results:
        qa_note = f"{r['qa_passed']}/{r['variants']} QA passed"
        print(f"  {r['name']:20s}  Score: {r['score']:3d}/100 ({r['tier']:4s})  {qa_note}")
    print(f"\nTotal prospects: {len(results)}")
    print(f"Pipeline complete.")


if __name__ == "__main__":
    run_pipeline()
