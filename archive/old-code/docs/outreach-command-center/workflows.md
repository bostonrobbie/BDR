# Workflows Reference

## How Workflows Work

Each workflow is a multi-step execution that takes structured input, runs through a series of agent steps, and produces structured output (drafts, research briefs, plans). Every workflow:

- Runs in DRY_RUN mode (no outbound actions)
- Creates a `workflow_runs` record with status tracking
- Creates `workflow_run_steps` for each execution step
- Logs activity to `activity_timeline`
- Stores outputs (drafts, research) in the appropriate tables

## Available Workflows

### 1. Account Research (`account_research`)
**Channel:** LinkedIn
**Input:** Company name (required), domain (optional), industry (optional)
**Steps:** validate_input, gather_company_data, analyze_icp_fit, identify_pain_points, generate_brief
**Output:** ICP score (0-7), pain points with severity and talk tracks, recommended proof point, predicted objection, recommended titles to target

**Example:**
```json
POST /api/workflows/account-research
{"company_name": "Stripe", "domain": "stripe.com", "industry": "FinTech"}
```

### 2. Prospect Shortlist Builder (`prospect_shortlist`)
**Channel:** LinkedIn
**Input:** contact_ids (optional, defaults to all active contacts), filters (optional)
**Steps:** validate_csv, filter_titles, score_icp, flag_exclusions, rank_output
**Output:** Ranked shortlist with priority scores, exclusion list with reasons, summary statistics

**Scoring factors:**
- Buyer Intent signal: +2
- QA-titled leader: +1
- Target vertical: +1
- Recently hired: +1
- Uses competitor tool: +1
- VP Eng at 50K+ company: -1

### 3. LinkedIn Message Drafts (`linkedin_message_draft`)
**Channel:** LinkedIn
**Input:** contact_id (required)
**Steps:** load_prospect, load_research, select_proof_point, generate_variants, quality_gate, finalize
**Output:** 3 message variants (warm conversational, direct concise, value-first), each with subject line, body, word count, personalization score

**SOP compliance checks:**
- No em-dashes (replaced with commas)
- Word count 70-120 for InMails
- Personalization score 1-3
- Industry-matched proof point
- Six-element structure (subject, opener, company ref, pain hypothesis, solution, soft ask)

### 4. Follow-Up Sequence Planner (`followup_sequence`)
**Channel:** LinkedIn + Email
**Input:** contact_id (required)
**Steps:** load_original, analyze_angle, draft_followup1, draft_followup2, draft_breakup, quality_gate
**Output:** Touch 3 (InMail follow-up, 40-70 words), Touch 5 (Email, more direct), Touch 6 (Break-up, 30-50 words, no pitch)

**Rules:**
- Each touch uses a DIFFERENT proof point than previous
- Touch 6 never pitches, just closes the loop respectfully
- No guilt-tripping language

### 5. Daily BDR Plan Generator (`daily_plan`)
**Channel:** Multi
**Input:** target_touches (default 50), hours_available (default 8)
**Steps:** load_pipeline, identify_hot, identify_overdue, plan_touches, generate_checklist
**Output:** 4-block daily schedule (morning calls, midday LinkedIn, afternoon follow-ups, late calls), summary statistics

**Time blocks:**
- 8-11 AM: Cold calls to hot prospects (West Coast prime time)
- 11 AM-1 PM: LinkedIn messages and research
- 1-3 PM: Follow-ups and overdue touches
- 3-6 PM: Second round of calls + email sends

### 6. Email Draft Generator (`email_draft`)
**Channel:** Email
**Input:** contact_id (required)
**Steps:** load_prospect, load_research, generate_subject, generate_body, quality_gate, finalize
**Output:** 3 subject line options, email body, draft_id

### 7. Cold Call Prep (`call_prep`)
**Channel:** Phone
**Input:** contact_id (required)
**Steps:** load_prospect, load_research, generate_opener, generate_pain, generate_bridge
**Output:** 3-line call script (opener, pain hypothesis, bridge to ask)

**Rules:**
- Total script: 3 lines max
- Uses different proof point than InMail (if one exists)
- Opener references something specific about the prospect

## Triggering Workflows

### From the UI
1. Go to LinkedIn Channel page
2. Click a Quick Action button
3. Fill in the inputs
4. Click "Run Workflow"
5. View results in the modal
6. Copy drafts with one click

### From the API
```bash
# Generic endpoint
POST /api/workflows/execute
{"workflow_type": "account_research", "input": {"company_name": "Stripe"}}

# Or use specific endpoints
POST /api/workflows/account-research
POST /api/workflows/prospect-shortlist
POST /api/workflows/linkedin-draft
POST /api/workflows/followup-sequence
POST /api/workflows/daily-plan
POST /api/workflows/email-draft
POST /api/workflows/call-prep
```

## Viewing Results

- **Workflow Runs**: LinkedIn Channel page shows recent runs table
- **Run Details**: Click "View" on any run to see step-by-step execution log
- **Drafts**: Generated drafts appear in the LinkedIn Drafts section and the Drafts page
- **Research**: Account research briefs are stored as research_snapshots
