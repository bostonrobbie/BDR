"""
Proof Point Selection Engine - Matches customer stories to prospect context.

Proof points are verified customer outcomes used in outreach messages.
Each proof point is matched to verticals, pain signals, and competitor tools,
with rotation logic to avoid repetition across touches.

Usage:
    from src.agents.proof_points import select_proof_point, PROOF_POINTS

    pp = select_proof_point("FinTech", known_tools=["selenium"])
"""

PROOF_POINTS = {
    "hansard_regression": {
        "text": "Hansard cut regression from 8 weeks to 5 weeks with AI auto-heal",
        "short": "regression 8 weeks to 5 weeks",
        "best_for": ["insurance", "financial services", "finserv", "long regression cycles"],
        "metric": "8 weeks to 5 weeks",
    },
    "medibuddy_scale": {
        "text": "Medibuddy automated 2,500 tests and cut maintenance 50%",
        "short": "2,500 tests automated, 50% maintenance cut",
        "best_for": ["healthcare", "digital health", "mid-size teams", "scaling"],
        "metric": "2,500 tests, 50% maintenance cut",
    },
    "cred_coverage": {
        "text": "CRED hit 90% regression automation and 5x faster execution",
        "short": "90% regression coverage, 5x faster",
        "best_for": ["fintech", "high-velocity", "fast release cycles"],
        "metric": "90% coverage, 5x faster",
    },
    "sanofi_speed": {
        "text": "Sanofi went from 3-day regression to 80 minutes",
        "short": "3 days to 80 minutes",
        "best_for": ["pharma", "healthcare", "compliance-heavy", "large regression"],
        "metric": "3 days to 80 minutes",
    },
    "fortune100_productivity": {
        "text": "A Fortune 100 company saw 3X productivity increase",
        "short": "3X productivity increase",
        "best_for": ["enterprise", "vp-level", "big tech"],
        "metric": "3X productivity",
    },
    "nagra_api": {
        "text": "Nagra DTV built 2,500 tests in 8 months, 4X faster",
        "short": "2,500 tests in 8 months, 4X faster",
        "best_for": ["media", "streaming", "api testing", "telecom"],
        "metric": "2,500 tests, 4X faster",
    },
    "spendflo_roi": {
        "text": "Spendflo cut 50% of manual testing with ROI in first quarter",
        "short": "50% manual testing cut, ROI in Q1",
        "best_for": ["saas", "small teams", "startup", "budget-conscious"],
        "metric": "50% manual testing cut",
    },
    "selenium_maintenance": {
        "text": "70% maintenance reduction vs Selenium",
        "short": "70% less maintenance than Selenium",
        "best_for": ["selenium users", "cypress users", "playwright users"],
        "metric": "70% maintenance reduction",
    },
    "self_healing": {
        "text": "90% maintenance reduction with AI self-healing",
        "short": "90% maintenance reduction",
        "best_for": ["flaky tests", "brittle tests", "frequent ui changes"],
        "metric": "90% maintenance reduction",
    },
}


def select_proof_point(vertical: str, pain_signals: list = None,
                       known_tools: list = None, previously_used: list = None) -> dict:
    """Select the best proof point for a prospect based on context.

    Args:
        vertical: Company vertical (FinTech, FinServ, Healthcare, etc.)
        pain_signals: List of pain indicators from research
        known_tools: List of known competitor tools
        previously_used: List of proof point keys already used for this contact

    Returns: proof point dict with 'key' plus standard fields
    """
    previously_used = previously_used or []
    pain_signals = pain_signals or []
    known_tools = known_tools or []
    vertical_lower = vertical.lower()

    scores = {}
    for key, pp in PROOF_POINTS.items():
        if key in previously_used:
            continue

        score = 0
        best_for_text = " ".join(pp["best_for"]).lower()

        if vertical_lower in best_for_text:
            score += 3
        if known_tools:
            for tool in known_tools:
                if tool.lower() in best_for_text:
                    score += 2
        for signal in pain_signals:
            if signal.lower() in best_for_text:
                score += 1

        scores[key] = score

    if not scores:
        for key, pp in PROOF_POINTS.items():
            scores[key] = 0

    best_key = max(scores, key=scores.get)
    return {"key": best_key, **PROOF_POINTS[best_key]}


def select_best_proof_point(artifact: dict, product_config: dict,
                            exclude_keys: list = None) -> dict:
    """Select best proof point from product config given the artifact."""
    exclude_keys = exclude_keys or []
    proof_points = product_config.get("proof_points", PROOF_POINTS)
    industry = artifact.get("company", {}).get("industry", "").lower()
    tech = artifact.get("signals", {}).get("tech_stack", [])
    tool_names = [t.get("value", "").lower() if isinstance(t, dict) else str(t).lower()
                  for t in tech]

    best_key = None
    best_score = -1

    for key, pp in proof_points.items():
        if key in exclude_keys:
            continue
        score = 0
        best_for = " ".join(pp.get("best_for", [])).lower()
        if industry and industry in best_for:
            score += 3
        for tool in tool_names:
            if tool in best_for:
                score += 2
        if score > best_score:
            best_score = score
            best_key = key

    if not best_key:
        for key in proof_points:
            if key not in exclude_keys:
                best_key = key
                break
    if not best_key:
        best_key = list(proof_points.keys())[0] if proof_points else None

    if best_key and best_key in proof_points:
        return {"key": best_key, **proof_points[best_key]}
    return {"key": "unknown", "text": "", "short": "", "best_for": [], "metric": ""}


def select_best_proof_point_with_feedback(artifact: dict, product_config: dict,
                                          exclude_keys: list = None) -> dict:
    """Select best proof point, biased by feedback data when available.

    Checks the feedback tracker for winning proof points. If there's
    enough data and a clear winner, biases toward it. Otherwise falls
    back to the standard selection logic.
    """
    exclude_keys = exclude_keys or []

    try:
        from src.agents.feedback_tracker import get_proof_point_preference
        preferred = get_proof_point_preference(min_sample=5, days=90)

        if preferred and preferred not in exclude_keys:
            proof_points = product_config.get("proof_points", PROOF_POINTS)
            if preferred in proof_points:
                return {"key": preferred, **proof_points[preferred]}
    except Exception:
        pass

    return select_best_proof_point(artifact, product_config, exclude_keys)


def bridge_phrase(pp_text: str, artifact: dict, tools: list) -> str:
    """Short phrase connecting the proof point to the prospect's situation."""
    competitor = next((t for t in tools if t.lower() in
                       ("selenium", "cypress", "playwright", "katalon", "testcomplete")), "")
    industry = artifact.get("company", {}).get("industry", "")

    if competitor and competitor.lower() not in pp_text.lower():
        return " after a similar switch"
    if not competitor and industry:
        ind_short = industry.split("/")[0].split(",")[0].strip().lower()
        return f" in a similar {ind_short} environment"
    return ""
