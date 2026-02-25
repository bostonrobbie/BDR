# BDR Outreach Command Center

AI-assisted BDR platform for LinkedIn, Email, and Call outreach. Human sends all messages manually. Every claim in outreach must be grounded in evidence.

## Architecture

```
Pipeline:  Contact + Account
               │
               ▼
         ┌─────────────┐     config/vertical_pains.json
         │  Researcher  │◄──── (per-vertical pain library)
         │  researcher.py│
         └──────┬──────┘
                │ ResearchArtifact
                ▼
         ┌─────────────┐     config/scoring_weights.json
         │   Scorer     │◄──── (tunable weights, decay, thresholds)
         │  scorer.py   │
         └──────┬──────┘
                │ ScoringResult
                ▼
         ┌─────────────┐     config/product_config.json
         │ Msg Writer   │◄──── (proof points, CTAs, forbidden phrases)
         │ message_writer│
         └──────┬──────┘
                │ MessageVariants (3 tones × 5 subject styles)
                ▼
         ┌─────────────┐
         │ Quality Gate │──── 10 QC checks per variant
         │ quality_gate │
         └──────┬──────┘
                │
                ▼
         ┌─────────────┐
         │ Channel Opt  │──── LinkedIn preview scoring, truncation
         │ linkedin_opt │
         └──────┬──────┘
                │
                ▼
          Human Review & Send
                │
                ▼
         ┌─────────────┐
         │  Feedback    │──── Reply sentiment, contradictions,
         │  Tracker     │     attribution chain, pain refinement
         └─────────────┘
```

## File Map

### Core Agents (`src/agents/`)

| File | Lines | Key Functions |
|------|-------|---------------|
| `researcher.py` | 887 | `build_research_artifact()`, `get_vertical_pains()` |
| `scorer.py` | 857 | `score_from_artifact()`, `compute_decay_factor()`, `score_pain_specificity()`, `compare_weight_configs()` |
| `message_writer.py` | 2106 | `generate_message_variants()`, `render_for_channel()`, `generate_subject_lines()`, `predict_objection_from_artifact()` |
| `quality_gate.py` | ~200 | `check_message_variant()` — 10 QC checks |
| `feedback_tracker.py` | 1357 | `record_reply()`, `score_reply_sentiment()`, `detect_contradictions_in_reply()`, `refine_pains_from_reply()`, `get_conversion_stats()`, `get_full_funnel_attribution()` |
| `message_components.py` | 302 | `score_opener()`, `score_pain_sentence()`, `score_proof_bridge()`, `score_cta()`, `score_message_components()` |
| `linkedin_optimizer.py` | 296 | `score_preview()`, `optimize_for_preview()`, `rank_variants_by_preview()` |
| `sequence_generator.py` | 497 | Sequence templates for multi-touch campaigns |
| `signal_enrichment.py` | 613 | Signal enrichment pipeline |
| `llm_gateway.py` | 317 | Unified Ollama client with retries, health checks, fallback |
| `llm_polish.py` | 263 | LLM-based message polishing (optional) |
| `deliverable_generator.py` | 978 | Pre-brief and deliverable generation |
| `batch_builder.py` | 376 | Batch processing for bulk outreach |
| `swarm_supervisor.py` | 586 | Multi-agent orchestration |
| `prospector.py` | 351 | Prospect discovery |
| `pre_brief.py` | 191 | Pre-call briefing documents |
| `ab_assigner.py` | 120 | A/B test group assignment |

### Data Layer (`src/db/`)

| File | Lines | Purpose |
|------|-------|---------|
| `models.py` | 1631 | CRUD for all tables: `create_contact()`, `create_account()`, `create_message_draft()`, `log_touchpoint()`, etc. |
| `init_db.py` | 393 | Schema DDL for 16+ tables |
| `migrate_v2.py` | 326 | Schema migrations |

### API (`src/api/`)

| File | Lines | Purpose |
|------|-------|---------|
| `app.py` | 1879 | FastAPI backend, 100+ endpoints |
| `pipeline_runner.py` | 494 | End-to-end pipeline orchestration |

### Config (`config/`)

| File | Purpose |
|------|---------|
| `scoring_weights.json` | Feature weights, thresholds, signal decay half-lives — edit JSON, not code |
| `product_config.json` | Value props, proof points, CTAs, forbidden phrases |
| `vertical_pains.json` | Per-vertical pain library (9 verticals with curated pains) |

### Scripts (`scripts/`)

| File | Purpose |
|------|---------|
| `run_tests.py` | Unified test runner — `python scripts/run_tests.py [group]` |
| `run_pipeline.py` | End-to-end pipeline demo (no LLM needed) |
| `rescore_stale.py` | Decay-aware re-scoring cron job |
| `llm_smoketest.py` | Ollama connectivity check |

## Data Contracts

**Pipeline:** `ResearchArtifact` → `ScoringResult` → `MessageVariants`

### ResearchArtifact
Built by `build_research_artifact()`. Every hook, pain, and tech stack item must cite an evidence source.
```python
{
    "contact": {...},
    "account": {...},
    "hooks": [{"hook": str, "evidence": str, "source": str}],
    "pain_hypotheses": [{"pain": str, "confidence": float, "evidence": str}],
    "tech_stack": [{"tool": str, "evidence": str}],
    "signals": [...],
    "data_quality": {...}
}
```

### ScoringResult
Returned by `score_from_artifact()`. Deterministic, explainable. 7 features summing to 100 max.
```python
{
    "total_score": int,        # 0-100
    "tier": str,               # hot/warm/cool/cold
    "feature_scores": {        # 7 features
        "title_seniority": int,
        "function_match": int,
        "company_size_fit": int,
        "industry_fit": int,
        "pain_confidence": int,
        "intent_signal": int,
        "data_quality": int,
    },
    "feature_weights": {...},  # sum to 100
    "reasons": [str],          # human-readable explanations
    "missing_data": [str],
    "decay_applied": [...]     # signal decay audit trail
}
```

### MessageVariants
Returned by `generate_message_variants()`. 3 tones × 5 subject styles. Sequence-aware via `touch_number`.
```python
{
    "variants": [
        {
            "tone": "friendly|direct|curious",
            "body": str,
            "subject_lines": [{...}],
            "proof_point": str,
            "proof_point_key": str,
            "cta": str,
            "opener": str,
            "opener_evidence": str,
            "predicted_objection": str,
            "objection_key": str,
            "touch_number": int,
        }
    ],
    "qa_results": [...],
    "metadata": {...}
}
```

## Commands

```bash
# Run ALL tests (233 tests across 7 groups)
python scripts/run_tests.py

# Run specific test group
python scripts/run_tests.py scorer      # Scoring: ICP, v2 scorer, decay, A/B, pain specificity
python scripts/run_tests.py messages    # Messages: variants, objections, components, subjects, channels
python scripts/run_tests.py feedback    # Feedback: tracking, sentiment, contradictions, attribution
python scripts/run_tests.py researcher  # Research artifact builder
python scripts/run_tests.py quality     # Quality gate checks
python scripts/run_tests.py sequences   # Sequence generation, LinkedIn optimization
python scripts/run_tests.py other       # Signal enrichment, LLM polish

# Run end-to-end pipeline (no LLM needed)
python scripts/run_pipeline.py

# Re-score stale contacts (decay-aware)
python scripts/rescore_stale.py --dry-run
python scripts/rescore_stale.py --threshold 0.3

# Start API server
uvicorn src.api.app:app --reload --port 8000

# Init DB
python src/db/init_db.py

# LLM smoketest (needs Ollama running)
python scripts/llm_smoketest.py
```

## Coding Rules

1. **Evidence grounding**: Messages must be grounded in ResearchArtifact evidence fields. Never hallucinate metrics, customers, or integrations.
2. **Evidence required**: Every tech stack item, pain hypothesis (>0.7 confidence), and personalization hook requires an evidence string.
3. **Proof points from config only**: Proof points must come from `config/product_config.json`. Never invent proof points.
4. **No em dashes**: Never use em dashes (—) or en dashes (–) in outreach messages.
5. **Scoring weights in JSON**: Edit `config/scoring_weights.json` for weight changes, not scorer.py code.
6. **Vertical pains in JSON**: Edit `config/vertical_pains.json` for vertical-specific pain hypotheses.
7. **Touch-number awareness**: `generate_message_variants()` accepts `touch_number` (1-6+). Touch 1 = full intro, 3-5 = shorter follow-up, 6+ = break-up.
8. **Attribution chain**: Every reply and meeting flows back through `record_reply()` which auto-scores sentiment and detects contradictions.
9. **Forbidden phrases**: Defined in `product_config.json`. Quality gate enforces them.
10. **Channel limits**: LinkedIn connection = 300 chars, InMail = 1900 chars, Email = no hard limit.

## Test Layout

```
tests/unit/
├── test_scorer.py              # 38 tests: ICP scoring, v2 scorer, decay, A/B, pain specificity
├── test_message_writer.py      # 35 tests: variants, QA, objections, components, subject lines
├── test_feedback.py            # 29 tests: tracking, sentiment, contradictions, attribution
├── test_channels.py            # 33 tests: LinkedIn optimizer, channel rendering, truncation
├── test_research_artifact.py   # 10 tests: artifact builder
├── test_quality_gate.py        #  8 tests: QC checks
├── test_wiring_enhancements.py # 11 tests: sentiment wiring, contradiction auto-trigger
├── test_intelligence_enhancements.py  # 26 tests: vertical pains, sequences, rescore, pain refinement
├── test_sequence_generator.py  # 15 tests: sequence templates
├── test_signal_enrichment.py   # 18 tests: signal pipeline
├── test_llm_polish.py          # 10 tests: LLM polishing
└── test_api.py                 # API integration tests
```

## Common Tasks

**Add a new proof point**: Edit `config/product_config.json` → add entry under `proof_points` → tests auto-validate.

**Add a new vertical**: Edit `config/vertical_pains.json` → add entry under `verticals` with pains, typical_tools, compliance_sensitive.

**Adjust scoring**: Edit `config/scoring_weights.json` → change feature weights or thresholds. Use `compare_weight_configs()` to A/B test.

**Add a new signal type**: Add decay half-life in `config/scoring_weights.json` under `signal_decay.half_lives`.

**Test a single module**: `python scripts/run_tests.py scorer` (or messages, feedback, etc.)

**Re-score after config change**: `python scripts/rescore_stale.py --dry-run` to preview, then without `--dry-run` to apply.
