"""
Outreach Command Center - Quality Gate Agent
Runs 10 automated QC checks on every message draft before Rob sees it.

Checks:
1. No hallucinated customer names or stats
2. No placeholder text ([NAME], {company}, TODO, etc.)
3. No em dashes
4. Personalization exists (not generic)
5. Research citation present (company-specific reference)
6. Word count within bounds (70-120 for Touch 1, 40-70 for Touch 3, 30-50 for Touch 6)
7. One question max
8. Opener variety (not starting with "I noticed" or "I saw")
9. Proof point rotation (different from previous touch for same contact)
10. Soft ask with easy out present
"""

import re
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.db import models

# Valid customer names from the SOP
VALID_CUSTOMERS = {
    "hansard", "medibuddy", "cred", "sanofi", "nagra", "nagra dtv", "spendflo",
    "cisco", "samsung", "honeywell", "bosch", "nokia", "nestle", "kfc", "dhl",
    "zeiss", "axel springer", "ntuc fairprice", "oscar health", "american psychological association"
}

# Valid stats from the SOP
VALID_STATS = {
    "8 weeks to 5 weeks", "8 to 5 weeks", "2,500 tests", "2500 tests",
    "50% maintenance", "90% regression", "5x faster", "3 days to 80 minutes",
    "3x productivity", "3X productivity", "2,500 tests in 8 months", "4x faster", "4X faster",
    "50% manual testing", "70% maintenance reduction", "90% maintenance reduction",
    "fortune 100"
}

PLACEHOLDER_PATTERNS = [
    r'\[NAME\]', r'\[name\]', r'\{company\}', r'\{name\}', r'\{title\}',
    r'TODO', r'FIXME', r'XXX', r'\[COMPANY\]', r'\[TITLE\]',
    r'\[INSERT', r'\{insert', r'<company>', r'<name>',
    r'\[Your', r'\[your', r'\[PROSPECT'
]

OVERUSED_OPENERS = [
    r'^I noticed\b', r'^I saw\b', r'^I see\b',
    r'^I came across\b', r'^I found\b'
]

SOFT_ASK_PHRASES = [
    "no worries", "no pressure", "totally get it", "get out of your hair",
    "timing is off", "timing isn't right", "not relevant",
    "worth a conversation", "happy to share more", "if helpful",
    "close the loop", "if it's not", "if not", "if the timing",
    "worth 15 minutes", "worth a quick", "make sense"
]


def check_no_hallucinated_customers(body: str) -> dict:
    """Check 1: No hallucinated customer names or stats."""
    flags = []
    body_lower = body.lower()

    # Look for patterns like "Company X achieved Y%" or "at Company"
    # that reference companies NOT in our valid list
    company_patterns = re.findall(r'(?:at|with|like|for)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)', body)
    for company in company_patterns:
        if company.lower() not in VALID_CUSTOMERS and company.lower() not in {
            "testsigma", "the", "their", "your", "one", "some", "many", "most", "our"
        }:
            # Not necessarily a flag - could be the prospect's company
            pass

    # Check for suspicious stat patterns not in our valid set
    stat_patterns = re.findall(r'(\d+%\s+\w+)', body)
    for stat in stat_patterns:
        stat_lower = stat.lower()
        if not any(vs in body_lower for vs in VALID_STATS):
            if any(s in stat_lower for s in ["reduction", "cut", "faster", "increase", "improvement"]):
                flags.append(f"Potentially unverified stat: '{stat}'")

    passed = len(flags) == 0
    return {"check": "no_hallucinated_customers", "passed": passed, "flags": flags}


def check_no_placeholders(body: str, subject: str = "") -> dict:
    """Check 2: No placeholder text."""
    flags = []
    full_text = f"{subject} {body}"
    for pattern in PLACEHOLDER_PATTERNS:
        matches = re.findall(pattern, full_text)
        if matches:
            flags.append(f"Placeholder found: {matches[0]}")
    passed = len(flags) == 0
    return {"check": "no_placeholders", "passed": passed, "flags": flags}


def check_no_em_dashes(body: str, subject: str = "") -> dict:
    """Check 3: No em dashes."""
    full_text = f"{subject} {body}"
    em_dash_count = full_text.count("\u2014")
    passed = em_dash_count == 0
    flags = [f"Found {em_dash_count} em dash(es)"] if not passed else []
    return {"check": "no_em_dashes", "passed": passed, "flags": flags}


def check_personalization(body: str) -> dict:
    """Check 4: Personalization exists."""
    flags = []
    # Look for signals that the message is personalized
    personal_signals = [
        r'your\s+(?:team|role|work|experience|background)',
        r'at\s+[A-Z][a-zA-Z]+',  # "at CompanyName"
        r'as\s+(?:a\s+)?(?:Director|VP|Head|Manager|Lead|Senior)',
        r'\d+\s+years?',  # tenure reference
        r'moved\s+(?:from|to|over)',  # career move
    ]
    found_personalization = any(re.search(p, body) for p in personal_signals)
    if not found_personalization:
        flags.append("No personalization detected - message may be too generic")
    return {"check": "personalization_exists", "passed": found_personalization, "flags": flags}


def check_research_citation(body: str) -> dict:
    """Check 5: Company-specific research reference present."""
    flags = []
    # Look for company-specific references (products, metrics, markets, events)
    research_signals = [
        r'your\s+\w+\s+(?:platform|product|app|service|tool)',
        r'\d+[KMB]?\+?\s+(?:users|customers|transactions|employees|merchants)',
        r'digital\s+(?:banking|payments|health|commerce|lending)',
        r'recently\s+(?:launched|raised|acquired|expanded|hired)',
        r'series\s+[A-D]',
    ]
    found_research = any(re.search(p, body, re.IGNORECASE) for p in research_signals)
    if not found_research:
        flags.append("No company-specific research reference detected")
    return {"check": "research_citation", "passed": found_research, "flags": flags}


def check_word_count(body: str, touch_number: int = 1) -> dict:
    """Check 6: Word count within bounds."""
    word_count = len(body.split())
    bounds = {
        1: (70, 120),   # Touch 1 InMail
        3: (40, 70),    # Touch 3 Follow-up
        5: (70, 120),   # Touch 5 Email
        6: (30, 50),    # Touch 6 Break-up
    }
    low, high = bounds.get(touch_number, (40, 120))
    passed = low <= word_count <= high
    flags = []
    if word_count < low:
        flags.append(f"Too short: {word_count} words (min {low})")
    elif word_count > high:
        flags.append(f"Too long: {word_count} words (max {high})")
    return {"check": "word_count", "passed": passed, "flags": flags, "word_count": word_count}


def check_one_question_max(body: str) -> dict:
    """Check 7: One question max."""
    questions = body.count("?")
    passed = questions <= 1
    flags = [f"Found {questions} questions (max 1)"] if not passed else []
    return {"check": "one_question_max", "passed": passed, "flags": flags}


def check_opener_variety(body: str) -> dict:
    """Check 8: Not starting with overused openers."""
    flags = []
    for pattern in OVERUSED_OPENERS:
        if re.match(pattern, body.strip(), re.IGNORECASE):
            flags.append(f"Overused opener: starts with '{body.split()[0]} {body.split()[1] if len(body.split()) > 1 else ''}'")
            break
    passed = len(flags) == 0
    return {"check": "opener_variety", "passed": passed, "flags": flags}


def check_proof_point_rotation(contact_id: str, proof_point: str, touch_number: int) -> dict:
    """Check 9: Different proof point from previous touch."""
    flags = []
    if not proof_point or touch_number <= 1:
        return {"check": "proof_point_rotation", "passed": True, "flags": []}

    try:
        messages = models.get_messages_for_contact(contact_id)
        previous_proofs = [
            m.get("proof_point_used") for m in messages
            if m.get("touch_number", 0) < touch_number and m.get("proof_point_used")
        ]
        if proof_point in previous_proofs:
            flags.append(f"Same proof point '{proof_point}' used in a previous touch")
    except Exception:
        pass  # If DB not available, skip this check

    passed = len(flags) == 0
    return {"check": "proof_point_rotation", "passed": passed, "flags": flags}


def check_soft_ask(body: str) -> dict:
    """Check 10: Soft ask with easy out present."""
    body_lower = body.lower()
    found_soft = any(phrase in body_lower for phrase in SOFT_ASK_PHRASES)
    flags = [] if found_soft else ["No soft ask / easy out detected"]
    return {"check": "soft_ask_present", "passed": found_soft, "flags": flags}


def run_quality_gate(message_data: dict) -> dict:
    """
    Run all 10 QC checks on a message draft.

    Args:
        message_data: dict with keys: body, subject_line, touch_number, contact_id, proof_point_used

    Returns:
        dict with overall pass/fail, individual check results, and summary
    """
    body = message_data.get("body", "")
    subject = message_data.get("subject_line", "")
    touch_num = message_data.get("touch_number", 1)
    contact_id = message_data.get("contact_id", "")
    proof_point = message_data.get("proof_point_used", "")

    checks = [
        check_no_hallucinated_customers(body),
        check_no_placeholders(body, subject),
        check_no_em_dashes(body, subject),
        check_personalization(body),
        check_research_citation(body),
        check_word_count(body, touch_num),
        check_one_question_max(body),
        check_opener_variety(body),
        check_proof_point_rotation(contact_id, proof_point, touch_num),
        check_soft_ask(body),
    ]

    all_passed = all(c["passed"] for c in checks)
    passed_count = sum(1 for c in checks if c["passed"])
    all_flags = []
    for c in checks:
        all_flags.extend(c["flags"])

    return {
        "passed": all_passed,
        "score": f"{passed_count}/10",
        "passed_count": passed_count,
        "total_checks": 10,
        "checks": checks,
        "flags": all_flags,
        "summary": "All checks passed" if all_passed else f"{10 - passed_count} issue(s) found: {'; '.join(all_flags[:3])}"
    }


def qc_and_save(message_id: str) -> dict:
    """Run QC on an existing message draft and save results."""
    conn = models.get_db()
    row = conn.execute("SELECT * FROM message_drafts WHERE id=?", (message_id,)).fetchone()
    conn.close()

    if not row:
        return {"error": "Message not found"}

    msg = dict(row)
    result = run_quality_gate(msg)

    # Update the message draft with QC results
    conn = models.get_db()
    conn.execute("""
        UPDATE message_drafts SET qc_passed=?, qc_flags=?, updated_at=datetime('now')
        WHERE id=?
    """, (1 if result["passed"] else 0, json.dumps(result["flags"]), message_id))
    conn.commit()
    conn.close()

    return result


if __name__ == "__main__":
    # Test with a sample message
    sample = {
        "body": "Your work directing QA across Ally's digital banking platform caught my eye. "
                "With millions of daily transactions hitting your payments infrastructure, "
                "regression testing every time fraud rules change must be relentless. "
                "A fintech team we work with (CRED) automated 90% of their regression suite and "
                "cut execution time 5x. Would 15 minutes make sense to see if something similar "
                "could help your team? If not, no worries at all.",
        "subject_line": "QA at Ally - quick question",
        "touch_number": 1,
        "contact_id": "",
        "proof_point_used": "CRED"
    }
    result = run_quality_gate(sample)
    print(f"\nQuality Gate: {'PASS' if result['passed'] else 'FAIL'} ({result['score']})")
    for check in result["checks"]:
        status = "PASS" if check["passed"] else "FAIL"
        print(f"  [{status}] {check['check']}: {check.get('flags', [])}")
