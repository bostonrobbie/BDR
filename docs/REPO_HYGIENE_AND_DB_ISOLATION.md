# Repo Hygiene + Channel DB Isolation

## What was reviewed
A full-file inventory was reviewed and a repeatable audit script was added to flag likely stale artifacts.

Run:
```bash
python scripts/repo_hygiene_audit.py
```

## Organization policy (going forward)
- Keep production code in `src/`, API handlers in `api/`, docs in `docs/`, trackers in `data/trackers/`, and batch outputs in `batches/` or `archive/`.
- Do not keep new generated one-off HTML/TXT/DOCX artifacts in repo root.
- Move dated run outputs to `archive/` by batch/date.

## Isolated databases (Email vs LinkedIn)
To keep Email and LinkedIn operations separate while retaining the same schema shape:

- **Email DB**: `api/data/outreach_email.db`
- **LinkedIn DB**: `api/data/outreach_linkedin.db`

Both databases are initialized from the same source schema so tables/columns remain compatible.

### Initialize isolated DBs
```bash
python scripts/init_isolated_channel_dbs.py \
  --source api/data/outreach_seed.db \
  --email-db api/data/outreach_email.db \
  --linkedin-db api/data/outreach_linkedin.db
```

### Data rules
- Shared baseline tables (accounts, contacts, workflows, feature_flags) are copied to both DBs.
- Channel activity tables copy only channel-matching rows when a `channel` column exists.
- This preserves the same data model while isolating channel histories, drafts, and tracking.

## Operational clarity
- LinkedIn SOP: `memory/sop-outreach.md`
- Email SOP: `memory/sop-email.md`

These SOPs are now explicitly channel-scoped and should be executed independently.


## Operational runbook
- DB write/update process for Apollo + local DB sync: `docs/DB_UPDATE_RUNBOOK.md`
