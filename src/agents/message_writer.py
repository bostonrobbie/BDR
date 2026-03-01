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

# Extracted engines (backward-compatible re-exports)
from src.agents.proof_points import (
    PROOF_POINTS,
    select_proof_point,
    select_best_proof_point as _select_best_proof_point,
    select_best_proof_point_with_feedback as _select_best_proof_point_with_feedback,
    bridge_phrase as _bridge_phrase,
)
from src.agents.objection_engine import (
    OBJECTION_MAP,
    map_objection,
    predict_objection_from_artifact,
    build_objection_aware_bridge,
)
from src.agents.cta_engine import (
    connected_cta as _connected_cta,
    build_soft_ask as _build_soft_ask,
    build_signoff as _build_signoff,
    build_ps_line as _build_ps_line,
)
from src.agents.tone_engine import (
    function_label as _function_label,
    render_opener as _render_opener,
    render_pain_sentence as _render_pain_sentence,
    pick_personalization_opener as _pick_personalization_opener,
    pick_pain_hook as _pick_pain_hook,
    short_pain_label as _short_pain_label,
    pick_value_prop as _pick_value_prop,
    get_tools_and_competitor as _get_tools_and_competitor,
)


# ─── DYNAMIC SUBJECT LINE GENERATION ────────────────────────
# Generates multiple subject line styles per variant, each scored.
# Styles: question, metric-led, curiosity, personalized, direct.

SUBJECT_STYLES = {
    "question": "Question about their specific challenge",
    "metric_led": "Leads with a compelling number",
    "curiosity": "Creates intrigue without giving away the ask",
    "personalized": "References their name, company, or role",
    "direct": "Straightforward value proposition",
}


def generate_subject_lines(artifact: dict, pain_label: str, pp: dict,
                            tone: str = "friendly", max_chars: int = 80) -> list:
    """Generate 5 scored subject line variants in different styles.

    Each subject line is designed for a different psychological trigger:
    - Question: invites mental engagement
    - Metric-led: creates credibility
    - Curiosity: creates information gap
    - Personalized: signals relevance
    - Direct: respects inbox scanning

    Args:
        artifact: ResearchArtifact dict.
        pain_label: Short pain label (e.g. "test maintenance").
        pp: Proof point dict.
        tone: Message tone.
        max_chars: Maximum subject line length.

    Returns:
        List of {"style": str, "subject": str, "score": float, "reasons": list}
        sorted by score descending.
    """
    prospect = artifact.get("prospect", {})
    first_name = prospect.get("full_name", "").split()[0] if prospect.get("full_name") else ""
    company = prospect.get("company_name", "")
    title = prospect.get("title", "")
    func = _function_label(title)
    metric = pp.get("metric", "")

    subjects = []

    # 1. Question style
    q_options = [
        f"How does {company} handle {pain_label}?",
        f"Quick question for {first_name}",
        f"{pain_label.capitalize()} at {company}?",
    ]
    q_subj = _pick_best_fit(q_options, max_chars)
    q_score, q_reasons = _score_subject(q_subj, first_name, company, metric)
    subjects.append({"style": "question", "subject": q_subj,
                     "score": q_score, "reasons": q_reasons})

    # 2. Metric-led style
    if metric:
        m_options = [
            f"{metric} - relevant for {company}?",
            f"{metric} (how {pp.get('short', '').split(',')[0]} did it)",
        ]
    else:
        m_options = [f"A thought on {pain_label} at {company}"]
    m_subj = _pick_best_fit(m_options, max_chars)
    m_score, m_reasons = _score_subject(m_subj, first_name, company, metric)
    subjects.append({"style": "metric_led", "subject": m_subj,
                     "score": m_score, "reasons": m_reasons})

    # 3. Curiosity style
    c_options = [
        f"Thought for {first_name} re: {pain_label}",
        f"Something {company}'s {func} team might find useful",
        f"An idea for {company}",
    ]
    c_subj = _pick_best_fit(c_options, max_chars)
    c_score, c_reasons = _score_subject(c_subj, first_name, company, metric)
    subjects.append({"style": "curiosity", "subject": c_subj,
                     "score": c_score, "reasons": c_reasons})

    # 4. Personalized style
    p_options = [
        f"{first_name} - {func} at {company}",
        f"{company}'s {func} team",
        f"For {first_name} at {company}",
    ]
    p_subj = _pick_best_fit(p_options, max_chars)
    p_score, p_reasons = _score_subject(p_subj, first_name, company, metric)
    subjects.append({"style": "personalized", "subject": p_subj,
                     "score": p_score, "reasons": p_reasons})

    # 5. Direct style
    d_options = [
        f"{pain_label.capitalize()} at {company}",
        f"{func} challenge at {company}",
    ]
    d_subj = _pick_best_fit(d_options, max_chars)
    d_score, d_reasons = _score_subject(d_subj, first_name, company, metric)
    subjects.append({"style": "direct", "subject": d_subj,
                     "score": d_score, "reasons": d_reasons})

    # Sort by score descending
    subjects.sort(key=lambda s: s["score"], reverse=True)
    return subjects


def _pick_best_fit(options: list, max_chars: int) -> str:
    """Pick the longest option that fits within max_chars."""
    fitting = [o for o in options if len(o) <= max_chars]
    if fitting:
        return max(fitting, key=len)
    # Truncate the shortest option
    return options[0][:max_chars]


def _score_subject(subject: str, first_name: str, company: str,
                    metric: str) -> tuple:
    """Score a subject line on 0-1 scale.

    Factors: length, personalization, metric presence, question mark.
    Returns (score, reasons).
    """
    score = 0.5
    reasons = []

    # Length: 30-60 chars is ideal
    length = len(subject)
    if 30 <= length <= 60:
        score += 0.1
        reasons.append("Good length (30-60 chars)")
    elif length > 80:
        score -= 0.1
        reasons.append("Too long for preview")
    elif length < 15:
        score -= 0.1
        reasons.append("Too short")

    # Personalization
    if first_name and first_name in subject:
        score += 0.15
        reasons.append("Contains first name")
    if company and company in subject:
        score += 0.1
        reasons.append("Contains company name")

    # Metric
    if metric and any(m in subject for m in metric.split(",")):
        score += 0.1
        reasons.append("Contains metric")

    # Question mark (curiosity)
    if "?" in subject:
        score += 0.05
        reasons.append("Question format")

    return max(0.0, min(1.0, round(score, 2))), reasons


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






def generate_message_variants(artifact: dict, scoring_result: dict,
                               product_config: dict = None,
                               channel: str = "linkedin",
                               touch_number: int = 1) -> dict:
    """Generate 3 grounded message variants from ResearchArtifact + ScoringResult.

    Each variant uses:
    - A naturally-rendered personalization opener (no raw evidence strings)
    - A seniority-aware pain framing (strategic for VPs, tactical for managers)
    - An integrated proof-and-ask paragraph where CTA flows from the proof point
    - Proof point rotation between variants where possible
    - Sequence-aware structure adapting to the touch_number position

    Sequence adaptation (F8):
    - Touch 1: Full 6-element message structure (opener, company ref, pain, proof, CTA, soft ask)
    - Touch 2-3: Shorter follow-up referencing earlier outreach, lighter structure
    - Touch 4-5: Different angle, can escalate directness, reference prior touches
    - Touch 6+: Break-up style, minimal pitch, respectful close-out

    Args:
        artifact: A validated ResearchArtifact.
        scoring_result: A ScoringResult from scorer.score_from_artifact().
        product_config: Product config dict (loaded from file if None).
        channel: "linkedin" or "email".
        touch_number: Which touch in the sequence (1-6+). Defaults to 1.

    Returns:
        {"variants": [...], "qa_results": [...], "metadata": {...}}
    """
    product_config = product_config or _load_product_config()
    prospect = artifact.get("prospect", {})
    company_info = artifact.get("company", {})
    first_name = prospect.get("full_name", "").split()[0] if prospect.get("full_name") else ""
    company_name = prospect.get("company_name", "your company")
    title = prospect.get("title", "")
    seniority = prospect.get("seniority", "").lower()
    sender = product_config.get("sender", "Rob Gorham")
    our_company = product_config.get("company", "Testsigma")
    tier = scoring_result.get("tier", "cool")

    raw_opener, opener_evidence = _pick_personalization_opener(artifact)
    raw_pain = _pick_pain_hook(artifact)
    tools, competitor = _get_tools_and_competitor(artifact)

    # Select primary + secondary proof points for variety across variants
    # Primary selection uses feedback data when available
    pp_primary = _select_best_proof_point_with_feedback(artifact, product_config)
    pp_secondary = _select_best_proof_point(artifact, product_config,
                                             exclude_keys=[pp_primary["key"]])

    # Predict likely objection for this prospect
    predicted_objection = predict_objection_from_artifact(artifact)

    tones = ["friendly", "direct", "curious"]
    variants = []

    for tone in tones:
        opener = _render_opener(raw_opener, artifact, tone)
        pain = _render_pain_sentence(raw_pain, artifact, tone)
        vp = _pick_value_prop(product_config, artifact, tone)

        # Rotate proof points: curious variant gets secondary if available
        if tone == "curious" and pp_secondary["key"] != pp_primary["key"]:
            pp = pp_secondary
            pp_other = pp_primary
        else:
            pp = pp_primary
            pp_other = pp_secondary

        # Build integrated closing pieces
        pp_text = pp.get("text", "")
        # Use objection-aware bridge when possible, fall back to standard
        obj_bridge = build_objection_aware_bridge(predicted_objection, tone, pp_text)
        bridge = obj_bridge if obj_bridge else _bridge_phrase(pp_text, artifact, tools)
        cta = _connected_cta(tier, tone, seniority, company_name, competitor)
        soft = _build_soft_ask(tier, tone)
        signoff = _build_signoff(tone, sender)
        ps = _build_ps_line(scoring_result, pp, pp_other, channel)

        pain_label = _short_pain_label(raw_pain)
        func = _function_label(title)

        if tone == "friendly":
            # PP in first paragraph with bridge, CTA flows from it
            cta_line = f"{cta} {soft}".rstrip() if soft else cta
            body = (
                f"Hi {first_name},\n\n"
                f"{opener}. "
                f"{pain[0].upper()}{pain[1:]} - "
                f"{pp_text}{bridge}.\n\n"
                f"{cta_line}\n\n"
                f"{signoff}"
            )
            if ps:
                body += f"\n\n{ps}"
            subjects = [
                f"{func} at {company_name}",
                f"Thought for {first_name} re: {pain_label}",
                f"{company_name}'s {func} team",
            ]

        elif tone == "direct":
            # Merge PP + value prop + bridge + CTA into one paragraph
            pp_metric = pp.get("metric", "").lower()
            vp_overlaps = pp_metric and any(
                word in vp.lower() for word in pp_metric.split()
                if len(word) > 3
            )
            proof_and_ask = f"{pp_text}{bridge}."
            if vp and not vp_overlaps:
                proof_and_ask += f" {vp}."
            proof_and_ask += f" {cta}"
            body = (
                f"Hi {first_name},\n\n"
                f"{opener}. {pain[0].upper()}{pain[1:]}.\n\n"
                f"{proof_and_ask}\n\n"
                f"{signoff}"
            )
            if ps:
                body += f"\n\n{ps}"
            subjects = [
                f"{pain_label.capitalize()} at {company_name}",
                f"{first_name} - quick question",
                f"{our_company} for {company_name}",
            ]

        else:  # curious
            # Merge PP + bridge + CTA into one flowing paragraph
            cta_line = f"{cta} {soft}".rstrip() if soft else cta
            proof_and_ask = f"{pp_text}{bridge}. {cta_line}"
            body = (
                f"Hi {first_name},\n\n"
                f"{opener} - {pain}?\n\n"
                f"{proof_and_ask}\n\n"
                f"{signoff}"
            )
            if ps:
                body += f"\n\n{ps}"
            subjects = [
                f"How {company_name} handles {pain_label}",
                f"Question for {first_name}",
                f"{func} challenge at {company_name}?",
            ]

        # F8: Sequence-aware adaptation for later touches
        if touch_number >= 6:
            body = _adapt_for_breakup(first_name, company_name, tone, sender)
            subjects = [
                f"Closing the loop, {first_name}",
                f"Last note from me",
                f"All good, {first_name}",
            ]
        elif touch_number >= 3:
            body = _adapt_for_followup(
                body, first_name, company_name, tone, sender,
                pp_text, bridge, cta, soft, signoff, touch_number
            )
            subjects = [
                f"Following up, {first_name}",
                f"Quick follow-up re: {pain_label}",
                f"Circling back on {pain_label}",
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
            "predicted_objection": predicted_objection.get("objection", ""),
            "objection_key": predicted_objection.get("objection_key", ""),
            "touch_number": touch_number,
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
            "touch_number": touch_number,
            "generated_at": datetime.utcnow().isoformat(),
        },
    }


def _adapt_for_followup(original_body: str, first_name: str, company_name: str,
                         tone: str, sender: str, pp_text: str, bridge: str,
                         cta: str, soft: str, signoff: str,
                         touch_number: int) -> str:
    """Adapt a full Touch 1 body into a shorter follow-up for touches 3-5.

    Follow-ups are shorter (40-70 words), reference prior outreach, use a
    different angle, and have a softer CTA.
    """
    cta_line = f"{cta} {soft}".rstrip() if soft else cta

    if tone == "friendly":
        if touch_number <= 3:
            return (
                f"Hi {first_name},\n\n"
                f"Circling back quick. {pp_text}{bridge}.\n\n"
                f"{cta_line}\n\n"
                f"{signoff}"
            )
        else:
            return (
                f"Hi {first_name},\n\n"
                f"One more thought on {company_name}'s testing setup. "
                f"{pp_text}{bridge}.\n\n"
                f"Happy to share more if helpful.\n\n"
                f"{signoff}"
            )
    elif tone == "direct":
        if touch_number <= 3:
            return (
                f"Hi {first_name},\n\n"
                f"Following up briefly. {pp_text}{bridge}. {cta}\n\n"
                f"{signoff}"
            )
        else:
            return (
                f"Hi {first_name},\n\n"
                f"Different angle for {company_name}: {pp_text}{bridge}. {cta}\n\n"
                f"{signoff}"
            )
    else:  # curious
        if touch_number <= 3:
            return (
                f"Hi {first_name},\n\n"
                f"Wanted to circle back. {pp_text}{bridge}. "
                f"{cta_line}\n\n"
                f"{signoff}"
            )
        else:
            return (
                f"Hi {first_name},\n\n"
                f"One last thought. {pp_text}{bridge}. "
                f"{cta_line}\n\n"
                f"{signoff}"
            )


def _adapt_for_breakup(first_name: str, company_name: str,
                        tone: str, sender: str) -> str:
    """Generate a break-up message for touch 6+.

    No pitch, no product mention, no proof points. Just a respectful
    close-out that leaves the door open.
    """
    if tone == "friendly":
        return (
            f"Hi {first_name},\n\n"
            f"I've reached out a few times and want to be respectful of your inbox. "
            f"If the timing isn't right, totally get it. "
            f"Just wanted to close the loop so I'm not adding noise.\n\n"
            f"If anything changes down the road, happy to chat.\n\n"
            f"Cheers,\n{sender}"
        )
    elif tone == "direct":
        return (
            f"Hi {first_name},\n\n"
            f"Closing the loop on my earlier messages. No worries if it's not a fit. "
            f"If things change, my door's open.\n\n"
            f"{sender}"
        )
    else:  # curious
        return (
            f"Hi {first_name},\n\n"
            f"I'll keep this short. I've reached out a few times and don't want to be a pest. "
            f"If this ever becomes relevant for {company_name}, I'm easy to find.\n\n"
            f"Best,\n{sender}"
        )


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


# ─── CHANNEL-SPECIFIC RENDERING ─────────────────────────────
# LinkedIn and email have different norms. These adapters take the
# standard variant output and reshape it for the target channel.


# LinkedIn limits
_LINKEDIN_INMAIL_LIMIT = 1900
_LINKEDIN_CONNECTION_NOTE_LIMIT = 300
_LINKEDIN_INMESSAGE_LIMIT = 600


def render_for_channel(variant: dict, channel: str, artifact: dict = None,
                        product_config: dict = None) -> dict:
    """Adapt a message variant for a specific channel's norms.

    LinkedIn: shorter, more casual, no "Hi Name," for connection notes,
              subject line only for InMails, tighter char limits.
    Email:    full treatment with subject lines, P.S. lines allowed,
              can be longer, more formal structure.

    Args:
        variant: A variant dict from generate_message_variants().
        channel: Target channel ("linkedin_inmail", "linkedin_connection",
                 "linkedin_message", "email").
        artifact: ResearchArtifact (optional, for context).
        product_config: Product config (optional).

    Returns:
        New variant dict adapted for the channel, with channel_metadata.
    """
    adapted = dict(variant)  # shallow copy
    body = variant.get("body", "")
    first_name = ""
    if artifact:
        prospect = artifact.get("prospect", {})
        first_name = prospect.get("full_name", "").split()[0] if prospect.get("full_name") else ""

    if channel == "linkedin_connection":
        adapted = _render_linkedin_connection(adapted, body, first_name)
    elif channel == "linkedin_message":
        adapted = _render_linkedin_message(adapted, body, first_name)
    elif channel == "linkedin_inmail":
        adapted = _render_linkedin_inmail(adapted, body)
    elif channel == "email":
        adapted = _render_email(adapted, body, product_config)
    # Default: return as-is

    adapted["channel"] = channel
    adapted["char_count"] = len(adapted.get("body", ""))
    adapted["word_count"] = len(adapted.get("body", "").split())

    return adapted


def _render_linkedin_connection(variant: dict, body: str, first_name: str) -> dict:
    """Adapt for LinkedIn connection request note (300 char limit).

    Connection notes are very short. Strip greeting, signoff, keep only
    the opener + one sentence of value + soft ask.
    """
    # Strip greeting
    lines = body.split("\n")
    content_lines = []
    past_greeting = False
    for line in lines:
        stripped = line.strip()
        if not past_greeting:
            if stripped.lower().startswith(("hi ", "hey ", "hello ")) or not stripped:
                continue
            past_greeting = True
        content_lines.append(line)

    content = "\n".join(content_lines).strip()

    # Strip signoff (last paragraph if it's short)
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    if len(paragraphs) > 1:
        last = paragraphs[-1]
        # If last para is signoff (short, contains sender name pattern)
        if len(last.split()) <= 5:
            paragraphs = paragraphs[:-1]

    # Take first 2 paragraphs max, join
    short_body = "\n\n".join(paragraphs[:2])

    # Truncate to limit
    if len(short_body) > _LINKEDIN_CONNECTION_NOTE_LIMIT:
        # Find a clean break point
        short_body = _truncate_cleanly(short_body, _LINKEDIN_CONNECTION_NOTE_LIMIT)

    variant["body"] = short_body
    variant["subject_lines"] = []  # No subject line for connection requests
    variant["channel_metadata"] = {
        "format": "connection_note",
        "char_limit": _LINKEDIN_CONNECTION_NOTE_LIMIT,
        "greeting_stripped": True,
        "signoff_stripped": True,
    }
    return variant


def _render_linkedin_message(variant: dict, body: str, first_name: str) -> dict:
    """Adapt for LinkedIn direct message (600 char limit, casual)."""
    # Keep greeting but ensure it's casual
    if body.startswith(f"Hi {first_name},"):
        body = body.replace(f"Hi {first_name},", f"Hey {first_name},", 1)

    # Strip P.S. lines
    if "P.S." in body:
        body = body[:body.index("P.S.")].rstrip()

    # Truncate if over limit
    if len(body) > _LINKEDIN_INMESSAGE_LIMIT:
        body = _truncate_cleanly(body, _LINKEDIN_INMESSAGE_LIMIT)

    variant["body"] = body
    variant["subject_lines"] = []  # No subject line for DMs
    variant["channel_metadata"] = {
        "format": "direct_message",
        "char_limit": _LINKEDIN_INMESSAGE_LIMIT,
    }
    return variant


def _render_linkedin_inmail(variant: dict, body: str) -> dict:
    """Adapt for LinkedIn InMail (1900 char limit, has subject line)."""
    # InMail is the closest to the standard output, just enforce limit
    if len(body) > _LINKEDIN_INMAIL_LIMIT:
        body = _truncate_cleanly(body, _LINKEDIN_INMAIL_LIMIT)

    variant["body"] = body
    variant["channel_metadata"] = {
        "format": "inmail",
        "char_limit": _LINKEDIN_INMAIL_LIMIT,
    }
    return variant


def _render_email(variant: dict, body: str, product_config: dict = None) -> dict:
    """Adapt for email (1200 char limit, full formatting allowed)."""
    product_config = product_config or _load_product_config()
    max_chars = product_config.get("max_chars", {}).get("email", 1200)

    if len(body) > max_chars:
        body = _truncate_cleanly(body, max_chars)

    variant["body"] = body
    variant["channel_metadata"] = {
        "format": "email",
        "char_limit": max_chars,
    }
    return variant


def _truncate_cleanly(text: str, limit: int) -> str:
    """Truncate text to limit at a clean sentence or word boundary."""
    if len(text) <= limit:
        return text

    # Try to break at last sentence boundary before limit
    truncated = text[:limit]
    for end_char in [".\n", ". ", ".\n\n"]:
        last_period = truncated.rfind(end_char)
        if last_period > limit * 0.6:  # At least 60% of content
            return text[:last_period + 1].rstrip()

    # Fall back to last space
    last_space = truncated.rfind(" ")
    if last_space > limit * 0.7:
        return text[:last_space].rstrip()

    return truncated.rstrip()


