# Outreach Command Center - Overview

## What It Is

The Outreach Command Center (OCC) is a BDR automation dashboard that helps you research prospects, generate personalized outreach drafts, plan your day, and track your pipeline, all from a single interface deployed on Vercel.

## Architecture

- **Frontend**: Single-file HTML dashboard (`public/index.html`) with inline CSS/JS, Chart.js for visualizations
- **Backend**: Python FastAPI serverless function (`api/index.py`) deployed as a Vercel serverless function
- **Database**: SQLite in `/tmp` (reinitialized on cold start with seed data)
- **Safety**: DRY_RUN mode always active, no outbound actions ever

## Pages

| Page | Purpose |
|------|---------|
| Home | KPIs, pipeline funnel chart, action queue |
| Pipeline | All contacts sorted by priority score |
| Launch Batch | Configure and launch a new prospect batch |
| Approval Queue | Review and approve/reject message drafts |
| **LinkedIn Channel** | Run workflows, import profiles, view drafts |
| Email Channel | Email sender health, identities, suppression |
| Activity Timeline | All actions across channels |
| Workflows | Flow catalog and run history |
| Accounts | Company records with ICP signals |
| Contacts | Prospect database with filters |
| Drafts | All message drafts across channels |
| Intelligence | Reply rate analytics, A/B results, trends |
| Experiments | A/B test tracking |
| Signals | Re-engagement triggers |
| Agent Logs | AI agent execution history |
| Swarm | Parallel agent execution |
| Health | System status, feature flags, DB tables |
| Settings | User preferences, API config |

## Key Features

1. **Workflow Engine** - 7 pre-built workflows for BDR tasks (Account Research, Prospect Shortlist, LinkedIn Drafts, Follow-ups, Daily Plan, Email Drafts, Call Prep)
2. **SOP Compliance** - All generated content follows the writing rules: no em-dashes, 70-120 word InMails, varied proof points, personalization scoring
3. **Safety First** - DRY_RUN always on, no outbound actions, all outputs are drafts only
4. **LinkedIn Integration** - CSV import from Sales Navigator, manual profile paste, personalized message generation
5. **Analytics** - Reply rates by persona/vertical/proof point, A/B experiment tracking, batch comparison

## Deployment

- **URL**: https://bdr-outreach.vercel.app
- **GitHub**: https://github.com/bostonrobbie/BDR
- **Auto-deploy**: Push to `main` triggers Vercel build
