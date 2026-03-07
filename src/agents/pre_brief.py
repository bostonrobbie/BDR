"""
Outreach Command Center - Pre-Brief Agent
Reads all previous batch data and generates a 5-line "What's Working" summary
to guide the next batch build.
"""

import json
import sys
import os
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.db import models


def generate_pre_brief() -> dict:
    """
    Analyze all historical data and generate a pre-brief for the next batch.

    Returns 5 insights:
    1. Best persona - which title/level replies most
    2. Best proof point - which customer story triggers replies
    3. Best vertical - which industry is warmest
    4. Best pattern - opener/ask/length pattern that works
    5. Stop doing - one thing to drop
    """
    conn = models.get_db()

    # Get all replies with full context
    replies = conn.execute("""
        SELECT r.*, c.persona_type, c.title, c.personalization_score,
               a.industry, a.employee_count,
               md.proof_point_used, md.pain_hook, md.opener_style, md.ask_style,
               md.word_count, md.ab_group, md.ab_variable, md.touch_number
        FROM replies r
        LEFT JOIN contacts c ON r.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        LEFT JOIN touchpoints tp ON r.touchpoint_id = tp.id
        LEFT JOIN message_drafts md ON tp.message_draft_id = md.id
    """).fetchall()
    replies = [dict(r) for r in replies]

    # Get all touchpoints for denominator
    touches = conn.execute("""
        SELECT tp.*, c.persona_type, c.title, a.industry,
               md.proof_point_used, md.opener_style, md.ask_style, md.word_count
        FROM touchpoints tp
        LEFT JOIN contacts c ON tp.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        LEFT JOIN message_drafts md ON tp.message_draft_id = md.id
    """).fetchall()
    touches = [dict(t) for t in touches]

    # Get opportunities for deeper attribution
    opps = conn.execute("""
        SELECT o.*, c.persona_type, a.industry
        FROM opportunities o
        LEFT JOIN contacts c ON o.contact_id = c.id
        LEFT JOIN accounts a ON o.account_id = a.id
    """).fetchall()
    opps = [dict(o) for o in opps]

    conn.close()

    brief = {
        "total_touches": len(touches),
        "total_replies": len(replies),
        "total_opportunities": len(opps),
        "insights": []
    }

    if len(replies) == 0:
        brief["insights"] = [
            {"label": "Best persona", "value": "Not enough data yet (0 replies)"},
            {"label": "Best proof point", "value": "Not enough data yet"},
            {"label": "Best vertical", "value": "Not enough data yet"},
            {"label": "Best pattern", "value": "Not enough data yet"},
            {"label": "Stop doing", "value": "Keep testing - need more data"},
        ]
        brief["summary"] = "No reply data yet. First batch results pending."
        return brief

    # 1. Best persona
    persona_replies = Counter(r.get("persona_type", "Unknown") for r in replies if r.get("intent") != "negative")
    persona_touches = Counter(t.get("persona_type", "Unknown") for t in touches)
    persona_rates = {}
    for persona in persona_touches:
        if persona_touches[persona] >= 3:  # minimum sample
            rate = persona_replies.get(persona, 0) / persona_touches[persona]
            persona_rates[persona] = {"rate": round(rate * 100, 1), "replies": persona_replies.get(persona, 0), "sent": persona_touches[persona]}
    if persona_rates:
        best_persona = max(persona_rates, key=lambda x: persona_rates[x]["rate"])
        brief["insights"].append({
            "label": "Best persona",
            "value": f"{best_persona} ({persona_rates[best_persona]['rate']}% reply rate, {persona_rates[best_persona]['replies']}/{persona_rates[best_persona]['sent']})"
        })
    else:
        brief["insights"].append({"label": "Best persona", "value": "Not enough data per persona yet"})

    # 2. Best proof point
    proof_replies = Counter(r.get("proof_point_used") for r in replies if r.get("proof_point_used") and r.get("intent") != "negative")
    if proof_replies:
        best_proof = proof_replies.most_common(1)[0]
        brief["insights"].append({
            "label": "Best proof point",
            "value": f"{best_proof[0]} ({best_proof[1]} positive replies)"
        })
    else:
        brief["insights"].append({"label": "Best proof point", "value": "No proof point attribution yet"})

    # 3. Best vertical
    vertical_replies = Counter(r.get("industry", "Unknown") for r in replies if r.get("intent") != "negative")
    vertical_touches = Counter(t.get("industry", "Unknown") for t in touches)
    vertical_rates = {}
    for v in vertical_touches:
        if vertical_touches[v] >= 3:
            rate = vertical_replies.get(v, 0) / vertical_touches[v]
            vertical_rates[v] = round(rate * 100, 1)
    if vertical_rates:
        best_vertical = max(vertical_rates, key=vertical_rates.get)
        brief["insights"].append({
            "label": "Best vertical",
            "value": f"{best_vertical} ({vertical_rates[best_vertical]}% reply rate)"
        })
    else:
        brief["insights"].append({"label": "Best vertical", "value": "Not enough data per vertical yet"})

    # 4. Best pattern
    patterns = []
    # Check opener style
    opener_replies = Counter(r.get("opener_style", "Unknown") for r in replies if r.get("opener_style"))
    if opener_replies:
        best_opener = opener_replies.most_common(1)[0]
        patterns.append(f"'{best_opener[0]}' openers: {best_opener[1]} replies")

    # Check ask style
    ask_replies = Counter(r.get("ask_style", "Unknown") for r in replies if r.get("ask_style"))
    if ask_replies:
        best_ask = ask_replies.most_common(1)[0]
        patterns.append(f"'{best_ask[0]}' asks: {best_ask[1]} replies")

    # Check personalization score correlation
    high_p_replies = sum(1 for r in replies if r.get("personalization_score", 0) == 3 and r.get("intent") != "negative")
    low_p_replies = sum(1 for r in replies if r.get("personalization_score", 0) == 1 and r.get("intent") != "negative")
    if high_p_replies + low_p_replies > 0:
        patterns.append(f"Score 3 personalization: {high_p_replies} replies vs Score 1: {low_p_replies}")

    brief["insights"].append({
        "label": "Best pattern",
        "value": "; ".join(patterns) if patterns else "Not enough pattern data yet"
    })

    # 5. Stop doing
    stop_items = []
    # Check for zero-reply segments
    for persona in persona_touches:
        if persona_touches[persona] >= 5 and persona_replies.get(persona, 0) == 0:
            stop_items.append(f"{persona} ({persona_touches[persona]} touches, 0 replies)")
    for v in vertical_touches:
        if vertical_touches[v] >= 5 and vertical_replies.get(v, 0) == 0:
            stop_items.append(f"{v} vertical ({vertical_touches[v]} touches, 0 replies)")

    if stop_items:
        brief["insights"].append({
            "label": "Stop doing",
            "value": f"Drop: {', '.join(stop_items[:2])}"
        })
    else:
        brief["insights"].append({
            "label": "Stop doing",
            "value": "No clear losers yet - keep testing"
        })

    # Summary line
    reply_rate = round(len(replies) / max(len(touches), 1) * 100, 1)
    brief["summary"] = f"{len(replies)} replies from {len(touches)} touches ({reply_rate}%). {len(opps)} meetings/opportunities."

    return brief


def format_pre_brief_text(brief: dict) -> str:
    """Format pre-brief as readable text for the top of a batch file."""
    lines = [f"PRE-BRIEF: {brief['summary']}", ""]
    for insight in brief.get("insights", []):
        lines.append(f"  {insight['label']}: {insight['value']}")
    return "\n".join(lines)


if __name__ == "__main__":
    brief = generate_pre_brief()
    print(format_pre_brief_text(brief))
