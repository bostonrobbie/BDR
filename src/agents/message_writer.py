"""
Outreach Command Center - Message Writer Agent
Generates all written touches per prospect using Claude LLM via Task subagents.

Core creative engine: produces Touch 1 InMail, Touch 3 Follow-up,
Touch 5 Email, Touch 6 Break-up, and Call Snippets for Touch 2 & 4.

All messages follow Rob's SOP from CLAUDE.md:
- No em dashes, warm conversational tone, specific proof points
- 6-element message structure, mobile-friendly word counts
- Different proof points per touch, different angles per channel
"""

import json
import os
import sys
import re
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.db import models


# ─── PROOF POINT LIBRARY ─────────────────────────────────────

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


# ─── OBJECTION MAPPING ───────────────────────────────────────

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


def select_proof_point(vertical: str, pain_signals: list = None,
                       known_tools: list = None, previously_used: list = None) -> dict:
    """Select the best proof point for a prospect based on context.

    Args:
        vertical: Company vertical (FinTech, FinServ, Healthcare, etc.)
        pain_signals: List of pain indicators from research
        known_tools: List of known competitor tools
        previously_used: List of proof point keys already used for this contact

    Returns: proof point dict from PROOF_POINTS
    """
    previously_used = previously_used or []
    pain_signals = pain_signals or []
    known_tools = known_tools or []
    vertical_lower = vertical.lower()

    # Score each proof point
    scores = {}
    for key, pp in PROOF_POINTS.items():
        if key in previously_used:
            continue  # Skip already-used proof points

        score = 0
        best_for_text = " ".join(pp["best_for"]).lower()

        # Vertical match
        if vertical_lower in best_for_text:
            score += 3

        # Tool match
        if known_tools:
            for tool in known_tools:
                if tool.lower() in best_for_text:
                    score += 2

        # Pain signal match
        for signal in pain_signals:
            if signal.lower() in best_for_text:
                score += 1

        scores[key] = score

    if not scores:
        # All proof points used, reset and pick best
        for key, pp in PROOF_POINTS.items():
            scores[key] = 0

    best_key = max(scores, key=scores.get)
    return {"key": best_key, **PROOF_POINTS[best_key]}


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

    # Check signals in priority order
    if recently_hired:
        obj = OBJECTION_MAP["recently_hired"]
        return {"objection": obj["objection"], "response": obj["response"]}

    if known_tools:
        obj = OBJECTION_MAP["existing_tool"]
        tool_name = known_tools[0].title()
        return {
            "objection": obj["objection"],
            "response": obj["response"].format(tool=tool_name)
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

    # Default: existing tool (most common objection)
    obj = OBJECTION_MAP["existing_tool"]
    return {
        "objection": obj["objection"],
        "response": obj["response"].format(tool="existing tools")
    }


# ─── MESSAGE GENERATION PROMPTS ───────────────────────────────

def build_touch1_prompt(contact: dict, research: dict, proof_point: dict,
                        pain_hook: str, ab_config: dict = None) -> str:
    """Build the LLM prompt for Touch 1 InMail generation.

    Returns a prompt string that Claude processes via Task subagent.
    """
    first_name = contact.get("first_name", "")
    title = contact.get("title", "")
    company = research.get("account", {}).get("name", contact.get("company_name", ""))
    person_notes = research.get("person_research", {})
    company_notes = research.get("company_research", {})

    prompt = f"""Write a LinkedIn InMail for Rob Gorham (BDR at Testsigma) to {first_name} {contact.get('last_name', '')}.

PROSPECT CONTEXT:
- Name: {first_name} {contact.get('last_name', '')}
- Title: {title}
- Company: {company}
- Person research: {json.dumps(person_notes, indent=2) if isinstance(person_notes, dict) else person_notes}
- Company research: {json.dumps(company_notes, indent=2) if isinstance(company_notes, dict) else company_notes}

PROOF POINT TO USE: {proof_point.get('text', '')}
PAIN HOOK: {pain_hook}

STRICT RULES:
1. NO em dashes (use commas or short hyphens only)
2. Must sound like Rob wrote it personally, not AI-generated
3. Warm, conversational, low-pressure, specific, respectful
4. 70-120 words ONLY
5. ONE question maximum
6. Clear spacing between paragraphs
7. Don't start with "I noticed" or "I saw" (vary the opener)

MESSAGE STRUCTURE (all 6 elements required):
1. Subject line - Short, relevant, not clickbaity. Reference their company or role.
2. Personalized opener - Reference something specific from their profile (title detail, years at company, career move, unique responsibility)
3. Company-specific reference - Something concrete about their company (product, metric, market, technology)
4. Problem hypothesis - Tie their responsibilities AND company context to a specific testing pain
5. Testsigma solution - How Testsigma solves THAT problem. Use the proof point with real numbers.
6. Soft ask with easy out - Low-pressure. Include escape hatch like "If not relevant, no worries"

OUTPUT FORMAT (return ONLY this, no extra commentary):
SUBJECT: [subject line]
BODY:
[message body with paragraph breaks]
PERSONALIZATION_SCORE: [1-3, where 3=deep personal reference, 2=company-specific, 1=industry-generic]
OPENER_STYLE: [career_reference|company_metric|title_detail|career_move|team_scope]
ASK_STYLE: [15_min_compare|quick_chat|trade_ideas|happy_to_share|worth_conversation]
"""
    return prompt


def build_touch3_prompt(contact: dict, research: dict, touch1_proof: str,
                        new_proof_point: dict) -> str:
    """Build prompt for Touch 3 InMail Follow-up (40-70 words)."""
    first_name = contact.get("first_name", "")
    company = research.get("account", {}).get("name", contact.get("company_name", ""))

    prompt = f"""Write a LinkedIn InMail FOLLOW-UP for Rob Gorham to {first_name} at {company}.

This is Touch 3 (follow-up to an earlier InMail). Keep it SHORT: 40-70 words.

RULES:
- Reference that you reached out before ("Circling back quick...")
- Use a DIFFERENT proof point than Touch 1 (Touch 1 used: {touch1_proof})
- NEW proof point to use: {new_proof_point.get('text', '')}
- Looser structure (not full 6 elements)
- Softer ask ("Worth a conversation?" or "Happy to share more if helpful")
- NO em dashes
- Warm, not pushy

PROSPECT: {first_name} {contact.get('last_name', '')} - {contact.get('title', '')} at {company}
COMPANY CONTEXT: {json.dumps(research.get('company_research', {}), indent=2) if isinstance(research.get('company_research', {}), dict) else research.get('company_research', '')}

OUTPUT FORMAT:
SUBJECT: [short subject]
BODY:
[message, 40-70 words]
"""
    return prompt


def build_touch5_prompt(contact: dict, research: dict,
                        used_proofs: list, new_proof_point: dict) -> str:
    """Build prompt for Touch 5 Email (70-120 words, slightly more direct)."""
    first_name = contact.get("first_name", "")
    company = research.get("account", {}).get("name", contact.get("company_name", ""))

    prompt = f"""Write a cold EMAIL for Rob Gorham to {first_name} at {company}.

This is Touch 5 (email, after 2 InMails and 2 calls). Can be slightly more direct than InMail.

RULES:
- 70-120 words
- Different angle than previous touches (used proofs: {', '.join(used_proofs)})
- NEW proof point: {new_proof_point.get('text', '')}
- NO em dashes
- Warm but can be more direct since email feels less intrusive
- One CTA, social proof

PROSPECT: {first_name} {contact.get('last_name', '')} - {contact.get('title', '')} at {company}

OUTPUT FORMAT:
SUBJECT: [short subject]
BODY:
[email body, 70-120 words]
"""
    return prompt


def build_touch6_prompt(contact: dict) -> str:
    """Build prompt for Touch 6 Break-up InMail (30-50 words)."""
    first_name = contact.get("first_name", "")
    company = contact.get("company_name", "")

    prompt = f"""Write a BREAK-UP LinkedIn InMail for Rob Gorham to {first_name} at {company}.

This is Touch 6 (final message). NEVER pitch. This is purely a respectful close-out.

RULES:
- 30-50 words ONLY
- Acknowledge the silence without guilt-tripping
- Offer to close the loop: "If the timing isn't right, totally get it. Just wanted to close the loop so I'm not clogging your inbox."
- Leave the door open but make it easy to say no
- NO em dashes
- NO pitch, NO product mention, NO proof points

OUTPUT FORMAT:
SUBJECT: [short subject]
BODY:
[message, 30-50 words]
"""
    return prompt


def build_call_snippet_prompt(contact: dict, research: dict,
                              proof_point: dict, pain_hook: str,
                              touch_number: int) -> str:
    """Build prompt for call snippet (3-line cheat sheet)."""
    first_name = contact.get("first_name", "")
    company = research.get("account", {}).get("name", contact.get("company_name", ""))

    prompt = f"""Write a 3-LINE cold call snippet for Rob Gorham calling {first_name} at {company}.

This is Touch {touch_number} (call). Rob glances at this before dialing.

STRUCTURE (exactly 3 lines):
1. OPENER (1 line): "Hey {first_name}, this is Rob from Testsigma - [personalized hook about their role or company]."
2. PAIN (1 line): "[Specific testing problem tied to their company context]."
3. BRIDGE (1 line): "We helped [proof point]. Worth 60 seconds to see if it's relevant?"

PROOF POINT: {proof_point.get('short', '')}
PAIN HOOK: {pain_hook}
PROSPECT: {contact.get('title', '')} at {company}
CONTEXT: {json.dumps(research.get('company_research', {}), indent=2) if isinstance(research.get('company_research', {}), dict) else research.get('company_research', '')}

RULES:
- Total: 3 lines MAX
- Opener must reference something specific (not generic cold call)
- Pain hypothesis should be DIFFERENT from what was used in InMails
- Use a DIFFERENT proof point than InMails to avoid repetition
- NO em dashes

OUTPUT FORMAT:
OPENER: [one line]
PAIN: [one line]
BRIDGE: [one line]
"""
    return prompt


# ─── MESSAGE PARSING ──────────────────────────────────────────

def parse_touch_response(response_text: str) -> dict:
    """Parse the LLM response for a written touch (InMail/Email).

    Extracts subject line, body, and metadata from the formatted output.
    """
    result = {
        "subject_line": "",
        "body": "",
        "personalization_score": 2,
        "opener_style": "",
        "ask_style": "",
        "word_count": 0,
    }

    lines = response_text.strip().split("\n")

    # Extract subject
    for i, line in enumerate(lines):
        if line.strip().upper().startswith("SUBJECT:"):
            result["subject_line"] = line.split(":", 1)[1].strip()
            break

    # Extract body (between BODY: and next metadata field)
    body_start = None
    body_end = len(lines)
    for i, line in enumerate(lines):
        if line.strip().upper().startswith("BODY:"):
            body_start = i + 1
        elif body_start and line.strip().upper().startswith(("PERSONALIZATION_SCORE:", "OPENER_STYLE:", "ASK_STYLE:")):
            body_end = i
            break

    if body_start:
        body_lines = lines[body_start:body_end]
        result["body"] = "\n".join(body_lines).strip()

    # Extract metadata
    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith("PERSONALIZATION_SCORE:"):
            try:
                score = int(re.search(r'\d', stripped.split(":", 1)[1]).group())
                result["personalization_score"] = min(3, max(1, score))
            except (ValueError, AttributeError):
                pass
        elif stripped.upper().startswith("OPENER_STYLE:"):
            result["opener_style"] = stripped.split(":", 1)[1].strip().lower()
        elif stripped.upper().startswith("ASK_STYLE:"):
            result["ask_style"] = stripped.split(":", 1)[1].strip().lower()

    # Calculate word count
    result["word_count"] = len(result["body"].split())

    return result


def parse_call_snippet_response(response_text: str) -> dict:
    """Parse the LLM response for a call snippet."""
    result = {"opener": "", "pain": "", "bridge": ""}

    for line in response_text.strip().split("\n"):
        stripped = line.strip()
        if stripped.upper().startswith("OPENER:"):
            result["opener"] = stripped.split(":", 1)[1].strip()
        elif stripped.upper().startswith("PAIN:"):
            result["pain"] = stripped.split(":", 1)[1].strip()
        elif stripped.upper().startswith("BRIDGE:"):
            result["bridge"] = stripped.split(":", 1)[1].strip()

    return result


# ─── FULL TOUCH SEQUENCE BUILDER ──────────────────────────────

def build_all_prompts(contact_id: str, ab_group: str = None,
                      ab_variable: str = None) -> dict:
    """Build all message generation prompts for a single prospect.

    Returns dict of prompts keyed by touch type, ready for Claude
    to process via Task subagents.
    """
    from src.agents.researcher import build_research_context

    research = build_research_context(contact_id)
    if research.get("error"):
        return {"error": research["error"]}

    contact = research["contact"]
    vertical = research.get("vertical", "Tech")
    known_tools = research.get("known_tools", [])

    # Select proof points (different per touch)
    used_proofs = []

    pp1 = select_proof_point(vertical, known_tools=known_tools, previously_used=used_proofs)
    used_proofs.append(pp1["key"])

    pp3 = select_proof_point(vertical, known_tools=known_tools, previously_used=used_proofs)
    used_proofs.append(pp3["key"])

    pp5 = select_proof_point(vertical, known_tools=known_tools, previously_used=used_proofs)
    used_proofs.append(pp5["key"])

    # Call snippets use different proof points than InMails
    pp_call2 = select_proof_point(vertical, known_tools=known_tools, previously_used=[pp1["key"]])
    pp_call4 = select_proof_point(vertical, known_tools=known_tools, previously_used=[pp3["key"], pp_call2["key"]])

    # Pain hook (may be influenced by A/B test)
    pain_hook = _determine_pain_hook(research, ab_group, ab_variable)

    # Map objection
    objection = map_objection(research)

    prompts = {
        "touch_1_inmail": {
            "prompt": build_touch1_prompt(contact, research, pp1, pain_hook),
            "proof_point": pp1,
            "pain_hook": pain_hook,
        },
        "touch_2_call": {
            "prompt": build_call_snippet_prompt(contact, research, pp_call2, pain_hook, 2),
            "proof_point": pp_call2,
        },
        "touch_3_followup": {
            "prompt": build_touch3_prompt(contact, research, pp1["short"], pp3),
            "proof_point": pp3,
        },
        "touch_4_call": {
            "prompt": build_call_snippet_prompt(contact, research, pp_call4, pain_hook, 4),
            "proof_point": pp_call4,
        },
        "touch_6_breakup": {
            "prompt": build_touch6_prompt(contact),
        },
        "objection": objection,
        "research_context": research,
    }

    # Touch 5 only if email available
    if contact.get("email"):
        prompts["touch_5_email"] = {
            "prompt": build_touch5_prompt(
                contact, research,
                [pp1["short"], pp3["short"]], pp5
            ),
            "proof_point": pp5,
        }

    return prompts


def _determine_pain_hook(research: dict, ab_group: str = None,
                         ab_variable: str = None) -> str:
    """Determine the pain hook based on research and A/B test config."""
    vertical = research.get("vertical", "").lower()
    known_tools = research.get("known_tools", [])

    # A/B test override
    if ab_variable == "pain_hook":
        if ab_group == "A":
            return "maintenance/flaky tests"
        elif ab_group == "B":
            return "release velocity/speed"

    # Auto-detect from signals
    if known_tools:
        return f"maintenance overhead with {known_tools[0]}"

    if "fintech" in vertical or "finserv" in vertical:
        return "regression testing across payment/financial workflows"
    elif "healthcare" in vertical or "pharma" in vertical:
        return "compliance-heavy regression cycles"
    elif "e-commerce" in vertical:
        return "catalog/checkout regression when UI changes"
    elif "insurance" in vertical:
        return "policy workflow regression testing"
    else:
        return "test maintenance and flaky tests"


# ─── STORE GENERATED MESSAGES ─────────────────────────────────

def store_generated_messages(contact_id: str, generated: dict,
                             batch_id: str = None, ab_group: str = None,
                             ab_variable: str = None) -> list:
    """Store generated messages in the database.

    generated: dict with keys like 'touch_1_inmail', 'touch_3_followup', etc.
    Each value has 'parsed' (from parse_touch_response) and metadata.
    """
    stored = []

    touch_configs = [
        ("touch_1_inmail", "linkedin", 1, "inmail"),
        ("touch_2_call", "phone", 2, "call_snippet"),
        ("touch_3_followup", "linkedin", 3, "inmail_followup"),
        ("touch_4_call", "phone", 4, "call_snippet"),
        ("touch_5_email", "email", 5, "email"),
        ("touch_6_breakup", "linkedin", 6, "inmail_breakup"),
    ]

    for key, channel, touch_num, touch_type in touch_configs:
        if key not in generated:
            continue

        data = generated[key]
        parsed = data.get("parsed", {})

        if touch_type == "call_snippet":
            # Call snippets stored as body with structured format
            body = f"OPENER: {parsed.get('opener', '')}\nPAIN: {parsed.get('pain', '')}\nBRIDGE: {parsed.get('bridge', '')}"
            msg_data = {
                "contact_id": contact_id,
                "batch_id": batch_id,
                "channel": channel,
                "touch_number": touch_num,
                "touch_type": touch_type,
                "body": body,
                "word_count": len(body.split()),
                "proof_point_used": data.get("proof_point", {}).get("short", ""),
                "ab_group": ab_group,
                "ab_variable": ab_variable,
                "approval_status": "draft",
            }
        else:
            msg_data = {
                "contact_id": contact_id,
                "batch_id": batch_id,
                "channel": channel,
                "touch_number": touch_num,
                "touch_type": touch_type,
                "subject_line": parsed.get("subject_line", ""),
                "body": parsed.get("body", ""),
                "word_count": parsed.get("word_count", 0),
                "personalization_score": parsed.get("personalization_score"),
                "proof_point_used": data.get("proof_point", {}).get("short", ""),
                "pain_hook": data.get("pain_hook", ""),
                "opener_style": parsed.get("opener_style", ""),
                "ask_style": parsed.get("ask_style", ""),
                "ab_group": ab_group,
                "ab_variable": ab_variable,
                "approval_status": "draft",
            }

        result = models.create_message_draft(msg_data)
        stored.append(result)

    # Store objection mapping on the contact
    if "objection" in generated:
        obj = generated["objection"]
        models.update_contact(contact_id, {
            "predicted_objection": obj.get("objection", ""),
            "objection_response": obj.get("response", ""),
        })

    return stored
