"""
Outreach Command Center - Response Tracking & Feedback Loop
Tracks which message attributes (tone, proof point, CTA, pain hook, opener style)
drive responses, and feeds winning patterns back into the pipeline.

Data flow:
1. RECORD: When a reply comes in, link it to the message attributes that generated it
2. ANALYZE: Compute conversion rates by tone, proof point, CTA, pain hook, etc.
3. RECOMMEND: Feed winning patterns back to the message writer for future prospects

Tables used:
- touchpoints: outbound touches with message_draft_id
- replies: inbound replies with intent classification
- message_drafts: the message attributes (tone, proof_point, pain_hook, etc.)
- opportunities: meetings/deals for full-funnel attribution
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Optional
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.db import models


# ─── RESPONSE RECORDING ──────────────────────────────────────

def record_reply(contact_id: str, touchpoint_id: str = None,
                 channel: str = "linkedin",
                 intent: str = "neutral",
                 reply_tag: str = "",
                 summary: str = "",
                 raw_text: str = "") -> dict:
    """Record a prospect reply and link it to the message that triggered it.

    Args:
        contact_id: The contact who replied.
        touchpoint_id: The touchpoint this reply is responding to.
        channel: Reply channel (linkedin/email/phone).
        intent: positive/neutral/negative/out_of_office/referral.
        reply_tag: Short tag (interested, not_now, unsubscribe, question, referral).
        summary: Brief summary of the reply.
        raw_text: The actual reply text.

    Returns:
        {"reply_id": str, "attribution": dict}
    """
    conn = models.get_db()
    reply_id = models.gen_id("rep")
    now = datetime.utcnow().isoformat()

    conn.execute("""
        INSERT INTO replies (id, contact_id, touchpoint_id, channel, intent,
            reply_tag, summary, raw_text, replied_at, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (reply_id, contact_id, touchpoint_id, channel, intent,
          reply_tag, summary, raw_text, now, now))
    conn.commit()

    # Build attribution by looking up the touchpoint and its message draft
    attribution = _build_attribution(conn, touchpoint_id, contact_id)

    conn.close()

    return {
        "reply_id": reply_id,
        "attribution": attribution,
    }


def _build_attribution(conn, touchpoint_id: str = None,
                        contact_id: str = None) -> dict:
    """Build attribution data linking a reply to message attributes."""
    attribution = {
        "tone": None,
        "proof_point_used": None,
        "pain_hook": None,
        "opener_style": None,
        "ask_style": None,
        "channel": None,
        "touch_number": None,
        "ab_group": None,
        "ab_variable": None,
        "personalization_score": None,
    }

    if touchpoint_id:
        tp = conn.execute("SELECT * FROM touchpoints WHERE id=?",
                          (touchpoint_id,)).fetchone()
        if tp:
            tp = dict(tp)
            attribution["channel"] = tp.get("channel")
            attribution["touch_number"] = tp.get("touch_number")

            # Get the message draft for full attribute data
            draft_id = tp.get("message_draft_id")
            if draft_id:
                draft = conn.execute("SELECT * FROM message_drafts WHERE id=?",
                                     (draft_id,)).fetchone()
                if draft:
                    draft = dict(draft)
                    attribution["proof_point_used"] = draft.get("proof_point_used")
                    attribution["pain_hook"] = draft.get("pain_hook")
                    attribution["opener_style"] = draft.get("opener_style")
                    attribution["ask_style"] = draft.get("ask_style")
                    attribution["ab_group"] = draft.get("ab_group")
                    attribution["ab_variable"] = draft.get("ab_variable")
                    attribution["personalization_score"] = draft.get("personalization_score")

    elif contact_id:
        # Fallback: find the most recent touchpoint for this contact
        tp = conn.execute("""
            SELECT * FROM touchpoints
            WHERE contact_id=? ORDER BY sent_at DESC LIMIT 1
        """, (contact_id,)).fetchone()
        if tp:
            return _build_attribution(conn, dict(tp)["id"], contact_id)

    return attribution


def record_meeting(contact_id: str, meeting_date: str = None,
                   trigger_touchpoint_id: str = None,
                   trigger_reply_id: str = None,
                   pipeline_value: float = None,
                   ae_name: str = "",
                   notes: str = "") -> dict:
    """Record a meeting/opportunity and attribute it to the outreach that caused it.

    Args:
        contact_id: The contact the meeting is with.
        meeting_date: ISO date string.
        trigger_touchpoint_id: The touchpoint that led to the meeting.
        trigger_reply_id: The reply that led to the meeting.
        pipeline_value: Dollar value of opportunity.
        ae_name: Account Executive name.
        notes: Additional notes.

    Returns:
        {"opportunity_id": str, "attribution": dict}
    """
    conn = models.get_db()
    opp_id = models.gen_id("opp")
    now = datetime.utcnow().isoformat()

    # Build full attribution
    attribution = _build_attribution(conn, trigger_touchpoint_id, contact_id)

    conn.execute("""
        INSERT INTO opportunities (id, contact_id, meeting_date, meeting_held,
            status, pipeline_value, trigger_touchpoint_id, trigger_reply_id,
            attribution_channel, attribution_touch_number,
            attribution_proof_point, attribution_pain_hook,
            attribution_opener_style, attribution_personalization_score,
            attribution_ab_group, attribution_ab_variable,
            ae_name, notes, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        opp_id, contact_id, meeting_date or now, 0,
        "meeting_booked", pipeline_value, trigger_touchpoint_id,
        trigger_reply_id,
        attribution.get("channel"),
        attribution.get("touch_number"),
        attribution.get("proof_point_used"),
        attribution.get("pain_hook"),
        attribution.get("opener_style"),
        attribution.get("personalization_score"),
        attribution.get("ab_group"),
        attribution.get("ab_variable"),
        ae_name, notes, now,
    ))
    conn.commit()
    conn.close()

    return {
        "opportunity_id": opp_id,
        "attribution": attribution,
    }


# ─── ANALYTICS ─────────────────────────────────────────────────

def get_conversion_stats(days: int = 90) -> dict:
    """Get conversion rates broken down by message attributes.

    Returns stats for: tone, proof point, pain hook, channel, touch number,
    opener style, and A/B groups.

    Args:
        days: Look-back window in days.

    Returns:
        {"by_proof_point": {...}, "by_channel": {...}, "by_touch_number": {...},
         "by_opener_style": {...}, "by_ab_group": {...},
         "totals": {...}, "period_days": int}
    """
    conn = models.get_db()
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()

    # Get all touchpoints in the period
    touchpoints = conn.execute("""
        SELECT t.*, md.proof_point_used, md.pain_hook, md.opener_style,
               md.ask_style, md.ab_group, md.ab_variable,
               md.personalization_score, md.touch_type
        FROM touchpoints t
        LEFT JOIN message_drafts md ON t.message_draft_id = md.id
        WHERE t.sent_at >= ?
    """, (cutoff,)).fetchall()
    touchpoints = [dict(r) for r in touchpoints]

    # Get all replies in the period
    replies = conn.execute("""
        SELECT r.*, t.contact_id as tp_contact_id
        FROM replies r
        LEFT JOIN touchpoints t ON r.touchpoint_id = t.id
        WHERE r.replied_at >= ?
    """, (cutoff,)).fetchall()
    replies = [dict(r) for r in replies]

    # Get meetings in the period
    meetings = conn.execute("""
        SELECT * FROM opportunities WHERE created_at >= ?
    """, (cutoff,)).fetchall()
    meetings = [dict(r) for r in meetings]

    conn.close()

    # Build reply lookup by touchpoint_id
    reply_by_tp = {}
    for r in replies:
        tp_id = r.get("touchpoint_id")
        if tp_id:
            reply_by_tp[tp_id] = r

    # Positive reply contacts
    positive_reply_contacts = set()
    for r in replies:
        if r.get("intent") in ("positive", "referral"):
            cid = r.get("contact_id") or r.get("tp_contact_id")
            if cid:
                positive_reply_contacts.add(cid)

    # Meeting contacts
    meeting_contacts = set()
    for m in meetings:
        cid = m.get("contact_id")
        if cid:
            meeting_contacts.add(cid)

    # Compute breakdowns
    stats = {
        "by_proof_point": _breakdown(touchpoints, reply_by_tp, "proof_point_used"),
        "by_channel": _breakdown(touchpoints, reply_by_tp, "channel"),
        "by_touch_number": _breakdown(touchpoints, reply_by_tp, "touch_number"),
        "by_opener_style": _breakdown(touchpoints, reply_by_tp, "opener_style"),
        "by_ab_group": _breakdown(touchpoints, reply_by_tp, "ab_group"),
        "totals": {
            "touches_sent": len(touchpoints),
            "replies_received": len(replies),
            "positive_replies": len([r for r in replies if r.get("intent") in ("positive", "referral")]),
            "meetings_booked": len(meetings),
            "reply_rate": _safe_rate(len(replies), len(touchpoints)),
            "positive_rate": _safe_rate(
                len([r for r in replies if r.get("intent") in ("positive", "referral")]),
                len(touchpoints)),
            "meeting_rate": _safe_rate(len(meetings), len(touchpoints)),
        },
        "period_days": days,
    }

    return stats


def _breakdown(touchpoints: list, reply_by_tp: dict, field: str) -> dict:
    """Compute sent/replied/rate breakdown for a given field."""
    buckets = defaultdict(lambda: {"sent": 0, "replied": 0, "positive": 0})

    for tp in touchpoints:
        value = tp.get(field)
        if value is None or value == "":
            value = "(unknown)"
        value = str(value)
        buckets[value]["sent"] += 1

        tp_id = tp.get("id")
        if tp_id and tp_id in reply_by_tp:
            buckets[value]["replied"] += 1
            if reply_by_tp[tp_id].get("intent") in ("positive", "referral"):
                buckets[value]["positive"] += 1

    # Compute rates
    result = {}
    for value, counts in buckets.items():
        result[value] = {
            "sent": counts["sent"],
            "replied": counts["replied"],
            "positive": counts["positive"],
            "reply_rate": _safe_rate(counts["replied"], counts["sent"]),
            "positive_rate": _safe_rate(counts["positive"], counts["sent"]),
        }

    # Sort by positive_rate desc
    result = dict(sorted(result.items(),
                         key=lambda x: x[1]["positive_rate"],
                         reverse=True))
    return result


def _safe_rate(numerator: int, denominator: int) -> float:
    """Compute a rate safely, returning 0.0 if denominator is 0."""
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)


# ─── WINNING PATTERNS ────────────────────────────────────────

def get_winning_patterns(min_sample_size: int = 5, days: int = 90) -> dict:
    """Identify which message attributes are performing best.

    Returns recommendations for proof point, channel, touch number,
    and opener style based on actual conversion data.

    Args:
        min_sample_size: Minimum touches to consider a pattern significant.
        days: Look-back window.

    Returns:
        {"recommendations": [...], "top_proof_point": str|None,
         "top_channel": str|None, "top_touch_number": int|None,
         "sample_size": int, "confidence": str}
    """
    stats = get_conversion_stats(days)
    recommendations = []

    total_sent = stats["totals"]["touches_sent"]
    confidence = "high" if total_sent >= 50 else "medium" if total_sent >= 20 else "low"

    # Best proof point
    top_pp = _find_winner(stats["by_proof_point"], min_sample_size)
    if top_pp:
        recommendations.append({
            "dimension": "proof_point",
            "winner": top_pp["key"],
            "positive_rate": top_pp["positive_rate"],
            "sample_size": top_pp["sent"],
            "recommendation": f"Prefer '{top_pp['key']}' proof point ({top_pp['positive_rate']:.0%} positive rate, n={top_pp['sent']})",
        })

    # Best channel
    top_ch = _find_winner(stats["by_channel"], min_sample_size)
    if top_ch:
        recommendations.append({
            "dimension": "channel",
            "winner": top_ch["key"],
            "positive_rate": top_ch["positive_rate"],
            "sample_size": top_ch["sent"],
            "recommendation": f"'{top_ch['key']}' channel performs best ({top_ch['positive_rate']:.0%} positive rate, n={top_ch['sent']})",
        })

    # Best touch number
    top_tn = _find_winner(stats["by_touch_number"], min_sample_size)
    if top_tn:
        recommendations.append({
            "dimension": "touch_number",
            "winner": top_tn["key"],
            "positive_rate": top_tn["positive_rate"],
            "sample_size": top_tn["sent"],
            "recommendation": f"Touch {top_tn['key']} has highest conversion ({top_tn['positive_rate']:.0%} positive rate, n={top_tn['sent']})",
        })

    # Best opener style
    top_os = _find_winner(stats["by_opener_style"], min_sample_size)
    if top_os:
        recommendations.append({
            "dimension": "opener_style",
            "winner": top_os["key"],
            "positive_rate": top_os["positive_rate"],
            "sample_size": top_os["sent"],
            "recommendation": f"'{top_os['key']}' opener style wins ({top_os['positive_rate']:.0%} positive rate, n={top_os['sent']})",
        })

    return {
        "recommendations": recommendations,
        "top_proof_point": top_pp["key"] if top_pp else None,
        "top_channel": top_ch["key"] if top_ch else None,
        "top_touch_number": top_tn["key"] if top_tn else None,
        "sample_size": total_sent,
        "confidence": confidence,
        "stats": stats,
    }


def _find_winner(breakdown: dict, min_sample: int) -> Optional[dict]:
    """Find the best-performing bucket in a breakdown, if significant."""
    candidates = []
    for key, data in breakdown.items():
        if key == "(unknown)":
            continue
        if data["sent"] >= min_sample:
            candidates.append({
                "key": key,
                "positive_rate": data["positive_rate"],
                "reply_rate": data["reply_rate"],
                "sent": data["sent"],
                "positive": data["positive"],
            })

    if not candidates:
        return None

    # Sort by positive_rate desc, then reply_rate desc
    candidates.sort(key=lambda x: (x["positive_rate"], x["reply_rate"]), reverse=True)
    return candidates[0]


# ─── FEEDBACK-INFORMED PROOF POINT SELECTION ──────────────────

def get_proof_point_preference(vertical: str = "",
                                known_tools: list = None,
                                min_sample: int = 5,
                                days: int = 90) -> Optional[str]:
    """Get the best proof point based on actual performance data.

    If we have enough data, returns the proof point with the highest
    positive reply rate. Falls back to None if insufficient data.

    This can be used by the message writer to bias proof point selection
    toward what's actually working.

    Args:
        vertical: Company vertical (for future per-vertical analysis).
        known_tools: Known competitor tools (for future per-tool analysis).
        min_sample: Minimum sample size to trust the data.
        days: Look-back window.

    Returns:
        Proof point key string, or None if insufficient data.
    """
    stats = get_conversion_stats(days)
    pp_stats = stats.get("by_proof_point", {})

    best = _find_winner(pp_stats, min_sample)
    if best and best["positive_rate"] > 0:
        return best["key"]

    return None


def generate_feedback_report(days: int = 90) -> str:
    """Generate a human-readable feedback report.

    Returns a formatted string with key performance insights.
    """
    patterns = get_winning_patterns(min_sample_size=3, days=days)
    stats = patterns["stats"]
    totals = stats["totals"]

    lines = []
    lines.append(f"=== OUTREACH PERFORMANCE REPORT ({days}-day window) ===")
    lines.append("")
    lines.append(f"Total touches: {totals['touches_sent']}")
    lines.append(f"Replies: {totals['replies_received']} ({totals['reply_rate']:.1%} rate)")
    lines.append(f"Positive replies: {totals['positive_replies']} ({totals['positive_rate']:.1%} rate)")
    lines.append(f"Meetings booked: {totals['meetings_booked']} ({totals['meeting_rate']:.1%} rate)")
    lines.append(f"Confidence: {patterns['confidence']}")
    lines.append("")

    if patterns["recommendations"]:
        lines.append("--- WINNING PATTERNS ---")
        for rec in patterns["recommendations"]:
            lines.append(f"  {rec['recommendation']}")
        lines.append("")

    # Proof point breakdown
    if stats["by_proof_point"]:
        lines.append("--- PROOF POINT PERFORMANCE ---")
        for pp, data in stats["by_proof_point"].items():
            if data["sent"] > 0:
                lines.append(
                    f"  {pp:30s}  sent={data['sent']:3d}  "
                    f"replied={data['replied']:3d}  "
                    f"positive={data['positive']:3d}  "
                    f"rate={data['positive_rate']:.0%}")
        lines.append("")

    # Channel breakdown
    if stats["by_channel"]:
        lines.append("--- CHANNEL PERFORMANCE ---")
        for ch, data in stats["by_channel"].items():
            if data["sent"] > 0:
                lines.append(
                    f"  {ch:15s}  sent={data['sent']:3d}  "
                    f"replied={data['replied']:3d}  "
                    f"rate={data['reply_rate']:.0%}")
        lines.append("")

    return "\n".join(lines)
