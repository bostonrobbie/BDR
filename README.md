# BDR Second Brain

Rob Gorham's central repository for all BDR operations at Testsigma. This is the single source of truth for outreach knowledge, prospect data, messaging, tracking, and learning.

## How It Works

Every Claude Code session reads `CLAUDE.md` first, which points to modular knowledge files. Sessions can read, write, and update any part of this repo. Knowledge compounds over time as outreach data flows back in.

```
                    CLAUDE.md (session router)
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
         knowledge/   batches/    data/
         (the brain)  (the work)  (the evidence)
```

## Structure

```
BDR/
├── CLAUDE.md              # Session instructions - read this first
├── knowledge/             # Domain knowledge (11 modular files)
│   ├── me.md              # Rob's profile and preferences
│   ├── company.md         # Testsigma product and people
│   ├── icp.md             # Target personas and verticals
│   ├── proof-points.md    # Customer stories with numbers
│   ├── outreach-rules.md  # Writing style and message structure
│   ├── sequences.md       # Multi-channel touch sequences
│   ├── objections.md      # Objection handling and reply patterns
│   ├── scoring.md         # Priority, MQS, and personalization scoring
│   ├── data-insights.md   # Data-driven rules from 1,330 conversations
│   ├── workflows.md       # Sales Nav, A/B testing, feedback loops
│   └── deliverable-format.md  # HTML deliverable spec
├── batches/               # Generated prospect batches
├── data/                  # Raw data, analysis, databases
├── config/                # App configuration
├── src/                   # Application code (17 agents, API, UI, DB)
├── tests/                 # Test suites
└── docs/                  # Technical documentation
```

## Quick Reference

| I want to... | Go to... |
|--------------|----------|
| Build a prospect batch | `CLAUDE.md` > Common Tasks |
| Check writing rules | `knowledge/outreach-rules.md` |
| Find a proof point | `knowledge/proof-points.md` |
| See what's working | `knowledge/data-insights.md` |
| Score a prospect | `knowledge/scoring.md` |
| Handle an objection | `knowledge/objections.md` |
| Review past batches | `batches/` |

## Built For

Rob Gorham, BDR @ Testsigma
