# BDR Repo ↔ Cowork Sync Guide

## Purpose
Maps what's in the GitHub repo (https://github.com/bostonrobbie/BDR.git) vs. what's in Cowork's working files. Use this when updating the repo with current work.

Last synced: 2026-03-01

---

## Critical Differences (Repo is OUTDATED in these areas)

### 1. CLAUDE.md — Message Style
| Area | Repo (OLD) | Cowork (CURRENT) |
|------|-----------|-----------------|
| Message style | C1 | **C2** (with Pre-Draft Steps 1-4, Single Theme Rule, Anti-pattern detection) |
| Touch sequence | 6-touch with cold calls | **3-touch** (2 InMail + 1 Email, no calls) |
| Research sources | 2 (LinkedIn + Company) | **3** (LinkedIn + Apollo + Company external) |
| Prospect mix | 12-15 QA + 8-10 VP Eng | **Data-driven**: 10-12 Manager/Lead, 4-6 Director, 3-5 Architect, 2-3 Buyer Intent, max 2 VP |
| Close rules | Generic acceptable | **Must tie proof point outcome to prospect's situation + "what day works"** |
| QA Gate | Basic | **14-point checklist + MQS >= 9/12** |

**Action:** Replace repo CLAUDE.md entirely with Cowork CLAUDE.md.

### 2. Missing Sections (Not in Repo at All)
| Section | Description |
|---------|-------------|
| Outbound Intelligence System | 1,326 conversation analysis, 10 Hard Constraints, Strong Preferences, timing matrix, phrase intelligence, MQS scoring |
| LinkedIn Safety & Compliance Rules | Pacing limits, session rules, account health monitoring, recovery protocol |
| Apollo Integration Strategy | Credit budget, sequence details, email accounts, enrichment workflow |
| Draft Safety & Cadence Enforcement | 7 rules from INC-001 (date-gating, TOUCH_ELIGIBLE_DATE, orphan prevention, etc.) |
| Incident Log | INC-001 documentation |
| "Run the Daily" Workflow | 5-phase automated daily outreach with adaptive logic |
| Intent-Based Outreach Pipeline SOP | 8-stage process for transferred accounts and buyer intent |
| Email-Only Sequence SOP | 5-touch 21-day email cadence for BDR-wide Apollo use |
| Warm/Inbound Lead SOP | Response framework for positive replies, referrals, demo requests |
| Module A1 (Known Person Blocker) | Past coworker detection |
| Module A2 (Already Messaged Blocker) | LinkedIn.com messaging history check |
| Follow-Up Schedule | Computed cadence dates for all batches |
| Master Send Log | Lifetime send totals with batch breakdowns |
| Email Send History | Feb 27-28 email tracking including INC-001 premature sends |

**Action:** All these sections exist in Cowork CLAUDE.md and should be copied to repo.

### 3. Scoring Engine (scoring_weights.json)
The repo has a sophisticated JSON-based scoring engine at `config/scoring_weights.json` with 7 feature categories, signal decay half-lives, and configurable thresholds. The Cowork CLAUDE.md has a simpler Priority Scoring section (1-5 scale with +/- factors).

**Action:** Keep BOTH. The JSON scoring engine is for the automated pipeline (Phase 1 MVP). The CLAUDE.md Priority Scoring is for manual batch building. They serve different purposes but should be aligned in their weight priorities.

### 4. Agent Code (src/agents/)
The repo has 15+ Python agent files that implement the automated pipeline. These are NOT used in Cowork sessions (Cowork uses Claude directly, not the Python agents). However, the agent logic should be consistent with the SOPs in CLAUDE.md.

Key agents to update:
| Agent | File | What Needs Updating |
|-------|------|-------------------|
| quality_gate.py | src/agents/quality_gate.py | Add all 14 QA Gate checks, MQS scoring, HC1-HC10, new Draft Safety rules |
| message_writer.py | src/agents/message_writer.py | Update to C2 style, Pre-Draft Steps, Close Construction rules |
| researcher.py | src/agents/researcher.py | Add Apollo as 3rd research source, tag research bullets |
| scorer.py | src/agents/scorer.py | Align with Cowork Priority Scoring factors |
| sequence_generator.py | src/agents/sequence_generator.py | Update to 3-touch cadence (was 6-touch) |

### 5. Prospect Tracker (data/trackers/prospect_master_tracker.md)
The repo tracker shows:
- 9 Step 2 prospects (buyer intent, emailed Feb 27)
- 30 Step 1 prospects (need email — these are the Apollo sequence website visitors)
- 13 Batch 3 website visitor prospects (added to Apollo sequence Feb 28)

This is a different pipeline than the Cowork batches. The "Step 1" and "Step 2" naming refers to Apollo sequence steps, not our Touch 1/Touch 2 naming.

**Action:** Clarify naming convention. "Step" = Apollo sequence step. "Touch" = our outreach cadence step. Keep both trackers but add cross-references.

---

## Files to Copy from Cowork → Repo

### Root Level
| Cowork File | Repo Destination | Action |
|-------------|-----------------|--------|
| CLAUDE.md | /CLAUDE.md | REPLACE (repo version is outdated) |
| EXECUTION-STATUS.md | /data/trackers/execution-status.md | NEW (doesn't exist in repo) |
| INCIDENT-LOG.md | /logs/incident-log.md | NEW |
| OPERATIONAL-SAFETY-CHECKLIST.md | /sops/operational-safety-checklist.md | NEW |
| BDR-REPO-SYNC-GUIDE.md | /docs/SYNC-GUIDE.md | NEW |

### Batch Trackers
| Cowork File | Repo Destination |
|-------------|-----------------|
| outreach-sent-feb26-batch3.html | /batches/batch3/outreach-sent-feb26-batch3.html |
| outreach-sent-feb27-batch5a.html | /batches/batch5a/outreach-sent-feb27-batch5a.html |
| outreach-sent-feb27-batch5b.html | /batches/batch5b/outreach-sent-feb27-batch5b.html |
| outreach-batch6-unsent.html | /batches/batch6/outreach-batch6.html |
| batch7-send-tracker.json | /batches/batch7/batch7-send-tracker.json |
| batch7-send-tracker.html | /batches/batch7/batch7-send-tracker.html |

### SOPs & Templates
| Cowork File | Repo Destination |
|-------------|-----------------|
| email-sequence-sop.html | /sops/email-sequence-sop.html |
| email-sequence-sop.docx | /sops/email-sequence-sop.docx |
| TEMPLATE_LIBRARY.md | /templates/TEMPLATE_LIBRARY.md |
| bdr-automation-pipeline-sop.docx | /sops/bdr-automation-pipeline-sop.docx |
| apollo-sequence-step-copy.md | /templates/apollo-sequence-step-copy.md |

### Analytics & Intelligence
| Cowork File | Repo Destination |
|-------------|-----------------|
| outreach-intelligence.html | /analytics/outreach-intelligence.html |
| outreach-intelligence-report.docx | /analytics/outreach-intelligence-report.docx |
| message-analytics-dashboard.html | /analytics/message-analytics-dashboard.html |

---

## Repo Strengths to Preserve (Don't Overwrite)

These repo features are NOT in Cowork and should be kept:

1. **config/scoring_weights.json** — Sophisticated lead scoring engine with decay functions
2. **src/agents/** — Python agent implementations (15+ files)
3. **src/db/schema.sql** — Database schema for the automated pipeline
4. **src/api/** — FastAPI backend code
5. **docs/ARCHITECTURE.md** — System architecture documentation
6. **docs/DATA_MODEL.md** — Database schema documentation
7. **docs/AGENT_SWARM.md** — Agent swarm design
8. **docs/ROADMAP.md** — 3-phase implementation plan
9. **batches/email-sequences/** — Historical email templates (useful for analysis)
10. **tests/** — Test files for the automated pipeline

---

## Naming Convention Alignment

| Concept | Cowork Term | Repo Term | Standard Going Forward |
|---------|------------|-----------|----------------------|
| Outreach step | Touch (Touch 1, 2, 3) | Step (Step 1, 2) | **Touch** for outreach cadence |
| Apollo sequence position | Step (Step 1, 2, 3, 4) | Step | **Apollo Step** (disambiguate) |
| Message quality | MQS (12-point) | Not defined | **MQS** |
| Quality validation | QA Gate (14 checks) | quality_gate.py | **QA Gate** |
| Lead temperature | Priority (1-5) | scoring_weights.json tiers | Keep both: Priority (manual) + Score (automated) |
| Message style | C2 | C1 | **C2** (C1 is deprecated) |
