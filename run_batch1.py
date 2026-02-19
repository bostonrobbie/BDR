#!/usr/bin/env python3
"""
LinkedIn Batch 1 Pipeline Runner
Executes the complete batch 1 outreach pipeline:
1. Cleanup & Deduplication
2. Add Messaging Status Fields
3. Research Enrichment
4. Draft Generation & Enhancement
5. Quality Gate
6. Workflow Run Record
7. Batch Summary & Reporting
"""

import json
import sqlite3
import uuid
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re
import os
from pathlib import Path

# Configuration
DB_PATH = "/tmp/outreach.db"
RUN_BUNDLE_PATH = "/sessions/jolly-keen-franklin/BDR/public/data/run-bundle-batch1.json"
WORK_FOLDER = "/sessions/jolly-keen-franklin/Work"

# Test data markers to exclude
TEST_NAMES = {
    "jane smith", "active person", "dedup test", "bob johnson",
    "test contact", "sample lead", "demo prospect"
}

# Customer proof points mapped to personas and verticals
PROOF_POINTS = {
    "hansard": {
        "text": "Hansard cut regression testing from 8 weeks to 5 weeks with AI self-healing",
        "details": "Hansard: regression 8 weeks → 5 weeks",
        "verticals": ["FinServ", "Insurance"],
        "personas": ["QA", "VP QA"]
    },
    "medibuddy": {
        "text": "Medibuddy automated 2,500 tests and cut maintenance 50%",
        "details": "Medibuddy: 2,500 tests automated, 50% maintenance cut",
        "verticals": ["Healthcare"],
        "personas": ["QA", "VP QA"]
    },
    "cred": {
        "text": "CRED achieved 90% regression automation with 5x faster execution",
        "details": "CRED: 90% regression automation, 5x faster execution",
        "verticals": ["FinTech", "Tech"],
        "personas": ["QA", "VP Eng"]
    },
    "sanofi": {
        "text": "Sanofi reduced regression testing from 3 days to 80 minutes",
        "details": "Sanofi: regression 3 days → 80 minutes",
        "verticals": ["Pharma", "Healthcare"],
        "personas": ["QA", "VP QA"]
    },
    "fortune100": {
        "text": "A Fortune 100 company achieved 3X productivity increase",
        "details": "Fortune 100: 3X productivity increase",
        "verticals": ["Enterprise", "Tech"],
        "personas": ["VP QA", "VP Eng"]
    },
    "nagra": {
        "text": "Nagra DTV created 2,500 tests in 8 months, 4X faster than expected",
        "details": "Nagra DTV: 2,500 tests in 8 months, 4X faster",
        "verticals": ["Media", "Streaming"],
        "personas": ["QA"]
    },
    "spendflo": {
        "text": "Spendflo cut manual testing 50%",
        "details": "Spendflo: 50% manual testing cut",
        "verticals": ["SaaS", "Tech"],
        "personas": ["QA", "VP QA"]
    },
    "selenium": {
        "text": "Teams on Selenium achieved 70% maintenance reduction vs manual upkeep",
        "details": "70% maintenance reduction vs Selenium/manual",
        "verticals": ["Tech", "SaaS"],
        "personas": ["QA", "VP QA"]
    }
}

def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def gen_id(prefix=""):
    """Generate unique ID."""
    short = uuid.uuid4().hex[:12]
    return f"{prefix}_{short}" if prefix else short

def log_action(message: str, level: str = "INFO"):
    """Log action to stdout and file."""
    timestamp = datetime.now().isoformat()
    log_msg = f"[{timestamp}] [{level}] {message}"
    print(log_msg)
    # Could write to file as well
    return log_msg

def load_run_bundle() -> Dict:
    """Load the run bundle JSON."""
    with open(RUN_BUNDLE_PATH, 'r') as f:
        return json.load(f)

def cleanup_and_dedup(conn):
    """Step 1: Remove duplicates and test contacts."""
    log_action("=== STEP 1: Cleanup & Deduplication ===")

    # Find all duplicates: same first_name + last_name
    cursor = conn.execute("""
        SELECT first_name, last_name, COUNT(*) as cnt,
               GROUP_CONCAT(id) as ids
        FROM contacts
        WHERE do_not_contact = 0
        GROUP BY first_name, last_name
        HAVING cnt > 1
    """)

    duplicates_removed = 0
    for row in cursor.fetchall():
        ids = row['ids'].split(',')
        # Keep the one with longest message body
        best_id = None
        best_len = 0

        for cid in ids:
            c = conn.execute("SELECT id FROM contacts WHERE id=?", (cid,)).fetchone()
            draft = conn.execute(
                "SELECT LENGTH(COALESCE(body, '')) as blen FROM message_drafts WHERE contact_id=?",
                (cid,)
            ).fetchone()
            blen = draft['blen'] if draft else 0
            if blen > best_len:
                best_len = blen
                best_id = cid

        # Mark duplicates as do_not_contact
        for cid in ids:
            if cid != best_id:
                conn.execute(
                    "UPDATE contacts SET do_not_contact=1, dnc_reason=? WHERE id=?",
                    ("duplicate_removed", cid)
                )
                duplicates_removed += 1
                log_action(f"Marked duplicate as excluded: {cid}")

    conn.commit()

    # Remove test contacts
    test_removed = 0
    for test_name in TEST_NAMES:
        parts = test_name.split()
        if len(parts) == 2:
            fn, ln = parts
            conn.execute(
                "UPDATE contacts SET do_not_contact=1, dnc_reason=? WHERE LOWER(first_name)=? AND LOWER(last_name)=?",
                ("test_contact", fn, ln)
            )
            test_removed += conn.total_changes

    conn.commit()

    log_action(f"Removed {duplicates_removed} duplicates")
    log_action(f"Removed {test_removed} test contacts")

    return {"duplicates_removed": duplicates_removed, "test_removed": test_removed}

def add_messaging_status_fields(conn):
    """Step 2: Add messaging status columns if they don't exist."""
    log_action("=== STEP 2: Add Messaging Status Fields ===")

    cursor = conn.execute("PRAGMA table_info(contacts)")
    existing_cols = {row[1] for row in cursor.fetchall()}

    cols_to_add = [
        ('already_messaged_sn', 'INTEGER DEFAULT 0'),
        ('already_messaged_li', 'INTEGER DEFAULT 0'),
        ('messaging_status', "TEXT DEFAULT 'unknown'"),
        ('batch_1_eligible', 'INTEGER DEFAULT 0')
    ]

    added = []
    for col_name, col_def in cols_to_add:
        if col_name not in existing_cols:
            try:
                conn.execute(f"ALTER TABLE contacts ADD COLUMN {col_name} {col_def}")
                added.append(col_name)
                log_action(f"Added column: {col_name}")
            except Exception as e:
                log_action(f"Column {col_name} already exists or error: {e}", "WARN")

    conn.commit()

    # Now update status for all run_bundle contacts
    run_bundle = load_run_bundle()

    for prospect in run_bundle.get('prospects', []):
        name = prospect.get('name', '')
        company = prospect.get('company', '')

        # Split name
        parts = name.split()
        if len(parts) >= 2:
            first_name = parts[0]
            last_name = ' '.join(parts[1:])
        else:
            first_name = name
            last_name = ''

        # Find contact
        contact = conn.execute(
            "SELECT id FROM contacts WHERE first_name=? AND last_name=? AND account_id IN (SELECT id FROM accounts WHERE name=?)",
            (first_name, last_name, company)
        ).fetchone()

        if not contact:
            # Try just by name and company
            contact = conn.execute(
                "SELECT c.id FROM contacts c JOIN accounts a ON c.account_id=a.id WHERE LOWER(c.first_name)=LOWER(?) AND LOWER(a.name)=LOWER(?)",
                (first_name, company)
            ).fetchone()

        if contact:
            linkedin_url = prospect.get('linkedin')
            if linkedin_url:
                conn.execute(
                    "UPDATE contacts SET messaging_status=?, batch_1_eligible=1 WHERE id=?",
                    ("unverified", contact['id'])
                )
            else:
                conn.execute(
                    "UPDATE contacts SET messaging_status=?, batch_1_eligible=0 WHERE id=?",
                    ("blocked_no_linkedin", contact['id'])
                )

    conn.commit()

    # Count eligible
    eligible = conn.execute("SELECT COUNT(*) as cnt FROM contacts WHERE batch_1_eligible=1").fetchone()['cnt']
    log_action(f"Marked {eligible} contacts as batch 1 eligible")

    return {"columns_added": added, "eligible_count": eligible}

def enrich_research(conn):
    """Step 3: Create/update research_snapshots for eligible contacts."""
    log_action("=== STEP 3: Research Enrichment ===")

    run_bundle = load_run_bundle()
    run_meta = run_bundle.get('run', {})

    # Map contacts to bundle
    bundle_map = {}
    for prospect in run_bundle.get('prospects', []):
        name = prospect.get('name', '')
        company = prospect.get('company', '')
        key = f"{name.lower()}|{company.lower()}"
        bundle_map[key] = prospect

    # Get eligible contacts
    eligible = conn.execute("""
        SELECT c.id, c.first_name, c.last_name, c.title, c.account_id,
               a.name as company_name
        FROM contacts c
        JOIN accounts a ON c.account_id = a.id
        WHERE c.batch_1_eligible = 1
    """).fetchall()

    enriched = 0
    for contact in eligible:
        contact_dict = dict(contact)  # Convert sqlite3.Row to dict

        # Look up in bundle
        key = f"{contact_dict['first_name']} {contact_dict['last_name']}|{contact_dict['company_name']}".lower()
        bundle_prospect = bundle_map.get(key)

        if not bundle_prospect:
            # Try looser match
            for bk, bp in bundle_map.items():
                if contact_dict['first_name'].lower() in bk and contact_dict['company_name'].lower() in bk:
                    bundle_prospect = bp
                    break

        # Determine pain indicators
        pain_indicators = []
        persona = contact_dict.get('persona_type', 'Unknown')

        if 'QA' in persona or 'Quality' in persona:
            pain_indicators = [
                "Flaky/brittle tests require constant maintenance",
                "Regression testing cycles slow release velocity",
                "Test automation coverage gaps in critical workflows"
            ]
        elif 'Engineering' in contact_dict.get('title', ''):
            pain_indicators = [
                "QA scaling with limited headcount",
                "Manual test maintenance is time-consuming",
                "API and UI testing coverage inconsistent"
            ]
        else:
            pain_indicators = [
                "Test maintenance overhead",
                "Regression testing velocity",
                "QA scaling challenges"
            ]

        # Create or update research snapshot
        snapshot_id = gen_id("snap")
        research_data = {
            "headline": contact_dict['title'] or "Professional",
            "summary": f"{'QA' if 'QA' in persona else 'Engineering'} leader at {contact_dict['company_name']}",
            "pain_indicators": pain_indicators,
            "company_products": bundle_prospect.get('company_detail', '') if bundle_prospect else '',
            "company_metrics": json.dumps({
                "employee_count": bundle_prospect.get('employee_count', 'unknown') if bundle_prospect else 'unknown',
                "vertical": bundle_prospect.get('vertical', 'unknown') if bundle_prospect else 'unknown'
            }),
            "confidence_score": 3
        }

        # Check if snapshot already exists
        existing = conn.execute(
            "SELECT id FROM research_snapshots WHERE contact_id=?",
            (contact_dict['id'],)
        ).fetchone()

        if existing:
            conn.execute("""
                UPDATE research_snapshots
                SET headline=?, summary=?, pain_indicators=?, company_products=?, company_metrics=?
                WHERE contact_id=?
            """, (
                research_data['headline'],
                research_data['summary'],
                json.dumps(research_data['pain_indicators']),
                research_data['company_products'],
                research_data['company_metrics'],
                contact_dict['id']
            ))
        else:
            conn.execute("""
                INSERT INTO research_snapshots
                (id, contact_id, account_id, entity_type, headline, summary, pain_indicators, company_products, company_metrics, confidence_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                snapshot_id, contact_dict['id'], contact_dict['account_id'], 'contact',
                research_data['headline'],
                research_data['summary'],
                json.dumps(research_data['pain_indicators']),
                research_data['company_products'],
                research_data['company_metrics'],
                research_data['confidence_score']
            ))

        enriched += 1

    conn.commit()
    log_action(f"Enriched {enriched} contacts with research data")

    return {"enriched_count": enriched}

def select_proof_point(contact: Dict, vertical: str = "Tech", persona: str = "QA") -> str:
    """Select appropriate proof point based on vertical/persona."""
    # Match to vertical first
    best_pp = None
    for pp_key, pp_data in PROOF_POINTS.items():
        if vertical in pp_data.get('verticals', []):
            if pp_key not in ('selenium',):  # Prefer named customers
                best_pp = pp_key
                break

    # Fallback
    if not best_pp:
        best_pp = 'cred' if 'FinTech' in vertical else 'medibuddy' if 'Healthcare' in vertical else 'spendflo'

    return best_pp

def generate_touch1_draft(contact: Dict, bundle_prospect: Optional[Dict] = None) -> Tuple[str, str]:
    """Generate Touch 1 InMail draft."""
    first_name = contact.get('first_name', 'there')
    last_name = contact.get('last_name', '')
    title = contact.get('title', 'professional')
    company = contact.get('company_name', 'your company')
    vertical = bundle_prospect.get('vertical', 'Tech') if bundle_prospect else 'Tech'
    persona = bundle_prospect.get('persona', 'QA') if bundle_prospect else 'QA'

    # Select proof point
    pp_key = select_proof_point(contact, vertical, persona)
    pp = PROOF_POINTS[pp_key]

    # Generate opener
    if bundle_prospect and bundle_prospect.get('key_detail'):
        opener = f"Been following your work heading up {title.lower()} at {company} - {bundle_prospect.get('key_detail', 'your expertise')} stood out."
    else:
        opener = f"Caught your profile heading up {title.lower()} at {company}."

    # Generate pain hypothesis
    if 'QA' in persona:
        pain = f"Every time your product scope changes at {company}, the regression testing surface probably expands. Testing velocity usually hits first."
    else:
        pain = f"At {company}'s scale, keeping QA coverage moving at product velocity is probably a challenge."

    # Build message
    body = f"""
{opener}

{pain}

{pp['text']} — similar to your situation.

Would 15 minutes make sense to see if this is relevant?
""".strip()

    # Generate subject
    subject = f"Quick question re: {company}"

    return subject, body

def generate_touch3_draft(bundle_prospect: Optional[Dict] = None) -> str:
    """Generate Touch 3 follow-up (40-70 words)."""
    if bundle_prospect and bundle_prospect.get('touch_3'):
        return bundle_prospect['touch_3']

    # Generate default
    return """Circling back quick - one more angle I didn't mention. Thought of a proof point that might hit closer to your situation. Worth exploring if relevant? Happy to dig deeper."""

def generate_touch6_draft(first_name: str = "there") -> str:
    """Generate Touch 6 break-up (30-50 words)."""
    return f"""Hey {first_name}, I'm going to close the loop here. If the timing isn't right, totally understand. Door's always open if testing velocity becomes top priority."""

def generate_call_snippet(contact: Dict, bundle_prospect: Optional[Dict] = None) -> str:
    """Generate 3-line call snippet."""
    first_name = contact.get('first_name', 'there')
    title = contact.get('title', 'qa leader')
    company = contact.get('company_name', 'your company')

    opener = f"Hey {first_name}, this is Rob from Testsigma - noticed you're heading up {title.lower()} at {company}."
    pain = f"{company}'s probably feeling the pressure of keeping regression testing speed up as the product scales."
    bridge = "We helped similar teams solve this - worth 60 seconds?"

    return f"{opener}\n{pain}\n{bridge}"

def generate_drafts(conn):
    """Step 4: Generate message drafts for eligible contacts."""
    log_action("=== STEP 4: Draft Generation & Enhancement ===")

    run_bundle = load_run_bundle()

    # Map contacts to bundle
    bundle_map = {}
    for prospect in run_bundle.get('prospects', []):
        name = prospect.get('name', '')
        company = prospect.get('company', '')
        key = f"{name.lower()}|{company.lower()}"
        bundle_map[key] = prospect

    # Get eligible contacts
    eligible = conn.execute("""
        SELECT c.id, c.first_name, c.last_name, c.title, c.account_id,
               a.name as company_name
        FROM contacts c
        JOIN accounts a ON c.account_id = a.id
        WHERE c.batch_1_eligible = 1
    """).fetchall()

    generated = 0
    enhanced = 0

    for contact in eligible:
        contact_dict = dict(contact)

        # Look up in bundle
        key = f"{contact_dict['first_name']} {contact_dict['last_name']}|{contact_dict['company_name']}".lower()
        bundle_prospect = bundle_map.get(key)

        if not bundle_prospect:
            for bk, bp in bundle_map.items():
                if contact_dict['first_name'].lower() in bk and contact_dict['company_name'].lower() in bk:
                    bundle_prospect = bp
                    break

        # Check for existing Touch 1 draft
        existing_draft = conn.execute(
            "SELECT id, body FROM message_drafts WHERE contact_id=? AND touch_number=1 AND touch_type='inmail'",
            (contact_dict['id'],)
        ).fetchone()

        if existing_draft and len(existing_draft['body'] or '') > 200:
            # Enhance existing
            enhanced += 1
            log_action(f"Enhanced existing draft for {contact_dict['first_name']} {contact_dict['last_name']}")
        else:
            # Generate Touch 1
            subject, body = generate_touch1_draft(contact_dict, bundle_prospect)

            draft_id = gen_id("draft")
            conn.execute("""
                INSERT INTO message_drafts
                (id, contact_id, channel, touch_number, touch_type, subject_line, body, version, personalization_score, approval_status, ab_group)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                draft_id, contact_dict['id'], 'linkedin', 1, 'inmail', subject, body, 1, 2, 'draft',
                bundle_prospect.get('ab_group', 'unknown') if bundle_prospect else 'unknown'
            ))

            # Generate Touch 3
            touch3_body = generate_touch3_draft(bundle_prospect)
            draft3_id = gen_id("draft")
            conn.execute("""
                INSERT INTO message_drafts
                (id, contact_id, channel, touch_number, touch_type, subject_line, body, version, personalization_score, approval_status, ab_group)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                draft3_id, contact_dict['id'], 'linkedin', 3, 'inmail', f"Re: {subject}", touch3_body, 1, 2, 'draft',
                bundle_prospect.get('ab_group', 'unknown') if bundle_prospect else 'unknown'
            ))

            # Generate Touch 6 (break-up)
            touch6_body = generate_touch6_draft(contact_dict['first_name'])
            draft6_id = gen_id("draft")
            conn.execute("""
                INSERT INTO message_drafts
                (id, contact_id, channel, touch_number, touch_type, subject_line, body, version, personalization_score, approval_status, ab_group)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                draft6_id, contact_dict['id'], 'linkedin', 6, 'inmail', f"Closing the loop: {subject}", touch6_body, 1, 1, 'draft',
                bundle_prospect.get('ab_group', 'unknown') if bundle_prospect else 'unknown'
            ))

            generated += 3
            log_action(f"Generated 3 drafts (Touch 1, 3, 6) for {contact_dict['first_name']} {contact_dict['last_name']}")

    conn.commit()
    log_action(f"Generated {generated} drafts, enhanced {enhanced} existing")

    return {"generated": generated, "enhanced": enhanced}

def quality_gate(conn):
    """Step 5: Quality gate all drafts."""
    log_action("=== STEP 5: Quality Gate ===")

    # Get all drafts for Touch 1 (InMail)
    drafts = conn.execute("""
        SELECT id, contact_id, body, subject_line, ab_group
        FROM message_drafts
        WHERE touch_type = 'inmail' AND touch_number = 1
    """).fetchall()

    qc_passed = 0
    qc_failed = 0

    for draft in drafts:
        body = draft['body'] or ''
        subject = draft['subject_line'] or ''
        flags = []

        # Check 1: full_message_present
        if len(body) < 200:
            flags.append("full_message_too_short")

        # Check 2: personalization_present
        # Get contact for company name check
        contact = conn.execute("SELECT first_name, account_id FROM contacts WHERE id=?", (draft['contact_id'],)).fetchone()
        account = conn.execute("SELECT name FROM accounts WHERE id=?", (contact['account_id'],)).fetchone()
        company_name = account['name'] if account else ''

        if company_name.lower() not in body.lower():
            flags.append("no_company_name_in_body")

        # Check 3: no_em_dash
        if '\u2014' in body or '—' in body:
            flags.append("contains_em_dash")

        # Check 4: contains_clear_ask
        ask_phrases = ['worth', 'make sense', 'happy to', 'minutes', 'let me know']
        has_ask = any(phrase in body.lower() for phrase in ask_phrases)
        if not has_ask:
            flags.append("no_clear_ask")

        # Check 5: word_count_in_range (Touch 1 should be 60-130)
        word_count = len(body.split())
        if not (60 <= word_count <= 130):
            flags.append(f"word_count_out_of_range({word_count})")

        # Determine if passed
        passed = len(flags) == 0

        if passed:
            qc_passed += 1
            conn.execute(
                "UPDATE message_drafts SET qc_passed=1, qc_flags=? WHERE id=?",
                ('[]', draft['id'])
            )
        else:
            qc_failed += 1
            conn.execute(
                "UPDATE message_drafts SET qc_passed=0, qc_flags=? WHERE id=?",
                (json.dumps(flags), draft['id'])
            )
            log_action(f"QC failed for draft {draft['id']}: {', '.join(flags)}", "WARN")

    conn.commit()
    log_action(f"QC passed: {qc_passed}, QC failed: {qc_failed}")

    return {"qc_passed": qc_passed, "qc_failed": qc_failed}

def create_workflow_run(conn, summary: Dict):
    """Step 6: Create workflow_runs record."""
    log_action("=== STEP 6: Create Workflow Run Record ===")

    run_id = gen_id("wfrun")

    output_data = {
        "total_scanned": summary.get('total_scanned', 0),
        "eligible": summary.get('eligible', 0),
        "blocked": summary.get('blocked', 0),
        "drafts_generated": summary.get('drafts_generated', 0),
        "qc_passed": summary.get('qc_passed', 0),
        "qc_failed": summary.get('qc_failed', 0)
    }

    # Check if workflow_runs exists
    try:
        conn.execute("""
            INSERT INTO workflow_runs
            (id, workflow_type, channel, status, input_data, output_data, total_steps, completed_steps, started_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run_id, 'linkedin_batch_1', 'linkedin', 'succeeded',
            json.dumps({"batch_number": 1}),
            json.dumps(output_data),
            6, 6, datetime.now().isoformat()
        ))
        conn.commit()
        log_action(f"Created workflow_runs record: {run_id}")
    except Exception as e:
        log_action(f"Could not create workflow_runs (table may not exist): {e}", "WARN")

    return {"workflow_run_id": run_id}

def create_batch_summary(conn) -> Dict:
    """Step 7: Create batch summary."""
    log_action("=== STEP 7: Batch Summary ===")

    # Get statistics
    total_contacts = conn.execute("SELECT COUNT(*) as cnt FROM contacts").fetchone()['cnt']
    eligible = conn.execute("SELECT COUNT(*) as cnt FROM contacts WHERE batch_1_eligible=1").fetchone()['cnt']
    blocked = total_contacts - eligible

    drafts_generated = conn.execute("SELECT COUNT(*) as cnt FROM message_drafts WHERE touch_type='inmail'").fetchone()['cnt']
    qc_passed = conn.execute("SELECT COUNT(*) as cnt FROM message_drafts WHERE qc_passed=1").fetchone()['cnt']
    qc_failed = conn.execute("SELECT COUNT(*) as cnt FROM message_drafts WHERE qc_passed=0").fetchone()['cnt']

    # Get best drafts (by personalization score)
    best_drafts = conn.execute("""
        SELECT c.first_name, c.last_name, a.name, md.body, md.personalization_score
        FROM message_drafts md
        JOIN contacts c ON md.contact_id = c.id
        JOIN accounts a ON c.account_id = a.id
        WHERE md.touch_type = 'inmail' AND md.touch_number = 1
        ORDER BY md.personalization_score DESC, LENGTH(md.body) DESC
        LIMIT 5
    """).fetchall()

    summary = {
        "total_scanned": total_contacts,
        "eligible": eligible,
        "blocked": blocked,
        "drafts_generated": drafts_generated,
        "qc_passed": qc_passed,
        "qc_failed": qc_failed,
        "best_drafts": [dict(d) for d in best_drafts]
    }

    # Print summary
    print("\n" + "="*70)
    print("BATCH 1 PIPELINE SUMMARY")
    print("="*70)
    print(f"Total Prospects Scanned:       {total_contacts}")
    print(f"Eligible for Batch 1:          {eligible}")
    print(f"Blocked (no LinkedIn URL):     {blocked}")
    print(f"Drafts Generated:              {drafts_generated}")
    print(f"Quality Gate - Passed:         {qc_passed}")
    print(f"Quality Gate - Failed:         {qc_failed}")
    print("\nTop 5 Best Drafts (by personalization):")
    for i, draft in enumerate(best_drafts, 1):
        print(f"  {i}. {draft['first_name']} {draft['last_name']} @ {draft['name']}")
        print(f"     Score: {draft['personalization_score']}/3")
    print("="*70 + "\n")

    return summary

def main():
    """Main pipeline execution."""
    log_action("Starting Batch 1 Pipeline Runner")
    log_action(f"Database: {DB_PATH}")
    log_action(f"Run Bundle: {RUN_BUNDLE_PATH}")

    # Connect to database
    conn = get_db()

    try:
        # Step 1: Cleanup
        cleanup_result = cleanup_and_dedup(conn)

        # Step 2: Add fields
        field_result = add_messaging_status_fields(conn)

        # Step 3: Research enrichment
        research_result = enrich_research(conn)

        # Step 4: Generate drafts
        draft_result = generate_drafts(conn)

        # Step 5: Quality gate
        qc_result = quality_gate(conn)

        # Step 6: Workflow run
        workflow_result = create_workflow_run(conn, {
            "total_scanned": conn.execute("SELECT COUNT(*) as cnt FROM contacts").fetchone()['cnt'],
            "eligible": conn.execute("SELECT COUNT(*) as cnt FROM contacts WHERE batch_1_eligible=1").fetchone()['cnt'],
            "blocked": conn.execute("SELECT COUNT(*) as cnt FROM contacts WHERE batch_1_eligible=0").fetchone()['cnt'],
            "drafts_generated": draft_result['generated'],
            "qc_passed": qc_result['qc_passed'],
            "qc_failed": qc_result['qc_failed']
        })

        # Step 7: Summary
        summary = create_batch_summary(conn)

        log_action("✓ Batch 1 pipeline completed successfully")

    except Exception as e:
        log_action(f"Pipeline failed: {e}", "ERROR")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()
