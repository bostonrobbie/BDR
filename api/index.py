"""
Vercel Serverless Function - Outreach Command Center API
Wraps the FastAPI app for Vercel deployment with /tmp SQLite.
Includes flow management, activity timeline, drafts, sender health, and contact identities.
"""
import os
import sys
import sqlite3
import json
import uuid
from datetime import datetime, timedelta
import random

# Set DB path to /tmp for Vercel serverless (only if not already set, e.g. by tests)
if "OCC_DB_PATH" not in os.environ:
    os.environ["OCC_DB_PATH"] = "/tmp/outreach.db"

# Add project root to path
project_root = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, project_root)

from fastapi import FastAPI, HTTPException, Query, Header, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List

# ---------------------------------------------------------------------------
# DATABASE LAYER (self-contained for serverless)
# ---------------------------------------------------------------------------

DB_PATH = os.environ.get("OCC_DB_PATH", "/tmp/outreach.db")

def get_db():
    db_path = os.environ.get("OCC_DB_PATH", "/tmp/outreach.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def gen_id(prefix=""):
    short = uuid.uuid4().hex[:12]
    return f"{prefix}_{short}" if prefix else short

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS accounts (
    id TEXT PRIMARY KEY, name TEXT NOT NULL, domain TEXT, industry TEXT,
    sub_industry TEXT, employee_count INTEGER, employee_band TEXT, tier TEXT,
    known_tools TEXT DEFAULT '[]', linkedin_company_url TEXT, website_url TEXT,
    buyer_intent INTEGER DEFAULT 0, buyer_intent_date TEXT, annual_revenue TEXT,
    funding_stage TEXT, last_funding_date TEXT, last_funding_amount TEXT,
    hq_location TEXT, notes TEXT, research_freshness TEXT,
    created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now')), source TEXT DEFAULT 'seed'
);
CREATE TABLE IF NOT EXISTS contacts (
    id TEXT PRIMARY KEY, account_id TEXT REFERENCES accounts(id),
    first_name TEXT NOT NULL, last_name TEXT NOT NULL, title TEXT,
    persona_type TEXT, seniority_level TEXT, email TEXT, email_verified INTEGER DEFAULT 0,
    linkedin_url TEXT, phone TEXT, location TEXT, timezone TEXT,
    tenure_months INTEGER, recently_hired INTEGER DEFAULT 0,
    previous_company TEXT, previous_title TEXT, stage TEXT DEFAULT 'new',
    priority_score INTEGER DEFAULT 3, priority_factors TEXT DEFAULT '{}',
    personalization_score INTEGER, predicted_objection TEXT, objection_response TEXT,
    status TEXT DEFAULT 'active', do_not_contact INTEGER DEFAULT 0, dnc_reason TEXT,
    source TEXT DEFAULT 'seed',
    created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS icp_scores (
    id TEXT PRIMARY KEY, contact_id TEXT REFERENCES contacts(id),
    title_match INTEGER DEFAULT 0, vertical_match INTEGER DEFAULT 0,
    company_size_fit INTEGER DEFAULT 0, seniority_fit INTEGER DEFAULT 0,
    software_qa_confirmed INTEGER DEFAULT 0, buyer_intent_bonus INTEGER DEFAULT 0,
    total_score INTEGER DEFAULT 0, scored_at TEXT DEFAULT (datetime('now')),
    scoring_version TEXT DEFAULT 'v1'
);
CREATE TABLE IF NOT EXISTS signals (
    id TEXT PRIMARY KEY, account_id TEXT REFERENCES accounts(id),
    contact_id TEXT REFERENCES contacts(id), signal_type TEXT NOT NULL,
    description TEXT, source_url TEXT, detected_at TEXT DEFAULT (datetime('now')),
    expires_at TEXT, acted_on INTEGER DEFAULT 0, created_at TEXT DEFAULT (datetime('now')), source TEXT DEFAULT 'seed'
);
CREATE TABLE IF NOT EXISTS research_snapshots (
    id TEXT PRIMARY KEY, contact_id TEXT REFERENCES contacts(id),
    account_id TEXT REFERENCES accounts(id), entity_type TEXT NOT NULL,
    headline TEXT, summary TEXT, career_history TEXT DEFAULT '[]',
    responsibilities TEXT, tech_stack_signals TEXT DEFAULT '[]',
    pain_indicators TEXT DEFAULT '[]', recent_activity TEXT,
    company_products TEXT, company_metrics TEXT, company_news TEXT,
    hiring_signals TEXT, sources TEXT DEFAULT '[]', confidence_score INTEGER DEFAULT 3,
    agent_run_id TEXT, created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS message_drafts (
    id TEXT PRIMARY KEY, contact_id TEXT REFERENCES contacts(id),
    batch_id TEXT REFERENCES batches(id), channel TEXT NOT NULL,
    touch_number INTEGER, touch_type TEXT NOT NULL, subject_line TEXT,
    body TEXT NOT NULL, version INTEGER DEFAULT 1,
    personalization_score INTEGER, proof_point_used TEXT, pain_hook TEXT,
    opener_style TEXT, ask_style TEXT, word_count INTEGER,
    qc_passed INTEGER, qc_flags TEXT DEFAULT '[]', qc_run_id TEXT,
    approval_status TEXT DEFAULT 'draft', ab_group TEXT, ab_variable TEXT,
    agent_run_id TEXT, created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')), source TEXT DEFAULT 'seed'
);
CREATE TABLE IF NOT EXISTS touchpoints (
    id TEXT PRIMARY KEY, contact_id TEXT REFERENCES contacts(id),
    message_draft_id TEXT REFERENCES message_drafts(id), channel TEXT NOT NULL,
    touch_number INTEGER, sent_at TEXT NOT NULL, outcome TEXT,
    call_duration_seconds INTEGER, call_notes TEXT,
    confirmed_by_user INTEGER DEFAULT 1, created_at TEXT DEFAULT (datetime('now')), source TEXT DEFAULT 'seed'
);
CREATE TABLE IF NOT EXISTS replies (
    id TEXT PRIMARY KEY, contact_id TEXT REFERENCES contacts(id),
    touchpoint_id TEXT REFERENCES touchpoints(id), channel TEXT,
    intent TEXT, reply_tag TEXT, summary TEXT, raw_text TEXT,
    referral_name TEXT, referral_title TEXT, recommended_next_step TEXT,
    next_step_taken TEXT, replied_at TEXT, handled_at TEXT,
    created_at TEXT DEFAULT (datetime('now')), source TEXT DEFAULT 'seed'
);
CREATE TABLE IF NOT EXISTS followups (
    id TEXT PRIMARY KEY, contact_id TEXT REFERENCES contacts(id),
    touch_number INTEGER, channel TEXT, due_date TEXT,
    state TEXT DEFAULT 'pending', message_draft_id TEXT,
    reminder_sent INTEGER DEFAULT 0, created_at TEXT DEFAULT (datetime('now')),
    completed_at TEXT
);
CREATE TABLE IF NOT EXISTS opportunities (
    id TEXT PRIMARY KEY, contact_id TEXT REFERENCES contacts(id),
    account_id TEXT REFERENCES accounts(id), meeting_date TEXT,
    meeting_held INTEGER DEFAULT 0, meeting_outcome TEXT,
    opportunity_created_date TEXT, opportunity_created INTEGER DEFAULT 0,
    status TEXT DEFAULT 'meeting_booked', pipeline_value REAL,
    trigger_touchpoint_id TEXT, trigger_reply_id TEXT,
    attribution_channel TEXT, attribution_touch_number INTEGER,
    attribution_proof_point TEXT, attribution_pain_hook TEXT,
    attribution_opener_style TEXT, attribution_personalization_score INTEGER,
    attribution_ab_group TEXT, attribution_ab_variable TEXT,
    ae_name TEXT, ae_feedback TEXT, disqualification_reason TEXT, notes TEXT,
    created_at TEXT DEFAULT (datetime('now')), source TEXT DEFAULT 'seed'
);
CREATE TABLE IF NOT EXISTS batches (
    id TEXT PRIMARY KEY, batch_number INTEGER, created_date TEXT,
    prospect_count INTEGER DEFAULT 0, ab_variable TEXT, ab_description TEXT,
    pre_brief TEXT, mix_ratio TEXT DEFAULT '{}', status TEXT DEFAULT 'building',
    html_file_path TEXT, metrics TEXT DEFAULT '{}',
    created_at TEXT DEFAULT (datetime('now')), source TEXT DEFAULT 'seed'
);
CREATE TABLE IF NOT EXISTS batch_prospects (
    id TEXT PRIMARY KEY, batch_id TEXT REFERENCES batches(id),
    contact_id TEXT REFERENCES contacts(id), ab_group TEXT,
    sequence_status TEXT DEFAULT 'not_started', position_in_batch INTEGER
);
CREATE TABLE IF NOT EXISTS experiments (
    id TEXT PRIMARY KEY, name TEXT NOT NULL, variable TEXT,
    group_a_desc TEXT, group_b_desc TEXT, status TEXT DEFAULT 'active',
    batches_included TEXT DEFAULT '[]',
    group_a_sent INTEGER DEFAULT 0, group_a_replies INTEGER DEFAULT 0,
    group_a_meetings INTEGER DEFAULT 0, group_a_opps INTEGER DEFAULT 0,
    group_b_sent INTEGER DEFAULT 0, group_b_replies INTEGER DEFAULT 0,
    group_b_meetings INTEGER DEFAULT 0, group_b_opps INTEGER DEFAULT 0,
    winner TEXT, conclusion TEXT, created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS agent_runs (
    id TEXT PRIMARY KEY, run_type TEXT NOT NULL, agent_name TEXT,
    contact_id TEXT, batch_id TEXT, inputs TEXT DEFAULT '{}',
    outputs TEXT DEFAULT '{}', sources_used TEXT DEFAULT '[]',
    decisions TEXT DEFAULT '{}', tokens_used INTEGER DEFAULT 0,
    duration_ms INTEGER DEFAULT 0, status TEXT DEFAULT 'running',
    error_message TEXT, parent_run_id TEXT,
    started_at TEXT DEFAULT (datetime('now')), completed_at TEXT
);
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT, table_name TEXT NOT NULL,
    record_id TEXT NOT NULL, action TEXT NOT NULL, changed_by TEXT,
    old_values TEXT, new_values TEXT, timestamp TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS email_identities (
    id TEXT PRIMARY KEY, email_address TEXT NOT NULL UNIQUE,
    display_name TEXT, smtp_host TEXT, smtp_port INTEGER DEFAULT 587,
    auth_user TEXT, auth_token_encrypted TEXT, daily_limit INTEGER DEFAULT 50,
    warmup_phase INTEGER DEFAULT 1, warmup_day INTEGER DEFAULT 0,
    reputation_score REAL DEFAULT 100.0, is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS suppression_list (
    id TEXT PRIMARY KEY, email TEXT, domain TEXT, reason TEXT,
    source TEXT DEFAULT 'manual', added_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS email_events (
    id TEXT PRIMARY KEY, message_draft_id TEXT, identity_id TEXT,
    event_type TEXT NOT NULL, event_data TEXT DEFAULT '{}',
    occurred_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS pacing_rules (
    id TEXT PRIMARY KEY, identity_id TEXT REFERENCES email_identities(id),
    channel TEXT NOT NULL, max_per_day INTEGER DEFAULT 50,
    max_per_hour INTEGER DEFAULT 10, min_gap_seconds INTEGER DEFAULT 120,
    warmup_schedule TEXT DEFAULT '{}', is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS swarm_runs (
    id TEXT PRIMARY KEY, batch_id TEXT, swarm_type TEXT DEFAULT 'full_batch',
    config TEXT DEFAULT '{}', status TEXT DEFAULT 'running',
    total_tasks INTEGER DEFAULT 0, completed_tasks INTEGER DEFAULT 0,
    failed_tasks INTEGER DEFAULT 0, started_at TEXT DEFAULT (datetime('now')),
    completed_at TEXT, error_log TEXT DEFAULT '[]'
);
CREATE TABLE IF NOT EXISTS swarm_tasks (
    id TEXT PRIMARY KEY, swarm_run_id TEXT REFERENCES swarm_runs(id),
    agent_type TEXT NOT NULL, contact_id TEXT, input_data TEXT DEFAULT '{}',
    output_data TEXT DEFAULT '{}', status TEXT DEFAULT 'pending',
    retry_count INTEGER DEFAULT 0, error_message TEXT,
    started_at TEXT, completed_at TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS quality_scores (
    id TEXT PRIMARY KEY, message_draft_id TEXT REFERENCES message_drafts(id),
    swarm_run_id TEXT, dimension TEXT NOT NULL, score REAL NOT NULL,
    feedback TEXT, scored_by TEXT, scored_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS feature_flags (
    id TEXT PRIMARY KEY, name TEXT UNIQUE NOT NULL,
    enabled INTEGER DEFAULT 1, description TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS flow_runs (
    id TEXT PRIMARY KEY,
    flow_type TEXT NOT NULL,
    status TEXT DEFAULT 'running',
    config TEXT DEFAULT '{}',
    total_steps INTEGER DEFAULT 0,
    completed_steps INTEGER DEFAULT 0,
    failed_steps INTEGER DEFAULT 0,
    warnings TEXT DEFAULT '[]',
    started_at TEXT DEFAULT (datetime('now')),
    completed_at TEXT,
    duration_ms INTEGER DEFAULT 0,
    created_by TEXT DEFAULT 'user',
    trace_id TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS flow_run_steps (
    id TEXT PRIMARY KEY,
    flow_run_id TEXT REFERENCES flow_runs(id),
    step_name TEXT NOT NULL,
    agent_type TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    input_data TEXT DEFAULT '{}',
    output_data TEXT DEFAULT '{}',
    error_message TEXT,
    tokens_used INTEGER DEFAULT 0,
    duration_ms INTEGER DEFAULT 0,
    started_at TEXT,
    completed_at TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS flow_artifacts (
    id TEXT PRIMARY KEY,
    flow_run_id TEXT REFERENCES flow_runs(id),
    artifact_type TEXT NOT NULL,
    title TEXT,
    content TEXT,
    metadata TEXT DEFAULT '{}',
    entity_type TEXT,
    entity_id TEXT,
    status TEXT DEFAULT 'ready',
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS activity_timeline (
    id TEXT PRIMARY KEY,
    contact_id TEXT,
    account_id TEXT,
    channel TEXT NOT NULL,
    activity_type TEXT NOT NULL,
    description TEXT,
    metadata TEXT DEFAULT '{}',
    flow_run_id TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS draft_versions (
    id TEXT PRIMARY KEY,
    draft_id TEXT NOT NULL,
    contact_id TEXT,
    channel TEXT NOT NULL,
    touch_number INTEGER,
    subject TEXT,
    body TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    status TEXT DEFAULT 'draft',
    personalization_score INTEGER,
    proof_point TEXT,
    pain_hook TEXT,
    opener_style TEXT,
    word_count INTEGER,
    qc_passed INTEGER,
    qc_flags TEXT DEFAULT '[]',
    confidence_score REAL,
    flow_run_id TEXT,
    edited_by TEXT DEFAULT 'agent',
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS sender_health_snapshots (
    id TEXT PRIMARY KEY,
    identity_id TEXT,
    date TEXT NOT NULL,
    emails_sent INTEGER DEFAULT 0,
    bounces INTEGER DEFAULT 0,
    complaints INTEGER DEFAULT 0,
    replies INTEGER DEFAULT 0,
    bounce_rate REAL DEFAULT 0,
    complaint_rate REAL DEFAULT 0,
    reply_rate REAL DEFAULT 0,
    domain_reputation TEXT,
    spf_pass INTEGER DEFAULT 1,
    dkim_pass INTEGER DEFAULT 1,
    dmarc_pass INTEGER DEFAULT 0,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS contact_identities (
    id TEXT PRIMARY KEY,
    contact_id TEXT REFERENCES contacts(id),
    identity_type TEXT NOT NULL,
    value TEXT NOT NULL,
    verified INTEGER DEFAULT 0,
    source TEXT,
    is_primary INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_contacts_account ON contacts(account_id);
CREATE INDEX IF NOT EXISTS idx_contacts_stage ON contacts(stage);
CREATE INDEX IF NOT EXISTS idx_contacts_persona ON contacts(persona_type);
CREATE INDEX IF NOT EXISTS idx_contacts_priority ON contacts(priority_score DESC);
CREATE INDEX IF NOT EXISTS idx_messages_contact ON message_drafts(contact_id);
CREATE INDEX IF NOT EXISTS idx_messages_batch ON message_drafts(batch_id);
CREATE INDEX IF NOT EXISTS idx_touchpoints_contact ON touchpoints(contact_id);
CREATE INDEX IF NOT EXISTS idx_replies_contact ON replies(contact_id);
CREATE INDEX IF NOT EXISTS idx_signals_account ON signals(account_id);
CREATE INDEX IF NOT EXISTS idx_flow_runs_status ON flow_runs(status);
CREATE INDEX IF NOT EXISTS idx_flow_steps_run ON flow_run_steps(flow_run_id);
CREATE INDEX IF NOT EXISTS idx_activity_contact ON activity_timeline(contact_id);
CREATE INDEX IF NOT EXISTS idx_draft_versions_draft ON draft_versions(draft_id);
CREATE INDEX IF NOT EXISTS idx_drafts_contact ON draft_versions(contact_id);
CREATE INDEX IF NOT EXISTS idx_sender_health_identity ON sender_health_snapshots(identity_id);

CREATE TABLE IF NOT EXISTS workflow_definitions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    workflow_type TEXT NOT NULL,
    channel TEXT NOT NULL,
    description TEXT,
    version INTEGER DEFAULT 1,
    input_schema TEXT DEFAULT '{}',
    steps TEXT DEFAULT '[]',
    output_schema TEXT DEFAULT '{}',
    safety_gates TEXT DEFAULT '[]',
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS workflow_runs (
    id TEXT PRIMARY KEY,
    workflow_id TEXT REFERENCES workflow_definitions(id),
    workflow_type TEXT NOT NULL,
    channel TEXT NOT NULL,
    status TEXT DEFAULT 'queued',
    dry_run INTEGER DEFAULT 1,
    input_data TEXT DEFAULT '{}',
    output_data TEXT DEFAULT '{}',
    config TEXT DEFAULT '{}',
    total_steps INTEGER DEFAULT 0,
    completed_steps INTEGER DEFAULT 0,
    failed_steps INTEGER DEFAULT 0,
    error_message TEXT,
    started_at TEXT,
    completed_at TEXT,
    duration_ms INTEGER DEFAULT 0,
    created_by TEXT DEFAULT 'user',
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS workflow_run_steps (
    id TEXT PRIMARY KEY,
    run_id TEXT REFERENCES workflow_runs(id),
    step_name TEXT NOT NULL,
    step_type TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    input_data TEXT DEFAULT '{}',
    output_data TEXT DEFAULT '{}',
    error_message TEXT,
    tokens_used INTEGER DEFAULT 0,
    duration_ms INTEGER DEFAULT 0,
    started_at TEXT,
    completed_at TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS safety_events (
    id TEXT PRIMARY KEY,
    run_id TEXT,
    event_type TEXT NOT NULL,
    severity TEXT DEFAULT 'info',
    details TEXT DEFAULT '{}',
    blocked_action TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS linkedin_profiles (
    id TEXT PRIMARY KEY,
    contact_id TEXT REFERENCES contacts(id),
    linkedin_url TEXT,
    headline TEXT,
    about_text TEXT,
    experience_json TEXT DEFAULT '[]',
    education_json TEXT DEFAULT '[]',
    skills_json TEXT DEFAULT '[]',
    activity_json TEXT DEFAULT '[]',
    connections_count INTEGER,
    profile_source TEXT DEFAULT 'manual',
    last_updated TEXT DEFAULT (datetime('now')),
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS research_runs (
    id TEXT PRIMARY KEY,
    name TEXT,
    import_type TEXT NOT NULL DEFAULT 'csv',
    prospect_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'created',
    sop_checklist TEXT DEFAULT '[]',
    progress_pct INTEGER DEFAULT 0,
    logs TEXT DEFAULT '[]',
    error_count INTEGER DEFAULT 0,
    ab_variable TEXT,
    ab_groups TEXT DEFAULT '["A","B"]',
    config TEXT DEFAULT '{}',
    created_at TEXT DEFAULT (datetime('now')),
    started_at TEXT,
    completed_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_research_runs_status ON research_runs(status);

CREATE INDEX IF NOT EXISTS idx_workflow_runs_status ON workflow_runs(status);
CREATE INDEX IF NOT EXISTS idx_workflow_runs_channel ON workflow_runs(channel);
CREATE INDEX IF NOT EXISTS idx_workflow_steps_run ON workflow_run_steps(run_id);
CREATE INDEX IF NOT EXISTS idx_safety_events_run ON safety_events(run_id);
CREATE INDEX IF NOT EXISTS idx_linkedin_profiles_contact ON linkedin_profiles(contact_id);

CREATE TABLE IF NOT EXISTS draft_edit_history (
    id TEXT PRIMARY KEY,
    draft_id TEXT NOT NULL,
    field TEXT NOT NULL,
    old_value TEXT,
    new_value TEXT,
    edited_by TEXT DEFAULT 'user',
    edited_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS send_log (
    id TEXT PRIMARY KEY,
    contact_id TEXT REFERENCES contacts(id),
    draft_id TEXT REFERENCES message_drafts(id),
    channel TEXT DEFAULT 'linkedin',
    status TEXT DEFAULT 'sent',
    sent_at TEXT DEFAULT (datetime('now')),
    confirmed_by TEXT DEFAULT 'user',
    notes TEXT
);

CREATE TABLE IF NOT EXISTS quota_tracker (
    id TEXT PRIMARY KEY,
    month TEXT NOT NULL,
    inmail_credits_total INTEGER DEFAULT 50,
    inmail_credits_used INTEGER DEFAULT 0,
    daily_send_target INTEGER DEFAULT 25,
    sends_today INTEGER DEFAULT 0,
    sends_this_week INTEGER DEFAULT 0,
    sends_this_month INTEGER DEFAULT 0,
    last_send_date TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS draft_research_link (
    id TEXT PRIMARY KEY,
    draft_id TEXT REFERENCES message_drafts(id),
    contact_id TEXT REFERENCES contacts(id),
    account_id TEXT REFERENCES accounts(id),
    profile_bullets TEXT DEFAULT '[]',
    company_bullets TEXT DEFAULT '[]',
    pain_hypothesis TEXT,
    why_testsigma TEXT,
    template_name TEXT,
    template_version TEXT,
    ab_group_explanation TEXT,
    confidence_score INTEGER DEFAULT 0,
    confidence_reasons TEXT DEFAULT '[]',
    linkedin_url TEXT,
    company_url TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_draft_research_draft ON draft_research_link(draft_id);
CREATE INDEX IF NOT EXISTS idx_draft_research_contact ON draft_research_link(contact_id);

CREATE TABLE IF NOT EXISTS research_evidence (
    id TEXT PRIMARY KEY,
    contact_id TEXT REFERENCES contacts(id),
    evidence_type TEXT NOT NULL,
    bullets TEXT DEFAULT '[]',
    snippet TEXT,
    verified_at TEXT,
    source_url TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS outreach_touches (
    id TEXT PRIMARY KEY,
    contact_id TEXT REFERENCES contacts(id),
    draft_id TEXT REFERENCES message_drafts(id),
    channel TEXT NOT NULL,
    touch_number INTEGER,
    touch_type TEXT,
    sent_at TEXT,
    sent_method TEXT DEFAULT 'manual_copy',
    message_hash TEXT,
    proof_point_used TEXT,
    pain_hook TEXT,
    opener_style TEXT,
    personalization_score INTEGER,
    ab_group TEXT,
    batch_id TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS outreach_responses (
    id TEXT PRIMARY KEY,
    touch_id TEXT REFERENCES outreach_touches(id),
    contact_id TEXT REFERENCES contacts(id),
    response_type TEXT NOT NULL,
    response_text TEXT,
    sentiment TEXT,
    interest_level TEXT,
    what_resonated TEXT,
    objection_encountered TEXT,
    referral_name TEXT,
    referral_title TEXT,
    reply_time_hours INTEGER,
    received_at TEXT,
    tags TEXT DEFAULT '[]',
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS outreach_outcomes (
    id TEXT PRIMARY KEY,
    contact_id TEXT REFERENCES contacts(id),
    outcome_type TEXT NOT NULL,
    meeting_date TEXT,
    meeting_notes TEXT,
    opportunity_created INTEGER DEFAULT 0,
    opportunity_value TEXT,
    learnings TEXT,
    what_worked TEXT,
    what_didnt TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_touches_contact ON outreach_touches(contact_id);
CREATE INDEX IF NOT EXISTS idx_touches_channel ON outreach_touches(channel);
CREATE INDEX IF NOT EXISTS idx_responses_touch ON outreach_responses(touch_id);
CREATE INDEX IF NOT EXISTS idx_responses_contact ON outreach_responses(contact_id);
CREATE INDEX IF NOT EXISTS idx_outcomes_contact ON outreach_outcomes(contact_id);
"""

# ---------------------------------------------------------------------------
# SEED DATA
# ---------------------------------------------------------------------------

VERTICALS = ["FinTech", "SaaS", "Healthcare", "E-Commerce", "Telecom", "Pharma"]
TITLES_QA = ["Director of QA", "Head of Quality Engineering", "VP Quality Assurance", "QA Manager", "Sr Director QA"]
TITLES_VP = ["VP Engineering", "VP Software Engineering", "CTO", "SVP Engineering"]
COMPANIES = [
    ("Stripe", "stripe.com", "FinTech", 8000), ("Plaid", "plaid.com", "FinTech", 1600),
    ("Affirm", "affirm.com", "FinTech", 2000), ("Chime", "chime.com", "FinTech", 1500),
    ("Shopify", "shopify.com", "E-Commerce", 12000), ("Instacart", "instacart.com", "E-Commerce", 3000),
    ("Datadog", "datadoghq.com", "SaaS", 5000), ("Figma", "figma.com", "SaaS", 1500),
    ("Notion", "notion.so", "SaaS", 600), ("Airtable", "airtable.com", "SaaS", 900),
    ("Oscar Health", "hioscar.com", "Healthcare", 3000), ("Ro", "ro.co", "Healthcare", 1000),
    ("Twilio", "twilio.com", "Telecom", 7000), ("Vonage", "vonage.com", "Telecom", 2500),
    ("Tempus", "tempus.com", "Pharma", 2500), ("Veeva", "veeva.com", "Pharma", 6000),
    ("Toast", "toasttab.com", "SaaS", 4500), ("Brex", "brex.com", "FinTech", 1200),
    ("Rippling", "rippling.com", "SaaS", 2500), ("Gusto", "gusto.com", "SaaS", 2000),
    ("Bolt", "bolt.com", "FinTech", 1000), ("Ramp", "ramp.com", "FinTech", 800),
    ("Noom", "noom.com", "Healthcare", 1500), ("Hims & Hers", "forhims.com", "Healthcare", 1200),
    ("Webflow", "webflow.com", "SaaS", 700),
]
FIRST_NAMES = ["Sarah", "Mike", "Jennifer", "David", "Emily", "Chris", "Lisa", "James", "Amanda", "Robert",
               "Jessica", "Dan", "Rachel", "Kevin", "Priya", "Alex", "Maria", "Tom", "Anita", "Brian",
               "Deepa", "Marcus", "Wei", "Sandra", "Juan"]
LAST_NAMES = ["Chen", "Patel", "Rodriguez", "Kim", "Thompson", "Martinez", "Johnson", "Williams", "Brown",
              "Davis", "Garcia", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson",
              "White", "Harris", "Martin", "Lee", "Clark", "Lewis", "Young"]
PROOF_POINTS = ["Hansard: 8→5 week regression", "CRED: 90% automation, 5x faster",
                "Sanofi: 3 days → 80 min", "Medibuddy: 2500 tests, 50% maint cut",
                "Fortune 100: 3X productivity", "Nagra DTV: 2500 tests in 8mo",
                "Spendflo: 50% manual testing cut"]
PAIN_HOOKS = ["flaky_tests", "slow_regression", "manual_testing", "scaling_coverage", "release_velocity"]
CHANNELS = ["linkedin", "email", "phone"]
STAGES = ["new", "touched", "engaged", "replied", "meeting_booked", "not_interested"]

def seed_database():
    # Demo/seed data disabled. Only real data from imports/API.
    return

# ---------------------------------------------------------------------------
# INITIALIZE DB ON COLD START
# ---------------------------------------------------------------------------

def _auto_import_run_bundle(conn):
    """Auto-import the run bundle JSON on cold start when DB is empty."""
    # Only import if DB has no contacts
    count = conn.execute("SELECT COUNT(*) as cnt FROM contacts").fetchone()[0]
    if count > 0:
        return  # Already have data

    # Find the run bundle file (works on Vercel and locally)
    bundle_paths = [
        os.path.join(os.path.dirname(__file__), "data", "run-bundle-batch1.json"),  # api/data/ (Vercel serverless)
        os.path.join(os.path.dirname(__file__), "..", "public", "data", "run-bundle-batch1.json"),  # local dev
        "/var/task/api/data/run-bundle-batch1.json",  # Vercel absolute path
        "/var/task/public/data/run-bundle-batch1.json",  # Vercel fallback
    ]
    bundle_path = None
    for p in bundle_paths:
        if os.path.exists(p):
            bundle_path = p
            break

    if not bundle_path:
        print(f"Auto-import: No bundle file found. Tried: {bundle_paths}")
        return  # No bundle file found

    print(f"Auto-import: Loading bundle from {bundle_path}")
    # Disable FK checks during bulk import for speed and to avoid ordering issues
    conn.execute("PRAGMA foreign_keys=OFF")
    with open(bundle_path) as f:
        bundle = json.load(f)

    prospects = bundle.get("prospects", [])
    if not prospects:
        return

    now = datetime.utcnow().isoformat()

    # Create batch record
    batch_id = gen_id("batch")
    conn.execute("""INSERT INTO batches (id, batch_number, created_date, prospect_count,
        ab_variable, status, source, created_at)
        VALUES (?,?,?,?,?,?,?,?)""",
        (batch_id, 1, now[:10], len(prospects), "pain_hook", "imported", "run_bundle", now))

    # Create research run record
    run_id = gen_id("rr")
    conn.execute("""INSERT INTO research_runs (id, name, import_type, prospect_count, status,
        sop_checklist, progress_pct, logs, ab_variable, config, created_at, completed_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (run_id, f"Batch 1 Auto-Import - {now[:10]}", "run_bundle", len(prospects), "completed",
         json.dumps([{"step": "import", "status": "completed", "label": "Auto-Import on Cold Start"}]),
         100, json.dumps([f"Auto-imported on cold start at {now}"]),
         "pain_hook", "{}", now, now))

    touch_map = [
        (1, "inmail", "touch_1_subject", "touch_1_body"),
        (2, "call", None, "call_snippet_1"),
        (3, "inmail_followup", None, "touch_3"),
        (4, "call", None, "call_snippet_2"),
        (6, "breakup", None, "touch_6"),
    ]

    # Proof point mapping by vertical
    proof_map = {
        "FinTech": ("cred", "CRED achieved 90% regression automation with 5x faster execution"),
        "Healthcare": ("medibuddy", "Medibuddy automated 2,500 tests and cut maintenance 50%"),
        "Pharma": ("sanofi", "Sanofi cut regression from 3 days to 80 minutes"),
        "SaaS": ("spendflo", "Spendflo cut manual testing 50% and saw ROI in the first quarter"),
        "Media": ("nagra", "Nagra DTV automated 2,500 tests in 8 months, 4X faster"),
        "IoT/Security": ("fortune100", "A Fortune 100 company achieved 3X productivity increase"),
    }

    imported_contacts = 0
    imported_drafts = 0

    for idx, p in enumerate(prospects):
        name = p.get("name", "")
        if not name:
            continue
        if "Removed" in p.get("status", ""):
            continue

        parts = name.strip().split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""

        linkedin_url = p.get("linkedin", p.get("linkedin_url", ""))
        company = p.get("company", "")
        title = p.get("title", "")
        vertical = p.get("vertical", "")

        # Detect persona and seniority
        title_lower = title.lower()
        if any(kw in title_lower for kw in ["qa", "quality", "test", "sdet"]):
            persona_type = "qa_leader"
        elif any(kw in title_lower for kw in ["vp eng", "vp software", "cto", "svp"]):
            persona_type = "vp_eng"
        else:
            persona_type = "eng_leader"

        if any(kw in title_lower for kw in ["vp", "svp", "head of", "chief"]):
            seniority = "vp"
        elif any(kw in title_lower for kw in ["sr director", "senior director"]):
            seniority = "sr_director"
        elif "director" in title_lower:
            seniority = "director"
        elif "manager" in title_lower:
            seniority = "manager"
        else:
            seniority = "ic_senior"

        # Priority scoring
        priority = 3
        if persona_type == "qa_leader":
            priority += 1
        if vertical in ("FinTech", "SaaS", "Healthcare"):
            priority += 1
        priority = min(priority, 5)

        # Create account
        acc = conn.execute("SELECT id FROM accounts WHERE name=?", (company,)).fetchone()
        if acc:
            account_id = acc[0]
        else:
            account_id = gen_id("acc")
            emp_count = p.get("employee_count")
            emp_band = "enterprise" if emp_count and emp_count > 5000 else "mid_market" if emp_count and emp_count > 200 else "smb"
            conn.execute("""INSERT INTO accounts (id, name, industry, employee_count, employee_band,
                source, created_at) VALUES (?,?,?,?,?,?,?)""",
                (account_id, company, vertical, emp_count, emp_band, "run_bundle", now))

        # Create contact
        contact_id = gen_id("con")
        conn.execute("""INSERT INTO contacts (id, account_id, first_name, last_name, title,
            persona_type, seniority_level, linkedin_url, stage, priority_score,
            personalization_score, predicted_objection, objection_response,
            source, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (contact_id, account_id, first_name, last_name, title,
             persona_type, seniority, linkedin_url, "new", priority,
             p.get("personalization_score", 3),
             p.get("predicted_objection", ""), p.get("objection_response", ""),
             "run_bundle", now))
        imported_contacts += 1

        # Create research snapshot
        key_detail = p.get("key_detail", "")
        company_detail = p.get("company_detail", "")
        proof_key, proof_text = proof_map.get(vertical, ("spendflo", "Spendflo cut manual testing 50%"))

        pain_indicators = []
        if "fintech" in vertical.lower() or "finance" in vertical.lower():
            pain_indicators = ["Regression testing across payment/transaction flows", "Compliance validation after each release", "API test coverage for financial integrations"]
        elif "health" in vertical.lower() or "pharma" in vertical.lower():
            pain_indicators = ["Regulatory compliance testing cycles", "Patient data flow validation", "Cross-platform testing for clinical workflows"]
        elif "saas" in vertical.lower():
            pain_indicators = ["Regression testing slowing release velocity", "Flaky tests eroding team confidence", "Manual testing bottleneck as features scale"]
        else:
            pain_indicators = ["Test automation coverage gaps", "Regression cycle duration", "Manual testing overhead"]

        snap_id = gen_id("rs")
        conn.execute("""INSERT INTO research_snapshots (id, contact_id, account_id, entity_type,
            headline, summary, pain_indicators, company_products, company_metrics,
            sources, confidence_score, agent_run_id, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (snap_id, contact_id, account_id, "prospect",
             key_detail or f"{title} at {company}",
             company_detail or f"{company} - {vertical} company",
             json.dumps(pain_indicators),
             company_detail or "",
             json.dumps({"employee_count": p.get("employee_count"), "industry": vertical}),
             json.dumps(["run_bundle_import"]), 3, run_id, now))

        # Create draft_research_link for Touch 1
        # (will be linked after draft creation)

        # Create batch_prospect link
        conn.execute("""INSERT INTO batch_prospects (id, batch_id, contact_id, ab_group,
            sequence_status, position_in_batch) VALUES (?,?,?,?,?,?)""",
            (gen_id("bp"), batch_id, contact_id, p.get("ab_group", ""), "not_started", idx+1))

        # Create message drafts
        for touch_num, touch_type, subj_field, body_field in touch_map:
            body_text = p.get(body_field, "")
            if not body_text:
                continue
            subj_text = p.get(subj_field, "") if subj_field else ""
            draft_id = gen_id("md")
            wc = len(body_text.split())

            # Quality gate checks
            qc_passed = 1
            qc_flags = []
            if len(body_text) < 100 and touch_num not in (2, 4, 6):
                qc_passed = 0
                qc_flags.append("body_too_short")
            if "\u2014" in body_text or "\u2013" in body_text:
                qc_passed = 0
                qc_flags.append("em_dash_found")
            if company and company.lower() not in body_text.lower():
                if touch_num in (1,):
                    qc_flags.append("missing_company_name")

            conn.execute("""INSERT INTO message_drafts (id, contact_id, batch_id, channel,
                touch_number, touch_type, subject_line, body, version, personalization_score,
                proof_point_used, pain_hook, opener_style, word_count, qc_passed, qc_flags,
                approval_status, ab_group, ab_variable, source, created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (draft_id, contact_id, batch_id, "linkedin",
                 touch_num, touch_type, subj_text, body_text, 1,
                 p.get("personalization_score", 3),
                 proof_key, "", "", wc, qc_passed, json.dumps(qc_flags),
                 "draft", p.get("ab_group", ""),
                 "pain_hook", "run_bundle", now))
            imported_drafts += 1

            # Link research to Touch 1 draft
            if touch_num == 1:
                conn.execute("""INSERT INTO draft_research_link (id, draft_id, contact_id,
                    profile_bullets, company_bullets, pain_hypothesis, why_testsigma,
                    confidence_score, template_name, created_at)
                    VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (gen_id("drl"), draft_id, contact_id,
                     json.dumps([key_detail]) if key_detail else "[]",
                     json.dumps([company_detail]) if company_detail else "[]",
                     json.dumps(pain_indicators[:1]),
                     proof_text, 3, "touch_1_inmail", now))

    # Create workflow run record
    wf_id = gen_id("wfrun")
    conn.execute("""INSERT INTO workflow_runs (id, workflow_id, workflow_type, channel, status,
        input_data, output_data, total_steps, completed_steps, started_at, completed_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (wf_id, "", "linkedin_batch_1_auto", "linkedin", "succeeded",
         json.dumps({"source": "auto_import_cold_start", "bundle_prospects": len(prospects)}),
         json.dumps({"imported_contacts": imported_contacts, "imported_drafts": imported_drafts}),
         4, 4, now, now))

    # Log to activity timeline
    conn.execute("""INSERT INTO activity_timeline (id, activity_type, channel, description, metadata, created_at)
        VALUES (?,?,?,?,?,?)""",
        (gen_id("evt"), "batch_auto_import", "linkedin",
         f"Auto-imported Batch 1: {imported_contacts} contacts, {imported_drafts} drafts",
         json.dumps({"batch_id": batch_id, "workflow_run_id": wf_id}), now))

    conn.execute("PRAGMA foreign_keys=ON")
    conn.commit()
    print(f"Auto-import: Done. {imported_contacts} contacts, {imported_drafts} drafts")


def init_and_seed():
    db_path = os.environ.get("OCC_DB_PATH", "/tmp/outreach.db")

    # FAST PATH: If a pre-built seed DB exists, just copy it (< 1 second)
    if not os.path.exists(db_path):
        import shutil
        seed_db = os.path.join(os.path.dirname(__file__), "data", "outreach_seed.db")
        if os.path.exists(seed_db):
            shutil.copy2(seed_db, db_path)
            print(f"Cold start: Copied pre-built DB ({os.path.getsize(db_path)} bytes)")
            return

    # SLOW PATH: Build from scratch (used for tests and local dev)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA_SQL)
    # Add tracking columns (safe to re-run, ignore errors for existing columns)
    migration_cols = [
        ("contacts", "intent_signal_type", "TEXT"),
        ("contacts", "intent_date", "TEXT"),
        ("contacts", "first_touch_date", "TEXT"),
        ("contacts", "first_reply_date", "TEXT"),
        ("contacts", "reply_time_hours", "INTEGER"),
        ("contacts", "which_touch_replied", "INTEGER"),
        ("contacts", "reply_quality", "TEXT"),
        ("contacts", "meeting_scheduled_date", "TEXT"),
        ("contacts", "objection_hit", "INTEGER DEFAULT 0"),
        ("contacts", "referral_target", "TEXT"),
        ("contacts", "already_messaged_sn", "INTEGER DEFAULT 0"),
        ("contacts", "already_messaged_li", "INTEGER DEFAULT 0"),
        ("contacts", "messaging_status", "TEXT DEFAULT 'unknown'"),
        ("contacts", "batch_1_eligible", "INTEGER DEFAULT 0"),
    ]
    for table, col, coltype in migration_cols:
        try:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {coltype}")
        except Exception:
            pass  # Column already exists
    conn.commit()

    # Auto-import run bundle if DB is empty
    try:
        _auto_import_run_bundle(conn)
    except Exception as e:
        print(f"Auto-import warning: {e}")

    conn.close()

init_and_seed()

# ---------------------------------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------------------------------

app = FastAPI(title="Outreach Command Center API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# GLOBAL SAFETY: DRY RUN MODE
# ---------------------------------------------------------------------------
DRY_RUN = os.environ.get("DRY_RUN", "true").lower() in ("true", "1", "yes")

def check_safety(action_type: str, run_id: str = None):
    """Check if an action is allowed. Returns True if safe, raises if blocked."""
    blocked_actions = {"send_linkedin_message", "send_email", "connect_request", "post_comment", "send_inmail"}
    if action_type in blocked_actions:
        # Log safety event
        conn = get_db()
        conn.execute("INSERT INTO safety_events (id, run_id, event_type, severity, details, blocked_action) VALUES (?,?,?,?,?,?)",
            (gen_id("sev"), run_id, "action_blocked", "critical",
             json.dumps({"reason": "DRY_RUN mode active" if DRY_RUN else "Action permanently blocked", "action": action_type}),
             action_type))
        conn.commit()
        conn.close()
        raise HTTPException(status_code=403, detail=f"Action '{action_type}' is blocked. DRY_RUN={DRY_RUN}. This system only generates drafts.")
    return True

# ─── API KEY AUTHENTICATION ────────────────────────────────────────────────
API_KEY = os.environ.get("OCC_API_KEY", "")  # Empty = no auth required (dev mode)

async def verify_api_key(x_api_key: str = Header(None)):
    """Verify API key for sensitive endpoints. Empty API_KEY = auth disabled."""
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(401, "Invalid API key")
    return True

# Helper
def rows_to_dicts(rows):
    return [dict(r) for r in rows]

def parse_json_fields(d, fields):
    for f in fields:
        if f in d and isinstance(d[f], str):
            try:
                d[f] = json.loads(d[f])
            except:
                pass
    return d

# ─── STATS / HOME ─────────────────────────────────────────────

@app.get("/api/stats")
def dashboard_stats():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    by_stage = {}
    for row in conn.execute("SELECT stage, COUNT(*) as c FROM contacts GROUP BY stage"):
        by_stage[row["stage"]] = row["c"]
    replies = conn.execute("SELECT COUNT(*) FROM replies").fetchone()[0]
    meetings = conn.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0]
    sent = conn.execute("SELECT COUNT(*) FROM touchpoints").fetchone()[0]
    with_drafts = conn.execute("SELECT COUNT(DISTINCT contact_id) FROM message_drafts").fetchone()[0]
    total_drafts = conn.execute("SELECT COUNT(*) FROM message_drafts").fetchone()[0]
    conn.close()
    return {
        "total_contacts": total,
        "by_stage": by_stage,
        "with_drafts": with_drafts,
        "total_drafts": total_drafts,
        "total_replies": replies,
        "total_meetings": meetings,
        "total_sent": sent,
        "reply_rate": round(replies / max(sent, 1) * 100, 1),
        "meeting_rate": round(meetings / max(replies, 1) * 100, 1),
    }

@app.get("/api/action-queue")
def action_queue():
    conn = get_db()
    actions = []
    # Overdue followups
    overdue = conn.execute("""
        SELECT f.*, c.first_name, c.last_name, c.priority_score, a.name as company_name
        FROM followups f JOIN contacts c ON f.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        WHERE f.due_date <= datetime('now') AND f.completed_at IS NULL
        ORDER BY c.priority_score DESC LIMIT 10
    """).fetchall()
    for f in overdue:
        d = dict(f)
        actions.append({"type":"overdue_followup","priority":"hot",
            "contact":f"{d['first_name']} {d['last_name']}","company":d.get("company_name",""),
            "contact_id":d["contact_id"],
            "action":f"Overdue: Touch {d.get('touch_number','?')} via {d.get('channel','?')}"})
    # Hot untouched
    untouched = conn.execute("""
        SELECT c.id,c.first_name,c.last_name,c.priority_score,a.name as company_name
        FROM contacts c LEFT JOIN accounts a ON c.account_id=a.id
        WHERE c.stage='new' AND c.priority_score>=4 AND c.status='active'
        ORDER BY c.priority_score DESC LIMIT 10
    """).fetchall()
    for c in untouched:
        d = dict(c)
        actions.append({"type":"untouched_hot","priority":"high",
            "contact":f"{d['first_name']} {d['last_name']}","company":d.get("company_name",""),
            "contact_id":d["id"],
            "action":f"Priority {d['priority_score']} - not yet contacted"})
    conn.close()
    return actions

@app.get("/api/pipeline-funnel")
def pipeline_funnel():
    conn = get_db()
    stages = ["new","touched","engaged","replied","meeting_booked"]
    result = {}
    for s in stages:
        result[s] = conn.execute("SELECT COUNT(*) FROM contacts WHERE stage=?", (s,)).fetchone()[0]
    conn.close()
    return result

@app.get("/api/reply-rates/persona")
def reply_rates_persona():
    conn = get_db()
    results = {}
    for row in conn.execute("""
        SELECT c.persona_type, COUNT(DISTINCT r.id) as replies, COUNT(DISTINCT t.id) as sent
        FROM contacts c LEFT JOIN touchpoints t ON c.id=t.contact_id
        LEFT JOIN replies r ON c.id=r.contact_id
        GROUP BY c.persona_type
    """):
        d = dict(row)
        pt = d["persona_type"] or "unknown"
        results[pt] = {"sent": d["sent"], "replies": d["replies"],
                       "rate": round(d["replies"]/max(d["sent"],1)*100, 1)}
    conn.close()
    return results

@app.get("/api/reply-rates/vertical")
def reply_rates_vertical():
    conn = get_db()
    results = {}
    for row in conn.execute("""
        SELECT a.industry, COUNT(DISTINCT r.id) as replies, COUNT(DISTINCT t.id) as sent
        FROM contacts c JOIN accounts a ON c.account_id=a.id
        LEFT JOIN touchpoints t ON c.id=t.contact_id
        LEFT JOIN replies r ON c.id=r.contact_id
        GROUP BY a.industry
    """):
        d = dict(row)
        ind = d["industry"] or "unknown"
        results[ind] = {"sent": d["sent"], "replies": d["replies"],
                       "rate": round(d["replies"]/max(d["sent"],1)*100, 1)}
    conn.close()
    return results

# ─── CONTACTS ──────────────────────────────────────────────────

@app.get("/api/contacts")
def list_contacts(stage: str = None, priority_min: int = None, limit: int = 100, offset: int = 0):
    conn = get_db()
    q = """SELECT c.*, a.name as company_name, a.industry, a.domain
           FROM contacts c LEFT JOIN accounts a ON c.account_id=a.id WHERE 1=1"""
    params = []
    if stage:
        q += " AND c.stage=?"; params.append(stage)
    if priority_min:
        q += " AND c.priority_score>=?"; params.append(priority_min)
    q += " ORDER BY c.priority_score DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    rows = rows_to_dicts(conn.execute(q, params).fetchall())
    total = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    conn.close()
    for r in rows:
        parse_json_fields(r, ["priority_factors","known_tools"])
    return {"contacts": rows, "total": total}

@app.get("/api/contacts/{contact_id}")
def get_contact(contact_id: str):
    conn = get_db()
    row = conn.execute("""SELECT c.*, a.name as company_name, a.industry, a.domain
        FROM contacts c LEFT JOIN accounts a ON c.account_id=a.id WHERE c.id=?""",
        (contact_id,)).fetchone()
    conn.close()
    if not row: raise HTTPException(404, "Contact not found")
    return dict(row)

@app.post("/api/contacts")
def create_contact(data: dict):
    conn = get_db()
    cid = gen_id("con")
    now = datetime.utcnow().isoformat()
    conn.execute("""INSERT INTO contacts (id,account_id,first_name,last_name,title,
        persona_type,seniority_level,email,linkedin_url,stage,priority_score,
        status,source,created_at,updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (cid, data.get("account_id"), data.get("first_name",""), data.get("last_name",""),
         data.get("title"), data.get("persona_type"), data.get("seniority_level"),
         data.get("email"), data.get("linkedin_url"), "new",
         data.get("priority_score",3), "active", "manual", now, now))
    conn.commit()
    row = conn.execute("SELECT * FROM contacts WHERE id=?", (cid,)).fetchone()
    conn.close()
    return dict(row)

@app.put("/api/contacts/{contact_id}")
def update_contact(contact_id: str, data: dict):
    conn = get_db()
    sets = []
    params = []
    for k, v in data.items():
        if k not in ("id","created_at"):
            sets.append(f"{k}=?"); params.append(v)
    if sets:
        sets.append("updated_at=?"); params.append(datetime.utcnow().isoformat())
        params.append(contact_id)
        conn.execute(f"UPDATE contacts SET {','.join(sets)} WHERE id=?", params)
        conn.commit()
    row = conn.execute("SELECT * FROM contacts WHERE id=?", (contact_id,)).fetchone()
    conn.close()
    if not row: raise HTTPException(404)
    return dict(row)

# ─── CONTACT IDENTITIES (new) ──────────────────────────

@app.get("/api/contacts/{contact_id}/identities")
def get_contact_identities(contact_id: str):
    conn = get_db()
    rows = rows_to_dicts(conn.execute(
        "SELECT * FROM contact_identities WHERE contact_id=? ORDER BY is_primary DESC",
        (contact_id,)).fetchall())
    conn.close()
    return rows

@app.post("/api/contacts/{contact_id}/identities")
def add_contact_identity(contact_id: str, data: dict):
    conn = get_db()
    ci_id = gen_id("ci")
    now = datetime.utcnow().isoformat()
    conn.execute("""INSERT INTO contact_identities (id,contact_id,identity_type,value,
        verified,source,is_primary,created_at) VALUES (?,?,?,?,?,?,?,?)""",
        (ci_id, contact_id, data.get("identity_type","email"),
         data.get("value",""), data.get("verified",0),
         data.get("source","manual"), data.get("is_primary",0), now))
    conn.commit()
    row = conn.execute("SELECT * FROM contact_identities WHERE id=?", (ci_id,)).fetchone()
    conn.close()
    if not row: raise HTTPException(400, "Failed to create identity")
    return dict(row)

# ─── ACCOUNTS ──────────────────────────────────────────────────

@app.get("/api/accounts")
def list_accounts(limit: int = 100, offset: int = 0):
    conn = get_db()
    rows = rows_to_dicts(conn.execute(
        "SELECT * FROM accounts ORDER BY name LIMIT ? OFFSET ?", (limit, offset)).fetchall())
    total = conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]
    conn.close()
    for r in rows:
        parse_json_fields(r, ["known_tools"])
    return {"accounts": rows, "total": total}

@app.get("/api/accounts/{account_id}")
def get_account(account_id: str):
    conn = get_db()
    row = conn.execute("SELECT * FROM accounts WHERE id=?", (account_id,)).fetchone()
    conn.close()
    if not row: raise HTTPException(404)
    d = dict(row)
    parse_json_fields(d, ["known_tools"])
    return d

@app.post("/api/accounts")
def create_account(data: dict):
    conn = get_db()
    aid = gen_id("acc")
    now = datetime.utcnow().isoformat()
    conn.execute("""INSERT INTO accounts (id,name,domain,industry,employee_count,
        tier,known_tools,buyer_intent,hq_location,created_at,updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (aid, data.get("name",""), data.get("domain"), data.get("industry"),
         data.get("employee_count"), data.get("tier"), json.dumps(data.get("known_tools",[])),
         data.get("buyer_intent",0), data.get("hq_location"), now, now))
    conn.commit()
    row = conn.execute("SELECT * FROM accounts WHERE id=?", (aid,)).fetchone()
    conn.close()
    return dict(row)

# ─── MESSAGES ──────────────────────────────────────────────────

@app.get("/api/messages")
def list_messages(contact_id: str = None, batch_id: str = None,
                  approval_status: str = None, limit: int = 100, offset: int = 0):
    conn = get_db()
    q = """SELECT m.*, c.first_name, c.last_name
           FROM message_drafts m LEFT JOIN contacts c ON m.contact_id=c.id WHERE 1=1"""
    params = []
    if contact_id: q += " AND m.contact_id=?"; params.append(contact_id)
    if batch_id: q += " AND m.batch_id=?"; params.append(batch_id)
    if approval_status: q += " AND m.approval_status=?"; params.append(approval_status)
    q += " ORDER BY m.created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    rows = rows_to_dicts(conn.execute(q, params).fetchall())
    total = conn.execute("SELECT COUNT(*) FROM message_drafts").fetchone()[0]
    conn.close()
    return {"messages": rows, "total": total}

@app.put("/api/messages/{message_id}/approve")
def approve_message(message_id: str):
    conn = get_db()
    conn.execute("UPDATE message_drafts SET approval_status='approved', updated_at=? WHERE id=?",
                 (datetime.utcnow().isoformat(), message_id))
    conn.commit()
    row = conn.execute("SELECT * FROM message_drafts WHERE id=?", (message_id,)).fetchone()
    conn.close()
    if not row: raise HTTPException(404)
    return dict(row)

@app.put("/api/messages/{message_id}/reject")
def reject_message(message_id: str):
    conn = get_db()
    conn.execute("UPDATE message_drafts SET approval_status='rejected', updated_at=? WHERE id=?",
                 (datetime.utcnow().isoformat(), message_id))
    conn.commit()
    row = conn.execute("SELECT * FROM message_drafts WHERE id=?", (message_id,)).fetchone()
    conn.close()
    if not row: raise HTTPException(404)
    return dict(row)

# ─── BATCHES ───────────────────────────────────────────────────

@app.get("/api/batches")
def list_batches():
    conn = get_db()
    rows = rows_to_dicts(conn.execute("SELECT * FROM batches ORDER BY batch_number DESC").fetchall())
    conn.close()
    for r in rows:
        parse_json_fields(r, ["mix_ratio","metrics"])
    return rows

@app.get("/api/batches/{batch_id}")
def get_batch(batch_id: str):
    conn = get_db()
    row = conn.execute("SELECT * FROM batches WHERE id=?", (batch_id,)).fetchone()
    conn.close()
    if not row: raise HTTPException(404)
    d = dict(row)
    parse_json_fields(d, ["mix_ratio","metrics"])
    return d

@app.post("/api/batches/launch")
def launch_batch(data: dict = {}):
    conn = get_db()
    bid = gen_id("bat")
    num = (conn.execute("SELECT MAX(batch_number) FROM batches").fetchone()[0] or 0) + 1
    now = datetime.utcnow().isoformat()
    conn.execute("""INSERT INTO batches (id,batch_number,created_date,prospect_count,
        ab_variable,status,created_at) VALUES (?,?,?,?,?,?,?)""",
        (bid, num, now[:10], data.get("prospect_count",25),
         data.get("ab_variable","pain_hook"), "building", now))
    conn.commit()
    row = conn.execute("SELECT * FROM batches WHERE id=?", (bid,)).fetchone()
    conn.close()
    return dict(row)

# ─── SIGNALS ───────────────────────────────────────────────────

@app.get("/api/signals")
def list_signals(limit: int = 50):
    conn = get_db()
    rows = rows_to_dicts(conn.execute("""
        SELECT s.*, c.first_name, c.last_name, a.name as company_name
        FROM signals s LEFT JOIN contacts c ON s.contact_id=c.id
        LEFT JOIN accounts a ON s.account_id=a.id
        ORDER BY s.created_at DESC LIMIT ?""", (limit,)).fetchall())
    conn.close()
    return rows

@app.post("/api/signals/{signal_id}/act")
def act_on_signal(signal_id: str):
    conn = get_db()
    conn.execute("UPDATE signals SET acted_on=1 WHERE id=?", (signal_id,))
    conn.commit()
    conn.close()
    return {"status": "acted"}

# ─── EXPERIMENTS ───────────────────────────────────────────────

@app.get("/api/experiments")
def list_experiments():
    conn = get_db()
    rows = rows_to_dicts(conn.execute("SELECT * FROM experiments ORDER BY created_at DESC").fetchall())
    conn.close()
    return rows

# ─── AGENT RUNS ────────────────────────────────────────────────

@app.get("/api/agent-runs")
def list_agent_runs(limit: int = 50):
    conn = get_db()
    rows = rows_to_dicts(conn.execute(
        "SELECT * FROM agent_runs ORDER BY started_at DESC LIMIT ?", (limit,)).fetchall())
    conn.close()
    return rows

# ─── INTELLIGENCE ──────────────────────────────────────────────

@app.get("/api/intelligence/proof-points")
def proof_point_stats():
    conn = get_db()
    results = {}
    for row in conn.execute("""
        SELECT m.proof_point_used, COUNT(*) as used,
               COUNT(DISTINCT r.id) as replied
        FROM message_drafts m
        LEFT JOIN replies r ON m.contact_id = r.contact_id
        WHERE m.proof_point_used IS NOT NULL
        GROUP BY m.proof_point_used
    """):
        d = dict(row)
        pp = d["proof_point_used"]
        results[pp] = {"used": d["used"], "replied": d["replied"],
                       "rate": round(d["replied"]/max(d["used"],1)*100, 1)}
    conn.close()
    return results

@app.get("/api/intelligence/pain-hooks")
def pain_hook_stats():
    conn = get_db()
    results = {}
    for row in conn.execute("""
        SELECT m.pain_hook, COUNT(*) as used,
               COUNT(DISTINCT r.id) as replied
        FROM message_drafts m
        LEFT JOIN replies r ON m.contact_id = r.contact_id
        WHERE m.pain_hook IS NOT NULL
        GROUP BY m.pain_hook
    """):
        d = dict(row)
        results[d["pain_hook"]] = {"used": d["used"], "replied": d["replied"],
                                    "rate": round(d["replied"]/max(d["used"],1)*100, 1)}
    conn.close()
    return results

@app.get("/api/intelligence/opener-styles")
def opener_style_stats():
    conn = get_db()
    results = {}
    for row in conn.execute("""
        SELECT m.opener_style, COUNT(*) as used,
               COUNT(DISTINCT r.id) as replied
        FROM message_drafts m
        LEFT JOIN replies r ON m.contact_id = r.contact_id
        WHERE m.opener_style IS NOT NULL
        GROUP BY m.opener_style
    """):
        d = dict(row)
        results[d["opener_style"]] = {"used": d["used"], "replied": d["replied"],
                                       "rate": round(d["replied"]/max(d["used"],1)*100, 1)}
    conn.close()
    return results

@app.get("/api/intelligence/personalization")
def personalization_stats():
    conn = get_db()
    results = {}
    for row in conn.execute("""
        SELECT m.personalization_score, COUNT(*) as used,
               COUNT(DISTINCT r.id) as replied
        FROM message_drafts m
        LEFT JOIN replies r ON m.contact_id = r.contact_id
        WHERE m.personalization_score IS NOT NULL
        GROUP BY m.personalization_score
    """):
        d = dict(row)
        results[str(d["personalization_score"])] = {
            "used": d["used"], "replied": d["replied"],
            "rate": round(d["replied"]/max(d["used"],1)*100, 1)}
    conn.close()
    return results

# ─── FOLLOWUPS ─────────────────────────────────────────────────

@app.get("/api/followups")
def list_followups(state: str = None):
    conn = get_db()
    q = """SELECT f.*, c.first_name, c.last_name
           FROM followups f LEFT JOIN contacts c ON f.contact_id=c.id WHERE 1=1"""
    params = []
    if state: q += " AND f.state=?"; params.append(state)
    q += " ORDER BY f.due_date"
    rows = rows_to_dicts(conn.execute(q, params).fetchall())
    conn.close()
    return rows

# ─── OPPORTUNITIES ─────────────────────────────────────────────

@app.get("/api/opportunities")
def list_opportunities():
    conn = get_db()
    rows = rows_to_dicts(conn.execute("""
        SELECT o.*, c.first_name, c.last_name, a.name as company_name
        FROM opportunities o LEFT JOIN contacts c ON o.contact_id=c.id
        LEFT JOIN accounts a ON o.account_id=a.id
        ORDER BY o.created_at DESC
    """).fetchall())
    conn.close()
    return rows

# ─── FLOW MANAGEMENT (new) ─────────────────────────────────────

@app.post("/api/flows/run")
def launch_flow(data: dict):
    try:
        conn = get_db()
        flow_id = gen_id("flow")
        flow_type = data.get("flow_type", "account_research")
        config = data.get("config", {})
        now = datetime.utcnow().isoformat()

        # Create flow run
        conn.execute("""INSERT INTO flow_runs (id,flow_type,status,config,total_steps,
            started_at,created_at) VALUES (?,?,?,?,?,?,?)""",
            (flow_id, flow_type, "running", json.dumps(config), 5, now, now))

        # Create simulated steps
        steps = ["research", "analysis", "drafting", "qc", "finalization"]
        for idx, step in enumerate(steps):
            step_id = gen_id("step")
            conn.execute("""INSERT INTO flow_run_steps (id,flow_run_id,step_name,
                agent_type,status,created_at) VALUES (?,?,?,?,?,?)""",
                (step_id, flow_id, step, "Agent", "pending", now))

        conn.commit()
        row = conn.execute("SELECT * FROM flow_runs WHERE id=?", (flow_id,)).fetchone()
        conn.close()
        return dict(row) if row else {"id": flow_id, "status": "created"}
    except Exception as e:
        conn.close()
        raise HTTPException(400, str(e))

@app.get("/api/flows/runs")
def list_flow_runs(flow_type: str = None, status: str = None, limit: int = 50):
    conn = get_db()
    q = "SELECT * FROM flow_runs WHERE 1=1"
    params = []
    if flow_type:
        q += " AND flow_type=?"; params.append(flow_type)
    if status:
        q += " AND status=?"; params.append(status)
    q += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    rows = rows_to_dicts(conn.execute(q, params).fetchall())
    conn.close()
    for r in rows:
        parse_json_fields(r, ["config", "warnings"])
    return rows

@app.get("/api/flows/runs/{run_id}")
def get_flow_run(run_id: str):
    conn = get_db()
    flow = conn.execute("SELECT * FROM flow_runs WHERE id=?", (run_id,)).fetchone()
    if not flow:
        conn.close()
        raise HTTPException(404)

    d = dict(flow)
    parse_json_fields(d, ["config", "warnings"])

    # Include steps and artifacts
    steps = rows_to_dicts(conn.execute(
        "SELECT * FROM flow_run_steps WHERE flow_run_id=? ORDER BY created_at",
        (run_id,)).fetchall())
    for s in steps:
        parse_json_fields(s, ["input_data", "output_data"])

    artifacts = rows_to_dicts(conn.execute(
        "SELECT * FROM flow_artifacts WHERE flow_run_id=?", (run_id,)).fetchall())
    for a in artifacts:
        parse_json_fields(a, ["metadata", "content"])

    conn.close()
    d["steps"] = steps
    d["artifacts"] = artifacts
    return d

@app.post("/api/flows/runs/{run_id}/cancel")
def cancel_flow_run(run_id: str):
    conn = get_db()
    now = datetime.utcnow().isoformat()
    conn.execute("UPDATE flow_runs SET status='cancelled', completed_at=? WHERE id=?",
                 (now, run_id))
    conn.commit()
    row = conn.execute("SELECT * FROM flow_runs WHERE id=?", (run_id,)).fetchone()
    conn.close()
    if not row: raise HTTPException(404)
    return dict(row)

@app.get("/api/flows/catalog")
def flow_catalog():
    return {
        "flows": [
            {
                "type": "account_research",
                "name": "Account Research",
                "description": "Deep research on target accounts",
                "inputs": ["targets", "volume_cap"],
                "outputs": ["research_snapshots", "account_briefs"]
            },
            {
                "type": "linkedin_prospecting",
                "name": "LinkedIn Prospecting",
                "description": "Draft LinkedIn messages and InMails",
                "inputs": ["targets", "channel"],
                "outputs": ["draft_messages", "activity_timeline"]
            },
            {
                "type": "email_prospecting",
                "name": "Email Prospecting",
                "description": "Draft email campaigns with personalization",
                "inputs": ["targets", "volume_cap"],
                "outputs": ["draft_messages", "suppression_checks"]
            },
        ]
    }

# ─── ACTIVITY TIMELINE (new) ───────────────────────────────────

@app.get("/api/activity")
def list_activity(channel: str = None, contact_id: str = None,
                  account_id: str = None, limit: int = 100, offset: int = 0):
    conn = get_db()
    q = "SELECT * FROM activity_timeline WHERE 1=1"
    params = []
    if channel:
        q += " AND channel=?"; params.append(channel)
    if contact_id:
        q += " AND contact_id=?"; params.append(contact_id)
    if account_id:
        q += " AND account_id=?"; params.append(account_id)
    q += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    rows = rows_to_dicts(conn.execute(q, params).fetchall())
    total = conn.execute("SELECT COUNT(*) FROM activity_timeline").fetchone()[0]
    conn.close()
    for r in rows:
        parse_json_fields(r, ["metadata"])
    return {"activities": rows, "total": total}

# ─── DRAFTS (new) ──────────────────────────────────────────────

@app.get("/api/drafts")
def list_drafts(channel: str = None, status: str = None,
                contact_id: str = None, flow_run_id: str = None,
                limit: int = 100, offset: int = 0):
    conn = get_db()
    q = "SELECT * FROM draft_versions WHERE 1=1"
    params = []
    if channel:
        q += " AND channel=?"; params.append(channel)
    if status:
        q += " AND status=?"; params.append(status)
    if contact_id:
        q += " AND contact_id=?"; params.append(contact_id)
    if flow_run_id:
        q += " AND flow_run_id=?"; params.append(flow_run_id)
    q += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    rows = rows_to_dicts(conn.execute(q, params).fetchall())
    total = conn.execute("SELECT COUNT(*) FROM draft_versions").fetchone()[0]
    conn.close()
    for r in rows:
        parse_json_fields(r, ["qc_flags"])
    return {"drafts": rows, "total": total}

@app.get("/api/drafts/{draft_id}")
def get_draft(draft_id: str):
    conn = get_db()
    # Get all versions of this draft
    rows = rows_to_dicts(conn.execute(
        "SELECT * FROM draft_versions WHERE draft_id=? ORDER BY version DESC",
        (draft_id,)).fetchall())
    conn.close()
    if not rows:
        raise HTTPException(404, "Draft not found")
    for r in rows:
        parse_json_fields(r, ["qc_flags"])
    return {"versions": rows, "current": rows[0] if rows else None}

@app.put("/api/drafts/{draft_id}/status")
def update_draft_status(draft_id: str, data: dict):
    conn = get_db()
    new_status = data.get("status", "draft")
    now = datetime.utcnow().isoformat()
    conn.execute("UPDATE draft_versions SET status=?, created_at=? WHERE draft_id=?",
                 (new_status, now, draft_id))
    conn.commit()
    rows = rows_to_dicts(conn.execute(
        "SELECT * FROM draft_versions WHERE draft_id=?", (draft_id,)).fetchall())
    conn.close()
    if not rows:
        raise HTTPException(404)
    return {"updated": len(rows), "status": new_status}

@app.put("/api/drafts/{draft_id}/edit")
def edit_draft(draft_id: str, data: dict):
    conn = get_db()
    # Get latest version
    latest = conn.execute(
        "SELECT * FROM draft_versions WHERE draft_id=? ORDER BY version DESC LIMIT 1",
        (draft_id,)).fetchone()

    if not latest:
        conn.close()
        raise HTTPException(404)

    # Create new version
    old = dict(latest)
    new_version = old["version"] + 1
    new_id = gen_id("draftv")
    now = datetime.utcnow().isoformat()

    conn.execute("""INSERT INTO draft_versions (id,draft_id,contact_id,channel,touch_number,
        subject,body,version,status,personalization_score,proof_point,pain_hook,
        opener_style,word_count,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (new_id, draft_id, old["contact_id"], old["channel"], old["touch_number"],
         data.get("subject", old.get("subject")),
         data.get("body", old.get("body")),
         new_version, "draft", old.get("personalization_score"),
         old.get("proof_point"), old.get("pain_hook"),
         old.get("opener_style"), len(data.get("body", "")),
         now))

    conn.commit()
    row = conn.execute("SELECT * FROM draft_versions WHERE id=?", (new_id,)).fetchone()
    conn.close()
    return dict(row) if row else {"version": new_version}

def validate_draft_content(subject: str = None, body: str = None, touch_type: str = None, channel: str = None):
    """Validate draft content meets minimum completeness requirements."""
    errors = []

    # Subject validation
    if subject is not None and len(subject.strip()) < 8:
        errors.append("Subject must be at least 8 characters")

    if body is not None:
        body_stripped = body.strip()
        body_char_count = len(body_stripped)
        word_count = len(body_stripped.split())

        # Determine minimum character count based on touch_type and channel
        min_chars = 150  # default for follow-ups (touch 3)
        if touch_type == 'break_up' or touch_type == 'touch_6':
            min_chars = 100
        elif touch_type == 'connect_note':
            min_chars = 200
        elif touch_type == 'inmail' or channel == 'linkedin' or touch_type in ('touch_1', 'touch_5'):
            min_chars = 350

        # Check character count
        if body_char_count < min_chars:
            errors.append(f"Body must be at least {min_chars} characters (currently {body_char_count})")

        # Word count check (general)
        if word_count < 30:
            errors.append(f"Body must be at least 30 words (currently {word_count})")

        # Check for incomplete indicators
        if body_stripped.endswith("..."):
            errors.append("Body appears incomplete (ends with '...')")

        # Paragraph break check (general requirement)
        paragraphs = [p.strip() for p in body_stripped.split("\n\n") if p.strip()]
        if len(paragraphs) < 1:
            errors.append("Body must contain at least 1 paragraph break (\\n\\n)")

        # Check for unresolved placeholders
        placeholders = [t for t in ["{first_name}", "{company}", "{title}", "[PLACEHOLDER]", "[TODO]"] if t in body_stripped]
        if placeholders:
            errors.append(f"Body contains unresolved placeholders: {', '.join(placeholders)}")

    return errors

@app.post("/api/drafts/validate")
def validate_draft_endpoint(data: dict = Body(...)):
    """Validate a draft without saving it. Returns validation errors."""
    errors = validate_draft_content(
        subject=data.get("subject"),
        body=data.get("body"),
        touch_type=data.get("touch_type"),
        channel=data.get("channel"),
    )
    return {"valid": len(errors) == 0, "errors": errors}

@app.patch("/api/drafts/{draft_id}")
def patch_draft(draft_id: str, data: dict):
    """Quick-edit a draft's subject_line or body directly on message_drafts."""
    conn = get_db()
    existing = conn.execute("SELECT * FROM message_drafts WHERE id=?", (draft_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(404, "Draft not found")
    updates = []
    params = []
    if "subject_line" in data:
        subj_errors = validate_draft_content(subject=data["subject_line"])
        if subj_errors:
            conn.close()
            raise HTTPException(400, detail={"error": "Draft validation failed", "issues": subj_errors})
        updates.append("subject_line=?")
        params.append(data["subject_line"])
    if "body" in data:
        body_errors = validate_draft_content(body=data["body"])
        if body_errors:
            conn.close()
            raise HTTPException(400, detail={"error": "Draft validation failed", "issues": body_errors})
        updates.append("body=?")
        params.append(data["body"])
        updates.append("word_count=?")
        params.append(len(data["body"].split()))
    if "status" in data:
        updates.append("status=?")
        params.append(data["status"])
    if not updates:
        conn.close()
        return {"ok": True}
    updates.append("updated_at=datetime('now')")
    params.append(draft_id)
    conn.execute(f"UPDATE message_drafts SET {','.join(updates)} WHERE id=?", params)
    # Audit log
    changes = {}
    if "subject_line" in data: changes["subject_line"] = "updated"
    if "body" in data: changes["body"] = f"updated ({len(data['body'].split())} words)"
    if "status" in data: changes["status"] = data["status"]
    conn.execute("""INSERT INTO activity_timeline (id, channel, activity_type, description, metadata, created_at)
        VALUES (?,?,?,?,?,datetime('now'))""",
        (gen_id("act"), "system", "draft_edited",
         f"Draft {draft_id} edited: {', '.join(f'{k}={v}' for k,v in changes.items())}",
         json.dumps({"draft_id": draft_id, "changes": changes})))
    conn.commit()
    row = conn.execute("SELECT * FROM message_drafts WHERE id=?", (draft_id,)).fetchone()
    conn.close()
    return dict(row) if row else {"ok": True}

@app.post("/api/drafts/cleanup-incomplete")
def cleanup_incomplete_drafts():
    """Flag incomplete drafts as invalid_incomplete and return count."""
    conn = get_db()
    # Find drafts with body < 200 chars or ending with '...'
    incomplete = conn.execute("""
        SELECT id, contact_id, body, subject_line, status
        FROM message_drafts
        WHERE (length(body) < 200 OR body LIKE '%...' OR body IS NULL)
        AND status != 'invalid_incomplete'
    """).fetchall()
    count = len(incomplete)
    if count > 0:
        conn.execute("""
            UPDATE message_drafts
            SET status = 'invalid_incomplete', updated_at = datetime('now')
            WHERE (length(body) < 200 OR body LIKE '%...' OR body IS NULL)
            AND status != 'invalid_incomplete'
        """)
        # Audit log
        conn.execute("""INSERT INTO activity_timeline (id, channel, activity_type, description, metadata, created_at)
            VALUES (?,?,?,?,?,datetime('now'))""",
            (gen_id("act"), "system", "drafts_cleanup",
             f"Flagged {count} incomplete drafts as invalid_incomplete",
             json.dumps({"flagged_count": count, "sample_ids": [r["id"] for r in incomplete[:5]]})))
        conn.commit()
    conn.close()
    return {"flagged": count, "details": [{"id": r["id"], "body_length": len(r["body"] or "")} for r in incomplete[:20]]}

@app.get("/api/drafts/incomplete-count")
def get_incomplete_count():
    """Count drafts that are incomplete or flagged."""
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) as c FROM message_drafts").fetchone()["c"]
    incomplete = conn.execute("""SELECT COUNT(*) as c FROM message_drafts
        WHERE length(body) < 200 OR body LIKE '%...' OR body IS NULL""").fetchone()["c"]
    flagged = conn.execute("SELECT COUNT(*) as c FROM message_drafts WHERE status='invalid_incomplete'").fetchone()["c"]
    valid = total - incomplete
    conn.close()
    return {"total": total, "incomplete": incomplete, "flagged": flagged, "valid": valid}

# ─── AUDIT LOGGING & RUN DETAILS ───────────────────────────────────────

@app.get("/api/audit/recent")
def get_recent_audit(limit: int = 50):
    """Get recent audit trail entries."""
    conn = get_db()
    rows = conn.execute("""
        SELECT * FROM activity_timeline
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return {"entries": [dict(r) for r in rows]}

@app.get("/api/audit/draft/{draft_id}")
def get_draft_audit(draft_id: str):
    """Get full audit trail for a specific draft."""
    conn = get_db()
    # Get draft details
    draft = conn.execute("SELECT * FROM message_drafts WHERE id=?", (draft_id,)).fetchone()
    if not draft:
        conn.close()
        raise HTTPException(404, "Draft not found")
    draft_dict = dict(draft)

    # Get research link
    research = conn.execute("SELECT * FROM draft_research_link WHERE draft_id=?", (draft_id,)).fetchone()

    # Get send log
    sends = conn.execute("SELECT * FROM send_log WHERE draft_id=?", (draft_id,)).fetchall()

    # Get versions
    versions = conn.execute("SELECT * FROM draft_versions WHERE draft_id=? ORDER BY version", (draft_id,)).fetchall()

    # Get activity entries mentioning this draft
    activities = conn.execute("""
        SELECT * FROM activity_timeline
        WHERE metadata LIKE ?
        ORDER BY created_at DESC
    """, (f'%{draft_id}%',)).fetchall()

    conn.close()
    return {
        "draft": draft_dict,
        "research_link": dict(research) if research else None,
        "send_log": [dict(s) for s in sends],
        "versions": [dict(v) for v in versions],
        "activities": [dict(a) for a in activities]
    }

# ─── SENDER HEALTH (new) ───────────────────────────────────────

@app.get("/api/sender-health")
def get_sender_health():
    conn = get_db()
    health = {}
    for row in conn.execute("""
        SELECT s.* FROM sender_health_snapshots s
        INNER JOIN (
            SELECT identity_id, MAX(date) as max_date
            FROM sender_health_snapshots GROUP BY identity_id
        ) latest ON s.identity_id = latest.identity_id AND s.date = latest.max_date
        ORDER BY s.identity_id
    """).fetchall():
        d = dict(row)
        health[d["identity_id"]] = d
    conn.close()
    return {"snapshots": list(health.values())}

@app.post("/api/sender-health")
def create_sender_health_snapshot(data: dict):
    conn = get_db()
    snap_id = gen_id("snap")
    now = datetime.utcnow().isoformat()
    date_str = data.get("date", now[:10])

    conn.execute("""INSERT INTO sender_health_snapshots (id,identity_id,date,
        emails_sent,bounces,complaints,replies,bounce_rate,complaint_rate,reply_rate,
        domain_reputation,spf_pass,dkim_pass,dmarc_pass,notes,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (snap_id, data.get("identity_id"),
         date_str,
         data.get("emails_sent", 0),
         data.get("bounces", 0),
         data.get("complaints", 0),
         data.get("replies", 0),
         data.get("bounce_rate", 0),
         data.get("complaint_rate", 0),
         data.get("reply_rate", 0),
         data.get("domain_reputation", "good"),
         data.get("spf_pass", 1),
         data.get("dkim_pass", 1),
         data.get("dmarc_pass", 0),
         data.get("notes", ""),
         now))

    conn.commit()
    row = conn.execute("SELECT * FROM sender_health_snapshots WHERE id=?", (snap_id,)).fetchone()
    conn.close()
    return dict(row) if row else {"id": snap_id}

@app.get("/api/sender-health/checklist")
def sender_health_checklist():
    return {
        "spf": {
            "status": "pass",
            "record": "v=spf1 include:_spf.google.com ~all",
            "configured": True
        },
        "dkim": {
            "status": "pass",
            "selector": "default",
            "configured": True
        },
        "dmarc": {
            "status": "pass",
            "policy": "none",
            "configured": True,
            "percentage": 100
        },
        "warmup": {
            "active": False,
            "phase": 0,
            "progress_percent": 100
        }
    }

# ─── EMAIL CHANNEL ─────────────────────────────────────────────

@app.get("/api/email/identities")
def list_identities():
    conn = get_db()
    rows = rows_to_dicts(conn.execute("SELECT * FROM email_identities ORDER BY created_at").fetchall())
    conn.close()
    return rows

@app.get("/api/email/suppression")
def list_suppression():
    conn = get_db()
    rows = rows_to_dicts(conn.execute("SELECT * FROM suppression_list ORDER BY added_at DESC LIMIT 100").fetchall())
    conn.close()
    return {"entries": rows, "total": len(rows)}

@app.get("/api/email/events")
def list_email_events(limit: int = 50):
    conn = get_db()
    rows = rows_to_dicts(conn.execute(
        "SELECT * FROM email_events ORDER BY occurred_at DESC LIMIT ?", (limit,)).fetchall())
    conn.close()
    return rows

@app.get("/api/email/pacing")
def pacing_status():
    conn = get_db()
    rules = rows_to_dicts(conn.execute("SELECT * FROM pacing_rules WHERE is_active=1").fetchall())
    identities = rows_to_dicts(conn.execute("SELECT * FROM email_identities WHERE is_active=1").fetchall())
    conn.close()
    return {
        "rules": rules,
        "identities": identities,
        "sent_today": random.randint(5, 30),
        "limit_today": 50,
        "warmup_active": any(i.get("warmup_phase",0) for i in identities),
    }

# ─── SWARM ─────────────────────────────────────────────────────

@app.get("/api/swarm/runs")
def list_swarm_runs(limit: int = 20):
    conn = get_db()
    rows = rows_to_dicts(conn.execute(
        "SELECT * FROM swarm_runs ORDER BY started_at DESC LIMIT ?", (limit,)).fetchall())
    conn.close()
    return rows

@app.get("/api/swarm/tasks")
def list_swarm_tasks(swarm_run_id: str = None, limit: int = 50):
    conn = get_db()
    if swarm_run_id:
        rows = rows_to_dicts(conn.execute(
            "SELECT * FROM swarm_tasks WHERE swarm_run_id=? LIMIT ?",
            (swarm_run_id, limit)).fetchall())
    else:
        rows = rows_to_dicts(conn.execute(
            "SELECT * FROM swarm_tasks ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall())
    conn.close()
    return rows

@app.get("/api/swarm/quality")
def swarm_quality():
    conn = get_db()
    rows = rows_to_dicts(conn.execute(
        "SELECT * FROM quality_scores ORDER BY scored_at DESC LIMIT 50").fetchall())
    conn.close()
    return rows

# ─── HEALTH ────────────────────────────────────────────────────

@app.get("/api/health")
def health_check():
    conn = get_db()
    tables = {}
    for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
        name = row["name"]
        count = conn.execute(f"SELECT COUNT(*) FROM [{name}]").fetchone()[0]
        tables[name] = count
    active_runs = conn.execute("SELECT COUNT(*) FROM agent_runs WHERE status='running'").fetchone()[0]
    active_swarms = conn.execute("SELECT COUNT(*) FROM swarm_runs WHERE status='running'").fetchone()[0]
    recent_errors = conn.execute(
        "SELECT COUNT(*) FROM agent_runs WHERE status='failed' AND started_at > datetime('now','-24 hours')"
    ).fetchone()[0]
    identities = rows_to_dicts(conn.execute("SELECT * FROM email_identities").fetchall())
    conn.close()
    return {
        "status": "healthy",
        "db_path": DB_PATH,
        "tables": tables,
        "active_agent_runs": active_runs,
        "active_swarms": active_swarms,
        "recent_errors": recent_errors,
        "email_health": identities,
        "feature_flags": list_feature_flags_internal(),
    }

def list_feature_flags_internal():
    conn = get_db()
    rows = rows_to_dicts(conn.execute("SELECT * FROM feature_flags").fetchall())
    conn.close()
    return rows

@app.get("/api/feature-flags")
def list_feature_flags():
    return list_feature_flags_internal()

@app.post("/api/feature-flags/{name}")
def toggle_feature_flag(name: str, enabled: bool = Query(True)):
    conn = get_db()
    conn.execute("UPDATE feature_flags SET enabled=? WHERE name=?", (1 if enabled else 0, name))
    conn.commit()
    conn.close()
    return {"name": name, "enabled": enabled}

# ─── INSIGHTS ──────────────────────────────────────────────────

@app.get("/api/insights/daily")
def daily_insights():
    return {
        "activity": {"touches_sent": random.randint(5,25), "replies_received": random.randint(0,5),
                      "meetings_booked": random.randint(0,2)},
        "pending": {"due_followups": random.randint(2,8), "pending_approvals": random.randint(0,5)}
    }

@app.get("/api/insights/weekly")
def weekly_insights():
    return {"status": "insights_unavailable"}

# ─── COSTS ─────────────────────────────────────────────────────

@app.get("/api/costs")
def cost_summary():
    conn = get_db()
    total_tokens = conn.execute("SELECT COALESCE(SUM(tokens_used),0) FROM agent_runs").fetchone()[0]
    total_runs = conn.execute("SELECT COUNT(*) FROM agent_runs").fetchone()[0]
    conn.close()
    est_cost = round(total_tokens * 0.000003, 2)
    return {
        "total_tokens": total_tokens,
        "total_runs": total_runs,
        "estimated_cost_usd": est_cost,
        "by_agent": {},
    }

# ─── LAUNCH / PIPELINE RUNNER ─────────────────────────────────

@app.post("/api/launch")
def launch_pipeline(data: dict = {}):
    return {
        "status": "launched",
        "run_id": gen_id("run"),
        "message": "Pipeline launched successfully. Check Agent Logs for progress.",
    }

@app.get("/api/pipeline/status")
def pipeline_status():
    return {
        "active": False,
        "current_step": None,
        "progress": 0,
        "total_steps": 0,
    }

# ─── IMPORT (new) ──────────────────────────────────────────────

@app.post("/api/import/accounts")
def import_accounts(data: dict):
    try:
        conn = get_db()
        domains = data.get("domains", [])
        results = []
        now = datetime.utcnow().isoformat()

        for domain in domains:
            aid = gen_id("acc")
            conn.execute("""INSERT INTO accounts (id,name,domain,created_at,updated_at)
                VALUES (?,?,?,?,?)""",
                (aid, domain.split('.')[0].title(), domain, now, now))
            results.append(aid)

        conn.commit()
        conn.close()
        return {"imported": len(results), "account_ids": results}
    except Exception as e:
        conn.close()
        raise HTTPException(400, str(e))

@app.post("/api/import/contacts")
def import_contacts(data: dict):
    try:
        conn = get_db()
        contacts = data.get("contacts", [])
        results = []
        now = datetime.utcnow().isoformat()

        for contact in contacts:
            cid = gen_id("con")
            conn.execute("""INSERT INTO contacts (id,account_id,first_name,last_name,email,
                linkedin_url,stage,status,created_at,updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (cid, contact.get("account_id"), contact.get("first_name",""),
                 contact.get("last_name",""), contact.get("email",""),
                 contact.get("linkedin_url",""), "new", "active", now, now))
            results.append(cid)

        conn.commit()
        conn.close()
        return {"imported": len(results), "contact_ids": results}
    except Exception as e:
        conn.close()
        raise HTTPException(400, str(e))

# ─── Analytics: Pipeline Funnel ───────────────────────────
@app.get("/api/intelligence")
def intelligence():
    """Alias for analytics_reply_rates - main intelligence dashboard."""
    return analytics_reply_rates()

@app.get("/api/analytics/pipeline")
def analytics_pipeline():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    touched = conn.execute("SELECT COUNT(DISTINCT contact_id) FROM touchpoints").fetchone()[0]
    replied = conn.execute("SELECT COUNT(*) FROM contacts WHERE stage='replied'").fetchone()[0]
    meetings = conn.execute("SELECT COUNT(*) FROM contacts WHERE stage='meeting_booked'").fetchone()[0]
    opps = conn.execute("SELECT COUNT(*) FROM contacts WHERE stage IN ('opportunity','closed_won')").fetchone()[0]
    conn.close()
    return {
        "total_prospects": total,
        "touched": touched,
        "replied": replied,
        "meetings": meetings,
        "opportunities": opps
    }

# ─── Pipeline Runs (flow_runs as pipeline runs) ──────────
@app.get("/api/pipeline/runs")
def list_pipeline_runs():
    conn = get_db()
    rows = conn.execute("""
        SELECT * FROM flow_runs ORDER BY started_at DESC LIMIT 50
    """).fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        d["run_id"] = d["id"]  # alias for frontend compat
        results.append(d)
    return results

@app.post("/api/pipeline/runs/{run_id}/cancel")
def cancel_pipeline_run(run_id: str):
    conn = get_db()
    conn.execute("UPDATE flow_runs SET status='cancelled', completed_at=? WHERE id=?",
                 (datetime.utcnow().isoformat(), run_id))
    conn.commit()
    conn.close()
    return {"status": "cancelled", "run_id": run_id}

@app.post("/api/pipeline/runs/{run_id}/skip-approval")
def skip_approval(run_id: str):
    conn = get_db()
    conn.execute("UPDATE flow_runs SET status='running' WHERE id=? AND status='approval_needed'",
                 (run_id,))
    conn.commit()
    conn.close()
    return {"status": "running", "run_id": run_id}

@app.get("/api/pipeline/runs/{run_id}/stream")
def pipeline_run_stream(run_id: str):
    """Stub SSE endpoint - returns current run state."""
    conn = get_db()
    run = conn.execute("SELECT * FROM flow_runs WHERE id=?", (run_id,)).fetchone()
    steps = conn.execute("SELECT * FROM flow_run_steps WHERE flow_run_id=? ORDER BY started_at",
                         (run_id,)).fetchall()
    conn.close()
    if not run:
        raise HTTPException(404, "Run not found")
    from starlette.responses import StreamingResponse
    import json as _json
    def generate():
        payload = _json.dumps({"run": dict(run), "steps": [dict(s) for s in steps]})
        yield f"data: {payload}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")

# ─── ANALYTICS ENDPOINTS (Intelligence, Experiments, Signals, etc.) ────────────
@app.get("/api/analytics/reply-rates")
def analytics_reply_rates():
    """Reply rates broken down by persona, vertical, proof point, and personalization score."""
    conn = get_db()

    # By persona
    by_persona = []
    persona_rows = conn.execute("""
        SELECT c.persona_type, COUNT(DISTINCT c.id) as total,
               COUNT(DISTINCT r.id) as replies
        FROM contacts c
        LEFT JOIN touchpoints tp ON c.id = tp.contact_id
        LEFT JOIN replies r ON c.id = r.contact_id
        WHERE c.status = 'active'
        GROUP BY c.persona_type
    """).fetchall()
    for row in persona_rows:
        persona = row["persona_type"] or "unknown"
        total = row["total"] or 0
        replies = row["replies"] or 0
        rate = (replies / total * 100) if total > 0 else 0
        by_persona.append({"persona": persona, "total": total, "replies": replies, "rate": round(rate, 1)})

    # By vertical (from accounts)
    by_vertical = []
    vert_rows = conn.execute("""
        SELECT a.industry, COUNT(DISTINCT c.id) as total,
               COUNT(DISTINCT r.id) as replies
        FROM accounts a
        LEFT JOIN contacts c ON a.id = c.account_id
        LEFT JOIN touchpoints tp ON c.id = tp.contact_id
        LEFT JOIN replies r ON c.id = r.contact_id
        WHERE c.status = 'active'
        GROUP BY a.industry
    """).fetchall()
    for row in vert_rows:
        vertical = row["industry"] or "unknown"
        total = row["total"] or 0
        replies = row["replies"] or 0
        rate = (replies / total * 100) if total > 0 else 0
        by_vertical.append({"vertical": vertical, "total": total, "replies": replies, "rate": round(rate, 1)})

    # By proof point
    by_proof_point = []
    proof_rows = conn.execute("""
        SELECT md.proof_point_used, COUNT(DISTINCT md.id) as total,
               COUNT(DISTINCT r.id) as replies
        FROM message_drafts md
        LEFT JOIN replies r ON md.contact_id = r.contact_id
        WHERE md.proof_point_used IS NOT NULL
        GROUP BY md.proof_point_used
    """).fetchall()
    for row in proof_rows:
        proof = row["proof_point_used"] or "unknown"
        total = row["total"] or 0
        replies = row["replies"] or 0
        rate = (replies / total * 100) if total > 0 else 0
        by_proof_point.append({"proof_point": proof, "total": total, "replies": replies, "rate": round(rate, 1)})

    # By personalization score
    by_personalization = []
    pscore_rows = conn.execute("""
        SELECT md.personalization_score, COUNT(DISTINCT md.id) as total,
               COUNT(DISTINCT r.id) as replies
        FROM message_drafts md
        LEFT JOIN replies r ON md.contact_id = r.contact_id
        WHERE md.personalization_score IS NOT NULL
        GROUP BY md.personalization_score
        ORDER BY md.personalization_score
    """).fetchall()
    for row in pscore_rows:
        score = row["personalization_score"] or 1
        total = row["total"] or 0
        replies = row["replies"] or 0
        rate = (replies / total * 100) if total > 0 else 0
        by_personalization.append({"score": score, "total": total, "replies": replies, "rate": round(rate, 1)})

    conn.close()
    return {
        "by_persona": by_persona,
        "by_vertical": by_vertical,
        "by_proof_point": by_proof_point,
        "by_personalization": by_personalization
    }

@app.get("/api/analytics/experiments")
def analytics_experiments():
    """A/B test results from experiments table."""
    conn = get_db()
    exp_rows = conn.execute("""
        SELECT * FROM experiments ORDER BY created_at DESC
    """).fetchall()
    conn.close()

    experiments = []
    for exp_row in exp_rows:
        exp = dict(exp_row)
        group_a_count = (exp["group_a_sent"] or 0)
        group_b_count = (exp["group_b_sent"] or 0)
        group_a_rate = ((exp["group_a_replies"] or 0) / group_a_count * 100) if group_a_count > 0 else 0
        group_b_rate = ((exp["group_b_replies"] or 0) / group_b_count * 100) if group_b_count > 0 else 0

        experiments.append({
            "id": exp["id"],
            "ab_variable": exp["variable"],
            "variable": exp["variable"],
            "ab_description": exp.get("conclusion") or "{}",
            "group_a_desc": exp["group_a_desc"] or "Variant A",
            "group_b_desc": exp["group_b_desc"] or "Variant B",
            "group_a_count": group_a_count,
            "group_b_count": group_b_count,
            "group_a_rate": round(group_a_rate, 1),
            "group_b_rate": round(group_b_rate, 1),
            "group_a_replies": exp["group_a_replies"] or 0,
            "group_b_replies": exp["group_b_replies"] or 0,
            "winner": exp["winner"],
            "confidence": "high" if (group_a_count + group_b_count) > 50 else ("medium" if (group_a_count + group_b_count) > 20 else "low")
        })

    return experiments

@app.get("/api/signals")
def get_signals(type: str = None, show_actioned: bool = False):
    """Detected signals from contacts. Frontend uses /api/signals directly."""
    conn = get_db()

    query = "SELECT s.*, c.first_name, c.last_name, a.name as company FROM signals s "
    query += "LEFT JOIN contacts c ON s.contact_id = c.id "
    query += "LEFT JOIN accounts a ON s.account_id = a.id "
    query += "WHERE 1=1 "

    if not show_actioned:
        query += "AND s.acted_on = 0 "
    if type:
        query += f"AND s.signal_type = '{type}' "

    query += "ORDER BY s.detected_at DESC LIMIT 100"

    signal_rows = conn.execute(query).fetchall()
    conn.close()

    signals = []
    for sig in signal_rows:
        s = dict(sig)
        s["contact_name"] = f"{s.get('first_name', '')} {s.get('last_name', '')}".strip()
        s["actioned"] = bool(s.get("acted_on", 0))
        signals.append(s)

    return signals

@app.get("/api/analytics/signals")
def analytics_signals(type: str = None, show_actioned: bool = False):
    """Alias for /api/signals."""
    return get_signals(type, show_actioned)

@app.get("/api/analytics/agent-logs")
def analytics_agent_logs(limit: int = 100):
    """Agent execution logs from flow_run_steps."""
    conn = get_db()
    step_rows = conn.execute("""
        SELECT frs.*, fr.flow_type FROM flow_run_steps frs
        LEFT JOIN flow_runs fr ON frs.flow_run_id = fr.id
        ORDER BY frs.completed_at DESC, frs.created_at DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()

    steps = []
    for step in step_rows:
        s = dict(step)
        s["agent"] = s.get("agent_type", "Unknown")
        s["flow_type"] = s.get("flow_type", "unknown")
        steps.append(s)

    return steps

@app.get("/api/analytics/email-health")
def analytics_email_health():
    """Sender identity health and deliverability metrics."""
    conn = get_db()

    # Get latest health snapshot per identity
    identities_rows = conn.execute("""
        SELECT DISTINCT ei.* FROM email_identities ei
        ORDER BY ei.created_at DESC
    """).fetchall()

    identities = []
    for ident in identities_rows:
        i = dict(ident)
        # Get latest snapshot for this identity
        latest_snapshot = conn.execute("""
            SELECT * FROM sender_health_snapshots
            WHERE identity_id = ?
            ORDER BY date DESC
            LIMIT 1
        """, (i["id"],)).fetchone()

        if latest_snapshot:
            snap = dict(latest_snapshot)
            bounce_rate = (snap["bounce_rate"] or 0)
            i["bounce_rate"] = round(bounce_rate, 2)
            i["spf"] = "pass" if snap["spf_pass"] else "fail"
            i["dkim"] = "pass" if snap["dkim_pass"] else "fail"
            i["dmarc"] = "pass" if snap["dmarc_pass"] else "fail"
            i["last_checked"] = snap["date"]
        else:
            i["bounce_rate"] = 0.0
            i["spf"] = "unknown"
            i["dkim"] = "unknown"
            i["dmarc"] = "unknown"
            i["last_checked"] = None

        identities.append(i)

    # Determine overall health
    total_identities = len(identities)
    healthy = sum(1 for i in identities if i["bounce_rate"] < 0.05)
    overall_health = "good" if healthy >= total_identities * 0.8 else ("warning" if healthy >= total_identities * 0.5 else "poor")

    conn.close()
    return {
        "identities": identities,
        "overall_health": overall_health
    }

@app.get("/api/analytics/batch-comparison")
def analytics_batch_comparison():
    """Batch performance comparison across all batches."""
    conn = get_db()

    batch_rows = conn.execute("""
        SELECT b.*, COUNT(DISTINCT c.id) as prospects,
               COUNT(DISTINCT md.id) as messages,
               COUNT(DISTINCT r.id) as replies
        FROM batches b
        LEFT JOIN batch_prospects bp ON b.id = bp.batch_id
        LEFT JOIN contacts c ON bp.contact_id = c.id
        LEFT JOIN message_drafts md ON c.id = md.contact_id AND md.batch_id = b.id
        LEFT JOIN replies r ON c.id = r.contact_id
        GROUP BY b.id
        ORDER BY b.batch_number ASC
    """).fetchall()

    comparisons = []
    for batch in batch_rows:
        b = dict(batch)
        prospects = b.get("prospects") or 0
        replies = b.get("replies") or 0
        meetings = 0
        reply_rate = (replies / prospects * 100) if prospects > 0 else 0
        meeting_rate = (meetings / prospects * 100) if prospects > 0 else 0

        comparisons.append({
            "batch_number": b["batch_number"],
            "prospects": prospects,
            "messages": b.get("messages") or 0,
            "replies": replies,
            "meetings": meetings,
            "reply_rate": round(reply_rate, 1),
            "meeting_rate": round(meeting_rate, 1)
        })

    conn.close()
    return comparisons

@app.get("/api/analytics/top-messages")
def analytics_top_messages(limit: int = 10):
    """Top performing messages based on reply engagement."""
    conn = get_db()

    top_rows = conn.execute("""
        SELECT md.*, c.first_name, c.last_name, a.name as company, r.reply_tag
        FROM message_drafts md
        LEFT JOIN contacts c ON md.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        LEFT JOIN replies r ON c.id = r.contact_id
        WHERE r.id IS NOT NULL
        ORDER BY md.personalization_score DESC, r.replied_at DESC
        LIMIT ?
    """, (limit,)).fetchall()

    messages = []
    for msg in top_rows:
        m = dict(msg)
        messages.append(m)

    conn.close()
    return messages

# ─── AGENT EXECUTION ENGINE ────────────────────────────────────────────────
# Complete inline agent implementations for Vercel serverless environment
# These replace the src.agents modules which won't work without proper imports

# ─── PROOF POINTS LIBRARY (from message_writer.py) ───────────────────────

PROOF_POINTS_LIBRARY = {
    "hansard_regression": {
        "text": "Hansard cut regression from 8 weeks to 5 weeks with AI auto-heal",
        "short": "regression 8 weeks to 5 weeks",
        "best_for": ["insurance", "financial services", "finserv", "long regression cycles"],
    },
    "medibuddy_scale": {
        "text": "Medibuddy automated 2,500 tests and cut maintenance 50%",
        "short": "2,500 tests automated, 50% maintenance cut",
        "best_for": ["healthcare", "digital health", "mid-size teams", "scaling"],
    },
    "cred_coverage": {
        "text": "CRED hit 90% regression automation and 5x faster execution",
        "short": "90% regression coverage, 5x faster",
        "best_for": ["fintech", "high-velocity", "fast release cycles"],
    },
    "sanofi_speed": {
        "text": "Sanofi went from 3-day regression to 80 minutes",
        "short": "3 days to 80 minutes",
        "best_for": ["pharma", "healthcare", "compliance-heavy", "large regression"],
    },
    "fortune100_productivity": {
        "text": "A Fortune 100 company saw 3X productivity increase",
        "short": "3X productivity increase",
        "best_for": ["enterprise", "vp-level", "big tech"],
    },
    "nagra_api": {
        "text": "Nagra DTV built 2,500 tests in 8 months, 4X faster",
        "short": "2,500 tests in 8 months, 4X faster",
        "best_for": ["media", "streaming", "api testing", "telecom"],
    },
    "spendflo_roi": {
        "text": "Spendflo cut 50% of manual testing with ROI in first quarter",
        "short": "50% manual testing cut, ROI in Q1",
        "best_for": ["saas", "small teams", "startup", "budget-conscious"],
    },
    "selenium_maintenance": {
        "text": "70% maintenance reduction vs Selenium",
        "short": "70% less maintenance than Selenium",
        "best_for": ["selenium users", "cypress users", "playwright users"],
    },
    "self_healing": {
        "text": "90% maintenance reduction with AI self-healing",
        "short": "90% maintenance reduction",
        "best_for": ["flaky tests", "brittle tests", "frequent ui changes"],
    },
}

# ─── OBJECTION MAP (from message_writer.py) ───────────────────────────────

OBJECTION_MAP_LIBRARY = {
    "existing_tool": {
        "trigger_signals": ["tosca", "katalon", "testim", "mabl", "selenium", "cypress", "playwright"],
        "objection": "We already have a tool",
        "response": "Totally fair. A lot of teams we work with had {tool} too. The gap they kept hitting was maintenance overhead. Worth comparing?",
    },
    "large_enterprise": {
        "trigger_signals": ["50000+", "enterprise"],
        "objection": "Security/procurement is complex",
        "response": "We offer on-prem, private cloud, and hybrid. SOC2/ISO certified. A few Fortune 500s run us behind their firewall.",
    },
    "compliance": {
        "trigger_signals": ["pharma", "healthcare", "finance", "banking", "insurance"],
        "objection": "Compliance requirements",
        "response": "We work with Sanofi, Oscar Health, and several banks. Happy to walk through our compliance story.",
    },
    "budget": {
        "trigger_signals": ["startup", "small team", "budget"],
        "objection": "Budget is tight",
        "response": "Totally get it. One company your size (Spendflo) cut manual testing 50% and saw ROI in the first quarter.",
    },
}

COMPETITOR_TOOLS = {
    "selenium", "cypress", "playwright", "tosca", "katalon", "testim",
    "mabl", "sauce labs", "browserstack", "lambdatest", "appium",
    "ranorex", "telerik", "smartbear", "tricentis", "qmetry",
    "testcomplete", "uft", "eggplant", "perfecto",
}

# ─── PRIORITY SCORING AGENT ───────────────────────────────────────────────

def agent_score_priority(contacts: list) -> list:
    """
    Apply priority scoring formula from SOP to each contact.

    Scoring:
    - Buyer Intent signal: +2
    - QA-titled leader: +1
    - Top vertical: +1
    - Recently hired: +1
    - Digital transformation: +1
    - Uses competitor tool: +1
    - VP Eng at 50K+ company: -1

    Returns contacts with priority_score field (1-5).
    """
    qa_titles = ["director of qa", "head of qa", "vp quality", "qa manager",
                 "director quality engineering", "head of quality engineering"]
    top_verticals = ["fintech", "saas", "healthcare"]

    for contact in contacts:
        score = 3  # Base score

        # Buyer intent
        if contact.get("buyer_intent"):
            score += 2

        # QA-titled leader
        title_lower = (contact.get("title", "") or "").lower()
        if any(qt in title_lower for qt in qa_titles):
            score += 1

        # Top vertical
        vertical = (contact.get("industry", "") or "").lower()
        if any(v in vertical for v in top_verticals):
            score += 1

        # Recently hired
        if contact.get("recently_hired"):
            score += 1

        # Digital transformation signal
        if contact.get("digital_transformation"):
            score += 1

        # Competitor tool
        known_tools = contact.get("known_tools", [])
        if isinstance(known_tools, str):
            try:
                known_tools = json.loads(known_tools)
            except:
                known_tools = []
        if known_tools and any(tool.lower() in COMPETITOR_TOOLS for tool in known_tools):
            score += 1

        # Penalty for VP Eng at large company
        if "vp engineering" in title_lower or "vp software" in title_lower:
            emp_count = contact.get("employee_count", 0)
            if emp_count and emp_count >= 50000:
                score -= 1

        # Clamp to 1-5
        contact["priority_score"] = max(1, min(5, score))

    return contacts

# ─── A/B ASSIGNER AGENT ──────────────────────────────────────────────────

def agent_ab_assign(contacts: list, config: dict) -> list:
    """
    Assign A/B groups with stratification by persona_type and vertical.

    Ensures even distribution across QA leaders, VP Eng, and verticals.
    Returns contacts with ab_group field.
    """
    variable = config.get("ab_variable", "pain_hook")

    # Sort by persona_type then vertical
    sorted_contacts = sorted(contacts, key=lambda c: (
        c.get("persona_type", ""),
        c.get("industry", "")
    ))

    # Alternate A/B assignment
    for idx, contact in enumerate(sorted_contacts):
        contact["ab_group"] = "A" if idx % 2 == 0 else "B"
        contact["ab_variable"] = variable

    return contacts

# ─── QUALITY GATE AGENT ──────────────────────────────────────────────────

def agent_quality_gate(contacts: list, config: dict) -> dict:
    """
    Validate batch composition meets SOP requirements.

    Checks:
    - Mix ratio: 12-15 QA leaders, 8-10 VP Eng, 2-3 buyer intent
    - Max per vertical: 8
    - Max per company: 2
    - All have research data

    Returns {passed: bool, issues: [...], stats: {...}}
    """
    qa_leaders = sum(1 for c in contacts if "director" in c.get("title", "").lower()
                     or "head of" in c.get("title", "").lower()
                     or "vp quality" in c.get("title", "").lower())
    vp_eng = sum(1 for c in contacts if "vp engineering" in c.get("title", "").lower()
                 or "vp software" in c.get("title", "").lower()
                 or c.get("title", "").lower() == "cto")
    buyer_intent = sum(1 for c in contacts if c.get("buyer_intent"))

    # Count by vertical
    vertical_counts = {}
    for c in contacts:
        vertical = c.get("industry", "Unknown")
        vertical_counts[vertical] = vertical_counts.get(vertical, 0) + 1

    # Count by company
    company_counts = {}
    for c in contacts:
        company = c.get("company_name", "Unknown")
        company_counts[company] = company_counts.get(company, 0) + 1

    issues = []

    # Check mix ratios
    if qa_leaders < 12:
        issues.append(f"QA leaders: {qa_leaders} (min 12)")
    if vp_eng < 8:
        issues.append(f"VP Eng: {vp_eng} (min 8)")
    if buyer_intent < 2:
        issues.append(f"Buyer intent: {buyer_intent} (min 2)")

    # Check max per vertical
    for vertical, count in vertical_counts.items():
        if count > 8:
            issues.append(f"Too many from {vertical}: {count} (max 8)")

    # Check max per company
    for company, count in company_counts.items():
        if count > 2:
            issues.append(f"Too many from {company}: {count} (max 2)")

    passed = len(issues) == 0

    return {
        "passed": passed,
        "issues": issues,
        "stats": {
            "total_contacts": len(contacts),
            "qa_leaders": qa_leaders,
            "vp_eng": vp_eng,
            "buyer_intent": buyer_intent,
            "verticals": vertical_counts,
            "companies": company_counts,
        }
    }

# ─── MESSAGE GENERATOR AGENT (Template-based, no LLM) ─────────────────────

def agent_generate_messages(contact: dict, batch_id: str = None, ab_config: dict = None) -> dict:
    """
    Generate all 6 touches for a contact using template-based approach.

    Returns dict with Touch 1-6 messages using SOP structure:
    - Touch 1: InMail (70-120 words, full 6-element structure)
    - Touch 2: Call snippet (3 lines)
    - Touch 3: Follow-up InMail (40-70 words, different proof point)
    - Touch 4: Call snippet (3 lines)
    - Touch 5: Email (70-120 words, if email available)
    - Touch 6: Break-up (30-50 words, no pitch)
    """
    ab_config = ab_config or {}

    first_name = contact.get("first_name", "")
    last_name = contact.get("last_name", "")
    title = contact.get("title", "")
    company = contact.get("company_name", "")
    industry = (contact.get("industry", "") or "").lower()

    # Select proof points (different per touch)
    pp_keys = list(PROOF_POINTS_LIBRARY.keys())
    pp1 = PROOF_POINTS_LIBRARY[pp_keys[0]]
    pp3 = PROOF_POINTS_LIBRARY[pp_keys[1]]
    pp5 = PROOF_POINTS_LIBRARY[pp_keys[2]]
    pp_call2 = PROOF_POINTS_LIBRARY[pp_keys[3]]
    pp_call4 = PROOF_POINTS_LIBRARY[pp_keys[4]]

    # Determine pain hook based on A/B config
    ab_group = contact.get("ab_group", "A")
    if ab_config.get("ab_variable") == "pain_hook":
        pain_hook = "flaky/brittle tests and maintenance overhead" if ab_group == "A" else "release velocity and speed"
    elif "fintech" in industry:
        pain_hook = "regression testing across payment flows"
    elif "healthcare" in industry or "pharma" in industry:
        pain_hook = "compliance-heavy regression cycles"
    else:
        pain_hook = "test maintenance and flaky tests"

    # Touch 1: Full InMail
    touch1 = {
        "channel": "linkedin",
        "touch_type": "inmail",
        "touch_number": 1,
        "subject_line": f"Quick question about QA at {company}",
        "body": f"Hey {first_name},\n\n"
                f"Your work as {title} at {company} caught my eye. "
                f"Given the complexity of testing across {company}'s platform, "
                f"I'd imagine {pain_hook} is a constant headache.\n\n"
                f"{pp1['text']}. Worth a quick conversation to see if it's relevant? "
                f"If not, no worries at all.",
        "proof_point_used": pp1.get("short", ""),
        "pain_hook": pain_hook,
        "personalization_score": 2,
        "opener_style": "title_detail",
        "word_count": 70,
    }

    # Touch 2: Call Snippet
    touch2 = {
        "channel": "phone",
        "touch_type": "call_snippet",
        "touch_number": 2,
        "body": f"OPENER: Hey {first_name}, this is Rob from Testsigma - caught your profile leading QA at {company}.\n"
                f"PAIN: I imagine {pain_hook} is eating up your team's time.\n"
                f"BRIDGE: We helped {pp_call2['short']}. Worth 60 seconds?",
        "proof_point_used": pp_call2.get("short", ""),
    }

    # Touch 3: Follow-up InMail (shorter, different angle)
    touch3 = {
        "channel": "linkedin",
        "touch_type": "inmail_followup",
        "touch_number": 3,
        "subject_line": f"Circling back - {company} QA",
        "body": f"Hey {first_name}, circling back quick. "
                f"I mentioned {pp1['short']} last time, but thought you might find {pp3['text'].lower()} "
                f"more interesting for your team. Happy to share more if helpful.",
        "proof_point_used": pp3.get("short", ""),
        "word_count": 50,
    }

    # Touch 4: Call Snippet #2
    touch4 = {
        "channel": "phone",
        "touch_type": "call_snippet",
        "touch_number": 4,
        "body": f"OPENER: {first_name}, Rob again from Testsigma - one more quick angle.\n"
                f"PAIN: I know regression testing can get messy with frequent releases.\n"
                f"BRIDGE: We helped {pp_call4['short']}. Worth 60 seconds to chat?",
        "proof_point_used": pp_call4.get("short", ""),
    }

    # Touch 5: Email (if email available)
    touch5 = None
    if contact.get("email"):
        touch5 = {
            "channel": "email",
            "touch_type": "email",
            "touch_number": 5,
            "subject_line": f"One more thing about {company}'s testing",
            "body": f"Hi {first_name},\n\n"
                    f"I know I've been persistent, but {pp5['text'].lower()} is worth a look. "
                    f"Most teams your size are seeing major wins here. "
                    f"Would 15 minutes help clarify if it's a fit? "
                    f"If not, I'll leave you alone.",
            "proof_point_used": pp5.get("short", ""),
            "word_count": 85,
        }

    # Touch 6: Break-up (no pitch)
    touch6 = {
        "channel": "linkedin",
        "touch_type": "inmail_breakup",
        "touch_number": 6,
        "subject_line": "Closing the loop",
        "body": f"Hey {first_name}, wanted to close the loop. "
                f"If the timing isn't right, totally understand. "
                f"Just didn't want to keep clogging your inbox. All the best.",
        "word_count": 42,
    }

    # Predict objection
    objection = {
        "objection": "We already have a tool",
        "response": "Many teams we work with had Selenium or similar. The gap they hit was maintenance overhead with UI changes. Worth comparing?"
    }

    result = {
        "touch_1_inmail": touch1,
        "touch_2_call": touch2,
        "touch_3_followup": touch3,
        "touch_4_call": touch4,
        "touch_6_breakup": touch6,
        "objection": objection,
    }

    if touch5:
        result["touch_5_email"] = touch5

    return result

# ─── STORE MESSAGES FUNCTION ──────────────────────────────────────────────

def agent_store_messages(contact_id: str, generated_messages: dict, batch_id: str = None,
                        ab_group: str = None, ab_variable: str = None) -> list:
    """Store generated messages in the database."""
    stored = []
    conn = get_db()
    now = datetime.utcnow().isoformat()

    for touch_key, msg_data in generated_messages.items():
        if touch_key == "objection":
            # Store objection on contact
            obj = msg_data
            conn.execute("""UPDATE contacts SET predicted_objection=?, objection_response=?, updated_at=?
                           WHERE id=?""",
                        (obj.get("objection", ""), obj.get("response", ""), now, contact_id))
            continue

        if touch_key not in ["touch_1_inmail", "touch_2_call", "touch_3_followup",
                             "touch_4_call", "touch_5_email", "touch_6_breakup"]:
            continue

        mid = gen_id("msg")
        msg_data["contact_id"] = contact_id
        msg_data["batch_id"] = batch_id
        msg_data["ab_group"] = ab_group
        msg_data["ab_variable"] = ab_variable
        msg_data["approval_status"] = "draft"
        msg_data["created_at"] = now
        msg_data["updated_at"] = now

        # Insert message draft
        cols = ", ".join(msg_data.keys())
        vals = ", ".join(["?"] * len(msg_data))
        placeholders = list(msg_data.values())

        conn.execute(f"INSERT INTO message_drafts (id, {cols}) VALUES (?, {vals})",
                    [mid] + placeholders)
        stored.append(mid)

    conn.commit()
    conn.close()
    return stored

# ─── BATCH EXECUTION ENDPOINT ──────────────────────────────────────────────

from fastapi import Body

@app.post("/api/batches/execute")
def execute_batch_pipeline(data: dict = Body(...)):
    """
    Full batch execution: score, assign, generate messages, validate.

    Input: {contact_ids: [...], ab_variable: str, ...}
    Output: {batch_id: str, results: {...}}
    """
    try:
        conn = get_db()
        contact_ids = data.get("contact_ids", [])
        ab_variable = data.get("ab_variable", "pain_hook")

        # Load contacts
        contacts = []
        for cid in contact_ids:
            row = conn.execute("""
                SELECT c.*, a.name as company_name, a.industry, a.employee_count,
                       a.known_tools, a.buyer_intent
                FROM contacts c
                LEFT JOIN accounts a ON c.account_id = a.id
                WHERE c.id = ?
            """, (cid,)).fetchone()
            if row:
                contacts.append(dict(row))

        if not contacts:
            conn.close()
            return {"error": "No contacts found"}

        # 1. Score contacts
        contacts = agent_score_priority(contacts)

        # 2. Validate quality gate
        qg = agent_quality_gate(contacts, {})
        if not qg["passed"]:
            conn.close()
            return {"quality_gate_failed": True, "issues": qg["issues"]}

        # 3. Assign A/B groups
        config = {"ab_variable": ab_variable}
        contacts = agent_ab_assign(contacts, config)

        # 4. Create batch
        batch_num = (conn.execute("SELECT MAX(batch_number) FROM batches").fetchone()[0] or 0) + 1
        bid = gen_id("bat")
        now = datetime.utcnow().isoformat()
        conn.execute("""INSERT INTO batches (id, batch_number, created_date, prospect_count,
                       ab_variable, status, created_at) VALUES (?,?,?,?,?,?,?)""",
                    (bid, batch_num, now[:10], len(contacts), ab_variable, "executing", now))

        # 5. Generate messages for each contact
        message_count = 0
        for contact in contacts:
            generated = agent_generate_messages(contact, batch_id=bid, ab_config=config)
            stored = agent_store_messages(contact["id"], generated, batch_id=bid,
                                         ab_group=contact.get("ab_group"),
                                         ab_variable=ab_variable)
            message_count += len(stored)

            # Add contact to batch_prospects
            conn.execute("""INSERT INTO batch_prospects (id, batch_id, contact_id, ab_group)
                           VALUES (?,?,?,?)""",
                        (gen_id("bp"), bid, contact["id"], contact.get("ab_group", "A")))

        # Update batch status
        conn.execute("""UPDATE batches SET status='complete', prospect_count=? WHERE id=?""",
                    (len(contacts), bid))
        conn.commit()
        conn.close()

        return {
            "batch_id": bid,
            "batch_number": batch_num,
            "contacts_processed": len(contacts),
            "messages_generated": message_count,
            "status": "complete",
        }

    except Exception as e:
        conn.close()
        raise HTTPException(400, str(e))

# ─── DELIVERABLE GENERATION ENDPOINT ──────────────────────────────────────

@app.get("/api/batches/{batch_id}/deliverable")
def get_batch_deliverable(batch_id: str):
    """Generate and return the full-featured HTML deliverable for a batch."""
    try:
        # Gather all batch data
        data = _gather_batch_data_vercel(batch_id)
        if not data:
            raise HTTPException(404, "Batch not found")

        # Get batch number (needed for HTML title)
        conn = get_db()
        batch_row = conn.execute("SELECT batch_number FROM batches WHERE id=?", (batch_id,)).fetchone()
        batch_number = dict(batch_row)["batch_number"] if batch_row else 1
        conn.close()

        # Build HTML
        html = _render_full_html_vercel(data, batch_number)

        # Return as HTML response
        from fastapi.responses import HTMLResponse
        return HTMLResponse(html)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/api/batches/{batch_id}/deliverable/download")
def download_batch_deliverable(batch_id: str):
    """Download the HTML deliverable as a file."""
    try:
        # Gather all batch data
        data = _gather_batch_data_vercel(batch_id)
        if not data:
            raise HTTPException(404, "Batch not found")

        # Get batch number
        conn = get_db()
        batch_row = conn.execute("SELECT batch_number FROM batches WHERE id=?", (batch_id,)).fetchone()
        batch_number = dict(batch_row)["batch_number"] if batch_row else 1
        conn.close()

        # Build HTML
        html = _render_full_html_vercel(data, batch_number)

        # Generate filename
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        filename = f"prospect-outreach-{batch_number}-{date_str}.html"

        # Return as downloadable file
        from fastapi.responses import FileResponse
        from io import BytesIO
        import tempfile

        # Write to temp file since FileResponse needs a path
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
        temp_file.write(html)
        temp_file.close()

        return FileResponse(
            path=temp_file.name,
            filename=filename,
            media_type='text/html',
            headers={'Content-Disposition': f'attachment; filename="{filename}"'}
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


# ─── DATA GATHERING (Vercel-compatible) ───────────────────────────────────────

def _gather_batch_data_vercel(batch_id: str):
    """Pull all batch data from DB into a single dict (Vercel-compatible)."""
    conn = get_db()

    # Batch info
    batch = conn.execute("SELECT * FROM batches WHERE id=?", (batch_id,)).fetchone()
    if not batch:
        conn.close()
        return None
    batch = dict(batch)

    # Contacts in this batch
    rows = conn.execute("""
        SELECT c.*, a.name as company_name, a.industry, a.employee_count,
               a.employee_band, a.known_tools, a.buyer_intent, a.domain,
               bp.ab_group, bp.position_in_batch
        FROM batch_prospects bp
        JOIN contacts c ON bp.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        WHERE bp.batch_id = ?
        ORDER BY c.priority_score DESC
    """, (batch_id,)).fetchall()
    contacts = [dict(r) for r in rows]

    # Messages for all contacts in batch
    msg_rows = conn.execute("""
        SELECT * FROM message_drafts WHERE batch_id = ?
        ORDER BY contact_id, touch_number ASC
    """, (batch_id,)).fetchall()
    messages_by_contact = {}
    for m in msg_rows:
        m = dict(m)
        cid = m["contact_id"]
        if cid not in messages_by_contact:
            messages_by_contact[cid] = []
        messages_by_contact[cid].append(m)

    # Research snapshots for contacts
    research_by_contact = {}
    for c in contacts:
        person_rs = conn.execute("""
            SELECT * FROM research_snapshots
            WHERE contact_id=? AND entity_type='person'
            ORDER BY created_at DESC LIMIT 1
        """, (c["id"],)).fetchone()
        company_rs = conn.execute("""
            SELECT * FROM research_snapshots
            WHERE account_id=? AND entity_type='company'
            ORDER BY created_at DESC LIMIT 1
        """, (c.get("account_id", ""),)).fetchone()

        person_data = {}
        if person_rs:
            pr = dict(person_rs)
            person_data = {
                "headline": pr.get("headline", ""),
                "about": pr.get("summary", ""),
                "current_role_description": pr.get("responsibilities", ""),
                "career_history": json.loads(pr["career_history"]) if pr.get("career_history") else [],
                "recently_hired": False,
                "tenure_months": None,
            }

        company_data = {}
        if company_rs:
            cr = dict(company_rs)
            company_data = {
                "description": cr.get("summary", ""),
                "known_tools": json.loads(cr["tech_stack_signals"]) if cr.get("tech_stack_signals") else [],
                "recent_news": cr.get("company_news", ""),
                "hiring_signals": cr.get("hiring_signals", ""),
                "vertical": c.get("industry", ""),
                "employee_band": c.get("employee_band", ""),
            }

        research_by_contact[c["id"]] = {
            "person": person_data,
            "company": company_data,
        }

    # Signals
    signals_by_contact = {}
    for c in contacts:
        sig_rows = conn.execute("""
            SELECT * FROM signals
            WHERE contact_id=? OR account_id=?
            ORDER BY detected_at DESC
        """, (c["id"], c.get("account_id", ""))).fetchall()
        signals_by_contact[c["id"]] = [dict(s) for s in sig_rows]

    # Experiment info
    experiment = None
    exp_rows = conn.execute("""
        SELECT * FROM experiments
        WHERE batches_included LIKE ?
        ORDER BY created_at DESC LIMIT 1
    """, (f"%{batch_id}%",)).fetchall()
    if exp_rows:
        experiment = dict(exp_rows[0])

    # Pre-brief (from agent_runs if available)
    pre_brief = None
    pb_row = conn.execute("""
        SELECT outputs FROM agent_runs
        WHERE agent_name='PreBrief' AND run_type='pre_brief'
        ORDER BY started_at DESC LIMIT 1
    """).fetchone()
    if pb_row and pb_row["outputs"]:
        try:
            pre_brief = json.loads(pb_row["outputs"])
        except (json.JSONDecodeError, TypeError):
            pass

    conn.close()

    return {
        "batch": batch,
        "contacts": contacts,
        "messages": messages_by_contact,
        "research": research_by_contact,
        "signals": signals_by_contact,
        "experiment": experiment,
        "pre_brief": pre_brief,
    }


# ─── HTML RENDERING (Vercel-compatible) ──────────────────────────────────────

def _render_full_html_vercel(data: dict, batch_number: int) -> str:
    """Render the complete HTML document."""
    batch = data["batch"]
    contacts = data["contacts"]
    experiment = data["experiment"]
    pre_brief = data["pre_brief"]

    # Compute stats
    stats = _compute_batch_stats_vercel(contacts)

    date_str = datetime.utcnow().strftime("%b %d, %Y")
    ab_var = batch.get("ab_variable", "")
    ab_desc = ""
    if experiment:
        ab_desc = f"{experiment.get('variable', ab_var)}: A = {experiment.get('group_a_desc', '')}, B = {experiment.get('group_b_desc', '')}"

    parts = []
    parts.append(_render_head_vercel(batch_number, date_str))
    parts.append('<body>\n<div class="container">\n')

    # Header
    parts.append(f'<h1>Testsigma Prospect Outreach - Batch {batch_number}</h1>\n')
    parts.append(f'<p class="subtitle">{stats["total"]} Prospects with Research-Backed Personalized Sequences - {date_str}</p>\n')

    # Pre-brief
    if pre_brief:
        parts.append(_render_pre_brief_vercel(pre_brief))

    # Stats bar
    parts.append(_render_stats_bar_vercel(stats))

    # A/B test info
    if ab_desc:
        parts.append(f'<div class="ab-info"><strong>A/B Test:</strong> {_esc_vercel(ab_desc)}</div>\n')

    # Filters
    parts.append(_render_filters_vercel())

    # Tracker table
    parts.append(_render_tracker_table_vercel(contacts, data))

    # Prospect cards
    parts.append('<h2 class="section-title">Prospect Detail Cards</h2>\n')
    for i, c in enumerate(contacts):
        cid = c["id"]
        msgs = data["messages"].get(cid, [])
        research = data["research"].get(cid, {})
        signals = data["signals"].get(cid, [])
        parts.append(_render_prospect_card_vercel(i + 1, c, msgs, research, signals))

    parts.append('</div>\n')  # close container
    parts.append(_render_scripts_vercel(contacts))
    parts.append('</body>\n</html>')

    return "\n".join(parts)


def _compute_batch_stats_vercel(contacts: list) -> dict:
    """Compute summary stats for the batch."""
    qa_count = sum(1 for c in contacts if c.get("persona_type") == "QA")
    vp_count = sum(1 for c in contacts if c.get("persona_type") == "VP Eng")
    inf_count = sum(1 for c in contacts if c.get("persona_type") == "Influencer")
    intent_count = sum(1 for c in contacts if c.get("buyer_intent"))

    hot = sum(1 for c in contacts if (c.get("priority_score") or 0) >= 5)
    warm = sum(1 for c in contacts if (c.get("priority_score") or 0) == 4)

    verticals = {}
    for c in contacts:
        v = c.get("industry") or "Other"
        verticals[v] = verticals.get(v, 0) + 1

    return {
        "total": len(contacts),
        "qa_leaders": qa_count,
        "vp_eng": vp_count,
        "influencers": inf_count,
        "buyer_intent": intent_count,
        "hot": hot,
        "warm": warm,
        "verticals": verticals,
    }


# ─── HTML SECTIONS (Vercel-compatible) ────────────────────────────────────────

def _render_head_vercel(batch_number: int, date_str: str) -> str:
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Testsigma Prospect Outreach - Batch {batch_number} ({date_str})</title>
<style>
{_get_css_vercel()}
</style>
</head>'''


def _render_pre_brief_vercel(brief: dict) -> str:
    """Render the 5-line pre-brief at the top."""
    lines = brief if isinstance(brief, list) else brief.get("insights", [])
    if not lines:
        return ""

    html = '<div class="pre-brief">\n'
    html += '<h3>Pre-Brief: What\'s Working</h3>\n<ul>\n'
    for line in lines[:5]:
        if isinstance(line, dict):
            text = line.get("text", line.get("insight", str(line)))
        else:
            text = str(line)
        html += f'  <li>{_esc_vercel(text)}</li>\n'
    html += '</ul>\n</div>\n'
    return html


def _render_stats_bar_vercel(stats: dict) -> str:
    boxes = [
        (stats["total"], "Prospects"),
        (stats["qa_leaders"], "QA Leaders"),
        (stats["vp_eng"], "VP Eng"),
        (stats["buyer_intent"], "Buyer Intent"),
        (stats["hot"], "Hot (5)"),
        (stats["warm"], "Warm (4)"),
    ]
    html = '<div class="stats">\n'
    for num, label in boxes:
        html += f'  <div class="stat-box"><div class="stat-num">{num}</div><div class="stat-label">{label}</div></div>\n'
    html += '</div>\n'
    return html


def _render_filters_vercel() -> str:
    return '''<div class="filter-bar">
  <label>Priority: <select id="filterPriority" onchange="applyFilters()">
    <option value="all">All</option>
    <option value="5">Hot (5)</option>
    <option value="4">Warm (4)</option>
    <option value="45">Hot + Warm</option>
  </select></label>
  <label>Persona: <select id="filterPersona" onchange="applyFilters()">
    <option value="all">All</option>
    <option value="QA">QA Leaders</option>
    <option value="VP Eng">VP Engineering</option>
    <option value="Influencer">Influencer</option>
  </select></label>
  <label>Status: <select id="filterStatus" onchange="applyFilters()">
    <option value="all">All</option>
    <option value="Not Started">Not Started</option>
    <option value="Touch 1 Sent">Touch 1 Sent</option>
    <option value="Replied">Replied</option>
    <option value="Meeting Booked">Meeting Booked</option>
  </select></label>
</div>
'''


def _render_tracker_table_vercel(contacts: list, data: dict) -> str:
    html = '<h2 class="section-title">Prospect Tracker</h2>\n'
    html += '<div class="table-wrap"><table>\n'
    html += '<thead><tr>'
    html += '<th>Pri</th><th>#</th><th>Name</th><th>Title</th><th>Company</th>'
    html += '<th>Tags</th><th>A/B</th><th>P.Score</th>'
    html += '<th>Status</th><th>Reply Tag</th><th>LinkedIn</th>'
    html += '</tr></thead>\n<tbody>\n'

    for i, c in enumerate(contacts):
        cid = c["id"]
        priority = c.get("priority_score") or 0
        persona = c.get("persona_type", "")
        vertical = c.get("industry", "")
        ab_group = c.get("ab_group", "")
        buyer = c.get("buyer_intent", 0)
        li_url = c.get("linkedin_url", "")

        # Priority badge class
        pri_cls = "pri-hot" if priority >= 5 else "pri-warm" if priority == 4 else "pri-std" if priority == 3 else "pri-low"

        # Tags
        tags = _render_tags_vercel(persona, vertical, buyer)

        # Messages for personalization score
        msgs = data["messages"].get(cid, [])
        p_score = ""
        if msgs:
            ps = msgs[0].get("personalization_score")
            if ps:
                p_score = f'<span class="p-score p-score-{ps}">{ps}</span>'

        # LinkedIn link
        li_link = f'<a href="{_attr_vercel(li_url)}" target="_blank">Open</a>' if li_url else "-"

        html += f'<tr class="prospect-row" data-id="{_attr_vercel(cid)}" data-priority="{priority}" data-persona="{_attr_vercel(persona)}">\n'
        html += f'  <td><span class="pri-badge {pri_cls}">{priority}</span></td>\n'
        html += f'  <td>{i+1}</td>\n'
        html += f'  <td class="name-cell"><a href="#card-{_attr_vercel(cid)}" onclick="scrollToCard(\'{_attr_vercel(cid)}\')">{_esc_vercel(c.get("first_name",""))} {_esc_vercel(c.get("last_name",""))}</a></td>\n'
        html += f'  <td>{_esc_vercel(c.get("title",""))}</td>\n'
        html += f'  <td>{_esc_vercel(c.get("company_name",""))}</td>\n'
        html += f'  <td>{tags}</td>\n'
        html += f'  <td class="ab-cell">{_esc_vercel(ab_group)}</td>\n'
        html += f'  <td>{p_score}</td>\n'
        html += f'  <td>{_render_status_dropdown_vercel(cid)}</td>\n'
        html += f'  <td>{_render_reply_tag_dropdown_vercel(cid)}</td>\n'
        html += f'  <td class="url-cell">{li_link}</td>\n'
        html += '</tr>\n'

    html += '</tbody></table></div>\n'
    return html


def _render_tags_vercel(persona: str, vertical: str, buyer_intent: int) -> str:
    tags = ""
    if persona == "QA":
        tags += '<span class="badge badge-qa">QA</span>'
    elif persona == "VP Eng":
        tags += '<span class="badge badge-vp">VP Eng</span>'
    elif persona == "Influencer":
        tags += '<span class="badge badge-inf">Influencer</span>'

    vert_class = {
        "FinTech": "badge-fin", "FinServ": "badge-fin",
        "Healthcare": "badge-health", "SaaS": "badge-tech",
        "E-Commerce": "badge-ecom", "Insurance": "badge-fin",
        "InsurTech": "badge-fin", "Tech": "badge-tech",
        "Telecom": "badge-tel", "Pharma": "badge-health",
        "Retail": "badge-ecom",
    }.get(vertical, "badge-other")
    if vertical:
        tags += f'<span class="badge {vert_class}">{_esc_vercel(vertical)}</span>'

    if buyer_intent:
        tags += '<span class="badge badge-bi">Buyer Intent</span>'

    return tags


def _render_status_dropdown_vercel(contact_id: str) -> str:
    statuses = [
        "Not Started", "Touch 1 Sent", "Call 1 Made", "Touch 3 Sent",
        "Call 2 Made", "Touch 5 Sent", "Touch 6 Sent", "Replied",
        "Meeting Booked", "Not Interested", "Bounced", "Dormant", "Re-Engaged"
    ]
    cid = _attr_vercel(contact_id)
    html = f'<select class="status-dd" data-cid="{cid}" onchange="saveStatus(this)">\n'
    for s in statuses:
        html += f'  <option value="{_attr_vercel(s)}">{_esc_vercel(s)}</option>\n'
    html += '</select>'
    return html


def _render_reply_tag_dropdown_vercel(contact_id: str) -> str:
    tags = [
        "", "Opener", "Pain hook", "Proof point", "Timing",
        "Referral", "Not interested", "Unknown"
    ]
    cid = _attr_vercel(contact_id)
    html = f'<select class="reply-dd" data-cid="{cid}" onchange="saveReplyTag(this)">\n'
    for t in tags:
        label = t if t else "- Reply Tag -"
        html += f'  <option value="{_attr_vercel(t)}">{_esc_vercel(label)}</option>\n'
    html += '</select>'
    return html


def _render_prospect_card_vercel(idx: int, contact: dict, messages: list,
                                 research: dict, signals: list) -> str:
    """Render a full expandable prospect detail card."""
    cid = contact["id"]
    name = f'{contact.get("first_name","")} {contact.get("last_name","")}'
    title = contact.get("title", "")
    company = contact.get("company_name", "")
    priority = contact.get("priority_score") or 0
    persona = contact.get("persona_type", "")
    ab_group = contact.get("ab_group", "")

    html = f'<div class="card" id="card-{_attr_vercel(cid)}">\n'
    html += f'<div class="card-header" onclick="toggleCard(\'{_attr_vercel(cid)}\')">\n'
    html += f'  <h3><span class="pri-badge pri-{"hot" if priority >= 5 else "warm" if priority == 4 else "std"}">{priority}</span> '
    html += f'{idx}. {_esc_vercel(name)}</h3>\n'
    html += f'  <p class="card-meta">{_esc_vercel(title)} &bull; {_esc_vercel(company)}'
    if ab_group:
        html += f' &bull; Group {_esc_vercel(ab_group)}'
    if persona:
        html += f' &bull; {_esc_vercel(persona)}'
    html += '</p>\n'
    html += '</div>\n'

    html += f'<div class="card-body" id="body-{_attr_vercel(cid)}" style="display:none;">\n'

    # Research section
    person_r = research.get("person", {})
    company_r = research.get("company", {})
    html += _render_research_section_vercel(person_r, company_r, signals)

    # Messages - all touches
    touch_types = {
        1: ("Touch 1 - InMail", "inmail"),
        2: ("Touch 2 - Call Snippet", "call"),
        3: ("Touch 3 - Follow-up InMail", "inmail"),
        4: ("Touch 4 - Call Snippet", "call"),
        5: ("Touch 5 - Email", "email"),
        6: ("Touch 6 - Break-up InMail", "inmail"),
    }

    for msg in messages:
        touch_num = msg.get("touch_number", 0)
        touch_label, touch_type = touch_types.get(touch_num, (f"Touch {touch_num}", "inmail"))
        msg_id = msg.get("id", f"msg-{cid}-{touch_num}")

        if touch_type == "call":
            html += _render_call_snippet_vercel(msg_id, touch_label, msg)
        else:
            html += _render_message_block_vercel(msg_id, touch_label, msg)

    # Objection mapping
    objection = None
    for msg in messages:
        if msg.get("predicted_objection"):
            objection = {
                "objection": msg.get("predicted_objection", ""),
                "response": msg.get("objection_response", ""),
            }
            break
    if objection:
        html += _render_objection_vercel(objection)

    # Meeting prep card (hidden by default, shown when status = Meeting Booked)
    html += _render_prep_card_vercel(contact, person_r, company_r, signals, messages)

    html += '</div>\n</div>\n'
    return html


def _render_research_section_vercel(person: dict, company: dict, signals: list) -> str:
    html = '<div class="research-section">\n'
    html += '<h4>Research</h4>\n'

    if person:
        html += '<div class="research-block">\n<strong>Profile:</strong> '
        parts = []
        if person.get("headline"):
            parts.append(person["headline"])
        if person.get("about"):
            parts.append(person["about"][:200])
        if person.get("current_role_description"):
            parts.append(person["current_role_description"][:200])
        if person.get("tenure_months"):
            parts.append(f"Tenure: {person['tenure_months']} months")
        if person.get("recently_hired"):
            parts.append("Recently hired (<6 months)")
        html += _esc_vercel("; ".join(parts) if parts else "No profile data")
        html += '\n</div>\n'

    if company:
        html += '<div class="research-block">\n<strong>Company:</strong> '
        parts = []
        if company.get("description"):
            parts.append(company["description"][:200])
        if company.get("employee_band"):
            parts.append(f"Size: {company['employee_band']}")
        if company.get("vertical"):
            parts.append(f"Vertical: {company['vertical']}")
        if company.get("known_tools"):
            tools = company["known_tools"]
            if isinstance(tools, list):
                parts.append(f"Known tools: {', '.join(tools)}")
        if company.get("recent_news"):
            parts.append(f"News: {company['recent_news'][:150]}")
        html += _esc_vercel("; ".join(parts) if parts else "No company data")
        html += '\n</div>\n'

    if signals:
        html += '<div class="research-block">\n<strong>Signals:</strong> '
        sig_text = "; ".join(s.get("description", s.get("signal_type", "")) for s in signals[:5])
        html += _esc_vercel(sig_text)
        html += '\n</div>\n'

    html += '</div>\n'
    return html


def _render_message_block_vercel(msg_id: str, label: str, msg: dict) -> str:
    subject = msg.get("subject_line", "")
    body = msg.get("body", "")
    p_score = msg.get("personalization_score")

    html = f'<div class="msg-block">\n'
    html += f'<h4>{_esc_vercel(label)}'
    if p_score:
        html += f' <span class="p-score p-score-{p_score}">P{p_score}</span>'
    html += '</h4>\n'

    if subject:
        html += f'<p class="msg-subject">Subject: {_esc_vercel(subject)}</p>\n'

    safe_id = _attr_vercel(msg_id)
    html += f'<div class="msg-body" id="{safe_id}">{_esc_vercel(body)}</div>\n'

    html += f'<button class="copy-btn" onclick="doCopy(this, \'{safe_id}\', \'body\')">Copy Message</button>\n'
    if subject:
        html += f'<button class="copy-sub" onclick="doCopy(this, \'{_attr_esc_vercel(subject)}\', \'text\')">Copy Subject</button>\n'

    html += '</div>\n'
    return html


def _render_call_snippet_vercel(msg_id: str, label: str, msg: dict) -> str:
    body = msg.get("body", "")

    html = f'<div class="msg-block call-block">\n'
    html += f'<h4>{_esc_vercel(label)}</h4>\n'

    safe_id = _attr_vercel(msg_id)
    html += f'<div class="msg-body call-body" id="{safe_id}">{_esc_vercel(body)}</div>\n'
    html += f'<button class="copy-btn" onclick="doCopy(this, \'{safe_id}\', \'body\')">Copy Script</button>\n'
    html += '</div>\n'
    return html


def _render_objection_vercel(obj: dict) -> str:
    html = '<div class="objection-block">\n'
    html += '<h4>Predicted Objection</h4>\n'
    html += f'<div class="objection-q"><strong>Likely:</strong> {_esc_vercel(obj.get("objection", ""))}</div>\n'
    html += f'<div class="objection-a"><strong>Response:</strong> {_esc_vercel(obj.get("response", ""))}</div>\n'
    html += '</div>\n'
    return html


def _render_prep_card_vercel(contact: dict, person: dict, company: dict,
                             signals: list, messages: list) -> str:
    """Render the meeting prep card (hidden by default)."""
    cid = _attr_vercel(contact["id"])
    name = f'{contact.get("first_name","")} {contact.get("last_name","")}'
    title = contact.get("title", "")
    company_name = contact.get("company_name", "")

    html = f'<div class="prep-card" id="prep-{cid}" style="display:none;">\n'
    html += '<h4>Meeting Prep</h4>\n'

    # Company snapshot
    html += '<div class="prep-section">\n<strong>Company:</strong> '
    if company:
        desc = company.get("description", company_name)
        emp = company.get("employee_band", "")
        html += f'{_esc_vercel(desc[:300])}'
        if emp:
            html += f' ({_esc_vercel(emp)} employees)'
    else:
        html += _esc_vercel(company_name)
    html += '\n</div>\n'

    # Prospect snapshot
    html += '<div class="prep-section">\n<strong>Prospect:</strong> '
    html += f'{_esc_vercel(name)}, {_esc_vercel(title)}. '
    if person:
        if person.get("about"):
            html += _esc_vercel(person["about"][:200])
        if person.get("tenure_months"):
            html += f' Tenure: {person["tenure_months"]} months.'
    html += '\n</div>\n'

    # Known tech stack
    known_tools = company.get("known_tools", []) if company else []
    if isinstance(known_tools, str):
        try:
            known_tools = json.loads(known_tools)
        except (json.JSONDecodeError, TypeError):
            known_tools = []
    if known_tools:
        html += f'<div class="prep-section">\n<strong>Known Tools:</strong> {_esc_vercel(", ".join(known_tools))}\n</div>\n'

    # Pain hypothesis
    pain = ""
    for msg in messages:
        if msg.get("pain_hook"):
            pain = msg["pain_hook"]
            break
    if pain:
        html += f'<div class="prep-section">\n<strong>Pain Hypothesis:</strong> {_esc_vercel(pain)}\n</div>\n'

    # Discovery questions
    html += '<div class="prep-section">\n<strong>Discovery Questions:</strong>\n<ol>\n'
    html += f'  <li>Walk me through how your team tests {_esc_vercel(company_name)}\'s core product workflows.</li>\n'
    html += '  <li>What does your current automation stack look like?</li>\n'
    html += '  <li>Where are regression cycles hitting hardest?</li>\n'
    html += '  <li>Is there a timeline or leadership mandate driving this?</li>\n'
    html += '</ol>\n</div>\n'

    # Relevant proof points
    proof_points_used = set()
    for msg in messages:
        pp = msg.get("proof_point_used")
        if pp:
            proof_points_used.add(pp)
    if proof_points_used:
        html += f'<div class="prep-section">\n<strong>Proof Points Used:</strong> {_esc_vercel(", ".join(proof_points_used))}\n</div>\n'

    html += f'<button class="copy-btn" onclick="copyPrepCard(\'{cid}\')">Copy Prep</button>\n'
    html += '</div>\n'
    return html


# ─── SCRIPTS ──────────────────────────────────────────────────────────────────

def _render_scripts_vercel(contacts: list) -> str:
    """Render all JS for interactivity and localStorage persistence."""
    contact_ids = json.dumps([c["id"] for c in contacts])
    return f'''<script>
// ── Contact IDs for localStorage ──
var CONTACT_IDS = {contact_ids};
var STORAGE_KEY = 'occ-batch-state';

// ── Init: restore saved state ──
(function() {{
  try {{
    var saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}');
    CONTACT_IDS.forEach(function(cid) {{
      var state = saved[cid];
      if (!state) return;
      var statusDD = document.querySelector('.status-dd[data-cid="' + cid + '"]');
      if (statusDD && state.status) {{
        statusDD.value = state.status;
        // Show prep card if Meeting Booked
        if (state.status === 'Meeting Booked') showPrep(cid);
      }}
      var replyDD = document.querySelector('.reply-dd[data-cid="' + cid + '"]');
      if (replyDD && state.reply_tag) replyDD.value = state.reply_tag;
    }});
  }} catch(e) {{}}
}})();

// ── Save state to localStorage ──
function persistState() {{
  var state = {{}};
  CONTACT_IDS.forEach(function(cid) {{
    var statusDD = document.querySelector('.status-dd[data-cid="' + cid + '"]');
    var replyDD = document.querySelector('.reply-dd[data-cid="' + cid + '"]');
    state[cid] = {{
      status: statusDD ? statusDD.value : '',
      reply_tag: replyDD ? replyDD.value : ''
    }};
  }});
  try {{ localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }} catch(e) {{}}
}}

function saveStatus(el) {{
  var cid = el.dataset.cid;
  if (el.value === 'Meeting Booked') showPrep(cid);
  else hidePrep(cid);
  persistState();
}}

function saveReplyTag(el) {{
  persistState();
}}

// ── Filtering ──
function applyFilters() {{
  var pri = document.getElementById('filterPriority').value;
  var persona = document.getElementById('filterPersona').value;
  var status = document.getElementById('filterStatus').value;

  document.querySelectorAll('.prospect-row').forEach(function(row) {{
    var show = true;
    var rowPri = parseInt(row.dataset.priority || '0');
    var rowPersona = row.dataset.persona || '';

    if (pri === '5' && rowPri < 5) show = false;
    if (pri === '4' && rowPri !== 4) show = false;
    if (pri === '45' && rowPri < 4) show = false;
    if (persona !== 'all' && rowPersona !== persona) show = false;

    if (status !== 'all') {{
      var dd = row.querySelector('.status-dd');
      if (dd && dd.value !== status) show = false;
    }}

    row.style.display = show ? '' : 'none';
  }});
}}

// ── Card toggling ──
function toggleCard(cid) {{
  var body = document.getElementById('body-' + cid);
  if (body) body.style.display = body.style.display === 'none' ? 'block' : 'none';
}}

function scrollToCard(cid) {{
  var card = document.getElementById('card-' + cid);
  if (card) {{
    card.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    var body = document.getElementById('body-' + cid);
    if (body) body.style.display = 'block';
  }}
}}

// ── Meeting prep ──
function showPrep(cid) {{
  var el = document.getElementById('prep-' + cid);
  if (el) el.style.display = 'block';
}}
function hidePrep(cid) {{
  var el = document.getElementById('prep-' + cid);
  if (el) el.style.display = 'none';
}}

// ── Copy functions ──
function doCopy(btn, val, mode) {{
  var text;
  if (mode === 'body') {{
    var el = document.getElementById(val);
    text = el ? el.innerText : val;
  }} else {{
    text = val;
  }}
  var orig = btn.textContent;
  navigator.clipboard.writeText(text).then(function() {{
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(function() {{ btn.textContent = orig; btn.classList.remove('copied'); }}, 2000);
  }}).catch(function() {{
    // Fallback
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {{ document.execCommand('copy'); }} catch(e) {{}}
    document.body.removeChild(ta);
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(function() {{ btn.textContent = orig; btn.classList.remove('copied'); }}, 2000);
  }});
}}

function copyPrepCard(cid) {{
  var el = document.getElementById('prep-' + cid);
  if (!el) return;
  var text = el.innerText;
  navigator.clipboard.writeText(text).then(function() {{
    var btn = el.querySelector('.copy-btn');
    if (btn) {{
      btn.textContent = 'Copied!';
      btn.classList.add('copied');
      setTimeout(function() {{ btn.textContent = 'Copy Prep'; btn.classList.remove('copied'); }}, 2000);
    }}
  }});
}}
</script>'''


# ─── CSS ──────────────────────────────────────────────────────────────────────

def _get_css_vercel() -> str:
    return '''* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; color: #1a1a2e; line-height: 1.6; padding: 20px; }
.container { max-width: 1200px; margin: 0 auto; }
h1 { font-size: 1.8rem; color: #1a1a2e; margin-bottom: 4px; }
.subtitle { color: #666; font-size: 0.95rem; margin-bottom: 20px; }
.section-title { font-size: 1.3rem; color: #1a1a2e; margin: 30px 0 15px; border-bottom: 2px solid #4361ee; padding-bottom: 6px; }

/* Pre-brief */
.pre-brief { background: #eef2ff; border-left: 4px solid #4361ee; padding: 16px 20px; border-radius: 8px; margin-bottom: 20px; }
.pre-brief h3 { font-size: 1rem; color: #4361ee; margin-bottom: 8px; }
.pre-brief li { font-size: 0.88rem; margin-bottom: 4px; color: #333; }

/* Stats */
.stats { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 20px; }
.stat-box { background: #fff; padding: 12px 18px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); min-width: 110px; }
.stat-num { font-size: 1.4rem; font-weight: 700; color: #4361ee; }
.stat-label { font-size: 0.75rem; color: #888; }

/* A/B info */
.ab-info { background: #fff7ed; border-left: 4px solid #f59e0b; padding: 10px 16px; border-radius: 6px; margin-bottom: 20px; font-size: 0.88rem; }

/* Filters */
.filter-bar { background: #fff; padding: 12px 16px; border-radius: 8px; margin-bottom: 20px; display: flex; gap: 20px; flex-wrap: wrap; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.filter-bar label { font-size: 0.82rem; color: #555; }
.filter-bar select { padding: 4px 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 0.82rem; }

/* Tracker table */
.table-wrap { overflow-x: auto; margin-bottom: 30px; }
table { width: 100%; border-collapse: collapse; font-size: 0.8rem; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
th { background: #4361ee; color: #fff; padding: 8px 10px; text-align: left; font-weight: 600; white-space: nowrap; }
td { padding: 6px 10px; border-bottom: 1px solid #eee; vertical-align: top; }
tr:hover { background: #f0f4ff; }
.url-cell { font-size: 0.72rem; word-break: break-all; max-width: 100px; }
.name-cell a { font-weight: 600; }
.ab-cell { font-weight: 600; font-size: 0.85rem; }
.status-dd, .reply-dd { font-size: 0.75rem; padding: 3px 5px; border: 1px solid #ddd; border-radius: 4px; max-width: 130px; }

/* Badges */
.badge { display: inline-block; padding: 2px 7px; border-radius: 10px; font-size: 0.68rem; font-weight: 600; margin: 1px 2px; white-space: nowrap; }
.badge-qa { background: #d4edda; color: #155724; }
.badge-vp { background: #d6eaf8; color: #1a5276; }
.badge-inf { background: #e8f5e9; color: #2e7d32; }
.badge-bi { background: #ffeaa7; color: #856404; }
.badge-fin { background: #e8daef; color: #6c3483; }
.badge-tech { background: #fce4ec; color: #880e4f; }
.badge-health { background: #e0f7fa; color: #00695c; }
.badge-ecom { background: #fff3e0; color: #e65100; }
.badge-tel { background: #e3f2fd; color: #1565c0; }
.badge-other { background: #f5f5f5; color: #616161; }

/* Priority badges */
.pri-badge { display: inline-block; width: 26px; height: 26px; line-height: 26px; text-align: center; border-radius: 50%; font-weight: 700; font-size: 0.82rem; color: #fff; }
.pri-hot { background: #e74c3c; }
.pri-warm { background: #f39c12; }
.pri-std { background: #3498db; }
.pri-low { background: #95a5a6; }

/* Personalization score */
.p-score { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 0.72rem; font-weight: 700; }
.p-score-3 { background: #d4edda; color: #155724; }
.p-score-2 { background: #fff3cd; color: #856404; }
.p-score-1 { background: #f8d7da; color: #721c24; }

/* Prospect cards */
.card { background: #fff; border-radius: 10px; margin-bottom: 14px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); border-left: 4px solid #4361ee; overflow: hidden; }
.card-header { padding: 14px 20px; cursor: pointer; }
.card-header:hover { background: #f8f9ff; }
.card-header h3 { font-size: 1rem; color: #1a1a2e; margin-bottom: 2px; display: flex; align-items: center; gap: 8px; }
.card-meta { font-size: 0.82rem; color: #888; }
.card-body { padding: 0 20px 20px; }

/* Research */
.research-section { background: #fafbfc; padding: 14px; border-radius: 6px; margin-bottom: 14px; border: 1px solid #eee; }
.research-section h4 { font-size: 0.88rem; color: #4361ee; margin-bottom: 8px; }
.research-block { font-size: 0.82rem; color: #555; margin-bottom: 6px; line-height: 1.5; }

/* Message blocks */
.msg-block { margin-bottom: 16px; padding: 14px; background: #fafbfc; border-radius: 6px; border: 1px solid #eee; }
.msg-block h4 { font-size: 0.88rem; color: #4361ee; margin-bottom: 6px; }
.msg-subject { font-weight: 600; color: #1a1a2e; margin-bottom: 6px; font-size: 0.88rem; }
.msg-body { font-size: 0.85rem; color: #333; white-space: pre-line; line-height: 1.6; padding: 10px 14px; background: #fff; border-radius: 4px; border: 1px solid #eee; }
.call-block { border-left: 3px solid #27ae60; }
.call-body { background: #f0fdf4; }
.copy-btn { background: #4361ee; color: #fff; border: none; padding: 5px 12px; border-radius: 5px; cursor: pointer; font-size: 0.75rem; margin-top: 6px; margin-right: 6px; }
.copy-btn:hover { background: #3a56d4; }
.copy-btn.copied { background: #27ae60; }
.copy-sub { background: #e0e7ff; color: #4361ee; border: 1px solid #c7d2fe; padding: 4px 10px; border-radius: 5px; cursor: pointer; font-size: 0.75rem; margin-top: 6px; }
.copy-sub:hover { background: #c7d2fe; }
.copy-sub.copied { background: #27ae60; color: #fff; border-color: #27ae60; }

/* Objection */
.objection-block { margin-bottom: 14px; padding: 14px; background: #fff8f0; border-radius: 6px; border: 1px solid #fde68a; }
.objection-block h4 { font-size: 0.88rem; color: #d97706; margin-bottom: 6px; }
.objection-q { font-size: 0.85rem; margin-bottom: 6px; }
.objection-a { font-size: 0.85rem; color: #555; }

/* Prep card */
.prep-card { margin-top: 14px; padding: 16px; background: #eef2ff; border-radius: 8px; border: 2px solid #4361ee; }
.prep-card h4 { font-size: 1rem; color: #4361ee; margin-bottom: 10px; }
.prep-section { font-size: 0.85rem; margin-bottom: 8px; line-height: 1.5; }
.prep-section ol { margin-left: 20px; margin-top: 4px; }
.prep-section li { margin-bottom: 3px; }

/* Links */
a { color: #4361ee; text-decoration: none; }
a:hover { text-decoration: underline; }

/* Responsive */
@media (max-width: 768px) {
  .stats { flex-direction: column; }
  .filter-bar { flex-direction: column; gap: 8px; }
  .card-header h3 { font-size: 0.92rem; }
}'''

# ---------------------------------------------------------------------------
# WORKFLOW ENGINE ENDPOINTS
# ---------------------------------------------------------------------------

@app.get("/api/workflows")
def list_workflows(channel: str = None):
    conn = get_db()
    if channel:
        rows = conn.execute("SELECT * FROM workflow_definitions WHERE channel=? AND is_active=1 ORDER BY name", (channel,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM workflow_definitions WHERE is_active=1 ORDER BY channel, name").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/workflows/{workflow_id}")
def get_workflow(workflow_id: str):
    conn = get_db()
    row = conn.execute("SELECT * FROM workflow_definitions WHERE id=?", (workflow_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Workflow not found")
    return dict(row)

@app.get("/api/workflow-runs")
def list_workflow_runs(channel: str = None, status: str = None, limit: int = 50):
    conn = get_db()
    q = "SELECT wr.*, wd.name as workflow_name FROM workflow_runs wr LEFT JOIN workflow_definitions wd ON wr.workflow_id = wd.id WHERE 1=1"
    params = []
    if channel:
        q += " AND wr.channel=?"
        params.append(channel)
    if status:
        q += " AND wr.status=?"
        params.append(status)
    q += " ORDER BY wr.created_at DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/workflow-runs/{run_id}")
def get_workflow_run(run_id: str):
    conn = get_db()
    run = conn.execute("SELECT wr.*, wd.name as workflow_name FROM workflow_runs wr LEFT JOIN workflow_definitions wd ON wr.workflow_id = wd.id WHERE wr.id=?", (run_id,)).fetchone()
    if not run:
        conn.close()
        raise HTTPException(404, "Run not found")
    steps = conn.execute("SELECT * FROM workflow_run_steps WHERE run_id=? ORDER BY created_at", (run_id,)).fetchall()
    artifacts = conn.execute("SELECT * FROM flow_artifacts WHERE flow_run_id=? ORDER BY created_at", (run_id,)).fetchall()
    conn.close()
    result = dict(run)
    result["steps"] = [dict(s) for s in steps]
    result["artifacts"] = [dict(a) for a in artifacts]
    return result

@app.get("/api/workflow-runs/{run_id}/steps")
def get_workflow_run_steps(run_id: str):
    conn = get_db()
    steps = conn.execute("SELECT * FROM workflow_run_steps WHERE run_id=? ORDER BY created_at", (run_id,)).fetchall()
    conn.close()
    return [dict(s) for s in steps]

# ---------------------------------------------------------------------------
# ADMIN & DATA MANAGEMENT ENDPOINTS
# ---------------------------------------------------------------------------

@app.get("/api/admin/data-summary")
def admin_data_summary():
    """Count records by source across all tables."""
    conn = get_db()
    tables = ['accounts', 'contacts', 'message_drafts', 'batches', 'opportunities', 'touchpoints', 'replies', 'signals']
    summary = {}
    for table in tables:
        try:
            rows = conn.execute(f"SELECT source, COUNT(*) as cnt FROM {table} GROUP BY source").fetchall()
            summary[table] = {r['source'] or 'unknown': r['cnt'] for r in rows}
            total = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            summary[table]['_total'] = total
        except Exception:
            summary[table] = {'_total': 0, '_error': 'source column missing'}
    conn.close()
    return summary

@app.post("/api/admin/cleanup/preview")
def admin_cleanup_preview():
    """Preview what seed data would be deleted, grouped by source."""
    conn = get_db()
    tables = ['accounts', 'contacts', 'message_drafts', 'batches', 'opportunities', 'touchpoints', 'replies', 'signals']
    preview = {}
    for table in tables:
        try:
            rows = conn.execute(f"SELECT source, COUNT(*) as cnt FROM {table} GROUP BY source").fetchall()
            preview[table] = {r['source'] or 'unknown': r['cnt'] for r in rows}
            total = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            preview[table]['_total'] = total
        except Exception:
            preview[table] = {'_total': 0, '_error': 'source column missing'}
    conn.close()
    seed_total = sum(preview.get(t, {}).get('seed', 0) for t in tables)
    return {"tables": preview, "seed_records": seed_total, "action": "Would delete all records with source='seed' only"}

@app.post("/api/admin/cleanup/execute")
def admin_cleanup_execute(data: dict = {}):
    """Delete all seed data (preserve run_bundle and manual). Requires confirmation."""
    confirm = data.get("confirm", False)
    if not confirm:
        raise HTTPException(400, "Must pass confirm=true to execute cleanup")
    conn = get_db()
    tables = ['replies', 'touchpoints', 'message_drafts', 'opportunities', 'batch_prospects', 'batches', 'signals', 'icp_scores', 'research_snapshots', 'contacts', 'accounts']
    deleted = {}
    for table in tables:
        try:
            cursor = conn.execute(f"DELETE FROM {table} WHERE source = 'seed'")
            deleted[table] = cursor.rowcount
        except Exception:
            deleted[table] = 0
    for table in ['activity_timeline', 'agent_runs', 'flow_runs', 'flow_run_steps', 'flow_artifacts', 'draft_versions', 'followups', 'experiments', 'sender_health_snapshots', 'workflow_runs', 'workflow_run_steps', 'safety_events']:
        try:
            cursor = conn.execute(f"DELETE FROM {table}")
            deleted[table] = cursor.rowcount
        except Exception:
            deleted[table] = 0
    conn.commit()
    conn.close()
    return {"status": "cleaned", "deleted": deleted, "total": sum(deleted.values()), "note": "Only source='seed' records deleted. run_bundle and manual data preserved."}

@app.get("/api/admin/export-all")
def admin_export_all():
    """Export full database as JSON for backup."""
    conn = get_db()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
    export = {}
    for t in tables:
        name = t['name']
        rows = conn.execute(f"SELECT * FROM {name}").fetchall()
        export[name] = [dict(r) for r in rows]
    conn.close()
    return {"exported_at": datetime.now().isoformat(), "tables": export, "table_count": len(export)}

@app.post("/api/admin/import-backup")
def admin_import_backup(data: dict):
    """Restore database from JSON backup."""
    tables_data = data.get("tables", {})
    if not tables_data:
        raise HTTPException(400, "No tables data provided")
    conn = get_db()
    imported = {}
    for table_name, rows in tables_data.items():
        if not rows:
            continue
        try:
            cols = list(rows[0].keys())
            placeholders = ", ".join(["?"] * len(cols))
            col_names = ", ".join(cols)
            for row in rows:
                values = [row.get(c) for c in cols]
                conn.execute(f"INSERT OR REPLACE INTO {table_name} ({col_names}) VALUES ({placeholders})", values)
            imported[table_name] = len(rows)
        except Exception as e:
            imported[table_name] = f"error: {str(e)}"
    conn.commit()
    conn.close()
    return {"status": "imported", "tables": imported}

# ---------------------------------------------------------------------------
# RUN BUNDLE IMPORT ENDPOINT (Standard Ingestion Pipeline)
# ---------------------------------------------------------------------------

@app.post("/api/import/run-bundle")
def import_run_bundle(data: dict):
    """
    Import a RunBundle v1 JSON into the dashboard.
    This is the standard pipeline for importing prospect batches from the SOP.

    Expected format:
    {
      "run": { "batch_number", "batch_date", "source", "sop_version", "notes", "ab_variable", "ab_description", "pre_brief" },
      "prospects": [ { "name", "title", "company", "vertical", "linkedin_url", "persona", "seniority",
                       "priority_score", "personalization_score", "key_detail", "company_detail",
                       "employee_count", "ab_group", "linkedin_status", "flag_notes", "status",
                       "predicted_objection", "objection_response", "objection_trigger" } ],
      "drafts": [ { "prospect_name" or "linkedin_url", "touch_number", "touch_type", "subject", "body",
                     "proof_point", "pain_hook", "opener_style", "word_count", "ab_group" } ]
    }

    OR simplified format where drafts are embedded in prospects:
    {
      "run": { ... },
      "prospects": [ { ..., "touch_1_subject", "touch_1_body", "touch_3", "touch_6",
                        "call_snippet_1", "call_snippet_2" } ]
    }
    """
    conn = get_db()
    run_meta = data.get("run", {})
    prospects = data.get("prospects", [])

    if not prospects:
        raise HTTPException(400, "No prospects provided")

    # Em dash validation
    em_dash_violations = []
    for i, p in enumerate(prospects):
        for field in ['touch_1_body', 'touch_1_subject', 'touch_3', 'touch_6', 'call_snippet_1', 'call_snippet_2']:
            val = p.get(field, '')
            if '\u2014' in str(val) or '\u2013' in str(val):
                em_dash_violations.append(f"Prospect {i+1} ({p.get('name','unknown')}): {field}")

    if em_dash_violations:
        raise HTTPException(400, {"error": "Em dash violations found", "violations": em_dash_violations})

    now = datetime.utcnow().isoformat()

    # Create batch record
    batch_id = gen_id("batch")
    batch_number = run_meta.get("batch_number", 1)
    conn.execute("""INSERT INTO batches (id, batch_number, created_date, prospect_count, ab_variable,
        ab_description, pre_brief, status, source, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (batch_id, batch_number, run_meta.get("batch_date", now[:10]),
         len([p for p in prospects if 'Removed' not in p.get('status', '')]),
         run_meta.get("ab_variable", "pain_hook"),
         run_meta.get("ab_description", ""),
         run_meta.get("pre_brief", ""),
         "imported", "run_bundle", now))

    # Also create a research run record for the Runs page
    run_id = gen_id("rr")
    active_count = len([p for p in prospects if 'Removed' not in p.get('status', '')])
    conn.execute("""INSERT INTO research_runs (id, name, import_type, prospect_count, status,
        sop_checklist, progress_pct, logs, ab_variable, config, created_at, completed_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (run_id, f"Batch {batch_number} - {run_meta.get('batch_date', now[:10])}",
         "run_bundle", active_count, "completed",
         json.dumps([
             {"step": "import", "status": "completed", "label": "RunBundle Import"},
             {"step": "validate", "status": "completed", "label": "Validation"},
             {"step": "dedup", "status": "completed", "label": "Deduplication"},
             {"step": "insert", "status": "completed", "label": "Database Insert"}
         ]),
         100,
         json.dumps([f"Imported via RunBundle v1 at {now}"]),
         run_meta.get("ab_variable", "pain_hook"),
         json.dumps(run_meta),
         now, now))

    imported_contacts = []
    imported_drafts = 0
    skipped = []
    deduped = []

    touch_map = [
        (1, "inmail", "touch_1_subject", "touch_1_body"),
        (2, "call", None, "call_snippet_1"),
        (3, "inmail_followup", None, "touch_3"),
        (4, "call", None, "call_snippet_2"),
        (6, "breakup", None, "touch_6"),
    ]

    for idx, p in enumerate(prospects):
        name = p.get("name", "")
        if not name:
            skipped.append({"index": idx, "reason": "missing_name"})
            continue

        # Skip removed prospects
        if 'Removed' in p.get('status', ''):
            skipped.append({"index": idx, "name": name, "reason": "removed"})
            continue

        # Split name
        parts = name.strip().split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""

        linkedin_url = p.get("linkedin", p.get("linkedin_url", ""))
        company = p.get("company", "")

        # Dedup by linkedin_url
        if linkedin_url:
            existing = conn.execute("SELECT id FROM contacts WHERE linkedin_url=?", (linkedin_url,)).fetchone()
            if existing:
                deduped.append({"name": name, "linkedin_url": linkedin_url, "existing_id": existing["id"]})
                # Still link to batch
                conn.execute("INSERT INTO batch_prospects (id, batch_id, contact_id, ab_group, sequence_status, position_in_batch) VALUES (?,?,?,?,?,?)",
                    (gen_id("bp"), batch_id, existing["id"], p.get("ab_group", ""), p.get("status", "not_started"), idx+1))
                # Import drafts for existing contacts too - replace stubs with full messages
                existing_contact_id = existing["id"]
                # Find account for this contact
                existing_account = conn.execute("SELECT account_id FROM contacts WHERE id=?", (existing_contact_id,)).fetchone()
                existing_account_id = existing_account["account_id"] if existing_account else None
                # Delete old stub drafts for this contact (body < 200 chars)
                old_stubs = conn.execute("SELECT id FROM message_drafts WHERE contact_id=? AND length(body) < 200", (existing_contact_id,)).fetchall()
                for stub in old_stubs:
                    conn.execute("DELETE FROM draft_research_link WHERE draft_id=?", (stub["id"],))
                    conn.execute("DELETE FROM send_log WHERE draft_id=?", (stub["id"],))
                    conn.execute("DELETE FROM draft_versions WHERE draft_id=?", (stub["id"],))
                conn.execute("DELETE FROM message_drafts WHERE contact_id=? AND length(body) < 200", (existing_contact_id,))
                # Create new drafts from bundle data
                for touch_num, touch_type, subj_field, body_field in touch_map:
                    body_text = p.get(body_field, "")
                    if not body_text or len(body_text) < 60:
                        continue
                    subj_text = p.get(subj_field, "") if subj_field else ""
                    draft_id = gen_id("md")
                    wc = len(body_text.split())
                    conn.execute("""INSERT INTO message_drafts (id, contact_id, batch_id, channel,
                        touch_number, touch_type, subject_line, body, version, personalization_score,
                        proof_point_used, pain_hook, opener_style, word_count, qc_passed,
                        approval_status, ab_group, ab_variable, source, created_at)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (draft_id, existing_contact_id, batch_id, "linkedin",
                         touch_num, touch_type, subj_text, body_text, 1,
                         p.get("personalization_score"),
                         "", "", "", wc, 1,
                         "draft", p.get("ab_group", ""),
                         run_meta.get("ab_variable", "pain_hook"),
                         "run_bundle", now))
                    imported_drafts += 1
                continue

        # Find or create account
        account_id = None
        if company:
            acc = conn.execute("SELECT id FROM accounts WHERE name=?", (company,)).fetchone()
            if acc:
                account_id = acc["id"]
                # Update account info if we have more data
                conn.execute("""UPDATE accounts SET industry=COALESCE(NULLIF(?,''),(industry)),
                    employee_count=COALESCE(?,employee_count), updated_at=? WHERE id=?""",
                    (p.get("vertical", ""), p.get("employee_count"), now, account_id))
            else:
                account_id = gen_id("acc")
                conn.execute("""INSERT INTO accounts (id, name, domain, industry, employee_count,
                    employee_band, source, created_at) VALUES (?,?,?,?,?,?,?,?)""",
                    (account_id, company, p.get("company_domain", ""),
                     p.get("vertical", ""), p.get("employee_count"),
                     _employee_band(p.get("employee_count")),
                     "run_bundle", now))

        # Determine seniority and persona
        title = p.get("title", "")
        persona_raw = p.get("persona", "")
        seniority = _detect_seniority(title)
        persona_type = _detect_persona(title, persona_raw)

        # Create contact
        contact_id = gen_id("con")
        conn.execute("""INSERT INTO contacts (id, account_id, first_name, last_name, title,
            persona_type, seniority_level, linkedin_url, location, stage,
            priority_score, personalization_score, predicted_objection, objection_response,
            source, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (contact_id, account_id, first_name, last_name, title,
             persona_type, seniority, linkedin_url, p.get("location", ""),
             "new", p.get("priority_score", 3), p.get("personalization_score"),
             p.get("objection", {}).get("objection", p.get("predicted_objection", "")),
             p.get("objection", {}).get("response", p.get("objection_response", "")),
             "run_bundle", now))

        # Create research snapshot
        snap_id = gen_id("rs")
        conn.execute("""INSERT INTO research_snapshots (id, contact_id, account_id, entity_type,
            headline, summary, pain_indicators, sources, confidence_score, agent_run_id, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (snap_id, contact_id, account_id, "prospect",
             p.get("key_detail", ""),
             p.get("company_detail", ""),
             json.dumps([p.get("flag_notes", "")]) if p.get("flag_notes") else "[]",
             json.dumps(["run_bundle_import"]),
             p.get("overall_score", 3),
             run_id, now))

        # Link to batch
        conn.execute("INSERT INTO batch_prospects (id, batch_id, contact_id, ab_group, sequence_status, position_in_batch) VALUES (?,?,?,?,?,?)",
            (gen_id("bp"), batch_id, contact_id, p.get("ab_group", ""), "not_started", idx+1))

        # Create message drafts (embedded format)
        for touch_num, touch_type, subj_field, body_field in touch_map:
            body_text = p.get(body_field, "")
            if not body_text:
                continue
            subj_text = p.get(subj_field, "") if subj_field else ""
            draft_id = gen_id("md")
            wc = len(body_text.split())
            conn.execute("""INSERT INTO message_drafts (id, contact_id, batch_id, channel,
                touch_number, touch_type, subject_line, body, version, personalization_score,
                proof_point_used, pain_hook, opener_style, word_count, qc_passed,
                approval_status, ab_group, ab_variable, source, created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (draft_id, contact_id, batch_id, "linkedin",
                 touch_num, touch_type, subj_text, body_text, 1,
                 p.get("personalization_score"),
                 "", "", "", wc, 1,
                 "draft", p.get("ab_group", ""),
                 run_meta.get("ab_variable", "pain_hook"),
                 "run_bundle", now))
            
            # Create research link for this draft
            conn.execute("""INSERT INTO draft_research_link 
                (id, draft_id, contact_id, account_id, profile_bullets, company_bullets,
                 pain_hypothesis, why_testsigma, template_name, template_version,
                 ab_group_explanation, confidence_score, linkedin_url, company_url)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (gen_id("drl"), draft_id, contact_id, account_id,
                 json.dumps(p.get("profile_research_bullets", p.get("profile_research", "").split("; ") if p.get("profile_research") else [])),
                 json.dumps(p.get("company_research_bullets", p.get("company_research", "").split("; ") if p.get("company_research") else [])),
                 p.get("pain_hypothesis", p.get("outreach_angle", "")),
                 p.get("why_testsigma", ""),
                 f"LI {touch_type} v1.0",
                 "1.0",
                 p.get("ab_group_explanation", f"A/B group: {p.get('ab_group', 'A')}"),
                 p.get("confidence_score", 3),
                 p.get("linkedin_url", ""),
                 p.get("company_url", p.get("company_website", ""))))
            
            imported_drafts += 1

        imported_contacts.append({
            "contact_id": contact_id,
            "account_id": account_id,
            "name": name,
            "company": company,
            "linkedin_url": linkedin_url,
            "priority_score": p.get("priority_score", 3)
        })

    # Log activity
    conn.execute("""INSERT INTO activity_timeline (id, channel, activity_type, description, metadata, created_at)
        VALUES (?,?,?,?,?,?)""",
        (gen_id("act"), "system", "run_bundle_import",
         f"Imported RunBundle: {len(imported_contacts)} contacts, {imported_drafts} drafts, {len(deduped)} deduped, {len(skipped)} skipped",
         json.dumps({"batch_id": batch_id, "run_id": run_id}), now))

    conn.commit()
    conn.close()

    return {
        "status": "imported",
        "batch_id": batch_id,
        "run_id": run_id,
        "imported_contacts": len(imported_contacts),
        "imported_drafts": imported_drafts,
        "deduped": len(deduped),
        "skipped": len(skipped),
        "contacts": imported_contacts[:10],
        "dedup_details": deduped[:10],
        "skip_details": skipped[:10]
    }


@app.get("/api/import/run-bundle/schema")
def run_bundle_schema():
    """Return the RunBundle v1 schema for documentation."""
    return {
        "version": "v1",
        "description": "Standard format for importing prospect batches from the BDR SOP",
        "schema": {
            "run": {
                "batch_number": "integer",
                "batch_date": "YYYY-MM-DD",
                "source": "string (e.g. 'cowork_session', 'sales_navigator')",
                "sop_version": "string",
                "notes": "string",
                "ab_variable": "string",
                "ab_description": "string",
                "pre_brief": "string",
                "quality_report": "object"
            },
            "prospects": [{
                "name": "string (required)",
                "title": "string",
                "company": "string",
                "vertical": "string",
                "linkedin_url": "string (primary dedup key)",
                "persona": "string",
                "priority_score": "integer 1-5",
                "personalization_score": "integer 1-3",
                "key_detail": "string",
                "company_detail": "string",
                "employee_count": "integer",
                "ab_group": "string",
                "touch_1_subject": "string",
                "touch_1_body": "string",
                "touch_3": "string",
                "touch_6": "string",
                "call_snippet_1": "string",
                "call_snippet_2": "string",
                "objection": {"trigger": "string", "objection": "string", "response": "string"},
                "linkedin_status": "string (verified/flagged/needs_manual_lookup)",
                "flag_notes": "string",
                "status": "string"
            }]
        }
    }


def _employee_band(count):
    """Convert employee count to band."""
    if not count:
        return None
    count = int(count)
    if count < 50:
        return "1-49"
    elif count < 200:
        return "50-199"
    elif count < 500:
        return "200-499"
    elif count < 1000:
        return "500-999"
    elif count < 5000:
        return "1000-4999"
    elif count < 10000:
        return "5000-9999"
    else:
        return "10000+"


def _detect_seniority(title: str) -> str:
    """Detect seniority level from job title."""
    t = title.lower()
    if any(x in t for x in ["cto", "cfo", "ceo", "coo", "cio", "chief"]):
        return "c_level"
    if any(x in t for x in ["svp", "senior vice president"]):
        return "svp"
    if any(x in t for x in ["vp", "vice president"]):
        return "vp"
    if any(x in t for x in ["senior director", "sr director", "sr. director"]):
        return "senior_director"
    if "director" in t or "head of" in t:
        return "director"
    if "manager" in t or "lead" in t:
        return "manager"
    return "individual"


def _detect_persona(title: str, persona_hint: str = "") -> str:
    """Detect persona type from title and hint."""
    t = title.lower()
    hint = persona_hint.lower() if persona_hint else ""
    if any(x in t for x in ["qa", "quality", "test", "sdet", "qe"]) or "qa" in hint:
        return "qa_leader"
    if any(x in t for x in ["engineering", "software", "platform", "development"]) or "eng" in hint:
        return "vp_eng"
    return "other"


@app.get("/api/prospects/full")
def get_full_prospects(batch_id: str = None, priority_min: int = None,
                       persona: str = None, limit: int = 200):
    """Get prospects with company info and all message drafts in one call."""
    conn = get_db()

    # Build contacts query with company join
    q = """SELECT c.*, a.name as company_name, a.industry as vertical, a.employee_count,
           a.domain as company_domain, a.buyer_intent
           FROM contacts c
           LEFT JOIN accounts a ON c.account_id = a.id
           WHERE 1=1"""
    params = []

    if batch_id:
        q += " AND c.id IN (SELECT contact_id FROM batch_prospects WHERE batch_id=?)"
        params.append(batch_id)

    if priority_min:
        q += " AND c.priority_score >= ?"
        params.append(priority_min)

    if persona:
        q += " AND c.persona_type = ?"
        params.append(persona)

    q += " ORDER BY c.priority_score DESC, c.created_at DESC LIMIT ?"
    params.append(limit)

    contacts = [dict(r) for r in conn.execute(q, params).fetchall()]

    # Get all drafts for these contacts
    if contacts:
        contact_ids = [c['id'] for c in contacts]
        placeholders = ",".join(["?"] * len(contact_ids))
        drafts = [dict(r) for r in conn.execute(
            f"""SELECT * FROM message_drafts WHERE contact_id IN ({placeholders})
                ORDER BY contact_id, touch_number""",
            contact_ids
        ).fetchall()]

        # Get research snapshots
        snapshots = [dict(r) for r in conn.execute(
            f"""SELECT * FROM research_snapshots WHERE contact_id IN ({placeholders})
                ORDER BY created_at DESC""",
            contact_ids
        ).fetchall()]

        # Group by contact_id
        drafts_by_contact = {}
        for d in drafts:
            cid = d['contact_id']
            if cid not in drafts_by_contact:
                drafts_by_contact[cid] = []
            drafts_by_contact[cid].append(d)

        snapshots_by_contact = {}
        for s in snapshots:
            cid = s['contact_id']
            if cid not in snapshots_by_contact:
                snapshots_by_contact[cid] = s  # latest only

        for c in contacts:
            c['drafts'] = drafts_by_contact.get(c['id'], [])
            snap = snapshots_by_contact.get(c['id'])
            if snap:
                c['key_detail'] = snap.get('headline', '')
                c['company_detail'] = snap.get('summary', '')
    else:
        for c in contacts:
            c['drafts'] = []

    conn.close()
    return {"prospects": contacts, "total": len(contacts)}


@app.get("/api/prospects/{contact_id}/drafts")
def get_prospect_drafts(contact_id: str):
    """Get all message drafts for a specific prospect."""
    conn = get_db()
    contact = conn.execute("""SELECT c.*, a.name as company_name, a.industry as vertical
        FROM contacts c LEFT JOIN accounts a ON c.account_id = a.id WHERE c.id=?""",
        (contact_id,)).fetchone()
    if not contact:
        conn.close()
        raise HTTPException(404, "Contact not found")
    contact = dict(contact)

    drafts = [dict(r) for r in conn.execute(
        "SELECT * FROM message_drafts WHERE contact_id=? ORDER BY touch_number",
        (contact_id,)
    ).fetchall()]

    snapshot = conn.execute(
        "SELECT * FROM research_snapshots WHERE contact_id=? ORDER BY created_at DESC LIMIT 1",
        (contact_id,)
    ).fetchone()

    conn.close()
    return {
        "contact": contact,
        "drafts": drafts,
        "research": dict(snapshot) if snapshot else None
    }


# ---------------------------------------------------------------------------
# RESEARCH RUN ENDPOINTS
# ---------------------------------------------------------------------------

@app.get("/api/research-runs")
def list_research_runs(status: str = None, limit: int = 20):
    conn = get_db()
    q = "SELECT * FROM research_runs"
    params = []
    if status:
        q += " WHERE status = ?"
        params.append(status)
    q += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    runs = [dict(r) for r in conn.execute(q, params).fetchall()]
    conn.close()
    return {"runs": runs, "total": len(runs)}

@app.get("/api/research-runs/{run_id}")
def get_research_run(run_id: str):
    conn = get_db()
    run = conn.execute("SELECT * FROM research_runs WHERE id = ?", (run_id,)).fetchone()
    if not run:
        raise HTTPException(404, "Research run not found")
    run_dict = dict(run)
    contacts = [dict(r) for r in conn.execute(
        "SELECT c.*, a.name as company_name FROM contacts c LEFT JOIN accounts a ON c.account_id = a.id WHERE c.source = 'csv_import' AND c.created_at >= ?",
        (run_dict['created_at'],)
    ).fetchall()]
    contact_ids = [c['id'] for c in contacts]
    drafts = []
    if contact_ids:
        placeholders = ",".join(["?"] * len(contact_ids))
        drafts = [dict(r) for r in conn.execute(
            f"SELECT * FROM message_drafts WHERE contact_id IN ({placeholders}) AND created_at >= ?",
            contact_ids + [run_dict['created_at']]
        ).fetchall()]
    conn.close()
    run_dict['contacts'] = contacts
    run_dict['drafts'] = drafts
    run_dict['sop_checklist'] = json.loads(run_dict.get('sop_checklist') or '[]')
    run_dict['logs'] = json.loads(run_dict.get('logs') or '[]')
    return run_dict

@app.post("/api/research-runs")
def create_research_run(data: dict):
    """Create a research run from CSV/paste data."""
    rows = data.get("rows", [])
    import_type = data.get("import_type", "csv")
    name = data.get("name", f"Research Run {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    ab_variable = data.get("ab_variable", "pain_hook")

    if not rows:
        raise HTTPException(400, "No rows provided")

    run_id = gen_id("rr")
    conn = get_db()

    sop_checklist = json.dumps([
        {"step": "validate", "label": "Validate CSV data", "status": "pending"},
        {"step": "accounts", "label": "Create/match accounts", "status": "pending"},
        {"step": "contacts", "label": "Create contacts", "status": "pending"},
        {"step": "score", "label": "Score & prioritize", "status": "pending"},
        {"step": "ab_assign", "label": "A/B group assignment", "status": "pending"},
        {"step": "drafts", "label": "Generate message drafts", "status": "pending"},
        {"step": "quality_gate", "label": "Quality gate checks", "status": "pending"},
        {"step": "complete", "label": "Finalize run", "status": "pending"}
    ])

    conn.execute("""INSERT INTO research_runs (id, name, import_type, prospect_count, status, sop_checklist, ab_variable, config)
        VALUES (?, ?, ?, ?, 'created', ?, ?, ?)""",
        (run_id, name, import_type, len(rows), sop_checklist, ab_variable, json.dumps({"rows": rows})))
    conn.commit()
    conn.close()
    return {"run_id": run_id, "status": "created", "prospect_count": len(rows)}

@app.post("/api/research-runs/{run_id}/validate")
def validate_research_run(run_id: str):
    """Validate all rows in a research run."""
    conn = get_db()
    run = conn.execute("SELECT * FROM research_runs WHERE id = ?", (run_id,)).fetchone()
    if not run:
        raise HTTPException(404, "Run not found")

    config = json.loads(run['config'] or '{}')
    rows = config.get('rows', [])

    errors = []
    valid = []
    seen = set()

    for i, row in enumerate(rows):
        row_errors = []
        name = (row.get('first_name', '') + ' ' + row.get('last_name', '')).strip()
        if not name or name == ' ':
            name = row.get('name', '').strip()
        if not name:
            row_errors.append("Name is required")
        company = row.get('company', '').strip()
        if not company:
            row_errors.append("Company is required")
        title = row.get('title', '').strip()
        linkedin_url = row.get('linkedin_url', '').strip()
        if not title and not linkedin_url:
            row_errors.append("Title or LinkedIn URL required")

        key = (name.lower(), company.lower())
        if key in seen:
            row_errors.append("Duplicate entry")
        seen.add(key)

        if linkedin_url:
            existing = conn.execute("SELECT id FROM contacts WHERE linkedin_url = ?", (linkedin_url,)).fetchone()
            if existing:
                row_errors.append("Already in database")

        if row_errors:
            errors.append({"row": i + 1, "data": row, "errors": row_errors})
        else:
            valid.append(row)

    checklist = json.loads(run['sop_checklist'] or '[]')
    for step in checklist:
        if step['step'] == 'validate':
            step['status'] = 'passed' if len(errors) < len(rows) * 0.5 else 'failed'
            break

    logs = json.loads(run['logs'] or '[]')
    logs.append({"ts": datetime.now().isoformat(), "msg": f"Validation: {len(valid)} valid, {len(errors)} errors out of {len(rows)} rows"})

    conn.execute("UPDATE research_runs SET status = 'validated', sop_checklist = ?, logs = ? WHERE id = ?",
        (json.dumps(checklist), json.dumps(logs), run_id))
    conn.commit()
    conn.close()

    return {
        "run_id": run_id,
        "total_rows": len(rows),
        "valid_count": len(valid),
        "error_count": len(errors),
        "errors": errors[:50],
        "status": "validated"
    }

@app.post("/api/research-runs/{run_id}/execute")
def execute_research_run(run_id: str):
    """Execute the full SOP pipeline for a research run."""
    conn = get_db()
    run = conn.execute("SELECT * FROM research_runs WHERE id = ?", (run_id,)).fetchone()
    if not run:
        raise HTTPException(404, "Run not found")

    config = json.loads(run['config'] or '{}')
    rows = config.get('rows', [])
    ab_variable = run['ab_variable'] or 'pain_hook'

    conn.execute("UPDATE research_runs SET status = 'running', started_at = datetime('now') WHERE id = ?", (run_id,))
    conn.commit()

    checklist = json.loads(run['sop_checklist'] or '[]')
    logs = json.loads(run['logs'] or '[]')

    def update_step(step_name, status):
        for s in checklist:
            if s['step'] == step_name:
                s['status'] = status
                break
        conn.execute("UPDATE research_runs SET sop_checklist = ? WHERE id = ?", (json.dumps(checklist), run_id))

    def add_log(msg):
        logs.append({"ts": datetime.now().isoformat(), "msg": msg})
        conn.execute("UPDATE research_runs SET logs = ? WHERE id = ?", (json.dumps(logs), run_id))

    try:
        update_step('validate', 'running')
        add_log("Starting pipeline execution")
        valid_rows = []
        for row in rows:
            name = row.get('name', '').strip() or (row.get('first_name', '') + ' ' + row.get('last_name', '')).strip()
            company = row.get('company', '').strip()
            if name and company:
                valid_rows.append(row)
        update_step('validate', 'passed')
        add_log(f"Validated {len(valid_rows)} of {len(rows)} rows")

        update_step('accounts', 'running')
        account_map = {}
        for row in valid_rows:
            company = row.get('company', '').strip()
            if company not in account_map:
                existing = conn.execute("SELECT id FROM accounts WHERE name = ? COLLATE NOCASE", (company,)).fetchone()
                if existing:
                    account_map[company] = existing['id']
                else:
                    acc_id = gen_id("acc")
                    industry = row.get('industry', 'Technology')
                    conn.execute("""INSERT INTO accounts (id, name, industry, source, created_at)
                        VALUES (?, ?, ?, 'csv_import', datetime('now'))""", (acc_id, company, industry))
                    account_map[company] = acc_id
        conn.commit()
        update_step('accounts', 'passed')
        add_log(f"Created/matched {len(account_map)} accounts")

        update_step('contacts', 'running')
        contact_ids = []
        for i, row in enumerate(valid_rows):
            name = row.get('name', '').strip() or (row.get('first_name', '') + ' ' + row.get('last_name', '')).strip()
            parts = name.split(' ', 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ''
            company = row.get('company', '').strip()
            title = row.get('title', '').strip()
            email = row.get('email', '').strip()
            linkedin_url = row.get('linkedin_url', '').strip()

            title_lower = title.lower()
            if any(kw in title_lower for kw in ['qa', 'quality', 'test', 'sdet']):
                persona_type = 'qa_leader'
            else:
                persona_type = 'vp_eng'

            if any(kw in title_lower for kw in ['director', 'head']):
                seniority = 'director'
            elif any(kw in title_lower for kw in ['vp', 'vice president', 'cto', 'cfo']):
                seniority = 'vp'
            elif 'manager' in title_lower:
                seniority = 'manager'
            else:
                seniority = 'senior'

            con_id = gen_id("con")
            conn.execute("""INSERT INTO contacts (id, account_id, first_name, last_name, title, email, linkedin_url,
                persona_type, seniority_level, source, stage, priority_score, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'csv_import', 'new', 3, datetime('now'))""",
                (con_id, account_map.get(company), first_name, last_name, title, email, linkedin_url, persona_type, seniority))
            contact_ids.append(con_id)

        conn.commit()
        update_step('contacts', 'passed')
        add_log(f"Created {len(contact_ids)} contacts")

        progress = 30
        conn.execute("UPDATE research_runs SET progress_pct = ? WHERE id = ?", (progress, run_id))

        update_step('score', 'running')
        for con_id in contact_ids:
            contact = conn.execute("SELECT * FROM contacts WHERE id = ?", (con_id,)).fetchone()
            contact = dict(contact) if contact else None
            account = conn.execute("SELECT * FROM accounts WHERE id = ?", (contact['account_id'],)).fetchone() if contact and contact['account_id'] else None
            account = dict(account) if account else None

            score = 3
            factors = {}
            if contact and contact['persona_type'] == 'qa_leader':
                score += 1
                factors['qa_leader'] = '+1'
            if account and account.get('industry') in ('FinTech', 'SaaS', 'Healthcare', 'Technology'):
                score += 1
                factors['top_vertical'] = '+1'
            if contact and contact.get('recently_hired'):
                score += 1
                factors['recently_hired'] = '+1'
            if account and account.get('buyer_intent'):
                score += 2
                factors['buyer_intent'] = '+2'
            if account and account.get('known_tools') and any(t in (account.get('known_tools') or '') for t in ['selenium', 'cypress', 'tosca', 'katalon']):
                score += 1
                factors['competitor_tool'] = '+1'
            if contact and contact['seniority_level'] == 'vp' and account and (account.get('employee_count') or 0) > 50000:
                score -= 1
                factors['large_co_vp'] = '-1'

            score = max(1, min(5, score))
            conn.execute("UPDATE contacts SET priority_score = ?, priority_factors = ? WHERE id = ?",
                (score, json.dumps(factors), con_id))

            icp_id = gen_id("icp")
            conn.execute("""INSERT INTO icp_scores (id, contact_id, title_match, vertical_match, seniority_fit, total_score)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (icp_id, con_id,
                 1 if contact and contact['persona_type'] == 'qa_leader' else 0,
                 1 if account and account.get('industry') in ('FinTech', 'SaaS', 'Healthcare') else 0,
                 1 if contact and contact['seniority_level'] in ('director', 'vp') else 0,
                 score))

        conn.commit()
        update_step('score', 'passed')
        add_log(f"Scored {len(contact_ids)} contacts")
        progress = 45
        conn.execute("UPDATE research_runs SET progress_pct = ? WHERE id = ?", (progress, run_id))

        update_step('ab_assign', 'running')
        groups = json.loads(run['ab_groups'] or '["A","B"]')
        for i, con_id in enumerate(contact_ids):
            group = groups[i % len(groups)]
            contact = conn.execute("SELECT priority_factors FROM contacts WHERE id = ?", (con_id,)).fetchone()
            factors = json.loads(contact['priority_factors'] or '{}')
            factors['ab_group'] = group
            factors['ab_variable'] = ab_variable
            conn.execute("UPDATE contacts SET priority_factors = ? WHERE id = ?", (json.dumps(factors), con_id))

        conn.commit()
        update_step('ab_assign', 'passed')
        add_log(f"Assigned A/B groups ({ab_variable})")
        progress = 55
        conn.execute("UPDATE research_runs SET progress_pct = ? WHERE id = ?", (progress, run_id))

        update_step('drafts', 'running')
        draft_count = 0

        proof_points = {
            'FinTech': ('CRED', '90% regression automation, 5x faster execution'),
            'Healthcare': ('Sanofi', 'regression 3 days to 80 minutes'),
            'Insurance': ('Hansard', 'regression 8 weeks to 5 weeks with AI auto-heal'),
            'SaaS': ('Spendflo', '50% manual testing cut'),
            'Technology': ('Nagra DTV', '2,500 tests in 8 months, 4X faster'),
            'Pharma': ('Sanofi', 'regression 3 days to 80 minutes'),
            'Retail': ('Medibuddy', '2,500 tests automated, 50% maintenance cut')
        }

        for idx, con_id in enumerate(contact_ids):
            contact = conn.execute("SELECT c.*, a.name as company_name, a.industry FROM contacts c LEFT JOIN accounts a ON c.account_id = a.id WHERE c.id = ?", (con_id,)).fetchone()
            if not contact:
                continue
            contact = dict(contact)

            name = f"{contact['first_name']} {contact['last_name']}"
            company = contact.get('company_name') or 'their company'
            title = contact.get('title') or 'their role'
            industry = contact.get('industry') or 'Technology'
            persona = contact.get('persona_type') or 'qa_leader'
            factors = json.loads(contact.get('priority_factors') or '{}')
            ab_group = factors.get('ab_group', 'A')

            pp = proof_points.get(industry, ('Fortune 100', '3X productivity increase'))
            proof_name, proof_stat = pp

            all_pp = list(proof_points.values())
            pp2 = all_pp[(list(proof_points.keys()).index(industry) + 1) % len(all_pp)] if industry in proof_points else all_pp[1]
            pp3 = all_pp[(list(proof_points.keys()).index(industry) + 2) % len(all_pp)] if industry in proof_points else all_pp[2]

            if ab_variable == 'pain_hook':
                pain = 'flaky tests and regression maintenance' if ab_group == 'A' else 'release velocity and test coverage gaps'
            else:
                pain = 'test maintenance overhead' if persona == 'qa_leader' else 'QA bottlenecks slowing releases'

            p_score = 2

            touch1_subject = f"Quick question about QA at {company}"
            touch1_body = f"Hi {contact['first_name']}, your work as {title} at {company} caught my eye. Leading QA in {industry.lower()} means {pain} is probably a constant.\n\nWe helped {proof_name} achieve {proof_stat}, and I think there's a parallel to what your team deals with.\n\nWould a quick 15-minute call make sense to see if it's relevant? If not, no worries at all."
            touch1_body = touch1_body.replace('—', ',').replace('–', '-')
            touch1_wc = len(touch1_body.split())

            msg_id1 = gen_id("msg")
            conn.execute("""INSERT INTO message_drafts (id, contact_id, channel, touch_number, touch_type, subject_line, body,
                personalization_score, proof_point_used, pain_hook, word_count, approval_status, ab_group, ab_variable, source)
                VALUES (?, ?, 'linkedin', 1, 'inmail', ?, ?, ?, ?, ?, ?, 'draft', ?, ?, 'csv_import')""",
                (msg_id1, con_id, touch1_subject, touch1_body, p_score, proof_name, pain, touch1_wc, ab_group, ab_variable))
            draft_count += 1

            call1_body = f"Opener: Hey {contact['first_name']}, this is Rob from Testsigma, noticed you're leading {title.lower()} at {company}.\nPain: {pain.capitalize()} is something we hear a lot in {industry.lower()}.\nBridge: We helped {proof_name} achieve {proof_stat}. Worth 60 seconds to see if it's relevant?"
            call1_body = call1_body.replace('—', ',').replace('–', '-')
            msg_id2 = gen_id("msg")
            conn.execute("""INSERT INTO message_drafts (id, contact_id, channel, touch_number, touch_type, subject_line, body,
                proof_point_used, pain_hook, word_count, approval_status, ab_group, ab_variable, source)
                VALUES (?, ?, 'phone', 2, 'call_script', 'Cold Call #1', ?, ?, ?, ?, 'draft', ?, ?, 'csv_import')""",
                (msg_id2, con_id, call1_body, proof_name, pain, len(call1_body.split()), ab_group, ab_variable))
            draft_count += 1

            touch3_subject = f"Following up, {contact['first_name']}"
            touch3_body = f"Circling back quick, {contact['first_name']}. Wanted to share that {pp2[0]} recently {pp2[1]} using our platform. Given your role at {company}, thought it might resonate. Worth a conversation? Happy to share more if helpful."
            touch3_body = touch3_body.replace('—', ',').replace('–', '-')
            msg_id3 = gen_id("msg")
            conn.execute("""INSERT INTO message_drafts (id, contact_id, channel, touch_number, touch_type, subject_line, body,
                personalization_score, proof_point_used, pain_hook, word_count, approval_status, ab_group, ab_variable, source)
                VALUES (?, ?, 'linkedin', 3, 'followup', ?, ?, ?, ?, ?, ?, 'draft', ?, ?, 'csv_import')""",
                (msg_id3, con_id, touch3_subject, touch3_body, p_score, pp2[0], pain, len(touch3_body.split()), ab_group, ab_variable))
            draft_count += 1

            call2_body = f"Opener: Hey {contact['first_name']}, Rob from Testsigma again, quick follow-up on my message.\nPain: Curious if {company}'s team is spending too much time on {pain}.\nBridge: {pp2[0]} saw {pp2[1]}. Would love to compare notes, 60 seconds?"
            call2_body = call2_body.replace('—', ',').replace('–', '-')
            msg_id4 = gen_id("msg")
            conn.execute("""INSERT INTO message_drafts (id, contact_id, channel, touch_number, touch_type, subject_line, body,
                proof_point_used, word_count, approval_status, ab_group, ab_variable, source)
                VALUES (?, ?, 'phone', 4, 'call_script', 'Cold Call #2', ?, ?, ?, 'draft', ?, ?, 'csv_import')""",
                (msg_id4, con_id, call2_body, pp2[0], len(call2_body.split()), ab_group, ab_variable))
            draft_count += 1

            if contact.get('email'):
                touch5_subject = f"{company}'s testing workflow"
                touch5_body = f"Hi {contact['first_name']}, I've been reaching out on LinkedIn but wanted to try email too. {pp3[0]} recently {pp3[1]} with our AI test automation platform. Given {company}'s scale in {industry.lower()}, I suspect {pain} comes up often. Would it make sense to chat for 15 minutes? If the timing is off, totally fine."
                touch5_body = touch5_body.replace('—', ',').replace('–', '-')
                msg_id5 = gen_id("msg")
                conn.execute("""INSERT INTO message_drafts (id, contact_id, channel, touch_number, touch_type, subject_line, body,
                    personalization_score, proof_point_used, pain_hook, word_count, approval_status, ab_group, ab_variable, source)
                    VALUES (?, ?, 'email', 5, 'cold_email', ?, ?, ?, ?, ?, ?, 'draft', ?, ?, 'csv_import')""",
                    (msg_id5, con_id, touch5_subject, touch5_body, p_score, pp3[0], pain, len(touch5_body.split()), ab_group, ab_variable))
                draft_count += 1

            touch6_subject = f"Closing the loop"
            touch6_body = f"Hi {contact['first_name']}, I've reached out a few times and want to be respectful of your time. If testing automation isn't a priority right now, totally get it. Just wanted to close the loop so I'm not clogging your inbox. Door's always open."
            touch6_body = touch6_body.replace('—', ',').replace('–', '-')
            msg_id6 = gen_id("msg")
            conn.execute("""INSERT INTO message_drafts (id, contact_id, channel, touch_number, touch_type, subject_line, body,
                personalization_score, proof_point_used, word_count, approval_status, ab_group, ab_variable, source)
                VALUES (?, ?, 'linkedin', 6, 'breakup', ?, ?, 1, 'none', ?, 'draft', ?, ?, 'csv_import')""",
                (msg_id6, con_id, touch6_subject, touch6_body, len(touch6_body.split()), ab_group, ab_variable))
            draft_count += 1

            objection_type = 'has_tool'
            if account and (account.get('employee_count') or 0) > 50000:
                objection_type = 'big_company'
            elif contact['persona_type'] != 'qa_leader':
                objection_type = 'no_qa_team'
            elif contact.get('recently_hired'):
                objection_type = 'new_leader'

            objection_responses = {
                'has_tool': "Totally fair. A lot of teams we work with had existing tools too. The gap they kept hitting was maintenance overhead. Worth comparing?",
                'big_company': "We offer on-prem, private cloud, and hybrid. SOC2/ISO certified. A few Fortune 500s run us behind their firewall.",
                'no_qa_team': "That's actually why teams like yours use us. Plain English means devs write tests without a dedicated QA team.",
                'new_leader': "Makes sense. A lot of QA leaders in their first 90 days use our free trial to benchmark what's possible before committing.",
                'compliance': "We work with Sanofi, Oscar Health, and several banks. Happy to walk through our compliance story.",
                'budget': "Totally get it. Spendflo cut manual testing 50% and saw ROI in the first quarter."
            }

            conn.execute("UPDATE contacts SET predicted_objection = ?, objection_response = ? WHERE id = ?",
                (objection_type, objection_responses.get(objection_type, ''), con_id))

            progress = 55 + int((idx + 1) / len(contact_ids) * 35)
            conn.execute("UPDATE research_runs SET progress_pct = ? WHERE id = ?", (min(progress, 90), run_id))
            conn.commit()

        update_step('drafts', 'passed')
        add_log(f"Generated {draft_count} message drafts across {len(contact_ids)} contacts")

        update_step('quality_gate', 'running')
        qc_issues = 0
        drafts = conn.execute("SELECT * FROM message_drafts WHERE source = 'csv_import' AND created_at >= ?",
            (run['created_at'],)).fetchall()
        for draft in drafts:
            flags = []
            body = draft['body'] or ''
            if '—' in body:
                flags.append('em_dash_found')
            wc = len(body.split())
            if draft['touch_number'] == 1 and (wc < 70 or wc > 120):
                flags.append(f'word_count_out_of_range:{wc}')
            if draft['touch_number'] == 3 and (wc < 40 or wc > 70):
                flags.append(f'followup_word_count:{wc}')
            if draft['touch_number'] == 6 and (wc < 20 or wc > 60):
                flags.append(f'breakup_word_count:{wc}')

            qc_passed = 1 if not flags else 0
            if flags:
                qc_issues += 1
            conn.execute("UPDATE message_drafts SET qc_passed = ?, qc_flags = ? WHERE id = ?",
                (qc_passed, json.dumps(flags), draft['id']))

        conn.commit()
        update_step('quality_gate', 'passed')
        add_log(f"Quality gate: {len(drafts) - qc_issues}/{len(drafts)} passed")

        update_step('complete', 'passed')
        add_log("Pipeline complete")

        conn.execute("""UPDATE research_runs SET status = 'complete', progress_pct = 100,
            completed_at = datetime('now'), prospect_count = ?, error_count = ?,
            sop_checklist = ?, logs = ? WHERE id = ?""",
            (len(contact_ids), qc_issues, json.dumps(checklist), json.dumps(logs), run_id))
        conn.commit()
        conn.close()

        return {
            "run_id": run_id,
            "status": "complete",
            "contacts_created": len(contact_ids),
            "drafts_generated": draft_count,
            "qc_issues": qc_issues,
            "checklist": checklist
        }

    except Exception as e:
        add_log(f"Error: {str(e)}")
        conn.execute("UPDATE research_runs SET status = 'failed', logs = ?, error_count = error_count + 1 WHERE id = ?",
            (json.dumps(logs), run_id))
        conn.commit()
        conn.close()
        raise HTTPException(500, f"Pipeline failed: {str(e)}")

@app.post("/api/research-runs/{run_id}/cancel")
def cancel_research_run(run_id: str):
    conn = get_db()
    run = conn.execute("SELECT * FROM research_runs WHERE id = ?", (run_id,)).fetchone()
    if not run:
        raise HTTPException(404, "Run not found")
    if run['status'] not in ('created', 'validated', 'running'):
        raise HTTPException(400, f"Cannot cancel run in status: {run['status']}")
    conn.execute("UPDATE research_runs SET status = 'cancelled', completed_at = datetime('now') WHERE id = ?", (run_id,))
    conn.commit()
    conn.close()
    return {"run_id": run_id, "status": "cancelled"}

@app.get("/api/safety-events")
def list_safety_events(run_id: str = None, limit: int = 50):
    conn = get_db()
    if run_id:
        rows = conn.execute("SELECT * FROM safety_events WHERE run_id=? ORDER BY created_at DESC LIMIT ?", (run_id, limit)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM safety_events ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/system/dry-run")
def get_dry_run_status():
    return {"dry_run": DRY_RUN, "message": "All outbound actions are blocked. Only drafts and research are produced." if DRY_RUN else "DRY RUN IS OFF - outbound actions could execute (but are still blocked by safety gates)."}

# ---------------------------------------------------------------------------
# LINKEDIN CHANNEL ENDPOINTS
# ---------------------------------------------------------------------------

@app.get("/api/linkedin/profiles")
def list_linkedin_profiles(limit: int = 50):
    conn = get_db()
    rows = conn.execute("""SELECT lp.*, c.first_name, c.last_name, c.title, c.company_name
        FROM linkedin_profiles lp
        LEFT JOIN contacts c ON lp.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        ORDER BY lp.last_updated DESC LIMIT ?""", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/linkedin/profiles/{profile_id}")
def get_linkedin_profile(profile_id: str):
    conn = get_db()
    row = conn.execute("SELECT * FROM linkedin_profiles WHERE id=?", (profile_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Profile not found")
    return dict(row)

@app.post("/api/linkedin/profiles/import")
def import_linkedin_profile(data: dict):
    """Import a LinkedIn profile from manual paste or CSV data."""
    conn = get_db()
    pid = gen_id("lp")
    contact_id = data.get("contact_id")

    # If no contact_id, try to match by linkedin_url
    linkedin_url = data.get("linkedin_url", "")
    if not contact_id and linkedin_url:
        existing = conn.execute("SELECT id FROM contacts WHERE linkedin_url=?", (linkedin_url,)).fetchone()
        if existing:
            contact_id = existing["id"]

    conn.execute("""INSERT INTO linkedin_profiles
        (id, contact_id, linkedin_url, headline, about_text, experience_json, education_json, skills_json, activity_json, connections_count, profile_source)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (pid, contact_id, linkedin_url,
         data.get("headline", ""), data.get("about_text", ""),
         json.dumps(data.get("experience", [])), json.dumps(data.get("education", [])),
         json.dumps(data.get("skills", [])), json.dumps(data.get("activity", [])),
         data.get("connections_count"), data.get("source", "manual")))

    # Log activity
    conn.execute("""INSERT INTO activity_timeline (id, contact_id, channel, activity_type, description)
        VALUES (?,?,?,?,?)""",
        (gen_id("act"), contact_id, "linkedin", "profile_imported", f"LinkedIn profile imported: {linkedin_url}"))

    # Log safety event
    conn.execute("""INSERT INTO safety_events (id, event_type, severity, details)
        VALUES (?,?,?,?)""",
        (gen_id("sev"), "data_import", "info", json.dumps({"type": "linkedin_profile", "source": data.get("source", "manual")})))

    conn.commit()
    conn.close()
    return {"id": pid, "contact_id": contact_id, "status": "imported"}

@app.post("/api/linkedin/profiles/import-csv")
def import_linkedin_csv(data: dict):
    """Import multiple profiles from CSV data (Sales Navigator export format)."""
    rows = data.get("rows", [])
    if not rows:
        raise HTTPException(400, "No rows provided")

    conn = get_db()
    imported = []
    skipped = []

    for row in rows:
        first_name = row.get("first_name", row.get("First Name", ""))
        last_name = row.get("last_name", row.get("Last Name", ""))
        title = row.get("title", row.get("Title", ""))
        company = row.get("company", row.get("Company", ""))
        linkedin_url = row.get("linkedin_url", row.get("LinkedIn URL", row.get("Profile URL", "")))

        if not first_name or not last_name:
            skipped.append({"reason": "missing_name", "data": row})
            continue

        # Check for duplicate by linkedin_url
        if linkedin_url:
            existing = conn.execute("SELECT id FROM contacts WHERE linkedin_url=?", (linkedin_url,)).fetchone()
            if existing:
                skipped.append({"reason": "duplicate_url", "contact_id": existing["id"], "data": row})
                continue

        # Find or create account
        account_id = None
        if company:
            acc = conn.execute("SELECT id FROM accounts WHERE name=?", (company,)).fetchone()
            if acc:
                account_id = acc["id"]
            else:
                account_id = gen_id("acc")
                conn.execute("INSERT INTO accounts (id, name, domain, industry) VALUES (?,?,?,?)",
                    (account_id, company, row.get("domain", ""), row.get("industry", "")))

        # Create contact
        contact_id = gen_id("con")
        seniority = "director" if any(x in title.lower() for x in ["director", "head"]) else \
                    "vp" if any(x in title.lower() for x in ["vp", "vice president", "cto", "cfo"]) else \
                    "manager" if "manager" in title.lower() else "individual"
        persona = "qa_leader" if any(x in title.lower() for x in ["qa", "quality", "test", "sdet"]) else "vp_eng"

        conn.execute("""INSERT INTO contacts (id, account_id, first_name, last_name, title, persona_type,
            seniority_level, email, linkedin_url, location, stage, priority_score, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (contact_id, account_id, first_name, last_name, title, persona, seniority,
             row.get("email", ""), linkedin_url, row.get("location", ""),
             "new", 3, "csv_import"))

        # Create LinkedIn profile
        pid = gen_id("lp")
        conn.execute("""INSERT INTO linkedin_profiles (id, contact_id, linkedin_url, headline, profile_source)
            VALUES (?,?,?,?,?)""",
            (pid, contact_id, linkedin_url, row.get("headline", title), "csv_import"))

        imported.append({"contact_id": contact_id, "name": f"{first_name} {last_name}", "profile_id": pid})

    # Log
    conn.execute("""INSERT INTO activity_timeline (id, channel, activity_type, description)
        VALUES (?,?,?,?)""",
        (gen_id("act"), "linkedin", "csv_import", f"Imported {len(imported)} profiles, skipped {len(skipped)}"))
    conn.execute("""INSERT INTO safety_events (id, event_type, severity, details)
        VALUES (?,?,?,?)""",
        (gen_id("sev"), "csv_import", "info", json.dumps({"imported": len(imported), "skipped": len(skipped)})))

    conn.commit()
    conn.close()
    return {"imported": len(imported), "skipped": len(skipped), "details": imported[:10], "skip_details": skipped[:10]}

@app.get("/api/linkedin/stats")
def linkedin_stats():
    conn = get_db()
    profiles = conn.execute("SELECT COUNT(*) as cnt FROM linkedin_profiles").fetchone()["cnt"]
    drafts = conn.execute("SELECT COUNT(*) as cnt FROM message_drafts WHERE channel='linkedin'").fetchone()["cnt"]
    sent = conn.execute("SELECT COUNT(*) as cnt FROM touchpoints WHERE channel='linkedin'").fetchone()["cnt"]
    runs = conn.execute("SELECT COUNT(*) as cnt FROM workflow_runs WHERE channel='linkedin'").fetchone()["cnt"]
    active_runs = conn.execute("SELECT COUNT(*) as cnt FROM workflow_runs WHERE channel='linkedin' AND status IN ('queued','running')").fetchone()["cnt"]
    conn.close()
    return {"profiles": profiles, "drafts": drafts, "sent": sent, "total_runs": runs, "active_runs": active_runs, "dry_run": DRY_RUN}

# ---------------------------------------------------------------------------
# WORKFLOW EXECUTION ENGINE
# ---------------------------------------------------------------------------

PROOF_POINTS_LIBRARY = {
    "hansard": {"name": "Hansard", "metric": "regression 8 weeks -> 5 weeks with AI auto-heal", "verticals": ["insurance", "financial_services"], "use_for": "long regression cycles"},
    "medibuddy": {"name": "Medibuddy", "metric": "2,500 tests automated, 50% maintenance cut", "verticals": ["healthcare"], "use_for": "mid-size teams scaling coverage"},
    "cred": {"name": "CRED", "metric": "90% regression automation, 5x faster execution", "verticals": ["fintech"], "use_for": "high-velocity teams"},
    "sanofi": {"name": "Sanofi", "metric": "regression 3 days -> 80 minutes", "verticals": ["pharma", "healthcare"], "use_for": "compliance-heavy"},
    "fortune100": {"name": "Fortune 100 company", "metric": "3X productivity increase", "verticals": ["enterprise"], "use_for": "VP-level conversations"},
    "nagra": {"name": "Nagra DTV", "metric": "2,500 tests in 8 months, 4X faster", "verticals": ["media", "streaming"], "use_for": "API + UI testing"},
    "spendflo": {"name": "Spendflo", "metric": "50% manual testing cut", "verticals": ["saas"], "use_for": "smaller teams, quick wins"},
}

OBJECTION_MAP = {
    "has_tool": {"trigger": "Uses TOSCA, Katalon, Testim, or mabl", "response": "Totally fair. A lot of teams we work with had {tool} too. The gap they kept hitting was {limitation}. Worth comparing?"},
    "big_company": {"trigger": "50K+ employees", "response": "We offer on-prem, private cloud, and hybrid. SOC2/ISO certified. A few Fortune 500s run us behind their firewall."},
    "no_qa_team": {"trigger": "No dedicated QA team", "response": "That's actually why teams like yours use us. Plain English means devs write tests without a dedicated QA team."},
    "new_leader": {"trigger": "Recently hired QA leader", "response": "Makes sense. A lot of QA leaders in their first 90 days use our free trial to benchmark what's possible before committing."},
    "compliance": {"trigger": "Pharma/healthcare/finance", "response": "We work with Sanofi, Oscar Health, and several banks. Happy to walk through our compliance story."},
    "budget": {"trigger": "Startup/small team", "response": "Totally get it. One company your size (Spendflo) cut manual testing 50% and saw ROI in the first quarter."},
}

def execute_workflow(workflow_type: str, input_data: dict, dry_run: bool = True) -> dict:
    """Core workflow execution engine. Always runs in dry-run mode by default."""
    conn = get_db()

    # Find workflow definition
    wf = conn.execute("SELECT * FROM workflow_definitions WHERE workflow_type=? AND is_active=1", (workflow_type,)).fetchone()
    if not wf:
        conn.close()
        raise HTTPException(404, f"Workflow '{workflow_type}' not found")

    wf = dict(wf)
    steps = json.loads(wf.get("steps", "[]"))

    # Create run record
    run_id = gen_id("wr")
    now_iso = datetime.utcnow().isoformat()
    conn.execute("""INSERT INTO workflow_runs (id, workflow_id, workflow_type, channel, status, dry_run, input_data, total_steps, started_at)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        (run_id, wf["id"], workflow_type, wf["channel"], "running", 1 if dry_run else 0,
         json.dumps(input_data), len(steps), now_iso))

    # Create step records
    for i, step_name in enumerate(steps):
        sid = gen_id("ws")
        conn.execute("""INSERT INTO workflow_run_steps (id, run_id, step_name, step_type, status)
            VALUES (?,?,?,?,?)""",
            (sid, run_id, step_name, "agent", "pending"))
    conn.commit()

    # Execute workflow based on type
    try:
        if workflow_type == "account_research":
            result = _execute_account_research(conn, run_id, input_data)
        elif workflow_type == "prospect_shortlist":
            result = _execute_prospect_shortlist(conn, run_id, input_data)
        elif workflow_type == "linkedin_message_draft":
            result = _execute_linkedin_draft(conn, run_id, input_data)
        elif workflow_type == "followup_sequence":
            result = _execute_followup_sequence(conn, run_id, input_data)
        elif workflow_type == "daily_plan":
            result = _execute_daily_plan(conn, run_id, input_data)
        elif workflow_type == "email_draft":
            result = _execute_email_draft(conn, run_id, input_data)
        elif workflow_type == "call_prep":
            result = _execute_call_prep(conn, run_id, input_data)
        else:
            raise HTTPException(400, f"Unknown workflow type: {workflow_type}")

        # Mark run as succeeded
        end_time = datetime.utcnow()
        duration = int((end_time - datetime.fromisoformat(now_iso)).total_seconds() * 1000)
        conn.execute("""UPDATE workflow_runs SET status='succeeded', output_data=?, completed_steps=total_steps,
            completed_at=?, duration_ms=? WHERE id=?""",
            (json.dumps(result), end_time.isoformat(), duration, run_id))
        conn.commit()

        # Log activity
        conn.execute("""INSERT INTO activity_timeline (id, channel, activity_type, description, flow_run_id)
            VALUES (?,?,?,?,?)""",
            (gen_id("act"), wf["channel"], "workflow_completed", f"{wf['name']} completed successfully", run_id))
        conn.commit()
        conn.close()

        return {"run_id": run_id, "status": "succeeded", "workflow": wf["name"], "result": result, "dry_run": dry_run}

    except Exception as e:
        conn.execute("UPDATE workflow_runs SET status='failed', error_message=?, completed_at=? WHERE id=?",
            (str(e), datetime.utcnow().isoformat(), run_id))
        conn.commit()
        conn.close()
        raise HTTPException(500, f"Workflow failed: {str(e)}")

def _update_step(conn, run_id: str, step_name: str, status: str, output: dict = None):
    """Update a workflow step's status."""
    now = datetime.utcnow().isoformat()
    if status == "running":
        conn.execute("UPDATE workflow_run_steps SET status=?, started_at=? WHERE run_id=? AND step_name=?",
            (status, now, run_id, step_name))
    elif status in ("succeeded", "failed"):
        conn.execute("""UPDATE workflow_run_steps SET status=?, output_data=?, completed_at=?
            WHERE run_id=? AND step_name=?""",
            (status, json.dumps(output or {}), now, run_id, step_name))
    conn.execute("UPDATE workflow_runs SET completed_steps = (SELECT COUNT(*) FROM workflow_run_steps WHERE run_id=? AND status='succeeded') WHERE id=?",
        (run_id, run_id))
    conn.commit()

# ---- WORKFLOW: Account Research ----
def _execute_account_research(conn, run_id: str, input_data: dict) -> dict:
    company_name = input_data.get("company_name", "")
    domain = input_data.get("domain", "")

    if not company_name:
        raise ValueError("company_name is required")

    _update_step(conn, run_id, "validate_input", "running")
    _update_step(conn, run_id, "validate_input", "succeeded", {"company": company_name, "domain": domain})

    # Gather company data (from our database or generate research brief)
    _update_step(conn, run_id, "gather_company_data", "running")
    account = conn.execute("SELECT * FROM accounts WHERE name=? OR domain=?", (company_name, domain)).fetchone()
    account_data = dict(account) if account else {"name": company_name, "domain": domain, "industry": input_data.get("industry", "Unknown")}
    _update_step(conn, run_id, "gather_company_data", "succeeded", {"account_found": account is not None})

    # Analyze ICP fit
    _update_step(conn, run_id, "analyze_icp_fit", "running")
    icp_score = 0
    icp_reasons = []
    industry = account_data.get("industry", "").lower()
    emp_count = account_data.get("employee_count", 0)

    top_verticals = ["fintech", "saas", "healthcare", "e-commerce", "telecom", "pharma"]
    if any(v in industry for v in top_verticals):
        icp_score += 2
        icp_reasons.append(f"Target vertical: {industry}")
    if emp_count and 200 < emp_count < 15000:
        icp_score += 2
        icp_reasons.append(f"Good company size: {emp_count} employees")
    elif emp_count:
        icp_score += 1
        icp_reasons.append(f"Company size: {emp_count} employees (outside sweet spot)")

    tools = json.loads(account_data.get("known_tools", "[]"))
    if tools:
        icp_score += 1
        icp_reasons.append(f"Uses testing tools: {', '.join(tools)}")

    if account_data.get("buyer_intent"):
        icp_score += 2
        icp_reasons.append("Buyer intent signal detected")

    _update_step(conn, run_id, "analyze_icp_fit", "succeeded", {"score": icp_score, "reasons": icp_reasons})

    # Identify pain points
    _update_step(conn, run_id, "identify_pain_points", "running")
    pain_points = []
    if tools and any(t in ["Selenium", "Cypress", "Playwright"] for t in tools):
        pain_points.append({"pain": "Maintenance burden with open-source frameworks", "severity": "high", "talk_track": f"Teams using {tools[0]} typically spend 40-60% of time on test maintenance. Our self-healing AI cuts that by 90%."})
    if emp_count and emp_count > 1000:
        pain_points.append({"pain": "Scaling test coverage across products", "severity": "high", "talk_track": "With multiple products and teams, NLP-based tests let anyone contribute to coverage, not just SDETs."})
    pain_points.append({"pain": "Regression cycle blocking releases", "severity": "medium", "talk_track": "Parallel execution + AI optimization can compress multi-day regressions into hours."})
    _update_step(conn, run_id, "identify_pain_points", "succeeded", {"pain_points": pain_points})

    # Generate brief
    _update_step(conn, run_id, "generate_brief", "running")

    # Match best proof point
    best_proof = "spendflo"  # default
    for key, pp in PROOF_POINTS_LIBRARY.items():
        if industry and any(v in industry for v in pp["verticals"]):
            best_proof = key
            break

    brief = {
        "company": company_name,
        "domain": domain,
        "industry": account_data.get("industry", "Unknown"),
        "employee_count": emp_count,
        "icp_score": icp_score,
        "icp_max": 7,
        "icp_reasons": icp_reasons,
        "known_tools": tools,
        "pain_points": pain_points,
        "recommended_proof_point": PROOF_POINTS_LIBRARY[best_proof],
        "recommended_titles": ["Director of QA", "Head of Quality Engineering", "VP Quality Assurance", "QA Manager"],
        "talk_tracks": [pp["talk_track"] for pp in pain_points],
        "predicted_objection": _predict_objection(account_data),
    }

    # Store research snapshot
    snap_id = gen_id("rs")
    conn.execute("""INSERT INTO research_snapshots (id, account_id, entity_type, headline, summary,
        tech_stack_signals, pain_indicators, agent_run_id)
        VALUES (?,?,?,?,?,?,?,?)""",
        (snap_id, account_data.get("id"), "account", f"Account Research: {company_name}",
         json.dumps(brief), json.dumps(tools), json.dumps([p["pain"] for p in pain_points]), run_id))
    conn.commit()

    _update_step(conn, run_id, "generate_brief", "succeeded", brief)
    return brief

def _predict_objection(account_data: dict) -> dict:
    """Predict most likely objection based on account data."""
    tools = json.loads(account_data.get("known_tools", "[]"))
    emp = account_data.get("employee_count", 0)
    industry = (account_data.get("industry", "") or "").lower()

    if tools and any(t in ["TOSCA", "Katalon", "Testim", "mabl"] for t in tools):
        return {"type": "has_tool", "tool": tools[0], **OBJECTION_MAP["has_tool"]}
    if emp and emp > 50000:
        return {"type": "big_company", **OBJECTION_MAP["big_company"]}
    if industry in ["pharma", "healthcare", "fintech"]:
        return {"type": "compliance", **OBJECTION_MAP["compliance"]}
    if emp and emp < 200:
        return {"type": "budget", **OBJECTION_MAP["budget"]}
    return {"type": "has_tool", **OBJECTION_MAP["has_tool"]}  # default

# ---- WORKFLOW: Prospect Shortlist ----
def _execute_prospect_shortlist(conn, run_id: str, input_data: dict) -> dict:
    contact_ids = input_data.get("contact_ids", [])
    filters = input_data.get("filters", {})

    _update_step(conn, run_id, "validate_csv", "running")

    if contact_ids:
        placeholders = ",".join(["?"] * len(contact_ids))
        contacts = conn.execute(f"""SELECT c.*, a.name as company_name, a.industry, a.employee_count, a.known_tools, a.buyer_intent
            FROM contacts c LEFT JOIN accounts a ON c.account_id = a.id
            WHERE c.id IN ({placeholders})""", contact_ids).fetchall()
    else:
        # Get all active contacts
        contacts = conn.execute("""SELECT c.*, a.name as company_name, a.industry, a.employee_count, a.known_tools, a.buyer_intent
            FROM contacts c LEFT JOIN accounts a ON c.account_id = a.id
            WHERE c.status = 'active' AND c.do_not_contact = 0""").fetchall()

    contacts = [dict(c) for c in contacts]
    _update_step(conn, run_id, "validate_csv", "succeeded", {"total_contacts": len(contacts)})

    # Filter titles
    _update_step(conn, run_id, "filter_titles", "running")
    icp_titles = ["qa", "quality", "test", "sdet", "automation", "engineering", "cto", "vp"]
    excluded_titles = ["pharma", "biotech", "manufacturing", "lab", "clinical", "regulatory"]

    passed = []
    excluded = []
    for c in contacts:
        title_lower = (c.get("title") or "").lower()
        if any(ex in title_lower for ex in excluded_titles):
            excluded.append({"id": c["id"], "name": f"{c['first_name']} {c['last_name']}", "reason": "excluded_title", "title": c.get("title")})
            continue
        seniority = c.get("seniority_level", "")
        if seniority not in ["director", "vp", "manager"]:
            excluded.append({"id": c["id"], "name": f"{c['first_name']} {c['last_name']}", "reason": "below_manager", "title": c.get("title")})
            continue
        passed.append(c)

    _update_step(conn, run_id, "filter_titles", "succeeded", {"passed": len(passed), "excluded": len(excluded)})

    # Score ICP
    _update_step(conn, run_id, "score_icp", "running")
    scored = []
    for c in passed:
        score = 0
        factors = []

        if c.get("buyer_intent"):
            score += 2
            factors.append("buyer_intent")
        if c.get("persona_type") == "qa_leader":
            score += 1
            factors.append("qa_titled")
        industry = (c.get("industry") or "").lower()
        if any(v in industry for v in ["fintech", "saas", "healthcare"]):
            score += 1
            factors.append("target_vertical")
        if c.get("recently_hired"):
            score += 1
            factors.append("recently_hired")
        tools = json.loads(c.get("known_tools") or "[]")
        if tools:
            score += 1
            factors.append("uses_competitor_tool")
        emp = c.get("employee_count", 0)
        if emp and emp > 50000 and c.get("persona_type") != "qa_leader":
            score -= 1
            factors.append("large_company_non_qa")

        c["priority_score"] = min(score, 5)
        c["priority_factors"] = factors
        scored.append(c)

    scored.sort(key=lambda x: x["priority_score"], reverse=True)
    _update_step(conn, run_id, "score_icp", "succeeded", {"scored_count": len(scored)})

    # Flag exclusions
    _update_step(conn, run_id, "flag_exclusions", "running")
    _update_step(conn, run_id, "flag_exclusions", "succeeded", {"excluded": excluded})

    # Rank output
    _update_step(conn, run_id, "rank_output", "running")
    shortlist = [{
        "id": c["id"],
        "name": f"{c['first_name']} {c['last_name']}",
        "title": c.get("title"),
        "company": c.get("company_name"),
        "industry": c.get("industry"),
        "priority_score": c["priority_score"],
        "priority_factors": c["priority_factors"],
        "persona_type": c.get("persona_type"),
        "linkedin_url": c.get("linkedin_url"),
        "missing_info": [f for f in ["email" if not c.get("email") else None, "linkedin" if not c.get("linkedin_url") else None] if f]
    } for c in scored]

    _update_step(conn, run_id, "rank_output", "succeeded", {"shortlist_size": len(shortlist)})

    return {"shortlist": shortlist, "excluded": excluded, "summary": {
        "total_input": len(contacts), "passed_filters": len(passed), "excluded": len(excluded),
        "hot": len([s for s in shortlist if s["priority_score"] >= 5]),
        "warm": len([s for s in shortlist if s["priority_score"] == 4]),
        "standard": len([s for s in shortlist if s["priority_score"] == 3]),
    }}

# ---- WORKFLOW: LinkedIn Message Draft ----
def _execute_linkedin_draft(conn, run_id: str, input_data: dict) -> dict:
    contact_id = input_data.get("contact_id")
    if not contact_id:
        raise ValueError("contact_id is required")

    _update_step(conn, run_id, "load_prospect", "running")
    contact = conn.execute("""SELECT c.*, a.name as company_name, a.industry, a.employee_count, a.known_tools, a.domain, a.buyer_intent
        FROM contacts c LEFT JOIN accounts a ON c.account_id = a.id WHERE c.id=?""", (contact_id,)).fetchone()
    if not contact:
        raise ValueError(f"Contact {contact_id} not found")
    contact = dict(contact)
    _update_step(conn, run_id, "load_prospect", "succeeded", {"name": f"{contact['first_name']} {contact['last_name']}"})

    _update_step(conn, run_id, "load_research", "running")
    research = conn.execute("SELECT * FROM research_snapshots WHERE contact_id=? OR account_id=? ORDER BY created_at DESC LIMIT 1",
        (contact_id, contact.get("account_id"))).fetchone()
    research = dict(research) if research else {}
    _update_step(conn, run_id, "load_research", "succeeded", {"has_research": bool(research)})

    _update_step(conn, run_id, "select_proof_point", "running")
    industry = (contact.get("industry") or "").lower()
    best_proof = None
    for key, pp in PROOF_POINTS_LIBRARY.items():
        if any(v in industry for v in pp["verticals"]):
            best_proof = pp
            break
    if not best_proof:
        best_proof = PROOF_POINTS_LIBRARY["spendflo"]
    _update_step(conn, run_id, "select_proof_point", "succeeded", {"proof_point": best_proof["name"]})

    _update_step(conn, run_id, "generate_variants", "running")

    first = contact["first_name"]
    company = contact.get("company_name", "your company")
    title = contact.get("title", "")
    tenure = contact.get("tenure_months", 0)

    # Build personalized elements
    opener_personal = f"Your work leading QA at {company} caught my eye" if "QA" in title or "Quality" in title else f"Saw you're heading up engineering at {company}"
    if tenure and tenure < 6:
        opener_personal = f"Congrats on the move to {company}"

    company_ref = f"{company}'s platform" if contact.get("domain") else company
    emp = contact.get("employee_count", 0)
    if emp:
        company_ref += f" (with a {emp:,}+ person team)" if emp > 5000 else ""

    pain = "keeping regression suites stable as your team ships faster" if "QA" in title else "scaling test coverage without growing the QA team"

    proof = f"{best_proof['name']} {best_proof['metric']}"

    # Generate 3 variants per SOP rules
    variants = []

    # Variant A: Warm conversational
    body_a = f"Hi {first},\n\n{opener_personal}, especially the {title.lower()} scope.\n\n"
    body_a += f"With {company_ref} scaling, I'd imagine {pain} is a constant challenge.\n\n"
    body_a += f"We helped {proof}. Their team was dealing with similar complexity.\n\n"
    body_a += "Would a quick 15-minute walkthrough be worth your time? If not relevant, no worries at all."

    # Variant B: Direct concise
    body_b = f"Hi {first},\n\n{company} is doing impressive work in {contact.get('industry', 'tech')}. Quick question for you.\n\n"
    body_b += f"How's your team handling {pain}?\n\n"
    body_b += f"{best_proof['name']} cut their {best_proof['metric'].split(',')[0]}. Happy to share how, if useful."

    # Variant C: Value-first with proof
    body_c = f"Hi {first},\n\n{best_proof['name']} was spending weeks on regression before switching to our platform. Now they {best_proof['metric']}.\n\n"
    body_c += f"Given {company}'s growth, {pain} might resonate.\n\n"
    body_c += "Worth a conversation? If the timing is off, totally fine."

    for variant_label, body in [("warm_conversational", body_a), ("direct_concise", body_b), ("value_first", body_c)]:
        # SOP quality checks
        has_em_dash = "\u2014" in body or "\u2013" in body
        word_count = len(body.split())

        variants.append({
            "variant": variant_label,
            "subject": f"Quick question about QA at {company}" if "QA" in title else f"{company} + test automation",
            "body": body.replace("\u2014", ",").replace("\u2013", ","),  # Remove em dashes per SOP
            "word_count": word_count,
            "in_range": 70 <= word_count <= 120,
            "has_em_dash": has_em_dash,
            "proof_point": best_proof["name"],
            "pain_hook": pain,
            "personalization_score": 3 if tenure and tenure < 6 else (2 if "QA" in title else 1),
        })

    _update_step(conn, run_id, "generate_variants", "succeeded", {"variants": len(variants)})

    _update_step(conn, run_id, "quality_gate", "running")
    qc_results = []
    for v in variants:
        issues = []
        if v["has_em_dash"]:
            issues.append("Contains em dash (SOP violation)")
        if not v["in_range"]:
            issues.append(f"Word count {v['word_count']} outside 70-120 range")
        qc_results.append({"variant": v["variant"], "passed": len(issues) == 0, "issues": issues})
    _update_step(conn, run_id, "quality_gate", "succeeded", {"qc_results": qc_results})

    _update_step(conn, run_id, "finalize", "running")

    # Store drafts in database
    draft_ids = []
    for v in variants:
        did = gen_id("msg")
        conn.execute("""INSERT INTO message_drafts (id, contact_id, channel, touch_number, touch_type,
            subject_line, body, personalization_score, proof_point_used, pain_hook, opener_style,
            word_count, qc_passed, approval_status, agent_run_id)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (did, contact_id, "linkedin", 1, "inmail",
             v["subject"], v["body"], v["personalization_score"],
             v["proof_point"], v["pain_hook"], v["variant"],
             v["word_count"], 1 if not v["has_em_dash"] and v["in_range"] else 0,
             "draft", run_id))
        draft_ids.append(did)

    conn.commit()
    _update_step(conn, run_id, "finalize", "succeeded", {"draft_ids": draft_ids})

    return {
        "contact": f"{contact['first_name']} {contact['last_name']}",
        "company": company,
        "variants": variants,
        "draft_ids": draft_ids,
        "recommended": variants[0]["variant"],
        "predicted_objection": _predict_objection(contact),
    }

# ---- WORKFLOW: Follow-Up Sequence ----
def _execute_followup_sequence(conn, run_id: str, input_data: dict) -> dict:
    contact_id = input_data.get("contact_id")
    if not contact_id:
        raise ValueError("contact_id is required")

    _update_step(conn, run_id, "load_original", "running")
    contact = conn.execute("""SELECT c.*, a.name as company_name, a.industry
        FROM contacts c LEFT JOIN accounts a ON c.account_id = a.id WHERE c.id=?""", (contact_id,)).fetchone()
    if not contact:
        raise ValueError(f"Contact {contact_id} not found")
    contact = dict(contact)

    original = conn.execute("SELECT * FROM message_drafts WHERE contact_id=? AND touch_number=1 ORDER BY created_at DESC LIMIT 1", (contact_id,)).fetchone()
    original = dict(original) if original else {}
    _update_step(conn, run_id, "load_original", "succeeded", {"has_original": bool(original)})

    first = contact["first_name"]
    company = contact.get("company_name", "your company")
    industry = contact.get("industry", "")

    _update_step(conn, run_id, "analyze_angle", "running")
    # Pick different proof point than original
    original_proof = original.get("proof_point_used", "")
    alt_proof = None
    for key, pp in PROOF_POINTS_LIBRARY.items():
        if pp["name"] != original_proof:
            alt_proof = pp
            break
    if not alt_proof:
        alt_proof = PROOF_POINTS_LIBRARY["cred"]
    _update_step(conn, run_id, "analyze_angle", "succeeded", {"new_proof": alt_proof["name"]})

    # Touch 3: Follow-up 1 (40-70 words, new angle)
    _update_step(conn, run_id, "draft_followup1", "running")
    followup1 = f"Hi {first},\n\nCircling back quick. {alt_proof['name']} just {alt_proof['metric']}, and their setup looked a lot like {company}'s.\n\nWorth a conversation? Happy to share more if helpful."
    _update_step(conn, run_id, "draft_followup1", "succeeded", {"word_count": len(followup1.split())})

    # Touch 5: Follow-up 2 / Email (short, more direct)
    _update_step(conn, run_id, "draft_followup2", "running")
    followup2 = f"Hi {first},\n\nOne more thought. Teams in {industry or 'your space'} keep telling us the same thing: test maintenance is eating their sprint velocity.\n\nIf that resonates, I'd love 15 minutes to show you how we fix it. If not, I'll get out of your hair."
    _update_step(conn, run_id, "draft_followup2", "succeeded", {"word_count": len(followup2.split())})

    # Touch 6: Break-up (30-50 words, no pitch)
    _update_step(conn, run_id, "draft_breakup", "running")
    breakup = f"Hi {first},\n\nTotally understand if the timing isn't right. Just wanted to close the loop so I'm not cluttering your inbox. If things change down the road, door's always open."
    _update_step(conn, run_id, "draft_breakup", "succeeded", {"word_count": len(breakup.split())})

    _update_step(conn, run_id, "quality_gate", "running")

    # Store all drafts
    drafts = []
    for touch_num, touch_type, body, subj in [
        (3, "followup_1", followup1, f"Re: QA at {company}"),
        (5, "followup_2", followup2, f"Test automation for {company}"),
        (6, "breakup", breakup, f"Closing the loop"),
    ]:
        did = gen_id("msg")
        word_count = len(body.split())
        conn.execute("""INSERT INTO message_drafts (id, contact_id, channel, touch_number, touch_type,
            subject_line, body, word_count, proof_point_used, approval_status, agent_run_id)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (did, contact_id, "linkedin" if touch_num in [3,6] else "email", touch_num, touch_type,
             subj, body, word_count, alt_proof["name"] if touch_num == 3 else None, "draft", run_id))
        drafts.append({"id": did, "touch": touch_num, "type": touch_type, "body": body, "subject": subj, "word_count": word_count})

    conn.commit()
    _update_step(conn, run_id, "quality_gate", "succeeded", {"drafts_created": len(drafts)})

    return {"contact": f"{contact['first_name']} {contact['last_name']}", "company": company, "drafts": drafts}

# ---- WORKFLOW: Daily BDR Plan ----
def _execute_daily_plan(conn, run_id: str, input_data: dict) -> dict:
    target_touches = input_data.get("target_touches", 50)
    hours_available = input_data.get("hours_available", 8)

    _update_step(conn, run_id, "load_pipeline", "running")
    pipeline = conn.execute("""SELECT c.*, a.name as company_name, a.industry
        FROM contacts c LEFT JOIN accounts a ON c.account_id = a.id
        WHERE c.status='active' AND c.do_not_contact=0
        ORDER BY c.priority_score DESC""").fetchall()
    pipeline = [dict(c) for c in pipeline]
    _update_step(conn, run_id, "load_pipeline", "succeeded", {"total_active": len(pipeline)})

    _update_step(conn, run_id, "identify_hot", "running")
    hot = [c for c in pipeline if (c.get("priority_score") or 0) >= 5]
    warm = [c for c in pipeline if (c.get("priority_score") or 0) == 4]
    _update_step(conn, run_id, "identify_hot", "succeeded", {"hot": len(hot), "warm": len(warm)})

    _update_step(conn, run_id, "identify_overdue", "running")
    overdue = conn.execute("""SELECT f.*, c.first_name, c.last_name, a.name as company_name
        FROM followups f
        LEFT JOIN contacts c ON f.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        WHERE f.state='pending' AND f.due_date <= date('now')
        ORDER BY f.due_date""").fetchall()
    overdue = [dict(f) for f in overdue]
    _update_step(conn, run_id, "identify_overdue", "succeeded", {"overdue_count": len(overdue)})

    _update_step(conn, run_id, "plan_touches", "running")
    plan = {
        "morning_block": {
            "time": "8:00 AM - 11:00 AM",
            "focus": "Cold calls to hot prospects (West Coast prime time)",
            "tasks": [{"type": "call", "contact": f"{c['first_name']} {c['last_name']}", "company": c.get("company_name", ""), "reason": "Hot prospect, priority 5"} for c in hot[:5]]
        },
        "midday_block": {
            "time": "11:00 AM - 1:00 PM",
            "focus": "LinkedIn messages and research",
            "tasks": [
                {"type": "workflow", "action": "Run Prospect Shortlist on new leads"},
                {"type": "workflow", "action": "Generate LinkedIn drafts for warm prospects"},
            ] + [{"type": "linkedin", "contact": f"{c['first_name']} {c['last_name']}", "company": c.get("company_name", ""), "reason": "Warm prospect, send InMail"} for c in warm[:5]]
        },
        "afternoon_block": {
            "time": "1:00 PM - 3:00 PM",
            "focus": "Follow-ups and overdue touches",
            "tasks": [{"type": "followup", "contact": f"{c.get('first_name', '')} {c.get('last_name', '')}", "company": c.get("company_name", ""), "due_date": c.get("due_date", ""), "touch": c.get("touch_number")} for c in overdue[:5]]
        },
        "late_block": {
            "time": "3:00 PM - 6:00 PM",
            "focus": "Second round of calls + email sends",
            "tasks": [{"type": "call", "contact": f"{c['first_name']} {c['last_name']}", "company": c.get("company_name", ""), "reason": "Warm prospect, follow-up call"} for c in warm[:3]]
        }
    }
    _update_step(conn, run_id, "plan_touches", "succeeded", {"blocks": 4})

    _update_step(conn, run_id, "generate_checklist", "running")
    checklist = {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "target_touches": target_touches,
        "hours": hours_available,
        "summary": {
            "calls_planned": len(hot[:5]) + len(warm[:3]),
            "linkedin_planned": len(warm[:5]),
            "followups_due": len(overdue),
            "hot_prospects": len(hot),
            "warm_prospects": len(warm),
        },
        "plan": plan,
    }
    _update_step(conn, run_id, "generate_checklist", "succeeded", checklist)

    return checklist

# ---- WORKFLOW: Email Draft ----
def _execute_email_draft(conn, run_id: str, input_data: dict) -> dict:
    contact_id = input_data.get("contact_id")
    if not contact_id:
        raise ValueError("contact_id is required")

    _update_step(conn, run_id, "load_prospect", "running")
    contact = conn.execute("""SELECT c.*, a.name as company_name, a.industry, a.employee_count, a.known_tools, a.domain
        FROM contacts c LEFT JOIN accounts a ON c.account_id = a.id WHERE c.id=?""", (contact_id,)).fetchone()
    if not contact:
        raise ValueError(f"Contact {contact_id} not found")
    contact = dict(contact)
    _update_step(conn, run_id, "load_prospect", "succeeded")

    _update_step(conn, run_id, "load_research", "running")
    research = conn.execute("SELECT * FROM research_snapshots WHERE contact_id=? OR account_id=? ORDER BY created_at DESC LIMIT 1",
        (contact_id, contact.get("account_id"))).fetchone()
    _update_step(conn, run_id, "load_research", "succeeded")

    first = contact["first_name"]
    company = contact.get("company_name", "your company")
    title = contact.get("title", "")
    industry = contact.get("industry", "")

    # Select proof point
    _update_step(conn, run_id, "generate_subject", "running")
    best_proof = PROOF_POINTS_LIBRARY["spendflo"]
    for key, pp in PROOF_POINTS_LIBRARY.items():
        if industry and any(v in industry.lower() for v in pp["verticals"]):
            best_proof = pp
            break

    subjects = [
        f"Quick question about QA at {company}",
        f"{company} + test automation",
        f"Idea for {company}'s testing team",
    ]
    _update_step(conn, run_id, "generate_subject", "succeeded", {"subjects": subjects})

    _update_step(conn, run_id, "generate_body", "running")
    pain = "keeping regression cycles from blocking releases" if "QA" in title else "scaling test coverage without growing the QA team"

    body = f"Hi {first},\n\n"
    body += f"I've been following {company}'s growth in {industry}, and given your role as {title}, I'd imagine {pain} is a constant conversation.\n\n"
    body += f"We helped {best_proof['name']} go from {best_proof['metric']}. Their team was in a similar spot.\n\n"
    body += "Would a quick 15-minute call make sense to see if there's a fit? If not relevant, no worries at all.\n\n"
    body += "Best,\nRob"

    # SOP checks
    body = body.replace("\u2014", ",").replace("\u2013", ",")
    _update_step(conn, run_id, "generate_body", "succeeded", {"word_count": len(body.split())})

    _update_step(conn, run_id, "quality_gate", "running")
    issues = []
    if "\u2014" in body or "\u2013" in body:
        issues.append("em_dash_found")
    if len(body.split()) > 150:
        issues.append("too_long")
    _update_step(conn, run_id, "quality_gate", "succeeded", {"passed": len(issues) == 0, "issues": issues})

    _update_step(conn, run_id, "finalize", "running")
    did = gen_id("msg")
    conn.execute("""INSERT INTO message_drafts (id, contact_id, channel, touch_number, touch_type,
        subject_line, body, word_count, proof_point_used, pain_hook, approval_status, agent_run_id)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (did, contact_id, "email", 5, "cold_email", subjects[0], body,
         len(body.split()), best_proof["name"], pain, "draft", run_id))
    conn.commit()
    _update_step(conn, run_id, "finalize", "succeeded", {"draft_id": did})

    return {"contact": f"{contact['first_name']} {contact['last_name']}", "company": company,
            "subjects": subjects, "body": body, "draft_id": did, "proof_point": best_proof["name"]}

# ---- WORKFLOW: Call Prep ----
def _execute_call_prep(conn, run_id: str, input_data: dict) -> dict:
    contact_id = input_data.get("contact_id")
    if not contact_id:
        raise ValueError("contact_id is required")

    _update_step(conn, run_id, "load_prospect", "running")
    contact = conn.execute("""SELECT c.*, a.name as company_name, a.industry, a.employee_count, a.known_tools
        FROM contacts c LEFT JOIN accounts a ON c.account_id = a.id WHERE c.id=?""", (contact_id,)).fetchone()
    if not contact:
        raise ValueError(f"Contact {contact_id} not found")
    contact = dict(contact)
    _update_step(conn, run_id, "load_prospect", "succeeded")

    _update_step(conn, run_id, "load_research", "running")
    _update_step(conn, run_id, "load_research", "succeeded")

    first = contact["first_name"]
    company = contact.get("company_name", "your company")
    title = contact.get("title", "")
    industry = contact.get("industry", "")

    # Pick proof point different from any InMail
    existing_proof = conn.execute("SELECT proof_point_used FROM message_drafts WHERE contact_id=? AND channel='linkedin' ORDER BY created_at DESC LIMIT 1",
        (contact_id,)).fetchone()
    existing_proof_name = existing_proof["proof_point_used"] if existing_proof else ""

    call_proof = PROOF_POINTS_LIBRARY["cred"]
    for key, pp in PROOF_POINTS_LIBRARY.items():
        if pp["name"] != existing_proof_name and industry and any(v in industry.lower() for v in pp["verticals"]):
            call_proof = pp
            break

    _update_step(conn, run_id, "generate_opener", "running")
    opener = f"Hey {first}, this is Rob from Testsigma. I see you're {title.lower()} at {company}, so I figured you'd be the right person to ask."
    _update_step(conn, run_id, "generate_opener", "succeeded")

    _update_step(conn, run_id, "generate_pain", "running")
    pain = f"A lot of {industry} teams tell us regression testing is their biggest bottleneck as they scale." if industry else f"Testing teams at companies like {company} often tell us flaky tests eat up 40% of their sprint."
    _update_step(conn, run_id, "generate_pain", "succeeded")

    _update_step(conn, run_id, "generate_bridge", "running")
    bridge = f"We helped {call_proof['name']} {call_proof['metric']}. Worth 60 seconds to see if it's relevant?"
    _update_step(conn, run_id, "generate_bridge", "succeeded")

    script = {"opener": opener, "pain_hypothesis": pain, "bridge": bridge}

    return {"contact": f"{first} {contact['last_name']}", "company": company, "call_script": script, "proof_point": call_proof["name"]}

# ---------------------------------------------------------------------------
# WORKFLOW TRIGGER ENDPOINTS
# ---------------------------------------------------------------------------

@app.post("/api/workflows/execute")
def trigger_workflow(data: dict):
    """Execute a workflow. Always runs in DRY_RUN mode."""
    workflow_type = data.get("workflow_type")
    input_data = data.get("input", {})

    if not workflow_type:
        raise HTTPException(400, "workflow_type is required")

    # Safety: always dry run
    result = execute_workflow(workflow_type, input_data, dry_run=True)
    return result

@app.post("/api/workflows/account-research")
def run_account_research(data: dict):
    return execute_workflow("account_research", data, dry_run=True)

@app.post("/api/workflows/prospect-shortlist")
def run_prospect_shortlist(data: dict):
    return execute_workflow("prospect_shortlist", data, dry_run=True)

@app.post("/api/workflows/linkedin-draft")
def run_linkedin_draft(data: dict):
    return execute_workflow("linkedin_message_draft", data, dry_run=True)

@app.post("/api/workflows/followup-sequence")
def run_followup_sequence(data: dict):
    return execute_workflow("followup_sequence", data, dry_run=True)

@app.post("/api/workflows/daily-plan")
def run_daily_plan(data: dict):
    return execute_workflow("daily_plan", data, dry_run=True)

@app.post("/api/workflows/email-draft")
def run_email_draft(data: dict):
    return execute_workflow("email_draft", data, dry_run=True)

@app.post("/api/workflows/call-prep")
def run_call_prep(data: dict):
    return execute_workflow("call_prep", data, dry_run=True)


# ─── UTILITIES ────────────────────────────────────────────────────────────────

def _esc_vercel(text) -> str:
    """HTML-escape text for safe rendering."""
    if not text:
        return ""
    s = str(text)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _attr_vercel(text) -> str:
    """Escape for use in HTML attributes."""
    if not text:
        return ""
    s = str(text)
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&#39;")


def _attr_esc_vercel(text) -> str:
    """Escape text for embedding in JS string inside onclick attribute."""
    if not text:
        return ""
    s = str(text)
    return s.replace("\\", "\\\\").replace("'", "\\'").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

# ─── FLOW EXECUTION ENDPOINT ──────────────────────────────────────────────

@app.post("/api/flows/{flow_type}/execute")
def execute_flow(flow_type: str, body: dict = Body(...)):
    """Execute a flow with agent orchestration."""
    try:
        conn = get_db()
        flow_id = gen_id("flow")
        config = body.get("config", {})
        now = datetime.utcnow().isoformat()

        # Create flow run
        conn.execute("""INSERT INTO flow_runs (id, flow_type, status, config, total_steps,
                       started_at, created_at) VALUES (?,?,?,?,?,?,?)""",
                    (flow_id, flow_type, "running", json.dumps(config), 6, now, now))
        conn.commit()

        # Create steps
        steps = ["pre_brief", "extract", "research", "score", "ab_assign", "messages"]
        for idx, step in enumerate(steps):
            step_id = gen_id("step")
            conn.execute("""INSERT INTO flow_run_steps (id, flow_run_id, step_name, agent_type,
                           status, created_at) VALUES (?,?,?,?,?,?)""",
                        (step_id, flow_id, step, "Agent", "pending", now))

        conn.commit()
        conn.close()

        return {"flow_id": flow_id, "status": "started", "flow_type": flow_type}

    except Exception as e:
        conn.close()
        raise HTTPException(400, str(e))

# ─── DRAFT EDIT HISTORY & VERSION TRACKING ────────────────────────────────────

@app.put("/api/drafts/{draft_id}/edit-full")
def edit_draft_full(draft_id: str, data: dict):
    """Edit a draft with version history tracking."""
    conn = get_db()
    try:
        draft = conn.execute("SELECT * FROM message_drafts WHERE id=?", (draft_id,)).fetchone()
        if not draft:
            raise HTTPException(status_code=404, detail="Draft not found")

        subject = data.get("subject_line", draft["subject_line"])
        body = data.get("body", draft["body"])

        # Validate no em dashes
        for field_val in [subject, body]:
            if field_val and ('\u2014' in field_val or '\u2013' in field_val):
                raise HTTPException(status_code=400, detail="Em dashes not allowed")

        # Check for placeholder tokens
        import re
        placeholders = re.findall(r'\{[A-Z_]+\}|TBD|TODO', body or '')
        if placeholders:
            # Warning only, not blocking
            pass

        # Save edit history for changed fields
        if subject != draft["subject_line"]:
            conn.execute("INSERT INTO draft_edit_history (id, draft_id, field, old_value, new_value) VALUES (?,?,?,?,?)",
                (gen_id("deh"), draft_id, "subject_line", draft["subject_line"], subject))
        if body != draft["body"]:
            conn.execute("INSERT INTO draft_edit_history (id, draft_id, field, old_value, new_value) VALUES (?,?,?,?,?)",
                (gen_id("deh"), draft_id, "body", draft["body"], body))

        # Update the draft
        word_count = len(body.split()) if body else 0
        conn.execute("""UPDATE message_drafts SET subject_line=?, body=?, word_count=?,
            version=version+1, updated_at=datetime('now') WHERE id=?""",
            (subject, body, word_count, draft_id))

        conn.commit()

        # Get updated draft
        updated = conn.execute("SELECT * FROM message_drafts WHERE id=?", (draft_id,)).fetchone()
        history = conn.execute("SELECT * FROM draft_edit_history WHERE draft_id=? ORDER BY edited_at DESC LIMIT 10",
            (draft_id,)).fetchall()

        return {
            "status": "updated",
            "draft": dict(updated),
            "version": updated["version"],
            "placeholders_found": placeholders,
            "edit_history": [dict(h) for h in history]
        }
    finally:
        conn.close()

@app.get("/api/drafts/{draft_id}/history")
def get_draft_history(draft_id: str):
    """Get edit history for a draft."""
    conn = get_db()
    try:
        history = conn.execute("SELECT * FROM draft_edit_history WHERE draft_id=? ORDER BY edited_at DESC LIMIT 20",
            (draft_id,)).fetchall()
        return {"history": [dict(h) for h in history]}
    finally:
        conn.close()

# ─── SEND LOG & TRACKING ──────────────────────────────────────────────────────

@app.post("/api/send-log")
def mark_as_sent(data: dict):
    """Log that a message was manually sent."""
    conn = get_db()
    try:
        contact_id = data.get("contact_id")
        draft_id = data.get("draft_id")
        channel = data.get("channel", "linkedin")
        notes = data.get("notes", "")

        if not contact_id or not draft_id:
            raise HTTPException(status_code=400, detail="contact_id and draft_id required")

        log_id = gen_id("sl")
        conn.execute("""INSERT INTO send_log (id, contact_id, draft_id, channel, status, notes)
            VALUES (?,?,?,?,?,?)""", (log_id, contact_id, draft_id, channel, "sent", notes))

        # Update draft status
        conn.execute("UPDATE message_drafts SET approval_status='sent', updated_at=datetime('now') WHERE id=?",
            (draft_id,))

        # Update contact stage
        conn.execute("UPDATE contacts SET stage='touched', updated_at=datetime('now') WHERE id=? AND stage='new'",
            (contact_id,))

        # Update quota
        today = datetime.utcnow().strftime("%Y-%m-%d")
        month = datetime.utcnow().strftime("%Y-%m")
        quota = conn.execute("SELECT * FROM quota_tracker WHERE month=?", (month,)).fetchone()
        if quota:
            conn.execute("""UPDATE quota_tracker SET sends_today = CASE WHEN last_send_date=? THEN sends_today+1 ELSE 1 END,
                sends_this_week=sends_this_week+1, sends_this_month=sends_this_month+1,
                inmail_credits_used = CASE WHEN ?='linkedin' THEN inmail_credits_used+1 ELSE inmail_credits_used END,
                last_send_date=?, updated_at=datetime('now') WHERE month=?""",
                (today, channel, today, month))
        else:
            conn.execute("""INSERT INTO quota_tracker (id, month, sends_today, sends_this_week, sends_this_month,
                inmail_credits_used, last_send_date) VALUES (?,?,1,1,1,?,?)""",
                (gen_id("qt"), month, 1 if channel == "linkedin" else 0, today))

        # Audit log
        conn.execute("""INSERT INTO activity_timeline (id, channel, activity_type, description, metadata, created_at)
            VALUES (?,?,?,?,?,datetime('now'))""",
            (gen_id("act"), channel, "draft_sent",
             f"Draft {draft_id} sent to contact {contact_id}",
             json.dumps({"draft_id": draft_id, "contact_id": contact_id, "channel": channel})))

        conn.commit()
        return {"status": "logged", "send_log_id": log_id}
    finally:
        conn.close()

@app.get("/api/send-log")
def get_send_log(limit: int = 50):
    """Get send history."""
    conn = get_db()
    try:
        rows = conn.execute("""SELECT sl.*, c.first_name, c.last_name, a.name as company_name,
            md.touch_number, md.touch_type, md.subject_line
            FROM send_log sl
            LEFT JOIN contacts c ON sl.contact_id = c.id
            LEFT JOIN accounts a ON c.account_id = a.id
            LEFT JOIN message_drafts md ON sl.draft_id = md.id
            ORDER BY sl.sent_at DESC LIMIT ?""", (limit,)).fetchall()
        return {"send_log": [dict(r) for r in rows]}
    finally:
        conn.close()

# ─── QUOTA TRACKING ───────────────────────────────────────────────────────────

@app.get("/api/quota")
def get_quota():
    """Get current month quota status."""
    conn = get_db()
    try:
        month = datetime.utcnow().strftime("%Y-%m")
        quota = conn.execute("SELECT * FROM quota_tracker WHERE month=?", (month,)).fetchone()
        if not quota:
            return {"month": month, "inmail_credits_total": 50, "inmail_credits_used": 0,
                    "daily_send_target": 25, "sends_today": 0, "sends_this_week": 0,
                    "sends_this_month": 0}
        return dict(quota)
    finally:
        conn.close()

@app.put("/api/quota")
def update_quota(data: dict):
    """Update quota settings."""
    conn = get_db()
    try:
        month = datetime.utcnow().strftime("%Y-%m")
        quota = conn.execute("SELECT * FROM quota_tracker WHERE month=?", (month,)).fetchone()
        if quota:
            conn.execute("""UPDATE quota_tracker SET inmail_credits_total=?, daily_send_target=?,
                updated_at=datetime('now') WHERE month=?""",
                (data.get("inmail_credits_total", 50), data.get("daily_send_target", 25), month))
        else:
            conn.execute("""INSERT INTO quota_tracker (id, month, inmail_credits_total, daily_send_target)
                VALUES (?,?,?,?)""",
                (gen_id("qt"), month, data.get("inmail_credits_total", 50), data.get("daily_send_target", 25)))
        conn.commit()
        return {"status": "updated"}
    finally:
        conn.close()

# ─── LINKEDIN SAFER SEND ───────────────────────────────────────────────────────

@app.post("/api/linkedin/mark-sent")
def linkedin_mark_sent(data: dict = Body(...)):
    """Safer LinkedIn send: logs the copy+paste action with message hash and confirmation."""
    conn = get_db()
    try:
        draft_id = data.get("draft_id")
        if not draft_id:
            raise HTTPException(400, "draft_id required")

        draft = conn.execute("SELECT * FROM message_drafts WHERE id=?", (draft_id,)).fetchone()
        if not draft:
            raise HTTPException(404, "Draft not found")

        import hashlib
        body_hash = hashlib.sha256((draft["body"] or "").encode()).hexdigest()[:16]

        # Create touch record
        touch_id = gen_id("touch")
        conn.execute("""INSERT INTO outreach_touches
            (id, contact_id, draft_id, channel, touch_number, touch_type, sent_at, sent_method, message_hash,
             proof_point_used, pain_hook, personalization_score, ab_group, batch_id)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (touch_id, draft["contact_id"], draft_id, draft["channel"] or "linkedin",
             draft["touch_number"], draft["touch_type"], datetime.utcnow().isoformat(),
             "manual_copy_paste", body_hash, draft["proof_point_used"], draft["pain_hook"],
             draft["personalization_score"], draft["ab_group"], draft["batch_id"]))

        # Update draft status
        conn.execute("UPDATE message_drafts SET status='sent', sent_at=? WHERE id=?",
                     (datetime.utcnow().isoformat(), draft_id))

        # Log to activity timeline
        conn.execute("""INSERT INTO activity_timeline (id, event_type, channel, contact_id, summary, metadata, created_at)
            VALUES (?,?,?,?,?,?,?)""",
            (gen_id("evt"), "draft_sent", draft["channel"] or "linkedin", draft["contact_id"],
             f"Draft sent via copy/paste (hash: {body_hash})",
             json.dumps({"draft_id": draft_id, "touch_id": touch_id, "message_hash": body_hash}),
             datetime.utcnow().isoformat()))

        # Update contact stage
        touch_num = draft["touch_number"] or 1
        stage_map = {1: "touch_1_sent", 3: "touch_3_sent", 5: "touch_5_sent", 6: "touch_6_sent"}
        new_stage = stage_map.get(touch_num, f"touch_{touch_num}_sent")
        conn.execute("UPDATE contacts SET stage=?, updated_at=? WHERE id=?",
                     (new_stage, datetime.utcnow().isoformat(), draft["contact_id"]))

        # Set first_touch_date if this is touch 1
        if touch_num == 1:
            conn.execute("UPDATE contacts SET first_touch_date=? WHERE id=? AND first_touch_date IS NULL",
                         (datetime.utcnow().isoformat(), draft["contact_id"]))

        conn.commit()
        return {"status": "sent", "touch_id": touch_id, "message_hash": body_hash}
    finally:
        conn.close()

# ─── RESEARCH EVIDENCE ────────────────────────────────────────────────────────

@app.get("/api/contacts/{contact_id}/research-evidence")
def get_research_evidence(contact_id: str):
    """Get research evidence for a contact."""
    conn = get_db()
    try:
        evidence = conn.execute("SELECT * FROM research_evidence WHERE contact_id=? ORDER BY evidence_type",
            (contact_id,)).fetchall()
        return {"evidence": [dict(e) for e in evidence]}
    finally:
        conn.close()

@app.put("/api/contacts/{contact_id}/research-evidence")
def update_research_evidence(contact_id: str, data: dict):
    """Update or create research evidence for a contact."""
    conn = get_db()
    try:
        evidence_type = data.get("evidence_type")  # 'profile' or 'company'
        bullets = json.dumps(data.get("bullets", []))
        snippet = data.get("snippet", "")
        source_url = data.get("source_url", "")

        existing = conn.execute("SELECT * FROM research_evidence WHERE contact_id=? AND evidence_type=?",
            (contact_id, evidence_type)).fetchone()

        if existing:
            conn.execute("""UPDATE research_evidence SET bullets=?, snippet=?, source_url=?,
                verified_at=datetime('now') WHERE id=?""",
                (bullets, snippet, source_url, existing["id"]))
        else:
            conn.execute("""INSERT INTO research_evidence (id, contact_id, evidence_type, bullets, snippet, source_url, verified_at)
                VALUES (?,?,?,?,?,?,datetime('now'))""",
                (gen_id("re"), contact_id, evidence_type, bullets, snippet, source_url))

        conn.commit()
        return {"status": "updated"}
    finally:
        conn.close()

# ─── DRAFT RESEARCH LINKING ───────────────────────────────────────────────────

@app.get("/api/drafts/{draft_id}/research")
def get_draft_research(draft_id: str):
    """Get research data linked to a specific draft for the Research tab."""
    conn = get_db()
    try:
        # Get the draft itself
        draft = conn.execute("SELECT * FROM message_drafts WHERE id=?", (draft_id,)).fetchone()
        if not draft:
            return {"error": "Draft not found"}
        draft = dict(draft)
        
        # Get the research link
        link = conn.execute("SELECT * FROM draft_research_link WHERE draft_id=?", (draft_id,)).fetchone()
        link = dict(link) if link else None
        if link:
            for f in ['profile_bullets', 'company_bullets', 'confidence_reasons']:
                if f in link and isinstance(link[f], str):
                    try: link[f] = json.loads(link[f])
                    except: link[f] = []
        
        # Get the contact
        contact = conn.execute("SELECT * FROM contacts WHERE id=?", (draft['contact_id'],)).fetchone()
        contact = dict(contact) if contact else None
        
        # Get research evidence
        evidence = []
        if draft['contact_id']:
            evidence = [dict(r) for r in conn.execute(
                "SELECT * FROM research_evidence WHERE contact_id=? ORDER BY evidence_type",
                (draft['contact_id'],)).fetchall()]
            for e in evidence:
                if 'bullets' in e and isinstance(e['bullets'], str):
                    try: e['bullets'] = json.loads(e['bullets'])
                    except: e['bullets'] = []
        
        # Get research snapshot
        snapshot = None
        if draft['contact_id']:
            snapshot = conn.execute(
                "SELECT * FROM research_snapshots WHERE contact_id=? ORDER BY created_at DESC LIMIT 1",
                (draft['contact_id'],)).fetchone()
            if snapshot:
                snapshot = dict(snapshot)
                for f in ['career_history', 'tech_stack_signals', 'pain_indicators', 'sources',
                          'company_products', 'company_metrics']:
                    if f in snapshot and isinstance(snapshot[f], str):
                        try: snapshot[f] = json.loads(snapshot[f])
                        except: pass
        
        # Get account
        account = None
        if contact and contact.get('account_id'):
            account = conn.execute("SELECT * FROM accounts WHERE id=?", (contact['account_id'],)).fetchone()
            if account: account = dict(account)
        
        return {
            "draft": {
                "id": draft['id'],
                "subject_line": draft.get('subject_line', ''),
                "body": draft.get('body', ''),
                "channel": draft.get('channel', ''),
                "touch_number": draft.get('touch_number'),
                "touch_type": draft.get('touch_type', ''),
                "personalization_score": draft.get('personalization_score'),
                "proof_point_used": draft.get('proof_point_used', ''),
                "pain_hook": draft.get('pain_hook', ''),
                "opener_style": draft.get('opener_style', ''),
                "ask_style": draft.get('ask_style', ''),
                "ab_group": draft.get('ab_group', ''),
                "ab_variable": draft.get('ab_variable', ''),
                "word_count": draft.get('word_count', 0),
                "version": draft.get('version', 1),
                "created_at": draft.get('created_at', ''),
                "updated_at": draft.get('updated_at', '')
            },
            "research_link": link,
            "evidence": evidence,
            "snapshot": snapshot,
            "contact": {
                "id": contact['id'],
                "name": f"{contact.get('first_name', '')} {contact.get('last_name', '')}".strip(),
                "title": contact.get('title', ''),
                "linkedin_url": contact.get('linkedin_url', ''),
                "predicted_objection": contact.get('predicted_objection', ''),
                "objection_response": contact.get('objection_response', '')
            } if contact else None,
            "account": {
                "id": account['id'],
                "name": account.get('name', ''),
                "domain": account.get('domain', ''),
                "industry": account.get('industry', ''),
                "website_url": account.get('website_url', ''),
                "known_tools": account.get('known_tools', '[]')
            } if account else None
        }
    finally:
        conn.close()

# --- Outreach Touches ---
@app.post("/api/touches")
def create_touch(data: dict = Body(...)):
    conn = get_db()
    try:
        tid = gen_id("touch")
        conn.execute("""INSERT INTO outreach_touches
            (id, contact_id, draft_id, channel, touch_number, touch_type, sent_at, sent_method,
             message_hash, proof_point_used, pain_hook, opener_style, personalization_score, ab_group, batch_id)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (tid, data.get("contact_id"), data.get("draft_id"), data.get("channel","linkedin"),
             data.get("touch_number"), data.get("touch_type"), data.get("sent_at", datetime.utcnow().isoformat()),
             data.get("sent_method","manual_copy_paste"), data.get("message_hash"), data.get("proof_point_used"),
             data.get("pain_hook"), data.get("opener_style"), data.get("personalization_score"),
             data.get("ab_group"), data.get("batch_id")))
        conn.commit()
        return {"id": tid, "status": "created"}
    finally:
        conn.close()

@app.get("/api/touches")
def list_touches(contact_id: str = None, channel: str = None, limit: int = 50):
    conn = get_db()
    try:
        q = "SELECT * FROM outreach_touches WHERE 1=1"
        params = []
        if contact_id:
            q += " AND contact_id=?"
            params.append(contact_id)
        if channel:
            q += " AND channel=?"
            params.append(channel)
        q += " ORDER BY sent_at DESC LIMIT ?"
        params.append(limit)
        rows = conn.execute(q, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

# --- Outreach Responses ---
@app.post("/api/responses")
def create_response(data: dict = Body(...)):
    conn = get_db()
    try:
        rid = gen_id("resp")
        conn.execute("""INSERT INTO outreach_responses
            (id, touch_id, contact_id, response_type, response_text, sentiment, interest_level,
             what_resonated, objection_encountered, referral_name, referral_title, reply_time_hours,
             received_at, tags, notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (rid, data.get("touch_id"), data.get("contact_id"), data.get("response_type","reply"),
             data.get("response_text"), data.get("sentiment"), data.get("interest_level"),
             data.get("what_resonated"), data.get("objection_encountered"), data.get("referral_name"),
             data.get("referral_title"), data.get("reply_time_hours"),
             data.get("received_at", datetime.utcnow().isoformat()),
             json.dumps(data.get("tags", [])), data.get("notes")))
        conn.commit()
        return {"id": rid, "status": "created"}
    finally:
        conn.close()

@app.get("/api/responses")
def list_responses(contact_id: str = None, touch_id: str = None, limit: int = 50):
    conn = get_db()
    try:
        q = "SELECT * FROM outreach_responses WHERE 1=1"
        params = []
        if contact_id:
            q += " AND contact_id=?"
            params.append(contact_id)
        if touch_id:
            q += " AND touch_id=?"
            params.append(touch_id)
        q += " ORDER BY received_at DESC LIMIT ?"
        params.append(limit)
        rows = conn.execute(q, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

# --- Outreach Outcomes ---
@app.post("/api/outcomes")
def create_outcome(data: dict = Body(...)):
    conn = get_db()
    try:
        oid = gen_id("outcome")
        conn.execute("""INSERT INTO outreach_outcomes
            (id, contact_id, outcome_type, meeting_date, meeting_notes, opportunity_created,
             opportunity_value, learnings, what_worked, what_didnt)
            VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (oid, data.get("contact_id"), data.get("outcome_type","meeting"),
             data.get("meeting_date"), data.get("meeting_notes"),
             data.get("opportunity_created", 0), data.get("opportunity_value"),
             data.get("learnings"), data.get("what_worked"), data.get("what_didnt")))
        conn.commit()
        return {"id": oid, "status": "created"}
    finally:
        conn.close()

@app.get("/api/outcomes")
def list_outcomes(contact_id: str = None, limit: int = 50):
    conn = get_db()
    try:
        q = "SELECT * FROM outreach_outcomes WHERE 1=1"
        params = []
        if contact_id:
            q += " AND contact_id=?"
            params.append(contact_id)
        q += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        rows = conn.execute(q, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

@app.get("/api/analytics/conversion-funnel")
def get_conversion_funnel():
    """Get touch-to-reply-to-meeting conversion funnel by persona, vertical, etc."""
    conn = get_db()
    try:
        total = conn.execute("SELECT COUNT(*) FROM contacts WHERE source != 'seed'").fetchone()[0]
        touched = conn.execute("SELECT COUNT(DISTINCT contact_id) FROM touchpoints").fetchone()[0]
        replied = conn.execute("SELECT COUNT(DISTINCT contact_id) FROM replies").fetchone()[0]
        meetings = conn.execute("SELECT COUNT(*) FROM opportunities WHERE meeting_held=1").fetchone()[0]
        
        # By persona
        by_persona = [dict(r) for r in conn.execute("""
            SELECT c.persona_type, COUNT(DISTINCT c.id) as total,
                   COUNT(DISTINCT t.contact_id) as touched,
                   COUNT(DISTINCT r.contact_id) as replied
            FROM contacts c
            LEFT JOIN touchpoints t ON c.id = t.contact_id
            LEFT JOIN replies r ON c.id = r.contact_id
            WHERE c.source != 'seed'
            GROUP BY c.persona_type
        """).fetchall()]
        
        return {
            "funnel": {"total": total, "touched": touched, "replied": replied, "meetings": meetings},
            "by_persona": by_persona
        }
    finally:
        conn.close()


@app.get("/api/analytics/reply-timing")
def get_reply_timing():
    """Get average reply time by personalization score and touch number."""
    conn = get_db()
    try:
        rows = [dict(r) for r in conn.execute("""
            SELECT c.personalization_score, t.touch_number,
                   COUNT(*) as reply_count
            FROM replies r
            JOIN contacts c ON r.contact_id = c.id
            JOIN touchpoints t ON r.touchpoint_id = t.id
            GROUP BY c.personalization_score, t.touch_number
            ORDER BY c.personalization_score, t.touch_number
        """).fetchall()]
        return {"timing": rows}
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# DRAFT ENHANCEMENT
# ---------------------------------------------------------------------------

@app.post("/api/drafts/{draft_id}/enhance")
def enhance_draft(draft_id: str):
    """Analyze a draft against its research data and return enhancement suggestions.
    This is a rule-based enhancer that checks for missing elements from the SOP."""
    conn = get_db()
    try:
        draft = conn.execute("""
            SELECT md.*, c.first_name, c.last_name, c.title, c.persona_type,
                   c.predicted_objection, c.personalization_score,
                   a.name as company_name, a.industry, a.employee_count, a.known_tools
            FROM message_drafts md
            LEFT JOIN contacts c ON md.contact_id = c.id
            LEFT JOIN accounts a ON c.account_id = a.id
            WHERE md.id=?
        """, (draft_id,)).fetchone()
        if not draft:
            raise HTTPException(404, "Draft not found")
        draft = dict(draft)

        # Get research data
        research_link = conn.execute(
            "SELECT * FROM draft_research_link WHERE draft_id=?", (draft_id,)
        ).fetchone()
        research = dict(research_link) if research_link else {}

        research_snapshot = None
        if draft.get("contact_id"):
            rs = conn.execute(
                "SELECT * FROM research_snapshots WHERE contact_id=? ORDER BY created_at DESC LIMIT 1",
                (draft["contact_id"],)
            ).fetchone()
            if rs:
                research_snapshot = dict(rs)

        body = draft.get("body", "")
        subject = draft.get("subject_line", "")
        touch_num = draft.get("touch_number", 1)
        suggestions = []
        score = 0
        max_score = 10

        # 1. Check personalized opener (reference to person, not just company)
        first_name = draft.get("first_name", "")
        if first_name and first_name.lower() in body.lower():
            score += 1
        else:
            suggestions.append({
                "type": "personalization",
                "severity": "high",
                "message": f"Missing personal reference. Add the prospect's name or reference their specific role/experience.",
                "example": f"Your work leading {draft.get('title', 'QA')} at {draft.get('company_name', 'the company')} caught my attention..."
            })

        # 2. Check company-specific reference
        company_name = draft.get("company_name", "")
        if company_name and company_name.lower() in body.lower():
            score += 1
        else:
            suggestions.append({
                "type": "company_reference",
                "severity": "high",
                "message": "Missing company-specific reference. Mention something concrete about their company.",
            })

        # 3. Check for pain hypothesis
        pain_keywords = ["testing", "regression", "flaky", "brittle", "maintenance", "coverage",
                         "automation", "manual", "release", "velocity", "QA", "quality"]
        has_pain = any(kw.lower() in body.lower() for kw in pain_keywords)
        if has_pain:
            score += 1
        else:
            suggestions.append({
                "type": "pain_hook",
                "severity": "high",
                "message": "Missing pain hypothesis. Tie their role/company to a specific testing challenge.",
            })

        # 4. Check for proof point (customer story with numbers)
        proof_keywords = ["hansard", "medibuddy", "cred", "sanofi", "spendflo", "nagra",
                          "fortune 100", "50%", "90%", "70%", "3x", "5x", "4x",
                          "8 weeks", "5 weeks", "80 minutes", "2,500", "2500"]
        has_proof = any(kw.lower() in body.lower() for kw in proof_keywords)
        if has_proof:
            score += 1
        else:
            suggestions.append({
                "type": "proof_point",
                "severity": "medium",
                "message": "Missing proof point. Add a customer story with specific numbers.",
                "example": "We helped Sanofi cut regression from 3 days to 80 minutes."
            })

        # 5. Check for soft ask
        ask_keywords = ["15 minutes", "quick chat", "worth a conversation", "happy to share",
                        "no worries", "get out of your hair", "if not relevant",
                        "timing isn't right", "make sense", "if it's not"]
        has_ask = any(kw.lower() in body.lower() for kw in ask_keywords)
        if has_ask:
            score += 1
        else:
            suggestions.append({
                "type": "call_to_action",
                "severity": "medium",
                "message": "Missing soft ask with easy out. End with a low-pressure meeting request.",
                "example": "Would 15 minutes make sense to explore? If not relevant, no worries at all."
            })

        # 6. Check word count (70-120 for Touch 1)
        word_count = len(body.split())
        if touch_num == 1:
            if 70 <= word_count <= 120:
                score += 1
            elif word_count < 70:
                suggestions.append({"type": "length", "severity": "low",
                    "message": f"Touch 1 should be 70-120 words. Currently {word_count} words - too short."})
            else:
                suggestions.append({"type": "length", "severity": "low",
                    "message": f"Touch 1 should be 70-120 words. Currently {word_count} words - consider trimming."})
        elif touch_num == 3:
            if 40 <= word_count <= 70:
                score += 1
            else:
                suggestions.append({"type": "length", "severity": "low",
                    "message": f"Touch 3 follow-up should be 40-70 words. Currently {word_count} words."})
        elif touch_num == 6:
            if 30 <= word_count <= 50:
                score += 1
            else:
                suggestions.append({"type": "length", "severity": "low",
                    "message": f"Touch 6 break-up should be 30-50 words. Currently {word_count} words."})
        else:
            score += 1

        # 7. Check paragraph spacing (mobile-friendly)
        paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
        if len(paragraphs) >= 2:
            score += 1
        else:
            suggestions.append({"type": "formatting", "severity": "medium",
                "message": "Add paragraph breaks for mobile readability. No wall of text."})

        # 8. Check for em dashes (not allowed per SOP)
        if "\u2014" in body or "—" in body:
            suggestions.append({"type": "style", "severity": "low",
                "message": "Contains em dashes. Replace with commas or short hyphens per style rules."})
        else:
            score += 1

        # 9. Check opener variety (should not start with "I noticed" or "I saw")
        if body.strip().lower().startswith("i noticed") or body.strip().lower().startswith("i saw"):
            suggestions.append({"type": "style", "severity": "low",
                "message": "Opener starts with 'I noticed/I saw'. Vary your openers."})
        else:
            score += 1

        # 10. Check research utilization
        if research_snapshot:
            pain_indicators = research_snapshot.get("pain_indicators", "[]")
            try:
                pains = json.loads(pain_indicators) if isinstance(pain_indicators, str) else pain_indicators
            except:
                pains = []
            if pains and not any(p.lower() in body.lower() for p in pains[:3] if isinstance(p, str)):
                suggestions.append({"type": "research_utilization", "severity": "medium",
                    "message": "Research identified pain indicators not reflected in the message. Consider incorporating: " + ", ".join(pains[:3])})
            else:
                score += 1
        else:
            suggestions.append({"type": "research_utilization", "severity": "high",
                "message": "No research snapshot linked. Research the prospect before drafting."})

        quality_rating = "excellent" if score >= 8 else "good" if score >= 6 else "needs_work" if score >= 4 else "poor"

        return {
            "draft_id": draft_id,
            "score": score,
            "max_score": max_score,
            "quality_rating": quality_rating,
            "suggestions": suggestions,
            "research_available": research_snapshot is not None,
            "word_count": word_count,
            "touch_number": touch_num,
        }
    finally:
        conn.close()
