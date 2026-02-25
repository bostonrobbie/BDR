"""
Outreach Command Center - Database Initialization
Creates all tables, indexes, and seeds initial data.
"""

import sqlite3
import os
from datetime import datetime
try:
    from .migrate_v2 import run_migration as run_v2_migration
except ImportError:
    from migrate_v2 import run_migration as run_v2_migration

DB_PATH = os.environ.get("OCC_DB_PATH", "outreach.db")

SCHEMA_SQL = """
-- Accounts (company-level)
CREATE TABLE IF NOT EXISTS accounts (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT,
    industry TEXT,
    sub_industry TEXT,
    employee_count INTEGER,
    employee_band TEXT,
    tier TEXT,
    known_tools TEXT DEFAULT '[]',
    linkedin_company_url TEXT,
    website_url TEXT,
    buyer_intent INTEGER DEFAULT 0,
    buyer_intent_date TEXT,
    annual_revenue TEXT,
    funding_stage TEXT,
    last_funding_date TEXT,
    last_funding_amount TEXT,
    hq_location TEXT,
    notes TEXT,
    research_freshness TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Contacts (person-level)
CREATE TABLE IF NOT EXISTS contacts (
    id TEXT PRIMARY KEY,
    account_id TEXT REFERENCES accounts(id),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    title TEXT,
    persona_type TEXT,
    seniority_level TEXT,
    email TEXT,
    email_verified INTEGER DEFAULT 0,
    linkedin_url TEXT UNIQUE,
    phone TEXT,
    location TEXT,
    timezone TEXT,
    tenure_months INTEGER,
    recently_hired INTEGER DEFAULT 0,
    previous_company TEXT,
    previous_title TEXT,
    stage TEXT DEFAULT 'new',
    priority_score INTEGER DEFAULT 3,
    priority_factors TEXT DEFAULT '{}',
    personalization_score INTEGER,
    predicted_objection TEXT,
    objection_response TEXT,
    status TEXT DEFAULT 'active',
    do_not_contact INTEGER DEFAULT 0,
    dnc_reason TEXT,
    source TEXT DEFAULT 'sales_nav',
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- ICP Scores
CREATE TABLE IF NOT EXISTS icp_scores (
    id TEXT PRIMARY KEY,
    contact_id TEXT REFERENCES contacts(id),
    title_match INTEGER DEFAULT 0,
    vertical_match INTEGER DEFAULT 0,
    company_size_fit INTEGER DEFAULT 0,
    seniority_fit INTEGER DEFAULT 0,
    software_qa_confirmed INTEGER DEFAULT 0,
    buyer_intent_bonus INTEGER DEFAULT 0,
    total_score INTEGER DEFAULT 0,
    scored_at TEXT DEFAULT (datetime('now')),
    scoring_version TEXT DEFAULT 'v1'
);

-- Signals
CREATE TABLE IF NOT EXISTS signals (
    id TEXT PRIMARY KEY,
    account_id TEXT REFERENCES accounts(id),
    contact_id TEXT REFERENCES contacts(id),
    signal_type TEXT NOT NULL,
    description TEXT,
    source_url TEXT,
    detected_at TEXT DEFAULT (datetime('now')),
    expires_at TEXT,
    acted_on INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Research Snapshots
CREATE TABLE IF NOT EXISTS research_snapshots (
    id TEXT PRIMARY KEY,
    contact_id TEXT REFERENCES contacts(id),
    account_id TEXT REFERENCES accounts(id),
    entity_type TEXT NOT NULL,
    headline TEXT,
    summary TEXT,
    career_history TEXT DEFAULT '[]',
    responsibilities TEXT,
    tech_stack_signals TEXT DEFAULT '[]',
    pain_indicators TEXT DEFAULT '[]',
    recent_activity TEXT,
    company_products TEXT,
    company_metrics TEXT,
    company_news TEXT,
    hiring_signals TEXT,
    sources TEXT DEFAULT '[]',
    confidence_score INTEGER DEFAULT 3,
    agent_run_id TEXT REFERENCES agent_runs(id),
    created_at TEXT DEFAULT (datetime('now'))
);

-- Message Drafts
CREATE TABLE IF NOT EXISTS message_drafts (
    id TEXT PRIMARY KEY,
    contact_id TEXT REFERENCES contacts(id),
    batch_id TEXT REFERENCES batches(id),
    channel TEXT NOT NULL,
    touch_number INTEGER,
    touch_type TEXT NOT NULL,
    subject_line TEXT,
    body TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    personalization_score INTEGER,
    proof_point_used TEXT,
    pain_hook TEXT,
    opener_style TEXT,
    ask_style TEXT,
    word_count INTEGER,
    qc_passed INTEGER,
    qc_flags TEXT DEFAULT '[]',
    qc_run_id TEXT,
    approval_status TEXT DEFAULT 'draft',
    ab_group TEXT,
    ab_variable TEXT,
    subject_line_style TEXT,
    agent_run_id TEXT REFERENCES agent_runs(id),
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Touchpoints
CREATE TABLE IF NOT EXISTS touchpoints (
    id TEXT PRIMARY KEY,
    contact_id TEXT REFERENCES contacts(id),
    message_draft_id TEXT REFERENCES message_drafts(id),
    channel TEXT NOT NULL,
    touch_number INTEGER,
    sent_at TEXT NOT NULL,
    outcome TEXT,
    call_duration_seconds INTEGER,
    call_notes TEXT,
    confirmed_by_user INTEGER DEFAULT 1,
    subject_line_style TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Replies
CREATE TABLE IF NOT EXISTS replies (
    id TEXT PRIMARY KEY,
    contact_id TEXT REFERENCES contacts(id),
    touchpoint_id TEXT REFERENCES touchpoints(id),
    channel TEXT,
    intent TEXT,
    reply_tag TEXT,
    summary TEXT,
    raw_text TEXT,
    referral_name TEXT,
    referral_title TEXT,
    recommended_next_step TEXT,
    next_step_taken TEXT,
    replied_at TEXT,
    handled_at TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Follow-ups
CREATE TABLE IF NOT EXISTS followups (
    id TEXT PRIMARY KEY,
    contact_id TEXT REFERENCES contacts(id),
    touch_number INTEGER,
    channel TEXT,
    due_date TEXT,
    state TEXT DEFAULT 'pending',
    message_draft_id TEXT REFERENCES message_drafts(id),
    reminder_sent INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    completed_at TEXT
);

-- Opportunities
CREATE TABLE IF NOT EXISTS opportunities (
    id TEXT PRIMARY KEY,
    contact_id TEXT REFERENCES contacts(id),
    account_id TEXT REFERENCES accounts(id),
    meeting_date TEXT,
    meeting_held INTEGER DEFAULT 0,
    meeting_outcome TEXT,
    opportunity_created_date TEXT,
    opportunity_created INTEGER DEFAULT 0,
    status TEXT DEFAULT 'meeting_booked',
    pipeline_value REAL,
    trigger_touchpoint_id TEXT REFERENCES touchpoints(id),
    trigger_reply_id TEXT REFERENCES replies(id),
    attribution_channel TEXT,
    attribution_touch_number INTEGER,
    attribution_proof_point TEXT,
    attribution_pain_hook TEXT,
    attribution_opener_style TEXT,
    attribution_personalization_score INTEGER,
    attribution_ab_group TEXT,
    attribution_ab_variable TEXT,
    ae_name TEXT,
    ae_feedback TEXT,
    disqualification_reason TEXT,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Batches
CREATE TABLE IF NOT EXISTS batches (
    id TEXT PRIMARY KEY,
    batch_number INTEGER,
    created_date TEXT,
    prospect_count INTEGER DEFAULT 0,
    ab_variable TEXT,
    ab_description TEXT,
    pre_brief TEXT,
    mix_ratio TEXT DEFAULT '{}',
    status TEXT DEFAULT 'building',
    html_file_path TEXT,
    metrics TEXT DEFAULT '{}',
    created_at TEXT DEFAULT (datetime('now'))
);

-- Batch Prospects (join table)
CREATE TABLE IF NOT EXISTS batch_prospects (
    id TEXT PRIMARY KEY,
    batch_id TEXT REFERENCES batches(id),
    contact_id TEXT REFERENCES contacts(id),
    ab_group TEXT,
    sequence_status TEXT DEFAULT 'not_started',
    position_in_batch INTEGER
);

-- Experiments
CREATE TABLE IF NOT EXISTS experiments (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    variable TEXT,
    group_a_desc TEXT,
    group_b_desc TEXT,
    status TEXT DEFAULT 'active',
    batches_included TEXT DEFAULT '[]',
    group_a_sent INTEGER DEFAULT 0,
    group_a_replies INTEGER DEFAULT 0,
    group_a_meetings INTEGER DEFAULT 0,
    group_a_opps INTEGER DEFAULT 0,
    group_b_sent INTEGER DEFAULT 0,
    group_b_replies INTEGER DEFAULT 0,
    group_b_meetings INTEGER DEFAULT 0,
    group_b_opps INTEGER DEFAULT 0,
    winner TEXT,
    conclusion TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Agent Runs
CREATE TABLE IF NOT EXISTS agent_runs (
    id TEXT PRIMARY KEY,
    run_type TEXT NOT NULL,
    agent_name TEXT,
    contact_id TEXT REFERENCES contacts(id),
    batch_id TEXT REFERENCES batches(id),
    inputs TEXT DEFAULT '{}',
    outputs TEXT DEFAULT '{}',
    sources_used TEXT DEFAULT '[]',
    decisions TEXT DEFAULT '{}',
    tokens_used INTEGER DEFAULT 0,
    duration_ms INTEGER DEFAULT 0,
    status TEXT DEFAULT 'running',
    error_message TEXT,
    parent_run_id TEXT REFERENCES agent_runs(id),
    started_at TEXT DEFAULT (datetime('now')),
    completed_at TEXT
);

-- Audit Log
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    record_id TEXT NOT NULL,
    action TEXT NOT NULL,
    changed_by TEXT,
    old_values TEXT,
    new_values TEXT,
    timestamp TEXT DEFAULT (datetime('now'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_contacts_account ON contacts(account_id);
CREATE INDEX IF NOT EXISTS idx_contacts_stage ON contacts(stage);
CREATE INDEX IF NOT EXISTS idx_contacts_priority ON contacts(priority_score DESC);
CREATE INDEX IF NOT EXISTS idx_contacts_linkedin ON contacts(linkedin_url);
CREATE INDEX IF NOT EXISTS idx_research_contact ON research_snapshots(contact_id);
CREATE INDEX IF NOT EXISTS idx_research_account ON research_snapshots(account_id);
CREATE INDEX IF NOT EXISTS idx_messages_contact ON message_drafts(contact_id);
CREATE INDEX IF NOT EXISTS idx_messages_batch ON message_drafts(batch_id);
CREATE INDEX IF NOT EXISTS idx_touchpoints_contact ON touchpoints(contact_id);
CREATE INDEX IF NOT EXISTS idx_touchpoints_sent ON touchpoints(sent_at);
CREATE INDEX IF NOT EXISTS idx_replies_contact ON replies(contact_id);
CREATE INDEX IF NOT EXISTS idx_followups_due ON followups(due_date, state);
CREATE INDEX IF NOT EXISTS idx_opportunities_contact ON opportunities(contact_id);
CREATE INDEX IF NOT EXISTS idx_opportunities_status ON opportunities(status);
CREATE INDEX IF NOT EXISTS idx_signals_account ON signals(account_id);
CREATE INDEX IF NOT EXISTS idx_batch_prospects ON batch_prospects(batch_id, contact_id);
CREATE INDEX IF NOT EXISTS idx_agent_runs_type ON agent_runs(run_type);
CREATE INDEX IF NOT EXISTS idx_audit_table ON audit_log(table_name, record_id);
"""


def init_db(db_path=None):
    """Initialize the database with all tables and indexes."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA_SQL)
    conn.commit()

    # Verify tables were created
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Database initialized at {path}")
    print(f"Tables created: {len(tables)}")
    for t in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t}: {count} rows")

    conn.close()
    return tables


def verify_db(db_path=None):
    """Verify the database schema is correct."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)

    expected_tables = [
        'accounts', 'contacts', 'icp_scores', 'signals',
        'research_snapshots', 'message_drafts', 'touchpoints',
        'replies', 'followups', 'opportunities', 'batches',
        'batch_prospects', 'experiments', 'agent_runs', 'audit_log'
    ]

    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    actual_tables = [row[0] for row in cursor.fetchall()]

    missing = set(expected_tables) - set(actual_tables)
    if missing:
        print(f"FAIL: Missing tables: {missing}")
        return False

    print(f"PASS: All {len(expected_tables)} tables present")
    conn.close()
    return True


if __name__ == "__main__":
    init_db()
    verify_db()
    print("\n[init_db] Running v2 migration...")
    if run_v2_migration():
        print("[init_db] v2 migration successful!")
    else:
        print("[init_db] WARNING: v2 migration failed")
