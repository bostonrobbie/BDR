"""
Outreach Command Center - Researcher Agent
Two-source research extraction: LinkedIn profiles + external company data.

LinkedIn data is extracted via Chrome MCP (Claude reads the profile).
Company data is extracted via WebSearch/WebFetch or parallel Task subagents.
This module provides structured extraction, caching, and signal detection.
"""

import json
import os
import sys
import re
from datetime import datetime, timedelta
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.db import models


# ─── COMPETITOR TOOLS TO DETECT ───────────────────────────────

COMPETITOR_TOOLS = {
    "selenium", "cypress", "playwright", "tosca", "katalon", "testim",
    "mabl", "sauce labs", "browserstack", "lambdatest", "appium",
    "ranorex", "telerik", "smartbear", "tricentis", "qmetry",
    "testcomplete", "uft", "eggplant", "perfecto",
}

# ─── VERTICAL CLASSIFICATION ─────────────────────────────────

VERTICAL_KEYWORDS = {
    "FinTech": ["fintech", "payments", "crypto", "blockchain", "lending", "neobank",
                "buy now pay later", "bnpl", "digital wallet", "remittance"],
    "FinServ": ["bank", "banking", "credit union", "mortgage", "wealth management",
                "asset management", "brokerage", "financial services", "capital markets",
                "investment", "insurance carrier"],
    "Healthcare": ["health", "medical", "clinical", "patient", "telehealth",
                   "healthtech", "digital health", "ehr", "emr", "health insurance"],
    "SaaS": ["saas", "software as a service", "cloud platform", "b2b software",
             "enterprise software", "developer tools"],
    "E-Commerce": ["e-commerce", "ecommerce", "online retail", "marketplace",
                   "shopping", "catalog", "direct to consumer", "d2c"],
    "InsurTech": ["insurtech", "insurance technology", "digital insurance"],
    "Insurance": ["insurance", "reinsurance", "underwriting", "claims"],
    "Tech": ["technology", "software", "internet", "platform", "infrastructure"],
    "Telecom": ["telecom", "telecommunications", "wireless", "mobile network"],
    "Pharma": ["pharmaceutical", "pharma", "drug", "biotech", "life sciences"],
    "Retail": ["retail", "store", "consumer goods", "cpg"],
}


def classify_vertical(company_description: str, industry: str = "") -> str:
    """Classify a company into a vertical based on description and industry."""
    text = f"{company_description} {industry}".lower()

    scores = {}
    for vertical, keywords in VERTICAL_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[vertical] = score

    if not scores:
        return "Tech"  # Default

    return max(scores, key=scores.get)


# ─── RESEARCH CACHING ────────────────────────────────────────

def check_company_cache(company_name: str, max_age_days: int = 30) -> Optional[dict]:
    """Check if we have fresh company research cached.

    Returns cached research dict if fresh, None if stale or missing.
    """
    conn = models.get_db()
    row = conn.execute("""
        SELECT rs.* FROM research_snapshots rs
        JOIN accounts a ON rs.account_id = a.id
        WHERE LOWER(a.name) = ? AND rs.entity_type = 'company'
        ORDER BY rs.created_at DESC LIMIT 1
    """, (company_name.lower(),)).fetchone()
    conn.close()

    if not row:
        return None

    # Check freshness
    created_at = row["created_at"]
    if created_at:
        try:
            research_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            cutoff = datetime.utcnow() - timedelta(days=max_age_days)
            if research_date.replace(tzinfo=None) < cutoff:
                return None  # Stale
        except (ValueError, TypeError):
            pass

    r = dict(row)
    return {
        "description": r.get("summary", ""),
        "known_tools": json.loads(r["tech_stack_signals"]) if r.get("tech_stack_signals") else [],
        "recent_news": r.get("company_news", ""),
        "hiring_signals": r.get("hiring_signals", ""),
    }


def check_person_cache(contact_id: str, max_age_days: int = 30) -> Optional[dict]:
    """Check if we have fresh person research cached."""
    conn = models.get_db()
    row = conn.execute("""
        SELECT * FROM research_snapshots
        WHERE contact_id = ? AND entity_type = 'person'
        ORDER BY created_at DESC LIMIT 1
    """, (contact_id,)).fetchone()
    conn.close()

    if not row:
        return None

    created_at = row["created_at"]
    if created_at:
        try:
            research_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            cutoff = datetime.utcnow() - timedelta(days=max_age_days)
            if research_date.replace(tzinfo=None) < cutoff:
                return None
        except (ValueError, TypeError):
            pass

    r = dict(row)
    return {
        "headline": r.get("headline", ""),
        "about": r.get("summary", ""),
        "current_role_description": r.get("responsibilities", ""),
        "career_history": json.loads(r["career_history"]) if r.get("career_history") else [],
        "recently_hired": False,
        "tenure_months": None,
    }


# ─── PERSON RESEARCH STRUCTURING ──────────────────────────────

def structure_person_research(raw_text: str, contact_data: dict = None) -> dict:
    """Structure raw profile text into a research snapshot.

    This processes the text Claude extracted from a LinkedIn profile
    via get_page_text or read_page and returns structured data.

    Claude passes in the raw text; this function extracts key fields.
    Claude may also pass pre-structured data from its own interpretation.
    """
    result = {
        "headline": "",
        "about": "",
        "current_role_description": "",
        "tenure_months": None,
        "recently_hired": False,
        "career_history": [],
        "key_responsibilities": [],
        "recent_activity": "",
        "skills_endorsements": [],
        "education": [],
        "extracted_at": datetime.utcnow().isoformat(),
        "source": "linkedin_profile",
    }

    # If Claude already structured the data, merge it
    if contact_data:
        for key in result:
            if key in contact_data and contact_data[key]:
                result[key] = contact_data[key]

    # Tenure check: if tenure_months < 6, mark as recently hired
    if result["tenure_months"] and result["tenure_months"] < 6:
        result["recently_hired"] = True

    return result


# ─── COMPANY RESEARCH STRUCTURING ─────────────────────────────

def structure_company_research(raw_data: dict) -> dict:
    """Structure raw company research data.

    raw_data can come from Claude's interpretation of company website,
    news articles, job postings, or engineering blogs.
    """
    result = {
        "description": raw_data.get("description", ""),
        "employee_count": raw_data.get("employee_count"),
        "employee_band": raw_data.get("employee_band", ""),
        "industry": raw_data.get("industry", ""),
        "vertical": "",
        "products": raw_data.get("products", []),
        "known_tools": [],
        "tech_stack": raw_data.get("tech_stack", []),
        "recent_news": raw_data.get("recent_news", ""),
        "hiring_signals": raw_data.get("hiring_signals", ""),
        "funding_info": raw_data.get("funding_info", ""),
        "key_metrics": raw_data.get("key_metrics", {}),
        "sources": raw_data.get("sources", []),
        "extracted_at": datetime.utcnow().isoformat(),
    }

    # Classify vertical
    result["vertical"] = classify_vertical(
        result["description"],
        result["industry"]
    )

    # Detect competitor tools from text
    all_text = json.dumps(raw_data).lower()
    detected_tools = [tool for tool in COMPETITOR_TOOLS if tool in all_text]
    result["known_tools"] = detected_tools

    # Infer employee band from count
    emp = result["employee_count"]
    if emp and not result["employee_band"]:
        if emp <= 50:
            result["employee_band"] = "1-50"
        elif emp <= 200:
            result["employee_band"] = "51-200"
        elif emp <= 500:
            result["employee_band"] = "201-500"
        elif emp <= 1000:
            result["employee_band"] = "501-1000"
        elif emp <= 5000:
            result["employee_band"] = "1001-5000"
        elif emp <= 10000:
            result["employee_band"] = "5001-10000"
        elif emp <= 50000:
            result["employee_band"] = "10001-50000"
        else:
            result["employee_band"] = "50000+"

    return result


# ─── SIGNAL DETECTION ─────────────────────────────────────────

def detect_signals(company_research: dict, person_research: dict = None) -> list:
    """Detect buyer intent and other signals from research data.

    Returns list of signal dicts ready for models.create_signal().
    """
    signals = []

    # Hiring signals (QA job postings)
    hiring = company_research.get("hiring_signals", "").lower()
    if any(term in hiring for term in ["qa", "quality", "test", "sdet", "automation"]):
        signals.append({
            "signal_type": "hiring_qa",
            "description": f"QA-related hiring: {company_research.get('hiring_signals', '')}",
            "source": "job_postings",
            "strength": "medium",
        })

    # Funding signals
    funding = company_research.get("funding_info", "")
    if funding:
        signals.append({
            "signal_type": "funding",
            "description": f"Recent funding: {funding}",
            "source": "news",
            "strength": "medium",
        })

    # Digital transformation signals
    news = company_research.get("recent_news", "").lower()
    if any(term in news for term in ["digital transformation", "migration", "modernization",
                                      "cloud", "platform", "replatform"]):
        signals.append({
            "signal_type": "digital_transformation",
            "description": f"Transformation signal: {company_research.get('recent_news', '')}",
            "source": "news",
            "strength": "high",
        })

    # Competitor tool usage
    known_tools = company_research.get("known_tools", [])
    if known_tools:
        signals.append({
            "signal_type": "competitor_tool",
            "description": f"Uses: {', '.join(known_tools)}",
            "source": "job_postings",
            "strength": "high",
        })

    # Recently hired signal (from person research)
    if person_research and person_research.get("recently_hired"):
        signals.append({
            "signal_type": "recently_hired",
            "description": "New to role (< 6 months)",
            "source": "linkedin",
            "strength": "medium",
        })

    return signals


# ─── RESEARCH SUMMARY FOR MESSAGE WRITER ──────────────────────

def build_research_context(contact_id: str) -> dict:
    """Build a complete research context for the message writer.

    Aggregates person research, company research, and signals into
    a single dict that the message writer uses for personalization.
    """
    contact = models.get_contact(contact_id)
    if not contact:
        return {"error": "Contact not found"}

    account = models.get_account(contact["account_id"]) if contact.get("account_id") else {}

    # Get person research
    person = check_person_cache(contact_id) or {}

    # Get company research
    company = check_company_cache(account.get("name", "")) if account else {}

    # Get signals
    conn = models.get_db()
    signal_rows = conn.execute(
        "SELECT * FROM signals WHERE contact_id=? OR account_id=? ORDER BY detected_at DESC",
        (contact_id, contact.get("account_id", ""))
    ).fetchall()
    conn.close()
    signals = [dict(r) for r in signal_rows]

    return {
        "contact": contact,
        "account": account or {},
        "person_research": person,
        "company_research": company or {},
        "signals": signals,
        "has_buyer_intent": any(s.get("signal_type") == "buyer_intent" for s in signals),
        "known_tools": (company or {}).get("known_tools", []),
        "vertical": (company or {}).get("vertical", account.get("industry", "Tech")),
        "recently_hired": person.get("recently_hired", contact.get("recently_hired", False)),
    }
