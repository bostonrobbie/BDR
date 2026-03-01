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

    Automatically runs:
    - Sentiment scoring (D1): scores raw_text on -1.0 to +1.0 scale
    - Contradiction detection (D2): checks reply against research artifact
      for tech_stack and role_fit contradictions

    Args:
        contact_id: The contact who replied.
        touchpoint_id: The touchpoint this reply is responding to.
        channel: Reply channel (linkedin/email/phone).
        intent: positive/neutral/negative/out_of_office/referral.
        reply_tag: Short tag (interested, not_now, unsubscribe, question, referral).
        summary: Brief summary of the reply.
        raw_text: The actual reply text.

    Returns:
        {"reply_id": str, "attribution": dict, "sentiment": dict,
         "contradictions": list, "corrections_recorded": list}
    """
    conn = models.get_db()
    reply_id = models.gen_id("rep")
    now = datetime.utcnow().isoformat()

    # D1: Auto-score sentiment from raw reply text
    sentiment = score_reply_sentiment(raw_text, existing_intent=intent)

    # Use sentiment-suggested intent if the caller passed "neutral" default
    effective_intent = intent
    if intent == "neutral" and sentiment.get("confidence", 0) >= 0.5:
        effective_intent = sentiment.get("suggested_intent", intent)

    conn.execute("""
        INSERT INTO replies (id, contact_id, touchpoint_id, channel, intent,
            reply_tag, summary, raw_text, replied_at, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (reply_id, contact_id, touchpoint_id, channel, effective_intent,
          reply_tag, summary, raw_text, now, now))
    conn.commit()

    # Build attribution by looking up the touchpoint and its message draft
    attribution = _build_attribution(conn, touchpoint_id, contact_id)

    conn.close()

    # D2: Auto-detect contradictions against the research artifact
    contradictions = []
    corrections_recorded = []
    if raw_text.strip():
        try:
            artifact = _get_latest_artifact(contact_id)
            if artifact:
                contradictions = detect_contradictions_in_reply(raw_text, artifact)
                # Auto-record corrections for high-confidence contradictions
                for c in contradictions:
                    if c.get("confidence", 0) >= 0.7:
                        correction = record_research_correction(
                            contact_id=contact_id,
                            field=c["field"],
                            original_value=c.get("our_assumption", ""),
                            corrected_value=c.get("reply_suggests", ""),
                            source="reply",
                            confidence=c["confidence"],
                        )
                        corrections_recorded.append(correction)
        except Exception:
            pass  # Don't let contradiction detection break reply recording

    return {
        "reply_id": reply_id,
        "attribution": attribution,
        "sentiment": sentiment,
        "contradictions": contradictions,
        "corrections_recorded": corrections_recorded,
    }


def _get_latest_artifact(contact_id: str) -> Optional[dict]:
    """Build a research artifact for contradiction detection.

    Uses cached contact/account data to build an artifact for
    comparing reply content against our research assumptions.
    """
    try:
        from src.agents.researcher import build_research_artifact
        contact = models.get_contact(contact_id)
        if not contact:
            return None
        account = models.get_account(contact.get("account_id", "")) if contact.get("account_id") else {}
        result = build_research_artifact(contact, account or {})
        return result.get("artifact")
    except Exception:
        return None


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
        "subject_line_style": None,
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
                    attribution["subject_line_style"] = draft.get("subject_line_style")

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
        "by_subject_style": _breakdown(touchpoints, reply_by_tp, "subject_line_style"),
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


# ─── FULL-FUNNEL ATTRIBUTION ─────────────────────────────────
# Traces the complete chain: message_draft -> touchpoint -> reply -> opportunity
# Answers: "which proof point actually books meetings?"

def get_full_funnel_attribution(contact_id: str) -> dict:
    """Build the complete attribution chain for a single contact.

    Traces every touch, reply, and outcome to show exactly which
    message attributes led to the result.

    Args:
        contact_id: The contact to trace.

    Returns:
        {"contact_id": str, "chain": [...], "outcome": str,
         "winning_attributes": {...}}
    """
    conn = models.get_db()

    # Get all touchpoints for this contact
    touchpoints = conn.execute("""
        SELECT t.*, md.proof_point_used, md.pain_hook, md.opener_style,
               md.ask_style, md.touch_type, md.ab_group, md.ab_variable,
               md.personalization_score
        FROM touchpoints t
        LEFT JOIN message_drafts md ON t.message_draft_id = md.id
        WHERE t.contact_id = ?
        ORDER BY t.sent_at ASC
    """, (contact_id,)).fetchall()

    # Get all replies
    replies = conn.execute("""
        SELECT * FROM replies WHERE contact_id = ? ORDER BY replied_at ASC
    """, (contact_id,)).fetchall()

    # Get opportunities
    opportunities = conn.execute("""
        SELECT * FROM opportunities WHERE contact_id = ? ORDER BY created_at ASC
    """, (contact_id,)).fetchall()

    conn.close()

    # Build the chain
    chain = []
    reply_lookup = {r["touchpoint_id"]: dict(r) for r in replies if r["touchpoint_id"]}

    for tp in touchpoints:
        tp_dict = dict(tp)
        link = {
            "type": "touch",
            "touch_number": tp_dict.get("touch_number"),
            "channel": tp_dict.get("channel"),
            "sent_at": tp_dict.get("sent_at"),
            "proof_point": tp_dict.get("proof_point_used"),
            "pain_hook": tp_dict.get("pain_hook"),
            "opener_style": tp_dict.get("opener_style"),
            "touch_type": tp_dict.get("touch_type"),
        }
        chain.append(link)

        # Check if this touch got a reply
        reply = reply_lookup.get(tp_dict["id"])
        if reply:
            chain.append({
                "type": "reply",
                "intent": reply.get("intent"),
                "reply_tag": reply.get("reply_tag"),
                "sentiment_score": reply.get("sentiment_score"),
                "replied_at": reply.get("replied_at"),
                "in_response_to_touch": tp_dict.get("touch_number"),
            })

    # Add opportunities
    outcome = "no_outcome"
    winning_touch = None
    for opp in opportunities:
        opp_dict = dict(opp)
        chain.append({
            "type": "outcome",
            "status": opp_dict.get("status"),
            "meeting_held": opp_dict.get("meeting_held"),
            "pipeline_value": opp_dict.get("pipeline_value"),
            "trigger_touch": opp_dict.get("attribution_touch_number"),
            "trigger_proof_point": opp_dict.get("attribution_proof_point"),
        })
        outcome = opp_dict.get("status", "meeting_booked")
        winning_touch = opp_dict.get("attribution_touch_number")

    # Determine winning attributes (from the touch that triggered the meeting)
    winning_attrs = {}
    if winning_touch:
        for tp in touchpoints:
            tp_dict = dict(tp)
            if tp_dict.get("touch_number") == winning_touch:
                winning_attrs = {
                    "proof_point": tp_dict.get("proof_point_used"),
                    "pain_hook": tp_dict.get("pain_hook"),
                    "opener_style": tp_dict.get("opener_style"),
                    "channel": tp_dict.get("channel"),
                    "touch_number": tp_dict.get("touch_number"),
                }
                break

    return {
        "contact_id": contact_id,
        "chain": chain,
        "chain_length": len(chain),
        "outcome": outcome,
        "winning_attributes": winning_attrs,
    }


def get_attribution_summary(days: int = 90) -> dict:
    """Aggregate full-funnel attribution across all contacts with outcomes.

    Returns which proof points, channels, and touch numbers actually
    convert to meetings, not just replies.

    Returns:
        {"meeting_attribution": {...}, "sample_size": int}
    """
    conn = models.get_db()
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()

    # Get all opportunities with attribution
    opps = conn.execute("""
        SELECT * FROM opportunities WHERE created_at >= ?
    """, (cutoff,)).fetchall()
    conn.close()

    by_proof_point = defaultdict(int)
    by_channel = defaultdict(int)
    by_touch_number = defaultdict(int)
    by_pain_hook = defaultdict(int)

    for opp in opps:
        opp = dict(opp)
        pp = opp.get("attribution_proof_point")
        if pp:
            by_proof_point[pp] += 1
        ch = opp.get("attribution_channel")
        if ch:
            by_channel[ch] += 1
        tn = opp.get("attribution_touch_number")
        if tn:
            by_touch_number[str(tn)] += 1
        ph = opp.get("attribution_pain_hook")
        if ph:
            by_pain_hook[ph] += 1

    return {
        "meeting_attribution": {
            "by_proof_point": dict(by_proof_point),
            "by_channel": dict(by_channel),
            "by_touch_number": dict(by_touch_number),
            "by_pain_hook": dict(by_pain_hook),
        },
        "total_meetings": len(opps),
        "period_days": days,
    }


# ─── REPLY SENTIMENT SCORING ────────────────────────────────────
# Replace ternary intent (positive/neutral/negative) with a -1 to +1
# continuous scale that distinguishes "let's schedule" from "interesting
# but not now" from "unsubscribe me."

SENTIMENT_KEYWORDS = {
    # Strong positive (+0.8 to +1.0)
    "strong_positive": {
        "keywords": ["yes", "let's schedule", "let's chat", "let's connect",
                     "interested", "love to", "sounds great", "book a time",
                     "available", "set up a call", "looking forward"],
        "score": 0.9,
    },
    # Mild positive (+0.3 to +0.7)
    "mild_positive": {
        "keywords": ["maybe", "could be", "tell me more", "send me more",
                     "share more", "good timing", "open to", "curious",
                     "worth exploring", "interesting"],
        "score": 0.5,
    },
    # Neutral (0.0)
    "neutral": {
        "keywords": ["thanks for reaching out", "noted", "received",
                     "will review", "let me think", "not sure"],
        "score": 0.0,
    },
    # Mild negative (-0.3 to -0.7)
    "mild_negative": {
        "keywords": ["not right now", "not the right time", "maybe later",
                     "busy right now", "check back", "not a priority",
                     "already have", "we use", "happy with"],
        "score": -0.5,
    },
    # Strong negative (-0.8 to -1.0)
    "strong_negative": {
        "keywords": ["not interested", "stop", "unsubscribe", "remove me",
                     "do not contact", "don't contact", "no thanks",
                     "please stop", "wrong person"],
        "score": -0.9,
    },
    # Referral (special: +0.3 for intent signal)
    "referral": {
        "keywords": ["talk to", "reach out to", "contact my colleague",
                     "try reaching", "better person", "connect you with"],
        "score": 0.3,
    },
    # Out of office (neutral but informative)
    "out_of_office": {
        "keywords": ["out of office", "ooo", "on vacation", "on leave",
                     "will be back", "return on", "away from"],
        "score": 0.0,
    },
}


def score_reply_sentiment(reply_text: str, existing_intent: str = "") -> dict:
    """Score a reply on a -1.0 to +1.0 sentiment scale.

    Goes beyond ternary intent to capture gradations:
    - +1.0: "Yes, let's book a time this week"
    - +0.5: "Interesting, tell me more"
    -  0.0: "Thanks, noted"
    - -0.5: "Not a priority right now"
    - -1.0: "Please remove me from your list"

    Args:
        reply_text: The raw reply text.
        existing_intent: The current ternary intent if already classified.

    Returns:
        {"sentiment_score": float, "sentiment_label": str,
         "matched_category": str, "confidence": float,
         "suggested_intent": str, "action": str}
    """
    text_lower = reply_text.lower().strip()

    if not text_lower:
        return {
            "sentiment_score": 0.0,
            "sentiment_label": "unknown",
            "matched_category": "none",
            "confidence": 0.0,
            "suggested_intent": existing_intent or "neutral",
            "action": "review_manually",
        }

    # Score against each category.
    # Check categories in priority order: strong signals first, then mild.
    # Within each category, check longer phrases first to avoid partial matches
    # (e.g., "maybe later" should match mild_negative before "maybe" matches mild_positive).
    best_match = None
    best_score = 0
    match_count = 0

    priority_order = [
        "strong_negative", "strong_positive", "out_of_office", "referral",
        "mild_negative", "mild_positive", "neutral",
    ]

    for category in priority_order:
        config = SENTIMENT_KEYWORDS.get(category, {})
        # Sort keywords by length descending so longer phrases match first
        keywords = sorted(config.get("keywords", []), key=len, reverse=True)
        for keyword in keywords:
            if keyword in text_lower:
                match_count += 1
                if best_match is None or abs(config["score"]) > abs(best_score):
                    best_match = category
                    best_score = config["score"]
                break  # Only count one match per category

    if best_match is None:
        # No keyword match, use existing intent as fallback
        intent_scores = {"positive": 0.5, "negative": -0.5, "neutral": 0.0,
                         "referral": 0.3, "out_of_office": 0.0}
        score = intent_scores.get(existing_intent, 0.0)
        return {
            "sentiment_score": score,
            "sentiment_label": _sentiment_label(score),
            "matched_category": "inferred_from_intent",
            "confidence": 0.3,
            "suggested_intent": existing_intent or "neutral",
            "action": "review_manually",
        }

    # Determine confidence based on match count and text length
    confidence = min(0.95, 0.5 + (match_count * 0.15))
    if len(text_lower) < 10:
        confidence = min(confidence, 0.6)  # Short replies are harder to classify

    # Map sentiment to suggested intent
    if best_score >= 0.3:
        suggested_intent = "positive"
    elif best_score <= -0.3:
        suggested_intent = "negative"
    elif best_match == "referral":
        suggested_intent = "referral"
    elif best_match == "out_of_office":
        suggested_intent = "out_of_office"
    else:
        suggested_intent = "neutral"

    # Determine recommended action
    if best_score >= 0.7:
        action = "schedule_meeting"
    elif best_score >= 0.3:
        action = "send_more_info"
    elif best_score >= -0.3:
        action = "follow_up_later"
    elif best_score >= -0.7:
        action = "pause_sequence"
    else:
        action = "mark_dnc"

    return {
        "sentiment_score": best_score,
        "sentiment_label": _sentiment_label(best_score),
        "matched_category": best_match,
        "confidence": round(confidence, 2),
        "suggested_intent": suggested_intent,
        "action": action,
    }


def _sentiment_label(score: float) -> str:
    """Convert numeric sentiment to human label."""
    if score >= 0.7:
        return "very_positive"
    if score >= 0.3:
        return "positive"
    if score >= -0.3:
        return "neutral"
    if score >= -0.7:
        return "negative"
    return "very_negative"


# ─── RESEARCH CONTRADICTION FEEDBACK ────────────────────────────
# When a prospect replies with information that contradicts our research
# (e.g., "we don't use Selenium"), this records the correction so future
# research and scoring for similar prospects can be adjusted.

def record_research_correction(contact_id: str, field: str, original_value: str,
                                corrected_value: str, source: str = "reply",
                                confidence: float = 0.9) -> dict:
    """Record a research contradiction for feedback.

    When a prospect says something that contradicts our research artifact
    (e.g., "we actually use Playwright, not Selenium"), this records the
    correction for future reference.

    Args:
        contact_id: The contact whose research needs correction.
        field: The research field being corrected (e.g., "tech_stack", "pain", "industry").
        original_value: What we thought was true.
        corrected_value: What the prospect told us.
        source: How we learned this ("reply", "call_notes", "manual").
        confidence: How confident we are in the correction (0-1).

    Returns:
        {"correction_id": str, "impact": dict}
    """
    conn = models.get_db()
    correction_id = models.gen_id("cor")
    now = datetime.utcnow().isoformat()

    # Store in audit_log as a structured correction
    conn.execute("""
        INSERT INTO audit_log (table_name, record_id, action, changed_by,
            old_values, new_values, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "research_corrections",
        contact_id,
        "correction",
        source,
        json.dumps({"field": field, "value": original_value}),
        json.dumps({"field": field, "value": corrected_value,
                    "confidence": confidence}),
        now,
    ))
    conn.commit()

    # Assess impact: how many other contacts might be affected?
    impact = _assess_correction_impact(conn, field, original_value)

    conn.close()

    return {
        "correction_id": correction_id,
        "contact_id": contact_id,
        "field": field,
        "original": original_value,
        "corrected": corrected_value,
        "source": source,
        "impact": impact,
    }


def _assess_correction_impact(conn, field: str, original_value: str) -> dict:
    """Assess how many other contacts might be affected by this correction."""
    impact = {"affected_contacts": 0, "recommendation": ""}

    if field == "tech_stack":
        # How many other contacts at this company or with this tool?
        rows = conn.execute("""
            SELECT COUNT(*) FROM accounts
            WHERE known_tools LIKE ?
        """, (f"%{original_value}%",)).fetchone()
        impact["affected_contacts"] = rows[0] if rows else 0
        if impact["affected_contacts"] > 0:
            impact["recommendation"] = (
                f"Review {impact['affected_contacts']} other accounts with "
                f"'{original_value}' in known_tools"
            )

    elif field == "pain":
        impact["recommendation"] = "Consider adjusting pain hypothesis confidence for similar prospects"

    elif field == "industry":
        rows = conn.execute("""
            SELECT COUNT(*) FROM accounts WHERE LOWER(industry) = LOWER(?)
        """, (original_value,)).fetchone()
        impact["affected_contacts"] = rows[0] if rows else 0
        if impact["affected_contacts"] > 0:
            impact["recommendation"] = (
                f"Verify industry classification for {impact['affected_contacts']} "
                f"accounts classified as '{original_value}'"
            )

    return impact


def get_research_corrections(contact_id: str = None, days: int = 90) -> list:
    """Get research corrections, optionally filtered by contact.

    Returns:
        List of correction dicts sorted by recency.
    """
    conn = models.get_db()
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()

    query = """
        SELECT * FROM audit_log
        WHERE table_name = 'research_corrections'
        AND action = 'correction'
        AND timestamp >= ?
    """
    params = [cutoff]

    if contact_id:
        query += " AND record_id = ?"
        params.append(contact_id)

    query += " ORDER BY timestamp DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()

    corrections = []
    for row in rows:
        r = dict(row)
        old = json.loads(r.get("old_values", "{}"))
        new = json.loads(r.get("new_values", "{}"))
        corrections.append({
            "contact_id": r["record_id"],
            "field": old.get("field", ""),
            "original": old.get("value", ""),
            "corrected": new.get("value", ""),
            "confidence": new.get("confidence", 0),
            "source": r.get("changed_by", ""),
            "timestamp": r.get("timestamp", ""),
        })

    return corrections


def detect_contradictions_in_reply(reply_text: str, artifact: dict) -> list:
    """Detect potential research contradictions in a reply.

    Scans the reply for statements that might contradict our research.
    Returns potential contradictions for human review.

    Args:
        reply_text: The raw reply text.
        artifact: The ResearchArtifact for this prospect.

    Returns:
        List of {"field": str, "our_assumption": str, "reply_suggests": str,
                 "confidence": float}
    """
    contradictions = []
    text_lower = reply_text.lower()

    # Check tech stack contradictions
    tech_stack = artifact.get("signals", {}).get("tech_stack", [])
    for item in tech_stack:
        tool = item.get("value", "") if isinstance(item, dict) else str(item)
        tool_lower = tool.lower()

        # "We don't use X" pattern
        negation_patterns = [
            f"don't use {tool_lower}", f"do not use {tool_lower}",
            f"not using {tool_lower}", f"stopped using {tool_lower}",
            f"moved away from {tool_lower}", f"migrated from {tool_lower}",
            f"no longer use {tool_lower}",
        ]
        if any(pattern in text_lower for pattern in negation_patterns):
            contradictions.append({
                "field": "tech_stack",
                "our_assumption": f"Uses {tool}",
                "reply_suggests": f"Does not use {tool}",
                "confidence": 0.8,
            })

        # "We actually use Y (not X)" pattern
        competitor_tools = ["selenium", "cypress", "playwright", "tosca",
                           "katalon", "testim", "mabl"]
        for other_tool in competitor_tools:
            if other_tool != tool_lower and other_tool in text_lower:
                if f"we use {other_tool}" in text_lower or f"using {other_tool}" in text_lower:
                    contradictions.append({
                        "field": "tech_stack",
                        "our_assumption": f"Uses {tool}",
                        "reply_suggests": f"Actually uses {other_tool.title()}",
                        "confidence": 0.7,
                    })

    # Check role/responsibility contradictions
    if any(phrase in text_lower for phrase in ["wrong person", "not my area",
                                                "don't handle", "not responsible",
                                                "try reaching"]):
        contradictions.append({
            "field": "role_fit",
            "our_assumption": f"Responsible for test automation decisions",
            "reply_suggests": "May not be the right contact",
            "confidence": 0.7,
        })

    return contradictions


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


# ─── F10: LLM-ASSISTED PAIN REFINEMENT ──────────────────────────
# When a reply reveals new information about the prospect's actual
# pain points, we can use the LLM to refine the research artifact's
# pain hypotheses rather than just flagging the correction.


def refine_pains_from_reply(contact_id: str, reply_text: str,
                             artifact: dict = None,
                             use_llm: bool = False) -> dict:
    """Refine pain hypotheses based on reply content.

    Uses keyword extraction and optional LLM refinement to update
    the artifact's pain hypotheses with information gleaned from
    the prospect's reply.

    Args:
        contact_id: The contact who replied.
        reply_text: The reply text to analyze.
        artifact: Existing research artifact (loaded if None).
        use_llm: Whether to use the LLM for deeper refinement.

    Returns:
        {"original_pains": list, "refined_pains": list,
         "new_signals": list, "llm_used": bool}
    """
    if not reply_text.strip():
        return {"original_pains": [], "refined_pains": [],
                "new_signals": [], "llm_used": False}

    # Load artifact if not provided
    if artifact is None:
        artifact = _get_latest_artifact(contact_id)
    if not artifact:
        return {"original_pains": [], "refined_pains": [],
                "new_signals": [], "llm_used": False}

    original_pains = artifact.get("pains", {}).get("hypothesized_pains", [])
    text_lower = reply_text.lower()

    # Extract new signals from reply text
    new_signals = _extract_signals_from_reply(text_lower)

    # Refine existing pains based on reply content
    refined_pains = _rule_based_pain_refinement(original_pains, text_lower, new_signals)

    # Optionally use LLM for deeper refinement
    llm_used = False
    if use_llm and reply_text.strip():
        llm_refined = _llm_refine_pains(original_pains, reply_text, artifact)
        if llm_refined:
            refined_pains = llm_refined
            llm_used = True

    # Record the refined pains as a research correction if they changed
    if refined_pains != original_pains:
        for rp in refined_pains:
            if rp not in original_pains:
                record_research_correction(
                    contact_id=contact_id,
                    field="pain_hypothesis",
                    original_value=json.dumps(original_pains[:1]) if original_pains else "[]",
                    corrected_value=json.dumps(rp),
                    source="reply_refinement",
                    confidence=rp.get("confidence", 0.5),
                )

    return {
        "original_pains": original_pains,
        "refined_pains": refined_pains,
        "new_signals": new_signals,
        "llm_used": llm_used,
    }


def _extract_signals_from_reply(text_lower: str) -> list:
    """Extract actionable signals from reply text.

    Looks for mentions of tools, processes, pain points, team size,
    and other contextual clues.
    """
    signals = []

    # Tool mentions
    tool_keywords = {
        "selenium": "test_tool", "cypress": "test_tool", "playwright": "test_tool",
        "tosca": "test_tool", "katalon": "test_tool", "testim": "test_tool",
        "jest": "test_tool", "junit": "test_tool", "pytest": "test_tool",
        "jenkins": "ci_tool", "github actions": "ci_tool", "gitlab ci": "ci_tool",
        "circleci": "ci_tool", "azure devops": "ci_tool",
    }
    for tool, sig_type in tool_keywords.items():
        if tool in text_lower:
            signals.append({"type": sig_type, "value": tool, "source": "reply"})

    # Pain-related keywords
    pain_indicators = {
        "flaky": "flaky_tests", "brittle": "flaky_tests", "unstable": "flaky_tests",
        "maintenance": "maintenance_overhead", "maintaining": "maintenance_overhead",
        "slow": "slow_cycles", "takes forever": "slow_cycles",
        "manual": "manual_testing", "manually": "manual_testing",
        "coverage": "coverage_gaps", "gaps in": "coverage_gaps",
        "hiring": "team_scaling", "headcount": "team_scaling",
    }
    for keyword, pain_type in pain_indicators.items():
        if keyword in text_lower:
            signals.append({"type": "pain_signal", "value": pain_type, "source": "reply"})

    # Process mentions
    if any(w in text_lower for w in ["sprint", "agile", "scrum", "kanban"]):
        signals.append({"type": "process", "value": "agile", "source": "reply"})
    if any(w in text_lower for w in ["waterfall", "release train", "quarterly"]):
        signals.append({"type": "process", "value": "structured_releases", "source": "reply"})

    return signals


def _rule_based_pain_refinement(original_pains: list, text_lower: str,
                                 new_signals: list) -> list:
    """Refine pain hypotheses using rule-based analysis of reply content.

    - Confirms pains mentioned in the reply (boost confidence)
    - Downgrades pains contradicted by the reply
    - Adds new pains revealed in the reply
    """
    refined = []
    pain_types_from_signals = {s["value"] for s in new_signals if s["type"] == "pain_signal"}

    for pain in original_pains:
        p = dict(pain)
        pain_lower = p.get("pain", "").lower()

        # Check if pain is confirmed by reply
        confirmed = False
        if "maintenance" in pain_lower and "maintenance_overhead" in pain_types_from_signals:
            confirmed = True
        elif "flaky" in pain_lower and "flaky_tests" in pain_types_from_signals:
            confirmed = True
        elif "scaling" in pain_lower and "team_scaling" in pain_types_from_signals:
            confirmed = True
        elif "manual" in pain_lower and "manual_testing" in pain_types_from_signals:
            confirmed = True
        elif "coverage" in pain_lower and "coverage_gaps" in pain_types_from_signals:
            confirmed = True

        if confirmed:
            p["confidence"] = min(1.0, p.get("confidence", 0.5) + 0.2)
            p["evidence"] = f"{p.get('evidence', '')}; confirmed by prospect reply"
        elif any(neg in text_lower for neg in ["not a problem", "not an issue",
                                                 "don't have that", "that's not"]):
            # Check if this specific pain is being denied
            pain_words = set(pain_lower.split())
            denied_overlap = sum(1 for w in pain_words if w in text_lower and len(w) > 3)
            if denied_overlap >= 2:
                p["confidence"] = max(0.1, p.get("confidence", 0.5) - 0.3)
                p["evidence"] = f"{p.get('evidence', '')}; contradicted by prospect reply"

        refined.append(p)

    # Add new pains from signals not already covered
    existing_pain_types = set()
    for p in refined:
        pl = p.get("pain", "").lower()
        if "maintenance" in pl:
            existing_pain_types.add("maintenance_overhead")
        if "flaky" in pl:
            existing_pain_types.add("flaky_tests")
        if "manual" in pl:
            existing_pain_types.add("manual_testing")

    new_pain_map = {
        "flaky_tests": "Flaky tests impacting CI/CD reliability",
        "maintenance_overhead": "Test maintenance overhead growing with the codebase",
        "slow_cycles": "Slow test execution cycles bottlenecking releases",
        "manual_testing": "Manual testing consuming too much team bandwidth",
        "coverage_gaps": "Gaps in test coverage creating risk",
        "team_scaling": "Scaling QA capacity without proportional headcount growth",
    }

    for sig in new_signals:
        if sig["type"] == "pain_signal" and sig["value"] not in existing_pain_types:
            pain_text = new_pain_map.get(sig["value"])
            if pain_text:
                refined.append({
                    "pain": pain_text,
                    "confidence": 0.7,
                    "evidence": "from prospect reply",
                })
                existing_pain_types.add(sig["value"])

    return refined


def _llm_refine_pains(original_pains: list, reply_text: str,
                       artifact: dict) -> Optional[list]:
    """Use LLM to refine pain hypotheses from reply content.

    Falls back to None if the LLM is unavailable, allowing the caller
    to use rule-based refinement instead.
    """
    try:
        from src.agents.llm_gateway import get_llm_client
        client = get_llm_client()
        if not client or not client.is_healthy():
            return None

        prospect = artifact.get("prospect", {})
        company = prospect.get("company_name", "unknown")
        title = prospect.get("title", "unknown")

        prompt = f"""Analyze this prospect reply and refine the pain hypotheses.

PROSPECT: {title} at {company}
REPLY TEXT: {reply_text}

CURRENT PAIN HYPOTHESES:
{json.dumps(original_pains, indent=2)}

INSTRUCTIONS:
1. If the reply confirms any existing pain, boost its confidence to 0.8-0.9
2. If the reply contradicts a pain, lower its confidence to 0.1-0.3
3. If the reply reveals new pains not in the list, add them with confidence 0.7
4. Keep the evidence field updated with "confirmed/contradicted/added from reply"

Return ONLY a valid JSON array of pain hypothesis objects.
Each object must have: "pain" (string), "confidence" (float 0-1), "evidence" (string)
"""

        response = client.generate(prompt, max_tokens=1000)
        if not response:
            return None

        # Parse JSON from response
        text = response.strip()
        # Find JSON array in the response
        start = text.find("[")
        end = text.rfind("]") + 1
        if start >= 0 and end > start:
            parsed = json.loads(text[start:end])
            # Validate structure
            if isinstance(parsed, list) and all(
                isinstance(p, dict) and "pain" in p and "confidence" in p
                for p in parsed
            ):
                return parsed

    except Exception:
        pass

    return None
