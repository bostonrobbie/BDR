# BDR Second Brain

Central repo for all of Rob Gorham's BDR work at Testsigma. Every Claude Code session reads from and writes to this repo.

## Who I Am
Rob Gorham, BDR at Testsigma. See `knowledge/me.md` for full profile and preferences.

## Knowledge Base (`knowledge/`)

All institutional knowledge lives here. Read the relevant files before doing any work.

| File | What's In It |
|------|-------------|
| `knowledge/me.md` | Rob's profile, preferences, outreach stats |
| `knowledge/company.md` | Testsigma product, people, value props, key customers |
| `knowledge/icp.md` | Target personas, verticals, prospect mix ratios, qualification checklist |
| `knowledge/proof-points.md` | Customer stories with numbers, rotation logic, vertical matching |
| `knowledge/outreach-rules.md` | Writing style rules, C1 message structure, common pitfalls |
| `knowledge/sequences.md` | Multi-channel touch sequence, cold call prep, re-engagement triggers |
| `knowledge/objections.md` | Objection pre-mapping, reply patterns, reply tagging |
| `knowledge/scoring.md` | Priority scoring (1-5), MQS (12-point), personalization scoring, QA gate |
| `knowledge/data-insights.md` | Hard constraints (HC1-HC7) and strong preferences from 1,330 conversation analysis |
| `knowledge/workflows.md` | Sales Nav workflow, research requirements, A/B testing, feedback loop, meeting prep |
| `knowledge/deliverable-format.md` | HTML deliverable structure, file naming, dashboard spec |

## Repo Structure

```
BDR/
├── CLAUDE.md              # This file - session instructions
├── knowledge/             # All domain knowledge (the second brain)
├── batches/               # Batch deliverables (the work product)
│   ├── batch-1/
│   ├── batch-2/
│   └── batch-N/
├── data/                  # Raw data, analysis, databases
│   ├── linkedin-conversations-full.xlsx
│   ├── analysis_output.json
│   ├── linkedin-outreach-analysis.docx
│   ├── outreach_seed.db
│   └── proof_points.json
├── config/                # App configuration (scoring weights, verticals, product config)
├── src/                   # Application code
│   ├── agents/            # 17 specialized agents
│   ├── api/               # FastAPI backend
│   ├── db/                # Database layer (15 tables)
│   └── ui/                # Dashboard frontend
├── tests/                 # All test suites
└── docs/                  # Technical documentation
```

## Session Rules

### Before Starting Any Task
1. Read the relevant `knowledge/` files for the task at hand
2. If building a batch, read ALL previous batch files in `batches/` first for the feedback loop
3. Check `data/analysis_output.json` for the latest data-driven rules

### Where to Put Things
| What | Where |
|------|-------|
| New batch deliverables | `batches/batch-[#]/prospect-outreach-[#]-[date].html` |
| Batch data bundles | `batches/batch-[#]/run-bundle-batch[#].json` |
| Updated knowledge or rules | Edit the relevant file in `knowledge/` |
| New analysis or reports | `data/` |
| Dashboard HTML | `batches/outreach-dashboard.html` |
| Code changes | `src/` |
| New tests | `tests/` |

### When Updating Knowledge
- If you learn something new (a pattern that works, a rule to add, a proof point update), update the relevant `knowledge/` file directly
- If Rob gives new instructions or preferences, update `knowledge/me.md` or the relevant file
- Keep knowledge files concise and scannable - tables over paragraphs

### Writing Messages
Read these files in order before writing any outreach:
1. `knowledge/outreach-rules.md` - Style and structure
2. `knowledge/data-insights.md` - Hard constraints and preferences
3. `knowledge/proof-points.md` - Available proof points
4. `knowledge/scoring.md` - QA gate requirements

### Common Tasks
| Task | What to Do |
|------|-----------|
| **Build a prospect batch** | Read all `knowledge/` files + previous batches. Generate Pre-Brief. Build HTML deliverable in `batches/batch-[#]/`. |
| **Write outreach messages** | Follow `outreach-rules.md` + `data-insights.md`. Run QA gate from `scoring.md`. |
| **Update what's working** | Edit `knowledge/data-insights.md` or `knowledge/proof-points.md` based on reply data. |
| **Add a new proof point** | Add to `knowledge/proof-points.md` with vertical matching. |
| **Change scoring rules** | Edit `knowledge/scoring.md` and `config/scoring_weights.json`. |
| **Prep for a meeting** | Follow meeting prep format in `knowledge/workflows.md`. |
| **Generate dashboard** | Read all batch files, generate `batches/outreach-dashboard.html`. |

## Style Rules (Always Apply)
- NO em dashes. Use commas or short hyphens only.
- Messages must sound like Rob wrote them personally.
- Under 100 words for Touch 1. Under 120 absolute max.
- Never "show your work" - no "I noticed" or "I saw" or profile recaps.
- At least one question mark. Close with a question mark.
- No easy-out lines. No "no worries" or "if not, all good."
- Always run QA gate (HC1-HC7 + MQS >= 9) before presenting messages.
