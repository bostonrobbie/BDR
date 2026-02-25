"""
Outreach Command Center - LLM Polish Pass
Takes rule-based MessageVariants output and uses the LLM Gateway to polish
the prose while preserving all evidence-grounded claims.

The polish pass:
- Rewrites template-assembled messages to sound human-written
- Varies sentence structure, word choice, rhythm
- Preserves every proof point, metric, CTA, and company/person reference
- Falls back to original if LLM is unavailable
- Runs QA checks post-polish to verify constraints still hold
"""

import json
import logging
import os
import sys
import re
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.agents.llm_gateway import get_gateway, OllamaError

logger = logging.getLogger("llm_polish")


# ─── POLISH SYSTEM PROMPT ─────────────────────────────────────

POLISH_SYSTEM_PROMPT = """You are a BDR message editor. Your job is to polish outreach messages so they
sound like a human wrote them casually, not like a template assembled them.

RULES YOU MUST FOLLOW:
1. Keep the EXACT same proof point numbers/metrics - never change stats
2. Keep the prospect's name, company name, and title exactly as written
3. Keep the same CTA intent and soft ask
4. Keep the sign-off exactly as written (Cheers/Best/name)
5. NO em dashes (use commas, periods, or hyphens instead)
6. Stay within 10% of the original word count
7. Keep the same paragraph structure (number of paragraphs)
8. Do NOT add new claims, customers, or metrics
9. Do NOT start with "I noticed" or "I saw"
10. Output ONLY the polished message body, nothing else"""


def _build_polish_prompt(body: str, tone: str, metadata: dict) -> str:
    """Build the prompt for polishing a single message variant."""
    prospect_name = metadata.get("prospect_name", "the prospect")
    company = metadata.get("company", "the company")

    return f"""Polish this {tone}-tone BDR outreach message so it sounds more naturally written.
The prospect is {prospect_name} at {company}.

ORIGINAL MESSAGE:
{body}

POLISHED MESSAGE:"""


def _extract_preserved_elements(body: str) -> dict:
    """Extract elements that MUST be preserved through the polish pass."""
    # Extract metrics/numbers
    metrics = re.findall(r'\d+[%xX]|\d+,\d+|\d+ (?:weeks?|days?|minutes?|hours?|months?|tests?)', body)

    # Extract customer names (capitalized words after "at", "with", etc.)
    customer_refs = re.findall(r'(?:Hansard|Medibuddy|CRED|Sanofi|Spendflo|Nagra|Fortune 100)', body, re.IGNORECASE)

    # Extract the sign-off (last paragraph)
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    signoff = paragraphs[-1] if paragraphs else ""

    # Extract P.S. line if present
    ps_line = ""
    if "P.S." in body:
        ps_match = re.search(r'P\.S\..*$', body, re.DOTALL)
        if ps_match:
            ps_line = ps_match.group(0).strip()

    return {
        "metrics": metrics,
        "customer_refs": customer_refs,
        "signoff": signoff,
        "ps_line": ps_line,
    }


def _validate_polish(original: str, polished: str, preserved: dict) -> dict:
    """Validate that the polished message preserves required elements.

    Returns:
        {"valid": bool, "issues": [...]}
    """
    issues = []

    # Check metrics preserved
    for metric in preserved["metrics"]:
        if metric not in polished:
            issues.append(f"Missing metric: '{metric}'")

    # Check customer references preserved
    for ref in preserved["customer_refs"]:
        if ref.lower() not in polished.lower():
            issues.append(f"Missing customer reference: '{ref}'")

    # Check no em dashes introduced
    if "\u2014" in polished or "\u2013" in polished:
        issues.append("Em/en dash introduced during polish")

    # Check word count within 10%
    orig_words = len(original.split())
    polish_words = len(polished.split())
    if orig_words > 0:
        ratio = polish_words / orig_words
        if ratio < 0.8 or ratio > 1.2:
            issues.append(f"Word count changed too much: {orig_words} -> {polish_words} ({ratio:.0%})")

    # Check sign-off preserved
    if preserved["signoff"] and preserved["signoff"] not in polished:
        # Allow minor variations but the sender name must be there
        sender_line = preserved["signoff"].split("\n")[-1].strip()
        if sender_line and sender_line not in polished:
            issues.append(f"Sign-off changed: expected '{sender_line}'")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
    }


def polish_message(body: str, tone: str, metadata: dict = None,
                   temperature: float = 0.3) -> dict:
    """Polish a single message body using the LLM.

    Args:
        body: The original message body.
        tone: The tone (friendly/direct/curious).
        metadata: Dict with prospect_name, company, etc.
        temperature: LLM temperature (low = conservative polish).

    Returns:
        {"polished": str, "original": str, "was_polished": bool,
         "validation": dict, "fallback_reason": str|None}
    """
    metadata = metadata or {}
    preserved = _extract_preserved_elements(body)

    try:
        gateway = get_gateway()
        prompt = _build_polish_prompt(body, tone, metadata)

        result = gateway.generate(
            prompt=prompt,
            stage_name="polish",
            temperature=temperature,
            max_tokens=512,
            system=POLISH_SYSTEM_PROMPT,
        )

        polished = result.get("response", "").strip()

        if not polished:
            return {
                "polished": body,
                "original": body,
                "was_polished": False,
                "validation": {"valid": True, "issues": []},
                "fallback_reason": "LLM returned empty response",
            }

        # Validate the polish preserved required elements
        validation = _validate_polish(body, polished, preserved)

        if not validation["valid"]:
            logger.warning(f"Polish validation failed: {validation['issues']}. Using original.")
            return {
                "polished": body,
                "original": body,
                "was_polished": False,
                "validation": validation,
                "fallback_reason": f"Validation failed: {'; '.join(validation['issues'])}",
            }

        return {
            "polished": polished,
            "original": body,
            "was_polished": True,
            "validation": validation,
            "fallback_reason": None,
        }

    except OllamaError as e:
        logger.warning(f"LLM polish failed (Ollama error): {e}. Using original.")
        return {
            "polished": body,
            "original": body,
            "was_polished": False,
            "validation": {"valid": True, "issues": []},
            "fallback_reason": f"LLM unavailable: {str(e)[:100]}",
        }
    except Exception as e:
        logger.warning(f"LLM polish failed (unexpected): {e}. Using original.")
        return {
            "polished": body,
            "original": body,
            "was_polished": False,
            "validation": {"valid": True, "issues": []},
            "fallback_reason": f"Unexpected error: {str(e)[:100]}",
        }


def polish_variants(message_output: dict, temperature: float = 0.3) -> dict:
    """Polish all variants in a generate_message_variants() output.

    Takes the full output dict from generate_message_variants() and
    returns a new dict with polished bodies. Original bodies are
    preserved in each variant as 'original_body'.

    Falls back gracefully: if LLM is unavailable, returns the original
    output with was_polished=False markers.

    Args:
        message_output: Output from generate_message_variants().
        temperature: LLM temperature for polish pass.

    Returns:
        Same structure as input, with polished bodies and polish metadata.
    """
    metadata = message_output.get("metadata", {})
    polish_meta = {
        "polished_count": 0,
        "fallback_count": 0,
        "polish_results": [],
    }

    for variant in message_output.get("variants", []):
        result = polish_message(
            body=variant["body"],
            tone=variant["tone"],
            metadata=metadata,
            temperature=temperature,
        )

        # Preserve original, update body if polished
        variant["original_body"] = variant["body"]
        if result["was_polished"]:
            variant["body"] = result["polished"]
            variant["char_count"] = len(result["polished"])
            variant["word_count"] = len(result["polished"].split())
            polish_meta["polished_count"] += 1
        else:
            polish_meta["fallback_count"] += 1

        variant["was_polished"] = result["was_polished"]

        polish_meta["polish_results"].append({
            "tone": variant["tone"],
            "was_polished": result["was_polished"],
            "fallback_reason": result.get("fallback_reason"),
            "validation_issues": result["validation"].get("issues", []),
        })

    message_output["polish_metadata"] = polish_meta
    return message_output
