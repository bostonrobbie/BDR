"""
Outreach Command Center - Message Component Library
Composable, scoreable message building blocks.

Each component (opener, pain sentence, proof bridge, CTA, signoff) can be
independently scored and swapped. This enables component-level A/B testing
and quality measurement.

Components:
- OpenerComponent: Personalized opening sentence
- PainComponent: Pain hypothesis framed for seniority
- ProofBridgeComponent: Proof point + bridge to prospect's context
- CTAComponent: Call-to-action with soft ask
- SignoffComponent: Closing with name
"""

import re
from dataclasses import dataclass, field, asdict
from typing import Optional


# ─── COMPONENT SCORING ──────────────────────────────────────────

@dataclass
class ComponentScore:
    """Score for a single message component."""
    component_type: str
    score: float  # 0.0 - 1.0
    reasons: list = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


# ─── OPENER COMPONENT ──────────────────────────────────────────

OPENER_QUALITY_SIGNALS = {
    "strong": ["your work", "your team", "your role", "congrats",
               "stood out", "caught my attention", "got me thinking"],
    "weak": ["i hope", "i wanted to", "just reaching out",
             "my name is", "i'm reaching out"],
    "personalized": [r"at [A-Z]", r"your \w+ team", r"as [A-Z]"],
}


def score_opener(opener_text: str, has_evidence: bool = True) -> ComponentScore:
    """Score an opener component on personalization, specificity, and naturalness.

    Returns a 0-1 score:
    - 0.0-0.3: Generic/weak opener
    - 0.4-0.6: Acceptable but improvable
    - 0.7-0.9: Strong, personalized opener
    - 1.0: Exceptional
    """
    score = 0.5
    reasons = []
    text_lower = opener_text.lower()

    # Evidence backing
    if not has_evidence:
        score -= 0.2
        reasons.append("No evidence backing")

    # Strong signals
    for signal in OPENER_QUALITY_SIGNALS["strong"]:
        if signal in text_lower:
            score += 0.15
            reasons.append(f"Strong signal: '{signal}'")
            break

    # Weak signals
    for signal in OPENER_QUALITY_SIGNALS["weak"]:
        if signal in text_lower:
            score -= 0.2
            reasons.append(f"Weak signal: '{signal}'")
            break

    # Personalization patterns
    for pattern in OPENER_QUALITY_SIGNALS["personalized"]:
        if re.search(pattern, opener_text):
            score += 0.1
            reasons.append("Contains personalization")
            break

    # Length check: too short or too long
    word_count = len(opener_text.split())
    if word_count < 4:
        score -= 0.1
        reasons.append("Too short")
    elif word_count > 25:
        score -= 0.1
        reasons.append("Too long for opener")

    return ComponentScore(
        component_type="opener",
        score=max(0.0, min(1.0, round(score, 2))),
        reasons=reasons,
    )


# ─── PAIN COMPONENT ────────────────────────────────────────────

def score_pain_sentence(pain_text: str, has_tool_reference: bool = False,
                         is_question: bool = False) -> ComponentScore:
    """Score a pain sentence on specificity and relevance.

    Args:
        pain_text: The rendered pain sentence.
        has_tool_reference: Whether it mentions a specific tool by name.
        is_question: Whether it's framed as a question (curiosity).
    """
    score = 0.5
    reasons = []
    text_lower = pain_text.lower()

    if has_tool_reference:
        score += 0.15
        reasons.append("References specific tool")

    if is_question:
        score += 0.1
        reasons.append("Question framing (creates dialogue)")

    # Specificity signals
    if any(word in text_lower for word in ["regression", "flaky", "maintenance", "ci/cd", "pipeline"]):
        score += 0.1
        reasons.append("Specific pain area referenced")

    # Company name reference
    if re.search(r"at [A-Z][a-z]+", pain_text):
        score += 0.1
        reasons.append("Company-specific reference")

    # Generic penalty
    if any(phrase in text_lower for phrase in ["test automation", "testing challenges", "software quality"]):
        if not has_tool_reference:
            score -= 0.1
            reasons.append("Generic pain framing")

    return ComponentScore(
        component_type="pain",
        score=max(0.0, min(1.0, round(score, 2))),
        reasons=reasons,
    )


# ─── PROOF BRIDGE COMPONENT ────────────────────────────────────

def score_proof_bridge(proof_text: str, bridge_text: str,
                        has_metric: bool = True) -> ComponentScore:
    """Score the proof point + bridge combination.

    Good proof bridges connect the customer story to the prospect's situation.
    """
    score = 0.5
    reasons = []

    if has_metric:
        score += 0.15
        reasons.append("Contains metric")

    # Check for specific numbers
    if re.search(r'\d+[%xX]|\d+,\d+|\d+ (times|days|weeks|hours|minutes)', proof_text):
        score += 0.1
        reasons.append("Quantified impact")

    # Bridge quality
    if bridge_text:
        score += 0.1
        reasons.append("Has bridge to prospect context")
        if "similar" in bridge_text.lower() or "same" in bridge_text.lower():
            score += 0.05
            reasons.append("Draws parallel to prospect")
    else:
        reasons.append("No bridge (proof point stands alone)")

    # Customer name presence
    if re.search(r'[A-Z][a-z]+(?:buddy|flo|sigma|sard|nofi)', proof_text, re.I):
        score += 0.1
        reasons.append("Named customer reference")

    return ComponentScore(
        component_type="proof_bridge",
        score=max(0.0, min(1.0, round(score, 2))),
        reasons=reasons,
    )


# ─── CTA COMPONENT ─────────────────────────────────────────────

def score_cta(cta_text: str, has_easy_out: bool = False,
              has_time_anchor: bool = False) -> ComponentScore:
    """Score a CTA on clarity, pressure level, and actionability.

    Args:
        cta_text: The CTA text.
        has_easy_out: Whether there's a "no worries" / "no pressure" softener.
        has_time_anchor: Whether it specifies time ("15 minutes").
    """
    score = 0.5
    reasons = []
    text_lower = cta_text.lower()

    # Time anchor
    if has_time_anchor or re.search(r'\d+ minute', text_lower):
        score += 0.15
        reasons.append("Time-anchored (specific commitment)")

    # Easy out
    if has_easy_out or any(phrase in text_lower for phrase in ["no worries", "no pressure", "if not"]):
        score += 0.1
        reasons.append("Has easy out (reduces pressure)")

    # Question vs statement
    if "?" in cta_text:
        score += 0.05
        reasons.append("Question format (invites response)")

    # Connected to proof point
    if any(word in text_lower for word in ["that", "similar", "same"]):
        score += 0.1
        reasons.append("References proof point (connected CTA)")

    # Penalty for pushy language
    if any(word in text_lower for word in ["must", "need to", "should", "urgent", "asap"]):
        score -= 0.2
        reasons.append("Pushy language detected")

    return ComponentScore(
        component_type="cta",
        score=max(0.0, min(1.0, round(score, 2))),
        reasons=reasons,
    )


# ─── FULL MESSAGE SCORING ──────────────────────────────────────

def score_message_components(variant: dict, artifact: dict = None) -> dict:
    """Score all components of a message variant individually.

    Provides a breakdown showing which parts are strong/weak,
    enabling targeted improvement.

    Args:
        variant: A variant dict from generate_message_variants().
        artifact: Optional ResearchArtifact for context.

    Returns:
        {"overall_score": float, "components": [...], "weakest": str,
         "improvement_suggestions": [...]}
    """
    body = variant.get("body", "")
    opener_text = variant.get("opener", "")
    pain_text = variant.get("pain_hook", "")
    cta_text = variant.get("cta", "")
    proof_text = variant.get("proof_point", "")
    has_evidence = bool(variant.get("opener_evidence", ""))

    # Extract tool references from artifact
    tools = []
    if artifact:
        for item in artifact.get("signals", {}).get("tech_stack", []):
            val = item.get("value", "") if isinstance(item, dict) else str(item)
            if val:
                tools.append(val.lower())

    has_tool = any(t in opener_text.lower() or t in pain_text.lower() for t in tools) if tools else False
    is_question = pain_text.strip().endswith("?") if pain_text else False

    # Score each component
    opener_score = score_opener(opener_text, has_evidence)
    pain_score = score_pain_sentence(pain_text, has_tool, is_question)
    proof_score = score_proof_bridge(proof_text, "", bool(proof_text))
    cta_score_ = score_cta(cta_text)

    components = [opener_score, pain_score, proof_score, cta_score_]
    component_dicts = [c.to_dict() for c in components]

    scores = [c.score for c in components]
    overall = round(sum(scores) / max(len(scores), 1), 2)

    # Find weakest
    weakest = min(components, key=lambda c: c.score)

    # Suggestions based on weakest
    suggestions = []
    if weakest.component_type == "opener" and weakest.score < 0.6:
        suggestions.append("Strengthen the opener with more specific personalization")
    if weakest.component_type == "pain" and weakest.score < 0.6:
        suggestions.append("Make the pain hypothesis more specific (mention tools or workflows)")
    if weakest.component_type == "proof_bridge" and weakest.score < 0.6:
        suggestions.append("Add a bridge connecting the proof point to the prospect's context")
    if weakest.component_type == "cta" and weakest.score < 0.6:
        suggestions.append("Add a time anchor to the CTA (e.g., '15 minutes')")

    return {
        "overall_score": overall,
        "components": component_dicts,
        "weakest": weakest.component_type,
        "improvement_suggestions": suggestions,
        "tone": variant.get("tone", ""),
    }
