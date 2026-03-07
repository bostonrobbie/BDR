"""
Outreach Analytics Engine - Aggregates data across batches for reporting.

Provides reply rates by persona, vertical, proof point, personalization score,
and A/B test results. Powers the outreach-dashboard.html and the pre-brief.

Usage:
    from src.agents.analytics import get_analytics_summary

    summary = get_analytics_summary()
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.db import models


def get_reply_rates_by_persona() -> list:
    """Reply rates grouped by persona type (QA Manager, VP Eng, etc.)."""
    conn = models.get_db()
    rows = conn.execute("""
        SELECT c.persona_type,
               COUNT(DISTINCT c.id) as total,
               COUNT(DISTINCT CASE WHEN bp.status IN ('replied', 'meeting_booked', 're-engaged')
                     THEN c.id END) as replied
        FROM contacts c
        JOIN batch_prospects bp ON bp.contact_id = c.id
        WHERE c.persona_type IS NOT NULL AND c.persona_type != ''
        GROUP BY c.persona_type
        ORDER BY total DESC
    """).fetchall()
    conn.close()

    return [{
        "persona": r["persona_type"],
        "total": r["total"],
        "replied": r["replied"],
        "reply_rate": round(r["replied"] / r["total"], 4) if r["total"] else 0.0,
    } for r in rows]


def get_reply_rates_by_vertical() -> list:
    """Reply rates grouped by company vertical/industry."""
    conn = models.get_db()
    rows = conn.execute("""
        SELECT c.company_industry,
               COUNT(DISTINCT c.id) as total,
               COUNT(DISTINCT CASE WHEN bp.status IN ('replied', 'meeting_booked', 're-engaged')
                     THEN c.id END) as replied
        FROM contacts c
        JOIN batch_prospects bp ON bp.contact_id = c.id
        WHERE c.company_industry IS NOT NULL AND c.company_industry != ''
        GROUP BY c.company_industry
        ORDER BY total DESC
    """).fetchall()
    conn.close()

    return [{
        "vertical": r["company_industry"],
        "total": r["total"],
        "replied": r["replied"],
        "reply_rate": round(r["replied"] / r["total"], 4) if r["total"] else 0.0,
    } for r in rows]


def get_reply_rates_by_proof_point() -> list:
    """Reply rates grouped by proof point used in Touch 1."""
    conn = models.get_db()
    rows = conn.execute("""
        SELECT md.proof_point_used,
               COUNT(DISTINCT md.contact_id) as total,
               COUNT(DISTINCT CASE WHEN bp.status IN ('replied', 'meeting_booked', 're-engaged')
                     THEN md.contact_id END) as replied
        FROM message_drafts md
        JOIN batch_prospects bp ON bp.contact_id = md.contact_id AND bp.batch_id = md.batch_id
        WHERE md.touch_number = 1
              AND md.proof_point_used IS NOT NULL AND md.proof_point_used != ''
        GROUP BY md.proof_point_used
        ORDER BY total DESC
    """).fetchall()
    conn.close()

    return [{
        "proof_point": r["proof_point_used"],
        "total": r["total"],
        "replied": r["replied"],
        "reply_rate": round(r["replied"] / r["total"], 4) if r["total"] else 0.0,
    } for r in rows]


def get_reply_rates_by_personalization_score() -> list:
    """Reply rates grouped by personalization score (1-3)."""
    conn = models.get_db()
    rows = conn.execute("""
        SELECT md.personalization_score,
               COUNT(DISTINCT md.contact_id) as total,
               COUNT(DISTINCT CASE WHEN bp.status IN ('replied', 'meeting_booked', 're-engaged')
                     THEN md.contact_id END) as replied
        FROM message_drafts md
        JOIN batch_prospects bp ON bp.contact_id = md.contact_id AND bp.batch_id = md.batch_id
        WHERE md.touch_number = 1
              AND md.personalization_score IS NOT NULL
        GROUP BY md.personalization_score
        ORDER BY md.personalization_score
    """).fetchall()
    conn.close()

    return [{
        "score": r["personalization_score"],
        "total": r["total"],
        "replied": r["replied"],
        "reply_rate": round(r["replied"] / r["total"], 4) if r["total"] else 0.0,
    } for r in rows]


def get_batch_trend() -> list:
    """Reply rate trend across batches over time."""
    conn = models.get_db()
    rows = conn.execute("""
        SELECT b.batch_number, b.created_at,
               COUNT(DISTINCT bp.contact_id) as total,
               COUNT(DISTINCT CASE WHEN bp.status IN ('replied', 'meeting_booked', 're-engaged')
                     THEN bp.contact_id END) as replied
        FROM batches b
        JOIN batch_prospects bp ON bp.batch_id = b.id
        GROUP BY b.batch_number
        ORDER BY b.batch_number
    """).fetchall()
    conn.close()

    return [{
        "batch": r["batch_number"],
        "date": r["created_at"],
        "total": r["total"],
        "replied": r["replied"],
        "reply_rate": round(r["replied"] / r["total"], 4) if r["total"] else 0.0,
    } for r in rows]


def get_top_messages(limit: int = 5) -> list:
    """Get top-performing messages (ones that led to replies)."""
    conn = models.get_db()
    rows = conn.execute("""
        SELECT md.contact_id, md.subject_line, md.body, md.proof_point_used,
               md.personalization_score, md.opener_style, md.pain_hook,
               c.first_name, c.last_name, c.title, c.company_name
        FROM message_drafts md
        JOIN batch_prospects bp ON bp.contact_id = md.contact_id AND bp.batch_id = md.batch_id
        JOIN contacts c ON c.id = md.contact_id
        WHERE bp.status IN ('replied', 'meeting_booked')
              AND md.touch_number = 1
        ORDER BY md.personalization_score DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()

    return [dict(r) for r in rows]


def get_analytics_summary() -> dict:
    """Full analytics summary for the dashboard."""
    return {
        "by_persona": get_reply_rates_by_persona(),
        "by_vertical": get_reply_rates_by_vertical(),
        "by_proof_point": get_reply_rates_by_proof_point(),
        "by_personalization_score": get_reply_rates_by_personalization_score(),
        "batch_trend": get_batch_trend(),
        "top_messages": get_top_messages(),
    }
