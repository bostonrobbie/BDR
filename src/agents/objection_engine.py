"""
Objection Engine - Predicts and handles prospect objections.

Maps research signals to likely objections and generates preemptive
phrases that can be woven into outreach messages. Integrates with the
memory layer for tool-specific battle card responses.

Usage:
    from src.agents.objection_engine import map_objection, predict_objection_from_artifact

    obj = map_objection(research_context)
    predicted = predict_objection_from_artifact(artifact)
"""

from src.memory.loader import get_memory


OBJECTION_MAP = {
    "existing_tool": {
        "trigger_signals": ["tosca", "katalon", "testim", "mabl", "selenium", "cypress", "playwright"],
        "objection": "We already have a tool",
        "response": "Totally fair. A lot of teams we work with had {tool} too. The gap they kept hitting was maintenance overhead when UI changes frequently. Worth comparing?",
    },
    "large_enterprise": {
        "trigger_signals": ["50000+", "enterprise"],
        "objection": "Security/procurement is complex",
        "response": "We offer on-prem, private cloud, and hybrid. SOC2/ISO certified. A few Fortune 500s run us behind their firewall.",
    },
    "no_qa_team": {
        "trigger_signals": ["no dedicated qa", "no qa team"],
        "objection": "QA isn't a priority",
        "response": "That's actually why teams like yours use us. Plain English means devs write tests without a dedicated QA team.",
    },
    "recently_hired": {
        "trigger_signals": ["recently_hired"],
        "objection": "Too early, still assessing",
        "response": "Makes sense. A lot of QA leaders in their first 90 days use our free trial to benchmark what's possible before committing.",
    },
    "compliance": {
        "trigger_signals": ["pharma", "healthcare", "finance", "banking", "insurance"],
        "objection": "Compliance requirements",
        "response": "We work with Sanofi, Oscar Health, and several banks. Happy to walk through our compliance story.",
    },
    "budget": {
        "trigger_signals": ["startup", "small team", "budget"],
        "objection": "Budget is tight",
        "response": "Totally get it. One company your size (Spendflo) cut manual testing 50% and saw ROI in the first quarter.",
    },
}


def map_objection(research_context: dict) -> dict:
    """Predict the most likely objection and pre-load a response.

    Args:
        research_context: Full research context from researcher.build_research_context()

    Returns: dict with 'objection' and 'response'
    """
    known_tools = research_context.get("known_tools", [])
    vertical = research_context.get("vertical", "").lower()
    recently_hired = research_context.get("recently_hired", False)
    emp_count = research_context.get("account", {}).get("employee_count", 0)
    emp_band = research_context.get("account", {}).get("employee_band", "")

    if recently_hired:
        obj = OBJECTION_MAP["recently_hired"]
        return {"objection": obj["objection"], "response": obj["response"]}

    if known_tools:
        mem = get_memory()
        tool_name = known_tools[0]
        battle_obj = mem.get_objection_response(tool_name)
        if battle_obj:
            return {
                "objection": battle_obj["objection"],
                "response": battle_obj["response"],
                "source": "battle_card",
                "tool": tool_name,
            }
        obj = OBJECTION_MAP["existing_tool"]
        return {
            "objection": obj["objection"],
            "response": obj["response"].format(tool=tool_name.title())
        }

    if emp_count and emp_count >= 50000 or emp_band == "50000+":
        obj = OBJECTION_MAP["large_enterprise"]
        return {"objection": obj["objection"], "response": obj["response"]}

    if any(v in vertical for v in ["pharma", "healthcare", "finance", "banking", "insurance"]):
        obj = OBJECTION_MAP["compliance"]
        return {"objection": obj["objection"], "response": obj["response"]}

    if emp_count and emp_count < 200:
        obj = OBJECTION_MAP["budget"]
        return {"objection": obj["objection"], "response": obj["response"]}

    obj = OBJECTION_MAP["existing_tool"]
    return {
        "objection": obj["objection"],
        "response": obj["response"].format(tool="existing tools")
    }


def predict_objection_from_artifact(artifact: dict) -> dict:
    """Predict the most likely objection based on research artifact signals.

    Uses tech stack, seniority, company size, and industry to predict
    what the prospect will think when they see an outreach message.

    Returns:
        {"objection_key": str, "objection": str, "preemptive_phrases": {...}}
    """
    tech_stack = artifact.get("signals", {}).get("tech_stack", [])
    tools = [t.get("value", "").lower() if isinstance(t, dict) else str(t).lower()
             for t in tech_stack]
    seniority = artifact.get("prospect", {}).get("seniority", "").lower()
    industry = artifact.get("company", {}).get("industry", "").lower()
    size_band = artifact.get("company", {}).get("size_band", "")
    company_name = artifact.get("prospect", {}).get("company_name", "")

    competitor_tools = {"selenium", "cypress", "playwright", "tosca", "katalon", "testim", "mabl"}
    has_competitor = any(t in competitor_tools for t in tools)
    primary_tool = next((t for t in tools if t in competitor_tools), "")

    if has_competitor and primary_tool:
        return {
            "objection_key": "existing_tool",
            "objection": f"We already use {primary_tool.title()}",
            "tool": primary_tool.title(),
            "preemptive_phrases": {
                "friendly": f"I know you've invested in {primary_tool.title()} already, which is actually why I'm reaching out",
                "direct": f"Not suggesting you rip out {primary_tool.title()}",
                "curious": f"Curious if {primary_tool.title()} handles everything you need at {company_name}'s scale",
            },
        }

    if size_band in ("10001-50000", "50000+"):
        return {
            "objection_key": "large_enterprise",
            "objection": "Security/procurement is complex",
            "tool": "",
            "preemptive_phrases": {
                "friendly": "We run on-prem and private cloud for several Fortune 500 teams, so security shouldn't be a blocker",
                "direct": "SOC2 and ISO certified, with on-prem deployment if needed",
                "curious": f"Curious how {company_name} handles vendor evaluation for dev tools",
            },
        }

    if any(v in industry for v in ["pharma", "healthcare", "finance", "banking", "insurance"]):
        ind_short = industry.split("/")[0].strip()
        return {
            "objection_key": "compliance",
            "objection": "Compliance requirements are strict",
            "tool": "",
            "preemptive_phrases": {
                "friendly": f"We already work with teams in regulated {ind_short} environments, so compliance isn't new territory for us",
                "direct": "Built for regulated environments with full audit trails",
                "curious": "Curious how your compliance requirements shape your test automation decisions",
            },
        }

    if seniority in ("individual", "senior") and "qa" not in artifact.get("prospect", {}).get("function", "").lower():
        return {
            "objection_key": "not_decision_maker",
            "objection": "I'm not the right person",
            "tool": "",
            "preemptive_phrases": {
                "friendly": "Even if this isn't your call directly, your perspective on the problem would be really valuable",
                "direct": "Would love your technical take, even if someone else owns the budget",
                "curious": "Not sure if this lands on your plate or someone else's",
            },
        }

    return {
        "objection_key": "budget_timing",
        "objection": "Not the right time/budget",
        "tool": "",
        "preemptive_phrases": {
            "friendly": "No rush on timing",
            "direct": "Even if now isn't the right time, worth having the data point",
            "curious": "Curious if this is even on your radar right now",
        },
    }


def build_objection_aware_bridge(objection: dict, tone: str, pp_text: str) -> str:
    """Build a bridge phrase that preemptively addresses the predicted objection.

    Weaves the objection inoculation naturally into the proof-point-to-CTA
    transition. Returns empty string if no natural integration is possible.
    """
    key = objection.get("objection_key", "")
    tool = objection.get("tool", "")

    if key == "existing_tool" and tool:
        if tone == "friendly":
            return f" (they were on {tool} before, too)"
        elif tone == "direct":
            return f" after switching from {tool}"
        else:
            return f" - they had a similar {tool} setup"

    if key == "compliance":
        if tone == "friendly":
            return " in a similarly regulated environment"
        elif tone == "direct":
            return " with full compliance requirements"
        return ""

    if key == "large_enterprise":
        if tone == "direct":
            return " at enterprise scale"
        return ""

    return ""
