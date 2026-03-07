#!/usr/bin/env python3
"""
Outbound Intelligence & QA Engine
==================================
Testsigma BDR - Rob Gorham
Built on: LinkedIn Outreach Analysis (Feb 2026)
Source: 1,330 conversations, 384 reply threads, 6,210 messages

This engine provides:
1. Message Quality Scoring (MQS) - 12-point system
2. Hard Constraint violation detection (HC1-HC10, all 10 enforced)
3. QA Gate enforcement (14-point check)
4. Prospect prioritization (reply-likelihood model)
5. Batch validation and reporting

ALL rules are derived from observed data. No external best practices.
"""

import re
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from datetime import datetime


# ============================================================
# SECTION 1: CANONICAL RULES (from outbound-intelligence.md)
# ============================================================

# Hard Constraints - violation = automatic rejection
# Labeled HC1-HC10 exactly per the canonical rules document
HARD_CONSTRAINTS = {
    "HC1_i_noticed": {
        "name": "No 'I noticed' / 'I saw' / 'I see' phrasing",
        "pattern": r"(?i)\b(i\s+noticed|i\s+saw\s+that|i\s+saw\s+you|i\s+see\s+that|i\s+see\s+you|based on your profile|i\s+came across)",
        "data_basis": "-13.4 pp diff (10.9% reply vs 24.3% no-reply). Strongest negative signal.",
        "severity": "CRITICAL"
    },
    "HC2_ai_headline": {
        "name": "No leading with AI/ML/self-healing as headline feature",
        "pattern": r"(?i)(our (ai|platform|tool) (auto[- ]?heals?|creates?|maintains?|executes?)|auto[- ]?heal(s|ing)\b|self[- ]?healing (function|feature|capability)|low[- ]?code automation platform|nlp[- ]?based|natural language (processing|programming) (test|platform))",
        "data_basis": "AI mention: -9.2 pp (11.1% vs 20.3%). Self-healing: -6.2 pp (10.3% vs 16.5%).",
        "severity": "CRITICAL"
    },
    "HC3_too_long": {
        "name": "No messages over 120 words",
        "check": "word_count",
        "threshold": 120,
        "data_basis": "75-99w = 39.0% reply rate. 125-149w = 23.4%. 150+ = 21.2%.",
        "severity": "HIGH"
    },
    "HC4_evening_send": {
        "name": "No evening sends (after 6 PM)",
        "check": "timing",
        "data_basis": "Evening (6-8 PM): 12.1% reply rate vs 56.5% for lunch window. -44.4 pp.",
        "severity": "HIGH"
    },
    "HC5_bullet_list": {
        "name": "No bullet-point or numbered-list feature dumps",
        "pattern": r"(\n\s*[-\u2022*]\s+.+\n\s*[-\u2022*]\s+)|(\n\s*\d+\.\s+.+\n\s*\d+\.\s+)",
        "data_basis": "Bullets: -2.2 pp diff (1.0% reply vs 3.2% no-reply). Zero high-performers use bullets.",
        "severity": "HIGH"
    },
    "HC6_permission_cta": {
        "name": "No 'would it be unreasonable' as sole CTA",
        "pattern": r"(?i)(would it be unreasonable|happy to share (more )?if\s|feel free to|no worries if|if not.{0,10}all good|no pressure)",
        "data_basis": "'Would it be unreasonable' as CTA: 12.8% reply rate (n=39).",
        "severity": "MEDIUM"
    },
    "HC7_phone_ask": {
        "name": "No phone-number asks",
        "pattern": r"(?i)(what('?s| is) your (phone|number|cell|direct)|drop my (number|#|cell)|call you at|give you a ring|best number to reach)",
        "data_basis": "Phone ask CTA: 5.0% reply rate (n=40). Worst-performing CTA by far.",
        "severity": "CRITICAL"
    },
    "HC8_reaching_out": {
        "name": "No 'reaching out' / 'wanted to connect' phrasing",
        "pattern": r"(?i)\b(i'?m reaching out|reaching out to you|wanted to connect|wanted to reach)\b",
        "data_basis": "-2.4 pp diff on first messages. Correlates with template-visible openers.",
        "severity": "HIGH"
    },
    "HC9_toxic_phrases": {
        "name": "No 'I figure' / 'would you like to share' / 'enough about me'",
        "pattern": r"(?i)\b(i figure|would you like to share|enough about me)\b",
        "data_basis": "'I figure': 9.8% (-19.0 pp). 'Would you like to share': 15.2% (-13.6 pp). 'Enough about me': 18.2% (-10.6 pp).",
        "severity": "CRITICAL"
    },
    "HC10_too_many_questions": {
        "name": "No 3+ question marks per message",
        "check": "question_count",
        "threshold": 3,
        "data_basis": "3 questions: 14.3% reply rate (n=7). Optimal is exactly 2 questions (34.8%).",
        "severity": "HIGH"
    },
}

# Toxic phrases that should trigger warnings (not hard fails but strong negative signals)
TOXIC_PHRASES = {
    "flaky tests": {"rate": "16.8%", "diff": "-11.9 pp", "severity": "HIGH"},
    "CI/CD": {"rate": "23.6%", "diff": "-5.1 pp", "severity": "MEDIUM"},
    "low code": {"rate": "25.8%", "diff": "-2.9 pp", "severity": "MEDIUM"},
}

# Generic closes that are BANNED per the rules
BANNED_CLOSES = [
    r"worth comparing notes\??",
    r"worth a quick chat\??",
    r"would exploring that be worth your time\??",
    r"thought it would be worth connecting\.?",
    r"worth a quick compare\??",
]

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
    },
    "cisco": {
        "text": "Cisco achieved 35% regression reduction",
        "short": "Cisco: 35% regression reduction",
        "verticals": ["enterprise", "tech", "networking"],
        "angle": "maintenance",
        "numbers": "35% reduction"
    },
    "meesho": {
        "text": "Meesho achieved 4X faster automation scaling",
        "short": "Meesho: 4X faster automation",
        "verticals": ["ecommerce", "retail"],
        "angle": "velocity",
        "numbers": "4X faster"
    },
    "freshworks": {
        "text": "Freshworks reduced flakiness at scale with codeless self-healing",
        "short": "Freshworks: flakiness reduced at scale",
        "verticals": ["saas", "tech"],
        "angle": "maintenance",
        "numbers": "flakiness reduced"
    },
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
    research_quality: str = ""
    research_sources: List[str] = field(default_factory=list)


# ============================================================
# SECTION 3: HARD CONSTRAINT SCANNER
# ============================================================

def scan_hard_constraints(message: str, send_hour: int = -1) -> List[HardConstraintViolation]:
    """Scan a message for ALL hard constraint violations (HC1-HC10)."""
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
        elif rule.get("check") == "timing":
            if send_hour >= 18:
                violations.append(HardConstraintViolation(
                    constraint_id=cid,
                    constraint_name=rule["name"],
                    severity=rule["severity"],
                    matched_text=f"Send hour: {send_hour}:00 (after 6 PM)",
                    data_basis=rule["data_basis"]
                ))
        elif rule.get("check") == "question_count":
            q_count = message.count('?')
            if q_count >= rule["threshold"]:
                violations.append(HardConstraintViolation(
                    constraint_id=cid,
                    constraint_name=f"{rule['name']} (got {q_count})",
                    severity=rule["severity"],
                    matched_text=f"Question marks: {q_count} >= {rule['threshold']}",
                    data_basis=rule["data_basis"]
                ))

    return violations


# ============================================================
# SECTION 4: MESSAGE QUALITY SCORER (MQS)
# ============================================================

def score_opener_clarity(message: str, prospect: Optional[ProspectRecord] = None) -> Tuple[int, str]:
    """
    Score opener clarity 1-3 per MQS Dimension 1.

    3 = Specific, insight-driven question about the prospect's situation.
        No "I noticed," no role-recap, no "reaching out."
    2 = Company-specific reference but generic frame.
    1 = Opens with "I noticed," role recap, or generic question.
    """
    lines = message.strip().split('\n')
    first_meaningful = ""
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r'^(hey|hi|hello|dear)\s+\w+[,.]?\s*$', stripped, re.IGNORECASE):
            continue
        first_meaningful = stripped
        break

    if not first_meaningful:
        return 1, "No meaningful opener found"

    fl = first_meaningful.lower()

    # Instant score 1: HC1 violations
    if re.search(r'\b(i\s+noticed|i\s+saw|i\s+see\s+that|based on your profile|i\s+came across)\b', fl):
        return 1, "Opens with 'I noticed/saw' phrasing (HC1 violation, -13.4 pp)"

    # Instant score 1: Role recap
    if re.search(r'(seeing that you|as the .{5,40} at |you\'?re the .{5,40} at )', fl):
        return 1, "Opens with role-at-company recap (HC2 pattern, -12.7 pp)"

    # Instant score 1: Generic question opener
    if re.search(r'^are you (looking|searching|interested|evaluating|considering)', fl):
        return 1, "Generic question opener (16.4% reply rate, worst common style)"

    # Instant score 1: Reaching out
    if re.search(r'\b(reaching out|wanted to connect|wanted to reach)\b', fl):
        return 1, "Opens with 'reaching out/wanted to connect' (HC8 violation)"

    # Score 3: Question that references specific prospect situation
    if '?' in first_meaningful:
        has_prospect_specifics = False
        if prospect:
            comp = prospect.company.lower()
            if comp and len(comp) > 2 and comp in fl:
                has_prospect_specifics = True
            if prospect.person_detail:
                detail_words = set(w for w in prospect.person_detail.lower().split()
                                   if len(w) > 4 and w not in {'their', 'about', 'which', 'other', 'these', 'those'})
                msg_words = set(fl.split())
                if len(detail_words & msg_words) >= 2:
                    has_prospect_specifics = True
        if re.search(r'(migration|acquisition|integration|platform|launch|refresh|consolidat)', fl):
            has_prospect_specifics = True
        if re.search(r'(shipping|releasing|deploying|scaling|expanding|growing)', fl):
            has_prospect_specifics = True

        if has_prospect_specifics:
            return 3, "Opens with specific, insight-driven question about the prospect's situation"
        return 2, "Opens with a question but could be more specific to the prospect's situation"

    # Score 3: Company event opener
    if prospect and prospect.company and len(prospect.company) > 2 and prospect.company.lower() in fl:
        if re.search(r'(acquisition|migration|launch|hiring|expansion|raised|integration)', fl):
            return 3, "Opens with specific company event reference (high personalization)"

    # Score 2: Some specificity
    if re.search(r'(your|team|company|platform|product|stack)', fl):
        return 2, "Company-specific reference but generic frame"

    return 2, "Moderate opener, has some context but could be sharper"


def score_cta_confidence(message: str) -> Tuple[int, str]:
    """
    Score CTA confidence 1-3 per MQS Dimension 2.

    3 = "What day works?" with tie to proof point outcome AND prospect situation.
    2 = Uses "what day works" but tie to proof point is weak or generic.
    1 = Permission-based, phone ask, open-ended question, or generic close.
    """
    tail = message[-400:].lower() if len(message) > 400 else message.lower()

    lines = [l.strip() for l in message.strip().split('\n') if l.strip()]
    close_lines = []
    for line in reversed(lines):
        if re.match(r'^(rob|best|regards|cheers|thanks)\s*,?\s*$', line, re.IGNORECASE):
            continue
        close_lines.insert(0, line)
        if len(close_lines) >= 2:
            break
    close_text = ' '.join(close_lines).lower()

    # Instant score 1: Permission-based CTAs
    if re.search(r'(would it be unreasonable|happy to share (more )?if|feel free to|no worries|if not.{0,10}all good|no pressure)', tail):
        return 1, "Permission-based CTA (HC6 violation, 12.8% rate)"

    # Instant score 1: Phone asks
    if re.search(r'(what.?s your (number|phone|cell)|drop my|give you a ring)', tail):
        return 1, "Phone ask CTA (HC7 violation, 5.0% rate)"

    # Instant score 1: Open-ended question closes
    if re.search(r'(what are your (initiatives|priorities|focus)|what.?s your (priority|focus|strategy)|what are you focusing)', tail):
        return 1, "Open-ended question CTA (14.0% rate, puts work on prospect)"

    # Instant score 1: Banned generic closes
    for pattern in BANNED_CLOSES:
        if re.search(pattern, tail, re.IGNORECASE):
            return 1, "Banned generic close (could be pasted into any message)"

    # Check for "what day works" pattern (optimal CTA, 40.4% reply rate)
    has_what_day = bool(re.search(r'what day works', close_text))

    # Check if close ties to a proof point outcome
    has_proof_tie = bool(re.search(
        r'(\d+%|\d+ (weeks?|days?|minutes?|hours?|months?)|half|fewer|less|cut|reduction|faster)',
        close_text
    ))

    # Check if close references prospect's specific situation
    has_prospect_tie = bool(re.search(
        r'(your|the .{3,30} (schedule|timeline|launch|migration|refresh|platform|releases?))',
        close_text
    ))

    if has_what_day and has_proof_tie and has_prospect_tie:
        return 3, "Direct 'what day works' CTA tied to proof point outcome AND prospect's situation (40.4% rate)"
    elif has_what_day and has_proof_tie:
        return 3, "Direct 'what day works' CTA with proof point tie (40.4% rate)"
    elif has_what_day:
        return 2, "'What day works' CTA present but not tied to proof point outcome"

    # Direct meeting ask without "what day works"
    if re.search(r'(quick (call|chat|look)|15 minutes|\d+ minutes|see how)', close_text) and '?' in close_text:
        return 2, "Has meeting ask with question but should use 'what day works' pattern"

    if '?' in tail[-80:]:
        return 2, "Ends with a question but CTA could be more specific"

    return 1, "No clear CTA or question at close"


def score_personalization(message: str, prospect: Optional[ProspectRecord] = None) -> Tuple[int, str]:
    """
    Score personalization density 1-3 per MQS Dimension 3.

    3 = References something only THIS person would recognize.
    2 = References their company specifically but could apply to anyone in that role.
    1 = Only swaps name, title, company. Indistinguishable from a template.
    """
    ml = message.lower()
    person_specific_signals = 0

    if prospect and prospect.person_detail:
        detail_words = set(w for w in prospect.person_detail.lower().split()
                          if len(w) > 4 and w not in {
                              'their', 'about', 'which', 'other', 'these', 'those',
                              'working', 'experience', 'years', 'company', 'manager'
                          })
        msg_words = set(ml.split())
        overlap = detail_words & msg_words
        if len(overlap) >= 3:
            person_specific_signals += 2

    # Specific product/project names
    product_refs = len(re.findall(
        r'(?:(?:the|your)\s+)?[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?\s+(?:platform|product|app|suite|module|integration|migration|launch|refresh)',
        message
    ))
    if product_refs >= 1:
        person_specific_signals += 1

    # Company events
    event_signals = [
        r"(acquisition|acquiring|acquired|merger|merged)",
        r"(launched|launch of|shipped|release of|new product)",
        r"(migration|migrating|transitioning|platform refresh|consolidat)",
        r"(integration|integrating|post-acquisition)",
    ]
    event_refs = sum(1 for pat in event_signals if re.search(pat, ml))
    person_specific_signals += event_refs

    # Technology references specific to their stack
    tech_refs = len(re.findall(r'(?i)\b(selenium|cypress|playwright|katalon|tosca|testim|mabl|appium|provar|accelq)\b', ml))
    if tech_refs >= 1:
        person_specific_signals += 1

    if person_specific_signals >= 3:
        return 3, f"Deep personalization: {person_specific_signals} person/company-specific references"
    elif person_specific_signals >= 1:
        if prospect and prospect.company and len(prospect.company) > 2 and prospect.company.lower() in ml:
            if person_specific_signals >= 2:
                return 3, "References company by name with specific events/products (person-specific)"
            return 2, "References company specifically but opener could apply to anyone in that role"
        return 2, "Has some specifics but could go deeper"
    else:
        if prospect and prospect.company and len(prospect.company) > 2 and prospect.company.lower() in ml:
            return 2, "References company by name but no deeper specifics"
        return 1, "Surface-level personalization (name/title swap only). Template-visible."


def score_friction(message: str, touch_number: int = 1) -> Tuple[int, str]:
    """
    Score friction 1-3 (inverted: 3=low friction) per MQS Dimension 4.

    3 = Sweet spot word count, exactly 2 questions, 4+ paragraphs,
        no bullets, max 1 hyphen, max 3 sentences per paragraph.
    2 = Slightly over optimal, still readable.
    1 = Over limits, bullets, wall-of-text, too many hyphens.
    """
    word_count = len(message.split())
    has_bullets = bool(re.search(r'(\n\s*[-\u2022*]\s+.+\n\s*[-\u2022*]\s+)|(\n\s*\d+\.\s+.+\n\s*\d+\.\s+)', message))
    question_count = message.count('?')
    para_breaks = len(re.findall(r'\n\s*\n', message))

    # Hyphen audit: count hyphens used as mid-sentence dashes
    body_lines = message.strip().split('\n')
    body_text = '\n'.join(body_lines[:-1]) if body_lines else message
    dash_hyphens = len(re.findall(r'\s-\s', body_text))

    # CTA count
    cta_count = len(re.findall(r'(?i)(would|could|should|want|available|interested)\s.{5,40}\?', message))

    # Max sentences per paragraph
    paragraphs = re.split(r'\n\s*\n', message)
    max_sentences_in_para = 0
    for para in paragraphs:
        sentences = len(re.findall(r'[.!?]+', para))
        max_sentences_in_para = max(max_sentences_in_para, sentences)

    # Touch-specific expectations
    if touch_number == 1:
        optimal_low, optimal_high, max_words = 80, 110, 120
    elif touch_number == 2:
        optimal_low, optimal_high, max_words = 40, 70, 70
    elif touch_number == 3:
        optimal_low, optimal_high, max_words = 60, 100, 100
    else:
        optimal_low, optimal_high, max_words = 60, 110, 120

    good_word_count = optimal_low <= word_count <= optimal_high
    good_questions = (question_count == 2) if touch_number == 1 else (1 <= question_count <= 2)
    good_spacing = para_breaks >= 3
    good_hyphens = dash_hyphens <= 1
    no_bullets = not has_bullets
    good_cta_count = cta_count <= 1
    good_para_length = max_sentences_in_para <= 3

    if (good_word_count and good_questions and good_spacing and
            good_hyphens and no_bullets and good_cta_count and good_para_length):
        return 3, f"Low friction: {word_count}w, {question_count}q, {para_breaks+1} paragraphs, clean structure"

    issues = []
    if word_count > max_words:
        issues.append(f"{word_count}w (max {max_words})")
    elif word_count > optimal_high:
        issues.append(f"{word_count}w (sweet spot {optimal_low}-{optimal_high})")
    if has_bullets:
        issues.append("bullet lists")
    if question_count >= 3 and touch_number == 1:
        issues.append(f"{question_count} questions (optimal: 2)")
    elif question_count == 0:
        issues.append("no questions")
    if para_breaks < 3:
        issues.append(f"only {para_breaks+1} paragraphs (need 4+)")
    if dash_hyphens > 1:
        issues.append(f"{dash_hyphens} mid-sentence hyphens (max 1)")
    if max_sentences_in_para > 3:
        issues.append(f"paragraph with {max_sentences_in_para} sentences (max 3)")
    if cta_count > 1:
        issues.append(f"{cta_count} CTAs")

    if len(issues) <= 2 and word_count <= max_words and not has_bullets:
        return 2, f"Moderate friction: {', '.join(issues) if issues else 'could be tighter'}"
    else:
        return 1, f"High friction: {', '.join(issues)}"


def compute_mqs(message: str, prospect: Optional[ProspectRecord] = None,
                touch_number: int = 1) -> MQSBreakdown:
    """Compute the full 12-point Message Quality Score."""
    oc, oc_r = score_opener_clarity(message, prospect)
    cc, cc_r = score_cta_confidence(message)
    pd, pd_r = score_personalization(message, prospect)
    fr, fr_r = score_friction(message, touch_number)

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
# SECTION 5: QA GATE (14-point check)
# ============================================================

def run_qa_gate(message: str, prospect: Optional[ProspectRecord] = None,
                touch_number: int = 1, touch_type: str = "outreach",
                send_hour: int = -1) -> QAResult:
    """
    Run the full 14-point QA gate on a message.

    Checks per outbound-intelligence.md:
    1. Hard Constraint scan (HC1-HC10)
    2. MQS score computation
    3. Threshold enforcement (>=9)
    4. Word count check
    5. Question count check (exactly 2 for Touch 1)
    6. Structural dedup (batch-level, in validate_batch)
    7. Evidence check (research sources)
    8. Angle rotation check (batch-level, in validate_batch)
    9. Phrase toxicity scan
    10. CTA validation ("what day works" tied to proof point)
    11. Hyphen audit
    12. Paragraph spacing check
    13. Close structure dedup (batch-level, in validate_batch)
    14. Research depth check
    """
    # Check 1: Hard Constraint scan
    violations = scan_hard_constraints(message, send_hour)
    warnings = []

    # Check 2: MQS computation
    mqs = compute_mqs(message, prospect, touch_number)

    if not message.strip():
        violations.append(HardConstraintViolation(
            "EMPTY", "Empty message", "CRITICAL", "", "Cannot send empty message"))

    # Em dash check
    if '\u2014' in message:
        violations.append(HardConstraintViolation(
            "EM_DASH", "Contains em dash (SOP bans em dashes)", "HIGH",
            "Found \u2014", "SOP: NO em dashes. Use commas or short hyphens only."
        ))

    # Follow-up / call have relaxed rules
    if touch_type in ("followup", "call"):
        has_critical = any(v.severity == "CRITICAL" for v in violations)
        threshold = 7 if touch_type == "followup" else 4
        if has_critical:
            return QAResult(passed=False, mqs=mqs, violations=violations,
                           warnings=warnings, recommendation="REWRITE")
        if mqs.total < threshold:
            return QAResult(passed=False, mqs=mqs, violations=violations,
                           warnings=warnings, recommendation="REWRITE")
        return QAResult(passed=True, mqs=mqs, violations=violations,
                       warnings=warnings, recommendation="SEND")

    # === Standard outreach - full 14-point gate ===

    # Check 4: Word count
    word_count = len(message.split())
    if touch_number == 1:
        if word_count < 80:
            warnings.append(f"Touch 1 under 80 words ({word_count}w). Sweet spot is 80-99w (39.0% reply rate).")
        elif 99 < word_count <= 120:
            warnings.append(f"Touch 1 at {word_count}w. Sweet spot is 80-99w (39.0% reply rate).")
    elif touch_number == 3:
        if word_count < 60:
            warnings.append(f"Touch 3 under 60 words ({word_count}w). Target 60-100w.")
        elif word_count > 100:
            warnings.append(f"Touch 3 over 100 words ({word_count}w). Target 60-100w.")

    # Check 5: Question count
    q_count = message.count('?')
    if touch_number == 1:
        if q_count == 0:
            warnings.append("No question marks. Touch 1 requires exactly 2 (34.8% reply rate).")
        elif q_count == 1:
            warnings.append("Only 1 question mark. Touch 1 optimal is exactly 2 (34.8% vs 23.4% for 1).")
    elif q_count == 0:
        warnings.append("No question mark in message.")

    # Check 7: Evidence check
    if prospect and hasattr(prospect, 'research_sources') and prospect.research_sources:
        sources = prospect.research_sources
        if len(sources) < 3:
            missing = set(["linkedin", "apollo", "company"]) - set(s.lower() for s in sources)
            if missing:
                warnings.append(f"Research incomplete: missing sources {missing}. Need all 3.")

    # Check 9: Phrase toxicity scan
    ml = message.lower()
    for phrase, info in TOXIC_PHRASES.items():
        if phrase.lower() in ml:
            sev = info["severity"]
            if sev == "HIGH":
                violations.append(HardConstraintViolation(
                    "TOXIC_PHRASE", f"Toxic phrase: '{phrase}'", "HIGH",
                    phrase, f"Reply rate: {info['rate']} ({info['diff']} vs baseline)"
                ))
            else:
                warnings.append(f"Toxic phrase detected: '{phrase}' ({info['rate']} reply rate, {info['diff']})")

    # Check 10: CTA validation
    tail = message[-400:].lower() if len(message) > 400 else message.lower()
    if touch_number == 1:
        if 'what day works' not in tail and 'what day would' not in tail:
            warnings.append("Close missing 'what day works' pattern (40.4% rate, best CTA at scale).")

    for pattern in BANNED_CLOSES:
        if re.search(pattern, tail, re.IGNORECASE):
            violations.append(HardConstraintViolation(
                "GENERIC_CLOSE", "Banned generic close detected", "HIGH",
                re.search(pattern, tail, re.IGNORECASE).group(0),
                "Generic closes could be pasted into any message. Must be prospect-specific."
            ))
            break

    # Check 11: Hyphen audit
    body_lines = message.strip().split('\n')
    body_text = '\n'.join(body_lines[:-1]) if body_lines else message
    dash_count = len(re.findall(r'\s-\s', body_text))
    if dash_count >= 2:
        violations.append(HardConstraintViolation(
            "HYPHEN_ABUSE", f"Too many mid-sentence hyphens ({dash_count})", "HIGH",
            f"{dash_count} hyphens used as dashes",
            "Hyphens as mid-sentence dashes are an AI writing signature. Max 1 allowed."
        ))
    elif dash_count == 1:
        warnings.append("1 mid-sentence hyphen detected. Consider replacing with comma.")

    # Check 12: Paragraph spacing
    para_breaks = len(re.findall(r'\n\s*\n', message))
    if para_breaks < 3:
        violations.append(HardConstraintViolation(
            "WALL_OF_TEXT", f"Insufficient paragraph breaks ({para_breaks + 1} paragraphs, need 4+)", "HIGH",
            f"Only {para_breaks + 1} paragraphs",
            "Opener, context, proof point, and close must each be separate paragraphs."
        ))

    paragraphs = re.split(r'\n\s*\n', message)
    for i, para in enumerate(paragraphs):
        sentences = len(re.findall(r'[.!?]+', para))
        if sentences > 3:
            warnings.append(f"Paragraph {i+1} has {sentences} sentences (max 3).")

    # Check 14: Testsigma mention (proof point should name Testsigma once)
    if 'testsigma' not in message.lower():
        warnings.append("No Testsigma mention. Proof point should name Testsigma once.")

    # Check 3: Threshold enforcement
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
    """Estimate reply likelihood based on historical patterns (0.0-1.0)."""
    score = 0.0
    title_lower = prospect.title.lower()

    if any(t in title_lower for t in ['architect']):
        score += 0.35
    elif any(t in title_lower for t in ['qa', 'quality', 'test']):
        if any(s in title_lower for s in ['director', 'head']):
            score += 0.26
        elif any(s in title_lower for s in ['manager', 'lead']):
            score += 0.27
        elif any(s in title_lower for s in ['senior', 'sdet', 'principal']):
            score += 0.30
        else:
            score += 0.15
    elif any(t in title_lower for t in ['vp', 'vice president']):
        score += 0.05 if prospect.employee_count > 50000 else 0.12
    elif any(t in title_lower for t in ['cto', 'chief technology', 'c-level']):
        score += 0.09

    signal_set = [s.lower().replace(' ', '_') for s in prospect.signals]
    if 'buyer_intent' in signal_set:
        score += 0.25
    if 'recently_hired' in signal_set:
        score += 0.10

    hot_verticals = ['fintech', 'saas', 'tech', 'healthcare', 'digital_health']
    if prospect.vertical.lower() in hot_verticals:
        score += 0.10

    if prospect.person_detail and len(prospect.person_detail) > 50:
        score += 0.10
    elif prospect.company_desc and len(prospect.company_desc) > 30:
        score += 0.05

    cd = prospect.company_desc.lower() if prospect.company_desc else ""
    if any(w in cd for w in ['acqui', 'merger', 'migration', 'scaling', 'launch', 'funding', 'raised']):
        score += 0.10

    return min(score, 1.0)


def prioritize_batch(prospects: List[ProspectRecord], max_size: int = 25) -> List[ProspectRecord]:
    """Select and rank the top prospects by reply likelihood."""
    for p in prospects:
        p.reply_likelihood = compute_reply_likelihood(p)
    ranked = sorted(prospects, key=lambda p: p.reply_likelihood, reverse=True)
    return [p for p in ranked if p.reply_likelihood >= 0.10][:max_size]


# ============================================================
# SECTION 7: BATCH VALIDATION
# ============================================================

def validate_batch(prospects_and_messages: List[Dict]) -> Dict:
    """
    Validate an entire batch. Handles batch-level checks:
    structural dedup, angle rotation, close structure dedup.
    """
    report = {
        "total_prospects": len(prospects_and_messages),
        "total_messages": 0, "avg_mqs": 0.0,
        "pass_count": 0, "rewrite_count": 0, "reject_count": 0,
        "violations_summary": {},
        "structural_dupes": [], "angle_conflicts": [],
        "close_structure_dupes": [], "details": []
    }

    all_scores = []
    message_fingerprints = {}
    close_fingerprints = {}

    for entry in prospects_and_messages:
        prospect = entry.get("prospect")
        messages = entry.get("messages", [])
        angles = entry.get("angles", [])
        touch_numbers = entry.get("touch_numbers", list(range(1, len(messages) + 1)))
        prospect_detail = {"name": prospect.full_name if prospect else "Unknown", "messages": []}

        # Check 8: Angle rotation
        if len(angles) != len(set(angles)):
            report["angle_conflicts"].append(f"{prospect.full_name}: repeated angle in sequence")

        for i, msg in enumerate(messages):
            report["total_messages"] += 1
            tn = touch_numbers[i] if i < len(touch_numbers) else i + 1
            tt = "outreach" if tn in (1, 3) else "followup"
            qa = run_qa_gate(msg, prospect, touch_number=tn, touch_type=tt)
            all_scores.append(qa.mqs.total)

            msg_detail = {
                "touch": tn, "mqs": qa.mqs.total,
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

            for v in qa.violations:
                report["violations_summary"][v.constraint_id] = report["violations_summary"].get(v.constraint_id, 0) + 1

            # Check 6: Structural dedup
            first_line = msg.strip().split('\n')[0][:60]
            fp = re.sub(r'[A-Z][a-z]+', 'NAME', first_line).lower().strip()
            if fp in message_fingerprints and tn == 1:
                report["structural_dupes"].append(
                    f"Structurally similar openers: {prospect.full_name} and {message_fingerprints[fp]}"
                )
            elif tn == 1:
                message_fingerprints[fp] = prospect.full_name

            # Check 13: Close structure dedup
            close_lines = [l.strip() for l in msg.strip().split('\n') if l.strip()]
            close_line = ""
            for cl in reversed(close_lines):
                if not re.match(r'^(rob|best|regards)\s*,?\s*$', cl, re.IGNORECASE):
                    close_line = cl
                    break
            close_fp = re.sub(r'[A-Z][a-z]+', 'NAME', close_line).lower()
            close_fp = re.sub(r'\d+', 'NUM', close_fp)
            if close_fp in close_fingerprints and tn == 1:
                report["close_structure_dupes"].append(
                    f"Close structure duplicate: {prospect.full_name} and {close_fingerprints[close_fp]}"
                )
            elif tn == 1:
                close_fingerprints[close_fp] = prospect.full_name

        report["details"].append(prospect_detail)

    if all_scores:
        report["avg_mqs"] = round(sum(all_scores) / len(all_scores), 1)

    return report


# ============================================================
# SECTION 8: CONVENIENCE FUNCTIONS
# ============================================================

def quick_score(message: str, touch_number: int = 1,
                prospect_json: str = "") -> str:
    """Quick score a single message. Returns human-readable report."""
    prospect = None
    if prospect_json:
        try:
            p = json.loads(prospect_json)
            prospect = ProspectRecord(
                full_name=p.get("name", ""),
                title=p.get("title", ""),
                company=p.get("company", ""),
                vertical=p.get("vertical", ""),
                person_detail=p.get("person_detail", ""),
                company_desc=p.get("company_desc", ""),
                research_sources=p.get("research_sources", []),
            )
        except (json.JSONDecodeError, KeyError):
            pass

    tt = "outreach" if touch_number in (1, 3) else "followup"
    qa = run_qa_gate(message, prospect, touch_number=touch_number, touch_type=tt)

    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"MESSAGE QUALITY SCORE: {qa.mqs.total}/12 [{qa.recommendation}]")
    lines.append(f"Touch: {touch_number} | Words: {len(message.split())} | Questions: {message.count('?')}")
    lines.append(f"{'='*60}")
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

    lines.append(f"\n{'='*60}")
    if qa.passed:
        lines.append("RESULT: PASS - Message is ready to send.")
    else:
        lines.append(f"RESULT: {qa.recommendation} - Fix violations/warnings above before sending.")

    return '\n'.join(lines)


def score_batch_file(json_path: str) -> str:
    """Score all messages in a batch JSON file."""
    with open(json_path) as f:
        data = json.load(f)

    prospects = data.get("prospects", [])
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
            research_sources=p.get("research_sources", []),
        )

        touch_type_map = {
            "touch_1_body": ("outreach", 1),
            "touch_2_body": ("followup", 2),
            "touch_3_body": ("outreach", 3),
        }

        touches = []
        for key in ["touch_1_body", "touch_2_body", "touch_3_body"]:
            if key in p and p[key]:
                tt, tn = touch_type_map.get(key, ("outreach", 1))
                touches.append((key, p[key], tt, tn))

        lines.append(f"--- {pr.full_name} ({pr.title} @ {pr.company}) ---")

        for touch_name, msg, tt, tn in touches:
            qa = run_qa_gate(msg, pr, touch_number=tn, touch_type=tt)
            total_scores.append(qa.mqs.total)
            violations_count += len(qa.violations)
            if qa.passed:
                pass_count += 1

            status = "PASS" if qa.passed else qa.recommendation
            lines.append(f"  {touch_name}: MQS={qa.mqs.total}/12 [{status}] ({len(msg.split())}w, {msg.count('?')}q)")
            if qa.violations:
                for v in qa.violations:
                    lines.append(f"    [{v.severity}] {v.constraint_name}: \"{v.matched_text[:50]}\"")
            if qa.warnings:
                for w in qa.warnings:
                    lines.append(f"    [WARN] {w}")

        lines.append("")

    avg = round(sum(total_scores) / len(total_scores), 1) if total_scores else 0
    lines.insert(2, f"Prospects: {len(prospects)}")
    lines.insert(3, f"Messages scored: {len(total_scores)}")
    lines.insert(4, f"Average MQS: {avg}/12")
    lines.insert(5, f"Pass rate: {pass_count}/{len(total_scores)} ({round(pass_count/max(len(total_scores),1)*100,1)}%)")
    lines.insert(6, f"Total violations: {violations_count}")
    lines.insert(7, "")

    return '\n'.join(lines)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "score-batch":
        path = sys.argv[2] if len(sys.argv) > 2 else "run-bundle-batch2.json"
        print(score_batch_file(path))

    elif len(sys.argv) > 1 and sys.argv[1] == "demo":
        good_msg = """Hey Nisha,

What's harder to keep stable right now, regression across the loan origination workflows or coverage as new dealer integrations come online?

Most auto lending QA teams find that every new integration path adds tests faster than anyone can maintain them.

Hansard (financial services) used Testsigma to cut their regression cycle from 8 weeks to 5 by letting AI handle the test maintenance.

If shaving 3 weeks off regression would help the origination schedule, what day works for a quick look at how they did it?

Rob"""

        bad_msg = """Hi John,

I'm reaching out because I noticed you're the QA Manager at Acme Corp and oversee software testing within an Agile team.

Mabl is a low code automation platform and could be of use to you because it has been able to:
- Improve release velocity
- Decrease bugs sent to production
- Cut maintenance by 85%
- Increase test execution speed by 300%
- Auto heal broken tests automatically

Companies like JetBlue, ADP, and Charles Schwab have all seen a major increase in testing efficiency.

What are your initiatives towards improving test automation in the new year?

Best,
Rob"""

        print("GOOD MESSAGE:")
        print(quick_score(good_msg, touch_number=1))
        print("\n" + "="*60 + "\n")
        print("BAD MESSAGE:")
        print(quick_score(bad_msg, touch_number=1))
    else:
        print("Usage:")
        print("  python outbound_qa_engine.py demo          # Score sample messages")
        print("  python outbound_qa_engine.py score-batch [file.json]  # Score a batch")
