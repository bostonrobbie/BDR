"""
Tone Engine - Renders raw evidence into natural prose by tone.

Converts raw personalization hooks, pain hypotheses, and value props
into tone-appropriate message text. Adapts framing by seniority level
and prospect context.

Usage:
    from src.agents.tone_engine import render_opener, render_pain_sentence

    opener = render_opener(raw_hook, artifact, "friendly")
    pain = render_pain_sentence(raw_pain, artifact, "direct")
"""


def function_label(title: str) -> str:
    """Turn a title into a short function label for natural prose."""
    t = title.lower()
    if any(kw in t for kw in ["qa", "quality", "test"]):
        return "QA"
    if any(kw in t for kw in ["engineering", "software"]):
        return "engineering"
    if "devops" in t or "platform" in t:
        return "platform engineering"
    if " of " in title:
        return title.split(" of ", 1)[-1].strip()
    return title


def render_opener(raw_hook: str, artifact: dict, tone: str) -> str:
    """Turn a raw personalization hook into a natural opener sentence.

    Prevents evidence labels from leaking into the message body.
    Varies phrasing by tone.
    """
    prospect = artifact.get("prospect", {})
    company = prospect.get("company_name", "your company")
    title = prospect.get("title", "")

    raw_lower = raw_hook.lower()

    if "linkedin headline" in raw_lower:
        func = function_label(title)
        func_lower = func if func == "QA" else func.lower()
        if tone == "friendly":
            return f"Your work leading {func} at {company} stood out"
        elif tone == "direct":
            return f"Given your background in {func_lower} at {company}"
        else:
            return f"Your experience leading {func_lower} at {company} got me thinking"

    if "recently started" in raw_lower or "recently hired" in raw_lower:
        if tone == "friendly":
            return f"Congrats on the new role at {company}"
        elif tone == "direct":
            return f"Starting a new {title} role is the perfect time to evaluate tools"
        else:
            return f"Curious what's top of mind as you settle into the {title} role at {company}"

    if raw_lower.startswith("about:"):
        snippet = raw_hook.split(":", 1)[1].strip()[:60].rstrip(".")
        if tone == "friendly":
            return f"Your focus on {snippet.lower()} resonated"
        elif tone == "direct":
            return f"Based on your background in {snippet.lower()}"
        else:
            return f"Your experience with {snippet.lower()} got me thinking"

    if raw_lower.startswith("role as"):
        func = function_label(title)
        if tone == "friendly":
            return f"Your work leading {func} at {company} stood out"
        elif tone == "direct":
            return f"Given your role as {title} at {company}"
        else:
            return f"Running {func} at a company like {company} is no small feat"

    if raw_lower.startswith("work at"):
        if tone == "friendly":
            return f"What {company} is building caught my attention"
        elif tone == "direct":
            return f"Reaching out because of {company}'s engineering team"
        else:
            return f"Curious about how {company} handles test automation at scale"

    func = function_label(title)
    if tone == "friendly":
        return f"Your work leading {func} at {company} stood out"
    elif tone == "direct":
        return f"Given your role as {title} at {company}"
    return f"Your work at {company} caught my attention"


def render_pain_sentence(raw_pain: str, artifact: dict, tone: str) -> str:
    """Turn a raw pain hypothesis into a natural sentence.

    Adapts framing by seniority: VPs/Directors get strategic angles,
    Managers/ICs get tactical angles. Uses actual tool names from signals.
    """
    prospect = artifact.get("prospect", {})
    company = prospect.get("company_name", "your company")
    seniority = prospect.get("seniority", "").lower()
    industry = artifact.get("company", {}).get("industry", "tech")

    tools = []
    for item in artifact.get("signals", {}).get("tech_stack", []):
        val = item.get("value", "") if isinstance(item, dict) else str(item)
        if val:
            tools.append(val)

    is_strategic = seniority in ("vp", "c-suite", "director", "head")
    pain_lower = raw_pain.lower()

    if "maintenance" in pain_lower and tools:
        tool_list = " and ".join(tools[:2])
        if is_strategic:
            if tone == "friendly":
                return f"Keeping {tool_list} suites stable while shipping fast is a grind most {industry} teams know well"
            elif tone == "direct":
                return f"at {company}'s scale, {tool_list} maintenance is probably eating into your team's velocity"
            else:
                return f"how much engineering time goes into keeping {tool_list} tests from breaking"
        else:
            if tone == "friendly":
                return f"Wrangling {tool_list} test maintenance while keeping release cycles tight is a constant balancing act"
            elif tone == "direct":
                return f"{tool_list} maintenance overhead tends to grow faster than teams can keep up with"
            else:
                return f"are flaky {tool_list} tests still the biggest time sink for your team"

    if "compliance" in pain_lower or "regulated" in pain_lower:
        if is_strategic:
            if tone == "curious":
                return f"how do you keep regression cycles short when compliance requires full coverage before every release"
            return f"Regression cycles in a regulated {industry} environment can be a real bottleneck for release velocity"
        else:
            if tone == "curious":
                return f"how much of your sprint gets eaten by compliance-driven regression"
            return f"Running full regression before every release in a compliance-heavy environment takes serious bandwidth"

    if "scaling" in pain_lower:
        if is_strategic:
            return f"Scaling test coverage without scaling headcount is one of the harder problems in {industry} engineering"
        else:
            return f"Growing automation coverage while your team's already stretched thin is a tough balance"

    if "maintenance" in pain_lower:
        if is_strategic:
            return f"At {company}'s scale, test maintenance tends to become a real drag on release velocity"
        else:
            return f"Keeping test suites reliable as {company} ships faster is a constant challenge"

    if is_strategic:
        return f"Test automation at {company}'s scale tends to become a strategic bottleneck"
    return f"Keeping test suites reliable as {company} ships faster is a constant challenge"


def pick_personalization_opener(artifact: dict) -> tuple:
    """Pick the best personalization hook and return (raw_hook_text, evidence_field).

    Only uses hooks that have evidence.
    """
    hooks = artifact.get("personalization", {}).get("hooks", [])
    prioritized = sorted(hooks, key=lambda h: (
        0 if "person_research" in h.get("evidence_field", "") else
        1 if "company" in h.get("evidence_field", "") else
        2
    ))
    for hook in prioritized:
        ev = hook.get("evidence_field", "")
        if ev and ev != "unknown - hypothesis only":
            return hook.get("hook", ""), ev
    prospect = artifact.get("prospect", {})
    return f"Role as {prospect.get('title', 'your role')} at {prospect.get('company_name', 'your company')}", "from CRM field: title"


def pick_pain_hook(artifact: dict) -> str:
    """Pick the best pain hypothesis for the hook (raw text)."""
    pains = artifact.get("pains", {}).get("hypothesized_pains", [])
    sorted_pains = sorted(pains, key=lambda p: p.get("confidence", 0), reverse=True)
    if sorted_pains:
        return sorted_pains[0].get("pain", "test maintenance and release velocity")
    return "test maintenance and release velocity"


def short_pain_label(raw_pain: str) -> str:
    """Create a short label from a pain hypothesis for subject lines."""
    p = raw_pain.lower()
    if "maintenance" in p:
        return "test maintenance"
    if "compliance" in p or "regulated" in p:
        return "regression cycles"
    if "scaling" in p:
        return "scaling automation"
    if "flaky" in p:
        return "flaky tests"
    words = raw_pain.split()[:3]
    return " ".join(words).lower().rstrip(",")


def pick_value_prop(product_config: dict, artifact: dict, tone: str) -> str:
    """Pick a value prop that fits the prospect's context."""
    vps = product_config.get("value_props", [])
    if not vps:
        return ""
    tools = []
    for item in artifact.get("signals", {}).get("tech_stack", []):
        val = item.get("value", "") if isinstance(item, dict) else str(item)
        if val:
            tools.append(val.lower())

    seniority = artifact.get("prospect", {}).get("seniority", "").lower()
    func = artifact.get("prospect", {}).get("function", "").lower()

    if seniority in ("vp", "c-suite"):
        for vp in vps:
            if "maintenance" in vp.lower() or "reduction" in vp.lower():
                return vp
        return vps[0]

    if any(t in ("selenium", "cypress", "playwright") for t in tools):
        for vp in vps:
            if "maintenance" in vp.lower() or "selenium" in vp.lower() or "cypress" in vp.lower():
                return vp

    if "qa" in func:
        for vp in vps:
            if "collaborate" in vp.lower() or "no-code" in vp.lower():
                return vp

    if tone == "friendly":
        return vps[0]
    elif tone == "direct":
        return vps[1] if len(vps) > 1 else vps[0]
    return vps[2] if len(vps) > 2 else vps[0]


def get_tools_and_competitor(artifact: dict) -> tuple:
    """Extract tool list and primary competitor name from artifact signals."""
    tools = []
    for item in artifact.get("signals", {}).get("tech_stack", []):
        val = item.get("value", "") if isinstance(item, dict) else str(item)
        if val:
            tools.append(val)
    competitor = next((t for t in tools if t.lower() in
                       ("selenium", "cypress", "playwright", "katalon", "testcomplete")), "")
    return tools, competitor
