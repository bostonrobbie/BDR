# Testing Guide

## Overview

The test suite validates the entire Outreach Command Center: API endpoints, workflow execution, LinkedIn channel operations, safety enforcement, and SOP compliance. All tests run against an in-memory SQLite database with fresh seed data.

## Running Tests

```bash
cd BDR
python -m pytest tests/test_api.py -v
```

Expected: 126 tests, all passing in under 2 seconds.

## Test Structure

Tests are organized into classes by domain:

### TestBasicEndpoints (10 tests)
Core API health checks:
- Home page serves HTML
- API info endpoint returns metadata
- KPI stats return expected fields
- Pipeline, contacts, accounts endpoints return data
- Activity timeline returns entries

### TestContactManagement (8 tests)
CRUD operations on contacts:
- List contacts with pagination
- Get single contact by ID
- Create new contact
- Update contact fields
- Search contacts by name/title/company
- Filter by persona type and stage

### TestAccountManagement (6 tests)
Company record operations:
- List accounts
- Get single account
- Create account with ICP signals
- Update account fields
- Link contacts to accounts

### TestDraftManagement (7 tests)
Message draft lifecycle:
- List drafts with filters
- Get single draft
- Create draft with all required fields
- Update draft status (draft → approved → sent)
- Filter by channel, status, touch type
- Copy draft content

### TestWorkflowEngine (15 tests)
Workflow execution system:
- List all workflow definitions
- Filter workflows by channel
- Get single workflow definition
- Handle 404 for missing workflows
- List workflow runs with status filter
- Execute Account Research workflow (verify ICP score, pain points, proof point)
- Execute Prospect Shortlist workflow (verify scoring, ranking, exclusions)
- Execute LinkedIn Message Draft workflow (verify 3 variants, word counts, subjects)
- Execute Follow-Up Sequence workflow (verify Touch 3, 5, 6 with different proof points)
- Execute Daily Plan workflow (verify 4 time blocks, touch targets)
- Execute Email Draft workflow (verify subject options, body, quality checks)
- Execute Call Prep workflow (verify 3-line structure: opener, pain, bridge)
- Verify run creation with step tracking
- Verify run detail retrieval with all steps

### TestLinkedInChannel (8 tests)
LinkedIn-specific operations:
- Stats endpoint returns profile/draft/run counts
- Single profile import with all fields
- CSV bulk import (multiple profiles)
- Duplicate detection by LinkedIn URL
- Empty CSV handling
- Profile listing with pagination
- Auto-account creation when importing profiles
- Persona type detection from title keywords

### TestSafetySystem (4 tests)
DRY_RUN and safety enforcement:
- Dry-run status endpoint returns `{active: true}`
- All workflows execute with dry_run=true
- Outbound actions are blocked and logged to safety_events
- Generated drafts remain in `draft` status (never auto-sent)

### TestSOPCompliance (9 tests)
SOP rule enforcement in generated content:
- No em-dashes (—) in LinkedIn drafts
- No em-dashes in email drafts
- Word count tracking on all messages
- Personalization score assigned (1-3 range)
- Proof points matched to prospect industry/vertical
- Follow-up sequences use different proof points than initial touch
- Call prep scripts are exactly 3 lines (opener, pain, bridge)
- Objection prediction maps to correct type based on signals
- Break-up messages stay within 30-50 word limit

### TestBatchOperations (6 tests)
Batch pipeline operations:
- Create batch with configuration
- Add contacts to batch
- Batch status tracking
- Priority scoring within batch
- A/B group assignment

### TestDeliverableGeneration (5 tests)
HTML deliverable output:
- Generate batch deliverable
- Deliverable contains all required sections
- Copy buttons present for messages
- Priority sorting applied

### Additional Test Classes
Various other test classes covering: experiments, signals, intelligence analytics, agent logs, swarm operations, and settings management.

## Key Test Patterns

### Database Isolation
Each test class uses `setUp` to get a fresh database connection. The test client creates a new FastAPI TestClient that shares the test database.

```python
class TestWorkflowEngine(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
```

### Workflow Execution Tests
Workflow tests follow a consistent pattern:
1. POST to the workflow endpoint with required inputs
2. Assert 200 status code
3. Verify output structure matches workflow type
4. Verify run was created in workflow_runs table
5. Verify steps were created in workflow_run_steps table

```python
def test_execute_account_research(self):
    resp = self.client.post("/api/workflows/account-research",
        json={"company_name": "Stripe", "industry": "FinTech"})
    self.assertEqual(resp.status_code, 200)
    data = resp.json()
    self.assertIn("icp_score", data["output"])
    self.assertIn("pain_points", data["output"])
```

### SOP Compliance Tests
SOP tests verify that generated content follows Rob's writing rules:

```python
def test_no_em_dashes_in_linkedin_drafts(self):
    resp = self.client.post("/api/workflows/linkedin-draft",
        json={"contact_id": "cnt_001"})
    data = resp.json()
    for variant in data["output"]["variants"]:
        self.assertNotIn("—", variant["body"])
```

## Adding New Tests

When adding a new workflow or feature:
1. Add tests to the appropriate class (or create a new one)
2. Test both the happy path and error cases
3. Verify safety constraints are enforced
4. Verify SOP compliance for any generated content
5. Run the full suite to check for regressions

## CI/CD Integration

Tests run automatically on every push to GitHub via Vercel's build process. The test command is:

```bash
python -m pytest tests/test_api.py -v --tb=short
```

If any test fails, the deployment is blocked until the issue is resolved.
