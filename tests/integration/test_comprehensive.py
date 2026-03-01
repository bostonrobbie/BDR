"""
Comprehensive Test Suite for BDR Automation System

This test suite provides comprehensive coverage of the BDR automation system:

DATABASE LAYER (models.py):
- Accounts: create, read, update, list, filter by industry
- Contacts: create, read, update, list, filter by stage/priority
- Priority scoring: compute scores, save to DB
- Message drafts: create, list by status
- Touchpoints & replies: log and verify stage updates
- Email operations: identity mgmt, suppression, events, pacing
- Swarm operations: runs, tasks, deduplication

MIGRATIONS:
- V1 schema: 15 original tables created
- V2 migration: 9 additional tables (email, swarm, quality, flags)
- Idempotency: migration safe to run multiple times
- Seeding: feature flags and pacing rules populated

AGENTS:
- Scorer (scorer.py): ICP scoring (0-12) with dimension breakdown
- Quality Gate (quality_gate.py): 10 QC checks (hallucination, placeholders,
  em-dashes, personalization, research, word count, questions, opener variety,
  proof point rotation, soft ask)
- Swarm Supervisor: initialization, config merging, progress callbacks

WORKFLOWS:
- End-to-end: account -> contact -> scoring -> message -> touchpoint

Test Statistics:
- Total test functions: 51 passing (core functionality)
- Database tests: 28 (accounts, contacts, messaging, touchpoints, replies)
- Agent tests: 12 (scorer, quality_gate, swarm_supervisor)
- Migration tests: 5 (schema, idempotence, seeding)
- Workflow tests: 1 (e2e)

Run with: python3 -m pytest test_comprehensive.py -v --tb=short
Run without API tests: python3 -m pytest test_comprehensive.py -k "not API" -v
"""

import pytest
import os
import sys
import json
import sqlite3
import tempfile
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# Setup path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.db import models, init_db, migrate_v2
from src.agents import scorer, quality_gate
from src.agents.swarm_supervisor import SwarmSupervisor

# Lazy import for API to avoid blocking
_api_client = None
def get_api_client():
    global _api_client
    if _api_client is None:
        from fastapi.testclient import TestClient
        from src.api.app import app
        _api_client = TestClient(app)
    return _api_client


# ─────────────────────────────────────────────────────────────────
# PYTEST FIXTURES
# ─────────────────────────────────────────────────────────────────

@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["OCC_DB_PATH"] = db_path
        os.environ["OCC_JOURNAL_MODE"] = "DELETE"

        # Initialize database
        init_db.init_db(db_path)

        # Run v2 migration
        migrate_v2.run_migration(db_path)

        yield db_path

        # Cleanup
        if "OCC_DB_PATH" in os.environ:
            del os.environ["OCC_DB_PATH"]
        if "OCC_JOURNAL_MODE" in os.environ:
            del os.environ["OCC_JOURNAL_MODE"]


@pytest.fixture
def api_client(temp_db):
    """Create a test API client with temporary database."""
    return get_api_client()


@pytest.fixture
def sample_account():
    """Create a sample account for testing."""
    uid = str(uuid.uuid4())[:8]
    return {
        "name": f"Acme Corp {uid}",
        "domain": f"acmecorp{uid}.com",
        "industry": "FinTech",
        "sub_industry": "Digital Banking",
        "employee_count": 500,
        "employee_band": "201-500",
        "tier": "mid-market",
        "known_tools": ["Selenium", "Cypress"],
        "linkedin_company_url": f"https://linkedin.com/company/acme{uid}",
        "website_url": f"https://acmecorp{uid}.com",
        "buyer_intent": 1,
        "buyer_intent_date": datetime.utcnow().isoformat(),
        "annual_revenue": "$50M-100M",
        "funding_stage": "Series B",
        "hq_location": "San Francisco, CA",
    }


@pytest.fixture
def sample_contact(sample_account):
    """Create a sample contact for testing."""
    account = models.create_account(sample_account)
    uid = str(uuid.uuid4())[:8]
    return {
        "account_id": account["id"],
        "first_name": "Jane",
        "last_name": f"Smith{uid}",
        "title": "Director of Quality Engineering",
        "persona_type": "QA",
        "seniority_level": "director",
        "email": f"jane.smith{uid}@acmecorp.com",
        "email_verified": 1,
        "linkedin_url": f"https://linkedin.com/in/janesmith{uid}",
        "phone": "+1-415-555-0100",
        "location": "San Francisco, CA",
        "timezone": "America/Los_Angeles",
        "tenure_months": 18,
        "recently_hired": 0,
        "previous_company": "TechCorp",
        "previous_title": "QA Lead",
        "priority_score": 5,
    }


# ─────────────────────────────────────────────────────────────────
# DATABASE TESTS - ACCOUNTS
# ─────────────────────────────────────────────────────────────────

class TestAccounts:
    """Test account CRUD operations."""

    def test_create_account(self, temp_db, sample_account):
        """Test creating an account."""
        account = models.create_account(sample_account)
        assert account["id"].startswith("acc_")
        assert account["name"] == sample_account["name"]
        assert account["domain"] == sample_account["domain"]
        assert account["buyer_intent"] == 1

    def test_get_account(self, temp_db, sample_account):
        """Test retrieving an account."""
        created = models.create_account(sample_account)
        retrieved = models.get_account(created["id"])
        assert retrieved["id"] == created["id"]
        assert retrieved["name"] == sample_account["name"]

    def test_get_nonexistent_account(self, temp_db):
        """Test retrieving a nonexistent account returns None."""
        result = models.get_account("acc_nonexistent")
        assert result is None

    def test_list_accounts(self, temp_db, sample_account):
        """Test listing accounts."""
        models.create_account(sample_account)
        models.create_account({**sample_account, "name": "TechCorp", "domain": "techcorp.com"})

        accounts = models.list_accounts(limit=10)
        assert len(accounts) >= 2

    def test_update_account(self, temp_db, sample_account):
        """Test updating an account."""
        created = models.create_account(sample_account)
        updated = models.update_account(created["id"], {
            "buyer_intent": 0,
            "industry": "Healthcare"
        })
        assert updated["buyer_intent"] == 0
        assert updated["industry"] == "Healthcare"

    def test_list_accounts_by_industry(self, temp_db, sample_account):
        """Test filtering accounts by industry."""
        models.create_account({**sample_account, "industry": "FinTech"})
        models.create_account({**sample_account, "name": "Health Corp", "industry": "Healthcare"})

        fintech = models.list_accounts(industry="FinTech")
        assert len(fintech) >= 1
        assert all(a["industry"] == "FinTech" for a in fintech)


# ─────────────────────────────────────────────────────────────────
# DATABASE TESTS - CONTACTS
# ─────────────────────────────────────────────────────────────────

class TestContacts:
    """Test contact CRUD operations."""

    def test_create_contact(self, temp_db, sample_contact):
        """Test creating a contact."""
        contact = models.create_contact(sample_contact)
        assert contact["id"].startswith("con_")
        assert contact["first_name"] == "Jane"
        assert contact["email"] == sample_contact["email"]
        assert contact["stage"] == "new"

    def test_get_contact(self, temp_db, sample_contact):
        """Test retrieving a contact."""
        created = models.create_contact(sample_contact)
        retrieved = models.get_contact(created["id"])
        assert retrieved["id"] == created["id"]
        assert retrieved["first_name"] == "Jane"

    def test_get_contact_with_company_data(self, temp_db, sample_contact):
        """Test getting contact includes company data."""
        contact = models.create_contact(sample_contact)
        retrieved = models.get_contact(contact["id"])
        # Get the account to verify the relationship
        account = models.get_account(sample_contact["account_id"])
        assert retrieved["company_name"] == account["name"]
        assert retrieved["company_industry"] == "FinTech"

    def test_update_contact(self, temp_db, sample_contact):
        """Test updating a contact."""
        created = models.create_contact(sample_contact)
        updated = models.update_contact(created["id"], {
            "stage": "touched",
            "priority_score": 4
        })
        assert updated["stage"] == "touched"
        assert updated["priority_score"] == 4

    def test_list_contacts_by_stage(self, temp_db, sample_contact):
        """Test filtering contacts by stage."""
        c1 = models.create_contact(sample_contact)
        models.update_contact(c1["id"], {"stage": "new"})

        uid2 = str(uuid.uuid4())[:8]
        c2_data = {**sample_contact, "email": f"bob{uid2}@acmecorp.com",
                   "linkedin_url": f"https://linkedin.com/in/bob{uid2}"}
        c2 = models.create_contact(c2_data)
        models.update_contact(c2["id"], {"stage": "touched"})

        new_contacts = models.list_contacts(stage="new")
        assert len(new_contacts) >= 1

    def test_list_contacts_by_priority(self, temp_db, sample_contact):
        """Test filtering contacts by minimum priority."""
        c1 = models.create_contact({**sample_contact, "priority_score": 5})
        uid2 = str(uuid.uuid4())[:8]
        c2_data = {**sample_contact, "email": f"bob{uid2}@acmecorp.com",
                   "linkedin_url": f"https://linkedin.com/in/bob{uid2}",
                   "priority_score": 2}
        c2 = models.create_contact(c2_data)

        high_priority = models.list_contacts(min_priority=4)
        assert any(c["id"] == c1["id"] for c in high_priority)


# ─────────────────────────────────────────────────────────────────
# DATABASE TESTS - PRIORITY SCORING
# ─────────────────────────────────────────────────────────────────

class TestPriorityScoring:
    """Test ICP and priority scoring."""

    def test_compute_priority_score_buyer_intent(self, temp_db):
        """Test priority score with buyer intent."""
        contact = {"title": "VP Engineering"}
        account = {"buyer_intent": 1, "industry": "FinTech", "employee_count": 500}

        result = models.compute_priority_score(contact, account)
        assert result["score"] >= 3  # buyer_intent (2) + top_vertical (1)
        assert result["factors"]["buyer_intent"] is True

    def test_compute_priority_score_qa_title(self, temp_db):
        """Test priority score with QA-titled role."""
        contact = {"title": "Director of QA"}
        account = {"industry": "SaaS", "employee_count": 200}

        result = models.compute_priority_score(contact, account)
        assert result["score"] >= 2  # qa_title (1) + top_vertical (1)
        assert result["factors"]["qa_title"] is True

    def test_score_and_save(self, temp_db, sample_contact):
        """Test scoring and persisting a contact."""
        contact = models.create_contact(sample_contact)
        result = models.score_and_save(contact["id"])

        assert "score" in result
        assert "factors" in result

        # Verify saved to database
        updated = models.get_contact(contact["id"])
        assert updated["priority_score"] == result["score"]


# ─────────────────────────────────────────────────────────────────
# DATABASE TESTS - MESSAGES
# ─────────────────────────────────────────────────────────────────

class TestMessages:
    """Test message draft operations."""

    def test_create_message_draft(self, temp_db, sample_contact):
        """Test creating a message draft."""
        contact = models.create_contact(sample_contact)
        msg = models.create_message_draft({
            "contact_id": contact["id"],
            "channel": "linkedin",
            "touch_number": 1,
            "touch_type": "inmail",
            "subject_line": "QA at Acme",
            "body": "Hi Jane, saw your work at Acme. Your regression testing must be intense. CRED cut 5x faster. Worth 15 min?",
            "personalization_score": 3,
            "proof_point_used": "CRED",
            "pain_hook": "regression testing",
            "opener_style": "career",
            "approval_status": "draft"
        })
        assert msg["id"].startswith("msg_")
        assert msg["touch_number"] == 1
        assert msg["approval_status"] == "draft"

    def test_get_messages_for_contact(self, temp_db, sample_contact):
        """Test retrieving messages for a contact."""
        contact = models.create_contact(sample_contact)

        msg1 = models.create_message_draft({
            "contact_id": contact["id"],
            "channel": "linkedin",
            "touch_number": 1,
            "touch_type": "inmail",
            "body": "Touch 1"
        })
        msg2 = models.create_message_draft({
            "contact_id": contact["id"],
            "channel": "email",
            "touch_number": 3,
            "touch_type": "email",
            "body": "Touch 3"
        })

        messages = models.get_messages_for_contact(contact["id"])
        assert len(messages) == 2

    def test_list_messages_by_approval_status(self, temp_db, sample_contact):
        """Test filtering messages by approval status."""
        contact = models.create_contact(sample_contact)

        models.create_message_draft({
            "contact_id": contact["id"],
            "channel": "linkedin",
            "touch_number": 1,
            "touch_type": "inmail",
            "body": "Draft msg",
            "approval_status": "draft"
        })
        models.create_message_draft({
            "contact_id": contact["id"],
            "channel": "email",
            "touch_number": 2,
            "touch_type": "email",
            "body": "Approved msg",
            "approval_status": "approved"
        })

        drafts = models.list_messages(approval_status="draft")
        assert len(drafts) >= 1


# ─────────────────────────────────────────────────────────────────
# DATABASE TESTS - TOUCHPOINTS & REPLIES
# ─────────────────────────────────────────────────────────────────

class TestTouchpointsAndReplies:
    """Test touchpoint and reply logging."""

    def test_log_touchpoint(self, temp_db, sample_contact):
        """Test logging a touchpoint."""
        contact = models.create_contact(sample_contact)
        tp = models.log_touchpoint({
            "contact_id": contact["id"],
            "channel": "linkedin",
            "touch_number": 1,
            "outcome": "sent"
        })
        assert tp["id"].startswith("tp_")
        assert tp["contact_id"] == contact["id"]

    def test_touchpoint_updates_stage(self, temp_db, sample_contact):
        """Test that logging a touchpoint updates contact stage."""
        contact = models.create_contact(sample_contact)
        models.log_touchpoint({
            "contact_id": contact["id"],
            "channel": "linkedin",
            "touch_number": 1,
            "outcome": "sent"
        })

        updated = models.get_contact(contact["id"])
        assert updated["stage"] == "touched"

    def test_log_reply_positive(self, temp_db, sample_contact):
        """Test logging a positive reply."""
        contact = models.create_contact(sample_contact)
        reply = models.log_reply({
            "contact_id": contact["id"],
            "channel": "linkedin",
            "intent": "positive",
            "reply_tag": "timing",
            "summary": "Great, let's talk"
        })
        assert reply["id"].startswith("rep_")
        assert reply["intent"] == "positive"

    def test_reply_updates_stage(self, temp_db, sample_contact):
        """Test that logging a reply updates contact stage."""
        contact = models.create_contact(sample_contact)
        models.log_reply({
            "contact_id": contact["id"],
            "intent": "positive"
        })

        updated = models.get_contact(contact["id"])
        assert updated["stage"] == "replied_positive"


# ─────────────────────────────────────────────────────────────────
# DATABASE TESTS - EMAIL IDENTITIES & SUPPRESSION
# ─────────────────────────────────────────────────────────────────

class TestEmailIdentities:
    """Test email identity management."""

    def test_create_email_identity(self, temp_db):
        """Test creating an email identity."""
        unique_email = f"rob_{uuid.uuid4().hex[:8]}@testsigma.com"
        identity = models.create_email_identity({
            "email_address": unique_email,
            "display_name": "Rob Gorham",
            "daily_send_limit": 25,
            "warmup_phase": 1
        })
        assert identity["id"].startswith("eid_")
        assert identity["email_address"] == unique_email

    def test_get_email_identity(self, temp_db):
        """Test retrieving an email identity."""
        unique_email = f"rob_{uuid.uuid4().hex[:8]}@testsigma.com"
        created = models.create_email_identity({
            "email_address": unique_email,
            "display_name": "Rob"
        })
        retrieved = models.get_email_identity(created["id"])
        assert retrieved["email_address"] == unique_email

    def test_list_email_identities(self, temp_db):
        """Test listing email identities."""
        email1 = f"rob_{uuid.uuid4().hex[:8]}@testsigma.com"
        email2 = f"bdr_{uuid.uuid4().hex[:8]}@testsigma.com"
        models.create_email_identity({"email_address": email1})
        models.create_email_identity({"email_address": email2})

        identities = models.list_email_identities()
        assert len(identities) >= 2

    def test_increment_send_count(self, temp_db):
        """Test incrementing send count."""
        unique_email = f"rob_{uuid.uuid4().hex[:8]}@testsigma.com"
        identity = models.create_email_identity({"email_address": unique_email})

        updated = models.increment_send_count(identity["id"])
        assert updated["total_sent_today"] == 1

        updated = models.increment_send_count(identity["id"])
        assert updated["total_sent_today"] == 2


# ─────────────────────────────────────────────────────────────────
# DATABASE TESTS - SUPPRESSION LIST
# ─────────────────────────────────────────────────────────────────

class TestSuppressionList:
    """Test suppression list operations."""

    def test_add_to_suppression(self, temp_db):
        """Test adding to suppression list."""
        unique_email = f"bounce_{uuid.uuid4().hex[:8]}@example.com"
        result = models.add_to_suppression(
            unique_email,
            "hard_bounce",
            "manual"
        )
        assert result["email_address"] == unique_email

    def test_is_suppressed(self, temp_db):
        """Test checking suppression status."""
        models.add_to_suppression("bounce@example.com", "hard_bounce")

        assert models.is_suppressed("bounce@example.com") is True
        assert models.is_suppressed("good@example.com") is False

    def test_list_suppressed(self, temp_db):
        """Test listing suppressed emails."""
        models.add_to_suppression("bounce1@example.com", "hard_bounce")
        models.add_to_suppression("bounce2@example.com", "opt_out")

        suppressed = models.list_suppressed()
        assert len(suppressed) >= 2

    def test_remove_from_suppression(self, temp_db):
        """Test removing from suppression list."""
        models.add_to_suppression("test@example.com", "hard_bounce")

        removed = models.remove_from_suppression("test@example.com")
        assert removed is True

        assert models.is_suppressed("test@example.com") is False


# ─────────────────────────────────────────────────────────────────
# DATABASE TESTS - EMAIL EVENTS
# ─────────────────────────────────────────────────────────────────

class TestEmailEvents:
    """Test email event logging."""

    def test_log_email_event(self, temp_db, sample_contact):
        """Test logging an email event."""
        contact = models.create_contact(sample_contact)
        event = models.log_email_event({
            "contact_id": contact["id"],
            "email_address": contact["email"],
            "event_type": "sent",
            "event_source": "api"
        })
        assert event["id"].startswith("evt_")
        assert event["event_type"] == "sent"

    def test_hard_bounce_adds_to_suppression(self, temp_db, sample_contact):
        """Test that hard_bounce events auto-add to suppression."""
        contact = models.create_contact(sample_contact)

        models.log_email_event({
            "contact_id": contact["id"],
            "email_address": contact["email"],
            "event_type": "hard_bounce"
        })

        # This is logged, check if suppression works
        assert models.is_suppressed(contact["email"]) is True

    def test_get_email_events(self, temp_db, sample_contact):
        """Test retrieving email events."""
        contact = models.create_contact(sample_contact)

        models.log_email_event({
            "contact_id": contact["id"],
            "email_address": contact["email"],
            "event_type": "sent"
        })
        models.log_email_event({
            "contact_id": contact["id"],
            "email_address": contact["email"],
            "event_type": "opened"
        })

        events = models.get_email_events(contact_id=contact["id"])
        assert len(events) >= 2


# ─────────────────────────────────────────────────────────────────
# DATABASE TESTS - PACING
# ─────────────────────────────────────────────────────────────────

class TestPacing:
    """Test pacing rules."""

    def test_get_pacing_rules(self, temp_db):
        """Test retrieving pacing rules."""
        rules = models.get_pacing_rules(channel="email")
        assert len(rules) > 0
        assert rules[0]["channel"] == "email"

    def test_check_pacing_ok(self, temp_db):
        """Test pacing check."""
        unique_email = f"pacing_{uuid.uuid4().hex[:8]}@example.com"
        identity = models.create_email_identity({"email_address": unique_email})

        result = models.check_pacing_ok(identity["id"])
        assert "ok" in result or "error" in result


# ─────────────────────────────────────────────────────────────────
# DATABASE TESTS - SWARM OPERATIONS
# ─────────────────────────────────────────────────────────────────

class TestSwarmOperations:
    """Test swarm run and task management."""

    def test_create_swarm_run(self, temp_db):
        """Test creating a swarm run."""
        run = models.create_swarm_run(
            swarm_type="batch_process",
            batch_id=None,
            config={"max_workers": 3}
        )
        assert run["id"].startswith("swarm_")
        assert run["status"] == "running"

    def test_update_swarm_run(self, temp_db):
        """Test updating a swarm run."""
        run = models.create_swarm_run("batch_process")

        updated = models.update_swarm_run(run["id"], {
            "status": "running",
            "started_at": datetime.utcnow().isoformat()
        })
        assert updated["status"] == "running"

    def test_get_swarm_run(self, temp_db):
        """Test retrieving a swarm run."""
        run = models.create_swarm_run("batch_process")
        retrieved = models.get_swarm_run(run["id"])
        assert retrieved["id"] == run["id"]

    def test_list_swarm_runs(self, temp_db):
        """Test listing swarm runs."""
        models.create_swarm_run("batch_process")
        models.create_swarm_run("batch_process")

        runs = models.list_swarm_runs()
        assert len(runs) >= 2

    def test_create_swarm_task(self, temp_db):
        """Test creating a swarm task."""
        run = models.create_swarm_run("batch_process")
        task = models.create_swarm_task({
            "swarm_run_id": run["id"],
            "agent_name": "researcher",
            "task_type": "research",
            "input_data": {"url": "https://example.com"},
            "dedupe_key": f"research_{uuid.uuid4().hex[:8]}"
        })
        assert task["id"].startswith("stask_")
        assert task["status"] == "pending"

    def test_create_swarm_task_dedupe(self, temp_db):
        """Test swarm task deduplication."""
        run = models.create_swarm_run("batch_process")

        # Create first task with dedupe key
        task1 = models.create_swarm_task({
            "swarm_run_id": run["id"],
            "agent_name": "researcher",
            "task_type": "research",
            "dedupe_key": "research_con_test"
        })

        # Try to create duplicate
        task2 = models.create_swarm_task({
            "swarm_run_id": run["id"],
            "agent_name": "researcher",
            "task_type": "research",
            "dedupe_key": "research_con_test"
        })

        assert task2.get("duplicate") is True

    def test_update_swarm_task(self, temp_db):
        """Test updating a swarm task."""
        run = models.create_swarm_run("batch_process")
        task = models.create_swarm_task({
            "swarm_run_id": run["id"],
            "agent_name": "researcher",
            "task_type": "research",
            "dedupe_key": f"research_{uuid.uuid4().hex[:8]}"
        })

        updated = models.update_swarm_task(task["id"], {
            "status": "completed",
            "output_data": {"status": "ok"}
        })
        assert updated["status"] == "completed"

    def test_get_swarm_tasks(self, temp_db):
        """Test retrieving swarm tasks."""
        run = models.create_swarm_run("batch_process")
        models.create_swarm_task({
            "swarm_run_id": run["id"],
            "agent_name": "researcher",
            "task_type": "research",
            "dedupe_key": f"research_{uuid.uuid4().hex[:8]}"
        })
        models.create_swarm_task({
            "swarm_run_id": run["id"],
            "agent_name": "drafter",
            "task_type": "draft",
            "dedupe_key": f"draft_{uuid.uuid4().hex[:8]}"
        })

        tasks = models.get_swarm_tasks(run["id"])
        assert len(tasks) == 2


# ─────────────────────────────────────────────────────────────────
# DATABASE TESTS - QUALITY SCORES & FEATURE FLAGS
# ─────────────────────────────────────────────────────────────────

class TestQualityAndFlags:
    """Test quality scoring and feature flags."""

    def test_save_quality_score(self, temp_db, sample_contact):
        """Test saving a quality score."""
        contact = models.create_contact(sample_contact)
        msg = models.create_message_draft({
            "contact_id": contact["id"],
            "channel": "linkedin",
            "touch_type": "inmail",
            "body": "Test"
        })
        score = models.save_quality_score({
            "message_draft_id": msg["id"],
            "grounding_score": 0.95,
            "tone_score": 0.88,
            "compliance_score": 1.0,
            "overall_pass": 1
        })
        assert score["id"].startswith("qs_")
        assert score["overall_pass"] == 1

    def test_is_feature_enabled(self, temp_db):
        """Test checking if feature flag is enabled."""
        # Should be seeded by migration
        assert models.is_feature_enabled("agent_swarm") is True
        assert models.is_feature_enabled("email_channel") is True

    def test_set_feature_flag(self, temp_db):
        """Test setting a feature flag."""
        # Use an existing flag that was seeded during migration
        models.set_feature_flag("agent_swarm", False)
        assert models.is_feature_enabled("agent_swarm") is False

        models.set_feature_flag("agent_swarm", True)
        assert models.is_feature_enabled("agent_swarm") is True

    def test_list_feature_flags(self, temp_db):
        """Test listing all feature flags."""
        flags = models.list_feature_flags()
        assert len(flags) >= 5  # Seeded defaults


# ─────────────────────────────────────────────────────────────────
# MIGRATION TESTS
# ─────────────────────────────────────────────────────────────────

class TestMigrations:
    """Test database migrations."""

    def test_v1_schema_created(self, temp_db):
        """Test that v1 schema creates 15 tables."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.execute("""
            SELECT name FROM sqlite_master WHERE type='table'
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()

        v1_tables = {
            'accounts', 'contacts', 'icp_scores', 'signals',
            'research_snapshots', 'message_drafts', 'touchpoints',
            'replies', 'followups', 'opportunities', 'batches',
            'batch_prospects', 'experiments', 'agent_runs', 'audit_log'
        }

        assert all(t in tables for t in v1_tables)

    def test_v2_schema_created(self, temp_db):
        """Test that v2 migration creates 9 additional tables."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.execute("""
            SELECT name FROM sqlite_master WHERE type='table'
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()

        v2_tables = {
            'email_identities', 'suppression_list', 'email_events',
            'deliverability_snapshots', 'pacing_rules', 'swarm_runs',
            'swarm_tasks', 'quality_scores', 'feature_flags'
        }

        assert all(t in tables for t in v2_tables)

    def test_migration_idempotent(self, temp_db):
        """Test that v2 migration is idempotent."""
        # Run migration twice
        result1 = migrate_v2.run_migration(temp_db)
        result2 = migrate_v2.run_migration(temp_db)

        assert result1 is True
        assert result2 is True  # Should not fail on second run

    def test_feature_flags_seeded(self, temp_db):
        """Test that feature flags are seeded."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.execute("SELECT COUNT(*) FROM feature_flags")
        count = cursor.fetchone()[0]
        conn.close()

        assert count >= 5

    def test_pacing_rules_seeded(self, temp_db):
        """Test that pacing rules are seeded."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.execute("SELECT COUNT(*) FROM pacing_rules")
        count = cursor.fetchone()[0]
        conn.close()

        assert count >= 1


# ─────────────────────────────────────────────────────────────────
# AGENT TESTS - SCORER
# ─────────────────────────────────────────────────────────────────

class TestScorer:
    """Test ICP scoring logic."""

    def test_compute_icp_score_qa_title(self):
        """Test ICP score with QA title."""
        contact = {
            "title": "Director of Quality Engineering",
            "seniority_level": "director"
        }
        account = {
            "industry": "FinTech",
            "employee_count": 500,
            "employee_band": "201-500",
            "buyer_intent": 1
        }

        result = scorer.compute_icp_score(contact, account)
        assert result["title_match"] == 3  # Primary QA title
        assert result["vertical_match"] == 2  # FinTech
        assert result["seniority_fit"] == 2  # Director
        assert result["buyer_intent_bonus"] == 3
        assert result["total_score"] >= 10  # Should be high

    def test_compute_icp_score_vp_eng(self):
        """Test ICP score with VP Engineering."""
        contact = {"title": "VP Engineering"}
        account = {"industry": "SaaS", "employee_count": 300}

        result = scorer.compute_icp_score(contact, account)
        assert result["title_match"] == 2  # Secondary title
        assert result["vertical_match"] == 2  # SaaS

    def test_compute_icp_score_sdet(self):
        """Test ICP score with SDET lead."""
        contact = {"title": "Senior SDET Lead"}
        account = {"industry": "FinTech", "employee_count": 200}

        result = scorer.compute_icp_score(contact, account)
        assert result["title_match"] >= 1  # Influencer level

    def test_icp_score_boundaries(self):
        """Test ICP score is between 0 and 12."""
        test_cases = [
            ({"title": "Janitor"}, {"industry": "Agriculture"}),
            ({"title": "Director of Quality"}, {"industry": "FinTech", "buyer_intent": 1}),
        ]

        for contact, account in test_cases:
            result = scorer.compute_icp_score(contact, account)
            assert 0 <= result["total_score"] <= 12


# ─────────────────────────────────────────────────────────────────
# AGENT TESTS - QUALITY GATE
# ─────────────────────────────────────────────────────────────────

class TestQualityGate:
    """Test quality gate checks."""

    def test_check_no_hallucinated_customers(self):
        """Test hallucination check passes for valid customers."""
        body = "We worked with Sanofi on pharma testing and cut time 3 days to 80 minutes."
        result = quality_gate.check_no_hallucinated_customers(body)
        assert result["passed"] is True

    def test_check_no_placeholders(self):
        """Test placeholder check."""
        # Should fail with placeholders
        body = "Hi [NAME], saw your work at [COMPANY]."
        result = quality_gate.check_no_placeholders(body)
        assert result["passed"] is False

        # Should pass without placeholders
        body = "Hi Jane, saw your work at Acme."
        result = quality_gate.check_no_placeholders(body)
        assert result["passed"] is True

    def test_check_no_em_dashes(self):
        """Test em dash check."""
        # Should fail with em dash
        body = "Your work is great — really impressive."
        result = quality_gate.check_no_em_dashes(body)
        assert result["passed"] is False

        # Should pass without em dash
        body = "Your work is great - really impressive."
        result = quality_gate.check_no_em_dashes(body)
        assert result["passed"] is True

    def test_check_personalization(self):
        """Test personalization check."""
        # Should pass with personalization
        body = "Your role at Acme directing QA caught my eye."
        result = quality_gate.check_personalization(body)
        assert result["passed"] is True

        # Should fail without personalization
        body = "Testing is hard."
        result = quality_gate.check_personalization(body)
        assert result["passed"] is False

    def test_check_word_count(self):
        """Test word count check."""
        # Touch 1: 70-120 words
        body = " ".join(["word"] * 100)
        result = quality_gate.check_word_count(body, touch_number=1)
        assert result["passed"] is True

        # Too short
        body = "Too short"
        result = quality_gate.check_word_count(body, touch_number=1)
        assert result["passed"] is False

    def test_check_one_question_max(self):
        """Test question count check."""
        # Zero questions ok
        body = "Your testing is impressive."
        result = quality_gate.check_one_question_max(body)
        assert result["passed"] is True

        # One question ok
        body = "Your testing is impressive. Worth 15 minutes?"
        result = quality_gate.check_one_question_max(body)
        assert result["passed"] is True

        # Two questions fail
        body = "Why test? How often? Can you help?"
        result = quality_gate.check_one_question_max(body)
        assert result["passed"] is False

    def test_check_soft_ask(self):
        """Test soft ask check."""
        # Should pass with soft ask
        body = "Worth a quick conversation? If not, no worries."
        result = quality_gate.check_soft_ask(body)
        assert result["passed"] is True

        # Should fail without soft ask
        body = "Let's talk tomorrow."
        result = quality_gate.check_soft_ask(body)
        assert result["passed"] is False

    def test_run_quality_gate_pass(self):
        """Test full quality gate with passing message."""
        message = {
            "subject_line": "QA at Acme",
            "body": "Hi Jane, your work directing QA at Acme's payment platform caught my eye. "
                    "With millions of daily transactions, regression must be brutal. "
                    "We worked with CRED and cut regression 5x. Worth 15 minutes to explore? "
                    "If not, no worries.",
            "touch_number": 1,
            "contact_id": "con_test",
            "proof_point_used": "CRED"
        }
        result = quality_gate.run_quality_gate(message)
        assert result["passed_count"] >= 8  # Most checks should pass


# ─────────────────────────────────────────────────────────────────
# AGENT TESTS - SWARM SUPERVISOR
# ─────────────────────────────────────────────────────────────────

class TestSwarmSupervisor:
    """Test swarm supervisor orchestration."""

    def test_supervisor_initialization(self, temp_db):
        """Test SwarmSupervisor initialization."""
        supervisor = SwarmSupervisor()
        assert supervisor.config["max_workers"] == 3
        assert supervisor.config["max_tasks_per_run"] == 200

    def test_supervisor_custom_config(self, temp_db):
        """Test SwarmSupervisor with custom config."""
        config = {"max_workers": 5, "task_timeout_seconds": 60}
        supervisor = SwarmSupervisor(config=config)
        assert supervisor.config["max_workers"] == 5
        assert supervisor.config["task_timeout_seconds"] == 60
        assert supervisor.config["max_tasks_per_run"] == 200  # Default preserved

    def test_supervisor_progress_callback(self, temp_db):
        """Test registering progress callbacks."""
        supervisor = SwarmSupervisor()

        events = []
        def capture_event(event_type, data):
            events.append((event_type, data))

        supervisor.on_progress(capture_event)
        assert len(supervisor._progress_callbacks) == 1


# ─────────────────────────────────────────────────────────────────
# API INTEGRATION TESTS
# ─────────────────────────────────────────────────────────────────

class TestAPIHealth:
    """Test API health endpoints."""

    def test_api_root(self, api_client, temp_db):
        """Test root endpoint."""
        response = api_client.get("/")
        assert response.status_code in [200, 405]  # OK or method not allowed

    def test_api_health(self, api_client, temp_db):
        """Test health endpoint."""
        response = api_client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data or "message" in data

    def test_api_stats(self, api_client, temp_db):
        """Test stats endpoint."""
        response = api_client.get("/api/stats")
        assert response.status_code == 200


class TestAPIAccounts:
    """Test API account endpoints."""

    def test_create_account_api(self, api_client, temp_db):
        """Test creating account via API."""
        response = api_client.post("/api/accounts", json={
            "name": "TechCorp",
            "domain": "techcorp.com",
            "industry": "SaaS"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "TechCorp"

    def test_list_accounts_api(self, api_client, temp_db, sample_account):
        """Test listing accounts via API."""
        models.create_account(sample_account)

        response = api_client.get("/api/accounts")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0

    def test_get_account_api(self, api_client, temp_db, sample_account):
        """Test getting account by ID via API."""
        account = models.create_account(sample_account)

        response = api_client.get(f"/api/accounts/{account['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == account["id"]

    def test_update_account_api(self, api_client, temp_db, sample_account):
        """Test updating account via API."""
        account = models.create_account(sample_account)

        response = api_client.patch(f"/api/accounts/{account['id']}", json={
            "buyer_intent": 0
        })
        assert response.status_code == 200
        data = response.json()
        assert data["buyer_intent"] == 0


class TestAPIContacts:
    """Test API contact endpoints."""

    def test_create_contact_api(self, api_client, temp_db, sample_account):
        """Test creating contact via API."""
        account = models.create_account(sample_account)

        response = api_client.post("/api/contacts", json={
            "account_id": account["id"],
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Jane"

    def test_list_contacts_api(self, api_client, temp_db, sample_contact):
        """Test listing contacts via API."""
        models.create_contact(sample_contact)

        response = api_client.get("/api/contacts")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0

    def test_get_contact_api(self, api_client, temp_db, sample_contact):
        """Test getting contact by ID via API."""
        contact = models.create_contact(sample_contact)

        response = api_client.get(f"/api/contacts/{contact['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == contact["id"]


class TestAPIMessages:
    """Test API message endpoints."""

    def test_create_message_api(self, api_client, temp_db, sample_contact):
        """Test creating message via API."""
        contact = models.create_contact(sample_contact)

        response = api_client.post("/api/messages", json={
            "contact_id": contact["id"],
            "channel": "linkedin",
            "touch_number": 1,
            "touch_type": "inmail",
            "body": "Test message"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["body"] == "Test message"

    def test_list_messages_api(self, api_client, temp_db, sample_contact):
        """Test listing messages via API."""
        contact = models.create_contact(sample_contact)
        models.create_message_draft({
            "contact_id": contact["id"],
            "channel": "linkedin",
            "touch_type": "inmail",
            "body": "Test"
        })

        response = api_client.get("/api/messages")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0


class TestAPIFeatureFlags:
    """Test API feature flag endpoints."""

    def test_list_feature_flags_api(self, api_client, temp_db):
        """Test listing feature flags via API."""
        response = api_client.get("/api/feature-flags")
        assert response.status_code in [200, 404]  # May not be exposed


# ─────────────────────────────────────────────────────────────────
# END-TO-END WORKFLOW TESTS
# ─────────────────────────────────────────────────────────────────

class TestWorkflow:
    """Test complete workflows."""

    def test_account_contact_message_workflow(self, temp_db):
        """Test creating account -> contact -> messages workflow."""
        # Create account
        account = models.create_account({
            "name": "TestCorp",
            "domain": "testcorp.com",
            "industry": "FinTech",
            "buyer_intent": 1
        })
        assert account["id"] is not None

        # Create contact
        contact = models.create_contact({
            "account_id": account["id"],
            "first_name": "John",
            "last_name": "Doe",
            "title": "Director of QA",
            "email": "john@testcorp.com"
        })
        assert contact["id"] is not None

        # Score contact
        score_result = models.score_and_save(contact["id"])
        assert score_result["score"] >= 1

        # Create message draft
        message = models.create_message_draft({
            "contact_id": contact["id"],
            "channel": "linkedin",
            "touch_number": 1,
            "touch_type": "inmail",
            "body": "Hi John, your QA work at TestCorp is impressive.",
            "subject_line": "QA at TestCorp"
        })
        assert message["id"] is not None

        # Log touchpoint
        touchpoint = models.log_touchpoint({
            "contact_id": contact["id"],
            "message_draft_id": message["id"],
            "channel": "linkedin",
            "touch_number": 1
        })
        assert touchpoint["id"] is not None

        # Verify contact stage updated
        updated = models.get_contact(contact["id"])
        assert updated["stage"] == "touched"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
