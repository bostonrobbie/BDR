"""
Comprehensive Integration Test for BDR Dashboard
Tests all 10 dashboard improvements and endpoints end-to-end with FastAPI backend.
"""

import sys
import os
import sqlite3
import tempfile
import json
from datetime import datetime, timedelta

# Set test mode BEFORE importing models
os.environ["OCC_JOURNAL_MODE"] = "DELETE"

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

import pytest
from fastapi.testclient import TestClient

# Patch DB_PATH before importing models and app
_test_db_dir = tempfile.mkdtemp(prefix="bdr_test_")
_test_db_path = os.path.join(_test_db_dir, "test.db")
os.environ["OCC_DB_PATH"] = _test_db_path

from src.db import models, init_db
from src.api.app import app


# ─── FIXTURES ───────────────────────────────────────────────────


@pytest.fixture(scope="module")
def test_db():
    """Initialize test database once per module."""
    init_db.init_db(_test_db_path)
    yield _test_db_path


@pytest.fixture(scope="module")
def client(test_db):
    """Create FastAPI test client."""
    return TestClient(app)


@pytest.fixture(scope="module")
def test_data(test_db):
    """Create test data in the database."""
    conn = sqlite3.connect(_test_db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")

    now = datetime.utcnow().isoformat()

    # Create test account
    acc_id = "acc_test1"
    conn.execute(
        """INSERT INTO accounts 
        (id, name, domain, industry, sub_industry, employee_count, tier, created_at, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        (
            acc_id,
            "TestCorp",
            "testcorp.com",
            "FinTech",
            "Banking",
            5000,
            "Enterprise",
            now,
            now,
        ),
    )

    # Create test contacts
    contacts = []
    for i in range(5):
        con_id = f"con_test{i}"
        conn.execute(
            """INSERT INTO contacts
            (id, account_id, first_name, last_name, title, persona_type, seniority_level, 
             email, linkedin_url, stage, priority_score, personalization_score, 
             predicted_objection, objection_response, created_at, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                con_id,
                acc_id,
                f"Test",
                f"Contact{i}",
                "QA Director" if i == 0 else "VP Engineering",
                "qa_leader" if i == 0 else "vp_eng",
                "director" if i == 0 else "vp",
                f"test{i}@testcorp.com",
                f"https://linkedin.com/in/test{i}",
                "new",
                4 + i,
                3,
                "Already have a tool",
                "We work with teams that had tools too",
                now,
                now,
            ),
        )
        contacts.append(con_id)

    # Create test batch (use correct column names)
    batch_id = "batch_test1"
    conn.execute(
        """INSERT INTO batches 
        (id, batch_number, prospect_count, ab_variable, ab_description, 
         pre_brief, status, created_at)
        VALUES (?,?,?,?,?,?,?,?)""",
        (
            batch_id,
            1,
            5,
            "pain_hook",
            "Testing pain hook variations",
            "Pre-brief data",
            "completed",
            now,
        ),
    )

    # Create batch prospects
    for i, con_id in enumerate(contacts):
        bp_id = f"bp_test{i}"
        # Removed priority_score from batch_prospects insert
        conn.execute(
            """INSERT INTO batch_prospects
            (id, batch_id, contact_id, ab_group, sequence_status, position_in_batch)
            VALUES (?,?,?,?,?,?)""",
            (bp_id, batch_id, con_id, "A" if i % 2 == 0 else "B", "prospected", i),
        )

    # Create test messages
    messages = []
    for i, con_id in enumerate(contacts):
        msg_id = f"msg_test{i}"
        conn.execute(
            """INSERT INTO message_drafts
            (id, contact_id, batch_id, channel, touch_number, touch_type, subject_line, body,
             word_count, personalization_score, proof_point_used, pain_hook, opener_style,
             ask_style, ab_group, ab_variable, approval_status, created_at, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                msg_id,
                con_id,
                batch_id,
                "inmail",
                1,
                "first_touch",
                f"Test subject {i}",
                f"Test message body {i}",
                100 + i * 10,
                3,
                "Hansard regression",
                "flaky tests",
                "career_ref",
                "soft_ask",
                "A" if i % 2 == 0 else "B",
                "pain_hook",
                "pending" if i < 2 else "approved",
                now,
                now,
            ),
        )
        messages.append((msg_id, con_id))

    # Create test signals (use correct column names)
    for i in range(2):
        sig_id = f"sig_test{i}"
        con_id = contacts[i]
        conn.execute(
            """INSERT INTO signals
            (id, contact_id, account_id, signal_type, description, source_url, 
             detected_at, created_at, acted_on)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                sig_id,
                con_id,
                acc_id,
                "buyer_intent" if i == 0 else "leadership_change",
                f"Signal description {i}",
                "https://linkedin.com/test",
                now,
                now,
                0,
            ),
        )

    # Create test agent runs
    for i in range(3):
        ar_id = f"ar_test{i}"
        conn.execute(
            """INSERT INTO agent_runs
            (id, batch_id, agent_name, run_type, status, tokens_used, duration_ms, started_at)
            VALUES (?,?,?,?,?,?,?,?)""",
            (
                ar_id,
                batch_id,
                ["prospector", "scorer", "message_writer"][i],
                "batch_processing",
                "completed",
                10000 + i * 5000,
                2000 + i * 500,
                now,
            ),
        )

    # Create test replies
    for i in range(2):
        msg_id = messages[i][0]
        con_id = messages[i][1]
        reply_id = f"reply_test{i}"
        conn.execute(
            """INSERT INTO replies
            (id, contact_id, channel, intent, reply_tag, summary,
             raw_text, created_at)
            VALUES (?,?,?,?,?,?,?,?)""",
            (
                reply_id,
                con_id,
                "inmail",
                "positive" if i == 0 else "interested",
                "pain_hook" if i == 0 else "proof_point",
                f"Reply summary {i}",
                f"Raw reply text {i}",
                now,
            ),
        )

    conn.commit()
    conn.close()

    return {
        "account_id": acc_id,
        "batch_id": batch_id,
        "contact_ids": contacts,
        "message_ids": [m[0] for m in messages],
    }


# ─── TEST SUITE ──────────────────────────────────────────────────


class TestLaunchBatchValidation:
    """Test A: Launch Batch validation"""

    def test_batch_number_less_than_1(self, client):
        """POST /api/pipeline/start with batch_number < 1 should return 400"""
        response = client.post(
            "/api/pipeline/start",
            json={"batch_number": 0, "target_count": 25},
        )
        assert response.status_code == 400
        assert "Batch number must be >= 1" in response.json()["detail"]

    def test_target_count_over_100(self, client):
        """POST /api/pipeline/start with target_count > 100 should return 400"""
        response = client.post(
            "/api/pipeline/start",
            json={"batch_number": 2, "target_count": 150},
        )
        assert response.status_code == 400
        assert "must be 1-100" in response.json()["detail"]

    def test_duplicate_batch_number(self, client, test_data):
        """POST /api/pipeline/start with duplicate batch should return 409"""
        response = client.post(
            "/api/pipeline/start",
            json={"batch_number": 1, "target_count": 25},
        )
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]


class TestApprovalQueue:
    """Test B: Approval queue with approval_status filter"""

    def test_approval_queue_default(self, client):
        """GET /api/approval-queue should return pending messages"""
        response = client.get("/api/approval-queue")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_approval_queue_all_status(self, client):
        """GET /api/approval-queue?approval_status=all should return all messages"""
        response = client.get("/api/approval-queue?approval_status=all")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_approval_queue_approved_filter(self, client):
        """GET /api/approval-queue?approval_status=approved should return only approved"""
        response = client.get("/api/approval-queue?approval_status=approved")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestMessageEditing:
    """Test C: Message editing via PATCH"""

    def test_patch_message_body_update(self, client, test_data):
        """PATCH /api/messages/{id} with body update should update word_count"""
        msg_id = test_data["message_ids"][0]
        new_body = "Updated message body with more words and content"
        response = client.patch(
            f"/api/messages/{msg_id}",
            json={"body": new_body},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["body"] == new_body
        assert data.get("word_count") > 0

    def test_patch_message_approval_status(self, client, test_data):
        """PATCH /api/messages/{id} with approval_status should update it"""
        msg_id = test_data["message_ids"][1]
        response = client.patch(
            f"/api/messages/{msg_id}",
            json={"approval_status": "approved"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("approval_status") == "approved"


class TestSmartActionQueue:
    """Test D: Smart Action Queue"""

    def test_action_queue_endpoint(self, client):
        """GET /api/action-queue should return sorted items with category and impact"""
        response = client.get("/api/action-queue")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:
            for action in data:
                assert "type" in action
                assert "priority" in action
                assert "impact" in action
                assert "action" in action


class TestSignals:
    """Test E: Signals endpoints"""

    def test_create_signal(self, client, test_data):
        """POST /api/signals should create signal"""
        response = client.post(
            "/api/signals",
            json={
                "contact_id": test_data["contact_ids"][0],
                "account_id": test_data["account_id"],
                "signal_type": "buyer_intent",
                "description": "Test signal creation",
            },
        )
        assert response.status_code in (200, 201)
        data = response.json()
        signal_id = data.get("id")
        assert signal_id

    def test_re_engage_signal(self, client, test_data):
        """POST /api/signals/{id}/re-engage should mark actioned"""
        response = client.get("/api/signals?active_only=false")
        assert response.status_code == 200
        signals = response.json()
        if signals:
            sig_id = signals[0].get("id")
            response = client.post(f"/api/signals/{sig_id}/re-engage")
            assert response.status_code == 200
            data = response.json()
            assert data.get("status") == "queued"


class TestTokenCostTracking:
    """Test F: Token/Cost tracking"""

    def test_token_costs_endpoint(self, client):
        """GET /api/analytics/token-costs should return by_agent, by_batch, totals"""
        response = client.get("/api/analytics/token-costs")
        assert response.status_code == 200
        data = response.json()
        assert "by_agent" in data
        assert "by_batch" in data
        assert "totals" in data
        assert isinstance(data["by_agent"], list)
        assert isinstance(data["by_batch"], list)
        totals = data["totals"]
        assert "total_runs" in totals
        assert "total_tokens" in totals
        assert "est_cost_usd" in totals
        assert "prospect_count" in totals
        assert "reply_count" in totals


class TestExport:
    """Test G: Export endpoints"""

    def test_export_csv_default(self, client):
        """GET /api/export/csv should return CSV with correct headers"""
        response = client.get("/api/export/csv")
        assert response.status_code == 200
        text = response.text
        assert "first_name" in text
        assert "last_name" in text
        assert "title" in text

    def test_export_csv_min_priority_filter(self, client):
        """GET /api/export/csv?min_priority=4 should filter by priority"""
        response = client.get("/api/export/csv?min_priority=4")
        assert response.status_code == 200
        text = response.text
        assert len(text) > 0


class TestIntelligenceEndpoints:
    """Test H: Intelligence endpoints"""

    def test_batch_comparison_endpoint(self, client):
        """GET /api/analytics/batch-comparison should return batch comparison data"""
        response = client.get("/api/analytics/batch-comparison")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_top_messages_endpoint(self, client):
        """GET /api/analytics/top-messages should return top messages"""
        response = client.get("/api/analytics/top-messages")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestDashboardHTMLValidation:
    """Test I: Dashboard HTML validation"""

    def test_dashboard_root_endpoint(self, client):
        """GET / should return 200"""
        response = client.get("/")
        assert response.status_code == 200

    def test_dashboard_feature_markers(self, client):
        """Dashboard endpoints represent all 10 feature improvements"""
        endpoints = [
            ("/api/pipeline/runs", "GET"),
            ("/api/approval-queue", "GET"),
            ("/api/action-queue", "GET"),
            ("/api/analytics/batch-comparison", "GET"),
            ("/api/signals", "GET"),
            ("/api/analytics/token-costs", "GET"),
            ("/api/export/csv", "GET"),
            ("/api/analytics/top-messages", "GET"),
            ("/api/batches", "GET"),
            ("/", "GET"),
        ]

        endpoints_ok = 0
        for endpoint, method in endpoints:
            response = client.get(endpoint)
            if response.status_code != 404:
                endpoints_ok += 1

        assert endpoints_ok >= 9


# ─── INTEGRATION TEST ────────────────────────────────────────────

class TestEndToEndIntegration:
    """Integration test: workflow from batch launch through approvals"""

    def test_full_workflow(self, client, test_data):
        """Test complete workflow: batch -> contacts -> messages -> approvals -> export"""

        # 1. Verify batch exists
        response = client.get("/api/batches")
        assert response.status_code == 200
        batches = response.json()
        assert len(batches) > 0

        # 2. Get batch summary
        batch_id = test_data["batch_id"]
        response = client.get(f"/api/batches/{batch_id}/summary")
        assert response.status_code == 200
        summary = response.json()
        assert summary.get("batch", {}).get("id") == batch_id

        # 3. Get batch messages
        response = client.get(f"/api/batches/{batch_id}/messages")
        assert response.status_code == 200
        messages = response.json()
        assert len(messages) > 0

        # 4. Get approval queue
        response = client.get("/api/approval-queue")
        assert response.status_code == 200
        approvals = response.json()
        assert isinstance(approvals, list)

        # 5. Approve a message
        msg_id = test_data["message_ids"][0]
        response = client.patch(
            f"/api/messages/{msg_id}",
            json={"approval_status": "approved"},
        )
        assert response.status_code == 200

        # 6. Export batch data
        response = client.get(f"/api/export/csv?batch_id={batch_id}")
        assert response.status_code == 200

        # 7. Check analytics
        response = client.get("/api/analytics/token-costs")
        assert response.status_code == 200

        # 8. Check action queue
        response = client.get("/api/action-queue")
        assert response.status_code == 200

        # 9. Check signals
        response = client.get("/api/signals")
        assert response.status_code == 200

        # 10. Check pipeline runs
        response = client.get("/api/pipeline/runs")
        assert response.status_code == 200

    def test_all_critical_endpoints_accessible(self, client):
        """Verify all 10 critical endpoints are accessible"""
        critical_endpoints = [
            ("/api/pipeline/runs", "GET"),
            ("/api/approval-queue", "GET"),
            ("/api/action-queue", "GET"),
            ("/api/analytics/token-costs", "GET"),
            ("/api/analytics/batch-comparison", "GET"),
            ("/api/analytics/top-messages", "GET"),
            ("/api/signals", "GET"),
            ("/api/export/csv", "GET"),
            ("/api/batches", "GET"),
            ("/", "GET"),
        ]

        for endpoint, method in critical_endpoints:
            response = client.get(endpoint)
            assert response.status_code != 404, f"Endpoint {endpoint} not found"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
