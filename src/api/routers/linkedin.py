"""LinkedIn channel routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.db import models

router = APIRouter(prefix="/api/linkedin", tags=["linkedin"])


class LinkedInEventLog(BaseModel):
    contact_id: str
    event_type: str
    details: Optional[str] = None


@router.get("/health")
def linkedin_health():
    return models.get_linkedin_health()


@router.get("/pacing")
def linkedin_pacing(daily_limit: int = 25):
    return models.check_linkedin_pacing(daily_limit)


@router.post("/events")
def log_linkedin_event(req: LinkedInEventLog):
    return models.log_linkedin_event(req.contact_id, req.event_type, req.details)


@router.get("/sequence/{contact_id}")
def get_linkedin_sequence(contact_id: str):
    contact = models.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    conn = models.get_db()

    touchpoints = conn.execute("""
        SELECT tp.*, md.touch_number, md.subject_line, md.body
        FROM touchpoints tp
        LEFT JOIN message_drafts md ON tp.message_draft_id = md.id
        WHERE tp.contact_id=? AND tp.channel='linkedin'
        ORDER BY md.touch_number ASC
    """, (contact_id,)).fetchall()

    followups = conn.execute("""
        SELECT * FROM followups
        WHERE contact_id=? AND channel='linkedin' AND state='pending'
        ORDER BY touch_number ASC
    """, (contact_id,)).fetchall()

    messages = conn.execute("""
        SELECT * FROM message_drafts
        WHERE contact_id=? AND channel='linkedin'
        ORDER BY touch_number ASC
    """, (contact_id,)).fetchall()

    replies = conn.execute("""
        SELECT * FROM replies
        WHERE contact_id=? AND channel='linkedin'
        ORDER BY replied_at DESC
    """, (contact_id,)).fetchall()

    conn.close()

    return {
        "contact_id": contact_id,
        "contact_name": f"{contact.get('first_name', '')} {contact.get('last_name', '')}",
        "company": contact.get("company_name", ""),
        "linkedin_url": contact.get("linkedin_url", ""),
        "touchpoints_sent": [dict(tp) for tp in touchpoints],
        "pending_followups": [dict(fu) for fu in followups],
        "all_messages": [dict(m) for m in messages],
        "replies_received": [dict(r) for r in replies],
        "sequence_summary": {
            "touches_sent": len(touchpoints),
            "pending_touches": len(followups),
            "total_messages_drafted": len(messages),
            "replies_count": len(replies),
            "latest_reply": dict(replies[0]) if replies else None,
        }
    }
