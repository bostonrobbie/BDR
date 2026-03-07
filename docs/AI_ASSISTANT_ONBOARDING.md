# AI Assistant Onboarding (Source of Truth)

Use this file as the **first read** for any AI assistant working in this repo.

## 1) Mission and Scope
This repository supports BDR outreach operations, including:
- prospect research,
- message drafting,
- sequence execution support,
- QA and tracking,
- local analytics and pipeline tooling.

## 2) Fast Start (5 minutes)
1. Read [`README.md`](../README.md) for system and setup context.
2. Read [`docs/ARCHITECTURE.md`](ARCHITECTURE.md) for component boundaries.
3. Read canonical SOP index: [`docs/sops/README.md`](sops/README.md).
4. Read the two primary SOPs listed there end-to-end.
5. Run tests before making claims or edits.

## 3) Canonical Operating Rules for AI Assistants
- Prefer Markdown docs in `docs/` as source of truth.
- Treat non-doc files in root (reports, exports, snapshots) as historical artifacts unless linked by docs.
- Do not invent process steps when SOPs already define them.
- If SOP content conflicts with implementation, document the mismatch and propose a patch.
- Keep changes minimal, traceable, and reversible.

## 4) Required Pre-Work Before Any Change
- Confirm current branch status and latest commits.
- Read impacted module docs before editing code.
- Identify whether change affects:
  - outreach rules,
  - QA gates,
  - sequence timing,
  - tracker format,
  - API/UI behavior.

## 5) Definition of Done for AI Contributions
A change is complete only if:
- docs are updated (if behavior/process changed),
- tests/checks were executed,
- output includes exact commands run,
- assumptions and limitations are explicitly called out.

## 6) “Stay Up to Date” Workflow (for any AI)
When an assistant starts work:

```bash
git fetch --all --prune
git pull --ff-only
python -m pip install -r requirements.txt
pytest -q
```

If `git pull --ff-only` fails, assistant should stop and report branch divergence with a suggested rebase/merge plan.

## 7) Repository Navigation Map
- `README.md` → primary setup + project overview.
- `docs/` → architecture, runbooks, SOPs, roadmap.
- `docs/sops/README.md` → **canonical SOP index** (start here for process work).
- `scripts/` → operational helpers and maintenance scripts.
- `tests/` → unit + integration coverage.
- `data/trackers/` → operational tracking datasets and markdown trackers.

## 8) Handoff Template (AI → Human/AI)
Every assistant handoff should include:
- Objective
- Files changed
- Commands run + outcomes
- Risks / follow-up
- If SOP impacted: exact SOP section updated

---

Maintainers: if process changes, update this file first, then SOP index, then README links.
