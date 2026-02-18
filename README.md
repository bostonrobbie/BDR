# Outreach Command Center

A local-first BDR operations platform that consolidates LinkedIn, Email, and Calls into a single dashboard with AI-powered research, drafting, and analytics.

## What It Does

- **Researches** prospects and companies using structured extraction from Sales Navigator and web sources
- **Drafts** personalized, human-sounding outreach for all channels (LinkedIn InMail, email, cold calls)
- **Tracks** every touchpoint, reply, and outcome in a local SQLite database
- **Learns** from accumulated data to improve messaging over time
- **Manages** follow-up sequences, call prep, and meeting handoff
- **Experiments** with A/B testing on messaging variables

## What It Does NOT Do

- Send messages or emails (you copy, paste, and send manually)
- Log into platforms autonomously
- Make financial transactions or store credentials

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React (single HTML via CDN) |
| Backend | Python FastAPI |
| Database | SQLite |
| AI Engine | Claude via Cowork |
| Browser Bridge | Claude in Chrome MCP |

## Project Structure

```
BDR/
├── docs/              # Architecture, data model, agent design, roadmap
├── src/
│   ├── api/           # FastAPI backend
│   ├── agents/        # Agent definitions and prompts
│   ├── db/            # Database schema and migrations
│   └── ui/            # Dashboard frontend
├── templates/         # Message templates by channel and persona
├── research/          # Cached company and prospect research
├── batches/           # Batch-specific deliverables
├── logs/              # Agent run logs and error logs
├── analytics/         # Generated dashboards and reports
├── sops/              # Standard operating procedures
└── tests/             # Unit, integration, and E2E tests
```

## Quick Start

```bash
# Initialize the database
cd src/db
python init_db.py

# Start the API server (coming in v1)
cd src/api
uvicorn server:app --port 3001

# Open the dashboard
open src/ui/dashboard.html
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - System overview, tech stack, design principles
- [Data Model](docs/DATA_MODEL.md) - Database schema, tables, relationships
- [Agent Swarm](docs/AGENT_SWARM.md) - Agent roles, communication, safety
- [Roadmap](docs/ROADMAP.md) - MVP → v1 → v2 build plan

## Built For

Rob Gorham, BDR @ Testsigma
