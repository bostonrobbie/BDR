-- BDR Analytics DB Schema v1.0 — Created Mar 15, 2026
-- USAGE: python3 -c "import sqlite3; conn=sqlite3.connect('/tmp/bdr_outreach.db'); conn.executescript(open('analytics/db_init.sql').read()); conn.commit(); conn.close()"
-- NOTE: SQLite cannot run on OneDrive-mounted paths (file locking limitation).
-- Skills that need the DB must build it at /tmp/bdr_outreach.db using this schema + CSV sources.

CREATE TABLE IF NOT EXISTS outreach_sends (
    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, norm_name TEXT,
    company TEXT, email TEXT, title TEXT, persona TEXT, vertical TEXT,
    batch TEXT, sequence TEXT, send_date TEXT, channel TEXT, touch_number INTEGER DEFAULT 1,
    subject_line TEXT, proof_point TEXT, word_count INTEGER, mqs_score INTEGER,
    status TEXT DEFAULT 'sent', replied INTEGER DEFAULT 0, reply_date TEXT,
    reply_sentiment TEXT, bounced INTEGER DEFAULT 0, unsubscribed INTEGER DEFAULT 0,
    source_file TEXT, created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS call_activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL UNIQUE,
    dials INTEGER DEFAULT 0, connects INTEGER DEFAULT 0, connect_rate REAL,
    positives INTEGER DEFAULT 0, win_rate REAL, voicemails INTEGER DEFAULT 0,
    callbacks INTEGER DEFAULT 0, notes TEXT, created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS weekly_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT, week_start TEXT NOT NULL UNIQUE,
    total_sends INTEGER DEFAULT 0, linkedin_sends INTEGER DEFAULT 0, email_sends INTEGER DEFAULT 0,
    total_replies INTEGER DEFAULT 0, reply_rate REAL, positive_replies INTEGER DEFAULT 0,
    meetings_booked INTEGER DEFAULT 0, total_dials INTEGER DEFAULT 0,
    total_connects INTEGER DEFAULT 0, call_connect_rate REAL, call_positives INTEGER DEFAULT 0,
    call_win_rate REAL, top_persona TEXT, top_vertical TEXT, notes TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS warm_leads_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, company TEXT, title TEXT,
    persona TEXT, vertical TEXT, priority TEXT, status TEXT,
    first_contact TEXT, last_contact TEXT, reply_date TEXT, reply_text TEXT,
    reply_sentiment TEXT, meeting_date TEXT, meeting_outcome TEXT, pipeline_stage TEXT,
    notes TEXT, created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS subject_line_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT, subject_line TEXT NOT NULL,
    formula_type TEXT, persona TEXT, vertical TEXT, send_count INTEGER DEFAULT 0,
    reply_count INTEGER DEFAULT 0, reply_rate REAL, positive_reply_count INTEGER DEFAULT 0,
    bounce_count INTEGER DEFAULT 0, first_seen TEXT, last_seen TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS trigger_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT, company TEXT NOT NULL, domain TEXT,
    event_type TEXT, event_detail TEXT, event_date TEXT, signal_strength TEXT DEFAULT 'medium',
    acted_on INTEGER DEFAULT 0, notes TEXT, created_at TEXT DEFAULT (datetime('now'))
);
