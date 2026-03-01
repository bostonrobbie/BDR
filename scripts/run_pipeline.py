#!/usr/bin/env python3
"""
End-to-end pipeline: Research -> Enrich -> Score -> Write for sample prospects.
Runs entirely offline using local data. No LLM calls required.

Usage:
    python scripts/run_pipeline.py
    python scripts/run_pipeline.py --with-enrichment   # Also run signal enrichment
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agents.researcher import build_research_artifact, validate_research_artifact
from src.agents.scorer import score_from_artifact
from src.agents.message_writer import generate_message_variants
from src.agents.signal_enrichment import enrich_from_signals, merge_enrichment_into_artifact


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
        "enrichment": {
            "job_postings": [
                {"title": "Senior SDET", "text": "We're looking for a Senior SDET to join our QA team. Requirements: Selenium WebDriver, Cypress, CI/CD pipeline experience. You'll help reduce flaky tests and improve test coverage."},
                {"title": "QA Automation Engineer", "text": "Build and maintain test automation framework. Experience with Selenium, API testing, and cross-browser testing. Help scale our automation to cover 500+ test cases."},
            ],
            "funding_text": "PayFlow raised $45M Series B led by Accel",
            "funding_stage": "Series B",
            "funding_amount": "$45M",
            "news_text": "PayFlow is undergoing a cloud migration to AWS, moving its payment infrastructure to microservices architecture.",
        },
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
        "enrichment": {
            "job_postings": [
                {"title": "QA Manager", "text": "Lead our QA team. Experience with compliance testing, HIPAA, and regulatory requirements. Test maintenance and shift-left testing culture."},
            ],
            "news_text": "HealthBridge announces digital transformation initiative to modernize its patient portal.",
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
        "enrichment": {
            "job_postings": [
                {"title": "SDET Lead", "text": "Own our Cypress and Playwright test infrastructure. Improve test stability and reduce flaky tests. Build cross-browser testing for our SaaS platform."},
                {"title": "QA Engineer", "text": "Write and maintain automated tests using Cypress. API testing with Postman and REST Assured. Experience with CI/CD pipelines required."},
                {"title": "Senior QA Engineer", "text": "Scale our automation framework. Experience with Playwright, performance testing with k6. Help us achieve 90% automation coverage."},
            ],
        },
    },
]


def run_pipeline(with_enrichment: bool = False):
    """Run the full research -> enrich -> score -> write pipeline for sample prospects."""
    print("=" * 70)
    print("BDR OUTREACH PIPELINE - End-to-End Run")
    if with_enrichment:
        print("  (with signal-based enrichment)")
    print("=" * 70)

    results = []

    for i, prospect_data in enumerate(PROSPECTS, 1):
        contact = prospect_data["contact"]
        account = prospect_data.get("account")
        person_research = prospect_data.get("person_research")
        enrichment_data = prospect_data.get("enrichment", {})
        name = f"{contact['first_name']} {contact['last_name']}"

        print(f"\n{'─' * 70}")
        print(f"PROSPECT {i}/{len(PROSPECTS)}: {name}")
        print(f"  Title: {contact.get('title', 'N/A')}")
        print(f"  Company: {contact.get('company_name', 'N/A')}")
        print(f"{'─' * 70}")

        # ── Phase 1: Research ──
        phases = 4 if with_enrichment and enrichment_data else 3
        print(f"\n  [1/{phases}] RESEARCH...")
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

        # ── Phase 1.5: Signal Enrichment (optional) ──
        if with_enrichment and enrichment_data:
            print(f"\n  [2/{phases}] SIGNAL ENRICHMENT...")
            enrichment = enrich_from_signals(
                company_name=contact.get("company_name", ""),
                job_postings=enrichment_data.get("job_postings", []),
                funding_text=enrichment_data.get("funding_text", ""),
                funding_amount=enrichment_data.get("funding_amount", ""),
                funding_stage=enrichment_data.get("funding_stage", ""),
                funding_date=enrichment_data.get("funding_date", ""),
                news_text=enrichment_data.get("news_text", ""),
            )
            artifact = merge_enrichment_into_artifact(artifact, enrichment)
            print(f"    Summary: {enrichment['enrichment_summary']}")
            print(f"    Signals found: {len(enrichment['signals'])}")
            print(f"    New pains: {len(enrichment['pain_hypotheses'])}")
            print(f"    Tech from postings: {[t['value'] for t in enrichment.get('tech_stack_evidence', [])]}")
            print(f"    Hiring velocity: {enrichment.get('hiring_velocity', 'none')}")
            if enrichment.get("transformations"):
                print(f"    Transformations: {enrichment['transformations']}")
            # Re-validate after enrichment
            validation = validate_research_artifact(artifact)
            print(f"    Post-enrichment validation: {'PASS' if validation['valid'] else 'FAIL'}")
            score_phase = 3
            write_phase = 4
        else:
            score_phase = 2
            write_phase = 3

        # ── Phase 2: Score ──
        print(f"\n  [{score_phase}/{phases}] SCORING...")
        scoring = score_from_artifact(artifact)

        print(f"    Total: {scoring['total_score']}/100 ({scoring['tier'].upper()})")
        for feat, score in scoring["feature_scores"].items():
            weight = scoring["feature_weights"].get(feat, "?")
            print(f"      {feat}: {score}/{weight}")
        if scoring["missing_data"]:
            print(f"    Missing: {', '.join(scoring['missing_data'][:3])}")

        # ── Phase 3: Write ──
        print(f"\n  [{write_phase}/{phases}] WRITING MESSAGES...")
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
            "enriched": with_enrichment and bool(enrichment_data),
        })

    # ── Summary ──
    print(f"\n{'=' * 70}")
    print("PIPELINE SUMMARY")
    print(f"{'=' * 70}")
    results.sort(key=lambda x: x["score"], reverse=True)
    for r in results:
        qa_note = f"{r['qa_passed']}/{r['variants']} QA passed"
        enriched_flag = " [enriched]" if r.get("enriched") else ""
        print(f"  {r['name']:20s}  Score: {r['score']:3d}/100 ({r['tier']:4s})  {qa_note}{enriched_flag}")
    print(f"\nTotal prospects: {len(results)}")
    print(f"Pipeline complete.")


if __name__ == "__main__":
    with_enrichment = "--with-enrichment" in sys.argv
    run_pipeline(with_enrichment=with_enrichment)
