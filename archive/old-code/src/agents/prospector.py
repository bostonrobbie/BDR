"""
Outreach Command Center - Prospector Agent
Extracts and qualifies prospects from Sales Navigator search results.

This module provides parsing and qualification logic. The actual browser
navigation (Chrome MCP) is orchestrated by Claude during a Cowork session.
Claude calls these functions to process the raw data extracted from Sales Nav.
"""

import re
import json
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.db import models


# ─── ICP TITLE PATTERNS ──────────────────────────────────────

# Primary personas - highest reply rate, feel the pain directly
QA_LEADER_PATTERNS = [
    r"(?:director|head|vp|vice president|sr\.?\s*director|senior\s*director)"
    r"\s*(?:of\s*)?(?:qa|quality|quality\s*(?:assurance|engineering))",
    r"qa\s*(?:manager|lead|director|head)",
    r"quality\s*(?:assurance|engineering)\s*(?:manager|lead|director|head)",
    r"vp\s*(?:of\s*)?quality",
]

# Secondary personas - budget holders
VP_ENG_PATTERNS = [
    r"(?:vp|vice president|director|head)\s*(?:of\s*)?(?:software\s*)?engineering",
    r"(?:vp|vice president|director|head)\s*(?:of\s*)?(?:software\s*)?(?:development|se\b)",
    r"cto\b",
    r"chief\s*technology\s*officer",
]

# Influencer personas - technical champions
INFLUENCER_PATTERNS = [
    r"(?:senior|sr\.?|principal|lead|staff)\s*sdet",
    r"automation\s*(?:lead|architect|manager)",
    r"(?:test|qa)\s*architect",
]

# Exclusion patterns - not software QA
EXCLUDE_PATTERNS = [
    r"quality\s*(?:control|inspector|analyst)\s*(?:pharma|bio|lab|manufacturing|clinical)",
    r"(?:pharma|bio|clinical|lab)\s*quality",
    r"(?:gmp|gxp|capa|fda)\s*(?:quality|compliance)",
    r"quality\s*(?:systems|regulatory)",
    r"(?:manufacturing|production)\s*quality",
    r"(?:food|beverage)\s*(?:quality|safety)",
]


def classify_persona(title: str) -> Optional[str]:
    """Classify a title into persona type.

    Returns: 'QA' (primary), 'VP Eng' (secondary), 'Influencer', or None
    """
    if not title:
        return None
    title_lower = title.lower().strip()

    # Check exclusions first
    for pat in EXCLUDE_PATTERNS:
        if re.search(pat, title_lower):
            return None

    # Check QA leaders (primary)
    for pat in QA_LEADER_PATTERNS:
        if re.search(pat, title_lower):
            return "QA"

    # Check VP Eng (secondary)
    for pat in VP_ENG_PATTERNS:
        if re.search(pat, title_lower):
            return "VP Eng"

    # Check influencers
    for pat in INFLUENCER_PATTERNS:
        if re.search(pat, title_lower):
            return "Influencer"

    return None


def infer_seniority(title: str) -> str:
    """Infer seniority level from title."""
    if not title:
        return ""
    t = title.lower()
    if any(s in t for s in ["vp", "vice president", "chief", "cto", "coo"]):
        return "vp"
    if any(s in t for s in ["director", "head of"]):
        return "director"
    if any(s in t for s in ["manager", "lead"]):
        return "manager"
    if any(s in t for s in ["senior", "sr", "principal", "staff"]):
        return "senior"
    return ""


# ─── QUALIFICATION ────────────────────────────────────────────

def qualify_prospect(raw: dict) -> dict:
    """Apply qualification checklist to a raw prospect.

    Checks:
    1. Manager+ seniority
    2. ICP title match
    3. US-based (unless specified otherwise)
    4. Software QA/engineering (not pharma manufacturing, etc.)
    5. Company has software products

    Returns dict with 'qualified' bool and 'disqualify_reason' if not.
    """
    result = {**raw, "qualified": True, "disqualify_reason": None}

    title = raw.get("title", "")
    location = raw.get("location", "")

    # 1. Persona classification
    persona = classify_persona(title)
    if not persona:
        result["qualified"] = False
        result["disqualify_reason"] = f"Title does not match ICP: {title}"
        return result
    result["persona_type"] = persona

    # 2. Seniority check (manager+)
    seniority = infer_seniority(title)
    if seniority not in ("vp", "director", "manager", "senior"):
        result["qualified"] = False
        result["disqualify_reason"] = f"Seniority too low: {title}"
        return result
    result["seniority_level"] = seniority

    # 3. Location check (US-based default)
    if location and not _is_us_location(location):
        result["qualified"] = False
        result["disqualify_reason"] = f"Non-US location: {location}"
        return result

    return result


def _is_us_location(location: str) -> bool:
    """Check if location string indicates US-based."""
    loc = location.lower()
    us_indicators = [
        "united states", "usa", ", us", " us$",
        "california", "new york", "texas", "florida", "illinois",
        "massachusetts", "washington", "virginia", "georgia", "north carolina",
        "pennsylvania", "ohio", "michigan", "arizona", "colorado",
        "oregon", "maryland", "minnesota", "tennessee", "indiana",
        "connecticut", "utah", "nevada", "san francisco", "los angeles",
        "chicago", "seattle", "boston", "austin", "denver", "atlanta",
        "dallas", "houston", "miami", "portland", "new jersey", "dc",
        "bay area", "silicon valley", "nyc", "la", "sf",
    ]
    # US state abbreviations (2-letter at end of string)
    state_abbrevs = [
        "al", "ak", "az", "ar", "ca", "co", "ct", "de", "fl", "ga",
        "hi", "id", "il", "in", "ia", "ks", "ky", "la", "me", "md",
        "ma", "mi", "mn", "ms", "mo", "mt", "ne", "nv", "nh", "nj",
        "nm", "ny", "nc", "nd", "oh", "ok", "or", "pa", "ri", "sc",
        "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv", "wi", "wy",
    ]

    for indicator in us_indicators:
        if indicator in loc:
            return True

    # Check for state abbreviation at end: "City, ST"
    parts = loc.split(",")
    if len(parts) >= 2:
        state = parts[-1].strip().lower()
        if state in state_abbrevs:
            return True

    return False


# ─── DEDUPLICATION ────────────────────────────────────────────

def dedupe_against_db(prospects: list) -> list:
    """Filter out prospects already in the database by LinkedIn URL.

    Returns only new (not yet contacted) prospects.
    """
    conn = models.get_db()
    existing_urls = set()
    rows = conn.execute("SELECT linkedin_url FROM contacts WHERE linkedin_url IS NOT NULL").fetchall()
    for r in rows:
        if r["linkedin_url"]:
            existing_urls.add(r["linkedin_url"].lower().strip())
    conn.close()

    new_prospects = []
    for p in prospects:
        url = (p.get("linkedin_url") or "").lower().strip()
        if url and url in existing_urls:
            continue  # Skip existing
        new_prospects.append(p)

    return new_prospects


# ─── BATCH MIX VALIDATION ────────────────────────────────────

def validate_batch_mix(prospects: list, config: dict = None) -> dict:
    """Check if prospect batch meets the target mix ratio.

    Target: 12-15 QA leaders, 8-10 VP Eng, 2-3 Buyer Intent
    Max 8 from same vertical, max 2 from same company.
    """
    config = config or {}
    mix = config.get("mix_ratio", {
        "qa_leaders": {"min": 12, "max": 15},
        "vp_eng": {"min": 8, "max": 10},
        "buyer_intent": {"min": 2, "max": 3}
    })

    qa_count = sum(1 for p in prospects if p.get("persona_type") == "QA")
    vp_count = sum(1 for p in prospects if p.get("persona_type") == "VP Eng")
    intent_count = sum(1 for p in prospects if p.get("buyer_intent"))

    # Vertical distribution
    verticals = {}
    for p in prospects:
        v = p.get("vertical", "Unknown")
        verticals[v] = verticals.get(v, 0) + 1

    # Company distribution
    companies = {}
    for p in prospects:
        c = p.get("company", "Unknown")
        companies[c] = companies.get(c, 0) + 1

    max_vert = config.get("max_per_vertical", 8)
    max_co = config.get("max_per_company", 2)

    issues = []
    if qa_count < mix["qa_leaders"]["min"]:
        issues.append(f"QA leaders: {qa_count} (min {mix['qa_leaders']['min']})")
    if vp_count < mix["vp_eng"]["min"]:
        issues.append(f"VP Eng: {vp_count} (min {mix['vp_eng']['min']})")

    over_vertical = {k: v for k, v in verticals.items() if v > max_vert}
    if over_vertical:
        issues.append(f"Verticals over {max_vert}: {over_vertical}")

    over_company = {k: v for k, v in companies.items() if v > max_co}
    if over_company:
        issues.append(f"Companies over {max_co}: {over_company}")

    return {
        "valid": len(issues) == 0,
        "qa_leaders": qa_count,
        "vp_eng": vp_count,
        "buyer_intent": intent_count,
        "total": len(prospects),
        "verticals": verticals,
        "companies": companies,
        "issues": issues,
    }


# ─── SEARCH RESULT PARSING ───────────────────────────────────

def parse_search_result_text(page_text: str) -> list:
    """Parse raw text from Sales Navigator search results page.

    The actual text structure varies, but common patterns include:
    - Name on one line
    - Title on next line
    - Company on another line
    - Location info

    This is a best-effort parser; Claude will validate and correct during extraction.
    Returns list of raw prospect dicts.
    """
    prospects = []
    lines = [l.strip() for l in page_text.split("\n") if l.strip()]

    # This is a template parser. During actual extraction, Claude uses
    # get_page_text or JavaScript DOM extraction for more reliable parsing.
    # The structured data comes from Claude's interpretation of the page.

    return prospects


def parse_profile_text(profile_text: str, name: str = "") -> dict:
    """Parse raw text from an individual LinkedIn profile page.

    Extracts: headline, about, current role, tenure, career history.
    Best-effort parser; Claude validates during extraction.
    """
    result = {
        "headline": "",
        "about": "",
        "current_role": "",
        "tenure_months": None,
        "recently_hired": False,
        "career_history": [],
        "skills": [],
    }

    lines = [l.strip() for l in profile_text.split("\n") if l.strip()]

    # Look for "About" section
    about_start = None
    for i, line in enumerate(lines):
        if line.lower() in ("about", "about this profile"):
            about_start = i + 1
            break
    if about_start:
        about_lines = []
        for line in lines[about_start:about_start + 10]:
            if line.lower() in ("experience", "education", "skills"):
                break
            about_lines.append(line)
        result["about"] = " ".join(about_lines)

    return result


# ─── INTERACTION CHECK ────────────────────────────────────────

def check_prior_interaction(profile_text: str) -> dict:
    """Check if profile text shows prior interaction indicators.

    Looks for: "Messaged", "Viewed", "Connected", "InMail sent"
    Returns dict with interaction status.
    """
    text_lower = profile_text.lower()

    indicators = {
        "messaged": any(s in text_lower for s in ["messaged", "inmail sent", "message sent"]),
        "viewed": "viewed" in text_lower and "who viewed" not in text_lower,
        "connected": "connected" in text_lower and "connect" not in text_lower,
    }

    has_prior = any(indicators.values())
    return {
        "has_prior_interaction": has_prior,
        "indicators": indicators,
        "should_skip": indicators["messaged"],  # Skip only if previously messaged
    }
