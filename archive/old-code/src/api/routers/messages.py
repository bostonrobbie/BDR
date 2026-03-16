"""Message draft routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.db import models

router = APIRouter(prefix="/api/messages", tags=["messages"])


class MessageDraftCreate(BaseModel):
    contact_id: str
    batch_id: Optional[str] = None
    channel: str
    touch_number: Optional[int] = None
    touch_type: str
    subject_line: Optional[str] = None
    body: str
    personalization_score: Optional[int] = None
    proof_point_used: Optional[str] = None
    pain_hook: Optional[str] = None
    opener_style: Optional[str] = None
    ask_style: Optional[str] = None
    ab_group: Optional[str] = None
    ab_variable: Optional[str] = None


class MessageEditRequest(BaseModel):
    body: Optional[str] = None
    subject_line: Optional[str] = None
    approval_status: Optional[str] = None


@router.post("")
def create_message(msg: MessageDraftCreate):
    data = msg.model_dump()
    data["word_count"] = len(data["body"].split())
    return models.create_message_draft(data)


@router.get("")
def list_messages(batch_id: str = None, channel: str = None,
                  approval_status: str = None, limit: int = 100):
    return models.list_messages(batch_id=batch_id, channel=channel,
                                approval_status=approval_status, limit=limit)


@router.patch("/{message_id}")
def edit_message(message_id: str, req: MessageEditRequest):
    """Edit a message draft (inline editing from dashboard)."""
    conn = models.get_db()
    msg = conn.execute("SELECT * FROM message_drafts WHERE id=?", (message_id,)).fetchone()
    if not msg:
        conn.close()
        raise HTTPException(status_code=404, detail="Message not found")

    updates = []
    params = []
    if req.body is not None:
        updates.append("body=?")
        params.append(req.body)
        updates.append("word_count=?")
        params.append(len(req.body.split()))
    if req.subject_line is not None:
        updates.append("subject_line=?")
        params.append(req.subject_line)
    if req.approval_status is not None:
        updates.append("approval_status=?")
        params.append(req.approval_status)

    if updates:
        params.append(message_id)
        conn.execute(f"UPDATE message_drafts SET {','.join(updates)} WHERE id=?", params)
        conn.commit()

    row = conn.execute("SELECT * FROM message_drafts WHERE id=?", (message_id,)).fetchone()
    conn.close()
    return dict(row)


@router.post("/bulk-approve")
def bulk_approve_messages(batch_id: str, action: str = "approve"):
    """Bulk approve or reject all pending messages in a batch."""
    conn = models.get_db()
    status = "approved" if action == "approve" else "rejected"
    result = conn.execute(
        "UPDATE message_drafts SET approval_status=? WHERE batch_id=? AND (approval_status IS NULL OR approval_status='pending')",
        (status, batch_id)
    )
    conn.commit()
    count = result.rowcount
    conn.close()
    return {"updated": count, "status": status, "batch_id": batch_id}
