#!/usr/bin/env python3
"""
Outbound Intelligence & QA Engine
==================================
Testsigma BDR - Rob Gorham
Built on: LinkedIn Outreach Analysis (Feb 2026)
Source: 1,326 conversations, 381 reply threads, 4,786 messages

This engine provides:
1. Message Quality Scoring (MQS) - 12-point system (4 dimensions x 3 pts)
2. Hard Constraint violation detection (10 constraints, HC1-HC10)
3. QA Gate enforcement (10-check mandatory gate)
4. Prospect prioritization (reply-likelihood model, persona-weighted)
5. Batch validation and reporting
6. Phrase toxicity scanning

ALL rules are derived from observed data. When data conflicts with intuition, the data wins.
"""

import re
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from datetime import datetime


# ============================================================
# SECTION 1: CANONICAL RULES (from analysis_output.json)
# ============================================================

# Hard Constraints - violation = automatic rejection
HARD_CONSTRAINTS = {
    "HC1_i_noticed": {
        "name": "No 'I noticed' / 'I saw' / 'I see' phrasing",
        "pattern": r"(?i)(i noticed|i saw that|i saw you|i see that|i see you|based on your profile|i came across)",
        "data_basis": "-13.4 pp diff (10.9% reply vs 24.3% no-reply). Strongest negative signal.",
        "severity": "CRITICAL"
    },
    "HC2_feature_headline": {
        "name": "No leading with AI/ML/self-healing as headline feature",
        "pattern": r"(?i)(our (ai|platform|tool) (auto[- ]?heals?|creates?|maintains?|executes?)|auto[- ]?heal(s|ing)|self[- ]?healing (function|feature|capability)|low[- ]?code automation platform|nlp[- ]?based|natural language (processing|programming) (test|platform))",
        "data_basis": "AI mention: -9.2 pp (11.1% vs 20.3%). Self-healing: -6.2 pp (10.3% vs 16.5%).",
        "severity": "CRITICAL"
    },
    "HC3_too_long": {
        "name": "No messages over 120 words",
        "check": "word_count",
        "threshold": 120,
        "data_basis": "75-99 words = 39.0% reply rate. 125-149 = 23.4%. 150+ = 21.2%.",
        "severity": "HIGH"
    },
    "HC4_evening_send": {
        "name": "No evening sends (after 6 PM)",
        "check": "send_time",
        "data_basis": "Evening (6-8 PM): 12.1% reply rate vs 56.5% for lunch window. -44.4 pp.",
        "severity": "HIGH"
    },
    "HC5_bullet_list": {
        "name": "No bullet-point or numbered-list feature dumps",
        "pattern": r"(\n\s*[-•*]\s+.+\n\s*[-•*]\s+)|(\n\s*\d+\.\s+.+\n\s*\d+\.\s+)",
        "data_basis": "Bullets: -2.2 pp diff (1.0% reply vs 3.2% no-reply). Zero high-performers use bullets.",
        "severity": "HIGH"
    },
    "HC6_unreasonable_cta": {
        "name": "No 'would it be unreasonable' as sole CTA",
        "pattern": r"(?i)would it be unreasonable",
        "data_basis": "As CTA: 12.8% reply rate (n=39), less than half the baseline.",
        "severity": "HIGH"
    },
    "HC7_phone_ask": {
        "name": "No phone-number asks",
        "pattern": r"(?i)(what\'?s your (number|phone|cell|#)|i can drop my (#|number|phone)|give you a (call|ring)|what number.{0,15}reach you|can i call)",
        "data_basis": "Phone ask CTA: 5.0% reply rate (n=40). Worst-performing CTA by far.",
        "severity": "HIGH"
    },
    "HC8_reaching_out": {
        "name": "No 'reaching out' / 'wanted to connect' phrasing",
        "pattern": r"(?i)(i\'?m reaching out|reaching out to|wanted to connect|reaching out because)",
        "data_basis": "-2.4 pp diff on first messages. Correlates with template-visible openers.",
        "severity": "MEDIUM"
    },
    "HC9_toxic_phrases": {
        "name": "No toxic phrases ('I figure', 'would you like to share', 'enough about me')",
        "pattern": r"(?i)(i figure |would you like to share|enough about me)",
        "data_basis": "'I figure': 9.8% (-19.0 pp). 'Would you like to share': 15.2% (-13.6 pp). 'Enough about me': 18.2% (-10.6 pp).",
        "severity": "MEDIUM"
    },
    "HC10_too_many_questions": {
        "name": "No 3+ question marks per message",
        "check": "question_count",
        "threshold": 3,
        "data_basis": "3 questions: 14.3% reply rate (n=7). Optimal is exactly 2 questions (34.8%).",
        "severity": "MEDIUM"
    }
}

# Toxic phrases - scanned separately for granular reporting
TOXIC_PHRASES = {
    "i figure": {"reply_rate": 9.8, "vs_baseline": -19.0, "n": 41},
    "would you like to share": {"reply_rate": 15.2, "vs_baseline": -13.6, "n": 33},
    "flaky tests": {"reply_rate": 16.8, "vs_baseline": -11.9, "n": 95},
    "enough about me": {"reply_rate": 18.2, "vs_baseline": -10.6, "n": 55},
    "ci/cd": {"reply_rate": 23.6, "vs_baseline": -5.1, "n": 110},
    "low code": {"reply_rate": 25.8, "vs_baseline": -2.9, "n": 93},
}

# High-performing phrases - use these
HIGH_PERFORMING_PHRASES = {
    "have you heard of": {"reply_rate": 81.8, "vs_baseline": 53.1, "n": 22},
    "increase testing efficiency": {"reply_rate": 41.4, "vs_baseline": 12.7, "n": 765},
    "thought it would be worth": {"reply_rate": 41.3, "vs_baseline": 12.6, "n": 767},
    "exploring your options": {"reply_rate": 39.7, "vs_baseline": 10.9, "n": 809},
    "test maintenance": {"reply_rate": 37.8, "vs_baseline": 9.0, "n": 916},
    "release cycles": {"reply_rate": 36.1, "vs_baseline": 7.4, "n": 981},
    "was hoping to hear": {"reply_rate": 32.9, "vs_baseline": 4.1, "n": 73},
}

# Proof points - verified, with vertical match
PROOF_POINTS = {
    "hansard": {
        "text": "Hansard cut regression from 8 weeks to 5 weeks with AI auto-heal",
        "short": "Hansard: regression 8wk to 5wk",
        "verticals": ["insurance", "financial_services", "fintech"],
        "angle": "maintenance",
        "numbers": "8 weeks to 5 weeks"
    },
    "medibuddy": {
        "text": "Medibuddy automated 2,500 tests and cut maintenance effort in half",
        "short": "Medibuddy: 2,500 tests, 50% maintenance cut",
        "verticals": ["healthcare", "digital_health", "mid_size"],
        "angle": "scale",
        "numbers": "2,500 tests, 50% cut"
    },
    "cred": {
        "text": "CRED hit 90% regression automation and 5x faster execution",
        "short": "CRED: 90% coverage, 5x faster",
        "verticals": ["fintech", "tech", "saas"],
        "angle": "velocity",
        "numbers": "90% automation, 5x faster"
    },
    "sanofi": {
        "text": "Sanofi compressed regression from 3 days to 80 minutes",
        "short": "Sanofi: 3 days to 80 minutes",
        "verticals": ["pharma", "healthcare", "compliance"],
        "angle": "velocity",
        "numbers": "3 days to 80 minutes"
    },
    "fortune100": {
        "text": "A Fortune 100 company saw 3X productivity increase",
        "short": "Fortune 100: 3X productivity",
        "verticals": ["enterprise", "tech", "any"],
        "angle": "productivity",
        "numbers": "3X productivity"
    },
    "nagra": {
        "text": "Nagra DTV automated 2,500 tests in 8 months, 4X faster execution",
        "short": "Nagra DTV: 2,500 tests in 8mo, 4X faster",
        "verticals": ["media", "streaming", "telecom"],
        "angle": "scale",
        "numbers": "2,500 tests, 4X faster"
    },
    "spendflo": {
        "text": "Spendflo cut manual testing 50%",
        "short": "Spendflo: 50% manual testing cut",
        "verticals": ["saas", "startup", "small_team"],
        "angle": "productivity",
        "numbers": "50% cut"
    },
    "selenium_comparison": {
        "text": "70% maintenance reduction vs Selenium",
        "short": "70% less maintenance vs Selenium",
        "verticals": ["any"],
        "angle": "maintenance",
        "numbers": "70% reduction"
    },
    "self_healing_stat": {
        "text": "90% maintenance reduction with self-healing",
        "short": "90% maintenance reduction",
        "verticals": ["any"],
        "angle": "maintenance",
        "numbers": "90% reduction"
    }
}

ANGLES = ["maintenance", "velocity", "scale", "productivity"]


# ============================================================
# SECTION 2: DATA CLASSES
# ============================================================

@dataclass
class HardConstraintViolation:
    constraint_id: str
    constraint_name: str
    severity: str
    matched_text: str
    data_basis: str

@dataclass
class MQSBreakdown:
    opener_clarity: int  # 1-3
    cta_confidence: int  # 1-3
    personalization_density: int  # 1-3
    friction: int  # 1-3 (inverted: 3=low friction)
    total: int  # sum, max 12
    opener_rationale: str = ""
    cta_rationale: str = ""
    personalization_rationale: str = ""
    friction_rationale: str = ""

@dataclass
class QAResult:
    passed: bool
    mqs: MQSBreakdown
    violations: List[HardConstraintViolation]
    warnings: List[str]
    recommendation: str  # "SEND", "REWRITE", "REJECT"

@dataclass
class ProspectRecord:
    full_name: str
    title: str
    company: str
    linkedin_url: str = ""
    source: str = ""
    vertical: str = ""
    employee_count: int = 0
    persona_type: str = ""
    seniority: str = ""
    priority_score: int = 0
    personalization_score: int = 0
    signals: List[str] = field(default_factory=list)
    company_desc: str = ""
    person_detail: str = ""
    predicted_objection: str = ""
    objection_response: str = ""
    reply_likelihood: float = 0.0
    research_quality: str = ""  # "deep", "medium", "light"


# ============================================================
# SECTION 3: HARD CONSTRAINT SCANNER
# ============================================================

def scan_hard_constraints(message: str, send_hour: Optional[int] = None) -> List[HardConstraintViolation]:
    """Scan a message for ALL hard constraint violations.

    Args:
        message: The message text to scan.
        send_hour: Optional hour (0-23) when the message will be sent.
                   Used for HC4 evening send check. None = skip time check.
    """
    violations = []

    for cid, rule in HARD_CONSTRAINTS.items():
        if "pattern" in rule:
            match = re.search(rule["pattern"], message)
            if match:
                violations.append(HardConstraintViolation(
                    constraint_id=cid,
                    constraint_name=rule["name"],
                    severity=rule["severity"],
                    matched_text=match.group(0)[:80],
                    data_basis=rule["data_basis"]
                ))
        elif rule.get("check") == "word_count":
            wc = len(message.split())
            if wc > rule["threshold"]:
                violations.append(HardConstraintViolation(
                    constraint_id=cid,
                    constraint_name=f"{rule['name']} (got {wc} words)",
                    severity=rule["severity"],
                    matched_text=f"Word count: {wc} > {rule['threshold']}",
                    data_basis=rule["data_basis"]
                ))
        elif rule.get("check") == "question_count":
            qc = message.count('?')
            if qc >= rule["threshold"]:
                violations.append(HardConstraintViolation(
                    constraint_id=cid,
                    constraint_name=f"{rule['name']} (got {qc} questions)",
                    severity=rule["severity"],
                    matched_text=f"Question marks: {qc} >= {rule['threshold']}",
                    data_basis=rule["data_basis"]
                ))
        elif rule.get("check") == "send_time":
            if send_hour is not None and send_hour >= 18:
                violations.append(HardConstraintViolation(
                    constraint_id=cid,
                    constraint_name=f"{rule['name']} (scheduled for {send_hour}:00)",
                    severity=rule["severity"],
                    matched_text=f"Send hour: {send_hour} >= 18",
                    data_basis=rule["data_basis"]
                ))

    return violations


def scan_toxic_phrases(message: str) -> List[Dict]:
    """Scan message for toxic phrases and return matches with data."""
    ml = message.lower()
    found = []
    for phrase, data in TOXIC_PHRASES.items():
        if phrase in ml:
            found.append({
                "phrase": phrase,
                "reply_rate": data["reply_rate"],
                "vs_baseline": data["vs_baseline"],
                "n": data["n"]
            })
    return found


def scan_high_performing_phrases(message: str) -> List[Dict]:
    """Scan message for high-performing phrases and return matches."""
    ml = message.lower()
    found = []
    for phrase, data in HIGH_PERFORMING_PHRASES.items():
        if phrase in ml:
            found.append({
                "phrase": phrase,
                "reply_rate": data["reply_rate"],
                "vs_baseline": data["vs_baseline"],
                "n": data["n"]
            })
    return found


# ============================================================
# SECTION 4: MESSAGE QUALITY SCORER (MQS)
# ============================================================

def score_opener_clarity(message: str) -> Tuple[int, str]:
    """Score opener clarity 1-3 based on observed patterns."""
    first_line = message.split('\n')[0].strip() if message.strip() else ""
    ml = message.lower()
    fl = first_line.lower()

    # Check for "I noticed" / "I saw" patterns (instant score 1)
    if re.search(r"(i noticed|i saw|i see that|i came across)", fl):
        return 1, "Opens with 'I noticed/saw' phrasing (HC1: -13.4 pp, strongest negative signal)"

    # Check for reaching_out patterns (instant score 1)
    if re.search(r"(reaching out|wanted to connect)", fl):
        return 1, "Opens with 'reaching out' / 'wanted to connect' (HC8: -2.4 pp)"

    # Check for role-at-company opener (instant score 1)
    if re.search(r"(seeing that you|i see that you|i see in your bio|as the .{5,40} at )", fl):
        return 1, "Opens with role-at-company recap (-3.1 pp role_reference diff)"

    # Check for question opener (good signal)
    if '?' in first_line and len(first_line) > 20:
        # Check if the question is specific (not generic)
        if re.search(r"(your|you|team|company|stack|suite|coverage|regression|release)", fl):
            return 3, "Opens with specific, insight-driven question (question_opener: promising signal)"
        return 2, "Opens with a question but could be more specific to the prospect"

    # Check for company/situation-specific opener (no question but shows research)
    if re.search(r"(acquisition|migration|integration|launch|hiring|scaling|growth|raised|funding)", fl):
        return 3, "Opens with specific company event/situation reference (high personalization)"

    # Check for name + specific reference
    if re.search(r"^[A-Z][a-z]+,?\s+(with|after|during|since|given)", fl):
        return 2, "Opens with name + situation reference (moderate specificity)"

    # Generic opener
    if re.search(r"^(hi|hey|hello)\s+[a-z]", fl):
        if len(first_line) < 30:
            return 1, "Generic greeting opener with no specificity"
        return 2, "Name + some context but not insight-driven"

    return 2, "Moderate opener - has some personalization but could be sharper"


def score_cta_confidence(message: str) -> Tuple[int, str]:
    """Score CTA confidence 1-3 based on observed patterns."""
    # Look at last 300 chars
    tail = message[-300:].lower() if len(message) > 300 else message.lower()

    # Phone ask (worst CTA, instant score 1)
    if re.search(r"(what\'?s your (number|phone|cell|#)|drop my (#|number)|give you a (call|ring))", tail):
        return 1, "Phone-number ask CTA (HC7: 5.0% reply rate, worst CTA by far)"

    # "Would it be unreasonable" (instant score 1)
    if re.search(r"would it be unreasonable", tail):
        return 1, "'Would it be unreasonable' CTA (HC6: 12.8% reply rate, less than half baseline)"

    # Permission-based CTAs (instant score 1)
    if re.search(r"(happy to share|feel free|no worries|if not.{0,10}all good|no pressure)", tail):
        return 1, "Permission-based / easy-out CTA (below baseline)"

    # Open-ended question CTAs (score 1)
    if re.search(r"(what are your initiatives|what are you focusing|what\'?s your (priority|focus))", tail):
        return 1, "Open-ended question CTA (14.0% reply rate for question_close style)"

    # "What day works?" pattern (BEST at scale, score 3)
    if re.search(r"(what day|what (time|morning|afternoon) works|which day|when works)", tail) and '?' in tail[-80:]:
        return 3, "'What day works?' CTA (40.4% reply rate, n=782, best at scale)"

    # Direct meeting ask with time/action (score 3)
    if re.search(r"(would \d+ minutes|15 minutes|quick (call|chat|look)|worth (a |15 |a quick )(conversation|chat|call|look|minute))", tail):
        if '?' in tail[-80:]:
            return 3, "Direct meeting ask with time/action and question mark (+18.6 pp meeting_ask advantage)"
        return 2, "Has meeting ask but missing question mark at close"

    # Awareness check ("heard of us?") - best rate but niche
    if re.search(r"(have you heard of|heard of us|familiar with)", tail) and '?' in tail[-80:]:
        return 3, "Awareness check CTA (52.4% reply rate, n=42, niche but powerful)"

    # Confident ask without specific time (score 2)
    if re.search(r"(worth (exploring|comparing|a conversation)|make sense|sound (useful|relevant|interesting))", tail) and '?' in tail[-80:]:
        return 2, "Confident ask with question but no specific time reference"

    # Question at the end (baseline)
    if '?' in tail[-60:]:
        return 2, "Ends with a question but CTA could be more specific"

    return 1, "No clear CTA or question at close"


def score_personalization(message: str, prospect: Optional[ProspectRecord] = None) -> Tuple[int, str]:
    """Score personalization density 1-3."""
    ml = message.lower()

    # Check for specific company events/situations
    specific_signals = [
        r"(acquisition|acquiring|acquired|merger|merged)",
        r"(raised|funding|series [a-d]|ipo|went public)",
        r"(launched|launch of|shipped|release of|new product)",
        r"(hiring|job posting|growing|expanding|scaling)",
        r"(migration|migrating|transitioning|consolidat)",
        r"(integration|integrating|post-acquisition)",
    ]
    event_refs = sum(1 for pat in specific_signals if re.search(pat, ml))

    # Check for specific technology/tool references
    tech_refs = len(re.findall(r"(selenium|cypress|playwright|katalon|tosca|testim|mabl|appium|jenkins|jira|salesforce)", ml))

    # Check for person-specific references (career, specific project)
    person_refs = 0
    if prospect and prospect.person_detail:
        # Check if message references something from their person_detail
        detail_words = set(prospect.person_detail.lower().split())
        msg_words = set(ml.split())
        overlap = detail_words & msg_words - {'the', 'a', 'an', 'and', 'or', 'at', 'in', 'of', 'to', 'for', 'is', 'are', 'was', 'were'}
        if len(overlap) > 3:
            person_refs = 2

    total_depth = event_refs + tech_refs + person_refs

    if total_depth >= 3 or (event_refs >= 1 and person_refs >= 1):
        return 3, f"Deep personalization: {event_refs} event refs, {tech_refs} tech refs, person-specific details"
    elif total_depth >= 1 or event_refs >= 1:
        return 2, f"Medium personalization: company-specific but not person-specific"
    else:
        # Check if it at least mentions the company by name
        if prospect and prospect.company.lower() in ml:
            return 2, "References company by name but no deeper specifics"
        return 1, "Surface-level personalization (name/title swap only). -12.7 pp risk."


def score_friction(message: str) -> Tuple[int, str]:
    """Score friction 1-3 (inverted: 3=low friction, 1=high friction).

    Data-backed scoring:
    - 75-99 words = 39.0% reply rate (optimal, score 3)
    - 100-124 words = 27.5% (at baseline, score 2)
    - 125+ words = 23.4% or worse (score 1)
    - Exactly 2 question marks = 34.8% (optimal)
    - No bullet lists (score 1 if present)
    """
    word_count = len(message.split())
    question_count = message.count('?')

    # Check for bullet lists
    has_bullets = bool(re.search(r"(\n\s*[-•*]\s+.+\n\s*[-•*]\s+)|(\n\s*\d+\.\s+.+\n\s*\d+\.\s+)", message))

    # Count proof points / stat mentions
    stat_count = len(re.findall(r"\d+[%xX]|\d+ (weeks?|days?|minutes?|hours?|months?|times?)", message))

    # Count CTAs / asks
    cta_count = len(re.findall(r"(?i)(would|could|can|should|want|like|happy|available|interested)\s.{5,40}\?", message))

    # Score 3: 75-99 words, exactly 2 questions, no bullets, clean structure
    if (75 <= word_count <= 99 and not has_bullets and stat_count <= 2
            and cta_count <= 1 and question_count == 2):
        return 3, f"Optimal friction: {word_count} words (sweet spot 75-99 = 39.0%), {question_count} questions (optimal = 34.8%)"

    # Score 3 if word count in sweet spot even with imperfect question count
    if 75 <= word_count <= 99 and not has_bullets and stat_count <= 2 and cta_count <= 1:
        return 3, f"Low friction: {word_count} words (sweet spot), {question_count} question(s)"

    # Score 2: 100-120 words or <75 words, still readable
    if word_count <= 120 and not has_bullets:
        detail = f"{word_count} words"
        if word_count < 75:
            detail += " (under sweet spot)"
        elif word_count >= 100:
            detail += " (above sweet spot, 27.5% at 100-124)"
        return 2, f"Moderate friction: {detail}, {question_count} question(s)"

    # Score 1: Over 120 words, bullets, multiple CTAs, etc.
    reasons = []
    if word_count > 120:
        reasons.append(f"{word_count} words (limit: 120, 23.4% at 125-149)")
    if has_bullets:
        reasons.append("contains bullet lists (-2.2 pp)")
    if stat_count > 2:
        reasons.append(f"{stat_count} stat mentions (feature dump risk)")
    if cta_count > 1:
        reasons.append(f"{cta_count} CTAs")
    if question_count >= 3:
        reasons.append(f"{question_count} questions (3+ = 14.3% reply rate)")
    return 1, f"High friction: {', '.join(reasons)}"


def compute_mqs(message: str, prospect: Optional[ProspectRecord] = None) -> MQSBreakdown:
    """Compute the full 12-point Message Quality Score."""
    oc, oc_r = score_opener_clarity(message)
    cc, cc_r = score_cta_confidence(message)
    pd, pd_r = score_personalization(message, prospect)
    fr, fr_r = score_friction(message)

    return MQSBreakdown(
        opener_clarity=oc,
        cta_confidence=cc,
        personalization_density=pd,
        friction=fr,
        total=oc + cc + pd + fr,
        opener_rationale=oc_r,
        cta_rationale=cc_r,
        personalization_rationale=pd_r,
        friction_rationale=fr_r
    )


# ============================================================
# SECTION 5: QA GATE
# ============================================================

def run_qa_gate(message: str, prospect: Optional[ProspectRecord] = None,
                touch_type: str = "outreach", send_hour: Optional[int] = None) -> QAResult:
    """
    Run the full 10-check QA gate on a message. Returns pass/fail with details.

    10 QA Checks (from CLAUDE.md):
    1. Hard Constraint scan (all 10 HCs)
    2. MQS score computation (4 dimensions)
    3. Threshold enforcement (>=9/12 for outreach)
    4. Word count check (75-99 optimal for Touch 1)
    5. Question count check (exactly 2 for Touch 1)
    6. Structural dedup (checked at batch level, not here)
    7. Evidence check (checked at batch level, not here)
    8. Angle rotation check (checked at batch level, not here)
    9. Phrase toxicity scan
    10. CTA validation

    touch_type options:
      - "outreach" (Touch 1) - full rules, threshold >=9, 75-99 words
      - "followup" (Touch 3, 5) - full rules, threshold >=9, 40-70 words
      - "breakup" (Touch 6) - relaxed rules, threshold >=6, 30-50 words
      - "call" (Touch 2, 4 call scripts) - minimal rules
    """
    violations = scan_hard_constraints(message, send_hour)
    mqs = compute_mqs(message, prospect)
    warnings = []
    word_count = len(message.split())
    question_count = message.count('?')

    # Check 1: Hard Constraint scan (done above)

    # Check for structural issues
    if not message.strip():
        violations.append(HardConstraintViolation(
            "EMPTY", "Empty message", "CRITICAL", "", "Cannot send empty message"))

    # Check for em dashes (SOP rule)
    if '\u2014' in message:
        warnings.append("Contains em dash (\u2014). SOP requires commas or short hyphens only.")

    # Check 9: Phrase toxicity scan
    toxic_found = scan_toxic_phrases(message)
    for tf in toxic_found:
        warnings.append(f"Toxic phrase '{tf['phrase']}': {tf['reply_rate']}% reply rate ({tf['vs_baseline']:+.1f} pp vs baseline)")

    # Check for high-performing phrases (positive feedback)
    good_found = scan_high_performing_phrases(message)
    for gf in good_found:
        warnings.append(f"[GOOD] High-performing phrase '{gf['phrase']}': {gf['reply_rate']}% reply rate ({gf['vs_baseline']:+.1f} pp)")

    # Breakup messages have different rules (SOP: "never pitch, purely respectful close-out")
    if touch_type == "breakup":
        # Check 4: Word count for breakups (30-50 words)
        if word_count > 50:
            warnings.append(f"Breakup message is {word_count} words (SOP target: 30-50).")
        has_critical = any(v.severity == "CRITICAL" for v in violations)
        if has_critical:
            recommendation = "REWRITE"
            passed = False
        elif mqs.total < 6:
            recommendation = "REWRITE"
            passed = False
        else:
            recommendation = "SEND"
            passed = True
        return QAResult(passed=passed, mqs=mqs, violations=violations,
                       warnings=warnings, recommendation=recommendation)

    # Call scripts have minimal rules
    if touch_type == "call":
        has_critical = any(v.severity == "CRITICAL" for v in violations)
        recommendation = "REWRITE" if has_critical else "SEND"
        return QAResult(passed=not has_critical, mqs=mqs, violations=violations,
                       warnings=warnings, recommendation=recommendation)

    # Standard outreach (Touch 1, 3, 5)

    # Check 4: Word count check
    if touch_type == "outreach":
        if word_count < 70 or word_count > 120:
            warnings.append(f"Touch 1 word count: {word_count} (optimal: 75-99 = 39.0% reply rate).")
        elif word_count > 99:
            warnings.append(f"Touch 1 word count: {word_count} (above sweet spot 75-99, rate drops to 27.5% at 100-124).")
    elif touch_type == "followup":
        if word_count > 70:
            warnings.append(f"Follow-up word count: {word_count} (SOP target: 40-70).")

    # Check 5: Question count check (exactly 2 for Touch 1)
    if touch_type == "outreach":
        if question_count != 2:
            warnings.append(f"Question marks: {question_count} (optimal: exactly 2 = 34.8% reply rate vs 23.4% for 1, 14.3% for 3+).")

    # Check for Testsigma mention
    if 'testsigma' not in message.lower() and touch_type in ("outreach", "followup"):
        warnings.append("No Testsigma mention. Proof point should name Testsigma once.")

    # Check 10: CTA validation
    if touch_type in ("outreach", "followup") and '?' not in message[-100:]:
        warnings.append("No question mark in final 100 chars. CTA should end with a question mark.")

    # Check 2 & 3: MQS threshold enforcement
    has_critical = any(v.severity == "CRITICAL" for v in violations)
    has_high = any(v.severity == "HIGH" for v in violations)

    if has_critical or mqs.total < 7:
        recommendation = "REJECT"
        passed = False
    elif has_high or mqs.total < 9:
        recommendation = "REWRITE"
        passed = False
    else:
        recommendation = "SEND"
        passed = True

    return QAResult(
        passed=passed,
        mqs=mqs,
        violations=violations,
        warnings=warnings,
        recommendation=recommendation
    )


# ============================================================
# SECTION 6: PROSPECT PRIORITIZATION
# ============================================================

def compute_reply_likelihood(prospect: ProspectRecord) -> float:
    """
    Estimate reply likelihood based on historical patterns.
    Returns 0.0-1.0 score.

    Based on observed data (1,326 conversations, 381 replies):
    - Architect: 39.3% reply rate (n=56) - HIGHEST, undervalued
    - Manager/Lead: 26.8% (n=471) - Best volume + rate combo
    - Director: 26.0% (n=208) - Has budget, decent rate
    - Senior IC: 30.0% (n=70) - Good if QA/SDET titled
    - VP: 11.9% (n=42) - Deprioritize unless Buyer Intent
    - C-Level: 9.1% (n=11) - Almost never worth cold outreach
    - Buyer Intent is strongest signal
    """
    score = 0.0
    title_lower = prospect.title.lower()

    # Persona type (from observed reply rates, data-weighted)
    is_qa_titled = any(t in title_lower for t in ['qa', 'quality', 'test', 'sdet', 'automation'])

    if any(s in title_lower for s in ['architect']):
        score += 0.35  # Architect: 39.3% reply rate, +10.6 pp above baseline
    elif is_qa_titled:
        if any(s in title_lower for s in ['director', 'head', 'sr director', 'senior director']):
            score += 0.28  # Director of QA: 26.0% (n=208), has budget
        elif any(s in title_lower for s in ['manager', 'lead']):
            score += 0.27  # Manager/Lead: 26.8% (n=471), best volume + rate
        elif any(s in title_lower for s in ['senior', 'sr', 'principal', 'staff']):
            score += 0.25  # Senior IC: 30.0% (n=70)
        elif any(s in title_lower for s in ['vp', 'vice president']):
            score += 0.15  # VP of QA: better than VP Eng but still lower
        else:
            score += 0.18  # IC QA: 22.8% (n=206)
    elif any(t in title_lower for t in ['vp', 'vice president', 'svp']):
        if any(t in title_lower for t in ['engineering', 'technology', 'product']):
            if prospect.employee_count > 50000:
                score += 0.03  # VP Eng at mega-corp: 11.9%, almost never worth it
            else:
                score += 0.08  # VP Eng at smaller co: still low
    elif any(t in title_lower for t in ['cto', 'cio', 'chief']):
        score += 0.05  # C-Level: 9.1% (n=11), very low
    elif any(t in title_lower for t in ['engineering', 'software', 'developer']):
        if any(s in title_lower for s in ['manager', 'lead', 'head', 'director']):
            score += 0.15  # Eng leadership: 19.0% (n=21)
        else:
            score += 0.10  # Engineering IC: 21.2% (n=236)

    # Signals
    signal_keys = [s.lower().replace(' ', '_') for s in prospect.signals]

    if 'buyer_intent' in signal_keys:
        score += 0.25  # Strongest boost

    if 'recently_hired' in signal_keys:
        score += 0.10

    # Vertical match
    hot_verticals = ['fintech', 'saas', 'tech', 'healthcare', 'digital_health']
    if prospect.vertical.lower() in hot_verticals:
        score += 0.10

    # Personalization potential (higher personalization = higher reply rate, hypothesized 2-3x)
    if prospect.person_detail and len(prospect.person_detail) > 50:
        score += 0.10  # Can write deep personalization (Score 3)
    elif prospect.company_desc and len(prospect.company_desc) > 30:
        score += 0.05  # Medium personalization (Score 2)

    # Company transformation signals
    cd = prospect.company_desc.lower() if prospect.company_desc else ""
    if any(w in cd for w in ['acqui', 'merger', 'migration', 'scaling', 'launch', 'funding', 'raised']):
        score += 0.10

    # Known competitor tool (gives strong opener angle)
    if any(w in cd for w in ['selenium', 'cypress', 'playwright', 'katalon', 'tosca', 'testim', 'mabl', 'appium']):
        score += 0.08

    return min(score, 1.0)


def prioritize_batch(prospects: List[ProspectRecord], max_size: int = 25) -> List[ProspectRecord]:
    """Select and rank the top prospects by reply likelihood."""
    for p in prospects:
        p.reply_likelihood = compute_reply_likelihood(p)

    # Sort by reply likelihood descending
    ranked = sorted(prospects, key=lambda p: p.reply_likelihood, reverse=True)

    # Filter: only include if MQS >=9 is achievable
    qualified = []
    for p in ranked:
        if p.reply_likelihood < 0.10:
            continue  # Skip long shots unless we need volume
        qualified.append(p)
        if len(qualified) >= max_size:
            break

    return qualified


# ============================================================
# SECTION 7: BATCH VALIDATION
# ============================================================

def validate_batch(prospects_and_messages: List[Dict]) -> Dict:
    """
    Validate an entire batch before presentation.

    Input: List of dicts with keys:
        - prospect: ProspectRecord
        - messages: List of message strings (touch 1, 3, 5, 6)
        - angles: List of angle strings per message

    Returns: Validation report dict
    """
    report = {
        "total_prospects": len(prospects_and_messages),
        "total_messages": 0,
        "avg_mqs": 0.0,
        "pass_count": 0,
        "rewrite_count": 0,
        "reject_count": 0,
        "violations_summary": {},
        "structural_dupes": [],
        "angle_conflicts": [],
        "details": []
    }

    all_scores = []
    message_fingerprints = {}

    for entry in prospects_and_messages:
        prospect = entry.get("prospect")
        messages = entry.get("messages", [])
        angles = entry.get("angles", [])
        prospect_detail = {"name": prospect.full_name if prospect else "Unknown", "messages": []}

        # Check angle rotation
        if len(angles) != len(set(angles)):
            report["angle_conflicts"].append(f"{prospect.full_name}: repeated angle in sequence")

        for i, msg in enumerate(messages):
            report["total_messages"] += 1
            qa = run_qa_gate(msg, prospect)
            all_scores.append(qa.mqs.total)

            msg_detail = {
                "touch": i + 1,
                "mqs": qa.mqs.total,
                "breakdown": asdict(qa.mqs),
                "recommendation": qa.recommendation,
                "violations": [asdict(v) for v in qa.violations],
                "warnings": qa.warnings
            }
            prospect_detail["messages"].append(msg_detail)

            if qa.recommendation == "SEND":
                report["pass_count"] += 1
            elif qa.recommendation == "REWRITE":
                report["rewrite_count"] += 1
            else:
                report["reject_count"] += 1

            # Track violations
            for v in qa.violations:
                key = v.constraint_id
                report["violations_summary"][key] = report["violations_summary"].get(key, 0) + 1

            # Check for structural duplicates (fingerprint = first 50 chars normalized)
            fp = re.sub(r'[A-Z][a-z]+', 'NAME', msg[:100]).lower().strip()
            if fp in message_fingerprints:
                report["structural_dupes"].append(
                    f"Messages for {prospect.full_name} touch {i+1} and "
                    f"{message_fingerprints[fp]} are structurally similar"
                )
            else:
                message_fingerprints[fp] = f"{prospect.full_name} touch {i+1}"

        report["details"].append(prospect_detail)

    if all_scores:
        report["avg_mqs"] = round(sum(all_scores) / len(all_scores), 1)

    return report


# ============================================================
# SECTION 8: CONVENIENCE FUNCTIONS
# ============================================================

def quick_score(message: str, touch_type: str = "outreach") -> str:
    """Quick score a single message. Returns human-readable report."""
    qa = run_qa_gate(message, touch_type=touch_type)
    word_count = len(message.split())
    question_count = message.count('?')

    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"MESSAGE QUALITY SCORE: {qa.mqs.total}/12 [{qa.recommendation}]")
    lines.append(f"{'='*60}")
    lines.append(f"  Word count:         {word_count} {'(OPTIMAL 75-99)' if 75 <= word_count <= 99 else ''}")
    lines.append(f"  Question marks:     {question_count} {'(OPTIMAL = 2)' if question_count == 2 else ''}")
    lines.append(f"  Opener Clarity:     {qa.mqs.opener_clarity}/3 - {qa.mqs.opener_rationale}")
    lines.append(f"  CTA Confidence:     {qa.mqs.cta_confidence}/3 - {qa.mqs.cta_rationale}")
    lines.append(f"  Personalization:    {qa.mqs.personalization_density}/3 - {qa.mqs.personalization_rationale}")
    lines.append(f"  Friction (inv):     {qa.mqs.friction}/3 - {qa.mqs.friction_rationale}")

    if qa.violations:
        lines.append(f"\nVIOLATIONS ({len(qa.violations)}):")
        for v in qa.violations:
            lines.append(f"  [{v.severity}] {v.constraint_name}")
            lines.append(f"    Matched: \"{v.matched_text}\"")
            lines.append(f"    Data: {v.data_basis}")

    if qa.warnings:
        lines.append(f"\nWARNINGS ({len(qa.warnings)}):")
        for w in qa.warnings:
            lines.append(f"  - {w}")

    return '\n'.join(lines)


def score_batch_file(json_path: str) -> str:
    """Score all messages in a batch JSON file."""
    with open(json_path) as f:
        data = json.load(f)

    prospects = data.get("prospects", [])
    entries = []
    total_scores = []
    violations_count = 0
    pass_count = 0

    lines = []
    lines.append(f"BATCH QA REPORT - {data.get('date', 'unknown')}")
    lines.append(f"{'='*60}\n")

    for p in prospects:
        pr = ProspectRecord(
            full_name=p.get("name", ""),
            title=p.get("title", ""),
            company=p.get("company", ""),
            linkedin_url=p.get("linkedin_url", ""),
            vertical=p.get("vertical", ""),
            employee_count=p.get("employee_count", 0),
            persona_type=p.get("persona_type", ""),
            seniority=p.get("seniority", ""),
            signals=p.get("signals", []),
            company_desc=p.get("company_desc", ""),
            person_detail=p.get("person_detail", ""),
        )

        # Map touch keys to touch types for proper QA thresholds
        touch_type_map = {
            "touch_1_body": "outreach",
            "touch_3_body": "outreach",
            "touch_5_body": "outreach",
            "touch_6_body": "breakup",
            "touch_2_call": "call",
            "touch_4_call": "call",
        }

        touches = []
        for key in ["touch_1_body", "touch_3_body", "touch_5_body", "touch_6_body"]:
            if key in p and p[key]:
                touches.append((key, p[key], touch_type_map.get(key, "outreach")))

        lines.append(f"--- {pr.full_name} ({pr.title} @ {pr.company}) ---")

        for touch_name, msg, tt in touches:
            qa = run_qa_gate(msg, pr, touch_type=tt)
            total_scores.append(qa.mqs.total)
            violations_count += len(qa.violations)
            if qa.passed: pass_count += 1

            status = "PASS" if qa.passed else qa.recommendation
            suffix = " [breakup]" if tt == "breakup" else ""
            lines.append(f"  {touch_name}{suffix}: MQS={qa.mqs.total}/12 [{status}]")
            if qa.violations:
                for v in qa.violations:
                    lines.append(f"    [{v.severity}] {v.constraint_name}: \"{v.matched_text[:50]}\"")

        lines.append("")

    # Summary
    avg = round(sum(total_scores) / len(total_scores), 1) if total_scores else 0
    lines.insert(2, f"Prospects: {len(prospects)}")
    lines.insert(3, f"Messages scored: {len(total_scores)}")
    lines.insert(4, f"Average MQS: {avg}/12")
    lines.insert(5, f"Pass rate: {pass_count}/{len(total_scores)} ({round(pass_count/max(len(total_scores),1)*100,1)}%)")
    lines.insert(6, f"Total violations: {violations_count}")
    lines.insert(7, "")

    return '\n'.join(lines)


# ============================================================
# MAIN (for testing)
# ============================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "score-batch":
        path = sys.argv[2] if len(sys.argv) > 2 else "run-bundle-batch2.json"
        print(score_batch_file(path))

    elif len(sys.argv) > 1 and sys.argv[1] == "demo":
        # Demo with a sample message
        good_msg = """Aditi, with Aethereus acquiring Myridius last year, how's the QE strategy holding up through the integration?

That's the moment where test suites built for one platform suddenly need to cover two, and maintenance tends to spiral.

Hansard cut regression from 8 weeks to 5 weeks using AI auto-heal with Testsigma during a similar integration period.

Would 15 minutes to compare approaches be useful while you're navigating the transition?"""

        bad_msg = """Hi John,

I'm reaching out because I noticed you're the QA Manager at Acme Corp and oversee software testing within an Agile team.

Testsigma is a low code automation platform and could be of use to you because it has been able to:
- Improve release velocity
- Decrease bugs sent to production
- Cut maintenance by 85%
- Increase test execution speed by 300%
- Auto heal broken tests automatically

Companies like Cisco, Samsung, and Honeywell have all seen a major increase in testing efficiency.

What are your initiatives towards improving test automation in the new year?

Best,
Rob"""

        print("GOOD MESSAGE:")
        print(quick_score(good_msg))
        print("\n" + "="*60 + "\n")
        print("BAD MESSAGE:")
        print(quick_score(bad_msg))
    else:
        print("Usage:")
        print("  python outbound_qa_engine.py demo          # Score sample messages")
        print("  python outbound_qa_engine.py score-batch [file.json]  # Score a batch")
