"""
Outreach Command Center - Researcher Agent
Input-driven research extraction that produces validated ResearchArtifacts.

Sources: CRM/CSV prospect data, local cached enrichment, internal notes.
No web lookups. Every non-trivial claim requires an evidence string.

Outputs a typed ResearchArtifact with evidence discipline and QA validation.
"""

import json
import os
import sys
import re
from datetime import datetime, timedelta
from typing import Optional, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.db import models


# ─── VERTICAL PAIN LIBRARY ──────────────────────────────────────

_VERTICAL_PAINS_PATH = os.path.join(os.path.dirname(__file__), "../../config/vertical_pains.json")
_vertical_pains_cache = None


def _load_vertical_pains(path: str = None) -> dict:
    """Load the per-vertical pain library from config."""
    global _vertical_pains_cache
    if _vertical_pains_cache is not None and path is None:
        return _vertical_pains_cache
    p = path or _VERTICAL_PAINS_PATH
    try:
        with open(p, "r") as f:
            _vertical_pains_cache = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        _vertical_pains_cache = {"verticals": {}}
    return _vertical_pains_cache


def get_vertical_pains(vertical: str, known_tools: list = None) -> list:
    """Get curated pain hypotheses for a specific vertical.

    Returns pain hypotheses from the vertical pain library with confidence
    boosted if the prospect's known tools match the vertical's typical tools.

    Args:
        vertical: Industry vertical name (e.g., "FinTech", "Healthcare").
        known_tools: List of tools the prospect uses (for confidence boosting).

    Returns:
        List of pain hypothesis dicts with pain, confidence, evidence, tags.
    """
    known_tools = known_tools or []
    config = _load_vertical_pains()
    verticals = config.get("verticals", {})

    # Try exact match first, then case-insensitive match
    vertical_data = verticals.get(vertical)
    if not vertical_data:
        for k, v in verticals.items():
            if k.lower() == vertical.lower():
                vertical_data = v
                break
    if not vertical_data:
        return []

    pains = []
    typical_tools = [t.lower() for t in vertical_data.get("typical_tools", [])]
    has_tool_overlap = any(t.lower() in typical_tools for t in known_tools)

    for p in vertical_data.get("pains", []):
        conf = p["confidence"]
        # Boost confidence if prospect uses a typical tool for this vertical
        if has_tool_overlap:
            conf = min(1.0, conf + 0.1)
        pains.append({
            "pain": p["pain"],
            "confidence": round(conf, 2),
            "evidence": f"from vertical pain library: {vertical}",
            "tags": p.get("tags", []),
        })

    return pains


# ─── RESEARCH ARTIFACT SCHEMA ──────────────────────────────────

# Default guardrails that must always be present
DEFAULT_MUST_NOT_CLAIM = [
    "No claims of having read private docs",
    "No claims of seeing recent news unless from cached research",
    "No claims of exact metrics unless provided in CRM data",
]


def make_evidence(value: str, source: str) -> dict:
    """Create an evidence-tracked field.

    Args:
        value: The claim or data point.
        source: One of:
          - "from CRM field: <field_name>"
          - "from local enrichment field: <field_name>"
          - "from cached research: <snapshot_id>"
          - "unknown - hypothesis only"
    """
    return {"value": value, "evidence": source}


def make_pain_hypothesis(pain: str, confidence: float, evidence: str) -> dict:
    """Create a pain hypothesis with confidence and evidence.

    Args:
        pain: Description of the hypothesized pain point.
        confidence: 0.0 to 1.0.
        evidence: Evidence string (required if confidence > 0.7).
    """
    return {
        "pain": pain,
        "confidence": round(min(1.0, max(0.0, confidence)), 2),
        "evidence": evidence,
    }


def make_hook(hook: str, evidence_field: str) -> dict:
    """Create a personalization hook with evidence citation.

    Args:
        hook: The personalization hook text.
        evidence_field: Which input field this is grounded in.
    """
    return {"hook": hook, "evidence_field": evidence_field}


def build_empty_artifact() -> dict:
    """Return an empty ResearchArtifact skeleton."""
    return {
        "prospect": {
            "full_name": "",
            "title": "",
            "seniority": "",
            "function": "",
            "linkedin_url": "",
            "company_name": "",
            "company_domain": "",
        },
        "company": {
            "industry": "",
            "size_band": "",
            "geo": "",
            "product_summary": "",
        },
        "signals": {
            "tech_stack": [],
            "intent_signals": [],
            "triggers": [],
        },
        "icp_fit": {
            "fit_summary": "",
            "fit_reasons": [],
            "disqualifiers": [],
        },
        "pains": {
            "hypothesized_pains": [],
        },
        "personalization": {
            "hooks": [],
            "mutual_context": [],
        },
        "constraints": {
            "must_not_claim": list(DEFAULT_MUST_NOT_CLAIM),
        },
        "metadata": {
            "created_at": datetime.utcnow().isoformat(),
            "data_sources": [],
            "research_quality_score": 0.0,
        },
    }


# ─── RESEARCH ARTIFACT VALIDATOR (QA) ────────────────────────────

class ResearchValidationError:
    """A single validation failure."""
    def __init__(self, field: str, message: str, severity: str = "error"):
        self.field = field
        self.message = message
        self.severity = severity  # "error" or "warning"

    def to_dict(self):
        return {"field": self.field, "message": self.message, "severity": self.severity}


def validate_research_artifact(artifact: dict) -> dict:
    """Validate a ResearchArtifact for evidence discipline.

    Returns:
        {"valid": bool, "errors": [...], "warnings": [...]}

    Rejects if:
    - hooks are present without evidence
    - pains have confidence > 0.7 without evidence
    - tech stack is populated without evidence
    - must_not_claim is empty
    """
    errors = []
    warnings = []

    # Check must_not_claim is not empty
    constraints = artifact.get("constraints", {})
    must_not = constraints.get("must_not_claim", [])
    if not must_not:
        errors.append(ResearchValidationError(
            "constraints.must_not_claim",
            "must_not_claim is empty. Must include default guardrails.",
        ))

    # Check hooks have evidence
    hooks = artifact.get("personalization", {}).get("hooks", [])
    for i, hook in enumerate(hooks):
        ev = hook.get("evidence_field", "")
        if not ev or ev == "unknown - hypothesis only":
            errors.append(ResearchValidationError(
                f"personalization.hooks[{i}]",
                f"Hook '{hook.get('hook', '')[:50]}' has no evidence field.",
            ))

    # Check pain confidence vs evidence
    pains = artifact.get("pains", {}).get("hypothesized_pains", [])
    for i, pain in enumerate(pains):
        conf = pain.get("confidence", 0)
        ev = pain.get("evidence", "")
        if conf > 0.7 and (not ev or ev == "unknown - hypothesis only"):
            errors.append(ResearchValidationError(
                f"pains.hypothesized_pains[{i}]",
                f"Pain '{pain.get('pain', '')[:50]}' has confidence {conf} but no evidence.",
            ))
        if conf > 0.5 and (not ev or ev == "unknown - hypothesis only"):
            warnings.append(ResearchValidationError(
                f"pains.hypothesized_pains[{i}]",
                f"Pain '{pain.get('pain', '')[:50]}' has confidence {conf} without evidence (consider lowering).",
                severity="warning",
            ))

    # Check tech stack has evidence
    tech = artifact.get("signals", {}).get("tech_stack", [])
    for i, item in enumerate(tech):
        if isinstance(item, dict):
            ev = item.get("evidence", "")
            if not ev or ev == "unknown - hypothesis only":
                errors.append(ResearchValidationError(
                    f"signals.tech_stack[{i}]",
                    f"Tech stack item '{item.get('value', '')[:50]}' has no evidence.",
                ))
        elif isinstance(item, str):
            # Plain strings without evidence are not allowed
            errors.append(ResearchValidationError(
                f"signals.tech_stack[{i}]",
                f"Tech stack item '{item[:50]}' is a plain string; must be {{value, evidence}} dict.",
            ))

    # Check prospect has basic fields
    prospect = artifact.get("prospect", {})
    if not prospect.get("full_name"):
        errors.append(ResearchValidationError("prospect.full_name", "Missing prospect name."))
    if not prospect.get("company_name"):
        warnings.append(ResearchValidationError(
            "prospect.company_name", "Missing company name.", severity="warning"))

    valid = len(errors) == 0
    return {
        "valid": valid,
        "errors": [e.to_dict() for e in errors],
        "warnings": [w.to_dict() for w in warnings],
        "error_count": len(errors),
        "warning_count": len(warnings),
    }


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


# ─── RESEARCH ARTIFACT BUILDER (input-driven) ────────────────

def _infer_function(title: str) -> str:
    """Infer job function from title."""
    t = title.lower()
    if any(kw in t for kw in ["qa", "quality", "test", "sdet", "automation"]):
        return "QA/Testing"
    if any(kw in t for kw in ["engineering", "software", "developer", "cto", "architect"]):
        return "Engineering"
    if any(kw in t for kw in ["devops", "platform", "infrastructure", "sre", "release"]):
        return "DevOps/Platform"
    if any(kw in t for kw in ["product", "program"]):
        return "Product"
    return "Other"


def _infer_seniority(title: str, seniority_field: str = "") -> str:
    """Infer seniority from title or explicit field."""
    if seniority_field:
        return seniority_field
    t = title.lower()
    if any(kw in t for kw in ["chief", "cto", "ceo", "coo", "cio"]):
        return "c-suite"
    if any(kw in t for kw in ["vp", "vice president"]):
        return "vp"
    if any(kw in t for kw in ["director", "head of"]):
        return "director"
    if any(kw in t for kw in ["manager", "lead"]):
        return "manager"
    if any(kw in t for kw in ["senior", "sr", "principal", "staff"]):
        return "senior"
    return "individual"


def build_research_artifact(contact: dict, account: dict = None,
                            person_research: dict = None,
                            company_research: dict = None,
                            signals: list = None) -> dict:
    """Build a validated ResearchArtifact from available input data.

    Uses ONLY:
    - contact/account row fields (CRM data)
    - cached person_research and company_research
    - detected signals

    No web lookups. Every claim is evidence-tagged.

    Returns:
        {"artifact": ResearchArtifact, "validation": validation_result}
    """
    account = account or {}
    person_research = person_research or {}
    company_research = company_research or {}
    signals = signals or []

    artifact = build_empty_artifact()
    data_sources = []

    # ── Prospect fields ──
    first = contact.get("first_name", "")
    last = contact.get("last_name", "")
    title = contact.get("title", "")
    artifact["prospect"]["full_name"] = f"{first} {last}".strip()
    artifact["prospect"]["title"] = title
    artifact["prospect"]["seniority"] = _infer_seniority(
        title, contact.get("seniority_level", ""))
    artifact["prospect"]["function"] = _infer_function(title)
    artifact["prospect"]["linkedin_url"] = contact.get("linkedin_url", "")
    artifact["prospect"]["company_name"] = contact.get("company_name", "") or account.get("name", "")
    artifact["prospect"]["company_domain"] = account.get("domain", "")
    data_sources.append("CRM contact record")

    # ── Company fields ──
    if account:
        artifact["company"]["industry"] = account.get("industry", "")
        artifact["company"]["size_band"] = account.get("employee_band", "")
        artifact["company"]["geo"] = account.get("hq_location", "")
        data_sources.append("CRM account record")

    if company_research:
        if company_research.get("description"):
            artifact["company"]["product_summary"] = company_research["description"]
        if company_research.get("industry") and not artifact["company"]["industry"]:
            artifact["company"]["industry"] = company_research["industry"]
        data_sources.append("cached company research")

    # ── Signals: tech stack (evidence-tagged) ──
    known_tools_raw = company_research.get("known_tools", [])
    if isinstance(known_tools_raw, str):
        try:
            known_tools_raw = json.loads(known_tools_raw)
        except (json.JSONDecodeError, TypeError):
            known_tools_raw = []
    # Also check account.known_tools
    account_tools_raw = account.get("known_tools", "[]")
    if isinstance(account_tools_raw, str):
        try:
            account_tools_raw = json.loads(account_tools_raw)
        except (json.JSONDecodeError, TypeError):
            account_tools_raw = []

    all_tools = set()
    for tool in known_tools_raw:
        if isinstance(tool, str) and tool.strip():
            all_tools.add(tool.strip())
    for tool in account_tools_raw:
        if isinstance(tool, str) and tool.strip():
            all_tools.add(tool.strip())

    for tool in all_tools:
        source = "from local enrichment field: known_tools"
        artifact["signals"]["tech_stack"].append(make_evidence(tool, source))

    # ── Signals: intent and triggers ──
    for sig in signals:
        sig_type = sig.get("signal_type", "")
        sig_desc = sig.get("description", "")
        sig_source = sig.get("source", "unknown")

        if sig_type in ("buyer_intent", "funding", "digital_transformation", "hiring_qa"):
            artifact["signals"]["intent_signals"].append(
                make_evidence(sig_desc, f"from local enrichment field: signal_{sig_type}"))
        if sig_type in ("recently_hired", "funding", "digital_transformation", "hiring_qa", "competitor_tool"):
            trigger_label = {
                "recently_hired": "job change",
                "funding": "funding event",
                "digital_transformation": "digital transformation",
                "hiring_qa": "QA hiring",
                "competitor_tool": "competitor tool usage",
            }.get(sig_type, sig_type)
            artifact["signals"]["triggers"].append(
                make_evidence(f"{trigger_label}: {sig_desc}", f"from local enrichment field: signal_{sig_type}"))

    if account.get("buyer_intent"):
        artifact["signals"]["intent_signals"].append(
            make_evidence("Buyer intent flag set", "from CRM field: buyer_intent"))

    # ── ICP fit ──
    vertical = classify_vertical(
        artifact["company"].get("product_summary", ""),
        artifact["company"].get("industry", ""))
    fit_reasons = []
    disqualifiers = []

    seniority = artifact["prospect"]["seniority"]
    function = artifact["prospect"]["function"]
    if function == "QA/Testing":
        fit_reasons.append("Prospect is in QA/Testing function")
    elif function == "Engineering":
        fit_reasons.append("Prospect is in Engineering (secondary ICP)")
    else:
        disqualifiers.append(f"Function '{function}' is not primary ICP")

    if seniority in ("director", "vp", "c-suite", "head"):
        fit_reasons.append(f"Senior role: {seniority}")
    elif seniority in ("manager", "senior"):
        fit_reasons.append(f"Mid-level: {seniority}")
    else:
        disqualifiers.append(f"Seniority '{seniority}' may lack decision-making authority")

    size = artifact["company"].get("size_band", "")
    if size in ("201-500", "501-1000", "1001-5000"):
        fit_reasons.append(f"Company size {size} is sweet spot")
    elif size in ("50000+", "1-50"):
        disqualifiers.append(f"Company size {size} is outside sweet spot")

    artifact["icp_fit"]["fit_summary"] = (
        f"{'Strong' if len(fit_reasons) >= 3 else 'Moderate' if len(fit_reasons) >= 2 else 'Weak'} "
        f"ICP fit: {function} {seniority} at {vertical} company"
    )
    artifact["icp_fit"]["fit_reasons"] = fit_reasons
    artifact["icp_fit"]["disqualifiers"] = disqualifiers

    # ── Pain hypotheses ──
    if all_tools:
        tool_list = ", ".join(all_tools)
        artifact["pains"]["hypothesized_pains"].append(
            make_pain_hypothesis(
                f"Test maintenance overhead with {tool_list}",
                0.8 if any(t.lower() in ("selenium", "cypress", "playwright") for t in all_tools) else 0.5,
                f"from local enrichment field: known_tools ({tool_list})"
            ))

    if function == "QA/Testing" and seniority in ("director", "vp", "manager", "head"):
        artifact["pains"]["hypothesized_pains"].append(
            make_pain_hypothesis(
                "Scaling test automation while managing team bandwidth",
                0.6,
                f"from CRM field: title ({title})"
            ))

    industry = artifact["company"]["industry"].lower()
    if any(v in industry for v in ["fintech", "finserv", "banking", "insurance"]):
        artifact["pains"]["hypothesized_pains"].append(
            make_pain_hypothesis(
                "Regression testing across compliance-sensitive financial workflows",
                0.5,
                f"from CRM field: industry ({artifact['company']['industry']})"
            ))
    elif any(v in industry for v in ["healthcare", "pharma", "health"]):
        artifact["pains"]["hypothesized_pains"].append(
            make_pain_hypothesis(
                "Compliance-heavy regression cycles in regulated environment",
                0.5,
                f"from CRM field: industry ({artifact['company']['industry']})"
            ))

    # F7: Enrich with per-vertical pain library
    vertical_pains = get_vertical_pains(vertical, all_tools)
    existing_pain_texts = {p["pain"].lower() for p in artifact["pains"]["hypothesized_pains"]}
    for vp in vertical_pains:
        # Avoid duplicating pain hypotheses already added from CRM signals
        if vp["pain"].lower() not in existing_pain_texts:
            artifact["pains"]["hypothesized_pains"].append(
                make_pain_hypothesis(vp["pain"], vp["confidence"], vp["evidence"])
            )
            existing_pain_texts.add(vp["pain"].lower())

    # Add a general fallback pain if none yet
    if not artifact["pains"]["hypothesized_pains"]:
        artifact["pains"]["hypothesized_pains"].append(
            make_pain_hypothesis(
                "Test maintenance and flaky tests slowing release velocity",
                0.3,
                "unknown - hypothesis only"
            ))

    # ── Personalization hooks ──
    if title:
        artifact["personalization"]["hooks"].append(
            make_hook(f"Role as {title}", f"from CRM field: title"))

    company_name = artifact["prospect"]["company_name"]
    if company_name:
        artifact["personalization"]["hooks"].append(
            make_hook(f"Work at {company_name}", f"from CRM field: company_name"))

    if person_research.get("headline"):
        artifact["personalization"]["hooks"].append(
            make_hook(
                f"LinkedIn headline: {person_research['headline']}",
                "from local enrichment field: person_research.headline"))
        data_sources.append("cached person research")

    if person_research.get("recently_hired"):
        artifact["personalization"]["hooks"].append(
            make_hook("Recently started in role (< 6 months)",
                      "from local enrichment field: person_research.recently_hired"))

    if person_research.get("about"):
        # Extract a short snippet for personalization
        about_snippet = person_research["about"][:100]
        artifact["personalization"]["hooks"].append(
            make_hook(f"About: {about_snippet}",
                      "from local enrichment field: person_research.about"))

    # ── Constraints ──
    artifact["constraints"]["must_not_claim"] = list(DEFAULT_MUST_NOT_CLAIM)
    if not person_research:
        artifact["constraints"]["must_not_claim"].append(
            "No claims about prospect's LinkedIn activity (no person research available)")
    if not company_research:
        artifact["constraints"]["must_not_claim"].append(
            "No claims about company products/metrics (no company research available)")

    # ── Metadata ──
    artifact["metadata"]["data_sources"] = data_sources
    # Compute research quality: ratio of filled fields
    filled = 0
    total = 0
    for section_key in ("prospect", "company"):
        section = artifact[section_key]
        for v in section.values():
            total += 1
            if v:
                filled += 1
    quality = round(filled / max(total, 1), 2)
    artifact["metadata"]["research_quality_score"] = quality

    # ── Validate ──
    validation = validate_research_artifact(artifact)

    return {"artifact": artifact, "validation": validation}


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
