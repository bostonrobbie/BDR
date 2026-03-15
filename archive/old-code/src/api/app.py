"""
Outreach Command Center - FastAPI Backend
REST API for CRUD, analytics, pipeline control, SSE streaming, and agent triggers.

Run: uvicorn src.api.app:app --reload --port 8000
"""

import os
import asyncio
import json

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, List

from src.db import models
from src.api.routers import accounts, contacts, messages, email, linkedin, analytics

ALLOWED_ORIGINS = os.environ.get("OCC_CORS_ORIGINS", "http://localhost:3000,http://localhost:8000,http://localhost:8765").split(",")

app = FastAPI(
    title="Outreach Command Center",
    description="BDR operations platform API for LinkedIn, Email, and Cold Calling outreach.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── ROUTERS ─────────────────────────────────────────────────
# New modular routers (preferred for new development)
app.include_router(accounts.router)
app.include_router(contacts.router)
app.include_router(messages.router)
app.include_router(email.router)
app.include_router(linkedin.router)
app.include_router(analytics.router)


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

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    industry: Optional[str] = None
    sub_industry: Optional[str] = None
    employee_count: Optional[int] = None
    employee_band: Optional[str] = None
    tier: Optional[str] = None
    known_tools: Optional[list] = None
    linkedin_company_url: Optional[str] = None
    website_url: Optional[str] = None
    buyer_intent: Optional[int] = None
    hq_location: Optional[str] = None
    notes: Optional[str] = None

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

class PipelineStartRequest(BaseModel):
    batch_number: int
    target_count: Optional[int] = 25
    ab_variable: Optional[str] = "pain_hook"
    ab_groups: Optional[dict] = None
    mix_ratio: Optional[dict] = None
    auto_approve: Optional[bool] = True
    saved_search_url: Optional[str] = None

class ApprovalRequest(BaseModel):
    decisions: dict  # message_id -> "approve" | "reject"

class AgentActionRequest(BaseModel):
    action: str  # re_score, re_research, regenerate_messages, run_qc, score_batch, generate_html, run_pre_brief
    contact_id: Optional[str] = None
    batch_id: Optional[str] = None
    params: Optional[dict] = None

class MessageEditRequest(BaseModel):
    body: Optional[str] = None
    subject_line: Optional[str] = None
    approval_status: Optional[str] = None  # approved, rejected, edited

class SyncItem(BaseModel):
    contact_id: str
    stage: str = None
    reply_tag: str = None
    notes: str = None

class SyncBulk(BaseModel):
    items: list[SyncItem]


# ─── DASHBOARD / HOME ───────────────────────────────────────────

@app.get("/")
def serve_dashboard():
    ui_dir = os.path.join(os.path.dirname(__file__), "../ui")
    # Try occ-dashboard.html first, then index.html
    for name in ("occ-dashboard.html", "index.html"):
        path = os.path.join(ui_dir, name)
        if os.path.exists(path):
            return FileResponse(path, media_type="text/html")
    return {"message": "Outreach Command Center API", "version": "2.0.0", "docs": "/docs"}


@app.get("/api/stats")
def dashboard_stats():
    return models.get_dashboard_stats()


@app.get("/api/action-queue")
def smart_action_queue():
    """Smart action queue: overdue followups, stuck prospects, re-engagement triggers, hot leads."""
    conn = models.get_db()
    actions = []

    # 1. Overdue followups (highest priority)
    overdue = conn.execute("""
        SELECT f.*, c.first_name, c.last_name, c.priority_score, a.name as company_name
        FROM followups f
        JOIN contacts c ON f.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        WHERE f.due_date <= datetime('now') AND f.completed_at IS NULL
        ORDER BY c.priority_score DESC LIMIT 10
    """).fetchall()
    for f in overdue:
        d = dict(f)
        actions.append({
            "type": "overdue_followup",
            "priority": "hot",
            "contact": f"{d['first_name']} {d['last_name']}",
            "company": d.get("company_name", ""),
            "contact_id": d["contact_id"],
            "action": f"Overdue: Touch {d.get('touch_number', '?')} via {d.get('channel', '?')} was due {d.get('due_date', '')}",
            "impact": 5,
        })

    # 2. High-priority prospects not yet touched
    untouched = conn.execute("""
        SELECT c.id, c.first_name, c.last_name, c.priority_score, c.stage, a.name as company_name
        FROM contacts c
        LEFT JOIN accounts a ON c.account_id = a.id
        WHERE c.stage = 'new' AND c.priority_score >= 4 AND c.status = 'active'
        ORDER BY c.priority_score DESC LIMIT 10
    """).fetchall()
    for c in untouched:
        d = dict(c)
        actions.append({
            "type": "untouched_hot",
            "priority": "high" if d["priority_score"] >= 5 else "medium",
            "contact": f"{d['first_name']} {d['last_name']}",
            "company": d.get("company_name", ""),
            "contact_id": d["id"],
            "action": f"Priority {d['priority_score']} prospect - not yet contacted",
            "impact": d["priority_score"],
        })

    # 3. Prospects stuck in a stage (touched but no progress for 7+ days)
    stuck = conn.execute("""
        SELECT c.id, c.first_name, c.last_name, c.priority_score, c.stage, c.updated_at,
               a.name as company_name
        FROM contacts c
        LEFT JOIN accounts a ON c.account_id = a.id
        WHERE c.stage NOT IN ('new', 'replied', 'meeting_booked', 'not_interested')
          AND c.status = 'active'
          AND c.updated_at < datetime('now', '-7 days')
        ORDER BY c.priority_score DESC LIMIT 8
    """).fetchall()
    for c in stuck:
        d = dict(c)
        actions.append({
            "type": "stuck",
            "priority": "medium",
            "contact": f"{d['first_name']} {d['last_name']}",
            "company": d.get("company_name", ""),
            "contact_id": d["id"],
            "action": f"Stuck at '{d['stage']}' since {(d.get('updated_at') or '')[:10]} - send next touch",
            "impact": 3,
        })

    # 4. Active re-engagement signals
    signals = conn.execute("""
        SELECT s.id as signal_id, s.signal_type, s.description,
               c.first_name, c.last_name, c.id as contact_id, c.priority_score,
               a.name as company_name
        FROM signals s
        LEFT JOIN contacts c ON s.contact_id = c.id
        LEFT JOIN accounts a ON s.account_id = a.id
        WHERE (s.acted_on IS NULL OR s.acted_on = 0)
          AND (s.expires_at IS NULL OR s.expires_at > datetime('now'))
        ORDER BY s.created_at DESC LIMIT 5
    """).fetchall()
    for s in signals:
        d = dict(s)
        actions.append({
            "type": "signal",
            "priority": "high" if d.get("signal_type") == "buyer_intent" else "medium",
            "contact": f"{d.get('first_name', '')} {d.get('last_name', '')}".strip() or "Unknown",
            "company": d.get("company_name", ""),
            "contact_id": d.get("contact_id"),
            "signal_id": d.get("signal_id"),
            "action": f"{d.get('signal_type', 'signal')}: {d.get('description', '')}",
            "impact": 4 if d.get("signal_type") == "buyer_intent" else 3,
        })

    conn.close()

    # Sort by impact score descending
    actions.sort(key=lambda x: x.get("impact", 0), reverse=True)

    return actions[:20]


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
def update_account(account_id: str, data: AccountUpdate):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = models.update_account(account_id, update_data)
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
    return models.score_and_save(contact_id)


# ─── MESSAGES ───────────────────────────────────────────────────

@app.post("/api/messages")
def create_message(msg: MessageDraftCreate):
    data = msg.model_dump()
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

@app.patch("/api/messages/{message_id}")
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
def list_batches(limit: int = 20):
    conn = models.get_db()
    rows = conn.execute("""
        SELECT b.*,
               (SELECT COUNT(*) FROM batch_prospects WHERE batch_id=b.id) as contact_count,
               (SELECT COUNT(*) FROM message_drafts WHERE batch_id=b.id) as message_count
        FROM batches b
        ORDER BY b.created_at DESC LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/batches/{batch_id}/summary")
def batch_summary(batch_id: str):
    result = models.get_batch_summary(batch_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/api/batches/{batch_id}/messages")
def batch_messages(batch_id: str, approval_status: str = None):
    """Get all messages for a batch, optionally filtered by approval status."""
    conn = models.get_db()
    query = """
        SELECT md.*, c.first_name, c.last_name, c.title, a.name as company_name
        FROM message_drafts md
        LEFT JOIN contacts c ON md.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        WHERE md.batch_id = ?
    """
    params = [batch_id]
    if approval_status:
        query += " AND md.approval_status = ?"
        params.append(approval_status)
    query += " ORDER BY c.priority_score DESC, md.touch_number ASC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── ANALYTICS ──────────────────────────────────────────────────

@app.get("/api/analytics/replies")
def reply_analytics():
    return models.get_reply_analytics()

@app.get("/api/analytics/pipeline")
def pipeline_analytics():
    conn = models.get_db()
    funnel = {
        "total_prospects": conn.execute("SELECT COUNT(*) FROM contacts WHERE status='active'").fetchone()[0],
        "touched": conn.execute("SELECT COUNT(*) FROM contacts WHERE stage NOT IN ('new')").fetchone()[0],
        "replied": conn.execute("SELECT COUNT(DISTINCT contact_id) FROM replies").fetchone()[0],
        "meetings": conn.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0],
        "opportunities": conn.execute("SELECT COUNT(*) FROM opportunities WHERE opportunity_created=1").fetchone()[0],
    }
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

@app.get("/api/analytics/batch-comparison")
def batch_comparison():
    """Cross-batch comparison for intelligence charts."""
    conn = models.get_db()
    batches = conn.execute("""
        SELECT b.id, b.batch_number, b.ab_variable, b.ab_description, b.created_at,
               (SELECT COUNT(*) FROM batch_prospects WHERE batch_id=b.id) as prospects,
               (SELECT COUNT(*) FROM message_drafts WHERE batch_id=b.id) as messages,
               (SELECT COUNT(*) FROM message_drafts WHERE batch_id=b.id AND qc_passed=1) as qc_passed,
               (SELECT COUNT(DISTINCT r.contact_id) FROM replies r
                JOIN batch_prospects bp ON r.contact_id=bp.contact_id
                WHERE bp.batch_id=b.id) as replies,
               (SELECT COUNT(*) FROM opportunities o
                JOIN contacts c ON o.contact_id=c.id
                JOIN batch_prospects bp ON c.id=bp.contact_id
                WHERE bp.batch_id=b.id) as meetings,
               (SELECT AVG(md.personalization_score) FROM message_drafts md
                WHERE md.batch_id=b.id AND md.personalization_score > 0) as avg_personalization
        FROM batches b ORDER BY b.batch_number ASC
    """).fetchall()
    conn.close()
    results = []
    for b in batches:
        d = dict(b)
        d["reply_rate"] = round(d["replies"] / d["prospects"] * 100, 1) if d["prospects"] > 0 else 0
        d["meeting_rate"] = round(d["meetings"] / d["replies"] * 100, 1) if d["replies"] > 0 else 0
        d["qc_pass_rate"] = round(d["qc_passed"] / d["messages"] * 100, 1) if d["messages"] > 0 else 0
        d["avg_personalization"] = round(d["avg_personalization"] or 0, 1)
        results.append(d)
    return results

@app.get("/api/analytics/top-messages")
def top_messages():
    """Top performing messages (those that got replies), ranked for pattern analysis."""
    conn = models.get_db()
    rows = conn.execute("""
        SELECT md.id, md.contact_id, md.touch_number, md.channel, md.subject_line,
               md.body as message_body, md.personalization_score, md.ab_group,
               c.first_name, c.last_name, c.persona_type, c.title,
               a.name as company,
               r.reply_tag, r.summary as reply_summary
        FROM message_drafts md
        JOIN contacts c ON md.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        LEFT JOIN replies r ON r.contact_id = md.contact_id
        WHERE r.id IS NOT NULL
        ORDER BY md.personalization_score DESC, r.created_at DESC
        LIMIT 10
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/api/analytics/token-costs")
def token_costs():
    """Token usage and cost tracking - by agent, by batch, and per-prospect."""
    conn = models.get_db()

    # By agent
    by_agent = conn.execute("""
        SELECT agent_name,
               COUNT(*) as runs,
               SUM(tokens_used) as total_tokens,
               AVG(tokens_used) as avg_tokens,
               SUM(duration_ms) as total_duration_ms
        FROM agent_runs
        GROUP BY agent_name
        ORDER BY total_tokens DESC
    """).fetchall()

    # By batch (approximate - using agent runs with batch metadata)
    by_batch = conn.execute("""
        SELECT b.batch_number,
               (SELECT COUNT(*) FROM batch_prospects WHERE batch_id=b.id) as prospects,
               (SELECT SUM(ar.tokens_used) FROM agent_runs ar
                WHERE ar.run_type LIKE '%batch%' OR ar.batch_id=b.id) as batch_tokens
        FROM batches b ORDER BY b.batch_number ASC
    """).fetchall()

    # Totals
    totals = conn.execute("""
        SELECT COUNT(*) as total_runs,
               SUM(tokens_used) as total_tokens,
               SUM(duration_ms) as total_duration_ms
        FROM agent_runs
    """).fetchone()

    # Total prospects and replies for per-unit costs
    prospect_count = conn.execute("SELECT COUNT(*) FROM contacts WHERE status='active'").fetchone()[0]
    reply_count = conn.execute("SELECT COUNT(DISTINCT contact_id) FROM replies").fetchone()[0]

    conn.close()

    # Cost rate: $3/1M input tokens (Claude Sonnet estimate)
    cost_rate = 3.0

    agent_results = []
    for r in by_agent:
        d = dict(r)
        d["est_cost_usd"] = round((d["total_tokens"] or 0) / 1_000_000 * cost_rate, 4)
        agent_results.append(d)

    batch_results = []
    for b in by_batch:
        d = dict(b)
        tokens = d.get("batch_tokens") or 0
        prospects = d.get("prospects") or 0
        d["est_cost_usd"] = round(tokens / 1_000_000 * cost_rate, 4)
        d["cost_per_prospect"] = round(d["est_cost_usd"] / prospects, 4) if prospects > 0 else 0
        batch_results.append(d)

    total_tokens = (totals["total_tokens"] or 0) if totals else 0
    total_cost = round(total_tokens / 1_000_000 * cost_rate, 4)

    return {
        "by_agent": agent_results,
        "by_batch": batch_results,
        "totals": {
            "total_runs": (totals["total_runs"] or 0) if totals else 0,
            "total_tokens": total_tokens,
            "total_duration_ms": (totals["total_duration_ms"] or 0) if totals else 0,
            "est_cost_usd": total_cost,
            "cost_per_prospect": round(total_cost / prospect_count, 4) if prospect_count > 0 else 0,
            "cost_per_reply": round(total_cost / reply_count, 4) if reply_count > 0 else 0,
            "prospect_count": prospect_count,
            "reply_count": reply_count,
        }
    }


# ─── SIGNALS ────────────────────────────────────────────────────

@app.get("/api/signals")
def list_signals(signal_type: str = None, active_only: bool = True, limit: int = 50):
    """List buyer intent and re-engagement signals."""
    conn = models.get_db()
    query = "SELECT s.*, c.first_name, c.last_name, c.title, a.name as company_name FROM signals s LEFT JOIN contacts c ON s.contact_id=c.id LEFT JOIN accounts a ON s.account_id=a.id WHERE 1=1"
    params = []
    if signal_type:
        query += " AND s.signal_type=?"
        params.append(signal_type)
    if active_only:
        query += " AND (s.expires_at IS NULL OR s.expires_at > datetime('now'))"
    query += " ORDER BY s.created_at DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.post("/api/signals/{signal_id}/re-engage")
def re_engage_signal(signal_id: str):
    """Mark a signal as.acted_on and queue a re-engagement sequence."""
    conn = models.get_db()
    signal = conn.execute("SELECT * FROM signals WHERE id=?", (signal_id,)).fetchone()
    if not signal:
        conn.close()
        raise HTTPException(status_code=404, detail="Signal not found")

    signal_data = dict(signal)
    contact_id = signal_data.get("contact_id")

    # Mark signal as.acted_on
    conn.execute("UPDATE signals SET acted_on=1 WHERE id=?", (signal_id,))

    # Update contact stage to re-engaged
    if contact_id:
        conn.execute("UPDATE contacts SET stage='re_engaged' WHERE id=?", (contact_id,))

    conn.commit()
    conn.close()

    return {
        "status": "queued",
        "signal_id": signal_id,
        "contact_id": contact_id,
        "trigger": signal_data.get("signal_type"),
        "message": f"Re-engagement queued for {signal_data.get('signal_type')} signal"
    }


@app.post("/api/signals")
def create_signal(data: dict):
    """Create a manual signal for a contact."""
    conn = models.get_db()
    import uuid
    signal_id = str(uuid.uuid4())[:8]
    conn.execute("""
        INSERT INTO signals (id, contact_id, account_id, signal_type, description, created_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    """, (signal_id, data.get("contact_id"), data.get("account_id"),
          data.get("signal_type", "manual"), data.get("description", "")))
    conn.commit()
    conn.close()
    return {"id": signal_id, "status": "created"}


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

        # Check LLM gateway connectivity
        gateway_status = "unknown"
        gateway_url = None
        try:
            gw = conn.execute("SELECT value FROM gateway_config WHERE key='gateway_url'").fetchone()
            if gw:
                gateway_url = gw[0]
                import urllib.request
                req = urllib.request.Request(f"{gateway_url}/health", method="GET")
                req.add_header("User-Agent", "OCC-HealthCheck")
                with urllib.request.urlopen(req, timeout=3) as resp:
                    gateway_status = "healthy" if resp.status == 200 else "degraded"
        except Exception:
            gateway_status = "unreachable" if gateway_url else "not_configured"

        conn.close()
        return {
            "status": "healthy",
            "tables": tables,
            "db_path": models.DB_PATH,
            "gateway": {"status": gateway_status, "url": gateway_url},
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "unhealthy", "error": str(e)})


# ─── INTELLIGENCE ──────────────────────────────────────────────

@app.get("/api/intelligence")
def intelligence():
    return models.get_intelligence_data()

@app.get("/api/contacts/{contact_id}/prep-card")
def prep_card(contact_id: str):
    result = models.get_prep_card(contact_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# ─── SYNC FROM HTML ────────────────────────────────────────────

@app.post("/api/sync")
def sync_html(payload: SyncBulk):
    results = []
    for item in payload.items:
        r = models.sync_html_status(
            contact_id=item.contact_id,
            stage=item.stage,
            reply_tag=item.reply_tag,
            notes=item.notes,
        )
        results.append(r)
    return {"synced": len(results), "results": results}


# ─── EXPERIMENT RESULTS ────────────────────────────────────────

@app.get("/api/experiments/{experiment_id}/results")
def experiment_results(experiment_id: str):
    result = models.get_experiment_results(experiment_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# ════════════════════════════════════════════════════════════════
# ═══ AGENTIC CONTROLS (NEW) ═══════════════════════════════════
# ════════════════════════════════════════════════════════════════

# ─── PIPELINE LAUNCHER ─────────────────────────────────────────

@app.post("/api/pipeline/start")
def start_pipeline(req: PipelineStartRequest):
    """Launch a new batch pipeline in the background."""
    from src.api.pipeline_runner import start_pipeline as _start

    # Validation
    if req.batch_number < 1:
        raise HTTPException(status_code=400, detail="Batch number must be >= 1")
    if req.target_count < 1 or req.target_count > 100:
        raise HTTPException(status_code=400, detail="Target count must be 1-100")

    # Duplicate batch number check
    conn = models.get_db()
    existing = conn.execute(
        "SELECT id FROM batches WHERE batch_number=?", (req.batch_number,)
    ).fetchone()
    conn.close()
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Batch #{req.batch_number} already exists. Use the next available number."
        )

    # Check no other pipeline is running
    from src.api.pipeline_runner import list_runs
    active = [r for r in list_runs() if r.get("status") in ("running", "approval_needed")]
    if active:
        raise HTTPException(
            status_code=409,
            detail=f"Pipeline already running (run {active[0]['run_id']}). Cancel it first or wait."
        )

    config = {
        "target_count": req.target_count,
        "ab_variable": req.ab_variable,
        "ab_groups": req.ab_groups or {"A": "Variant A", "B": "Variant B"},
        "mix_ratio": req.mix_ratio or {},
        "auto_approve": req.auto_approve,
        "saved_search_url": req.saved_search_url,
    }

    run = _start(req.batch_number, config)
    return {"run_id": run.run_id, "status": run.status, "batch_number": req.batch_number}


@app.get("/api/pipeline/runs")
def list_pipeline_runs():
    """List all pipeline runs (active and completed)."""
    from src.api.pipeline_runner import list_runs
    return list_runs()


@app.get("/api/pipeline/runs/{run_id}")
def get_pipeline_run(run_id: str):
    """Get status of a specific pipeline run."""
    from src.api.pipeline_runner import get_run
    run = get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Pipeline run not found")
    return run.to_dict()


@app.post("/api/pipeline/runs/{run_id}/cancel")
def cancel_pipeline_run(run_id: str):
    """Cancel a running pipeline."""
    from src.api.pipeline_runner import cancel_run
    success = cancel_run(run_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot cancel - run not active")
    return {"cancelled": True, "run_id": run_id}


# ─── APPROVAL GATE ─────────────────────────────────────────────

@app.post("/api/pipeline/runs/{run_id}/approve")
def approve_pipeline_messages(run_id: str, req: ApprovalRequest):
    """Submit message approval decisions for a paused pipeline."""
    from src.api.pipeline_runner import approve_messages
    success = approve_messages(run_id, req.decisions)
    if not success:
        raise HTTPException(status_code=400, detail="Run not in approval_needed state")
    return {"approved": True, "run_id": run_id, "decisions": len(req.decisions)}


@app.post("/api/pipeline/runs/{run_id}/skip-approval")
def skip_approval(run_id: str):
    """Auto-approve all messages and continue pipeline."""
    from src.api.pipeline_runner import skip_approval as _skip
    success = _skip(run_id)
    if not success:
        raise HTTPException(status_code=400, detail="Run not in approval_needed state")
    return {"skipped": True, "run_id": run_id}


# ─── SSE STREAMING ─────────────────────────────────────────────

@app.get("/api/pipeline/runs/{run_id}/stream")
async def stream_pipeline_events(run_id: str):
    """Server-Sent Events stream for live pipeline progress."""
    from src.api.pipeline_runner import subscribe, unsubscribe, get_run

    run = get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Pipeline run not found")

    q = subscribe(run_id)

    async def event_generator():
        try:
            while True:
                try:
                    # Non-blocking check with timeout
                    msg = await asyncio.get_event_loop().run_in_executor(
                        None, lambda: q.get(timeout=30)
                    )
                    yield f"event: {msg['event']}\ndata: {json.dumps(msg['data'])}\n\n"

                    # Stop streaming if pipeline is done
                    if msg["event"] in ("completed", "failed", "cancelled"):
                        break
                except Exception:
                    # Send keepalive
                    yield f": keepalive\n\n"

                    # Check if run is done
                    current = get_run(run_id)
                    if current and current.status in ("completed", "failed", "cancelled"):
                        yield f"event: {current.status}\ndata: {json.dumps(current.to_dict())}\n\n"
                        break
        finally:
            unsubscribe(run_id, q)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


# ─── AGENT ACTIONS (per-prospect) ──────────────────────────────

@app.post("/api/agent/action")
def run_agent_action(req: AgentActionRequest):
    """Run a single agent action (re-score, QC, generate HTML, etc.)."""
    from src.api.pipeline_runner import run_agent_action as _run
    result = _run(
        action=req.action,
        contact_id=req.contact_id,
        batch_id=req.batch_id,
        params=req.params,
    )
    return result


@app.post("/api/contacts/{contact_id}/re-score")
def re_score_contact(contact_id: str):
    """Re-run ICP + priority scoring for a single contact."""
    from src.api.pipeline_runner import run_agent_action as _run
    return _run(action="re_score", contact_id=contact_id)


@app.post("/api/contacts/{contact_id}/run-qc")
def run_qc_contact(contact_id: str):
    """Re-run quality gate on all messages for a contact."""
    from src.api.pipeline_runner import run_agent_action as _run
    return _run(action="run_qc", contact_id=contact_id)


@app.post("/api/contacts/{contact_id}/re-research")
def re_research_contact(contact_id: str):
    """Re-run company + person research for a contact."""
    from src.api.pipeline_runner import run_agent_action as _run
    return _run(action="re_research", contact_id=contact_id)


@app.post("/api/contacts/{contact_id}/regenerate-messages")
def regenerate_messages_contact(contact_id: str):
    """Regenerate all message drafts for a contact."""
    from src.api.pipeline_runner import run_agent_action as _run
    return _run(action="regenerate_messages", contact_id=contact_id)


@app.post("/api/batches/{batch_id}/score-all")
def score_batch(batch_id: str):
    """Re-score all contacts in a batch."""
    from src.api.pipeline_runner import run_agent_action as _run
    return _run(action="score_batch", batch_id=batch_id)


@app.post("/api/batches/{batch_id}/generate-html")
def regenerate_html(batch_id: str):
    """Regenerate the HTML deliverable for a batch."""
    from src.api.pipeline_runner import run_agent_action as _run
    return _run(action="generate_html", batch_id=batch_id)


@app.post("/api/pre-brief")
def run_pre_brief():
    """Generate a fresh pre-brief from accumulated data."""
    from src.api.pipeline_runner import run_agent_action as _run
    return _run(action="run_pre_brief")


# ─── BATCH APPROVAL QUEUE ─────────────────────────────────────

@app.get("/api/approval-queue")
def approval_queue(batch_id: str = None, approval_status: str = None):
    """Get messages pending approval, grouped by contact."""
    conn = models.get_db()
    # Build WHERE clause based on filters
    if approval_status and approval_status != 'pending':
        if approval_status == 'all':
            where = "WHERE 1=1"
        else:
            where = "WHERE md.approval_status = ?"
    else:
        where = "WHERE (md.approval_status IS NULL OR md.approval_status = 'pending')"
    query = f"""
        SELECT md.*, c.first_name, c.last_name, c.title, c.priority_score,
               a.name as company_name, a.industry,
               bp.ab_group
        FROM message_drafts md
        JOIN contacts c ON md.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        LEFT JOIN batch_prospects bp ON md.contact_id = bp.contact_id AND md.batch_id = bp.batch_id
        {where}
    """
    params = []
    if approval_status and approval_status not in ('pending', 'all'):
        params.append(approval_status)
    if batch_id:
        query += " AND md.batch_id = ?"
        params.append(batch_id)
    query += " ORDER BY c.priority_score DESC, md.touch_number ASC"
    rows = conn.execute(query, params).fetchall()
    conn.close()

    # Group by contact
    grouped = {}
    for r in rows:
        d = dict(r)
        cid = d["contact_id"]
        if cid not in grouped:
            grouped[cid] = {
                "contact_id": cid,
                "name": f"{d['first_name']} {d['last_name']}",
                "title": d["title"],
                "company": d["company_name"],
                "industry": d["industry"],
                "priority_score": d["priority_score"],
                "ab_group": d["ab_group"],
                "messages": [],
            }
        grouped[cid]["messages"].append(d)

    return list(grouped.values())


@app.post("/api/messages/bulk-approve")
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


# ─── EXPORT ────────────────────────────────────────────────────

@app.get("/api/export/csv")
def export_csv(batch_id: str = None, min_priority: int = None,
               persona_type: str = None, stage: str = None,
               columns: str = None):
    """Export contacts + status as CSV for CRM import.
    Optional column selection via comma-separated string.
    """
    import csv
    import io
    from datetime import datetime

    all_columns = [
        "first_name", "last_name", "title", "email", "linkedin_url", "phone",
        "persona_type", "seniority_level", "stage", "priority_score",
        "personalization_score", "predicted_objection", "objection_response",
        "company", "industry", "domain", "employee_count", "hq_location",
        "buyer_intent"
    ]

    selected = columns.split(",") if columns else all_columns
    # Validate columns
    selected = [c.strip() for c in selected if c.strip() in all_columns]
    if not selected:
        selected = all_columns

    conn = models.get_db()
    query = """
        SELECT c.first_name, c.last_name, c.title, c.email, c.linkedin_url, c.phone,
               c.persona_type, c.seniority_level, c.stage, c.priority_score,
               c.personalization_score, c.predicted_objection, c.objection_response,
               a.name as company, a.industry, a.domain, a.employee_count,
               a.hq_location, a.buyer_intent
        FROM contacts c
        LEFT JOIN accounts a ON c.account_id = a.id
    """
    conditions = ["c.status = 'active'"]
    params = []

    if batch_id:
        query = query.replace("LEFT JOIN accounts", "JOIN batch_prospects bp ON c.id = bp.contact_id LEFT JOIN accounts")
        conditions.append("bp.batch_id = ?")
        params.append(batch_id)
    if min_priority:
        conditions.append("c.priority_score >= ?")
        params.append(min_priority)
    if persona_type:
        conditions.append("c.persona_type = ?")
        params.append(persona_type)
    if stage:
        conditions.append("c.stage = ?")
        params.append(stage)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY c.priority_score DESC"

    rows = conn.execute(query, params).fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=selected, extrasaction="ignore")
    writer.writeheader()
    for r in rows:
        writer.writerow(dict(r))

    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    filename = f"occ-export-{timestamp}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# ─── EMAIL IDENTITIES ──────────────────────────────────────────

class EmailIdentityCreate(BaseModel):
    email_address: str
    display_name: Optional[str] = None
    daily_send_limit: Optional[int] = 25
    warmup_phase: Optional[int] = 1
    warmup_daily_cap: Optional[int] = 5

@app.post("/api/email/identities")
def create_identity(req: EmailIdentityCreate):
    """Create a new email sending identity."""
    return models.create_email_identity(req.model_dump())

@app.get("/api/email/identities")
def list_identities(active_only: bool = True):
    """List all email identities."""
    return models.list_email_identities(active_only)

@app.get("/api/email/identities/{identity_id}")
def get_identity(identity_id: str):
    """Get a specific email identity."""
    result = models.get_email_identity(identity_id)
    if not result:
        raise HTTPException(status_code=404, detail="Identity not found")
    return result

@app.post("/api/email/identities/{identity_id}/mark-sent")
def mark_email_sent(identity_id: str):
    """Rob confirms an email was sent manually."""
    pacing = models.check_pacing_ok(identity_id)
    if not pacing["ok"]:
        raise HTTPException(status_code=429, detail=pacing["reason"])
    return models.increment_send_count(identity_id)

@app.post("/api/email/identities/reset-daily")
def reset_daily():
    """Reset daily send counters (call at midnight)."""
    models.reset_daily_counts()
    return {"status": "reset"}


# ─── SUPPRESSION LIST ──────────────────────────────────────────

class SuppressionAdd(BaseModel):
    email_address: str
    reason: str
    source: Optional[str] = "manual"

@app.post("/api/email/suppression")
def add_suppression(req: SuppressionAdd):
    """Add email to suppression list."""
    return models.add_to_suppression(req.email_address, req.reason, req.source)

@app.get("/api/email/suppression")
def list_suppressions(limit: int = 100):
    """List suppressed emails."""
    return models.list_suppressed(limit)

@app.get("/api/email/suppression/check")
def check_suppression(email: str):
    """Check if email is suppressed."""
    return {"email": email, "suppressed": models.is_suppressed(email)}

@app.delete("/api/email/suppression")
def remove_suppression(email: str):
    """Remove email from suppression list."""
    removed = models.remove_from_suppression(email)
    if not removed:
        raise HTTPException(status_code=404, detail="Email not in suppression list")
    return {"removed": True, "email": email}


# ─── EMAIL EVENTS ──────────────────────────────────────────────

class EmailEventLog(BaseModel):
    contact_id: Optional[str] = None
    email_address: Optional[str] = None
    event_type: str  # bounce, hard_bounce, soft_bounce, opt_out, unsubscribe, reply, open, click
    event_source: Optional[str] = "manual"
    details: Optional[str] = None

@app.post("/api/email/events")
def log_event(req: EmailEventLog):
    """Log an email event (bounce, reply, open, etc.)."""
    return models.log_email_event(req.model_dump())

@app.get("/api/email/events")
def list_events(contact_id: str = None, event_type: str = None, limit: int = 50):
    """List email events."""
    return models.get_email_events(contact_id, event_type, limit)


# ─── PACING & DELIVERABILITY ──────────────────────────────────

@app.get("/api/email/pacing")
def get_pacing():
    """Get current pacing rules and status."""
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

@app.get("/api/email/health")
def email_health():
    """Get email channel health metrics."""
    return models.get_email_health()


# ─── LINKEDIN CHANNEL ──────────────────────────────────────────

class LinkedInEventLog(BaseModel):
    contact_id: str
    event_type: str  # inmail_sent, inmail_viewed, inmail_replied, connection_sent, connection_accepted, profile_viewed
    details: Optional[str] = None

@app.get("/api/linkedin/health")
def linkedin_health():
    """Get LinkedIn channel health metrics (daily/weekly stats, engagement rates)."""
    return models.get_linkedin_health()

@app.get("/api/linkedin/pacing")
def linkedin_pacing(daily_limit: int = 25):
    """Get current LinkedIn pacing status (sent today, limit, remaining)."""
    return models.check_linkedin_pacing(daily_limit)

@app.post("/api/linkedin/events")
def log_linkedin_event(req: LinkedInEventLog):
    """Log a LinkedIn event (inmail_sent, connection_request, etc.)."""
    return models.log_linkedin_event(req.contact_id, req.event_type, req.details)

@app.get("/api/linkedin/sequence/{contact_id}")
def get_linkedin_sequence(contact_id: str):
    """Get the full LinkedIn sequence status for a contact (which touches sent, which pending)."""
    contact = models.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    conn = models.get_db()

    # Get all LinkedIn touchpoints for this contact
    touchpoints = conn.execute("""
        SELECT tp.*, md.touch_number, md.subject_line, md.body
        FROM touchpoints tp
        LEFT JOIN message_drafts md ON tp.message_draft_id = md.id
        WHERE tp.contact_id=? AND tp.channel='linkedin'
        ORDER BY md.touch_number ASC
    """, (contact_id,)).fetchall()

    # Get pending followups on LinkedIn
    followups = conn.execute("""
        SELECT * FROM followups
        WHERE contact_id=? AND channel='linkedin' AND state='pending'
        ORDER BY touch_number ASC
    """, (contact_id,)).fetchall()

    # Get all LinkedIn messages (drafts) for this contact
    messages = conn.execute("""
        SELECT * FROM message_drafts
        WHERE contact_id=? AND channel='linkedin'
        ORDER BY touch_number ASC
    """, (contact_id,)).fetchall()

    # Get LinkedIn replies
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


# ─── SWARM CONTROL ─────────────────────────────────────────────

import threading

class SwarmStartRequest(BaseModel):
    contact_ids: Optional[List[str]] = None
    batch_id: Optional[str] = None
    max_workers: Optional[int] = 3
    channels: Optional[List[str]] = ["linkedin", "email"]

_active_swarms = {}

@app.post("/api/swarm/start")
def start_swarm(req: SwarmStartRequest):
    """Launch a swarm run for a batch of contacts."""
    if not models.is_feature_enabled("agent_swarm"):
        raise HTTPException(status_code=403, detail="Agent swarm is disabled")
    
    # Get contact IDs
    contact_ids = req.contact_ids
    if not contact_ids and req.batch_id:
        conn = models.get_db()
        rows = conn.execute("SELECT contact_id FROM batch_prospects WHERE batch_id=?",
                           (req.batch_id,)).fetchall()
        conn.close()
        contact_ids = [r["contact_id"] for r in rows]
    
    if not contact_ids:
        raise HTTPException(status_code=400, detail="No contacts specified")
    
    # Check for active swarm
    active = [s for s in _active_swarms.values() if s.get("status") == "running"]
    if active:
        raise HTTPException(status_code=409, detail="A swarm is already running")
    
    try:
        from src.agents.swarm_supervisor import SwarmSupervisor
    except ImportError:
        raise HTTPException(status_code=501, detail="SwarmSupervisor not available")
    
    config = {"max_workers": req.max_workers, "channels": req.channels}
    supervisor = SwarmSupervisor(config)
    
    def run_swarm():
        try:
            result = supervisor.run_batch(contact_ids, req.batch_id)
            has_errors = result.get("phases", {}).get("errors")
            _active_swarms[supervisor.run_id] = {
                "status": "error" if has_errors else "completed",
                "result": result
            }
        except Exception as e:
            _active_swarms[supervisor.run_id] = {"status": "error", "error": str(e)}
    
    thread = threading.Thread(target=run_swarm, daemon=True)
    thread.start()
    
    # Wait briefly for run_id to be set
    import time
    time.sleep(0.5)
    
    run_id = supervisor.run_id
    if run_id:
        _active_swarms[run_id] = {"status": "running", "supervisor": supervisor}
    
    return {"run_id": run_id, "status": "running", "contact_count": len(contact_ids)}

@app.get("/api/swarm/runs")
def list_swarm_runs():
    """List all swarm runs."""
    return models.list_swarm_runs()

@app.get("/api/swarm/runs/{run_id}")
def get_swarm_run(run_id: str):
    """Get details for a specific swarm run."""
    run = models.get_swarm_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Swarm run not found")
    tasks = models.get_swarm_tasks(run_id)
    return {**run, "tasks": tasks}

@app.post("/api/swarm/runs/{run_id}/cancel")
def cancel_swarm(run_id: str):
    """Cancel a running swarm."""
    if run_id in _active_swarms and _active_swarms[run_id].get("supervisor"):
        _active_swarms[run_id]["supervisor"].cancel()
        return {"cancelled": True}
    models.update_swarm_run(run_id, {"status": "cancelled"})
    return {"cancelled": True}


# ─── FEATURE FLAGS ─────────────────────────────────────────────

@app.get("/api/feature-flags")
def list_flags():
    """List all feature flags."""
    return models.list_feature_flags()

@app.post("/api/feature-flags/{flag_name}")
def toggle_flag(flag_name: str, enabled: bool = Query(True)):
    """Toggle a feature flag."""
    return models.set_feature_flag(flag_name, enabled)


# ─── SYSTEM HEALTH ─────────────────────────────────────────────

@app.get("/api/system/health")
def system_health():
    """Comprehensive system health check."""
    conn = models.get_db()
    
    # Table counts
    tables = {}
    for t in ["contacts", "accounts", "message_drafts", "touchpoints", "replies",
              "followups", "opportunities", "signals", "agent_runs", "batches",
              "email_identities", "suppression_list", "email_events",
              "swarm_runs", "swarm_tasks", "quality_scores", "feature_flags"]:
        try:
            tables[t] = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        except Exception:
            tables[t] = -1  # Table doesn't exist yet
    
    # Recent errors
    try:
        recent_errors = conn.execute("""
            SELECT id, agent_name, error_message, started_at
            FROM agent_runs WHERE status='error'
            ORDER BY started_at DESC LIMIT 5
        """).fetchall()
        recent_errors = [dict(e) for e in recent_errors]
    except Exception:
        recent_errors = []
    
    # Active runs
    try:
        active_runs = conn.execute(
            "SELECT COUNT(*) FROM agent_runs WHERE status='running'"
        ).fetchone()[0]
    except Exception:
        active_runs = 0
    
    # Active swarms
    try:
        active_swarms = conn.execute(
            "SELECT COUNT(*) FROM swarm_runs WHERE status='running'"
        ).fetchone()[0]
    except Exception:
        active_swarms = 0
    
    conn.close()
    
    email_health = models.get_email_health()
    
    return {
        "status": "healthy",
        "tables": tables,
        "active_agent_runs": active_runs,
        "active_swarms": active_swarms,
        "recent_errors": recent_errors,
        "email_health": email_health,
        "feature_flags": models.list_feature_flags(),
    }

@app.get("/api/insights/daily")
def daily_insights():
    """Get daily summary insights."""
    try:
        from src.agents.swarm_supervisor import InsightsAgent
        return InsightsAgent.daily_summary()
    except (ImportError, Exception):
        # Return expected structure with default values if InsightsAgent unavailable
        return {
            "activity": {
                "touches_sent": 0,
                "replies_received": 0,
                "meetings_booked": 0
            },
            "pending": {
                "due_followups": 0,
                "pending_approvals": 0
            }
        }

@app.get("/api/insights/weekly")
def weekly_insights():
    """Get weekly review insights."""
    try:
        from src.agents.swarm_supervisor import InsightsAgent
        return InsightsAgent.weekly_review()
    except ImportError:
        return {"status": "insights_unavailable"}

