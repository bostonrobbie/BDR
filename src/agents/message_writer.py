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
from datetime import datetime

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


# ─── LINKEDIN SEQUENCE MANAGEMENT ─────────────────────────────

def get_linkedin_sequence_status(contact_id: str) -> dict:
    """Check which LinkedIn touches have been sent via touchpoints table.

    Returns dict with:
    - touches_sent: list of touch numbers sent
    - pending_touches: list of touch numbers due but not sent
    - next_touch: dict with details of next expected touch
    """
    conn = models.get_db()

    # Get sent touchpoints
    sent = conn.execute("""
        SELECT DISTINCT touch_number FROM touchpoints
        WHERE contact_id=? AND channel='linkedin'
        ORDER BY touch_number ASC
    """, (contact_id,)).fetchall()
    touches_sent = [row[0] for row in sent]

    # Get pending followups (scheduled but not yet sent)
    pending = conn.execute("""
        SELECT touch_number, due_date FROM followups
        WHERE contact_id=? AND channel='linkedin' AND state='pending'
        ORDER BY touch_number ASC
    """, (contact_id,)).fetchall()
    pending_touches = [dict(row) for row in pending]

    # Determine next touch based on SOP
    # Touch sequence: 1 (InMail), 3 (InMail Follow-up), 6 (Break-up)
    linkedin_sequence = [1, 3, 6]
    next_touch = None
    for touch_num in linkedin_sequence:
        if touch_num not in touches_sent:
            # Check if there's a pending followup for this touch
            pending_fu = next((fu for fu in pending_touches if fu["touch_number"] == touch_num), None)
            next_touch = {
                "touch_number": touch_num,
                "due_date": pending_fu.get("due_date") if pending_fu else None,
                "touch_type": "inmail" if touch_num in (1, 3) else "breakup",
            }
            break

    conn.close()

    return {
        "contact_id": contact_id,
        "touches_sent": touches_sent,
        "pending_touches": pending_touches,
        "next_touch": next_touch,
    }


def get_next_linkedin_touch(contact_id: str) -> Optional[dict]:
    """Determine what the next LinkedIn touch should be based on SOP timing.

    Returns dict with:
    - touch_number: next touch number (1, 3, or 6)
    - should_send_now: bool (true if due_date <= now)
    - due_date: ISO string of when this touch should go out
    - days_until_due: integer (negative if overdue)
    - touch_type: 'inmail' or 'breakup'
    """
    status = get_linkedin_sequence_status(contact_id)
    next_touch = status.get("next_touch")

    if not next_touch:
        return None

    due_date_str = next_touch.get("due_date")
    if not due_date_str:
        return {
            "touch_number": next_touch["touch_number"],
            "should_send_now": True,
            "due_date": None,
            "days_until_due": 0,
            "touch_type": next_touch.get("touch_type", "inmail"),
            "status": "no_followup_scheduled",
        }

    try:
        due_date = datetime.fromisoformat(due_date_str)
        now = datetime.utcnow()
        days_until = (due_date - now).days
        should_send = due_date <= now

        return {
            "touch_number": next_touch["touch_number"],
            "should_send_now": should_send,
            "due_date": due_date_str,
            "days_until_due": days_until,
            "touch_type": next_touch.get("touch_type", "inmail"),
            "status": "overdue" if days_until < 0 else "pending" if days_until > 0 else "due_today",
        }
    except (ValueError, TypeError):
        return {
            "touch_number": next_touch["touch_number"],
            "should_send_now": True,
            "due_date": due_date_str,
            "days_until_due": 0,
            "touch_type": next_touch.get("touch_type", "inmail"),
            "status": "invalid_date",
        }


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


# ═══════════════════════════════════════════════════════════════
# GROUNDED MULTI-VARIANT MESSAGE GENERATION (v2)
# Consumes ResearchArtifact + ScoringResult + ProductConfig
# Produces 3 variants (friendly/direct/curious) with QA checks
# ═══════════════════════════════════════════════════════════════

_PRODUCT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../../config/product_config.json")
_product_config_cache = None


def _load_product_config(path: str = None) -> dict:
    """Load product config (value props, proof points, CTAs)."""
    global _product_config_cache
    if _product_config_cache is not None and path is None:
        return _product_config_cache
    p = path or _PRODUCT_CONFIG_PATH
    try:
        with open(p, "r") as f:
            _product_config_cache = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        _product_config_cache = {
            "company": "Testsigma", "sender": "Rob Gorham",
            "value_props": ["AI-powered test automation"],
            "proof_points": PROOF_POINTS,
            "cta_options": ["Worth a quick chat?", "Happy to share more if helpful."],
            "forbidden_phrases": ["saw your post", "noticed you", "came across your",
                                  "I was browsing", "I looked you up"],
            "max_chars": {"linkedin": 600, "email": 1200, "subject_line": 80},
            "tone_descriptions": {
                "friendly": "Warm, conversational.",
                "direct": "Concise, to the point.",
                "curious": "Question-led, exploratory.",
            },
        }
    return _product_config_cache


def _select_best_proof_point(artifact: dict, product_config: dict,
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
        # fallback to first non-excluded
        for key in proof_points:
            if key not in exclude_keys:
                best_key = key
                break
    if not best_key:
        best_key = list(proof_points.keys())[0] if proof_points else None

    if best_key and best_key in proof_points:
        return {"key": best_key, **proof_points[best_key]}
    return {"key": "unknown", "text": "", "short": "", "best_for": [], "metric": ""}


def _pick_personalization_opener(artifact: dict) -> tuple:
    """Pick the best personalization hook and return (raw_hook_text, evidence_field).

    Only uses hooks that have evidence. Returns raw data; use _render_opener()
    to turn this into natural prose for the message body.
    """
    hooks = artifact.get("personalization", {}).get("hooks", [])
    # Prefer hooks with non-CRM evidence first (person_research > company > CRM)
    prioritized = sorted(hooks, key=lambda h: (
        0 if "person_research" in h.get("evidence_field", "") else
        1 if "company" in h.get("evidence_field", "") else
        2
    ))
    for hook in prioritized:
        ev = hook.get("evidence_field", "")
        if ev and ev != "unknown - hypothesis only":
            return hook.get("hook", ""), ev
    # Fallback: use title+company
    prospect = artifact.get("prospect", {})
    return f"Role as {prospect.get('title', 'your role')} at {prospect.get('company_name', 'your company')}", "from CRM field: title"


# ─── NATURAL LANGUAGE RENDERERS ────────────────────────────────
# These turn raw evidence-tagged data into human-sounding prose.
# Each renderer varies output by tone so the 3 variants read differently.

def _render_opener(raw_hook: str, artifact: dict, tone: str) -> str:
    """Turn a raw personalization hook into a natural opener sentence.

    Prevents evidence labels (\"LinkedIn headline: ...\") from leaking
    into the message body. Varies phrasing by tone.
    """
    prospect = artifact.get("prospect", {})
    company = prospect.get("company_name", "your company")
    title = prospect.get("title", "")

    raw_lower = raw_hook.lower()

    # ── LinkedIn headline hook ──
    if "linkedin headline" in raw_lower:
        headline = raw_hook.split(":", 1)[1].strip() if ":" in raw_hook else raw_hook
        # Take just the first part before any pipe separator, keep original casing
        headline_short = headline.split("|")[0].strip()
        func = _function_label(title)
        # Keep "QA" uppercase, lowercase everything else
        func_lower = func if func == "QA" else func.lower()
        if tone == "friendly":
            return f"Your work leading {func} at {company} stood out"
        elif tone == "direct":
            return f"Given your background in {func_lower} at {company}"
        else:
            return f"Your experience leading {func_lower} at {company} got me thinking"

    # ── Recently hired hook ──
    if "recently started" in raw_lower or "recently hired" in raw_lower:
        if tone == "friendly":
            return f"Congrats on the new role at {company}"
        elif tone == "direct":
            return f"Starting a new {title} role is the perfect time to evaluate tools"
        else:
            return f"Curious what's top of mind as you settle into the {title} role at {company}"

    # ── About / bio hook ──
    if raw_lower.startswith("about:"):
        snippet = raw_hook.split(":", 1)[1].strip()[:60].rstrip(".")
        if tone == "friendly":
            return f"Your focus on {snippet.lower()} resonated"
        elif tone == "direct":
            return f"Based on your background in {snippet.lower()}"
        else:
            return f"Your experience with {snippet.lower()} got me thinking"

    # ── Role-based hook ──
    if raw_lower.startswith("role as"):
        func = _function_label(title)
        if tone == "friendly":
            return f"Your work leading {func} at {company} stood out"
        elif tone == "direct":
            return f"Given your role as {title} at {company}"
        else:
            return f"Running {func} at a company like {company} is no small feat"

    # ── Company-based hook ──
    if raw_lower.startswith("work at"):
        if tone == "friendly":
            return f"What {company} is building caught my attention"
        elif tone == "direct":
            return f"Reaching out because of {company}'s engineering team"
        else:
            return f"Curious about how {company} handles test automation at scale"

    # ── Generic fallback ──
    func = _function_label(title)
    if tone == "friendly":
        return f"Your work leading {func} at {company} stood out"
    elif tone == "direct":
        return f"Given your role as {title} at {company}"
    return f"Your work at {company} caught my attention"


def _function_label(title: str) -> str:
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


def _render_pain_sentence(raw_pain: str, artifact: dict, tone: str) -> str:
    """Turn a raw pain hypothesis into a natural sentence.

    Adapts framing by seniority: VPs/Directors get strategic angles,
    Managers/ICs get tactical angles. Uses actual tool names from signals.
    """
    prospect = artifact.get("prospect", {})
    company = prospect.get("company_name", "your company")
    seniority = prospect.get("seniority", "").lower()
    industry = artifact.get("company", {}).get("industry", "tech")

    # Extract tool names
    tools = []
    for item in artifact.get("signals", {}).get("tech_stack", []):
        val = item.get("value", "") if isinstance(item, dict) else str(item)
        if val:
            tools.append(val)

    is_strategic = seniority in ("vp", "c-suite", "director", "head")
    pain_lower = raw_pain.lower()

    # ── Maintenance pain with known tools ──
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

    # ── Compliance / regulated pain ──
    if "compliance" in pain_lower or "regulated" in pain_lower:
        if is_strategic:
            if tone == "curious":
                return f"how do you keep regression cycles short when compliance requires full coverage before every release"
            return f"Regression cycles in a regulated {industry} environment can be a real bottleneck for release velocity"
        else:
            if tone == "curious":
                return f"how much of your sprint gets eaten by compliance-driven regression"
            return f"Running full regression before every release in a compliance-heavy environment takes serious bandwidth"

    # ── Scaling pain ──
    if "scaling" in pain_lower:
        if is_strategic:
            return f"Scaling test coverage without scaling headcount is one of the harder problems in {industry} engineering"
        else:
            return f"Growing automation coverage while your team's already stretched thin is a tough balance"

    # ── Maintenance pain without specific tools ──
    if "maintenance" in pain_lower:
        if is_strategic:
            return f"At {company}'s scale, test maintenance tends to become a real drag on release velocity"
        else:
            return f"Keeping test suites reliable as {company} ships faster is a constant challenge"

    # ── Generic fallback ──
    if is_strategic:
        return f"Test automation at {company}'s scale tends to become a strategic bottleneck"
    return f"Keeping test suites reliable as {company} ships faster is a constant challenge"


def _pick_pain_hook(artifact: dict) -> str:
    """Pick the best pain hypothesis for the hook (raw text)."""
    pains = artifact.get("pains", {}).get("hypothesized_pains", [])
    sorted_pains = sorted(pains, key=lambda p: p.get("confidence", 0), reverse=True)
    if sorted_pains:
        return sorted_pains[0].get("pain", "test maintenance and release velocity")
    return "test maintenance and release velocity"


def _short_pain_label(raw_pain: str) -> str:
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


def _pick_cta(product_config: dict, tone: str) -> str:
    """Pick a CTA matching the tone."""
    ctas = product_config.get("cta_options", [])
    if tone == "friendly" and len(ctas) > 1:
        return ctas[1]  # "Worth a quick reply..."
    elif tone == "direct" and len(ctas) > 0:
        return ctas[0]  # "Would a 15-minute comparison..."
    elif tone == "curious" and len(ctas) > 3:
        return ctas[3]  # "Worth a conversation?"
    elif tone == "curious" and len(ctas) > 2:
        return ctas[2]  # "Happy to share more..."
    return ctas[0] if ctas else "Worth a quick chat?"


def _pick_value_prop(product_config: dict, artifact: dict, tone: str) -> str:
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

    # Strategic VPs get high-level props
    if seniority in ("vp", "c-suite"):
        for vp in vps:
            if "maintenance" in vp.lower() or "reduction" in vp.lower():
                return vp
        return vps[0]

    # Users of competitor tools get the maintenance reduction prop
    if any(t in ("selenium", "cypress", "playwright") for t in tools):
        for vp in vps:
            if "maintenance" in vp.lower() or "selenium" in vp.lower() or "cypress" in vp.lower():
                return vp

    # QA roles get the collaboration prop
    if "qa" in func:
        for vp in vps:
            if "collaborate" in vp.lower() or "no-code" in vp.lower():
                return vp

    # Vary by tone as final fallback
    if tone == "friendly":
        return vps[0]
    elif tone == "direct":
        return vps[1] if len(vps) > 1 else vps[0]
    return vps[2] if len(vps) > 2 else vps[0]


def generate_message_variants(artifact: dict, scoring_result: dict,
                               product_config: dict = None,
                               channel: str = "linkedin") -> dict:
    """Generate 3 grounded message variants from ResearchArtifact + ScoringResult.

    Each variant uses:
    - A naturally-rendered personalization opener (no raw evidence strings)
    - A seniority-aware pain framing (strategic for VPs, tactical for managers)
    - A context-matched proof point and value prop
    - A tone-specific CTA with soft ask
    - Proof point rotation between variants where possible

    Args:
        artifact: A validated ResearchArtifact.
        scoring_result: A ScoringResult from scorer.score_from_artifact().
        product_config: Product config dict (loaded from file if None).
        channel: "linkedin" or "email".

    Returns:
        {"variants": [...], "qa_results": [...], "metadata": {...}}
    """
    product_config = product_config or _load_product_config()
    prospect = artifact.get("prospect", {})
    company_info = artifact.get("company", {})
    first_name = prospect.get("full_name", "").split()[0] if prospect.get("full_name") else ""
    company_name = prospect.get("company_name", "your company")
    title = prospect.get("title", "")
    sender = product_config.get("sender", "Rob Gorham")
    our_company = product_config.get("company", "Testsigma")

    raw_opener, opener_evidence = _pick_personalization_opener(artifact)
    raw_pain = _pick_pain_hook(artifact)

    # Select primary + secondary proof points for variety across variants
    pp_primary = _select_best_proof_point(artifact, product_config)
    pp_secondary = _select_best_proof_point(artifact, product_config,
                                             exclude_keys=[pp_primary["key"]])

    tones = ["friendly", "direct", "curious"]
    variants = []

    for tone in tones:
        opener = _render_opener(raw_opener, artifact, tone)
        pain = _render_pain_sentence(raw_pain, artifact, tone)
        cta = _pick_cta(product_config, tone)
        vp = _pick_value_prop(product_config, artifact, tone)

        # Rotate proof points: curious variant gets secondary if available
        if tone == "curious" and pp_secondary["key"] != pp_primary["key"]:
            pp = pp_secondary
        else:
            pp = pp_primary

        pain_label = _short_pain_label(raw_pain)
        func = _function_label(title)

        if tone == "friendly":
            body = (
                f"Hi {first_name},\n\n"
                f"{opener}. "
                f"{pain[0].upper()}{pain[1:]} - "
                f"and {pp.get('text', '')}.\n\n"
                f"{cta} If not, totally get it.\n\n"
                f"Best,\n{sender}"
            )
            subjects = [
                f"{func} at {company_name}",
                f"Thought for {first_name} re: {pain_label}",
                f"{company_name}'s {func} team",
            ]

        elif tone == "direct":
            # Only include value prop if it doesn't duplicate the proof point stat
            pp_text = pp.get("text", "")
            pp_metric = pp.get("metric", "").lower()
            vp_overlaps = pp_metric and any(
                word in vp.lower() for word in pp_metric.split()
                if len(word) > 3
            )
            proof_line = pp_text
            if vp and not vp_overlaps:
                proof_line = f"{pp_text}. {vp}"
            body = (
                f"Hi {first_name},\n\n"
                f"{opener}. {pain[0].upper()}{pain[1:]}.\n\n"
                f"{proof_line}.\n\n"
                f"{cta}\n\n"
                f"{sender}"
            )
            subjects = [
                f"{pain_label.capitalize()} at {company_name}",
                f"{first_name} - quick question",
                f"{our_company} for {company_name}",
            ]

        else:  # curious
            body = (
                f"Hi {first_name},\n\n"
                f"{opener} - {pain}?\n\n"
                f"{pp.get('text', '')}.\n\n"
                f"{cta} Either way, no worries.\n\n"
                f"Best,\n{sender}"
            )
            subjects = [
                f"How {company_name} handles {pain_label}",
                f"Question for {first_name}",
                f"{func} challenge at {company_name}?",
            ]

        variants.append({
            "tone": tone,
            "subject_lines": subjects,
            "body": body,
            "opener": opener,
            "opener_evidence": opener_evidence,
            "value_prop": vp,
            "proof_point": pp.get("short", ""),
            "proof_point_key": pp.get("key", ""),
            "cta": cta,
            "pain_hook": raw_pain,
            "char_count": len(body),
            "word_count": len(body.split()),
        })

    # Run QA on all variants
    qa_results = []
    for v in variants:
        qa = check_message_variant(v, artifact, product_config, channel)
        qa_results.append(qa)

    return {
        "variants": variants,
        "qa_results": qa_results,
        "metadata": {
            "prospect_name": prospect.get("full_name", ""),
            "company": company_name,
            "channel": channel,
            "scoring_tier": scoring_result.get("tier", "unknown"),
            "total_score": scoring_result.get("total_score", 0),
            "proof_point_used": pp_primary.get("key", ""),
            "generated_at": datetime.utcnow().isoformat(),
        },
    }


# ─── MESSAGE QA CHECKS (v2) ─────────────────────────────────────

def check_message_variant(variant: dict, artifact: dict,
                           product_config: dict = None,
                           channel: str = "linkedin") -> dict:
    """Run QA checks on a single message variant.

    Rejects or flags if:
    - personalization hook lacks evidence
    - message exceeds character limit
    - contains forbidden phrases (unless evidenced)
    - mentions browsing/scraping
    - says "I saw" / "I noticed" without evidence
    """
    product_config = product_config or _load_product_config()
    body = variant.get("body", "")
    opener_ev = variant.get("opener_evidence", "")
    checks = []
    all_passed = True

    # 1. Evidence check on opener
    has_opener_evidence = bool(opener_ev and opener_ev != "unknown - hypothesis only")
    checks.append({
        "check": "opener_has_evidence",
        "passed": has_opener_evidence,
        "detail": f"Evidence: {opener_ev}" if has_opener_evidence else "Opener lacks evidence grounding",
    })
    if not has_opener_evidence:
        all_passed = False

    # 2. Character limit
    max_chars = product_config.get("max_chars", {}).get(channel, 600)
    char_ok = len(body) <= max_chars
    checks.append({
        "check": "char_limit",
        "passed": char_ok,
        "detail": f"{len(body)}/{max_chars} chars" if char_ok else f"Over limit: {len(body)}/{max_chars}",
    })
    if not char_ok:
        all_passed = False

    # 3. Forbidden phrases
    forbidden = product_config.get("forbidden_phrases", [])
    body_lower = body.lower()
    found_forbidden = [fp for fp in forbidden if fp.lower() in body_lower]
    checks.append({
        "check": "no_forbidden_phrases",
        "passed": len(found_forbidden) == 0,
        "detail": f"Found: {found_forbidden}" if found_forbidden else "Clean",
    })
    if found_forbidden:
        all_passed = False

    # 4. No em dashes
    has_em = "\u2014" in body or "\u2013" in body
    checks.append({
        "check": "no_em_dashes",
        "passed": not has_em,
        "detail": "Contains em/en dash" if has_em else "Clean",
    })
    if has_em:
        all_passed = False

    # 5. Anti-hallucination: check proof point is from config
    pp_key = variant.get("proof_point_key", "")
    valid_pp = pp_key in (product_config.get("proof_points", {}) or PROOF_POINTS)
    checks.append({
        "check": "proof_point_valid",
        "passed": valid_pp or not pp_key,
        "detail": f"Using '{pp_key}'" if valid_pp else f"Unknown proof point: '{pp_key}'",
    })
    if pp_key and not valid_pp:
        all_passed = False

    # 6. Must_not_claim check
    constraints = artifact.get("constraints", {}).get("must_not_claim", [])
    constraint_violations = []
    for c in constraints:
        if "private docs" in c.lower() and any(phrase in body_lower for phrase in
                                                 ["private doc", "internal doc", "your document"]):
            constraint_violations.append(c)
        if "recent news" in c.lower() and "i saw" in body_lower and "news" in body_lower:
            constraint_violations.append(c)
    checks.append({
        "check": "constraints_respected",
        "passed": len(constraint_violations) == 0,
        "detail": f"Violations: {constraint_violations}" if constraint_violations else "All constraints met",
    })
    if constraint_violations:
        all_passed = False

    return {
        "tone": variant.get("tone", ""),
        "passed": all_passed,
        "checks": checks,
        "passed_count": sum(1 for c in checks if c["passed"]),
        "total_checks": len(checks),
    }
