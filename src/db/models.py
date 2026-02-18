"""
Outreach Command Center - Data Access Layer
Provides CRUD operations for all 15 tables via a clean Python API.
"""

import sqlite3
import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Optional


DB_PATH = os.environ.get("OCC_DB_PATH", os.path.join(os.path.dirname(__file__), "../../outreach.db"))


def get_db():
    """Get a database connection with row_factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Use DELETE journal mode in test environment to avoid WAL locking
    journal_mode = os.environ.get("OCC_JOURNAL_MODE", "WAL")
    conn.execute(f"PRAGMA journal_mode={journal_mode}")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def gen_id(prefix=""):
    """Generate a prefixed UUID."""
    short = uuid.uuid4().hex[:12]
    return f"{prefix}_{short}" if prefix else short


# ─── ACCOUNTS ───────────────────────────────────────────────────

def create_account(data: dict) -> dict:
    conn = get_db()
    aid = data.get("id", gen_id("acc"))
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO accounts (id, name, domain, industry, sub_industry, employee_count,
            employee_band, tier, known_tools, linkedin_company_url, website_url,
            buyer_intent, buyer_intent_date, annual_revenue, funding_stage,
            last_funding_date, last_funding_amount, hq_location, notes, research_freshness,
            created_at, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        aid, data.get("name"), data.get("domain"), data.get("industry"),
        data.get("sub_industry"), data.get("employee_count"), data.get("employee_band"),
        data.get("tier"), json.dumps(data.get("known_tools", [])),
        data.get("linkedin_company_url"), data.get("website_url"),
        data.get("buyer_intent", 0), data.get("buyer_intent_date"),
        data.get("annual_revenue"), data.get("funding_stage"),
        data.get("last_funding_date"), data.get("last_funding_amount"),
        data.get("hq_location"), data.get("notes"), data.get("research_freshness"),
        now, now
    ))
    conn.commit()
    row = conn.execute("SELECT * FROM accounts WHERE id=?", (aid,)).fetchone()
    conn.close()
    return dict(row)


def get_account(account_id: str) -> Optional[dict]:
    conn = get_db()
    row = conn.execute("SELECT * FROM accounts WHERE id=?", (account_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def list_accounts(limit=100, offset=0, industry=None) -> list:
    conn = get_db()
    query = "SELECT * FROM accounts"
    params = []
    if industry:
        query += " WHERE industry=?"
        params.append(industry)
    query += " ORDER BY updated_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_account(account_id: str, data: dict) -> Optional[dict]:
    conn = get_db()
    data["updated_at"] = datetime.utcnow().isoformat()
    fields = ", ".join(f"{k}=?" for k in data.keys())
    values = list(data.values()) + [account_id]
    conn.execute(f"UPDATE accounts SET {fields} WHERE id=?", values)
    conn.commit()
    row = conn.execute("SELECT * FROM accounts WHERE id=?", (account_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ─── CONTACTS ───────────────────────────────────────────────────

def create_contact(data: dict) -> dict:
    conn = get_db()
    cid = data.get("id", gen_id("con"))
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO contacts (id, account_id, first_name, last_name, title, persona_type,
            seniority_level, email, email_verified, linkedin_url, phone, location, timezone,
            tenure_months, recently_hired, previous_company, previous_title, stage,
            priority_score, priority_factors, personalization_score, predicted_objection,
            objection_response, status, do_not_contact, dnc_reason, source, created_at, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        cid, data.get("account_id"), data["first_name"], data["last_name"],
        data.get("title"), data.get("persona_type"), data.get("seniority_level"),
        data.get("email"), data.get("email_verified", 0), data.get("linkedin_url"),
        data.get("phone"), data.get("location"), data.get("timezone"),
        data.get("tenure_months"), data.get("recently_hired", 0),
        data.get("previous_company"), data.get("previous_title"),
        data.get("stage", "new"), data.get("priority_score", 3),
        json.dumps(data.get("priority_factors", {})),
        data.get("personalization_score"), data.get("predicted_objection"),
        data.get("objection_response"), data.get("status", "active"),
        data.get("do_not_contact", 0), data.get("dnc_reason"),
        data.get("source", "sales_nav"), now, now
    ))
    conn.commit()
    row = conn.execute("SELECT * FROM contacts WHERE id=?", (cid,)).fetchone()
    conn.close()
    return dict(row)


def get_contact(contact_id: str) -> Optional[dict]:
    conn = get_db()
    row = conn.execute("""
        SELECT c.*, a.name as company_name, a.industry as company_industry,
               a.employee_count as company_size, a.domain as company_domain
        FROM contacts c
        LEFT JOIN accounts a ON c.account_id = a.id
        WHERE c.id=?
    """, (contact_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def list_contacts(limit=100, offset=0, stage=None, min_priority=None,
                  persona_type=None, account_id=None) -> list:
    conn = get_db()
    query = """
        SELECT c.*, a.name as company_name, a.industry as company_industry
        FROM contacts c
        LEFT JOIN accounts a ON c.account_id = a.id
        WHERE 1=1
    """
    params = []
    if stage:
        query += " AND c.stage=?"
        params.append(stage)
    if min_priority:
        query += " AND c.priority_score>=?"
        params.append(min_priority)
    if persona_type:
        query += " AND c.persona_type=?"
        params.append(persona_type)
    if account_id:
        query += " AND c.account_id=?"
        params.append(account_id)
    query += " ORDER BY c.priority_score DESC, c.updated_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_contact(contact_id: str, data: dict) -> Optional[dict]:
    conn = get_db()
    data["updated_at"] = datetime.utcnow().isoformat()
    fields = ", ".join(f"{k}=?" for k in data.keys())
    values = list(data.values()) + [contact_id]
    conn.execute(f"UPDATE contacts SET {fields} WHERE id=?", values)
    conn.commit()
    row = conn.execute("SELECT * FROM contacts WHERE id=?", (contact_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ─── ICP SCORING ────────────────────────────────────────────────

PRIORITY_WEIGHTS = {
    "buyer_intent": 2,
    "qa_title": 1,
    "top_vertical": 1,
    "recently_hired": 1,
    "digital_transformation": 1,
    "competitor_tool": 1,
    "vp_eng_50k_minus": -1,
}

TOP_VERTICALS = {"fintech", "saas", "healthcare", "retail", "telecom", "pharma", "e-commerce"}
QA_TITLES = {"qa manager", "qa lead", "director of qa", "head of qa", "vp quality",
             "sr director quality", "quality engineering manager", "sdet lead",
             "automation lead", "vp quality engineering", "director quality engineering"}
COMPETITOR_TOOLS = {"selenium", "cypress", "playwright", "tosca", "katalon", "testim",
                    "mabl", "sauce labs", "browserstack", "lambdatest", "appium"}


def compute_priority_score(contact: dict, account: dict) -> dict:
    """Compute priority score (1-5) based on signals."""
    score = 0
    factors = {}

    # Buyer intent
    if account.get("buyer_intent"):
        score += PRIORITY_WEIGHTS["buyer_intent"]
        factors["buyer_intent"] = True

    # QA title
    title_lower = (contact.get("title") or "").lower()
    if any(qa in title_lower for qa in QA_TITLES):
        score += PRIORITY_WEIGHTS["qa_title"]
        factors["qa_title"] = True

    # Top vertical
    industry_lower = (account.get("industry") or "").lower()
    if any(v in industry_lower for v in TOP_VERTICALS):
        score += PRIORITY_WEIGHTS["top_vertical"]
        factors["top_vertical"] = True

    # Recently hired
    if contact.get("recently_hired"):
        score += PRIORITY_WEIGHTS["recently_hired"]
        factors["recently_hired"] = True

    # Competitor tool
    known_tools = account.get("known_tools", "[]")
    if isinstance(known_tools, str):
        try:
            known_tools = json.loads(known_tools)
        except json.JSONDecodeError:
            known_tools = []
    if any(t.lower() in COMPETITOR_TOOLS for t in known_tools):
        score += PRIORITY_WEIGHTS["competitor_tool"]
        factors["competitor_tool"] = True

    # VP Eng at large company penalty
    emp = account.get("employee_count") or 0
    if emp >= 50000 and "vp" in title_lower and "quality" not in title_lower and "qa" not in title_lower:
        score += PRIORITY_WEIGHTS["vp_eng_50k_minus"]
        factors["vp_eng_large_co_penalty"] = True

    # Clamp to 1-5
    score = max(1, min(5, score))

    return {"score": score, "factors": factors}


def score_and_save(contact_id: str) -> dict:
    """Score a contact and persist the result."""
    contact = get_contact(contact_id)
    if not contact:
        return {"error": "Contact not found"}
    account = get_account(contact["account_id"]) if contact.get("account_id") else {}
    result = compute_priority_score(contact, account or {})
    update_contact(contact_id, {
        "priority_score": result["score"],
        "priority_factors": json.dumps(result["factors"])
    })
    return result


# ─── MESSAGE DRAFTS ─────────────────────────────────────────────

def create_message_draft(data: dict) -> dict:
    conn = get_db()
    mid = data.get("id", gen_id("msg"))
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO message_drafts (id, contact_id, batch_id, channel, touch_number,
            touch_type, subject_line, body, version, personalization_score, proof_point_used,
            pain_hook, opener_style, ask_style, word_count, qc_passed, qc_flags, qc_run_id,
            approval_status, ab_group, ab_variable, agent_run_id, created_at, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        mid, data.get("contact_id"), data.get("batch_id"), data["channel"],
        data.get("touch_number"), data["touch_type"], data.get("subject_line"),
        data["body"], data.get("version", 1), data.get("personalization_score"),
        data.get("proof_point_used"), data.get("pain_hook"), data.get("opener_style"),
        data.get("ask_style"), data.get("word_count"), data.get("qc_passed"),
        json.dumps(data.get("qc_flags", [])), data.get("qc_run_id"),
        data.get("approval_status", "draft"), data.get("ab_group"),
        data.get("ab_variable"), data.get("agent_run_id"), now, now
    ))
    conn.commit()
    row = conn.execute("SELECT * FROM message_drafts WHERE id=?", (mid,)).fetchone()
    conn.close()
    return dict(row)


def get_messages_for_contact(contact_id: str) -> list:
    conn = get_db()
    rows = conn.execute("""
        SELECT * FROM message_drafts WHERE contact_id=?
        ORDER BY touch_number ASC, version DESC
    """, (contact_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_messages(batch_id=None, channel=None, approval_status=None, limit=100) -> list:
    conn = get_db()
    query = """
        SELECT md.*, c.first_name, c.last_name, c.title as contact_title,
               a.name as company_name
        FROM message_drafts md
        LEFT JOIN contacts c ON md.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        WHERE 1=1
    """
    params = []
    if batch_id:
        query += " AND md.batch_id=?"
        params.append(batch_id)
    if channel:
        query += " AND md.channel=?"
        params.append(channel)
    if approval_status:
        query += " AND md.approval_status=?"
        params.append(approval_status)
    query += " ORDER BY md.created_at DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── TOUCHPOINTS ────────────────────────────────────────────────

def log_touchpoint(data: dict) -> dict:
    conn = get_db()
    tid = gen_id("tp")
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO touchpoints (id, contact_id, message_draft_id, channel,
            touch_number, sent_at, outcome, call_duration_seconds, call_notes,
            confirmed_by_user, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (
        tid, data["contact_id"], data.get("message_draft_id"), data["channel"],
        data.get("touch_number"), data.get("sent_at", now), data.get("outcome"),
        data.get("call_duration_seconds"), data.get("call_notes"),
        data.get("confirmed_by_user", 1), now
    ))
    conn.commit()

    # Update contact stage based on touch
    stage_map = {1: "touched", 2: "touched", 3: "sequencing", 4: "sequencing", 5: "sequencing", 6: "break_up_sent"}
    touch_num = data.get("touch_number", 1)
    if touch_num in stage_map:
        update_contact(data["contact_id"], {"stage": stage_map[touch_num]})

    row = conn.execute("SELECT * FROM touchpoints WHERE id=?", (tid,)).fetchone()
    conn.close()
    return dict(row)


# ─── REPLIES ────────────────────────────────────────────────────

def log_reply(data: dict) -> dict:
    conn = get_db()
    rid = gen_id("rep")
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO replies (id, contact_id, touchpoint_id, channel, intent, reply_tag,
            summary, raw_text, referral_name, referral_title, recommended_next_step,
            next_step_taken, replied_at, handled_at, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        rid, data["contact_id"], data.get("touchpoint_id"), data.get("channel"),
        data.get("intent"), data.get("reply_tag"), data.get("summary"),
        data.get("raw_text"), data.get("referral_name"), data.get("referral_title"),
        data.get("recommended_next_step"), data.get("next_step_taken"),
        data.get("replied_at", now), data.get("handled_at"), now
    ))
    conn.commit()

    # Update contact stage
    intent = data.get("intent", "").lower()
    if intent == "positive":
        update_contact(data["contact_id"], {"stage": "replied_positive"})
    elif intent == "negative":
        update_contact(data["contact_id"], {"stage": "replied_negative"})
    elif intent == "referral":
        update_contact(data["contact_id"], {"stage": "referred"})
    else:
        update_contact(data["contact_id"], {"stage": "replied"})

    row = conn.execute("SELECT * FROM replies WHERE id=?", (rid,)).fetchone()
    conn.close()
    return dict(row)


# ─── OPPORTUNITIES ──────────────────────────────────────────────

def create_opportunity(data: dict) -> dict:
    conn = get_db()
    oid = gen_id("opp")
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO opportunities (id, contact_id, account_id, meeting_date, meeting_held,
            meeting_outcome, opportunity_created_date, opportunity_created, status,
            pipeline_value, trigger_touchpoint_id, trigger_reply_id, attribution_channel,
            attribution_touch_number, attribution_proof_point, attribution_pain_hook,
            attribution_opener_style, attribution_personalization_score, attribution_ab_group,
            attribution_ab_variable, ae_name, ae_feedback, disqualification_reason, notes,
            created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        oid, data["contact_id"], data.get("account_id"), data.get("meeting_date"),
        data.get("meeting_held", 0), data.get("meeting_outcome"),
        data.get("opportunity_created_date"), data.get("opportunity_created", 0),
        data.get("status", "meeting_booked"), data.get("pipeline_value"),
        data.get("trigger_touchpoint_id"), data.get("trigger_reply_id"),
        data.get("attribution_channel"), data.get("attribution_touch_number"),
        data.get("attribution_proof_point"), data.get("attribution_pain_hook"),
        data.get("attribution_opener_style"), data.get("attribution_personalization_score"),
        data.get("attribution_ab_group"), data.get("attribution_ab_variable"),
        data.get("ae_name"), data.get("ae_feedback"), data.get("disqualification_reason"),
        data.get("notes"), now
    ))
    conn.commit()

    # Update contact stage
    update_contact(data["contact_id"], {"stage": "meeting_booked"})

    row = conn.execute("SELECT * FROM opportunities WHERE id=?", (oid,)).fetchone()
    conn.close()
    return dict(row)


# ─── FOLLOWUPS ──────────────────────────────────────────────────

def schedule_followup(contact_id: str, touch_number: int, channel: str, days_from_now: int) -> dict:
    conn = get_db()
    fid = gen_id("fu")
    due = (datetime.utcnow() + timedelta(days=days_from_now)).isoformat()
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO followups (id, contact_id, touch_number, channel, due_date, state,
            message_draft_id, reminder_sent, created_at, completed_at)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (fid, contact_id, touch_number, channel, due, "pending", None, 0, now, None))
    conn.commit()
    row = conn.execute("SELECT * FROM followups WHERE id=?", (fid,)).fetchone()
    conn.close()
    return dict(row)


def get_due_followups(as_of=None) -> list:
    conn = get_db()
    cutoff = as_of or datetime.utcnow().isoformat()
    rows = conn.execute("""
        SELECT f.*, c.first_name, c.last_name, c.title as contact_title,
               a.name as company_name
        FROM followups f
        LEFT JOIN contacts c ON f.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        WHERE f.state='pending' AND f.due_date <= ?
        ORDER BY f.due_date ASC
    """, (cutoff,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── BATCHES ────────────────────────────────────────────────────

def create_batch(data: dict) -> dict:
    conn = get_db()
    bid = gen_id("bat")
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO batches (id, batch_number, created_date, prospect_count, ab_variable,
            ab_description, pre_brief, mix_ratio, status, html_file_path, metrics, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        bid, data.get("batch_number"), data.get("created_date", now[:10]),
        data.get("prospect_count", 0), data.get("ab_variable"),
        data.get("ab_description"), data.get("pre_brief"),
        json.dumps(data.get("mix_ratio", {})), data.get("status", "building"),
        data.get("html_file_path"), json.dumps(data.get("metrics", {})), now
    ))
    conn.commit()
    row = conn.execute("SELECT * FROM batches WHERE id=?", (bid,)).fetchone()
    conn.close()
    return dict(row)


# ─── AGENT RUNS ─────────────────────────────────────────────────

def start_agent_run(run_type: str, agent_name: str, contact_id=None, batch_id=None,
                    inputs=None, parent_run_id=None) -> dict:
    conn = get_db()
    rid = gen_id("run")
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO agent_runs (id, run_type, agent_name, contact_id, batch_id, inputs,
            outputs, sources_used, decisions, tokens_used, duration_ms, status,
            error_message, parent_run_id, started_at, completed_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        rid, run_type, agent_name, contact_id, batch_id,
        json.dumps(inputs or {}), '{}', '[]', '{}',
        0, 0, "running", None, parent_run_id, now, None
    ))
    conn.commit()
    conn.close()
    return {"id": rid, "status": "running"}


def complete_agent_run(run_id: str, outputs: dict, sources: list = None,
                       decisions: dict = None, tokens: int = 0, error: str = None) -> dict:
    conn = get_db()
    now = datetime.utcnow().isoformat()
    status = "error" if error else "completed"
    conn.execute("""
        UPDATE agent_runs SET outputs=?, sources_used=?, decisions=?, tokens_used=?,
            status=?, error_message=?, completed_at=?
        WHERE id=?
    """, (
        json.dumps(outputs), json.dumps(sources or []), json.dumps(decisions or {}),
        tokens, status, error, now, run_id
    ))
    conn.commit()
    row = conn.execute("SELECT * FROM agent_runs WHERE id=?", (run_id,)).fetchone()
    conn.close()
    return dict(row) if row else {}


# ─── RESEARCH SNAPSHOTS ────────────────────────────────────────

def save_research(data: dict) -> dict:
    conn = get_db()
    rid = gen_id("res")
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO research_snapshots (id, contact_id, account_id, entity_type, headline,
            summary, career_history, responsibilities, tech_stack_signals, pain_indicators,
            recent_activity, company_products, company_metrics, company_news, hiring_signals,
            sources, confidence_score, agent_run_id, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        rid, data.get("contact_id"), data.get("account_id"), data["entity_type"],
        data.get("headline"), data.get("summary"),
        json.dumps(data.get("career_history", [])), data.get("responsibilities"),
        json.dumps(data.get("tech_stack_signals", [])),
        json.dumps(data.get("pain_indicators", [])),
        data.get("recent_activity"), json.dumps(data.get("company_products", [])),
        json.dumps(data.get("company_metrics", {})), data.get("company_news"),
        data.get("hiring_signals"), json.dumps(data.get("sources", [])),
        data.get("confidence_score", 3), data.get("agent_run_id"), now
    ))
    conn.commit()
    row = conn.execute("SELECT * FROM research_snapshots WHERE id=?", (rid,)).fetchone()
    conn.close()
    return dict(row)


# ─── SIGNALS ────────────────────────────────────────────────────

def create_signal(data: dict) -> dict:
    conn = get_db()
    sid = gen_id("sig")
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO signals (id, account_id, contact_id, signal_type, description,
            source_url, detected_at, expires_at, acted_on, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (
        sid, data.get("account_id"), data.get("contact_id"), data["signal_type"],
        data.get("description"), data.get("source_url"),
        data.get("detected_at", now), data.get("expires_at"),
        data.get("acted_on", 0), now
    ))
    conn.commit()
    row = conn.execute("SELECT * FROM signals WHERE id=?", (sid,)).fetchone()
    conn.close()
    return dict(row)


# ─── EXPERIMENTS ────────────────────────────────────────────────

def create_experiment(data: dict) -> dict:
    conn = get_db()
    eid = gen_id("exp")
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO experiments (id, name, variable, group_a_desc, group_b_desc, status,
            batches_included, group_a_sent, group_a_replies, group_a_meetings, group_a_opps,
            group_b_sent, group_b_replies, group_b_meetings, group_b_opps, winner,
            conclusion, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        eid, data["name"], data.get("variable"), data.get("group_a_desc"),
        data.get("group_b_desc"), data.get("status", "active"),
        json.dumps(data.get("batches_included", [])),
        0, 0, 0, 0, 0, 0, 0, 0, None, None, now
    ))
    conn.commit()
    row = conn.execute("SELECT * FROM experiments WHERE id=?", (eid,)).fetchone()
    conn.close()
    return dict(row)


# ─── AUDIT LOG ──────────────────────────────────────────────────

def audit(table_name: str, record_id: str, action: str,
          old_values: dict = None, new_values: dict = None, changed_by: str = "system"):
    conn = get_db()
    conn.execute("""
        INSERT INTO audit_log (table_name, record_id, action, changed_by, old_values, new_values)
        VALUES (?,?,?,?,?,?)
    """, (table_name, record_id, action, changed_by,
          json.dumps(old_values) if old_values else None,
          json.dumps(new_values) if new_values else None))
    conn.commit()
    conn.close()


# ─── ANALYTICS QUERIES ──────────────────────────────────────────

def get_dashboard_stats() -> dict:
    """Get high-level stats for the home page."""
    conn = get_db()
    stats = {}

    stats["total_contacts"] = conn.execute("SELECT COUNT(*) FROM contacts WHERE status='active'").fetchone()[0]
    stats["total_accounts"] = conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]
    stats["touches_sent"] = conn.execute("SELECT COUNT(*) FROM touchpoints").fetchone()[0]
    stats["total_replies"] = conn.execute("SELECT COUNT(*) FROM replies").fetchone()[0]
    stats["positive_replies"] = conn.execute("SELECT COUNT(*) FROM replies WHERE intent='positive'").fetchone()[0]
    stats["meetings_booked"] = conn.execute("SELECT COUNT(*) FROM opportunities WHERE status IN ('meeting_booked','meeting_held','opportunity_created')").fetchone()[0]
    stats["opportunities_created"] = conn.execute("SELECT COUNT(*) FROM opportunities WHERE opportunity_created=1").fetchone()[0]
    stats["pending_followups"] = conn.execute("SELECT COUNT(*) FROM followups WHERE state='pending' AND due_date<=datetime('now')").fetchone()[0]
    stats["active_batches"] = conn.execute("SELECT COUNT(*) FROM batches WHERE status IN ('building','active')").fetchone()[0]

    # Reply rate
    if stats["touches_sent"] > 0:
        stats["reply_rate"] = round(stats["total_replies"] / stats["touches_sent"] * 100, 1)
    else:
        stats["reply_rate"] = 0

    # Meeting rate (from replies)
    if stats["total_replies"] > 0:
        stats["meeting_rate"] = round(stats["meetings_booked"] / stats["total_replies"] * 100, 1)
    else:
        stats["meeting_rate"] = 0

    conn.close()
    return stats


def get_reply_analytics() -> dict:
    """Get reply analytics broken down by various dimensions."""
    conn = get_db()
    analytics = {}

    # By reply tag
    rows = conn.execute("""
        SELECT reply_tag, COUNT(*) as cnt FROM replies
        WHERE reply_tag IS NOT NULL GROUP BY reply_tag ORDER BY cnt DESC
    """).fetchall()
    analytics["by_reply_tag"] = [dict(r) for r in rows]

    # By channel
    rows = conn.execute("""
        SELECT channel, COUNT(*) as cnt FROM replies
        WHERE channel IS NOT NULL GROUP BY channel ORDER BY cnt DESC
    """).fetchall()
    analytics["by_channel"] = [dict(r) for r in rows]

    # By persona type (through contacts)
    rows = conn.execute("""
        SELECT c.persona_type, COUNT(*) as cnt FROM replies r
        JOIN contacts c ON r.contact_id = c.id
        WHERE c.persona_type IS NOT NULL GROUP BY c.persona_type ORDER BY cnt DESC
    """).fetchall()
    analytics["by_persona"] = [dict(r) for r in rows]

    # By proof point (through message drafts)
    rows = conn.execute("""
        SELECT md.proof_point_used, COUNT(*) as cnt FROM replies r
        JOIN touchpoints tp ON r.touchpoint_id = tp.id
        JOIN message_drafts md ON tp.message_draft_id = md.id
        WHERE md.proof_point_used IS NOT NULL GROUP BY md.proof_point_used ORDER BY cnt DESC
    """).fetchall()
    analytics["by_proof_point"] = [dict(r) for r in rows]

    conn.close()
    return analytics


def get_action_queue() -> list:
    """Get today's action queue - due followups + hot prospects not yet touched."""
    items = []

    # Due followups
    followups = get_due_followups()
    for f in followups:
        items.append({
            "type": "followup",
            "priority": "high",
            "contact_name": f"{f.get('first_name','')} {f.get('last_name','')}",
            "company": f.get("company_name", ""),
            "action": f"Send Touch {f['touch_number']} ({f['channel']})",
            "due": f["due_date"],
            "contact_id": f["contact_id"],
            "followup_id": f["id"]
        })

    # Hot prospects (priority 5) not yet touched
    conn = get_db()
    rows = conn.execute("""
        SELECT c.*, a.name as company_name FROM contacts c
        LEFT JOIN accounts a ON c.account_id = a.id
        WHERE c.priority_score = 5 AND c.stage = 'new' AND c.status = 'active'
        ORDER BY c.created_at ASC
    """).fetchall()
    conn.close()

    for r in rows:
        row = dict(r)
        items.append({
            "type": "hot_prospect",
            "priority": "hot",
            "contact_name": f"{row['first_name']} {row['last_name']}",
            "company": row.get("company_name", ""),
            "action": "Start sequence (InMail + Call)",
            "due": "today",
            "contact_id": row["id"]
        })

    return sorted(items, key=lambda x: 0 if x["priority"] == "hot" else 1)


# ─── PREP CARD ─────────────────────────────────────────────────

def get_prep_card(contact_id: str) -> dict:
    """Aggregate research + messages + touchpoints + reply data for meeting prep."""
    contact = get_contact(contact_id)
    if not contact:
        return {"error": "Contact not found"}

    account = get_account(contact["account_id"]) if contact.get("account_id") else {}

    conn = get_db()

    # Person research
    person_row = conn.execute("""
        SELECT * FROM research_snapshots
        WHERE contact_id=? AND entity_type='person'
        ORDER BY created_at DESC LIMIT 1
    """, (contact_id,)).fetchone()
    person = {}
    if person_row:
        pr = dict(person_row)
        person = {
            "headline": pr.get("headline", ""),
            "about": pr.get("summary", ""),
            "responsibilities": pr.get("responsibilities", ""),
            "career_history": json.loads(pr["career_history"]) if pr.get("career_history") else [],
        }

    # Company research
    company_row = conn.execute("""
        SELECT * FROM research_snapshots
        WHERE account_id=? AND entity_type='company'
        ORDER BY created_at DESC LIMIT 1
    """, (contact.get("account_id", ""),)).fetchone()
    company = {}
    if company_row:
        cr = dict(company_row)
        company = {
            "description": cr.get("summary", ""),
            "known_tools": json.loads(cr["tech_stack_signals"]) if cr.get("tech_stack_signals") else [],
            "recent_news": cr.get("company_news", ""),
            "hiring_signals": cr.get("hiring_signals", ""),
        }

    # Messages
    messages = conn.execute("""
        SELECT * FROM message_drafts WHERE contact_id=?
        ORDER BY touch_number ASC
    """, (contact_id,)).fetchall()
    messages = [dict(m) for m in messages]

    # Reply data
    replies = conn.execute("""
        SELECT * FROM replies WHERE contact_id=?
        ORDER BY replied_at DESC
    """, (contact_id,)).fetchall()
    replies = [dict(r) for r in replies]

    # Signals
    signals = conn.execute("""
        SELECT * FROM signals
        WHERE contact_id=? OR account_id=?
        ORDER BY detected_at DESC
    """, (contact_id, contact.get("account_id", ""))).fetchall()
    signals = [dict(s) for s in signals]

    conn.close()

    # What triggered the reply
    reply_trigger = ""
    if replies:
        reply_trigger = replies[0].get("reply_tag", "Unknown")

    # Pain hypothesis from messages
    pain = ""
    for m in messages:
        if m.get("pain_hook"):
            pain = m["pain_hook"]
            break

    # Known tools
    known_tools = company.get("known_tools", [])
    if isinstance(known_tools, str):
        try:
            known_tools = json.loads(known_tools)
        except (json.JSONDecodeError, TypeError):
            known_tools = []

    return {
        "contact": contact,
        "account": account or {},
        "person_research": person,
        "company_research": company,
        "messages": messages,
        "replies": replies,
        "signals": signals,
        "reply_trigger": reply_trigger,
        "pain_hypothesis": pain,
        "known_tools": known_tools,
    }


# ─── BATCH SUMMARY ────────────────────────────────────────────

def get_batch_summary(batch_id: str) -> dict:
    """Batch-level stats: sent, replied, meetings, by persona/vertical."""
    conn = get_db()

    batch = conn.execute("SELECT * FROM batches WHERE id=?", (batch_id,)).fetchone()
    if not batch:
        conn.close()
        return {"error": "Batch not found"}

    # Contact count
    contact_count = conn.execute(
        "SELECT COUNT(*) FROM batch_prospects WHERE batch_id=?", (batch_id,)
    ).fetchone()[0]

    # Persona breakdown
    persona_rows = conn.execute("""
        SELECT c.persona_type, COUNT(*) as cnt
        FROM batch_prospects bp
        JOIN contacts c ON bp.contact_id = c.id
        WHERE bp.batch_id=?
        GROUP BY c.persona_type
    """, (batch_id,)).fetchall()

    # Vertical breakdown
    vertical_rows = conn.execute("""
        SELECT a.industry, COUNT(*) as cnt
        FROM batch_prospects bp
        JOIN contacts c ON bp.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        WHERE bp.batch_id=?
        GROUP BY a.industry
    """, (batch_id,)).fetchall()

    # Messages
    msg_count = conn.execute(
        "SELECT COUNT(*) FROM message_drafts WHERE batch_id=?", (batch_id,)
    ).fetchone()[0]

    qc_passed = conn.execute(
        "SELECT COUNT(*) FROM message_drafts WHERE batch_id=? AND qc_passed=1", (batch_id,)
    ).fetchone()[0]

    # Touches sent from this batch
    touch_count = conn.execute("""
        SELECT COUNT(*) FROM touchpoints tp
        JOIN message_drafts md ON tp.message_draft_id = md.id
        WHERE md.batch_id=?
    """, (batch_id,)).fetchone()[0]

    # Replies from this batch
    reply_count = conn.execute("""
        SELECT COUNT(*) FROM replies r
        JOIN contacts c ON r.contact_id = c.id
        JOIN batch_prospects bp ON bp.contact_id = c.id AND bp.batch_id=?
    """, (batch_id,)).fetchone()[0]

    # Meetings from this batch
    meeting_count = conn.execute("""
        SELECT COUNT(*) FROM opportunities o
        JOIN contacts c ON o.contact_id = c.id
        JOIN batch_prospects bp ON bp.contact_id = c.id AND bp.batch_id=?
        WHERE o.status IN ('meeting_booked','meeting_held')
    """, (batch_id,)).fetchone()[0]

    conn.close()

    return {
        "batch": dict(batch),
        "contact_count": contact_count,
        "personas": {r["persona_type"]: r["cnt"] for r in persona_rows},
        "verticals": {r["industry"] or "Other": r["cnt"] for r in vertical_rows},
        "messages_generated": msg_count,
        "messages_qc_passed": qc_passed,
        "touches_sent": touch_count,
        "replies": reply_count,
        "meetings": meeting_count,
        "reply_rate": round(reply_count / max(touch_count, 1) * 100, 1),
    }


# ─── INTELLIGENCE DATA ────────────────────────────────────────

def get_intelligence_data() -> dict:
    """Aggregated analytics for Intelligence page."""
    conn = get_db()
    intelligence = {}

    # Reply rates by persona
    rows = conn.execute("""
        SELECT c.persona_type,
               COUNT(DISTINCT tp.id) as touches,
               COUNT(DISTINCT r.id) as replies
        FROM contacts c
        LEFT JOIN touchpoints tp ON tp.contact_id = c.id
        LEFT JOIN replies r ON r.contact_id = c.id
        WHERE c.persona_type IS NOT NULL
        GROUP BY c.persona_type
    """).fetchall()
    intelligence["by_persona"] = [
        {"persona": r["persona_type"], "touches": r["touches"], "replies": r["replies"],
         "rate": round(r["replies"] / max(r["touches"], 1) * 100, 1)}
        for r in rows
    ]

    # Reply rates by vertical
    rows = conn.execute("""
        SELECT a.industry,
               COUNT(DISTINCT tp.id) as touches,
               COUNT(DISTINCT r.id) as replies
        FROM contacts c
        LEFT JOIN accounts a ON c.account_id = a.id
        LEFT JOIN touchpoints tp ON tp.contact_id = c.id
        LEFT JOIN replies r ON r.contact_id = c.id
        WHERE a.industry IS NOT NULL
        GROUP BY a.industry
    """).fetchall()
    intelligence["by_vertical"] = [
        {"vertical": r["industry"], "touches": r["touches"], "replies": r["replies"],
         "rate": round(r["replies"] / max(r["touches"], 1) * 100, 1)}
        for r in rows
    ]

    # Reply rates by proof point
    rows = conn.execute("""
        SELECT md.proof_point_used,
               COUNT(DISTINCT tp.id) as touches,
               COUNT(DISTINCT r.id) as replies
        FROM message_drafts md
        LEFT JOIN touchpoints tp ON tp.message_draft_id = md.id
        LEFT JOIN replies r ON r.touchpoint_id = tp.id
        WHERE md.proof_point_used IS NOT NULL
        GROUP BY md.proof_point_used
    """).fetchall()
    intelligence["by_proof_point"] = [
        {"proof_point": r["proof_point_used"], "touches": r["touches"], "replies": r["replies"],
         "rate": round(r["replies"] / max(r["touches"], 1) * 100, 1)}
        for r in rows
    ]

    # Reply rates by personalization score
    rows = conn.execute("""
        SELECT md.personalization_score,
               COUNT(DISTINCT tp.id) as touches,
               COUNT(DISTINCT r.id) as replies
        FROM message_drafts md
        LEFT JOIN touchpoints tp ON tp.message_draft_id = md.id
        LEFT JOIN replies r ON r.touchpoint_id = tp.id
        WHERE md.personalization_score IS NOT NULL
        GROUP BY md.personalization_score
    """).fetchall()
    intelligence["by_personalization"] = [
        {"score": r["personalization_score"], "touches": r["touches"], "replies": r["replies"],
         "rate": round(r["replies"] / max(r["touches"], 1) * 100, 1)}
        for r in rows
    ]

    conn.close()
    return intelligence


# ─── SYNC FROM HTML ────────────────────────────────────────────

def sync_html_status(contact_id: str, stage: str = None,
                     reply_tag: str = None, notes: str = None) -> dict:
    """Accept status updates from HTML localStorage sync."""
    update = {}
    if stage:
        update["stage"] = stage

    if update:
        update_contact(contact_id, update)

    # Log reply tag if provided
    if reply_tag:
        log_reply({
            "contact_id": contact_id,
            "reply_tag": reply_tag,
            "summary": notes or "",
        })

    return {"success": True, "synced": True, "contact_id": contact_id}


# ─── EXPERIMENT RESULTS ────────────────────────────────────────

def get_experiment_results(experiment_id: str) -> dict:
    """A/B test metrics with sample sizes."""
    conn = get_db()

    exp = conn.execute("SELECT * FROM experiments WHERE id=?", (experiment_id,)).fetchone()
    if not exp:
        conn.close()
        return {"error": "Experiment not found"}
    exp = dict(exp)

    variable = exp.get("variable", "")

    # Get batch IDs for this experiment
    try:
        batch_ids = json.loads(exp.get("batches_included", "[]"))
    except (json.JSONDecodeError, TypeError):
        batch_ids = []

    if not batch_ids:
        conn.close()
        return {"experiment": exp, "results": {"A": {}, "B": {}}, "conclusion": "No batches linked"}

    placeholders = ",".join("?" for _ in batch_ids)

    # Group A metrics
    a_touches = conn.execute(f"""
        SELECT COUNT(DISTINCT tp.id) FROM touchpoints tp
        JOIN message_drafts md ON tp.message_draft_id = md.id
        WHERE md.batch_id IN ({placeholders}) AND md.ab_group='A'
    """, batch_ids).fetchone()[0]

    a_replies = conn.execute(f"""
        SELECT COUNT(DISTINCT r.id) FROM replies r
        JOIN touchpoints tp ON r.touchpoint_id = tp.id
        JOIN message_drafts md ON tp.message_draft_id = md.id
        WHERE md.batch_id IN ({placeholders}) AND md.ab_group='A'
    """, batch_ids).fetchone()[0]

    # Group B metrics
    b_touches = conn.execute(f"""
        SELECT COUNT(DISTINCT tp.id) FROM touchpoints tp
        JOIN message_drafts md ON tp.message_draft_id = md.id
        WHERE md.batch_id IN ({placeholders}) AND md.ab_group='B'
    """, batch_ids).fetchone()[0]

    b_replies = conn.execute(f"""
        SELECT COUNT(DISTINCT r.id) FROM replies r
        JOIN touchpoints tp ON r.touchpoint_id = tp.id
        JOIN message_drafts md ON tp.message_draft_id = md.id
        WHERE md.batch_id IN ({placeholders}) AND md.ab_group='B'
    """, batch_ids).fetchone()[0]

    conn.close()

    a_rate = round(a_replies / max(a_touches, 1) * 100, 1)
    b_rate = round(b_replies / max(b_touches, 1) * 100, 1)

    # Simple conclusion
    min_sample = 10
    if a_touches < min_sample or b_touches < min_sample:
        conclusion = f"Insufficient data (need {min_sample}+ touches per group)"
    elif a_rate > b_rate * 1.2:
        conclusion = f"Group A winning ({a_rate}% vs {b_rate}%)"
    elif b_rate > a_rate * 1.2:
        conclusion = f"Group B winning ({b_rate}% vs {a_rate}%)"
    else:
        conclusion = f"No significant difference ({a_rate}% vs {b_rate}%)"

    return {
        "experiment": exp,
        "results": {
            "A": {"desc": exp.get("group_a_desc", ""), "touches": a_touches, "replies": a_replies, "rate": a_rate},
            "B": {"desc": exp.get("group_b_desc", ""), "touches": b_touches, "replies": b_replies, "rate": b_rate},
        },
        "conclusion": conclusion,
    }


# ─── EMAIL IDENTITIES ──────────────────────────────────────────

def create_email_identity(data: dict) -> dict:
    """Create a new email identity (sender account)."""
    conn = get_db()
    eid = data.get("id", gen_id("eid"))
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO email_identities (id, email_address, display_name, daily_send_limit,
            warmup_phase, warmup_daily_cap, is_active, notes, created_at, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (eid, data["email_address"], data.get("display_name"), data.get("daily_send_limit", 25),
          data.get("warmup_phase", 1), data.get("warmup_daily_cap", 5),
          data.get("is_active", 1), data.get("notes"), now, now))
    conn.commit()
    row = conn.execute("SELECT * FROM email_identities WHERE id=?", (eid,)).fetchone()
    conn.close()
    return dict(row) if row else {}


def get_email_identity(identity_id: str) -> Optional[dict]:
    """Get an email identity by ID."""
    conn = get_db()
    row = conn.execute("SELECT * FROM email_identities WHERE id=?", (identity_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def list_email_identities(active_only=True) -> list:
    """List all email identities, optionally filtered to active only."""
    conn = get_db()
    query = "SELECT * FROM email_identities"
    if active_only:
        query += " WHERE is_active=1"
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def increment_send_count(identity_id: str) -> dict:
    """Increment send counters for an email identity."""
    conn = get_db()
    conn.execute("""
        UPDATE email_identities
        SET total_sent_today = total_sent_today + 1,
            total_sent_all_time = total_sent_all_time + 1,
            updated_at = datetime('now')
        WHERE id=?
    """, (identity_id,))
    conn.commit()
    row = conn.execute("SELECT * FROM email_identities WHERE id=?", (identity_id,)).fetchone()
    conn.close()
    return dict(row) if row else {}


def reset_daily_counts():
    """Reset daily send counts for all email identities."""
    conn = get_db()
    conn.execute("UPDATE email_identities SET total_sent_today=0, updated_at=datetime('now')")
    conn.commit()
    conn.close()


# ─── SUPPRESSION LIST ──────────────────────────────────────────

def add_to_suppression(email_address: str, reason: str, source: str = "manual") -> dict:
    """Add an email address to the suppression list."""
    conn = get_db()
    sid = gen_id("sup")
    try:
        conn.execute("""
            INSERT INTO suppression_list (id, email_address, reason, source, added_at)
            VALUES (?,?,?,?,datetime('now'))
        """, (sid, email_address.lower().strip(), reason, source))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return {"already_exists": True, "email": email_address}
    row = conn.execute("SELECT * FROM suppression_list WHERE id=?", (sid,)).fetchone()
    conn.close()
    return dict(row)


def is_suppressed(email_address: str) -> bool:
    """Check if an email address is on the suppression list."""
    conn = get_db()
    row = conn.execute("SELECT 1 FROM suppression_list WHERE email_address=?",
                       (email_address.lower().strip(),)).fetchone()
    conn.close()
    return row is not None


def list_suppressed(limit=100) -> list:
    """List suppressed email addresses."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM suppression_list ORDER BY added_at DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def remove_from_suppression(email_address: str) -> bool:
    """Remove an email from the suppression list."""
    conn = get_db()
    result = conn.execute("DELETE FROM suppression_list WHERE email_address=?",
                          (email_address.lower().strip(),))
    conn.commit()
    conn.close()
    return result.rowcount > 0


# ─── EMAIL EVENTS ──────────────────────────────────────────────

def log_email_event(data: dict) -> dict:
    """Log an email event (bounce, opt-out, etc.)."""
    conn = get_db()
    eid = gen_id("evt")
    conn.execute("""
        INSERT INTO email_events (id, contact_id, email_address, event_type,
            event_source, details, raw_data, created_at)
        VALUES (?,?,?,?,?,?,?,datetime('now'))
    """, (eid, data.get("contact_id"), data.get("email_address"), data["event_type"],
          data.get("event_source", "manual"), data.get("details"),
          json.dumps(data.get("raw_data")) if data.get("raw_data") else None))
    conn.commit()
    
    # Auto-add to suppression on hard bounce or opt-out
    if data["event_type"] in ("hard_bounce", "opt_out", "unsubscribe") and data.get("email_address"):
        add_to_suppression(data["email_address"], data["event_type"], "auto")
    
    row = conn.execute("SELECT * FROM email_events WHERE id=?", (eid,)).fetchone()
    conn.close()
    return dict(row)


def get_email_events(contact_id: str = None, event_type: str = None, limit=50) -> list:
    """Get email events, optionally filtered by contact or event type."""
    conn = get_db()
    query = "SELECT * FROM email_events WHERE 1=1"
    params = []
    if contact_id:
        query += " AND contact_id=?"
        params.append(contact_id)
    if event_type:
        query += " AND event_type=?"
        params.append(event_type)
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── PACING ────────────────────────────────────────────────────

def get_pacing_rules(channel: str = "email") -> list:
    """Get active pacing rules for a channel."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM pacing_rules WHERE channel=? AND is_active=1",
                        (channel,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def check_pacing_ok(identity_id: str) -> dict:
    """Check if we can send another email given pacing rules."""
    identity = get_email_identity(identity_id)
    if not identity:
        return {"ok": False, "reason": "Identity not found"}
    
    rules = get_pacing_rules("email")
    rule = rules[0] if rules else {"max_per_day": 25, "max_per_hour": 5}
    
    # Check daily limit
    effective_limit = rule.get("max_per_day", 25)
    if identity.get("warmup_phase"):
        effective_limit = min(effective_limit, identity.get("warmup_daily_cap", 5))
    
    if identity.get("total_sent_today", 0) >= effective_limit:
        return {"ok": False, "reason": f"Daily limit reached ({effective_limit})",
                "sent_today": identity["total_sent_today"], "limit": effective_limit}
    
    return {"ok": True, "sent_today": identity.get("total_sent_today", 0),
            "limit": effective_limit, "remaining": effective_limit - identity.get("total_sent_today", 0)}


# ─── SWARM RUNS ────────────────────────────────────────────────

def create_swarm_run(swarm_type: str, batch_id: str = None, config: dict = None) -> dict:
    """Create a new swarm run."""
    conn = get_db()
    rid = gen_id("swarm")
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO swarm_runs (id, swarm_type, batch_id, config, status, started_at, created_at)
        VALUES (?,?,?,?,?,?,?)
    """, (rid, swarm_type, batch_id, json.dumps(config or {}), "running", now, now))
    conn.commit()
    row = conn.execute("SELECT * FROM swarm_runs WHERE id=?", (rid,)).fetchone()
    conn.close()
    return dict(row) if row else {}


def update_swarm_run(run_id: str, data: dict) -> dict:
    """Update a swarm run."""
    conn = get_db()
    fields = ", ".join(f"{k}=?" for k in data.keys())
    values = list(data.values()) + [run_id]
    conn.execute(f"UPDATE swarm_runs SET {fields} WHERE id=?", values)
    conn.commit()
    row = conn.execute("SELECT * FROM swarm_runs WHERE id=?", (run_id,)).fetchone()
    conn.close()
    return dict(row) if row else {}


def get_swarm_run(run_id: str) -> Optional[dict]:
    """Get a swarm run by ID."""
    conn = get_db()
    row = conn.execute("SELECT * FROM swarm_runs WHERE id=?", (run_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def list_swarm_runs(limit=20) -> list:
    """List recent swarm runs."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM swarm_runs ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── SWARM TASKS ───────────────────────────────────────────────

def create_swarm_task(data: dict) -> dict:
    """Create a new swarm task within a run."""
    conn = get_db()
    tid = gen_id("stask")
    now = datetime.utcnow().isoformat()
    dedupe_key = data.get("dedupe_key") or f"{data.get('agent_name')}:{data.get('task_type')}:{data.get('contact_id')}"
    
    # Check for duplicate
    existing = conn.execute("SELECT id FROM swarm_tasks WHERE dedupe_key=? AND status IN ('pending','running','completed')",
                            (dedupe_key,)).fetchone()
    if existing:
        conn.close()
        return {"duplicate": True, "existing_id": existing[0]}
    
    conn.execute("""
        INSERT INTO swarm_tasks (id, swarm_run_id, agent_name, task_type, contact_id,
            input_data, output_data, status, dedupe_key, parent_task_id, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (tid, data.get("swarm_run_id"), data["agent_name"], data["task_type"],
          data.get("contact_id"), json.dumps(data.get("input_data", {})),
          '{}', "pending", dedupe_key, data.get("parent_task_id"), now))
    conn.commit()
    row = conn.execute("SELECT * FROM swarm_tasks WHERE id=?", (tid,)).fetchone()
    conn.close()
    return dict(row)


def update_swarm_task(task_id: str, data: dict) -> dict:
    """Update a swarm task."""
    conn = get_db()
    if "output_data" in data and isinstance(data["output_data"], dict):
        data["output_data"] = json.dumps(data["output_data"])
    fields = ", ".join(f"{k}=?" for k in data.keys())
    values = list(data.values()) + [task_id]
    conn.execute(f"UPDATE swarm_tasks SET {fields} WHERE id=?", values)
    conn.commit()
    row = conn.execute("SELECT * FROM swarm_tasks WHERE id=?", (task_id,)).fetchone()
    conn.close()
    return dict(row) if row else {}


def get_swarm_tasks(swarm_run_id: str, status: str = None) -> list:
    """Get tasks in a swarm run, optionally filtered by status."""
    conn = get_db()
    query = "SELECT * FROM swarm_tasks WHERE swarm_run_id=?"
    params = [swarm_run_id]
    if status:
        query += " AND status=?"
        params.append(status)
    query += " ORDER BY created_at ASC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── QUALITY SCORES ────────────────────────────────────────────

def save_quality_score(data: dict) -> dict:
    """Save a quality score from the QA agent."""
    conn = get_db()
    qid = gen_id("qs")
    conn.execute("""
        INSERT INTO quality_scores (id, swarm_task_id, message_draft_id, grounding_score,
            tone_score, compliance_score, hallucination_flags, overall_pass, reviewer_notes,
            created_at)
        VALUES (?,?,?,?,?,?,?,?,?,datetime('now'))
    """, (qid, data.get("swarm_task_id"), data.get("message_draft_id"),
          data.get("grounding_score", 0), data.get("tone_score", 0),
          data.get("compliance_score", 0), json.dumps(data.get("hallucination_flags", [])),
          data.get("overall_pass", 0), data.get("reviewer_notes")))
    conn.commit()
    row = conn.execute("SELECT * FROM quality_scores WHERE id=?", (qid,)).fetchone()
    conn.close()
    return dict(row)


# ─── FEATURE FLAGS ─────────────────────────────────────────────

def is_feature_enabled(flag_name: str) -> bool:
    """Check if a feature flag is enabled."""
    conn = get_db()
    row = conn.execute("SELECT enabled FROM feature_flags WHERE flag_name=?", (flag_name,)).fetchone()
    conn.close()
    return bool(row and row[0])


def set_feature_flag(flag_name: str, enabled: bool) -> dict:
    """Enable or disable a feature flag."""
    conn = get_db()
    conn.execute("UPDATE feature_flags SET enabled=?, updated_at=datetime('now') WHERE flag_name=?",
                 (1 if enabled else 0, flag_name))
    conn.commit()
    row = conn.execute("SELECT * FROM feature_flags WHERE flag_name=?", (flag_name,)).fetchone()
    conn.close()
    return dict(row) if row else {}


def list_feature_flags() -> list:
    """List all feature flags."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM feature_flags ORDER BY flag_name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── DELIVERABILITY ANALYTICS ──────────────────────────────────

def get_email_health() -> dict:
    """Get email channel health metrics."""
    conn = get_db()

    total_sent = conn.execute("SELECT COALESCE(SUM(total_sent_all_time),0) FROM email_identities").fetchone()[0]
    bounces = conn.execute("SELECT COUNT(*) FROM email_events WHERE event_type IN ('hard_bounce','soft_bounce')").fetchone()[0]
    opt_outs = conn.execute("SELECT COUNT(*) FROM email_events WHERE event_type IN ('opt_out','unsubscribe')").fetchone()[0]
    suppressed = conn.execute("SELECT COUNT(*) FROM suppression_list").fetchone()[0]

    # Today's sends
    today_sent = conn.execute("SELECT COALESCE(SUM(total_sent_today),0) FROM email_identities").fetchone()[0]

    # Active identities
    active_ids = conn.execute("SELECT COUNT(*) FROM email_identities WHERE is_active=1").fetchone()[0]

    conn.close()

    bounce_rate = round(bounces / max(total_sent, 1) * 100, 2)
    opt_out_rate = round(opt_outs / max(total_sent, 1) * 100, 2)

    return {
        "total_sent": total_sent,
        "today_sent": today_sent,
        "bounces": bounces,
        "opt_outs": opt_outs,
        "suppressed_contacts": suppressed,
        "bounce_rate": bounce_rate,
        "opt_out_rate": opt_out_rate,
        "active_identities": active_ids,
        "health_status": "good" if bounce_rate < 2 and opt_out_rate < 1 else "warning" if bounce_rate < 5 else "critical"
    }


# ─── LINKEDIN CHANNEL SUPPORT ──────────────────────────────────

def get_linkedin_daily_stats(date: str = None) -> dict:
    """Get LinkedIn InMail stats for a specific date (defaults to today)."""
    if not date:
        date = datetime.utcnow().strftime("%Y-%m-%d")

    conn = get_db()

    # Count InMails sent today
    inmail_sent = conn.execute("""
        SELECT COUNT(*) FROM touchpoints
        WHERE channel='linkedin' AND sent_at >= ? AND sent_at < datetime(?, '+1 day')
    """, (date, date)).fetchone()[0]

    # Count InMail replies today
    inmail_replies = conn.execute("""
        SELECT COUNT(*) FROM replies
        WHERE channel='linkedin' AND replied_at >= ? AND replied_at < datetime(?, '+1 day')
    """, (date, date)).fetchone()[0]

    # Count connection requests sent today
    conn_requests = conn.execute("""
        SELECT COUNT(*) FROM signals
        WHERE signal_type='linkedin_connection_sent' AND detected_at >= ? AND detected_at < datetime(?, '+1 day')
    """, (date, date)).fetchone()[0]

    conn.close()

    return {
        "date": date,
        "inmails_sent": inmail_sent,
        "inmails_replied": inmail_replies,
        "connection_requests": conn_requests,
        "reply_rate": round(inmail_replies / max(inmail_sent, 1) * 100, 1),
    }


def check_linkedin_pacing(daily_limit: int = 25) -> dict:
    """Check if we can send another LinkedIn InMail given daily pacing limit.

    Returns dict with 'ok' (bool), 'sent_today', 'limit', 'remaining'.
    """
    today = datetime.utcnow().strftime("%Y-%m-%d")

    conn = get_db()
    sent_today = conn.execute("""
        SELECT COUNT(*) FROM touchpoints
        WHERE channel='linkedin' AND sent_at >= ? AND sent_at < datetime(?, '+1 day')
    """, (today, today)).fetchone()[0]
    conn.close()

    remaining = max(0, daily_limit - sent_today)
    return {
        "ok": sent_today < daily_limit,
        "sent_today": sent_today,
        "limit": daily_limit,
        "remaining": remaining,
    }


def log_linkedin_event(contact_id: str, event_type: str, details: str = None) -> dict:
    """Log a LinkedIn-specific event (inmail_sent, inmail_viewed, inmail_replied,
    connection_sent, connection_accepted, profile_viewed).

    Uses the signals table to track LinkedIn channel events.
    """
    conn = get_db()
    sid = gen_id("sig")
    now = datetime.utcnow().isoformat()

    event_type_map = {
        "inmail_sent": "linkedin_inmail_sent",
        "inmail_viewed": "linkedin_inmail_viewed",
        "inmail_replied": "linkedin_inmail_replied",
        "connection_sent": "linkedin_connection_sent",
        "connection_accepted": "linkedin_connection_accepted",
        "profile_viewed": "linkedin_profile_viewed",
    }

    signal_type = event_type_map.get(event_type, event_type)

    conn.execute("""
        INSERT INTO signals (id, contact_id, signal_type, description, detected_at, created_at)
        VALUES (?,?,?,?,?,?)
    """, (sid, contact_id, signal_type, details or "", now, now))
    conn.commit()

    row = conn.execute("SELECT * FROM signals WHERE id=?", (sid,)).fetchone()
    conn.close()
    return dict(row) if row else {}


def get_linkedin_health() -> dict:
    """Get LinkedIn channel health metrics (daily/weekly stats, engagement rates)."""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    week_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")

    conn = get_db()

    # Today's stats
    today_stats = get_linkedin_daily_stats(today)

    # Weekly stats
    week_inmails = conn.execute("""
        SELECT COUNT(*) FROM touchpoints
        WHERE channel='linkedin' AND sent_at >= ?
    """, (week_ago,)).fetchone()[0]

    week_replies = conn.execute("""
        SELECT COUNT(DISTINCT contact_id) FROM replies
        WHERE channel='linkedin' AND replied_at >= ?
    """, (week_ago,)).fetchone()[0]

    # Total LinkedIn touchpoints
    total_inmails = conn.execute("""
        SELECT COUNT(*) FROM touchpoints WHERE channel='linkedin'
    """).fetchone()[0]

    # Connection request acceptance rate (via signals)
    connections_sent = conn.execute("""
        SELECT COUNT(*) FROM signals
        WHERE signal_type='linkedin_connection_sent'
    """).fetchone()[0]

    connections_accepted = conn.execute("""
        SELECT COUNT(*) FROM signals
        WHERE signal_type='linkedin_connection_accepted'
    """).fetchone()[0]

    conn.close()

    week_reply_rate = round(week_replies / max(week_inmails, 1) * 100, 1)
    connection_acceptance_rate = round(connections_accepted / max(connections_sent, 1) * 100, 1)

    return {
        "today": today_stats,
        "this_week": {
            "inmails_sent": week_inmails,
            "replies": week_replies,
            "reply_rate": week_reply_rate,
        },
        "all_time": {
            "total_inmails": total_inmails,
            "connections_sent": connections_sent,
            "connections_accepted": connections_accepted,
            "connection_acceptance_rate": connection_acceptance_rate,
        },
        "health_status": "good" if week_reply_rate >= 1.0 else "warning" if week_reply_rate >= 0.5 else "low",
    }
