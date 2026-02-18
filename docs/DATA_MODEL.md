# Data Model - Outreach Command Center

## Entity Relationship Diagram

```
accounts ──┐
           ├──→ contacts ──→ research_snapshots (person)
           │       │
           │       ├──→ icp_scores
           │       ├──→ signals
           │       ├──→ message_drafts ──→ message_versions
           │       ├──→ touchpoints ──→ replies
           │       ├──→ followups
           │       └──→ opportunities
           │
           └──→ research_snapshots (company)

batches ──→ batch_prospects ──→ contacts
       └──→ experiments

agent_runs (linked to contacts, batches, or standalone)
audit_log (tracks all changes across all tables)
```

## Tables

### accounts
Company-level records.

| Field | Type | Notes |
|-------|------|-------|
| id | TEXT (UUID) PK | |
| name | TEXT NOT NULL | Company name |
| domain | TEXT | Primary website domain |
| industry | TEXT | SaaS, FinTech, Healthcare, etc. |
| sub_industry | TEXT | More specific category |
| employee_count | INTEGER | Approximate headcount |
| employee_band | TEXT | 1-50, 51-200, 201-1000, 1001-5000, 5000+ |
| tier | TEXT | Enterprise, Mid-Market, SMB |
| known_tools | TEXT (JSON) | Testing tools: ["Selenium","Cypress"] |
| linkedin_company_url | TEXT | Sales Navigator company page |
| website_url | TEXT | Company website |
| buyer_intent | BOOLEAN DEFAULT 0 | Buyer intent signal detected |
| buyer_intent_date | DATE | When intent was detected |
| annual_revenue | TEXT | Revenue range if known |
| funding_stage | TEXT | Seed, Series A/B/C, Public |
| last_funding_date | DATE | Most recent funding |
| last_funding_amount | TEXT | Amount raised |
| hq_location | TEXT | Headquarters city/state |
| notes | TEXT | Free-form account notes |
| research_freshness | DATE | When company research was last done |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |
| updated_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |

### contacts
Person-level records. Each belongs to one account.

| Field | Type | Notes |
|-------|------|-------|
| id | TEXT (UUID) PK | |
| account_id | TEXT FK → accounts.id | |
| first_name | TEXT NOT NULL | |
| last_name | TEXT NOT NULL | |
| full_name | TEXT GENERATED | Computed: first_name + ' ' + last_name |
| title | TEXT | Current job title |
| persona_type | TEXT | QA Director, VP Eng, QA Manager, SDET |
| seniority_level | TEXT | IC, Manager, Director, VP, C-Suite |
| email | TEXT | Work email (nullable) |
| email_verified | BOOLEAN | Whether email was validated |
| linkedin_url | TEXT UNIQUE | Sales Navigator profile URL |
| phone | TEXT | |
| location | TEXT | City, State |
| timezone | TEXT | IANA timezone |
| tenure_months | INTEGER | Months in current role |
| recently_hired | BOOLEAN | < 6 months in role |
| previous_company | TEXT | Prior employer |
| previous_title | TEXT | Prior role |
| stage | TEXT DEFAULT 'new' | new, researched, drafted, sent, follow_up, replied, meeting_booked, meeting_held, opportunity, dormant, re_engaged, closed |
| priority_score | INTEGER DEFAULT 3 | 1-5 calculated |
| priority_factors | TEXT (JSON) | Breakdown |
| personalization_score | INTEGER | 1-3 for best message |
| predicted_objection | TEXT | Most likely objection |
| objection_response | TEXT | Pre-loaded response |
| status | TEXT DEFAULT 'active' | active, dormant, bounced, do_not_contact |
| do_not_contact | BOOLEAN DEFAULT 0 | |
| dnc_reason | TEXT | Why DNC was set |
| source | TEXT | sales_nav, apollo, manual, referral |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |
| updated_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |

### icp_scores
ICP fit scoring per contact.

| Field | Type | Notes |
|-------|------|-------|
| id | TEXT (UUID) PK | |
| contact_id | TEXT FK → contacts.id | |
| title_match | INTEGER (0-3) | 0=none, 1=secondary, 2=primary, 3=exact |
| vertical_match | INTEGER (0-2) | 0=off, 1=adjacent, 2=top |
| company_size_fit | INTEGER (0-2) | 0=wrong, 1=ok, 2=sweet spot |
| seniority_fit | INTEGER (0-2) | 0=junior, 1=manager, 2=director+ |
| software_qa_confirmed | BOOLEAN | Owns software testing decisions |
| buyer_intent_bonus | INTEGER DEFAULT 0 | +2 if buyer intent |
| total_score | INTEGER | Composite 0-12 |
| scored_at | DATETIME | |
| scoring_version | TEXT | Track scoring formula version |

### signals
Detected signals for accounts and contacts.

| Field | Type | Notes |
|-------|------|-------|
| id | TEXT (UUID) PK | |
| account_id | TEXT FK → accounts.id | |
| contact_id | TEXT FK → contacts.id (nullable) | |
| signal_type | TEXT | buyer_intent, qa_job_posting, funding, leadership_change, product_launch, competitor_eval |
| description | TEXT | What was detected |
| source_url | TEXT | Where it was found |
| detected_at | DATETIME | |
| expires_at | DATE | When signal becomes stale |
| acted_on | BOOLEAN DEFAULT 0 | Whether we acted on this |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |

### research_snapshots
Structured research per entity. Cached and reusable.

| Field | Type | Notes |
|-------|------|-------|
| id | TEXT (UUID) PK | |
| contact_id | TEXT FK (nullable) | |
| account_id | TEXT FK (nullable) | |
| entity_type | TEXT | 'person' or 'company' |
| headline | TEXT | LinkedIn headline or company tagline |
| summary | TEXT | Structured summary |
| career_history | TEXT (JSON) | Previous roles and tenures |
| responsibilities | TEXT | Key responsibilities |
| tech_stack_signals | TEXT (JSON) | Tools, frameworks |
| pain_indicators | TEXT (JSON) | Testing pain signals |
| recent_activity | TEXT | Posts, shares, comments |
| company_products | TEXT | Products, platforms, services |
| company_metrics | TEXT | Users, revenue, transactions |
| company_news | TEXT | Recent news, launches |
| hiring_signals | TEXT | QA/eng job postings |
| sources | TEXT (JSON array) | URLs used |
| confidence_score | INTEGER (1-5) | How confident in the data |
| agent_run_id | TEXT FK → agent_runs.id | |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |

### message_drafts
One per message per contact. Versioned.

| Field | Type | Notes |
|-------|------|-------|
| id | TEXT (UUID) PK | |
| contact_id | TEXT FK → contacts.id | |
| batch_id | TEXT FK → batches.id (nullable) | |
| channel | TEXT | linkedin, email, call |
| touch_number | INTEGER | 1-6 |
| touch_type | TEXT | inmail, email, call_snippet, breakup, re_engagement, reply_draft |
| subject_line | TEXT | For email/InMail |
| body | TEXT NOT NULL | Message body or call snippet |
| version | INTEGER DEFAULT 1 | |
| personalization_score | INTEGER | 1-3 |
| proof_point_used | TEXT | Customer story used |
| pain_hook | TEXT | Pain angle used |
| opener_style | TEXT | career_reference, company_metric, activity_reference |
| ask_style | TEXT | direct_ask, soft_offer, value_add |
| word_count | INTEGER | Auto-calculated |
| qc_passed | BOOLEAN | |
| qc_flags | TEXT (JSON) | Issues found |
| qc_run_id | TEXT FK → agent_runs.id | |
| approval_status | TEXT DEFAULT 'draft' | draft, ready, sent, archived |
| ab_group | TEXT | A, B, or C |
| ab_variable | TEXT | What's being tested |
| agent_run_id | TEXT FK → agent_runs.id | |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |
| updated_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |

### touchpoints
Every actual outreach action Rob takes. Created when Rob marks "sent" or "called."

| Field | Type | Notes |
|-------|------|-------|
| id | TEXT (UUID) PK | |
| contact_id | TEXT FK → contacts.id | |
| message_draft_id | TEXT FK → message_drafts.id | |
| channel | TEXT | linkedin, email, call |
| touch_number | INTEGER | 1-6 |
| sent_at | DATETIME | When Rob sent/called |
| outcome | TEXT | For calls: connected, voicemail, no_answer, wrong_number |
| call_duration_seconds | INTEGER | If connected, how long |
| call_notes | TEXT | Post-call notes |
| confirmed_by_user | BOOLEAN DEFAULT 1 | Always true (user confirms) |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |

### replies
When a prospect replies.

| Field | Type | Notes |
|-------|------|-------|
| id | TEXT (UUID) PK | |
| contact_id | TEXT FK → contacts.id | |
| touchpoint_id | TEXT FK → touchpoints.id | Which touch triggered |
| channel | TEXT | linkedin, email, call |
| intent | TEXT | positive, neutral, not_now, referral, unsubscribe, negative |
| reply_tag | TEXT | opener, pain_hook, proof_point, timing, referral, not_interested, unknown |
| summary | TEXT | Brief summary |
| raw_text | TEXT | The actual reply text |
| referral_name | TEXT | If referred someone |
| referral_title | TEXT | Their title |
| recommended_next_step | TEXT | Agent suggestion |
| next_step_taken | TEXT | What Rob actually did |
| replied_at | DATETIME | |
| handled_at | DATETIME | When Rob responded |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |

### followups
Scheduled follow-up actions.

| Field | Type | Notes |
|-------|------|-------|
| id | TEXT (UUID) PK | |
| contact_id | TEXT FK → contacts.id | |
| touch_number | INTEGER | |
| channel | TEXT | |
| due_date | DATE | |
| state | TEXT DEFAULT 'pending' | pending, completed, skipped, overdue |
| message_draft_id | TEXT FK → message_drafts.id | |
| reminder_sent | BOOLEAN DEFAULT 0 | |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |
| completed_at | DATETIME | |

### opportunities
The North Star table.

| Field | Type | Notes |
|-------|------|-------|
| id | TEXT (UUID) PK | |
| contact_id | TEXT FK → contacts.id | |
| account_id | TEXT FK → accounts.id | |
| meeting_date | DATETIME | |
| meeting_held | BOOLEAN DEFAULT 0 | |
| meeting_outcome | TEXT | qualified, disqualified, no_show, rescheduled |
| opportunity_created_date | DATETIME | |
| opportunity_created | BOOLEAN DEFAULT 0 | |
| status | TEXT | meeting_booked, meeting_held, opportunity_created, disqualified, lost |
| pipeline_value | REAL | Estimated deal value |
| trigger_touchpoint_id | TEXT FK → touchpoints.id | |
| trigger_reply_id | TEXT FK → replies.id | |
| attribution_channel | TEXT | |
| attribution_touch_number | INTEGER | |
| attribution_proof_point | TEXT | |
| attribution_pain_hook | TEXT | |
| attribution_opener_style | TEXT | |
| attribution_personalization_score | INTEGER | |
| attribution_ab_group | TEXT | |
| attribution_ab_variable | TEXT | |
| ae_name | TEXT | Which AE got the meeting |
| ae_feedback | TEXT | AE feedback on lead quality |
| disqualification_reason | TEXT | Why it didn't convert |
| notes | TEXT | |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |

### batches
Batch grouping.

| Field | Type | Notes |
|-------|------|-------|
| id | TEXT (UUID) PK | |
| batch_number | INTEGER | Sequential |
| created_date | DATE | |
| prospect_count | INTEGER | |
| ab_variable | TEXT | What's being tested |
| ab_description | TEXT | Details of the test |
| pre_brief | TEXT | 5-line summary |
| mix_ratio | TEXT (JSON) | {"qa_leaders":14,"vp_eng":8,"buyer_intent":3} |
| status | TEXT | building, ready, active, completed |
| html_file_path | TEXT | Path to exported HTML |
| metrics | TEXT (JSON) | Post-batch metrics summary |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |

### batch_prospects
Join table.

| Field | Type | Notes |
|-------|------|-------|
| id | TEXT (UUID) PK | |
| batch_id | TEXT FK → batches.id | |
| contact_id | TEXT FK → contacts.id | |
| ab_group | TEXT | A, B, or C |
| sequence_status | TEXT | not_started through completed |
| position_in_batch | INTEGER | Sort order |

### experiments
A/B test definitions and results.

| Field | Type | Notes |
|-------|------|-------|
| id | TEXT (UUID) PK | |
| name | TEXT | |
| variable | TEXT | pain_hook, proof_point_style, opener_style, ask_intensity, message_length |
| group_a_desc | TEXT | |
| group_b_desc | TEXT | |
| status | TEXT | active, completed, inconclusive |
| batches_included | TEXT (JSON array) | Which batches are part of this |
| group_a_sent | INTEGER DEFAULT 0 | |
| group_a_replies | INTEGER DEFAULT 0 | |
| group_a_meetings | INTEGER DEFAULT 0 | |
| group_a_opps | INTEGER DEFAULT 0 | |
| group_b_sent | INTEGER DEFAULT 0 | |
| group_b_replies | INTEGER DEFAULT 0 | |
| group_b_meetings | INTEGER DEFAULT 0 | |
| group_b_opps | INTEGER DEFAULT 0 | |
| winner | TEXT | A, B, or NULL |
| conclusion | TEXT | |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |

### agent_runs
Full audit log for agent execution.

| Field | Type | Notes |
|-------|------|-------|
| id | TEXT (UUID) PK | |
| run_type | TEXT | research, draft, qc, analysis, pre_brief, batch_build, reply_triage, call_prep, signal_scan |
| agent_name | TEXT | Which agent ran |
| contact_id | TEXT FK (nullable) | |
| batch_id | TEXT FK (nullable) | |
| inputs | TEXT (JSON) | |
| outputs | TEXT (JSON) | |
| sources_used | TEXT (JSON array) | |
| decisions | TEXT (JSON) | |
| tokens_used | INTEGER | |
| duration_ms | INTEGER | |
| status | TEXT | success, partial, error |
| error_message | TEXT | |
| parent_run_id | TEXT FK → agent_runs.id | For sub-tasks |
| started_at | DATETIME | |
| completed_at | DATETIME | |

### audit_log
Immutable change log.

| Field | Type | Notes |
|-------|------|-------|
| id | INTEGER AUTOINCREMENT PK | |
| table_name | TEXT | |
| record_id | TEXT | |
| action | TEXT | insert, update, delete |
| changed_by | TEXT | 'user' or 'agent:{run_id}' |
| old_values | TEXT (JSON) | |
| new_values | TEXT (JSON) | |
| timestamp | DATETIME DEFAULT CURRENT_TIMESTAMP | |

## Indexes

```sql
CREATE INDEX idx_contacts_account ON contacts(account_id);
CREATE INDEX idx_contacts_stage ON contacts(stage);
CREATE INDEX idx_contacts_priority ON contacts(priority_score DESC);
CREATE INDEX idx_contacts_linkedin ON contacts(linkedin_url);
CREATE INDEX idx_research_contact ON research_snapshots(contact_id);
CREATE INDEX idx_research_account ON research_snapshots(account_id);
CREATE INDEX idx_messages_contact ON message_drafts(contact_id);
CREATE INDEX idx_messages_batch ON message_drafts(batch_id);
CREATE INDEX idx_touchpoints_contact ON touchpoints(contact_id);
CREATE INDEX idx_touchpoints_sent ON touchpoints(sent_at);
CREATE INDEX idx_replies_contact ON replies(contact_id);
CREATE INDEX idx_followups_due ON followups(due_date, state);
CREATE INDEX idx_opportunities_contact ON opportunities(contact_id);
CREATE INDEX idx_opportunities_status ON opportunities(status);
CREATE INDEX idx_signals_account ON signals(account_id);
CREATE INDEX idx_batch_prospects ON batch_prospects(batch_id, contact_id);
CREATE INDEX idx_agent_runs_type ON agent_runs(run_type);
CREATE INDEX idx_audit_table ON audit_log(table_name, record_id);
```
