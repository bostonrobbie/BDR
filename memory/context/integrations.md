# Integrations Guide

This file documents every tool Rob and Claude use together, how they connect, and the operational rules for each.

---

## Tool Ecosystem Overview

```
LinkedIn Sales Navigator  -->  Prospect Discovery + Research
         |
         v
Apollo.io  -->  Contact Enrichment + Email Sequences + Website Visitor Intent
         |
         v
Claude (Cowork/Code)  -->  Research, Drafting, QA, Analytics, File Management
         |
         v
Gmail  -->  Manual Email Sends (Rob copies from deliverables)
         |
         v
GitHub (BDR repo)  -->  Version Control, Batch Storage, Memory Persistence
         |
         v
SQLite (OCC Database)  -->  Prospect Tracking, Touchpoint Logging, Analytics
```

---

## 1. LinkedIn Sales Navigator

### Purpose
Primary prospecting channel. Used for finding prospects, reading profiles, checking interaction history, and sending InMails.

### How Claude Interacts
- Claude reads Sales Navigator pages via Chrome MCP (browser bridge)
- Uses `get_page_text` for profile data extraction (more reliable than screenshots)
- Bulk JavaScript DOM extraction from search pages for batch prospecting

### Key Workflows
1. **Saved Searches** - Use Rob's saved searches. Click "Show X new results" for fresh prospects.
2. **Profile Research** - Read headline, about, role description, responsibilities, recent activity.
3. **Interaction Check** - MUST check if "Messaged:" or "Viewed:" shows prior activity. If so, EXCLUDE.
4. **InMail Drafting** - Claude drafts, Rob copies and sends manually.

### Rules
- Manager level and above only
- Must fit ICP titles (see Target Personas in CLAUDE.md)
- Filter out: pharma/biotech manufacturing QA (not software), non-US, non-software testing titles
- Capture and log the Sales Navigator profile URL for every prospect
- Never send InMails programmatically

### Data Captured Per Prospect
- Full name, title, company
- LinkedIn/Sales Navigator URL
- Headline and about section summary
- Role description and responsibilities
- Recent activity (posts, comments, shares)
- Interaction history (messaged/viewed/connected status)
- Buyer Intent signals

---

## 2. Apollo.io

### Purpose
Contact enrichment, email discovery, sequence management, and website visitor intent tracking.

### Account Details
- Send from: robert.gorham@testsigma.net
- Email account ID: 68f65bdf998c4c0015f3446a
- Key sequence: Q1 Website Visitor - Tier 1 Intent (ID: 69a1b3564fa5fa001152eb66)

### How Claude Interacts
- Apollo API for contact creation, enrichment, and sequence management
- Apollo MCP tools for search, enrichment, and campaign management
- Browser UI for tasks the API can't handle (per-sequence contact counts, draft statuses, step-level info)

### Key Workflows

#### Contact Enrichment
1. Search contacts by name/company via `apollo_contacts_search`
2. Enrich companies via `apollo_organizations_enrich` (bulk: up to 10 at a time)
3. Match people via `apollo_people_match` or `apollo_people_bulk_match`
4. Create contacts via `apollo_contacts_create`
5. Update contacts via `apollo_contacts_update`

#### Website Visitor Prospecting
1. Open Apollo > Visitors
2. Filter: Pricing, Demo Request, Features, Comparison pages
3. Filter: Company size 200+, Geography: US
4. Cross-reference against existing sequences (no duplicates)
5. Find right persona at each company via People Search

#### Email Sequences
1. Search sequences via `apollo_emailer_campaigns_search`
2. Add contacts to sequence via `apollo_emailer_campaigns_add_contact_ids`
3. Remove/stop contacts via `apollo_emailer_campaigns_remove_or_stop_contact_ids`

### Rules
- Always check if contact already exists before creating
- Always cross-reference against active sequences before adding
- Use browser UI when API data is incomplete
- Monitor catchall domains (bounces silently)
- Log Apollo Contact IDs for tracking

### Catchall Domains to Watch
These domains may accept all emails but not deliver - monitor for engagement:
- OppFi, Drata, Epic Games, Crestron, OpSec, RedSail, Cedar Gate, FreedomPay

---

## 3. Gmail

### Purpose
Manual email sending for outbound sequences that aren't routed through Apollo.

### How It Works
- Rob copies pre-written emails from deliverables or batch files
- Pastes into Gmail compose
- Reviews, potentially edits, sends manually
- Future: Gmail API for bulk draft creation (Rob reviews and sends)

### Rules
- Claude NEVER sends emails directly
- All emails must pass QA gate before being presented to Rob
- Subject lines under 80 characters
- Send window: 12-5 PM (afternoon only)
- Track sends in email_outreach_tracker.csv

---

## 4. GitHub (BDR Repository)

### Purpose
Version control for all BDR operational files, batch deliverables, memory, and code.

### Repository Structure
```
BDR/
  CLAUDE.md           # Primary brain (instructions + memory)
  memory/             # Secondary brain layer
    context/          # Voice rules, playbook, gold standards, integrations
    session/          # Session manager
    ops/              # Operational procedures
  batches/            # Batch deliverables and email sequences
  data/               # Trackers and historical data
  analytics/          # Analysis outputs
  config/             # Scoring weights, proof points, vertical pains
  src/                # OCC codebase
  docs/               # Architecture and operational docs
  tests/              # Test suite
```

### Branch Strategy
- `main` / `master` - stable
- `claude/*` - feature branches for Claude Code sessions
- Push with `-u origin <branch-name>`
- Clear commit messages following conventional commits

### What Gets Committed
- Batch email drafts and deliverables
- Tracker updates (CSV, MD)
- New SOPs and workflow docs
- Memory layer updates
- Code changes to OCC

### What Does NOT Get Committed
- .env files or API keys
- SQLite database files (.db)
- Node modules or Python cache

---

## 5. SQLite (OCC Database)

### Purpose
Persistent storage for prospects, touchpoints, messages, experiments, and analytics.

### Location
- Default: `src/api/data/outreach_seed.db`
- Override: ENV variable `OCC_DB_PATH`

### Key Tables
| Table | Purpose |
|-------|---------|
| accounts | Company records |
| contacts | Person records with priority scores |
| icp_scores | ICP fit calculations |
| signals | Buyer intent signals |
| research_snapshots | Cached company/person research |
| message_drafts | Message containers |
| message_versions | Version history per draft |
| touchpoints | Outreach events |
| replies | Prospect responses with reply tags |
| batches | Batch definitions |
| batch_prospects | Batch membership with A/B groups |
| experiments | A/B test configurations |
| agent_runs | AI execution logs |

### Rules
- Always use the CRUD layer in `src/db/models.py`
- Run migrations before using new schema features
- Cache company research to avoid redundant API calls
- Full audit trail on all touchpoint changes

---

## 6. Slack (MCP Tools)

### Purpose
Team communication, sharing batch results, and getting quick feedback from Rob.

### Available Tools
- `slack_send_message` - Send messages to channels
- `slack_search_public` / `slack_search_public_and_private` - Search messages
- `slack_search_channels` / `slack_search_users` - Find channels/people
- `slack_read_channel` / `slack_read_thread` - Read conversations
- `slack_send_message_draft` - Create draft messages

### Rules
- Only use for sharing batch summaries or asking Rob questions
- Never send prospect outreach via Slack
- Check channel before posting (right audience)

---

## 7. Google Calendar (MCP Tools)

### Purpose
Scheduling meetings with prospects who reply positively.

### Available Tools
- `gcal_list_events` / `gcal_get_event` - View calendar
- `gcal_find_my_free_time` / `gcal_find_meeting_times` - Find availability
- `gcal_create_event` / `gcal_update_event` - Manage events
- `gcal_respond_to_event` - RSVP

### Rules
- Only create calendar events when Rob explicitly asks
- Default meeting length: 15-30 minutes
- Include prospect prep card link in calendar event description
- Check for conflicts before proposing times

---

## Integration Health Checks

Before each session, verify:
1. Apollo API is responding (can search contacts)
2. Sales Navigator is accessible (MCP browser bridge working)
3. GitHub repo is synced (no uncommitted changes blocking work)
4. SQLite database is initialized and accessible
5. All MCP tools are loaded and available
