"""
Outreach Command Center - Signal-Based Enrichment
Extracts actionable signals from job postings, funding data, tech stack mentions,
and other enrichment sources to feed into the research pipeline.

Signals detected:
- Job postings: QA/SDET/automation hiring = scaling pain, tool mentions = tech stack
- Funding events: Series A-D, revenue milestones = budget availability + growth mode
- Tech stack from job descriptions: competitor tools mentioned in requirements
- Hiring velocity: number of open QA roles = team scaling indicator
- Digital transformation: cloud migration, replatform, modernization signals

All signals include evidence strings for the evidence discipline.
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.agents.researcher import COMPETITOR_TOOLS, make_evidence, make_pain_hypothesis


# ─── JOB POSTING SIGNALS ────────────────────────────────────

# QA-related job title patterns
QA_JOB_PATTERNS = [
    r"qa\s+(?:engineer|analyst|lead|manager|director|architect)",
    r"sdet",
    r"test\s+(?:engineer|automation|architect|lead|manager)",
    r"quality\s+(?:engineer|assurance|lead|manager|director)",
    r"automation\s+(?:engineer|lead|architect|developer)",
    r"software\s+engineer\s+in\s+test",
]

# Senior QA titles (indicate serious investment)
SENIOR_QA_PATTERNS = [
    r"(?:senior|sr\.?|staff|principal|lead)\s+(?:sdet|qa|test|quality|automation)",
    r"(?:sdet|qa|test|quality|automation)\s+(?:lead|manager|director|head|architect)",
    r"(?:director|head|vp|manager)\s+(?:of\s+)?(?:qa|quality|test|automation)",
]

# Tool mentions in job descriptions
TOOL_PATTERNS = {
    "selenium": [r"\bselenium\b", r"\bwebdriver\b"],
    "cypress": [r"\bcypress\b", r"\bcypress\.io\b"],
    "playwright": [r"\bplaywright\b"],
    "appium": [r"\bappium\b"],
    "testcomplete": [r"\btestcomplete\b"],
    "katalon": [r"\bkatalon\b"],
    "tosca": [r"\btosca\b", r"\btricentis\b"],
    "browserstack": [r"\bbrowserstack\b"],
    "sauce labs": [r"\bsauce\s*labs?\b"],
    "lambdatest": [r"\blambdatest\b"],
    "testim": [r"\btestim\b"],
    "mabl": [r"\bmabl\b"],
    "ranorex": [r"\branorex\b"],
    "smartbear": [r"\bsmartbear\b"],
    "uft": [r"\buft\b", r"\bunified\s+functional\s+testing\b"],
    "jest": [r"\bjest\b"],
    "pytest": [r"\bpytest\b"],
    "junit": [r"\bjunit\b"],
    "testng": [r"\btestng\b"],
    "robot framework": [r"\brobot\s+framework\b"],
    "cucumber": [r"\bcucumber\b"],
    "postman": [r"\bpostman\b"],
    "rest assured": [r"\brest\s*assured\b"],
    "jmeter": [r"\bjmeter\b"],
    "k6": [r"\bk6\b"],
    "locust": [r"\blocust\b"],
}

# Pain indicators in job descriptions
PAIN_KEYWORDS = {
    "flaky_tests": ["flaky", "intermittent", "unstable tests", "test stability", "unreliable tests"],
    "slow_regression": ["regression", "slow pipeline", "long test cycles", "release velocity",
                        "deployment frequency", "ci/cd bottleneck"],
    "maintenance_overhead": ["test maintenance", "brittle tests", "framework migration",
                             "technical debt", "legacy tests", "refactor"],
    "scaling_automation": ["scale automation", "scaling automation", "scaling our automation",
                           "increase coverage", "expand test", "automation strategy",
                           "test strategy", "automation roadmap", "grow the automation"],
    "cross_platform": ["cross-browser", "cross-platform", "mobile testing", "responsive testing",
                       "multi-device", "ios and android"],
    "shift_left": ["shift left", "shift-left", "developer testing", "dev-led testing",
                   "test early", "quality ownership"],
}


def analyze_job_posting(posting_text: str, job_title: str = "",
                         company_name: str = "") -> dict:
    """Analyze a single job posting for signals.

    Args:
        posting_text: Full text of the job description.
        job_title: The job title.
        company_name: Company name for evidence strings.

    Returns:
        {"signals": [...], "tools_detected": [...], "pains_detected": [...],
         "is_qa_role": bool, "is_senior": bool, "evidence_source": str}
    """
    text_lower = posting_text.lower()
    title_lower = job_title.lower()
    evidence_source = f"from job posting: {job_title} at {company_name}" if company_name else f"from job posting: {job_title}"

    result = {
        "signals": [],
        "tools_detected": [],
        "pains_detected": [],
        "is_qa_role": False,
        "is_senior": False,
        "evidence_source": evidence_source,
    }

    # Check if it's a QA role
    for pattern in QA_JOB_PATTERNS:
        if re.search(pattern, title_lower) or re.search(pattern, text_lower[:500]):
            result["is_qa_role"] = True
            break

    # Check if it's a senior QA role
    for pattern in SENIOR_QA_PATTERNS:
        if re.search(pattern, title_lower):
            result["is_senior"] = True
            break

    # Detect tools mentioned
    for tool_name, patterns in TOOL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                result["tools_detected"].append(tool_name)
                break

    # Detect pain indicators
    for pain_type, keywords in PAIN_KEYWORDS.items():
        matched_keywords = [kw for kw in keywords if kw in text_lower]
        if matched_keywords:
            result["pains_detected"].append({
                "type": pain_type,
                "keywords_matched": matched_keywords,
                "evidence": f"{evidence_source} mentions: {', '.join(matched_keywords[:3])}",
            })

    # Build signals
    if result["is_qa_role"]:
        signal = {
            "signal_type": "hiring_qa",
            "description": f"Hiring for QA: {job_title}",
            "source": "job_posting",
            "strength": "high" if result["is_senior"] else "medium",
            "evidence": evidence_source,
        }
        result["signals"].append(signal)

    if result["tools_detected"]:
        # Competitor tools are higher-value signals
        competitors = [t for t in result["tools_detected"] if t in COMPETITOR_TOOLS]
        if competitors:
            result["signals"].append({
                "signal_type": "competitor_tool",
                "description": f"Job posting requires: {', '.join(competitors)}",
                "source": "job_posting",
                "strength": "high",
                "evidence": evidence_source,
            })

    for pain in result["pains_detected"]:
        result["signals"].append({
            "signal_type": f"pain_indicator_{pain['type']}",
            "description": f"Pain signal ({pain['type']}): {', '.join(pain['keywords_matched'][:2])}",
            "source": "job_posting",
            "strength": "medium",
            "evidence": pain["evidence"],
        })

    return result


def analyze_job_postings_batch(postings: list, company_name: str = "") -> dict:
    """Analyze multiple job postings for a company.

    Args:
        postings: List of dicts with 'title' and 'text' keys.
        company_name: Company name.

    Returns:
        {"total_qa_roles": int, "senior_qa_roles": int, "hiring_velocity": str,
         "all_tools": [...], "all_pains": [...], "signals": [...],
         "pain_hypotheses": [...], "tech_stack_evidence": [...]}
    """
    all_tools = set()
    all_pains = {}
    all_signals = []
    qa_count = 0
    senior_count = 0

    for posting in postings:
        title = posting.get("title", "")
        text = posting.get("text", posting.get("description", ""))
        result = analyze_job_posting(text, title, company_name)

        if result["is_qa_role"]:
            qa_count += 1
        if result["is_senior"]:
            senior_count += 1

        all_tools.update(result["tools_detected"])
        all_signals.extend(result["signals"])

        for pain in result["pains_detected"]:
            ptype = pain["type"]
            if ptype not in all_pains:
                all_pains[ptype] = pain
            else:
                # Merge keywords
                existing_kw = set(all_pains[ptype]["keywords_matched"])
                existing_kw.update(pain["keywords_matched"])
                all_pains[ptype]["keywords_matched"] = list(existing_kw)

    # Determine hiring velocity
    if qa_count >= 5:
        velocity = "high"
    elif qa_count >= 2:
        velocity = "medium"
    elif qa_count >= 1:
        velocity = "low"
    else:
        velocity = "none"

    # Build pain hypotheses from detected pains
    pain_hypotheses = []
    evidence_base = f"from job postings at {company_name}" if company_name else "from job postings"

    if qa_count >= 3:
        pain_hypotheses.append(
            make_pain_hypothesis(
                f"Rapidly scaling QA team ({qa_count} open QA roles)",
                min(0.9, 0.6 + qa_count * 0.05),
                f"{evidence_base}: {qa_count} QA-related job postings",
            ))

    for ptype, pain_data in all_pains.items():
        pain_labels = {
            "flaky_tests": "Flaky/unstable test suites causing pipeline failures",
            "slow_regression": "Slow regression cycles bottlenecking release velocity",
            "maintenance_overhead": "High test maintenance overhead and technical debt",
            "scaling_automation": "Need to scale test automation coverage",
            "cross_platform": "Cross-platform/cross-browser testing complexity",
            "shift_left": "Shifting testing left to developer-led quality ownership",
        }
        label = pain_labels.get(ptype, ptype.replace("_", " ").title())
        confidence = min(0.85, 0.5 + len(pain_data["keywords_matched"]) * 0.1)
        pain_hypotheses.append(
            make_pain_hypothesis(label, confidence, pain_data["evidence"]))

    # Build tech stack evidence items
    tech_stack_evidence = []
    for tool in all_tools:
        if tool in COMPETITOR_TOOLS:
            tech_stack_evidence.append(
                make_evidence(tool, f"{evidence_base}: mentioned in job requirements"))

    # Add hiring velocity signal
    if velocity != "none":
        all_signals.append({
            "signal_type": "hiring_velocity",
            "description": f"QA hiring velocity: {velocity} ({qa_count} open roles)",
            "source": "job_postings",
            "strength": velocity,
            "evidence": f"{evidence_base}: {qa_count} QA-related postings found",
        })

    return {
        "total_qa_roles": qa_count,
        "senior_qa_roles": senior_count,
        "hiring_velocity": velocity,
        "all_tools": sorted(all_tools),
        "all_pains": all_pains,
        "signals": all_signals,
        "pain_hypotheses": pain_hypotheses,
        "tech_stack_evidence": tech_stack_evidence,
    }


# ─── FUNDING SIGNAL ANALYSIS ─────────────────────────────────

FUNDING_STAGES = {
    "seed": {"strength": "low", "budget_signal": "early_stage"},
    "pre-seed": {"strength": "low", "budget_signal": "early_stage"},
    "series a": {"strength": "medium", "budget_signal": "growth_mode"},
    "series b": {"strength": "high", "budget_signal": "growth_mode"},
    "series c": {"strength": "high", "budget_signal": "scaling"},
    "series d": {"strength": "high", "budget_signal": "scaling"},
    "series e": {"strength": "medium", "budget_signal": "mature"},
    "ipo": {"strength": "medium", "budget_signal": "public"},
    "growth equity": {"strength": "high", "budget_signal": "scaling"},
    "pe": {"strength": "medium", "budget_signal": "mature"},
}


def analyze_funding(funding_text: str, company_name: str = "",
                     amount: str = "", stage: str = "",
                     date: str = "") -> dict:
    """Analyze funding information for signals.

    Args:
        funding_text: Free-text funding description.
        company_name: Company name.
        amount: Funding amount string (e.g., "$50M").
        stage: Funding stage (e.g., "Series B").
        date: Date string.

    Returns:
        {"signals": [...], "pain_hypotheses": [...], "stage_info": dict}
    """
    text_lower = funding_text.lower()
    evidence_base = f"from funding data: {company_name}" if company_name else "from funding data"

    signals = []
    pain_hypotheses = []

    # Detect funding stage from text if not provided
    detected_stage = stage.lower() if stage else ""
    if not detected_stage:
        for stage_key in FUNDING_STAGES:
            if stage_key in text_lower:
                detected_stage = stage_key
                break

    stage_info = FUNDING_STAGES.get(detected_stage, {"strength": "medium", "budget_signal": "unknown"})

    # Build funding signal
    desc_parts = []
    if detected_stage:
        desc_parts.append(detected_stage.title())
    if amount:
        desc_parts.append(amount)
    if date:
        desc_parts.append(f"on {date}")

    description = f"Funding: {' - '.join(desc_parts)}" if desc_parts else f"Funding activity: {funding_text[:100]}"

    signals.append({
        "signal_type": "funding",
        "description": description,
        "source": "funding_data",
        "strength": stage_info["strength"],
        "evidence": f"{evidence_base}: {description}",
    })

    # Growth-mode companies have scaling pains
    if stage_info["budget_signal"] in ("growth_mode", "scaling"):
        pain_hypotheses.append(
            make_pain_hypothesis(
                "Scaling engineering and QA to match growth-stage velocity",
                0.65,
                f"{evidence_base}: {detected_stage.title() if detected_stage else 'growth'} funding indicates rapid scaling",
            ))

    # Recent funding = budget available for new tools
    if stage_info["budget_signal"] in ("growth_mode", "scaling"):
        signals.append({
            "signal_type": "budget_available",
            "description": f"Post-funding budget likely available for tooling ({detected_stage.title() if detected_stage else 'growth'})",
            "source": "funding_data",
            "strength": stage_info["strength"],
            "evidence": f"{evidence_base}: recent funding suggests tooling budget",
        })

    return {
        "signals": signals,
        "pain_hypotheses": pain_hypotheses,
        "stage_info": stage_info,
        "detected_stage": detected_stage,
    }


# ─── TECH NEWS / TRANSFORMATION SIGNALS ──────────────────────

TRANSFORMATION_PATTERNS = {
    "cloud_migration": [
        r"cloud\s+migration", r"migrate\s+to\s+(?:aws|azure|gcp|cloud)",
        r"moving\s+to\s+(?:the\s+)?cloud", r"cloud\s+(?:first|native|adoption)",
    ],
    "platform_rewrite": [
        r"replatform", r"platform\s+(?:rewrite|migration|modernization)",
        r"monolith\s+to\s+microservices", r"legacy\s+(?:migration|modernization)",
    ],
    "devops_transformation": [
        r"devops\s+transformation", r"ci/cd\s+(?:pipeline|adoption|implementation)",
        r"continuous\s+(?:delivery|deployment|integration)",
        r"infrastructure\s+as\s+code",
    ],
    "digital_transformation": [
        r"digital\s+transformation", r"digitization", r"digital\s+(?:first|strategy)",
    ],
    "agile_transformation": [
        r"agile\s+transformation", r"adopting\s+agile", r"scrum\s+(?:adoption|implementation)",
        r"move\s+to\s+agile",
    ],
}


def analyze_company_news(news_text: str, company_name: str = "") -> dict:
    """Analyze company news/announcements for transformation signals.

    Args:
        news_text: Free-text news content.
        company_name: Company name.

    Returns:
        {"signals": [...], "pain_hypotheses": [...], "transformations_detected": [...]}
    """
    text_lower = news_text.lower()
    evidence_base = f"from company news: {company_name}" if company_name else "from company news"

    signals = []
    pain_hypotheses = []
    transformations = []

    for transform_type, patterns in TRANSFORMATION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                transformations.append(transform_type)

                label_map = {
                    "cloud_migration": "Cloud migration",
                    "platform_rewrite": "Platform rewrite/modernization",
                    "devops_transformation": "DevOps transformation",
                    "digital_transformation": "Digital transformation",
                    "agile_transformation": "Agile transformation",
                }
                label = label_map.get(transform_type, transform_type)

                signals.append({
                    "signal_type": "digital_transformation",
                    "description": f"{label} underway",
                    "source": "company_news",
                    "strength": "high",
                    "evidence": f"{evidence_base}: mentions {label.lower()}",
                })

                pain_hypotheses.append(
                    make_pain_hypothesis(
                        f"Test automation complexity increasing due to {label.lower()}",
                        0.7,
                        f"{evidence_base}: {label.lower()} creates new testing surfaces",
                    ))
                break  # Only one signal per transformation type

    return {
        "signals": signals,
        "pain_hypotheses": pain_hypotheses,
        "transformations_detected": list(set(transformations)),
    }


# ─── UNIFIED ENRICHMENT PIPELINE ─────────────────────────────

def enrich_from_signals(company_name: str = "",
                         job_postings: list = None,
                         funding_text: str = "",
                         funding_amount: str = "",
                         funding_stage: str = "",
                         funding_date: str = "",
                         news_text: str = "") -> dict:
    """Run all signal enrichment and return unified results.

    This is the main entry point. Feed it whatever data you have and
    it returns structured signals ready to merge into a ResearchArtifact.

    Args:
        company_name: Company name.
        job_postings: List of dicts with 'title' and 'text'/'description'.
        funding_text: Free-text funding info.
        funding_amount: e.g., "$50M".
        funding_stage: e.g., "Series B".
        funding_date: Date string.
        news_text: Company news text.

    Returns:
        {"signals": [...], "pain_hypotheses": [...], "tech_stack_evidence": [...],
         "hiring_velocity": str, "total_qa_roles": int,
         "transformations": [...], "enrichment_summary": str}
    """
    all_signals = []
    all_pains = []
    all_tech = []
    transformations = []
    hiring_velocity = "none"
    total_qa_roles = 0

    # Job posting analysis
    if job_postings:
        jp_result = analyze_job_postings_batch(job_postings, company_name)
        all_signals.extend(jp_result["signals"])
        all_pains.extend(jp_result["pain_hypotheses"])
        all_tech.extend(jp_result["tech_stack_evidence"])
        hiring_velocity = jp_result["hiring_velocity"]
        total_qa_roles = jp_result["total_qa_roles"]

    # Funding analysis
    if funding_text or funding_stage:
        fund_result = analyze_funding(
            funding_text, company_name, funding_amount, funding_stage, funding_date)
        all_signals.extend(fund_result["signals"])
        all_pains.extend(fund_result["pain_hypotheses"])

    # News/transformation analysis
    if news_text:
        news_result = analyze_company_news(news_text, company_name)
        all_signals.extend(news_result["signals"])
        all_pains.extend(news_result["pain_hypotheses"])
        transformations = news_result["transformations_detected"]

    # Deduplicate signals by type+description
    seen = set()
    unique_signals = []
    for sig in all_signals:
        key = f"{sig['signal_type']}:{sig['description'][:50]}"
        if key not in seen:
            seen.add(key)
            unique_signals.append(sig)

    # Build summary
    parts = []
    if total_qa_roles:
        parts.append(f"{total_qa_roles} QA roles open")
    if all_tech:
        tools = [t["value"] for t in all_tech]
        parts.append(f"uses {', '.join(tools)}")
    if funding_stage:
        parts.append(f"{funding_stage} funding")
    if transformations:
        parts.append(f"{', '.join(t.replace('_', ' ') for t in transformations)}")
    summary = "; ".join(parts) if parts else "No enrichment signals detected"

    return {
        "signals": unique_signals,
        "pain_hypotheses": all_pains,
        "tech_stack_evidence": all_tech,
        "hiring_velocity": hiring_velocity,
        "total_qa_roles": total_qa_roles,
        "transformations": transformations,
        "enrichment_summary": summary,
    }


def merge_enrichment_into_artifact(artifact: dict, enrichment: dict) -> dict:
    """Merge enrichment signals into an existing ResearchArtifact.

    Non-destructive: adds new signals/pains/tech but doesn't overwrite
    existing data. Returns the modified artifact.

    Args:
        artifact: Existing ResearchArtifact dict.
        enrichment: Output from enrich_from_signals().

    Returns:
        The artifact dict with enrichment data merged in.
    """
    # Merge tech stack evidence
    existing_tools = set()
    for item in artifact.get("signals", {}).get("tech_stack", []):
        val = item.get("value", "") if isinstance(item, dict) else str(item)
        existing_tools.add(val.lower())

    for tech_ev in enrichment.get("tech_stack_evidence", []):
        if tech_ev["value"].lower() not in existing_tools:
            artifact["signals"]["tech_stack"].append(tech_ev)
            existing_tools.add(tech_ev["value"].lower())

    # Merge intent signals
    for sig in enrichment.get("signals", []):
        if sig["signal_type"] in ("funding", "budget_available", "digital_transformation",
                                   "hiring_qa", "hiring_velocity"):
            artifact["signals"]["intent_signals"].append(
                make_evidence(sig["description"], sig.get("evidence", "from signal enrichment")))

        if sig["signal_type"] in ("hiring_qa", "hiring_velocity", "funding",
                                   "digital_transformation", "competitor_tool"):
            artifact["signals"]["triggers"].append(
                make_evidence(
                    f"{sig['signal_type'].replace('_', ' ')}: {sig['description']}",
                    sig.get("evidence", "from signal enrichment"),
                ))

    # Merge pain hypotheses (avoid duplicates by checking pain text)
    existing_pains = set()
    for p in artifact.get("pains", {}).get("hypothesized_pains", []):
        existing_pains.add(p.get("pain", "").lower()[:50])

    for pain in enrichment.get("pain_hypotheses", []):
        pain_key = pain.get("pain", "").lower()[:50]
        if pain_key not in existing_pains:
            artifact["pains"]["hypothesized_pains"].append(pain)
            existing_pains.add(pain_key)

    # Update metadata
    if "signal_enrichment" not in artifact.get("metadata", {}).get("data_sources", []):
        artifact["metadata"]["data_sources"].append("signal_enrichment")

    # Add enrichment summary to ICP fit reasons
    summary = enrichment.get("enrichment_summary", "")
    if summary and summary != "No enrichment signals detected":
        artifact["icp_fit"]["fit_reasons"].append(f"Enrichment: {summary}")

    return artifact
