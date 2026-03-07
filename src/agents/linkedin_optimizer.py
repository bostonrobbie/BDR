"""
Outreach Command Center - LinkedIn Preview Optimizer
Optimizes the first ~100 characters of LinkedIn InMails for the preview window.

LinkedIn shows a preview of the first ~100 characters in the notification/inbox.
This determines whether someone clicks "read more" or scrolls past.

The optimizer:
- Scores openers on preview-worthiness (specificity, curiosity, personalization)
- Ensures the most compelling content appears in the first 100 chars
- Strips "Hi Name," greeting from preview calculation (it's always shown)
- Checks that the preview ends cleanly (no mid-word truncation)
"""

import re
import sys
import os
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))


# ─── CONSTANTS ────────────────────────────────────────────────

LINKEDIN_PREVIEW_CHARS = 100  # LinkedIn preview window
LINKEDIN_INMESSAGE_LIMIT = 600  # Connection request
LINKEDIN_INMAIL_LIMIT = 1900  # InMail body (paid)
LINKEDIN_CONNECTION_NOTE_LIMIT = 300  # Connection request note


# ─── PREVIEW SCORING ─────────────────────────────────────────

# Words that signal generic/weak openers
WEAK_OPENER_SIGNALS = [
    "i hope", "hope this", "i wanted to", "just reaching out",
    "my name is", "i'm reaching out", "i came across",
    "i wanted to reach out", "i'm writing to",
]

# Words that signal strong/specific openers
STRONG_OPENER_SIGNALS = [
    "congrats", "your work", "your team", "your role",
    "curious", "question", "quick thought",
]

# Company/role mentions boost score
PERSONALIZATION_PATTERNS = [
    r"at [A-Z][a-z]+",  # "at PayFlow"
    r"your \w+ team",   # "your QA team"
    r"as [A-Z]",        # "as Director"
]


def score_preview(body: str, first_name: str = "") -> dict:
    """Score a message's LinkedIn preview on a 1-10 scale.

    Evaluates the first ~100 characters after the greeting for:
    - Specificity (company/role mentions)
    - Curiosity gap (does it create intrigue?)
    - Clean truncation (doesn't cut mid-word)
    - Avoids weak opener patterns

    Args:
        body: The full message body.
        first_name: Prospect first name (to strip greeting).

    Returns:
        {"score": 1-10, "preview_text": str, "preview_chars": int,
         "issues": [...], "suggestions": [...]}
    """
    # Strip greeting to get the content preview
    content = _strip_greeting(body, first_name)
    preview = content[:LINKEDIN_PREVIEW_CHARS]
    issues = []
    suggestions = []
    score = 5  # baseline

    # ── Truncation check ──
    truncation = _check_truncation(content, LINKEDIN_PREVIEW_CHARS)
    if truncation["mid_word"]:
        issues.append(f"Preview cuts mid-word at '{truncation['cut_word']}'")
        score -= 1
    if truncation["mid_sentence"] and not truncation["mid_word"]:
        # Mid-sentence is OK if it creates curiosity, penalize slightly
        pass

    # ── Weak opener detection ──
    preview_lower = preview.lower()
    for weak in WEAK_OPENER_SIGNALS:
        if weak in preview_lower:
            issues.append(f"Weak opener pattern: '{weak}'")
            score -= 1
            break

    # ── Strong opener detection ──
    for strong in STRONG_OPENER_SIGNALS:
        if strong in preview_lower:
            score += 1
            break

    # ── Personalization ──
    has_personalization = False
    for pattern in PERSONALIZATION_PATTERNS:
        if re.search(pattern, preview):
            has_personalization = True
            score += 1
            break

    if not has_personalization:
        issues.append("Preview lacks company/role specificity")
        suggestions.append("Include company name or role reference in first 100 chars")

    # ── Curiosity / Hook ──
    if "?" in preview:
        score += 1  # Questions create curiosity
    if any(word in preview_lower for word in ["stood out", "got me thinking", "caught"]):
        score += 1  # Curiosity hooks

    # ── Content density ──
    # Empty or very short previews are bad
    if len(preview.strip()) < 40:
        issues.append("Preview too short - not enough to hook the reader")
        score -= 2
    elif len(preview.strip()) < 70:
        suggestions.append("Consider making the opener longer to fill the preview window")

    # ── Numbers/metrics in preview ──
    if re.search(r'\d+[%xX]|\d+,\d+', preview):
        score += 1  # Metrics create credibility
        suggestions.append("Great - metrics in preview add credibility")

    # Clamp score
    score = max(1, min(10, score))

    return {
        "score": score,
        "preview_text": preview.rstrip(),
        "preview_chars": len(preview.rstrip()),
        "full_preview_capacity": LINKEDIN_PREVIEW_CHARS,
        "issues": issues,
        "suggestions": suggestions,
        "rating": _score_label(score),
    }


def _score_label(score: int) -> str:
    """Convert numeric score to label."""
    if score >= 8:
        return "excellent"
    if score >= 6:
        return "good"
    if score >= 4:
        return "fair"
    return "weak"


def _strip_greeting(body: str, first_name: str = "") -> str:
    """Strip the 'Hi Name,' greeting and leading whitespace.

    LinkedIn already shows the recipient's name, so the greeting
    is wasted preview space. We measure from after the greeting.
    """
    lines = body.split("\n")
    content_start = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        # Check if this line is a greeting
        if first_name and stripped.lower().startswith(f"hi {first_name.lower()}"):
            content_start = i + 1
            break
        if stripped.lower().startswith(("hi ", "hey ", "hello ")):
            content_start = i + 1
            break
        break  # First non-empty line isn't a greeting, start from here

    # Skip blank lines after greeting
    while content_start < len(lines) and not lines[content_start].strip():
        content_start += 1

    return "\n".join(lines[content_start:]).strip()


def _check_truncation(text: str, limit: int) -> dict:
    """Check if truncation at `limit` chars cuts cleanly."""
    if len(text) <= limit:
        return {"mid_word": False, "mid_sentence": False, "cut_word": ""}

    # Check mid-word
    char_at = text[limit - 1] if limit > 0 else ""
    char_after = text[limit] if limit < len(text) else ""
    mid_word = char_at.isalpha() and char_after.isalpha()

    # Find the cut word
    cut_word = ""
    if mid_word:
        # Walk back to find word start
        start = limit - 1
        while start > 0 and text[start - 1].isalpha():
            start -= 1
        # Walk forward to find word end
        end = limit
        while end < len(text) and text[end].isalpha():
            end += 1
        cut_word = text[start:end]

    # Check mid-sentence
    preview = text[:limit].rstrip()
    mid_sentence = not preview.endswith((".", "!", "?", ",", ";", ":"))

    return {
        "mid_word": mid_word,
        "mid_sentence": mid_sentence,
        "cut_word": cut_word,
    }


# ─── CHANNEL-AWARE LENGTH CHECKER ────────────────────────────

def check_linkedin_length(body: str, message_type: str = "inmail") -> dict:
    """Check if a message fits LinkedIn's character limits.

    Args:
        body: Message body text.
        message_type: "inmail", "connection_note", or "inmessage".

    Returns:
        {"fits": bool, "char_count": int, "limit": int,
         "over_by": int, "message_type": str}
    """
    limits = {
        "inmail": LINKEDIN_INMAIL_LIMIT,
        "connection_note": LINKEDIN_CONNECTION_NOTE_LIMIT,
        "inmessage": LINKEDIN_INMESSAGE_LIMIT,
    }
    limit = limits.get(message_type, LINKEDIN_INMAIL_LIMIT)
    char_count = len(body)
    over_by = max(0, char_count - limit)

    return {
        "fits": char_count <= limit,
        "char_count": char_count,
        "limit": limit,
        "over_by": over_by,
        "message_type": message_type,
    }


def optimize_for_preview(body: str, first_name: str = "") -> dict:
    """Full optimization pass: score preview, check length, suggest improvements.

    Returns:
        {"preview": {...}, "length": {...}, "optimized": bool}
    """
    preview = score_preview(body, first_name)
    length = check_linkedin_length(body, "inmail")

    return {
        "preview": preview,
        "length": length,
        "optimized": preview["score"] >= 6 and length["fits"],
    }


def rank_variants_by_preview(variants: list, first_name: str = "") -> list:
    """Rank message variants by their LinkedIn preview score.

    Takes a list of variant dicts (from generate_message_variants)
    and returns them sorted by preview score descending.

    Args:
        variants: List of variant dicts with 'body' and 'tone' keys.
        first_name: Prospect first name.

    Returns:
        List of {"tone": str, "preview_score": int, "preview_text": str,
                 "rating": str, "issues": [...]}
        sorted by preview_score descending.
    """
    ranked = []
    for v in variants:
        preview = score_preview(v.get("body", ""), first_name)
        ranked.append({
            "tone": v.get("tone", ""),
            "preview_score": preview["score"],
            "preview_text": preview["preview_text"],
            "preview_chars": preview["preview_chars"],
            "rating": preview["rating"],
            "issues": preview["issues"],
            "suggestions": preview["suggestions"],
        })

    ranked.sort(key=lambda x: x["preview_score"], reverse=True)
    return ranked
