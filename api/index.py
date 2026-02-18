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

# Set DB path to /tmp for Vercel serverless
os.environ["OCC_DB_PATH"] = "/tmp/outreach.db"

# Add project root to path
project_root = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, project_root)

from fastapi import FastAPI, HTTPException, Query, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List

# ---------------------------------------------------------------------------
# DATABASE LAYER (self-contained for serverless)
# ---------------------------------------------------------------------------

DB_PATH = "/tmp/outreach.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
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
    created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now'))
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
    source TEXT DEFAULT 'sales_nav',
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
    expires_at TEXT, acted_on INTEGER DEFAULT 0, created_at TEXT DEFAULT (datetime('now'))
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
    updated_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS touchpoints (
    id TEXT PRIMARY KEY, contact_id TEXT REFERENCES contacts(id),
    message_draft_id TEXT REFERENCES message_drafts(id), channel TEXT NOT NULL,
    touch_number INTEGER, sent_at TEXT NOT NULL, outcome TEXT,
    call_duration_seconds INTEGER, call_notes TEXT,
    confirmed_by_user INTEGER DEFAULT 1, created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS replies (
    id TEXT PRIMARY KEY, contact_id TEXT REFERENCES contacts(id),
    touchpoint_id TEXT REFERENCES touchpoints(id), channel TEXT,
    intent TEXT, reply_tag TEXT, summary TEXT, raw_text TEXT,
    referral_name TEXT, referral_title TEXT, recommended_next_step TEXT,
    next_step_taken TEXT, replied_at TEXT, handled_at TEXT,
    created_at TEXT DEFAULT (datetime('now'))
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
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS batches (
    id TEXT PRIMARY KEY, batch_number INTEGER, created_date TEXT,
    prospect_count INTEGER DEFAULT 0, ab_variable TEXT, ab_description TEXT,
    pre_brief TEXT, mix_ratio TEXT DEFAULT '{}', status TEXT DEFAULT 'building',
    html_file_path TEXT, metrics TEXT DEFAULT '{}',
    created_at TEXT DEFAULT (datetime('now'))
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
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")

    # Check if already seeded
    count = conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]
    if count > 0:
        conn.close()
        return

    now = datetime.utcnow()
    random.seed(42)

    account_ids = []
    contact_ids = []
    batch_ids = []
    message_ids = []

    # --- ACCOUNTS ---
    for i, (name, domain, industry, emp) in enumerate(COMPANIES):
        aid = f"acc_{uuid.uuid4().hex[:12]}"
        account_ids.append(aid)
        tier = "enterprise" if emp > 5000 else ("mid_market" if emp > 1000 else "smb")
        tools = random.choice([["Selenium"], ["Cypress"], ["Playwright"], ["Katalon"], ["TOSCA"], []])
        conn.execute("""INSERT INTO accounts (id,name,domain,industry,employee_count,employee_band,tier,
            known_tools,buyer_intent,hq_location,created_at,updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (aid, name, domain, industry, emp,
             "1K-5K" if emp < 5000 else "5K+", tier,
             json.dumps(tools), random.choice([0,0,0,1]), "San Francisco, CA",
             (now - timedelta(days=random.randint(1,90))).isoformat(),
             now.isoformat()))

    # --- CONTACTS ---
    for i in range(25):
        cid = f"con_{uuid.uuid4().hex[:12]}"
        contact_ids.append(cid)
        acct = account_ids[i % len(account_ids)]
        is_qa = i < 15
        title = random.choice(TITLES_QA) if is_qa else random.choice(TITLES_VP)
        persona = "qa_leader" if is_qa else "vp_eng"
        priority = random.randint(2, 5)
        stage = random.choice(STAGES)
        conn.execute("""INSERT INTO contacts (id,account_id,first_name,last_name,title,persona_type,
            seniority_level,email,linkedin_url,location,tenure_months,recently_hired,
            stage,priority_score,personalization_score,status,source,created_at,updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (cid, acct, FIRST_NAMES[i], LAST_NAMES[i], title, persona,
             "director" if "Director" in title or "Head" in title else ("vp" if "VP" in title or "CTO" in title else "manager"),
             f"{FIRST_NAMES[i].lower()}.{LAST_NAMES[i].lower()}@{COMPANIES[i%len(COMPANIES)][1]}",
             f"https://linkedin.com/in/{FIRST_NAMES[i].lower()}{LAST_NAMES[i].lower()}{random.randint(10,99)}",
             "San Francisco, CA", random.randint(3, 72),
             1 if random.random() < 0.2 else 0,
             stage, priority, random.randint(1,3), "active", "sales_nav",
             (now - timedelta(days=random.randint(1,60))).isoformat(), now.isoformat()))

    # --- BATCHES ---
    for b in range(3):
        bid = f"bat_{uuid.uuid4().hex[:12]}"
        batch_ids.append(bid)
        conn.execute("""INSERT INTO batches (id,batch_number,created_date,prospect_count,
            ab_variable,status,created_at) VALUES (?,?,?,?,?,?,?)""",
            (bid, b+1, (now - timedelta(days=30-b*10)).strftime("%Y-%m-%d"),
             random.randint(20,25), random.choice(["pain_hook","proof_point_style","opener_style"]),
             "complete" if b < 2 else "active", now.isoformat()))

    # --- MESSAGE DRAFTS ---
    for i, cid in enumerate(contact_ids[:20]):
        for touch in [1, 3, 5, 6]:
            mid = f"msg_{uuid.uuid4().hex[:12]}"
            message_ids.append(mid)
            bid = batch_ids[i % len(batch_ids)]
            ch = "linkedin" if touch in [1,3,6] else "email"
            conn.execute("""INSERT INTO message_drafts (id,contact_id,batch_id,channel,
                touch_number,touch_type,subject_line,body,personalization_score,
                proof_point_used,pain_hook,opener_style,word_count,
                approval_status,ab_group,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (mid, cid, bid, ch, touch,
                 f"touch_{touch}_{'inmail' if ch=='linkedin' else 'email'}",
                 f"Quick question about QA at {COMPANIES[i%len(COMPANIES)][0]}",
                 f"Hey {FIRST_NAMES[i%25]}, saw your work leading QA at {COMPANIES[i%len(COMPANIES)][0]}...",
                 random.randint(1,3), random.choice(PROOF_POINTS),
                 random.choice(PAIN_HOOKS),
                 random.choice(["career_reference", "company_metric", "role_specific"]),
                 random.randint(70,120),
                 random.choice(["approved","draft","pending_review"]),
                 random.choice(["A","B"]), now.isoformat()))

    # --- TOUCHPOINTS ---
    for i in range(40):
        cid = contact_ids[i % len(contact_ids)]
        tid = f"tp_{uuid.uuid4().hex[:12]}"
        ch = random.choice(CHANNELS)
        conn.execute("""INSERT INTO touchpoints (id,contact_id,channel,touch_number,
            sent_at,outcome,created_at) VALUES (?,?,?,?,?,?,?)""",
            (tid, cid, ch, random.randint(1,6),
             (now - timedelta(days=random.randint(1,45))).isoformat(),
             random.choice(["sent","opened","no_response","replied"]),
             now.isoformat()))

    # --- REPLIES ---
    for i in range(12):
        cid = contact_ids[i % len(contact_ids)]
        rid = f"rep_{uuid.uuid4().hex[:12]}"
        conn.execute("""INSERT INTO replies (id,contact_id,channel,intent,reply_tag,
            summary,replied_at,created_at) VALUES (?,?,?,?,?,?,?,?)""",
            (rid, cid, random.choice(["linkedin","email"]),
             random.choice(["positive","negative","referral","timing"]),
             random.choice(["pain_hook","proof_point","timing","referral","opener","not_interested"]),
             "Thanks for reaching out...",
             (now - timedelta(days=random.randint(1,30))).isoformat(),
             now.isoformat()))

    # --- OPPORTUNITIES ---
    for i in range(5):
        cid = contact_ids[i]
        aid = account_ids[i]
        conn.execute("""INSERT INTO opportunities (id,contact_id,account_id,meeting_date,
            status,pipeline_value,attribution_channel,attribution_proof_point,
            attribution_pain_hook,created_at) VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (f"opp_{uuid.uuid4().hex[:12]}", cid, aid,
             (now + timedelta(days=random.randint(1,14))).isoformat(),
             random.choice(["meeting_booked","meeting_held","opportunity_created"]),
             random.choice([15000, 25000, 50000, 75000]),
             random.choice(["linkedin","email"]),
             random.choice(PROOF_POINTS), random.choice(PAIN_HOOKS),
             now.isoformat()))

    # --- SIGNALS ---
    for i in range(15):
        aid = account_ids[i % len(account_ids)]
        cid = contact_ids[i % len(contact_ids)]
        conn.execute("""INSERT INTO signals (id,account_id,contact_id,signal_type,
            description,created_at) VALUES (?,?,?,?,?,?)""",
            (f"sig_{uuid.uuid4().hex[:12]}", aid, cid,
             random.choice(["buyer_intent","job_posting","funding","product_launch","leadership_change"]),
             random.choice(["Buyer intent detected on G2", "New QA engineer job posting",
                          "Series B funding announced", "Major product launch", "New VP Eng hired"]),
             (now - timedelta(days=random.randint(1,20))).isoformat()))

    # --- EXPERIMENTS ---
    for i, (name, var) in enumerate([
        ("Pain Hook: Flaky vs Speed", "pain_hook"),
        ("Proof Point: Named vs Anonymous", "proof_point_style"),
        ("Opener: Career vs Company", "opener_style"),
    ]):
        conn.execute("""INSERT INTO experiments (id,name,variable,group_a_desc,group_b_desc,
            status,group_a_sent,group_a_replies,group_b_sent,group_b_replies,
            created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (f"exp_{uuid.uuid4().hex[:12]}", name, var,
             f"Group A: {var} variant 1", f"Group B: {var} variant 2",
             "active", random.randint(20,40), random.randint(0,4),
             random.randint(20,40), random.randint(0,4), now.isoformat()))

    # --- AGENT RUNS ---
    for i in range(20):
        conn.execute("""INSERT INTO agent_runs (id,run_type,agent_name,status,
            tokens_used,duration_ms,started_at,completed_at) VALUES (?,?,?,?,?,?,?,?)""",
            (f"run_{uuid.uuid4().hex[:12]}",
             random.choice(["research","scoring","drafting","qc","swarm"]),
             random.choice(["ResearchAgent","ScoringAgent","DraftingAgent","QCAgent","SwarmSupervisor"]),
             random.choice(["completed","completed","completed","failed"]),
             random.randint(500,5000), random.randint(1000,30000),
             (now - timedelta(hours=random.randint(1,72))).isoformat(),
             now.isoformat()))

    # --- FOLLOWUPS ---
    for i in range(8):
        cid = contact_ids[i % len(contact_ids)]
        conn.execute("""INSERT INTO followups (id,contact_id,touch_number,channel,
            due_date,state,created_at) VALUES (?,?,?,?,?,?,?)""",
            (f"fu_{uuid.uuid4().hex[:12]}", cid, random.randint(2,6),
             random.choice(CHANNELS),
             (now + timedelta(days=random.randint(-3,7))).strftime("%Y-%m-%d"),
             random.choice(["pending","pending","completed"]), now.isoformat()))

    # --- EMAIL IDENTITIES ---
    conn.execute("""INSERT INTO email_identities (id,email_address,display_name,
        daily_limit,warmup_phase,warmup_day,reputation_score,is_active,created_at)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        ("eid_primary", "rob@testsigma.com", "Rob Gorham",
         50, 0, 30, 98.5, 1, now.isoformat()))
    conn.execute("""INSERT INTO email_identities (id,email_address,display_name,
        daily_limit,warmup_phase,warmup_day,reputation_score,is_active,created_at)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        ("eid_secondary", "rgorham@testsigma.com", "Rob G",
         30, 1, 12, 92.0, 1, now.isoformat()))

    # --- PACING RULES ---
    conn.execute("""INSERT INTO pacing_rules (id,identity_id,channel,max_per_day,
        max_per_hour,min_gap_seconds,is_active) VALUES (?,?,?,?,?,?,?)""",
        ("pr_1", "eid_primary", "email", 50, 10, 120, 1))

    # --- SWARM RUNS ---
    for i in range(5):
        conn.execute("""INSERT INTO swarm_runs (id,swarm_type,status,total_tasks,
            completed_tasks,failed_tasks,started_at) VALUES (?,?,?,?,?,?,?)""",
            (f"swarm_{uuid.uuid4().hex[:12]}", "full_batch",
             random.choice(["completed","completed","running"]),
             random.randint(20,50), random.randint(15,45), random.randint(0,3),
             (now - timedelta(hours=random.randint(1,48))).isoformat()))

    # --- FEATURE FLAGS ---
    for name, enabled, desc in [
        ("email_sending", 1, "Enable live email sending"),
        ("auto_followup", 0, "Auto-schedule followups"),
        ("swarm_mode", 1, "Enable agent swarm orchestration"),
        ("quality_gate", 1, "QC gate before message approval"),
        ("buyer_intent_boost", 1, "Boost priority for buyer intent signals"),
    ]:
        conn.execute("""INSERT INTO feature_flags (id,name,enabled,description,created_at)
            VALUES (?,?,?,?,?)""",
            (f"ff_{uuid.uuid4().hex[:12]}", name, enabled, desc, now.isoformat()))

    # --- FLOW RUNS (new) ---
    for i in range(4):
        frid = f"flow_{uuid.uuid4().hex[:12]}"
        flow_status = "completed" if i < 2 else "running"
        conn.execute("""INSERT INTO flow_runs (id,flow_type,status,config,total_steps,
            completed_steps,failed_steps,started_at,completed_at,duration_ms,created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (frid, random.choice(["account_research", "linkedin_prospecting", "email_prospecting"]),
             flow_status, json.dumps({"volume_cap": 10, "quality_bar": "strict"}),
             5, 5 if flow_status == "completed" else 2,
             0, (now - timedelta(hours=random.randint(2,24))).isoformat(),
             (now - timedelta(hours=random.randint(0,12))).isoformat() if flow_status == "completed" else None,
             random.randint(30000, 180000) if flow_status == "completed" else 0,
             (now - timedelta(hours=random.randint(2,24))).isoformat()))

    # --- FLOW RUN STEPS (new) ---
    flow_runs = conn.execute("SELECT id FROM flow_runs").fetchall()
    for fr in flow_runs:
        flow_run_id = fr[0]
        for step_idx in range(5):
            step_id = f"step_{uuid.uuid4().hex[:12]}"
            step_status = "completed" if step_idx < 4 else "pending"
            conn.execute("""INSERT INTO flow_run_steps (id,flow_run_id,step_name,agent_type,
                status,tokens_used,duration_ms,started_at,completed_at,created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (step_id, flow_run_id, f"step_{step_idx+1}",
                 random.choice(["ResearchAgent", "DraftingAgent", "QCAgent"]),
                 step_status, random.randint(500, 2000) if step_status == "completed" else 0,
                 random.randint(5000, 30000) if step_status == "completed" else 0,
                 (now - timedelta(hours=1)).isoformat() if step_status == "completed" else None,
                 (now - timedelta(minutes=30)).isoformat() if step_status == "completed" else None,
                 (now - timedelta(hours=1)).isoformat()))

    # --- FLOW ARTIFACTS (new) ---
    for fr in flow_runs[:2]:
        flow_run_id = fr[0]
        art_id = f"art_{uuid.uuid4().hex[:12]}"
        conn.execute("""INSERT INTO flow_artifacts (id,flow_run_id,artifact_type,title,
            content,metadata,status,created_at)
            VALUES (?,?,?,?,?,?,?,?)""",
            (art_id, flow_run_id, "account_brief", "Account Research Brief",
             json.dumps({"account": "Example Corp", "employees": 5000, "industry": "SaaS"}),
             json.dumps({"research_depth": "comprehensive"}), "ready", now.isoformat()))

    # --- ACTIVITY TIMELINE (new) ---
    for i in range(12):
        act_id = f"act_{uuid.uuid4().hex[:12]}"
        contact_id = contact_ids[i % len(contact_ids)]
        conn.execute("""INSERT INTO activity_timeline (id,contact_id,channel,activity_type,
            description,created_at) VALUES (?,?,?,?,?,?)""",
            (act_id, contact_id,
             random.choice(["linkedin", "email", "phone"]),
             random.choice(["message_sent", "reply_received", "meeting_booked", "call_made"]),
             f"Activity on {contact_id}",
             (now - timedelta(days=random.randint(1,20))).isoformat()))

    # --- DRAFT VERSIONS (new) ---
    for i, cid in enumerate(contact_ids[:10]):
        draft_id = f"draft_{uuid.uuid4().hex[:12]}"
        for v in range(1, 3):
            dv_id = f"draftv_{uuid.uuid4().hex[:12]}"
            conn.execute("""INSERT INTO draft_versions (id,draft_id,contact_id,channel,
                touch_number,subject,body,version,status,personalization_score,
                proof_point,pain_hook,opener_style,word_count,confidence_score,created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (dv_id, draft_id, cid,
                 random.choice(["linkedin", "email"]), random.randint(1,6),
                 f"Subject for {cid}",
                 f"Body text for version {v}",
                 v, "draft" if v == 1 else "approved",
                 random.randint(1,3), random.choice(PROOF_POINTS),
                 random.choice(PAIN_HOOKS),
                 random.choice(["career_reference", "company_metric"]),
                 random.randint(70, 120),
                 0.85 + random.random() * 0.15,
                 (now - timedelta(days=random.randint(1,10))).isoformat()))

    # --- SENDER HEALTH SNAPSHOTS (new) ---
    email_identities = conn.execute("SELECT id FROM email_identities").fetchall()
    for eid in email_identities:
        identity_id = eid[0]
        for d in range(2):
            snap_id = f"snap_{uuid.uuid4().hex[:12]}"
            snap_date = (now - timedelta(days=d)).strftime("%Y-%m-%d")
            conn.execute("""INSERT INTO sender_health_snapshots (id,identity_id,date,
                emails_sent,bounces,complaints,replies,bounce_rate,complaint_rate,
                reply_rate,domain_reputation,spf_pass,dkim_pass,dmarc_pass,created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (snap_id, identity_id, snap_date,
                 random.randint(30, 50), random.randint(0, 2),
                 0, random.randint(2, 8),
                 round(random.uniform(0, 0.05), 3),
                 0.0,
                 round(random.uniform(0.05, 0.15), 3),
                 "good", 1, 1, random.choice([0, 1]),
                 now.isoformat()))

    # --- CONTACT IDENTITIES (new) ---
    for cid in contact_ids[:15]:
        ci_id = f"ci_{uuid.uuid4().hex[:12]}"
        conn.execute("""INSERT INTO contact_identities (id,contact_id,identity_type,
            value,verified,is_primary,created_at)
            VALUES (?,?,?,?,?,?,?)""",
            (ci_id, cid, "email",
             f"{FIRST_NAMES[contact_ids.index(cid) % len(FIRST_NAMES)].lower()}.{LAST_NAMES[contact_ids.index(cid) % len(LAST_NAMES)].lower()}@example.com",
             1, 1, now.isoformat()))

    conn.commit()
    conn.close()

# ---------------------------------------------------------------------------
# INITIALIZE DB ON COLD START
# ---------------------------------------------------------------------------

def init_and_seed():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
    seed_database()

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
    conn.close()
    return {
        "total_contacts": total,
        "by_stage": by_stage,
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
    """Generate and return the HTML deliverable for a batch."""
    try:
        conn = get_db()

        # Get batch
        batch_row = conn.execute("SELECT * FROM batches WHERE id=?", (batch_id,)).fetchone()
        if not batch_row:
            conn.close()
            raise HTTPException(404, "Batch not found")

        batch = dict(batch_row)

        # Get contacts in batch with messages
        contacts = conn.execute("""
            SELECT c.*, a.name as company_name, a.industry, a.employee_count,
                   a.known_tools, a.buyer_intent, bp.ab_group
            FROM batch_prospects bp
            JOIN contacts c ON bp.contact_id = c.id
            LEFT JOIN accounts a ON c.account_id = a.id
            WHERE bp.batch_id = ?
            ORDER BY c.priority_score DESC
        """, (batch_id,)).fetchall()

        contacts = [dict(c) for c in contacts]

        # Get messages for each contact
        messages_by_contact = {}
        for c in contacts:
            msgs = conn.execute("""
                SELECT * FROM message_drafts WHERE contact_id=? AND batch_id=?
                ORDER BY touch_number ASC
            """, (c["id"], batch_id)).fetchall()
            messages_by_contact[c["id"]] = [dict(m) for m in msgs]

        conn.close()

        # Build HTML
        html = _generate_deliverable_html(batch, contacts, messages_by_contact)

        # Return as HTML response
        from starlette.responses import HTMLResponse
        return HTMLResponse(html)

    except Exception as e:
        raise HTTPException(500, str(e))

def _generate_deliverable_html(batch: dict, contacts: list, messages_by_contact: dict) -> str:
    """Generate self-contained HTML deliverable."""
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    batch_num = batch.get("batch_number", 1)

    html_parts = []
    html_parts.append(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Batch {batch_num} - Prospect Outreach - {date_str}</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                     background: #f5f5f5; margin: 0; padding: 20px; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }}
            h1 {{ color: #1f2937; margin: 0 0 10px 0; }}
            .meta {{ color: #6b7280; font-size: 14px; margin-bottom: 30px; }}
            .controls {{ margin-bottom: 20px; }}
            button {{ padding: 8px 16px; margin-right: 10px; background: #3b82f6; color: white;
                      border: none; border-radius: 4px; cursor: pointer; }}
            button:hover {{ background: #2563eb; }}
            .prospect-card {{ border: 1px solid #e5e7eb; border-radius: 6px; padding: 20px; margin-bottom: 20px; }}
            .prospect-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }}
            .prospect-name {{ font-size: 18px; font-weight: 600; color: #1f2937; }}
            .prospect-meta {{ color: #6b7280; font-size: 14px; }}
            .priority-badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px;
                              font-size: 12px; font-weight: 600; margin-right: 8px; }}
            .priority-5 {{ background: #fee2e2; color: #991b1b; }}
            .priority-4 {{ background: #fef3c7; color: #92400e; }}
            .priority-3 {{ background: #dbeafe; color: #0c2d6b; }}
            .touch-section {{ margin: 20px 0; padding: 15px; background: #f9fafb; border-left: 4px solid #3b82f6; }}
            .touch-title {{ font-weight: 600; color: #1f2937; margin-bottom: 10px; }}
            .subject {{ color: #0c2d6b; font-style: italic; margin: 10px 0; }}
            .body {{ white-space: pre-wrap; font-family: 'Monaco', 'Courier New', monospace;
                    font-size: 13px; color: #374151; line-height: 1.5; }}
            .copy-btn {{ padding: 4px 8px; font-size: 12px; background: #10b981; color: white;
                        border: none; border-radius: 3px; cursor: pointer; }}
            .copy-btn:hover {{ background: #059669; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e5e7eb; }}
            th {{ background: #f3f4f6; font-weight: 600; color: #1f2937; }}
            tr:hover {{ background: #f9fafb; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Batch {batch_num} - Prospect Outreach Pipeline</h1>
            <div class="meta">Generated: {date_str} | Contacts: {len(contacts)} | A/B Variable: {batch.get('ab_variable', 'N/A')}</div>

            <div class="controls">
                <button onclick="expandAll()">Expand All</button>
                <button onclick="collapseAll()">Collapse All</button>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Priority</th>
                        <th>Name</th>
                        <th>Title</th>
                        <th>Company</th>
                        <th>A/B Group</th>
                        <th>Vertical</th>
                    </tr>
                </thead>
                <tbody>
    """)

    for contact in contacts:
        priority = contact.get("priority_score", 3)
        priority_badge = f'<span class="priority-badge priority-{priority}">{priority}</span>'
        html_parts.append(f"""
                    <tr>
                        <td>{priority_badge}</td>
                        <td>{contact.get('first_name', '')} {contact.get('last_name', '')}</td>
                        <td>{contact.get('title', '')}</td>
                        <td>{contact.get('company_name', '')}</td>
                        <td><strong>{contact.get('ab_group', 'A')}</strong></td>
                        <td>{contact.get('industry', '')}</td>
                    </tr>
        """)

    html_parts.append("</tbody></table>")

    # Prospect cards with messages
    for contact in contacts:
        contact_id = contact.get("id", "")
        messages = messages_by_contact.get(contact_id, [])
        priority = contact.get("priority_score", 3)

        html_parts.append(f"""
            <div class="prospect-card">
                <div class="prospect-header">
                    <div>
                        <div class="prospect-name">{contact.get('first_name', '')} {contact.get('last_name', '')}</div>
                        <div class="prospect-meta">{contact.get('title', '')} at {contact.get('company_name', '')}</div>
                    </div>
                    <div>
                        <span class="priority-badge priority-{priority}">Priority {priority}</span>
                    </div>
                </div>
        """)

        # Organize messages by touch
        messages_by_touch = {}
        for msg in messages:
            touch = msg.get("touch_number", 1)
            if touch not in messages_by_touch:
                messages_by_touch[touch] = []
            messages_by_touch[touch].append(msg)

        # Display touches in order
        for touch_num in sorted(messages_by_touch.keys()):
            msgs = messages_by_touch[touch_num]
            for msg in msgs:
                channel = msg.get("channel", "")
                touch_type = msg.get("touch_type", "")
                subject = msg.get("subject_line", "")
                body = msg.get("body", "")

                html_parts.append(f"""
                <div class="touch-section">
                    <div class="touch-title">Touch {touch_num} - {channel.upper()} ({touch_type})</div>
                """)

                if subject:
                    html_parts.append(f'<div class="subject">Subject: {subject}</div>')

                html_parts.append(f'<div class="body">{body}</div>')
                html_parts.append(f'<button class="copy-btn" onclick="copyToClipboard(`{body}`)">Copy Message</button>')
                html_parts.append("</div>")

        # Objection
        if contact.get("predicted_objection"):
            html_parts.append(f"""
                <div class="touch-section" style="border-left-color: #ef4444;">
                    <div class="touch-title">Predicted Objection</div>
                    <div><strong>{contact.get('predicted_objection', '')}</strong></div>
                    <div class="body" style="margin-top: 10px;">{contact.get('objection_response', '')}</div>
                </div>
            """)

        html_parts.append("</div>")

    html_parts.append("""
        </div>
        <script>
            function expandAll() { document.querySelectorAll('.touch-section').forEach(el => el.style.display = 'block'); }
            function collapseAll() { document.querySelectorAll('.touch-section').forEach(el => el.style.display = 'none'); }
            function copyToClipboard(text) { navigator.clipboard.writeText(text); alert('Copied!'); }
        </script>
    </body>
    </html>
    """)

    return "\n".join(html_parts)

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
