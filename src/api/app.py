"""
Outreach Command Center - FastAPI Backend
REST API for all CRUD operations, dashboard stats, and agent triggers.

Run: uvicorn src.api.app:app --reload --port 8000
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import json

from src.db import models

app = FastAPI(title="Outreach Command Center", version="0.1.0")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── PYDANTIC MODELS ────────────────────────────────────────────

class AccountCreate(BaseModel):
    name: str
    domain: Optional[str] = None
    industry: Optional[str] = None
    sub_industry: Optional[str] = None
    employee_count: Optional[int] = None
    employee_band: Optional[str] = None
    tier: Optional[str] = None
    known_tools: Optional[list] = []
    linkedin_company_url: Optional[str] = None
    website_url: Optional[str] = None
    buyer_intent: Optional[int] = 0
    hq_location: Optional[str] = None
    notes: Optional[str] = None

class ContactCreate(BaseModel):
    account_id: Optional[str] = None
    first_name: str
    last_name: str
    title: Optional[str] = None
    persona_type: Optional[str] = None
    seniority_level: Optional[str] = None
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    timezone: Optional[str] = None
    tenure_months: Optional[int] = None
    recently_hired: Optional[int] = 0
    previous_company: Optional[str] = None
    previous_title: Optional[str] = None
    source: Optional[str] = "sales_nav"
    predicted_objection: Optional[str] = None
    objection_response: Optional[str] = None

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

class TouchpointLog(BaseModel):
    contact_id: str
    message_draft_id: Optional[str] = None
    channel: str
    touch_number: Optional[int] = None
    outcome: Optional[str] = None
    call_duration_seconds: Optional[int] = None
    call_notes: Optional[str] = None

class ReplyLog(BaseModel):
    contact_id: str
    touchpoint_id: Optional[str] = None
    channel: Optional[str] = None
    intent: Optional[str] = None
    reply_tag: Optional[str] = None
    summary: Optional[str] = None
    raw_text: Optional[str] = None
    referral_name: Optional[str] = None
    referral_title: Optional[str] = None
    recommended_next_step: Optional[str] = None

class OpportunityCreate(BaseModel):
    contact_id: str
    account_id: Optional[str] = None
    meeting_date: Optional[str] = None
    status: Optional[str] = "meeting_booked"
    pipeline_value: Optional[float] = None
    trigger_touchpoint_id: Optional[str] = None
    trigger_reply_id: Optional[str] = None
    attribution_channel: Optional[str] = None
    attribution_touch_number: Optional[int] = None
    attribution_proof_point: Optional[str] = None
    attribution_pain_hook: Optional[str] = None
    ae_name: Optional[str] = None
    notes: Optional[str] = None

class BatchCreate(BaseModel):
    batch_number: Optional[int] = None
    prospect_count: Optional[int] = 0
    ab_variable: Optional[str] = None
    ab_description: Optional[str] = None
    pre_brief: Optional[str] = None

class ContactUpdate(BaseModel):
    stage: Optional[str] = None
    priority_score: Optional[int] = None
    status: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    predicted_objection: Optional[str] = None
    objection_response: Optional[str] = None
    personalization_score: Optional[int] = None
    do_not_contact: Optional[int] = None
    dnc_reason: Optional[str] = None
    notes: Optional[str] = None


# ─── DASHBOARD / HOME ───────────────────────────────────────────

@app.get("/")
def serve_dashboard():
    """Serve the main dashboard HTML."""
    ui_path = os.path.join(os.path.dirname(__file__), "../ui/index.html")
    if os.path.exists(ui_path):
        return FileResponse(ui_path, media_type="text/html")
    return {"message": "Outreach Command Center API", "version": "0.1.0", "docs": "/docs"}


@app.get("/api/stats")
def dashboard_stats():
    """Get high-level dashboard statistics."""
    return models.get_dashboard_stats()


@app.get("/api/action-queue")
def action_queue():
    """Get today's prioritized action queue."""
    return models.get_action_queue()


# ─── ACCOUNTS ───────────────────────────────────────────────────

@app.post("/api/accounts")
def create_account(account: AccountCreate):
    return models.create_account(account.model_dump())


@app.get("/api/accounts")
def list_accounts(limit: int = 100, offset: int = 0, industry: str = None):
    return models.list_accounts(limit=limit, offset=offset, industry=industry)


@app.get("/api/accounts/{account_id}")
def get_account(account_id: str):
    result = models.get_account(account_id)
    if not result:
        raise HTTPException(status_code=404, detail="Account not found")
    return result


@app.patch("/api/accounts/{account_id}")
def update_account(account_id: str, data: dict):
    result = models.update_account(account_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Account not found")
    return result


# ─── CONTACTS ───────────────────────────────────────────────────

@app.post("/api/contacts")
def create_contact(contact: ContactCreate):
    return models.create_contact(contact.model_dump())


@app.get("/api/contacts")
def list_contacts(limit: int = 100, offset: int = 0, stage: str = None,
                  min_priority: int = None, persona_type: str = None,
                  account_id: str = None):
    return models.list_contacts(
        limit=limit, offset=offset, stage=stage,
        min_priority=min_priority, persona_type=persona_type, account_id=account_id
    )


@app.get("/api/contacts/{contact_id}")
def get_contact(contact_id: str):
    result = models.get_contact(contact_id)
    if not result:
        raise HTTPException(status_code=404, detail="Contact not found")
    return result


@app.patch("/api/contacts/{contact_id}")
def update_contact(contact_id: str, data: ContactUpdate):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = models.update_contact(contact_id, update_data)
    if not result:
        raise HTTPException(status_code=404, detail="Contact not found")
    return result


@app.post("/api/contacts/{contact_id}/score")
def score_contact(contact_id: str):
    """Compute and save priority score for a contact."""
    return models.score_and_save(contact_id)


# ─── MESSAGES ───────────────────────────────────────────────────

@app.post("/api/messages")
def create_message(msg: MessageDraftCreate):
    data = msg.model_dump()
    # Auto-compute word count
    data["word_count"] = len(data["body"].split())
    return models.create_message_draft(data)


@app.get("/api/messages")
def list_messages(batch_id: str = None, channel: str = None,
                  approval_status: str = None, limit: int = 100):
    return models.list_messages(batch_id=batch_id, channel=channel,
                                approval_status=approval_status, limit=limit)


@app.get("/api/contacts/{contact_id}/messages")
def get_contact_messages(contact_id: str):
    return models.get_messages_for_contact(contact_id)


# ─── TOUCHPOINTS ────────────────────────────────────────────────

@app.post("/api/touchpoints")
def log_touchpoint(tp: TouchpointLog):
    return models.log_touchpoint(tp.model_dump())


# ─── REPLIES ────────────────────────────────────────────────────

@app.post("/api/replies")
def log_reply(reply: ReplyLog):
    return models.log_reply(reply.model_dump())


# ─── OPPORTUNITIES ──────────────────────────────────────────────

@app.post("/api/opportunities")
def create_opportunity(opp: OpportunityCreate):
    return models.create_opportunity(opp.model_dump())


@app.get("/api/opportunities")
def list_opportunities():
    conn = models.get_db()
    rows = conn.execute("""
        SELECT o.*, c.first_name, c.last_name, c.title as contact_title,
               a.name as company_name
        FROM opportunities o
        LEFT JOIN contacts c ON o.contact_id = c.id
        LEFT JOIN accounts a ON o.account_id = a.id
        ORDER BY o.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── FOLLOWUPS ──────────────────────────────────────────────────

@app.get("/api/followups/due")
def due_followups():
    return models.get_due_followups()


@app.post("/api/followups")
def schedule_followup(contact_id: str, touch_number: int, channel: str, days_from_now: int):
    return models.schedule_followup(contact_id, touch_number, channel, days_from_now)


# ─── BATCHES ────────────────────────────────────────────────────

@app.post("/api/batches")
def create_batch(batch: BatchCreate):
    return models.create_batch(batch.model_dump())


@app.get("/api/batches")
def list_batches():
    conn = models.get_db()
    rows = conn.execute("SELECT * FROM batches ORDER BY batch_number DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── ANALYTICS ──────────────────────────────────────────────────

@app.get("/api/analytics/replies")
def reply_analytics():
    return models.get_reply_analytics()


@app.get("/api/analytics/pipeline")
def pipeline_analytics():
    """Get pipeline funnel metrics."""
    conn = models.get_db()
    funnel = {
        "total_prospects": conn.execute("SELECT COUNT(*) FROM contacts WHERE status='active'").fetchone()[0],
        "touched": conn.execute("SELECT COUNT(*) FROM contacts WHERE stage NOT IN ('new')").fetchone()[0],
        "replied": conn.execute("SELECT COUNT(DISTINCT contact_id) FROM replies").fetchone()[0],
        "meetings": conn.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0],
        "opportunities": conn.execute("SELECT COUNT(*) FROM opportunities WHERE opportunity_created=1").fetchone()[0],
    }

    # Conversion rates
    if funnel["touched"] > 0:
        funnel["reply_rate"] = round(funnel["replied"] / funnel["touched"] * 100, 1)
    else:
        funnel["reply_rate"] = 0

    if funnel["replied"] > 0:
        funnel["meeting_rate"] = round(funnel["meetings"] / funnel["replied"] * 100, 1)
    else:
        funnel["meeting_rate"] = 0

    if funnel["meetings"] > 0:
        funnel["opp_rate"] = round(funnel["opportunities"] / funnel["meetings"] * 100, 1)
    else:
        funnel["opp_rate"] = 0

    conn.close()
    return funnel


@app.get("/api/analytics/experiments")
def experiment_analytics():
    conn = models.get_db()
    rows = conn.execute("SELECT * FROM experiments ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── AGENT RUNS ─────────────────────────────────────────────────

@app.get("/api/agent-runs")
def list_agent_runs(limit: int = 50, agent_name: str = None):
    conn = models.get_db()
    query = "SELECT * FROM agent_runs"
    params = []
    if agent_name:
        query += " WHERE agent_name=?"
        params.append(agent_name)
    query += " ORDER BY started_at DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── HEALTH CHECK ───────────────────────────────────────────────

@app.get("/api/health")
def health():
    try:
        conn = models.get_db()
        tables = conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table'"
        ).fetchone()[0]
        conn.close()
        return {"status": "healthy", "tables": tables, "db_path": models.DB_PATH}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "unhealthy", "error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
