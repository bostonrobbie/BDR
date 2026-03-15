"""Email channel routes (identities, suppression, events, pacing)."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.db import models

router = APIRouter(prefix="/api/email", tags=["email"])


class EmailIdentityCreate(BaseModel):
    email_address: str
    display_name: Optional[str] = None
    daily_send_limit: Optional[int] = 25
    warmup_phase: Optional[int] = 1
    warmup_daily_cap: Optional[int] = 5


class SuppressionAdd(BaseModel):
    email_address: str
    reason: str
    source: Optional[str] = "manual"


class EmailEventLog(BaseModel):
    contact_id: Optional[str] = None
    email_address: Optional[str] = None
    event_type: str
    event_source: Optional[str] = "manual"
    details: Optional[str] = None


# ─── IDENTITIES ───────────────────────────────────────────────

@router.post("/identities")
def create_identity(req: EmailIdentityCreate):
    return models.create_email_identity(req.model_dump())


@router.get("/identities")
def list_identities(active_only: bool = True):
    return models.list_email_identities(active_only)


@router.get("/identities/{identity_id}")
def get_identity(identity_id: str):
    result = models.get_email_identity(identity_id)
    if not result:
        raise HTTPException(status_code=404, detail="Identity not found")
    return result


@router.post("/identities/{identity_id}/mark-sent")
def mark_email_sent(identity_id: str):
    pacing = models.check_pacing_ok(identity_id)
    if not pacing["ok"]:
        raise HTTPException(status_code=429, detail=pacing["reason"])
    return models.increment_send_count(identity_id)


@router.post("/identities/reset-daily")
def reset_daily():
    models.reset_daily_counts()
    return {"status": "reset"}


# ─── SUPPRESSION ──────────────────────────────────────────────

@router.post("/suppression")
def add_suppression(req: SuppressionAdd):
    return models.add_to_suppression(req.email_address, req.reason, req.source)


@router.get("/suppression")
def list_suppressions(limit: int = 100):
    return models.list_suppressed(limit)


@router.get("/suppression/check")
def check_suppression(email: str):
    return {"email": email, "suppressed": models.is_suppressed(email)}


@router.delete("/suppression")
def remove_suppression(email: str):
    removed = models.remove_from_suppression(email)
    if not removed:
        raise HTTPException(status_code=404, detail="Email not in suppression list")
    return {"removed": True, "email": email}


# ─── EVENTS ──────────────────────────────────────────────────

@router.post("/events")
def log_event(req: EmailEventLog):
    return models.log_email_event(req.model_dump())


@router.get("/events")
def list_events(contact_id: str = None, event_type: str = None, limit: int = 50):
    return models.get_email_events(contact_id, event_type, limit)


# ─── PACING & HEALTH ────────────────────────────────────────

@router.get("/pacing")
def get_pacing():
    rules = models.get_pacing_rules("email")
    identities = models.list_email_identities(active_only=True)
    total_remaining = 0
    identity_status = []
    for ident in identities:
        check = models.check_pacing_ok(ident["id"])
        identity_status.append({
            "id": ident["id"],
            "email": ident["email_address"],
            "sent_today": check.get("sent_today", 0),
            "limit": check.get("limit", 0),
            "remaining": check.get("remaining", 0),
            "ok": check.get("ok", False),
        })
        total_remaining += check.get("remaining", 0)
    return {"rules": rules, "identities": identity_status, "total_remaining": total_remaining}


@router.get("/health")
def email_health():
    return models.get_email_health()
