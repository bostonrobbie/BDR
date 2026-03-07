"""
Migration 003: Add process-intelligence tables for deterministic contact workflows.

These tables make per-contact execution explicit for humans and AI assistants:
- contact_action_plans: single source of truth for next-best action
- qualification_checks: auditable pass/fail checks before outreach
- research_evidence: fact-level research with citations and confidence
- sequence_state: Apollo/task cadence and send-state synchronization
- message_strategies: pre-draft strategy decisions per touch
- process_compliance_log: SOP step compliance tracking
"""


def up(conn):
    # ─── CONTACT ACTION PLANS ───────────────────────────────────────
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contact_action_plans (
            id TEXT PRIMARY KEY,
            contact_id TEXT NOT NULL REFERENCES contacts(id),
            current_step TEXT NOT NULL,
            next_action TEXT NOT NULL,
            next_action_due_at TEXT,
            blocked_reason TEXT,
            owner TEXT,
            priority_reason TEXT,
            last_decision_run_id TEXT REFERENCES agent_runs(id),
            status TEXT DEFAULT 'open',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # ─── QUALIFICATION CHECKS ───────────────────────────────────────
    conn.execute("""
        CREATE TABLE IF NOT EXISTS qualification_checks (
            id TEXT PRIMARY KEY,
            contact_id TEXT NOT NULL REFERENCES contacts(id),
            check_name TEXT NOT NULL,
            status TEXT NOT NULL,
            evidence TEXT,
            checked_by TEXT,
            run_id TEXT REFERENCES agent_runs(id),
            checked_at TEXT DEFAULT (datetime('now')),
            UNIQUE(contact_id, check_name, checked_at)
        )
    """)

    # ─── RESEARCH EVIDENCE ──────────────────────────────────────────
    conn.execute("""
        CREATE TABLE IF NOT EXISTS research_evidence (
            id TEXT PRIMARY KEY,
            contact_id TEXT REFERENCES contacts(id),
            account_id TEXT REFERENCES accounts(id),
            fact_type TEXT NOT NULL,
            fact_text TEXT NOT NULL,
            source_url TEXT,
            source_type TEXT,
            captured_at TEXT DEFAULT (datetime('now')),
            confidence INTEGER DEFAULT 3,
            expires_at TEXT,
            contradicted_by_reply INTEGER DEFAULT 0,
            run_id TEXT REFERENCES agent_runs(id)
        )
    """)

    # ─── SEQUENCE STATE ─────────────────────────────────────────────
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sequence_state (
            id TEXT PRIMARY KEY,
            contact_id TEXT NOT NULL REFERENCES contacts(id),
            apollo_sequence_id TEXT,
            apollo_step_number INTEGER,
            touch_number INTEGER,
            touch_eligible_date TEXT,
            last_sent_at TEXT,
            send_method TEXT DEFAULT 'apollo_ui_task_queue',
            delivery_status TEXT,
            skip_reason TEXT,
            next_action_date TEXT,
            updated_by TEXT,
            updated_at TEXT DEFAULT (datetime('now')),
            UNIQUE(contact_id)
        )
    """)

    # ─── MESSAGE STRATEGIES ─────────────────────────────────────────
    conn.execute("""
        CREATE TABLE IF NOT EXISTS message_strategies (
            id TEXT PRIMARY KEY,
            contact_id TEXT NOT NULL REFERENCES contacts(id),
            touch_number INTEGER NOT NULL,
            channel TEXT NOT NULL,
            primary_pain TEXT,
            proof_point_selected TEXT,
            opener_strategy TEXT,
            cta_strategy TEXT,
            risk_flags TEXT DEFAULT '[]',
            strategy_version TEXT DEFAULT 'v1',
            approved_by TEXT,
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            UNIQUE(contact_id, touch_number, channel, strategy_version)
        )
    """)

    # ─── PROCESS COMPLIANCE LOG ─────────────────────────────────────
    conn.execute("""
        CREATE TABLE IF NOT EXISTS process_compliance_log (
            id TEXT PRIMARY KEY,
            contact_id TEXT REFERENCES contacts(id),
            batch_id TEXT REFERENCES batches(id),
            sop_name TEXT NOT NULL,
            sop_step_id TEXT NOT NULL,
            required INTEGER DEFAULT 1,
            completed INTEGER DEFAULT 0,
            completed_at TEXT,
            evidence_ref TEXT,
            exceptions TEXT,
            actor TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # ─── INDEXES ────────────────────────────────────────────────────
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_cap_contact_status
        ON contact_action_plans(contact_id, status, next_action_due_at)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_qual_contact_check
        ON qualification_checks(contact_id, check_name, status)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_research_evidence_contact
        ON research_evidence(contact_id, fact_type, captured_at)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_sequence_state_touch
        ON sequence_state(touch_number, touch_eligible_date, delivery_status)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_message_strategies_contact
        ON message_strategies(contact_id, touch_number, channel)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_compliance_contact
        ON process_compliance_log(contact_id, sop_name, completed)
    """)
