# Implementation Roadmap

## Phase 1: MVP - Foundation Layer

**Goal:** Replace standalone HTML batch files with a database-backed system. Basic LinkedIn workflow functional.

### User Stories
- As Rob, I can create a new batch and have prospects stored in the database
- As Rob, I can view all my prospects in a unified pipeline table
- As Rob, I can trigger research for a prospect and see structured results
- As Rob, I can generate all 6 touches for a prospect with copy buttons
- As Rob, I can mark a touch as "sent" and have it logged
- As Rob, I can see my daily action queue on the home page

### Backend Tasks
- [ ] Initialize SQLite database with all 15 tables
- [ ] Create FastAPI CRUD endpoints for accounts, contacts, batches
- [ ] Build priority scoring calculation endpoint
- [ ] Build ICP scoring calculation endpoint
- [ ] Create message draft CRUD with version tracking
- [ ] Create touchpoint logging endpoint
- [ ] Build follow-up scheduling logic

### Frontend Tasks
- [ ] Home page: daily action queue, pipeline snapshot
- [ ] Pipeline page: sortable, filterable prospect table
- [ ] LinkedIn Workspace: batch manager, prospect cards, message editor
- [ ] Copy-to-clipboard buttons for all messages
- [ ] Status dropdown per prospect
- [ ] Priority badge display
- [ ] Right-side detail panel with research and timeline

### Database Migrations
- [ ] v001: Create all tables (init_db.py)
- [ ] v002: Seed proof points and objection mappings

### Tests
- [ ] Unit: ICP scoring logic
- [ ] Unit: Priority scoring logic
- [ ] Unit: Follow-up date calculation
- [ ] Unit: Word count validation
- [ ] Integration: Create account + contact + research flow
- [ ] Integration: Generate drafts and verify QC

### Validation
- Build a 25-prospect batch using the new system
- All data persists in SQLite (no standalone HTML dependency)
- Batch build time < 2 hours

---

## Phase 2: v1 - Full Multi-Channel + Tracking

**Goal:** All three workspaces functional. Full touchpoint tracking. QC automation. Meeting prep.

### User Stories
- As Rob, I can manage email outreach with subject lines and mobile preview
- As Rob, I can see my call queue sorted by priority and time zone
- As Rob, I can log call outcomes and post-call notes
- As Rob, I can classify replies by intent and reply tag
- As Rob, I get next-action recommendations after logging a reply
- As Rob, I can see a meeting prep card when a prospect books a meeting
- As Rob, I can see a full audit trail for any prospect

### Backend Tasks
- [ ] Email workspace API (email-specific draft rules)
- [ ] Call workspace API (call queue sorting, outcome logging)
- [ ] Reply classification API with next-action engine
- [ ] Meeting prep card generation endpoint
- [ ] Full audit log triggers on all tables
- [ ] Follow-up overdue detection and alerting
- [ ] Opportunity creation and attribution flow

### Frontend Tasks
- [ ] Email Workspace: queue, composer, mobile preview, follow-up calendar
- [ ] Calls Workspace: call queue, call card, outcome buttons, notes
- [ ] Reply handling modal with intent classification
- [ ] Meeting prep card display
- [ ] Prospect timeline view (full audit trail)
- [ ] Accounts & Contacts page (CRM-lite)

### Agent Development
- [ ] Quality Gate Agent (all 10 checks)
- [ ] Reply Triage Agent
- [ ] Call Prep Agent
- [ ] Sequencer Agent

### Tests
- [ ] Unit: Stage transition validation
- [ ] Unit: Proof point rotation check
- [ ] Unit: A/B group assignment balance
- [ ] Integration: Full touchpoint → reply → opportunity flow
- [ ] Integration: Company research caching
- [ ] E2E: LinkedIn prospect → research → draft → send → follow-up → reply → meeting

### Validation
- All 3 workspaces functional
- Follow-up compliance > 90%
- QC pass rate > 95% on first draft
- Reply handling < 4 hours from receipt

---

## Phase 3: v2 - Intelligence + Agent Swarm

**Goal:** System actively learns and improves. Full analytics. Agent swarm orchestration.

### User Stories
- As Rob, I see analytics showing which personas, verticals, and proof points perform best
- As Rob, I can configure and track A/B experiments
- As Rob, I get a pre-brief before each new batch showing what's working
- As Rob, I can see token usage and efficiency trends
- As Rob, dormant prospects are surfaced for re-engagement when triggers appear
- As Rob, I can see every agent run with full transparency

### Backend Tasks
- [ ] Intelligence API (aggregation queries for all analytics)
- [ ] Experiment engine (create, assign, track, conclude)
- [ ] Pre-brief generation endpoint
- [ ] Signal Scanner integration
- [ ] Re-engagement trigger detection
- [ ] Token usage tracking across all agents
- [ ] Weekly insights generation

### Frontend Tasks
- [ ] Intelligence page: 7 analytics charts
- [ ] Experiments page: create, view, analyze
- [ ] Agent Logs page: run history, QA flags, token usage
- [ ] Research & Signals page
- [ ] Batch comparison dashboard
- [ ] Settings/Admin page

### Agent Development
- [ ] Supervisor Agent (orchestrates all workers)
- [ ] Pre-Brief Agent
- [ ] Insights Agent
- [ ] Experiment Analyst Agent
- [ ] Signal Scanner Agent
- [ ] Full swarm coordination protocol

### Tests
- [ ] Unit: Experiment statistical analysis
- [ ] Unit: Pre-brief generation from mock data
- [ ] Integration: Full batch lifecycle with pre-brief
- [ ] Integration: Re-engagement trigger detection
- [ ] E2E: Multi-batch learning loop (batch 1 data improves batch 2)

### Validation
- Reply rate > 1.5% (up from ~1% baseline)
- Meeting-to-opportunity conversion > 40%
- Token cost per batch shows decreasing trend
- Pre-briefs accurately reflect historical data

---

## GitHub Workflow

### Branch Strategy
```
main
├── feat/database-schema
├── feat/api-core
├── feat/linkedin-workspace
├── feat/email-workspace
├── feat/calls-workspace
├── feat/agent-research
├── feat/agent-draft
├── feat/agent-qc
├── feat/agent-swarm
├── feat/analytics
├── feat/experiments
└── fix/* (bugfixes)
```

### Commit Convention
```
feat: add contact CRUD endpoints
fix: correct priority scoring for VP Eng at large companies
docs: update data model with signals table
test: add unit tests for ICP scoring
refactor: extract message QC into standalone module
```

### PR Template
```markdown
## What
Brief description of the change.

## Why
Problem this solves or feature this enables.

## Testing
How this was tested.

## Database Changes
Any schema changes (with migration number).
```

### Deployment Checklist (for Cloud Code later)
- [ ] All tests pass
- [ ] Database migrations run clean
- [ ] No hardcoded paths
- [ ] Environment variables documented
- [ ] README updated
- [ ] Agent prompts stored in templates (not inline)
