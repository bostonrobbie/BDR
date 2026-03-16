# LinkedIn Channel

## Overview

The LinkedIn Channel tab is the primary workspace for LinkedIn-based BDR workflows. It provides quick access to all LinkedIn workflows, data import tools, and draft management.

## Location

Sidebar > System section > LinkedIn Channel (above Email Channel)

## Sections

### KPI Bar
Displays: Profiles imported, LinkedIn drafts generated, Messages sent (manual), Total workflow runs, Active runs, DRY RUN badge

### Quick Actions
Six workflow buttons:
- **Account Research** - Research a target company
- **Prospect Shortlist** - Score and rank prospects against ICP
- **Draft Messages** - Generate personalized InMail drafts
- **Follow-Up Sequence** - Create follow-up + break-up messages
- **Daily Plan** - Generate today's action checklist
- **Call Prep** - Generate 3-line call script

### Data Import

#### CSV Import
For Sales Navigator exports. Paste CSV data with columns:
```
first_name,last_name,title,company,linkedin_url,email,industry,location
```

The importer will:
- Parse CSV headers automatically
- Create contacts and accounts
- Link LinkedIn profiles
- Detect duplicates by LinkedIn URL
- Set persona type (QA leader vs VP Eng) based on title
- Set seniority level based on title keywords

#### Manual Paste
For copying profile text from LinkedIn:
1. Copy text from a LinkedIn profile page
2. Paste into the text area
3. Add the LinkedIn URL and company name
4. Click Import Profile

### Recent Workflow Runs
Table showing all LinkedIn workflow executions with status, steps completed, duration, and a "View" button for detailed logs.

### LinkedIn Drafts
Displays the most recent LinkedIn message drafts with:
- Subject line and touch type
- Message body preview
- Word count, proof point used, personalization score
- Copy button for quick clipboard copy

## Safety

The DRY RUN badge is always visible at the top of the page. When DRY RUN is ON (default):
- No LinkedIn messages can be sent
- No connection requests can be made
- No InMails can be sent
- Only drafts and research outputs are produced
- All workflow runs are logged for audit

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/linkedin/stats | GET | LinkedIn channel statistics |
| /api/linkedin/profiles | GET | List imported profiles |
| /api/linkedin/profiles/{id} | GET | Get single profile |
| /api/linkedin/profiles/import | POST | Import single profile |
| /api/linkedin/profiles/import-csv | POST | Bulk CSV import |
