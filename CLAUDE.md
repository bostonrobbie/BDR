# BDR Outreach Command Center

BDR platform for LinkedIn, Email, and Call outreach to sales prospects. Human sends all messages manually.

## Key Files

| Component | File | Purpose |
|-----------|------|---------|
| Researcher | `src/agents/researcher.py` | Builds validated `ResearchArtifact` from CRM + cached data |
| Scorer | `src/agents/scorer.py` | Feature-based 0-100 scoring with `score_from_artifact()`, plus legacy 0-12 ICP |
| Message Writer | `src/agents/message_writer.py` | `generate_message_variants()` produces 3 tones (friendly/direct/curious) |
| Quality Gate | `src/agents/quality_gate.py` | 10 QC checks on message drafts |
| LLM Gateway | `src/agents/llm_gateway.py` | Unified Ollama client with retries, health checks, fallback |
| Scoring Config | `config/scoring_weights.json` | Tunable scoring weights (edit without code changes) |
| Product Config | `config/product_config.json` | Value props, proof points, CTAs, forbidden phrases |
| DB Models | `src/db/models.py` | CRUD for all tables |
| API | `src/api/app.py` | FastAPI backend, 40+ endpoints |

## Data Contracts

**Pipeline flow:** `ResearchArtifact` -> `ScoringResult` -> `MessageVariants`

- **ResearchArtifact**: structured research with evidence discipline. Every hook, pain, and tech stack item must cite an evidence source. See `build_research_artifact()` in researcher.py.
- **ScoringResult**: `{total_score, tier, feature_scores, feature_weights, reasons, missing_data}`. Deterministic, explainable. See `score_from_artifact()` in scorer.py.
- **MessageVariants**: 3 variants (friendly/direct/curious) with subject lines, proof points, CTAs. See `generate_message_variants()` in message_writer.py.

## Commands

```bash
# Run tests
python tests/unit/test_research_artifact.py
python tests/unit/test_scorer_v2.py
python tests/unit/test_message_writer_v2.py
python tests/unit/test_scoring.py
python tests/unit/test_quality_gate.py

# Run end-to-end pipeline (no LLM needed)
python scripts/run_pipeline.py

# LLM smoketest (needs Ollama running)
python scripts/llm_smoketest.py

# Start API server
uvicorn src.api.app:app --reload --port 8000

# Init DB
python src/db/init_db.py
```

## Coding Rules

- Messages must be grounded in ResearchArtifact evidence fields. Never hallucinate metrics, customers, or integrations.
- Every tech stack item, pain hypothesis (>0.7 confidence), and personalization hook requires an evidence string.
- Proof points must come from `config/product_config.json` only.
- No em dashes in outreach messages.
- Scoring weights are in `config/scoring_weights.json` - edit JSON, not code.
