"""
Unit tests for signal-based enrichment.
Tests job posting analysis, funding signals, news analysis, and artifact merging.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.agents.signal_enrichment import (
    analyze_job_posting,
    analyze_job_postings_batch,
    analyze_funding,
    analyze_company_news,
    enrich_from_signals,
    merge_enrichment_into_artifact,
)
from src.agents.researcher import build_research_artifact


# ─── JOB POSTING TESTS ───────────────────────────────────────

def test_detect_qa_role():
    """Should identify QA-related job titles."""
    result = analyze_job_posting(
        "Build automated tests using Selenium...",
        job_title="Senior QA Engineer",
        company_name="TestCo",
    )
    assert result["is_qa_role"], "Senior QA Engineer should be detected as QA role"
    assert result["is_senior"], "Senior QA Engineer should be detected as senior"
    print("PASS: test_detect_qa_role")


def test_detect_sdet():
    """Should identify SDET roles."""
    result = analyze_job_posting(
        "We need an SDET to build test frameworks...",
        job_title="SDET Lead",
        company_name="TestCo",
    )
    assert result["is_qa_role"], "SDET Lead should be detected as QA role"
    assert result["is_senior"], "SDET Lead should be detected as senior"
    print("PASS: test_detect_sdet")


def test_detect_non_qa_role():
    """Should NOT flag non-QA roles as QA."""
    result = analyze_job_posting(
        "Build product features...",
        job_title="Frontend Engineer",
        company_name="TestCo",
    )
    assert not result["is_qa_role"], "Frontend Engineer should not be QA"
    print("PASS: test_detect_non_qa_role")


def test_detect_tools_in_posting():
    """Should detect testing tools mentioned in job descriptions."""
    result = analyze_job_posting(
        "Requirements: 3+ years with Selenium WebDriver, Cypress experience preferred. "
        "Familiarity with BrowserStack for cross-browser testing. Postman for API testing.",
        job_title="QA Engineer",
        company_name="TestCo",
    )
    assert "selenium" in result["tools_detected"], f"Should detect Selenium: {result['tools_detected']}"
    assert "cypress" in result["tools_detected"], f"Should detect Cypress: {result['tools_detected']}"
    assert "browserstack" in result["tools_detected"], f"Should detect BrowserStack: {result['tools_detected']}"
    assert "postman" in result["tools_detected"], f"Should detect Postman: {result['tools_detected']}"
    print("PASS: test_detect_tools_in_posting")


def test_detect_pain_in_posting():
    """Should detect pain indicators in job descriptions."""
    result = analyze_job_posting(
        "Help us reduce flaky tests and improve test stability. "
        "You'll work on scaling our automation coverage and reducing test maintenance overhead.",
        job_title="QA Engineer",
        company_name="TestCo",
    )
    pain_types = [p["type"] for p in result["pains_detected"]]
    assert "flaky_tests" in pain_types, f"Should detect flaky_tests pain: {pain_types}"
    assert "maintenance_overhead" in pain_types, f"Should detect maintenance: {pain_types}"
    assert "scaling_automation" in pain_types, f"Should detect scaling: {pain_types}"
    print("PASS: test_detect_pain_in_posting")


def test_batch_analysis():
    """Batch analysis should aggregate signals across multiple postings."""
    postings = [
        {"title": "Senior SDET", "text": "Build Selenium test framework. Fix flaky tests."},
        {"title": "QA Engineer", "text": "Write Cypress tests. Cross-browser testing with BrowserStack."},
        {"title": "QA Manager", "text": "Lead QA team. Scale automation. Reduce test maintenance."},
    ]
    result = analyze_job_postings_batch(postings, "TestCo")

    assert result["total_qa_roles"] == 3, f"Should find 3 QA roles: {result['total_qa_roles']}"
    assert result["senior_qa_roles"] >= 1, f"Should find at least 1 senior: {result['senior_qa_roles']}"
    assert result["hiring_velocity"] == "medium", f"3 roles = medium velocity: {result['hiring_velocity']}"
    assert "selenium" in result["all_tools"], f"Should aggregate Selenium: {result['all_tools']}"
    assert "cypress" in result["all_tools"], f"Should aggregate Cypress: {result['all_tools']}"
    assert len(result["signals"]) > 0, "Should produce signals"
    assert len(result["pain_hypotheses"]) > 0, "Should produce pain hypotheses"
    print("PASS: test_batch_analysis")


def test_high_hiring_velocity():
    """5+ QA roles should be high velocity."""
    postings = [
        {"title": f"QA Engineer {i}", "text": "Automated testing with Selenium."}
        for i in range(5)
    ]
    result = analyze_job_postings_batch(postings, "BigCo")
    assert result["hiring_velocity"] == "high", f"5 roles = high: {result['hiring_velocity']}"
    print("PASS: test_high_hiring_velocity")


# ─── FUNDING TESTS ───────────────────────────────────────────

def test_funding_series_b():
    """Series B should produce growth-mode signals."""
    result = analyze_funding(
        "Raised $50M Series B from Accel",
        company_name="GrowthCo",
        amount="$50M",
        stage="Series B",
    )
    assert len(result["signals"]) >= 1, "Should produce funding signal"
    assert result["detected_stage"] == "series b"
    assert result["stage_info"]["budget_signal"] == "growth_mode"
    # Growth-mode should produce scaling pain hypothesis
    assert len(result["pain_hypotheses"]) > 0, "Growth stage should produce pain hypothesis"
    print("PASS: test_funding_series_b")


def test_funding_seed():
    """Seed funding should be lower strength."""
    result = analyze_funding(
        "Pre-seed round",
        company_name="TinyCo",
        stage="seed",
    )
    assert result["stage_info"]["strength"] == "low"
    assert result["stage_info"]["budget_signal"] == "early_stage"
    print("PASS: test_funding_seed")


def test_funding_auto_detect_stage():
    """Should auto-detect funding stage from free text."""
    result = analyze_funding(
        "The company recently closed a Series C round at $100M valuation",
        company_name="ScaleCo",
    )
    assert result["detected_stage"] == "series c", f"Should detect Series C: {result['detected_stage']}"
    print("PASS: test_funding_auto_detect_stage")


# ─── COMPANY NEWS TESTS ──────────────────────────────────────

def test_cloud_migration_signal():
    """Should detect cloud migration from news."""
    result = analyze_company_news(
        "The company is undergoing a cloud migration to AWS, moving legacy systems to the cloud.",
        company_name="MigrateCo",
    )
    assert "cloud_migration" in result["transformations_detected"]
    assert len(result["signals"]) > 0
    assert result["signals"][0]["signal_type"] == "digital_transformation"
    assert len(result["pain_hypotheses"]) > 0, "Transformation should produce pain"
    print("PASS: test_cloud_migration_signal")


def test_devops_transformation():
    """Should detect DevOps transformation."""
    result = analyze_company_news(
        "We're implementing CI/CD pipelines across all teams as part of our DevOps transformation.",
        company_name="DevOpsCo",
    )
    assert "devops_transformation" in result["transformations_detected"]
    print("PASS: test_devops_transformation")


def test_no_transformation():
    """Ordinary news should not trigger transformation signals."""
    result = analyze_company_news(
        "The company reported strong Q4 earnings and plans to expand into new markets.",
        company_name="NormalCo",
    )
    assert len(result["transformations_detected"]) == 0
    assert len(result["signals"]) == 0
    print("PASS: test_no_transformation")


# ─── UNIFIED ENRICHMENT TESTS ────────────────────────────────

def test_unified_enrichment():
    """enrich_from_signals should combine all signal sources."""
    result = enrich_from_signals(
        company_name="PayFlow",
        job_postings=[
            {"title": "Senior SDET", "text": "Selenium, Cypress, flaky tests, scaling automation."},
        ],
        funding_text="Series B round",
        funding_stage="Series B",
        funding_amount="$45M",
        news_text="PayFlow announces cloud migration to AWS.",
    )
    assert len(result["signals"]) >= 3, f"Should have signals from jobs + funding + news: {len(result['signals'])}"
    assert len(result["pain_hypotheses"]) > 0, "Should have pain hypotheses"
    assert result["total_qa_roles"] >= 1
    assert "cloud_migration" in result["transformations"]
    assert result["enrichment_summary"], "Should have non-empty summary"
    print("PASS: test_unified_enrichment")


def test_enrichment_empty_input():
    """Should handle empty input gracefully."""
    result = enrich_from_signals(company_name="EmptyCo")
    assert result["signals"] == []
    assert result["pain_hypotheses"] == []
    assert result["hiring_velocity"] == "none"
    assert result["enrichment_summary"] == "No enrichment signals detected"
    print("PASS: test_enrichment_empty_input")


# ─── ARTIFACT MERGE TESTS ────────────────────────────────────

def test_merge_into_artifact():
    """Enrichment should merge into existing artifact without overwriting."""
    contact = {
        "first_name": "Sarah", "last_name": "Chen",
        "title": "Director of Quality Engineering", "seniority_level": "director",
        "company_name": "PayFlow",
    }
    account = {
        "name": "PayFlow", "industry": "FinTech",
        "employee_band": "201-500", "known_tools": '["Selenium"]',
    }
    research = build_research_artifact(contact, account)
    artifact = research["artifact"]

    original_pain_count = len(artifact["pains"]["hypothesized_pains"])
    original_tech_count = len(artifact["signals"]["tech_stack"])

    enrichment = enrich_from_signals(
        company_name="PayFlow",
        job_postings=[
            {"title": "QA Engineer", "text": "Cypress testing, fix flaky tests"},
        ],
        funding_text="Series B",
        funding_stage="Series B",
    )

    merged = merge_enrichment_into_artifact(artifact, enrichment)

    # Should add new tech (Cypress) but not duplicate existing (Selenium is already in the artifact)
    tech_values = [t["value"].lower() if isinstance(t, dict) else t.lower()
                   for t in merged["signals"]["tech_stack"]]
    assert "cypress" in tech_values, f"Should add Cypress from job posting: {tech_values}"

    # Should add new pains
    assert len(merged["pains"]["hypothesized_pains"]) >= original_pain_count, \
        "Should not lose existing pains"

    # Should add signal enrichment to data sources
    assert "signal_enrichment" in merged["metadata"]["data_sources"]

    # ICP fit reasons should include enrichment summary
    fit_reasons = " ".join(merged["icp_fit"]["fit_reasons"])
    assert "Enrichment" in fit_reasons or "enrichment" in fit_reasons.lower()

    print("PASS: test_merge_into_artifact")


def test_merge_deduplicates_tools():
    """Merge should not duplicate tools already in the artifact."""
    contact = {
        "first_name": "Test", "last_name": "User",
        "title": "QA Manager", "company_name": "TestCo",
    }
    account = {"name": "TestCo", "known_tools": '["Selenium", "Cypress"]'}
    research = build_research_artifact(contact, account)
    artifact = research["artifact"]

    enrichment = enrich_from_signals(
        company_name="TestCo",
        job_postings=[
            {"title": "QA Engineer", "text": "Selenium and Cypress experience required."},
        ],
    )

    merged = merge_enrichment_into_artifact(artifact, enrichment)
    tech_values = [t["value"].lower() if isinstance(t, dict) else t.lower()
                   for t in merged["signals"]["tech_stack"]]

    # Count occurrences of each tool
    selenium_count = tech_values.count("selenium")
    cypress_count = tech_values.count("cypress")
    assert selenium_count == 1, f"Selenium should appear once, found {selenium_count}"
    assert cypress_count == 1, f"Cypress should appear once, found {cypress_count}"
    print("PASS: test_merge_deduplicates_tools")


def test_evidence_discipline_maintained():
    """All enrichment items should have evidence strings."""
    enrichment = enrich_from_signals(
        company_name="EvidenceCo",
        job_postings=[
            {"title": "Senior SDET", "text": "Selenium, cross-browser testing, scale automation"},
        ],
        funding_stage="Series B",
        news_text="Cloud migration underway.",
    )

    for sig in enrichment["signals"]:
        assert sig.get("evidence"), f"Signal missing evidence: {sig}"

    for pain in enrichment["pain_hypotheses"]:
        assert pain.get("evidence"), f"Pain missing evidence: {pain}"

    for tech in enrichment.get("tech_stack_evidence", []):
        assert tech.get("evidence"), f"Tech stack item missing evidence: {tech}"

    print("PASS: test_evidence_discipline_maintained")


if __name__ == "__main__":
    test_detect_qa_role()
    test_detect_sdet()
    test_detect_non_qa_role()
    test_detect_tools_in_posting()
    test_detect_pain_in_posting()
    test_batch_analysis()
    test_high_hiring_velocity()
    test_funding_series_b()
    test_funding_seed()
    test_funding_auto_detect_stage()
    test_cloud_migration_signal()
    test_devops_transformation()
    test_no_transformation()
    test_unified_enrichment()
    test_enrichment_empty_input()
    test_merge_into_artifact()
    test_merge_deduplicates_tools()
    test_evidence_discipline_maintained()
    print("\n=== All 18 signal enrichment tests passed ===")
