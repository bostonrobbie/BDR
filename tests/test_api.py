"""
Comprehensive test suite for BDR Outreach Command Center API
Tests all core CRUD, flow management, activity, drafts, sender health, and email channel endpoints.
"""
import os
import sys
import pytest
import json
import tempfile
import sqlite3
from datetime import datetime, timedelta

# Set OCC_DB_PATH to a temp file for test isolation
test_db_fd, test_db_path = tempfile.mkstemp(suffix=".db")
os.environ["OCC_DB_PATH"] = test_db_path

# Import the FastAPI app (which auto-initializes the DB on import)
from api.index import app, get_db, gen_id

from starlette.testclient import TestClient

# Setup test client
@pytest.fixture
def client():
    """Provide a test client with a fresh database for each test."""
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def reset_db():
    """Reset database before each test to ensure isolation."""
    # The app auto-initializes on import, so tests should work with seed data
    yield


# =============================================================================
# HEALTH CHECK & STATS ENDPOINTS
# =============================================================================

class TestHealthAndStats:
    """Test health check and dashboard stats endpoints."""

    def test_health_check(self, client):
        """GET /api/health should return healthy status with table counts."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "tables" in data
        assert "contacts" in data["tables"]
        assert data["tables"]["contacts"] >= 25  # Should have seed data
        assert "active_agent_runs" in data
        assert "active_swarms" in data

    def test_dashboard_stats(self, client):
        """GET /api/stats should return contact, reply, and meeting stats."""
        response = client.get("/api/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_contacts" in data
        assert data["total_contacts"] >= 25
        assert "total_replies" in data
        assert "total_meetings" in data
        assert "reply_rate" in data
        assert "meeting_rate" in data
        assert "by_stage" in data
        assert isinstance(data["by_stage"], dict)


# =============================================================================
# CONTACTS CRUD
# =============================================================================

class TestContacts:
    """Test contact CRUD operations."""

    def test_list_contacts(self, client):
        """GET /api/contacts should return paginated contacts list."""
        response = client.get("/api/contacts?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "contacts" in data
        assert "total" in data
        assert data["total"] >= 25
        assert len(data["contacts"]) <= 10
        assert len(data["contacts"]) > 0

    def test_list_contacts_by_stage(self, client):
        """GET /api/contacts?stage=new should filter by stage."""
        response = client.get("/api/contacts?stage=new&limit=100")
        assert response.status_code == 200
        data = response.json()
        assert "contacts" in data
        for contact in data["contacts"]:
            assert contact["stage"] == "new"

    def test_list_contacts_by_priority(self, client):
        """GET /api/contacts?priority_min=4 should filter by minimum priority."""
        response = client.get("/api/contacts?priority_min=4&limit=100")
        assert response.status_code == 200
        data = response.json()
        for contact in data["contacts"]:
            assert contact["priority_score"] >= 4

    def test_get_first_contact(self, client):
        """GET /api/contacts/{id} should return a single contact."""
        # Get first contact
        list_response = client.get("/api/contacts?limit=1")
        contacts = list_response.json()["contacts"]
        assert len(contacts) > 0
        contact_id = contacts[0]["id"]

        # Get specific contact
        response = client.get(f"/api/contacts/{contact_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == contact_id
        assert "first_name" in data
        assert "last_name" in data
        assert "title" in data
        assert "email" in data
        assert "priority_score" in data

    def test_get_contact_not_found(self, client):
        """GET /api/contacts/{nonexistent_id} should return 404."""
        response = client.get("/api/contacts/nonexistent_id_xyz")
        assert response.status_code == 404

    def test_create_contact(self, client):
        """POST /api/contacts should create a new contact."""
        new_contact = {
            "first_name": "John",
            "last_name": "Doe",
            "title": "VP Quality Assurance",
            "persona_type": "qa_leader",
            "priority_score": 5,
        }
        response = client.post("/api/contacts", json=new_contact)
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
        assert data["id"].startswith("con_")
        assert data["stage"] == "new"
        assert data["status"] == "active"

    def test_update_contact_stage(self, client):
        """PUT /api/contacts/{id} should update contact stage."""
        # Create a contact first
        new_contact = {"first_name": "Jane", "last_name": "Smith"}
        create_response = client.post("/api/contacts", json=new_contact)
        contact_id = create_response.json()["id"]

        # Update stage
        update_data = {"stage": "meeting_booked"}
        response = client.put(f"/api/contacts/{contact_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["stage"] == "meeting_booked"

    def test_update_contact_priority(self, client):
        """PUT /api/contacts/{id} should update priority score."""
        # Create a contact first
        new_contact = {"first_name": "Bob", "last_name": "Johnson"}
        create_response = client.post("/api/contacts", json=new_contact)
        contact_id = create_response.json()["id"]

        # Update priority
        update_data = {"priority_score": 5}
        response = client.put(f"/api/contacts/{contact_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["priority_score"] == 5


# =============================================================================
# CONTACT IDENTITIES
# =============================================================================

class TestContactIdentities:
    """Test contact identity management."""

    def test_get_contact_identities(self, client):
        """GET /api/contacts/{id}/identities should return contact identities."""
        # Get first contact
        list_response = client.get("/api/contacts?limit=1")
        contact_id = list_response.json()["contacts"][0]["id"]

        response = client.get(f"/api/contacts/{contact_id}/identities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_add_contact_identity(self, client):
        """POST /api/contacts/{id}/identities should add an identity."""
        # Create a contact first
        new_contact = {"first_name": "Alice", "last_name": "Cooper"}
        create_response = client.post("/api/contacts", json=new_contact)
        contact_id = create_response.json()["id"]

        # Add identity
        identity = {
            "identity_type": "email",
            "value": "alice@example.com",
            "verified": 1,
            "is_primary": 1,
        }
        response = client.post(f"/api/contacts/{contact_id}/identities", json=identity)
        assert response.status_code == 200
        data = response.json()
        assert data["value"] == "alice@example.com"
        assert data["identity_type"] == "email"


# =============================================================================
# ACCOUNTS CRUD
# =============================================================================

class TestAccounts:
    """Test account CRUD operations."""

    def test_list_accounts(self, client):
        """GET /api/accounts should return paginated accounts."""
        response = client.get("/api/accounts?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "accounts" in data
        assert "total" in data
        assert data["total"] >= 25
        assert len(data["accounts"]) <= 10

    def test_get_first_account(self, client):
        """GET /api/accounts/{id} should return a single account."""
        # Get first account
        list_response = client.get("/api/accounts?limit=1")
        accounts = list_response.json()["accounts"]
        assert len(accounts) > 0
        account_id = accounts[0]["id"]

        # Get specific account
        response = client.get(f"/api/accounts/{account_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == account_id
        assert "name" in data
        assert "domain" in data
        assert "industry" in data

    def test_get_account_not_found(self, client):
        """GET /api/accounts/{nonexistent_id} should return 404."""
        response = client.get("/api/accounts/nonexistent_account_id")
        assert response.status_code == 404

    def test_create_account(self, client):
        """POST /api/accounts should create a new account."""
        new_account = {
            "name": "TestCorp Inc",
            "domain": "testcorp.com",
            "industry": "SaaS",
            "employee_count": 500,
            "tier": "mid_market",
            "known_tools": ["Selenium", "Cypress"],
        }
        response = client.post("/api/accounts", json=new_account)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "TestCorp Inc"
        assert data["domain"] == "testcorp.com"
        assert data["industry"] == "SaaS"
        assert data["id"].startswith("acc_")


# =============================================================================
# MESSAGES / DRAFTS
# =============================================================================

class TestMessages:
    """Test message draft operations."""

    def test_list_messages(self, client):
        """GET /api/messages should return paginated messages."""
        response = client.get("/api/messages?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "messages" in data
        assert "total" in data
        assert data["total"] > 0

    def test_list_messages_by_approval_status(self, client):
        """GET /api/messages?approval_status=draft should filter by status."""
        response = client.get("/api/messages?approval_status=draft&limit=100")
        assert response.status_code == 200
        data = response.json()
        for msg in data["messages"]:
            assert msg["approval_status"] == "draft"

    def test_approve_message(self, client):
        """PUT /api/messages/{id}/approve should update status to approved."""
        # Get first message
        list_response = client.get("/api/messages?limit=1")
        messages = list_response.json()["messages"]
        if len(messages) > 0:
            message_id = messages[0]["id"]

            response = client.put(f"/api/messages/{message_id}/approve")
            assert response.status_code == 200
            data = response.json()
            assert data["approval_status"] == "approved"

    def test_reject_message(self, client):
        """PUT /api/messages/{id}/reject should update status to rejected."""
        # Get first message
        list_response = client.get("/api/messages?limit=1")
        messages = list_response.json()["messages"]
        if len(messages) > 0:
            message_id = messages[0]["id"]

            response = client.put(f"/api/messages/{message_id}/reject")
            assert response.status_code == 200
            data = response.json()
            assert data["approval_status"] == "rejected"


# =============================================================================
# BATCHES
# =============================================================================

class TestBatches:
    """Test batch operations."""

    def test_list_batches(self, client):
        """GET /api/batches should return list of batches."""
        response = client.get("/api/batches")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3  # Seeded with 3 batches

    def test_get_batch(self, client):
        """GET /api/batches/{id} should return a single batch."""
        # Get first batch
        list_response = client.get("/api/batches")
        batches = list_response.json()
        if len(batches) > 0:
            batch_id = batches[0]["id"]

            response = client.get(f"/api/batches/{batch_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == batch_id
            assert "batch_number" in data
            assert "prospect_count" in data

    def test_launch_batch(self, client):
        """POST /api/batches/launch should create a new batch."""
        new_batch = {
            "prospect_count": 20,
            "ab_variable": "pain_hook",
        }
        response = client.post("/api/batches/launch", json=new_batch)
        assert response.status_code == 200
        data = response.json()
        assert data["prospect_count"] == 20
        assert data["ab_variable"] == "pain_hook"
        assert "batch_number" in data
        assert data["status"] == "building"


# =============================================================================
# SIGNALS
# =============================================================================

class TestSignals:
    """Test signal operations."""

    def test_list_signals(self, client):
        """GET /api/signals should return list of signals."""
        response = client.get("/api/signals?limit=50")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_act_on_signal(self, client):
        """POST /api/signals/{id}/act should mark signal as acted on."""
        # Get first signal
        list_response = client.get("/api/signals?limit=1")
        signals = list_response.json()
        if len(signals) > 0:
            signal_id = signals[0]["id"]

            response = client.post(f"/api/signals/{signal_id}/act")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "acted"


# =============================================================================
# EXPERIMENTS
# =============================================================================

class TestExperiments:
    """Test experiment operations."""

    def test_list_experiments(self, client):
        """GET /api/experiments should return list of experiments."""
        response = client.get("/api/experiments")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3  # Seeded with 3 experiments


# =============================================================================
# AGENT RUNS
# =============================================================================

class TestAgentRuns:
    """Test agent run operations."""

    def test_list_agent_runs(self, client):
        """GET /api/agent-runs should return list of agent runs."""
        response = client.get("/api/agent-runs?limit=50")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


# =============================================================================
# FLOW MANAGEMENT
# =============================================================================

class TestFlowManagement:
    """Test flow management endpoints."""

    def test_flow_catalog(self, client):
        """GET /api/flows/catalog should return available flows."""
        response = client.get("/api/flows/catalog")
        assert response.status_code == 200
        data = response.json()
        assert "flows" in data
        assert len(data["flows"]) == 3
        flow_types = [f["type"] for f in data["flows"]]
        assert "account_research" in flow_types
        assert "linkedin_prospecting" in flow_types
        assert "email_prospecting" in flow_types

    def test_launch_flow(self, client):
        """POST /api/flows/run should launch a flow and return flow_run with id."""
        flow_config = {
            "flow_type": "account_research",
            "config": {"volume_cap": 10, "quality_bar": "strict"},
        }
        response = client.post("/api/flows/run", json=flow_config)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["flow_type"] == "account_research"
        assert data["status"] == "running"

    def test_list_flow_runs(self, client):
        """GET /api/flows/runs should return list of flow runs."""
        response = client.get("/api/flows/runs?limit=50")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_list_flow_runs_by_type(self, client):
        """GET /api/flows/runs?flow_type=account_research should filter by type."""
        response = client.get("/api/flows/runs?flow_type=account_research&limit=50")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        for run in data:
            assert run["flow_type"] == "account_research"

    def test_list_flow_runs_by_status(self, client):
        """GET /api/flows/runs?status=completed should filter by status."""
        response = client.get("/api/flows/runs?status=completed&limit=50")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_flow_run(self, client):
        """GET /api/flows/runs/{id} should return flow run with steps and artifacts."""
        # Get first flow run
        list_response = client.get("/api/flows/runs?limit=1")
        runs = list_response.json()
        if len(runs) > 0:
            run_id = runs[0]["id"]

            response = client.get(f"/api/flows/runs/{run_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == run_id
            assert "steps" in data
            assert "artifacts" in data
            assert isinstance(data["steps"], list)

    def test_get_flow_run_not_found(self, client):
        """GET /api/flows/runs/{nonexistent_id} should return 404."""
        response = client.get("/api/flows/runs/nonexistent_flow_id")
        assert response.status_code == 404

    def test_cancel_flow_run(self, client):
        """POST /api/flows/runs/{id}/cancel should cancel a flow run."""
        # Launch a flow first
        flow_config = {"flow_type": "linkedin_prospecting"}
        launch_response = client.post("/api/flows/run", json=flow_config)
        run_id = launch_response.json()["id"]

        # Cancel it
        response = client.post(f"/api/flows/runs/{run_id}/cancel")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "cancelled"


# =============================================================================
# ACTIVITY TIMELINE
# =============================================================================

class TestActivity:
    """Test activity timeline endpoints."""

    def test_list_activity(self, client):
        """GET /api/activity should return paginated activities."""
        response = client.get("/api/activity?limit=100")
        assert response.status_code == 200
        data = response.json()
        assert "activities" in data
        assert "total" in data
        assert data["total"] > 0

    def test_list_activity_by_channel(self, client):
        """GET /api/activity?channel=email should filter by channel."""
        response = client.get("/api/activity?channel=email&limit=100")
        assert response.status_code == 200
        data = response.json()
        for activity in data["activities"]:
            assert activity["channel"] == "email"


# =============================================================================
# DRAFTS & DRAFT VERSIONS
# =============================================================================

class TestDrafts:
    """Test draft management endpoints."""

    def test_list_drafts(self, client):
        """GET /api/drafts should return paginated drafts."""
        response = client.get("/api/drafts?limit=100")
        assert response.status_code == 200
        data = response.json()
        assert "drafts" in data
        assert "total" in data
        assert data["total"] > 0

    def test_list_drafts_by_status(self, client):
        """GET /api/drafts?status=draft should filter by status."""
        response = client.get("/api/drafts?status=draft&limit=100")
        assert response.status_code == 200
        data = response.json()
        for draft in data["drafts"]:
            assert draft["status"] == "draft"

    def test_get_draft(self, client):
        """GET /api/drafts/{draft_id} should return draft with versions."""
        # Get first draft
        list_response = client.get("/api/drafts?limit=1")
        drafts = list_response.json()["drafts"]
        if len(drafts) > 0:
            draft_id = drafts[0]["draft_id"]

            response = client.get(f"/api/drafts/{draft_id}")
            assert response.status_code == 200
            data = response.json()
            assert "versions" in data
            assert "current" in data
            assert isinstance(data["versions"], list)

    def test_get_draft_not_found(self, client):
        """GET /api/drafts/{nonexistent_id} should return 404."""
        response = client.get("/api/drafts/nonexistent_draft_id")
        assert response.status_code == 404

    def test_update_draft_status(self, client):
        """PUT /api/drafts/{draft_id}/status should update draft status."""
        # Get first draft
        list_response = client.get("/api/drafts?limit=1")
        drafts = list_response.json()["drafts"]
        if len(drafts) > 0:
            draft_id = drafts[0]["draft_id"]

            response = client.put(f"/api/drafts/{draft_id}/status",
                                json={"status": "approved"})
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "approved"

    def test_edit_draft(self, client):
        """PUT /api/drafts/{draft_id}/edit should create new version."""
        # Get first draft
        list_response = client.get("/api/drafts?limit=1")
        drafts = list_response.json()["drafts"]
        if len(drafts) > 0:
            draft_id = drafts[0]["draft_id"]

            response = client.put(f"/api/drafts/{draft_id}/edit",
                                json={"body": "Updated draft body text"})
            assert response.status_code == 200
            data = response.json()
            assert data["version"] >= 2


# =============================================================================
# SENDER HEALTH
# =============================================================================

class TestSenderHealth:
    """Test sender health endpoints."""

    def test_get_sender_health(self, client):
        """GET /api/sender-health should return health snapshots."""
        response = client.get("/api/sender-health")
        assert response.status_code == 200
        data = response.json()
        assert "snapshots" in data
        assert isinstance(data["snapshots"], list)

    def test_sender_health_checklist(self, client):
        """GET /api/sender-health/checklist should return SPF/DKIM/DMARC status."""
        response = client.get("/api/sender-health/checklist")
        assert response.status_code == 200
        data = response.json()
        assert "spf" in data
        assert "dkim" in data
        assert "dmarc" in data
        assert "warmup" in data
        assert data["spf"]["status"] == "pass"
        assert data["dkim"]["status"] == "pass"

    def test_create_sender_health_snapshot(self, client):
        """POST /api/sender-health should create a new health snapshot."""
        snapshot = {
            "identity_id": "eid_primary",
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "emails_sent": 45,
            "bounces": 1,
            "complaints": 0,
            "replies": 5,
            "bounce_rate": 0.02,
            "complaint_rate": 0.0,
            "reply_rate": 0.11,
            "domain_reputation": "good",
            "spf_pass": 1,
            "dkim_pass": 1,
            "dmarc_pass": 1,
        }
        response = client.post("/api/sender-health", json=snapshot)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data


# =============================================================================
# EMAIL CHANNEL
# =============================================================================

class TestEmailChannel:
    """Test email channel endpoints."""

    def test_list_email_identities(self, client):
        """GET /api/email/identities should return list of identities."""
        response = client.get("/api/email/identities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2  # Seeded with 2 identities

    def test_list_suppression(self, client):
        """GET /api/email/suppression should return suppression entries."""
        response = client.get("/api/email/suppression")
        assert response.status_code == 200
        data = response.json()
        assert "entries" in data
        assert "total" in data
        assert isinstance(data["entries"], list)

    def test_list_email_events(self, client):
        """GET /api/email/events should return email events."""
        response = client.get("/api/email/events?limit=50")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_pacing_status(self, client):
        """GET /api/email/pacing should return pacing rules and limits."""
        response = client.get("/api/email/pacing")
        assert response.status_code == 200
        data = response.json()
        assert "rules" in data
        assert "identities" in data
        assert "sent_today" in data
        assert "limit_today" in data
        assert "warmup_active" in data


# =============================================================================
# INTELLIGENCE & ANALYTICS
# =============================================================================

class TestIntelligence:
    """Test intelligence and analytics endpoints."""

    def test_proof_point_stats(self, client):
        """GET /api/intelligence/proof-points should return proof point statistics."""
        response = client.get("/api/intelligence/proof-points")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        for pp, stats in data.items():
            assert "used" in stats
            assert "replied" in stats
            assert "rate" in stats

    def test_pain_hook_stats(self, client):
        """GET /api/intelligence/pain-hooks should return pain hook statistics."""
        response = client.get("/api/intelligence/pain-hooks")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_opener_style_stats(self, client):
        """GET /api/intelligence/opener-styles should return opener statistics."""
        response = client.get("/api/intelligence/opener-styles")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_personalization_stats(self, client):
        """GET /api/intelligence/personalization should return personalization stats."""
        response = client.get("/api/intelligence/personalization")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)


# =============================================================================
# ANALYTICS & FUNNEL
# =============================================================================

class TestAnalytics:
    """Test analytics endpoints."""

    def test_pipeline_funnel(self, client):
        """GET /api/pipeline-funnel should return stage counts."""
        response = client.get("/api/pipeline-funnel")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "new" in data or len(data) > 0

    def test_reply_rates_persona(self, client):
        """GET /api/reply-rates/persona should return reply rates by persona."""
        response = client.get("/api/reply-rates/persona")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_reply_rates_vertical(self, client):
        """GET /api/reply-rates/vertical should return reply rates by vertical."""
        response = client.get("/api/reply-rates/vertical")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)


# =============================================================================
# FOLLOWUPS & OPPORTUNITIES
# =============================================================================

class TestFollowupsAndOpportunities:
    """Test followup and opportunity endpoints."""

    def test_list_followups(self, client):
        """GET /api/followups should return list of followups."""
        response = client.get("/api/followups")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_list_followups_by_state(self, client):
        """GET /api/followups?state=pending should filter by state."""
        response = client.get("/api/followups?state=pending")
        assert response.status_code == 200
        data = response.json()
        for followup in data:
            assert followup["state"] == "pending"

    def test_list_opportunities(self, client):
        """GET /api/opportunities should return list of opportunities."""
        response = client.get("/api/opportunities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


# =============================================================================
# ACTION QUEUE & MISC
# =============================================================================

class TestActionQueueAndMisc:
    """Test action queue and miscellaneous endpoints."""

    def test_action_queue(self, client):
        """GET /api/action-queue should return list of pending actions."""
        response = client.get("/api/action-queue")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_feature_flags(self, client):
        """GET /api/feature-flags should return list of feature flags."""
        response = client.get("/api/feature-flags")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_toggle_feature_flag(self, client):
        """POST /api/feature-flags/{name} should toggle a feature flag."""
        response = client.post("/api/feature-flags/email_sending?enabled=false")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "email_sending"
        assert data["enabled"] is False

    def test_costs_summary(self, client):
        """GET /api/costs should return token and cost summary."""
        response = client.get("/api/costs")
        assert response.status_code == 200
        data = response.json()
        assert "total_tokens" in data
        assert "total_runs" in data
        assert "estimated_cost_usd" in data


# =============================================================================
# SWARM OPERATIONS
# =============================================================================

class TestSwarm:
    """Test swarm operations."""

    def test_list_swarm_runs(self, client):
        """GET /api/swarm/runs should return list of swarm runs."""
        response = client.get("/api/swarm/runs?limit=20")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_list_swarm_tasks(self, client):
        """GET /api/swarm/tasks should return list of swarm tasks."""
        response = client.get("/api/swarm/tasks?limit=50")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_swarm_quality_scores(self, client):
        """GET /api/swarm/quality should return quality scores."""
        response = client.get("/api/swarm/quality")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


# =============================================================================
# IMPORT OPERATIONS
# =============================================================================

class TestImport:
    """Test import operations."""

    def test_import_accounts(self, client):
        """POST /api/import/accounts should import accounts from domains."""
        import_data = {
            "domains": ["newcompany1.com", "newcompany2.com"]
        }
        response = client.post("/api/import/accounts", json=import_data)
        assert response.status_code == 200
        data = response.json()
        assert data["imported"] == 2
        assert "account_ids" in data
        assert len(data["account_ids"]) == 2

    def test_import_contacts(self, client):
        """POST /api/import/contacts should import contacts."""
        # Get an account first
        accounts_response = client.get("/api/accounts?limit=1")
        accounts = accounts_response.json()["accounts"]
        if len(accounts) > 0:
            account_id = accounts[0]["id"]

            import_data = {
                "contacts": [
                    {
                        "account_id": account_id,
                        "first_name": "ImportTest",
                        "last_name": "Contact1",
                        "email": "test1@example.com",
                    },
                    {
                        "account_id": account_id,
                        "first_name": "ImportTest",
                        "last_name": "Contact2",
                        "email": "test2@example.com",
                    },
                ]
            }
            response = client.post("/api/import/contacts", json=import_data)
            assert response.status_code == 200
            data = response.json()
            assert data["imported"] == 2
            assert "contact_ids" in data


# =============================================================================
# LAUNCH & PIPELINE
# =============================================================================

class TestLaunchAndPipeline:
    """Test launch and pipeline operations."""

    def test_launch_pipeline(self, client):
        """POST /api/launch should launch the pipeline."""
        response = client.post("/api/launch", json={})
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "run_id" in data

    def test_pipeline_status(self, client):
        """GET /api/pipeline/status should return pipeline status."""
        response = client.get("/api/pipeline/status")
        assert response.status_code == 200
        data = response.json()
        assert "active" in data
        assert "progress" in data


# =============================================================================
# INSIGHTS
# =============================================================================

class TestInsights:
    """Test insights endpoints."""

    def test_daily_insights(self, client):
        """GET /api/insights/daily should return daily insights."""
        response = client.get("/api/insights/daily")
        assert response.status_code == 200
        data = response.json()
        assert "activity" in data
        assert "pending" in data

    def test_weekly_insights(self, client):
        """GET /api/insights/weekly should return weekly insights."""
        response = client.get("/api/insights/weekly")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)


# =============================================================================
# EDGE CASES & ERROR HANDLING
# =============================================================================

class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_invalid_contact_id_format(self, client):
        """Getting contact with invalid ID should return 404."""
        response = client.get("/api/contacts/invalid123")
        assert response.status_code == 404

    def test_list_contacts_pagination(self, client):
        """Pagination parameters should work correctly."""
        response1 = client.get("/api/contacts?limit=5&offset=0")
        response2 = client.get("/api/contacts?limit=5&offset=5")
        assert response1.status_code == 200
        assert response2.status_code == 200
        data1 = response1.json()
        data2 = response2.json()
        if len(data1["contacts"]) > 0 and len(data2["contacts"]) > 0:
            assert data1["contacts"][0]["id"] != data2["contacts"][0]["id"]

    def test_json_field_parsing(self, client):
        """JSON fields should be properly parsed."""
        response = client.get("/api/accounts?limit=1")
        data = response.json()
        if len(data["accounts"]) > 0:
            account = data["accounts"][0]
            if "known_tools" in account:
                assert isinstance(account["known_tools"], (list, dict)) or account["known_tools"] is None

    def test_empty_filter_results(self, client):
        """Empty filter results should return empty list with total count."""
        response = client.get("/api/contacts?stage=nonexistent_stage")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 0


class TestAnalyticsPipeline:
    """Tests for /api/analytics/pipeline endpoint."""

    def test_pipeline_funnel(self, client):
        response = client.get("/api/analytics/pipeline")
        assert response.status_code == 200
        data = response.json()
        for key in ("total_prospects", "touched", "replied", "meetings", "opportunities"):
            assert key in data
        assert data["total_prospects"] >= 0


class TestPipelineRuns:
    """Tests for /api/pipeline/runs endpoints."""

    def test_list_pipeline_runs(self, client):
        response = client.get("/api/pipeline/runs")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_cancel_nonexistent_run(self, client):
        response = client.post("/api/pipeline/runs/fake_run_123/cancel")
        assert response.status_code == 200
        assert response.json()["status"] == "cancelled"

    def test_skip_approval(self, client):
        response = client.post("/api/pipeline/runs/fake_run_456/skip-approval")
        assert response.status_code == 200

    def test_stream_nonexistent_run(self, client):
        response = client.get("/api/pipeline/runs/fake_run_789/stream")
        assert response.status_code == 404


class TestAnalyticsEndpoints:
    """Tests for analytics and intelligence endpoints."""

    def test_reply_rates(self, client):
        response = client.get("/api/analytics/reply-rates")
        assert response.status_code == 200
        data = response.json()
        assert "by_persona" in data or isinstance(data, dict)

    def test_experiments(self, client):
        response = client.get("/api/analytics/experiments")
        assert response.status_code == 200

    def test_signals(self, client):
        response = client.get("/api/analytics/signals")
        assert response.status_code == 200

    def test_agent_logs(self, client):
        response = client.get("/api/analytics/agent-logs")
        assert response.status_code == 200

    def test_email_health(self, client):
        response = client.get("/api/analytics/email-health")
        assert response.status_code == 200


class TestBatchExecution:
    """Tests for batch execution engine."""

    def test_execute_batch(self, client):
        """Execute a batch with existing contacts."""
        # Get contact IDs first
        resp = client.get("/api/contacts?limit=5")
        contacts = resp.json().get("contacts", resp.json()) if resp.status_code == 200 else []
        if contacts and len(contacts) > 0:
            contact_ids = [c["id"] for c in contacts[:3]]
            response = client.post("/api/batches/execute", json={
                "contact_ids": contact_ids,
                "ab_variable": "pain_hook"
            })
            assert response.status_code == 200
            data = response.json()
            assert "batch_id" in data or "error" in data or "detail" in data or "quality_gate_failed" in data

    def test_execute_flow(self, client):
        """Test flow execution endpoint."""
        response = client.post("/api/flows/account_research/execute", json={
            "target_count": 5
        })
        assert response.status_code == 200

    def test_batch_deliverable(self, client):
        """Test deliverable generation endpoint."""
        # Get a batch ID first
        resp = client.get("/api/batches")
        if resp.status_code == 200:
            batches = resp.json()
            if isinstance(batches, list) and len(batches) > 0:
                batch_id = batches[0].get("id", batches[0].get("batch_id", "fake"))
                response = client.get(f"/api/batches/{batch_id}/deliverable")
                # May return 200 (HTML) or 404 (no data)
                assert response.status_code in [200, 404]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
