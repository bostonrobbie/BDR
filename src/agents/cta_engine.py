"""
CTA Engine - Builds closing elements for outreach messages.

Generates CTAs, softeners, sign-offs, and P.S. lines that are tied
to the proof point and prospect context rather than being generic
drop-in blocks.

Usage:
    from src.agents.cta_engine import connected_cta, build_soft_ask, build_signoff

    cta = connected_cta("warm", "friendly", "director", "Acme Corp", "Selenium")
"""


def connected_cta(tier: str, tone: str, seniority: str, company: str,
                  competitor: str) -> str:
    """Build a CTA that references the proof point just mentioned.

    Uses 'that', 'similar results', etc. so the ask flows from the PP
    instead of reading like a separate drop-in block.
    """
    is_strategic = seniority in ("vp", "c-suite", "director", "head")

    if tier == "hot":
        if tone == "friendly":
            if competitor:
                return f"Happy to show you what that'd look like against your {competitor} setup - 15 minutes, tops."
            return f"Happy to show you what that'd look like for {company} - 15 minutes, tops."
        elif tone == "direct":
            if is_strategic:
                return f"Open to exploring how that maps to {company}?"
            if competitor:
                return f"Open to seeing how that compares to your {competitor} setup?"
            return f"Open to seeing how that'd work for {company}?"
        else:
            return f"Curious if you'd see similar results at {company}."

    elif tier == "warm":
        if tone == "friendly":
            if competitor:
                return f"If that resonates, happy to walk through how it'd compare to your {competitor} setup."
            return f"If that resonates, happy to walk through how it'd map to {company}."
        elif tone == "direct":
            if is_strategic:
                return f"Worth exploring how that'd apply to {company}?"
            if competitor:
                return f"Worth seeing how that stacks up against {competitor}?"
            return f"Worth exploring if that fits {company}?"
        else:
            return f"Curious if you're running into something similar at {company}."

    elif tier == "cool":
        if tone == "friendly":
            return f"If any of that's relevant to {company}, happy to share more."
        elif tone == "direct":
            return "Happy to share more if useful."
        else:
            return "Curious if this is even on your radar."

    else:
        return "Figured I'd flag it in case it's helpful down the road."


def build_soft_ask(tier: str, tone: str) -> str:
    """Build the softener/easy-out after the CTA.

    Hot prospects get minimal softeners. Cold prospects get generous easy-outs.
    Direct tone skips softeners entirely.
    """
    if tone == "direct":
        return ""
    if tier == "hot":
        return "" if tone == "friendly" else "Either way, appreciate the read."
    elif tier == "warm":
        return "No worries if the timing's off." if tone == "friendly" else "No pressure either way."
    else:
        return "Either way, no worries at all." if tone == "friendly" else "No pressure at all."


def build_signoff(tone: str, sender: str) -> str:
    """Build the sign-off based on tone."""
    if tone == "friendly":
        return f"Cheers,\n{sender}"
    elif tone == "direct":
        return sender
    return f"Best,\n{sender}"


def build_ps_line(scoring_result: dict, pp_used: dict,
                  pp_other: dict, channel: str) -> str:
    """Build an optional P.S. line for hot/warm prospects on email channel."""
    if channel != "email":
        return ""
    tier = scoring_result.get("tier", "cool")
    if tier not in ("hot", "warm"):
        return ""
    if not pp_other or pp_other.get("key") == pp_used.get("key"):
        return ""
    if tier == "hot":
        return f"P.S. {pp_other.get('text', '')}"
    return f"P.S. {pp_other.get('text', '')} - happy to share the full story if relevant."
