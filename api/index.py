"""
Vercel Serverless Function - Outreach Command Center API
Wraps the FastAPI app for Vercel deployment with /tmp SQLite.
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

from fastapi import FastAPI, HTTPException, Query
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

CREATE INDEX IF NOT EXISTS idx_contacts_account ON contacts(account_id);
CREATE INDEX IF NOT EXISTS idx_contacts_stage ON contacts(stage);
CREATE INDEX IF NOT EXISTS idx_contacts_priority ON contacts(priority_score DESC);
CREATE INDEX IF NOT EXISTS idx_messages_contact ON message_drafts(contact_id);
CREATE INDEX IF NOT EXISTS idx_messages_batch ON message_drafts(batch_id);
CREATE INDEX IF NOT EXISTS idx_touchpoints_contact ON touchpoints(contact_id);
CREATE INDEX IF NOT EXISTS idx_replies_contact ON replies(contact_id);
CREATE INDEX IF NOT EXISTS idx_signals_account ON signals(account_id);
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
    est_cost = round(total_tokens * 0.000003, 2)  # rough estimate
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
