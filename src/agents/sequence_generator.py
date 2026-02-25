"""
Outreach Command Center - Multi-Touch Sequence Generator
Generates a coherent 5-6 touch sequence where each message escalates,
references the previous one, and uses a different angle/proof point.

Touch sequence SOP:
  Touch 1: LinkedIn InMail (opening cold outreach)
  Touch 2: Call snippet (3-line cheat sheet)
  Touch 3: LinkedIn InMail follow-up (shorter, new proof point)
  Touch 4: Call snippet (different angle)
  Touch 5: Email (if available; slightly more direct)
  Touch 6: LinkedIn break-up (no pitch, respectful close-out)

Cadence timing is tier-driven:
  Hot:  5 touches in 10 days (aggressive)
  Warm: 5 touches in 14 days (standard)
  Cool: 3 touches in 21 days (gentle)
  Cold: 2 touches in 14 days (light)
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.agents.message_writer import (
    _load_product_config,
    _select_best_proof_point,
    _pick_personalization_opener,
    _pick_pain_hook,
    _get_tools_and_competitor,
    _render_opener,
    _render_pain_sentence,
    _pick_value_prop,
    _bridge_phrase,
    _connected_cta,
    _build_soft_ask,
    _build_signoff,
    _build_ps_line,
    _short_pain_label,
    _function_label,
    check_message_variant,
)


# ─── CADENCE CONFIGS ──────────────────────────────────────────

CADENCE = {
    "hot": {
        "touches": [1, 2, 3, 4, 5, 6],
        "days_between": [0, 2, 3, 5, 7, 10],
        "label": "aggressive (10 days)",
    },
    "warm": {
        "touches": [1, 2, 3, 4, 5, 6],
        "days_between": [0, 3, 5, 8, 11, 14],
        "label": "standard (14 days)",
    },
    "cool": {
        "touches": [1, 3, 6],
        "days_between": [0, 7, 21],
        "label": "gentle (21 days)",
    },
    "cold": {
        "touches": [1, 6],
        "days_between": [0, 14],
        "label": "light (14 days)",
    },
}


# ─── FOLLOW-UP BODY RENDERERS ────────────────────────────────

def _render_touch3_followup(first_name: str, company_name: str,
                             pp_text: str, bridge: str,
                             cta: str, soft: str, signoff: str,
                             tone: str) -> str:
    """Render Touch 3 follow-up (shorter, references previous outreach)."""
    cta_line = f"{cta} {soft}".rstrip() if soft else cta

    if tone == "friendly":
        body = (
            f"Hi {first_name},\n\n"
            f"Circling back quick. Thought this might be relevant for {company_name} - "
            f"{pp_text}{bridge}.\n\n"
            f"{cta_line}\n\n"
            f"{signoff}"
        )
    elif tone == "direct":
        body = (
            f"Hi {first_name},\n\n"
            f"Following up. {pp_text}{bridge}. {cta}\n\n"
            f"{signoff}"
        )
    else:  # curious
        body = (
            f"Hi {first_name},\n\n"
            f"Circling back - {pp_text}{bridge}. {cta_line}\n\n"
            f"{signoff}"
        )
    return body


def _render_touch5_email(first_name: str, company_name: str,
                          opener: str, pain: str,
                          pp_text: str, bridge: str,
                          vp: str, cta: str, soft: str,
                          signoff: str, ps: str,
                          tone: str) -> str:
    """Render Touch 5 email (can be longer, slightly more direct)."""
    cta_line = f"{cta} {soft}".rstrip() if soft else cta

    if tone == "friendly":
        body = (
            f"Hi {first_name},\n\n"
            f"Reaching out via email since I know LinkedIn can get noisy. "
            f"{opener}.\n\n"
            f"{pain[0].upper()}{pain[1:]} - "
            f"{pp_text}{bridge}.\n\n"
            f"{cta_line}\n\n"
            f"{signoff}"
        )
    elif tone == "direct":
        proof_and_ask = f"{pp_text}{bridge}."
        if vp:
            proof_and_ask += f" {vp}."
        proof_and_ask += f" {cta}"
        body = (
            f"Hi {first_name},\n\n"
            f"Switching to email. {opener}. {pain[0].upper()}{pain[1:]}.\n\n"
            f"{proof_and_ask}\n\n"
            f"{signoff}"
        )
    else:  # curious
        body = (
            f"Hi {first_name},\n\n"
            f"Trying email since LinkedIn can be easy to miss. "
            f"{opener} - {pain}?\n\n"
            f"{pp_text}{bridge}. {cta_line}\n\n"
            f"{signoff}"
        )

    if ps:
        body += f"\n\n{ps}"
    return body


def _render_touch6_breakup(first_name: str, signoff: str, tone: str) -> str:
    """Render Touch 6 break-up (no pitch, respectful close-out)."""
    if tone == "friendly":
        body = (
            f"Hi {first_name},\n\n"
            f"I've reached out a couple of times and haven't heard back, which is totally fine. "
            f"Just wanted to close the loop so I'm not clogging your inbox.\n\n"
            f"If the timing's ever right, my door's open.\n\n"
            f"{signoff}"
        )
    elif tone == "direct":
        body = (
            f"Hi {first_name},\n\n"
            f"Closing the loop here. If testing tooling comes back on the radar, happy to chat.\n\n"
            f"{signoff}"
        )
    else:  # curious
        body = (
            f"Hi {first_name},\n\n"
            f"Figured I'd close the loop rather than keep pinging. "
            f"If priorities shift down the road, feel free to reach out.\n\n"
            f"{signoff}"
        )
    return body


def _render_call_snippet(first_name: str, company_name: str, title: str,
                          pain: str, pp_short: str, tone: str) -> str:
    """Render a 3-line call snippet (opener, pain, bridge)."""
    if tone == "friendly":
        opener_line = f"Hey {first_name}, this is Rob from Testsigma - calling about your {title} work at {company_name}."
    elif tone == "direct":
        opener_line = f"Hi {first_name}, Rob from Testsigma. Quick call about {company_name}."
    else:
        opener_line = f"Hey {first_name}, Rob from Testsigma - had a question about how {company_name} handles test automation."

    pain_line = f"{pain[0].upper()}{pain[1:]}."
    bridge_line = f"We helped {pp_short}. Worth 60 seconds to see if it's relevant?"

    return f"OPENER: {opener_line}\nPAIN: {pain_line}\nBRIDGE: {bridge_line}"


# ─── SEQUENCE SUBJECT LINES ──────────────────────────────────

def _touch_subject_lines(touch_number: int, first_name: str,
                          company_name: str, func: str,
                          pain_label: str, our_company: str) -> list:
    """Generate subject lines for each touch in the sequence."""
    if touch_number == 1:
        return [
            f"{func} at {company_name}",
            f"Thought for {first_name} re: {pain_label}",
            f"{company_name}'s {func} team",
        ]
    elif touch_number == 3:
        return [
            f"Re: {func} at {company_name}",
            f"Quick follow-up, {first_name}",
            f"One more thought for {company_name}",
        ]
    elif touch_number == 5:
        return [
            f"{pain_label.capitalize()} at {company_name}",
            f"{first_name} - different angle",
            f"{our_company} + {company_name}",
        ]
    elif touch_number == 6:
        return [
            f"Closing the loop",
            f"Last note, {first_name}",
        ]
    return [f"Touch {touch_number}"]


# ─── MAIN SEQUENCE GENERATOR ─────────────────────────────────

def generate_sequence(artifact: dict, scoring_result: dict,
                       product_config: dict = None,
                       tone: str = "friendly",
                       has_email: bool = False,
                       start_date: str = None) -> dict:
    """Generate a complete multi-touch outreach sequence.

    Produces all touches in the cadence with proof point rotation,
    escalating angles, and tier-driven timing.

    Args:
        artifact: A validated ResearchArtifact.
        scoring_result: A ScoringResult from score_from_artifact().
        product_config: Product config dict (loaded if None).
        tone: Primary tone for the sequence (friendly/direct/curious).
        has_email: Whether the prospect has an email address.
        start_date: ISO date string for sequence start (defaults to now).

    Returns:
        {"touches": [...], "cadence": {...}, "metadata": {...}}
    """
    product_config = product_config or _load_product_config()
    prospect = artifact.get("prospect", {})
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
    func = _function_label(title)
    pain_label = _short_pain_label(raw_pain)

    # Get cadence for this tier
    cadence = CADENCE.get(tier, CADENCE["warm"])
    base_date = datetime.fromisoformat(start_date) if start_date else datetime.utcnow()

    # Select proof points for rotation (one per written touch)
    pp1 = _select_best_proof_point(artifact, product_config)
    pp3 = _select_best_proof_point(artifact, product_config, exclude_keys=[pp1["key"]])
    pp5 = _select_best_proof_point(artifact, product_config, exclude_keys=[pp1["key"], pp3["key"]])
    # Call snippets use different PPs from the adjacent written touches
    pp_call = _select_best_proof_point(artifact, product_config, exclude_keys=[pp1["key"]])

    touches = []
    used_pps = []

    for i, touch_num in enumerate(cadence["touches"]):
        send_date = (base_date + timedelta(days=cadence["days_between"][i])).isoformat()

        if touch_num == 1:
            # Touch 1: Full InMail (same as generate_message_variants friendly)
            opener = _render_opener(raw_opener, artifact, tone)
            pain = _render_pain_sentence(raw_pain, artifact, tone)
            vp = _pick_value_prop(product_config, artifact, tone)
            pp = pp1
            pp_text = pp.get("text", "")
            bridge = _bridge_phrase(pp_text, artifact, tools)
            cta = _connected_cta(tier, tone, seniority, company_name, competitor)
            soft = _build_soft_ask(tier, tone)
            signoff = _build_signoff(tone, sender)

            cta_line = f"{cta} {soft}".rstrip() if soft else cta
            body = (
                f"Hi {first_name},\n\n"
                f"{opener}. "
                f"{pain[0].upper()}{pain[1:]} - "
                f"{pp_text}{bridge}.\n\n"
                f"{cta_line}\n\n"
                f"{signoff}"
            )
            subjects = _touch_subject_lines(1, first_name, company_name, func, pain_label, our_company)
            touch = {
                "touch_number": 1,
                "channel": "linkedin",
                "touch_type": "inmail",
                "subject_lines": subjects,
                "body": body,
                "proof_point_key": pp["key"],
                "proof_point": pp.get("short", ""),
                "pain_hook": raw_pain,
                "opener": opener,
                "opener_evidence": opener_evidence,
                "cta": cta,
                "send_date": send_date,
                "char_count": len(body),
                "word_count": len(body.split()),
            }

        elif touch_num in (2, 4):
            # Call snippets
            pp_for_call = pp_call if touch_num == 2 else pp3
            pain = _render_pain_sentence(raw_pain, artifact, tone)
            body = _render_call_snippet(
                first_name, company_name, title, pain,
                pp_for_call.get("short", ""), tone)
            touch = {
                "touch_number": touch_num,
                "channel": "phone",
                "touch_type": "call_snippet",
                "body": body,
                "proof_point_key": pp_for_call["key"],
                "proof_point": pp_for_call.get("short", ""),
                "pain_hook": raw_pain,
                "send_date": send_date,
                "char_count": len(body),
                "word_count": len(body.split()),
            }

        elif touch_num == 3:
            # Follow-up InMail (shorter, new proof point)
            pp = pp3
            pp_text = pp.get("text", "")
            bridge = _bridge_phrase(pp_text, artifact, tools)
            cta = _connected_cta(tier, tone, seniority, company_name, competitor)
            soft = _build_soft_ask(tier, tone)
            signoff = _build_signoff(tone, sender)
            body = _render_touch3_followup(
                first_name, company_name, pp_text, bridge,
                cta, soft, signoff, tone)
            subjects = _touch_subject_lines(3, first_name, company_name, func, pain_label, our_company)
            touch = {
                "touch_number": 3,
                "channel": "linkedin",
                "touch_type": "inmail_followup",
                "subject_lines": subjects,
                "body": body,
                "proof_point_key": pp["key"],
                "proof_point": pp.get("short", ""),
                "pain_hook": raw_pain,
                "send_date": send_date,
                "char_count": len(body),
                "word_count": len(body.split()),
            }

        elif touch_num == 5:
            if not has_email:
                continue
            # Email (slightly more direct, different channel acknowledgment)
            opener = _render_opener(raw_opener, artifact, tone)
            pain = _render_pain_sentence(raw_pain, artifact, tone)
            vp = _pick_value_prop(product_config, artifact, tone)
            pp = pp5
            pp_text = pp.get("text", "")
            bridge = _bridge_phrase(pp_text, artifact, tools)
            cta = _connected_cta(tier, tone, seniority, company_name, competitor)
            soft = _build_soft_ask(tier, tone)
            signoff = _build_signoff(tone, sender)
            scoring_for_ps = scoring_result.copy()
            pp_other = pp1
            ps = _build_ps_line(scoring_for_ps, pp, pp_other, "email")
            body = _render_touch5_email(
                first_name, company_name, opener, pain,
                pp_text, bridge, vp, cta, soft, signoff, ps, tone)
            subjects = _touch_subject_lines(5, first_name, company_name, func, pain_label, our_company)
            touch = {
                "touch_number": 5,
                "channel": "email",
                "touch_type": "email",
                "subject_lines": subjects,
                "body": body,
                "proof_point_key": pp["key"],
                "proof_point": pp.get("short", ""),
                "pain_hook": raw_pain,
                "opener": opener,
                "opener_evidence": opener_evidence,
                "cta": cta,
                "send_date": send_date,
                "char_count": len(body),
                "word_count": len(body.split()),
            }

        elif touch_num == 6:
            # Break-up (no pitch)
            signoff = _build_signoff(tone, sender)
            body = _render_touch6_breakup(first_name, signoff, tone)
            subjects = _touch_subject_lines(6, first_name, company_name, func, pain_label, our_company)
            touch = {
                "touch_number": 6,
                "channel": "linkedin",
                "touch_type": "inmail_breakup",
                "subject_lines": subjects,
                "body": body,
                "proof_point_key": "",
                "proof_point": "",
                "send_date": send_date,
                "char_count": len(body),
                "word_count": len(body.split()),
            }

        else:
            continue

        touches.append(touch)

    # Run QA on written touches (not call snippets)
    qa_results = []
    for touch in touches:
        if touch["touch_type"] == "call_snippet":
            continue
        variant_for_qa = {
            "tone": tone,
            "body": touch["body"],
            "opener_evidence": touch.get("opener_evidence", opener_evidence),
            "proof_point_key": touch.get("proof_point_key", ""),
        }
        qa = check_message_variant(variant_for_qa, artifact, product_config,
                                    touch.get("channel", "linkedin"))
        qa_results.append({
            "touch_number": touch["touch_number"],
            "touch_type": touch["touch_type"],
            **qa,
        })

    # Proof point rotation summary
    pp_keys_used = [t["proof_point_key"] for t in touches if t.get("proof_point_key")]
    unique_pps = len(set(pp_keys_used))

    return {
        "touches": touches,
        "cadence": {
            "tier": tier,
            "label": cadence["label"],
            "total_touches": len(touches),
            "total_days": cadence["days_between"][-1] if cadence["days_between"] else 0,
        },
        "qa_results": qa_results,
        "metadata": {
            "prospect_name": prospect.get("full_name", ""),
            "company": company_name,
            "tone": tone,
            "scoring_tier": tier,
            "total_score": scoring_result.get("total_score", 0),
            "proof_points_used": list(set(pp_keys_used)),
            "proof_point_rotation": f"{unique_pps} unique PPs across {len(pp_keys_used)} touches",
            "has_email": has_email,
            "generated_at": datetime.utcnow().isoformat(),
        },
    }


def get_cadence_schedule(tier: str, start_date: str = None) -> list:
    """Get the cadence schedule for a tier (useful for planning views).

    Returns:
        List of {"touch_number": int, "day_offset": int, "send_date": str,
                 "channel": str, "touch_type": str}
    """
    cadence = CADENCE.get(tier, CADENCE["warm"])
    base_date = datetime.fromisoformat(start_date) if start_date else datetime.utcnow()

    channel_map = {1: "linkedin", 2: "phone", 3: "linkedin", 4: "phone", 5: "email", 6: "linkedin"}
    type_map = {1: "inmail", 2: "call", 3: "followup", 4: "call", 5: "email", 6: "breakup"}

    schedule = []
    for i, touch_num in enumerate(cadence["touches"]):
        day_offset = cadence["days_between"][i]
        send_date = (base_date + timedelta(days=day_offset)).isoformat()
        schedule.append({
            "touch_number": touch_num,
            "day_offset": day_offset,
            "send_date": send_date,
            "channel": channel_map.get(touch_num, "linkedin"),
            "touch_type": type_map.get(touch_num, "message"),
        })

    return schedule
