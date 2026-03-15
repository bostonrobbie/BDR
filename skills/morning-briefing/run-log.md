# Run Log — Morning Briefing Skill

**Skill:** Morning Briefing (HTML Dashboard Generator)
**Created:** 2026-03-15
**Purpose:** Track execution history, data source availability, metric trends, and quality of generated dashboards

---

## Entry Format

Each run appends an entry with the following structure:

```markdown
### Run #[N] — [YYYY-MM-DD HH:MM]
- **Result:** [1-2 sentence summary]
- **Key metrics:** Overnight replies: [N] | Calendar events: [N] | Prospect meetings: [N] | T2/T3 due: [N] | Work queue: [N]
- **Anomalies:** [Data gaps, parse errors, unexpected findings]
- **Adjustments made this run:** [Deviations from SKILL.md if any]
- **Output quality:** [Accurate / Mostly accurate / Needs calibration / Failed]
- **File generated:** [Path or error]
```

If a run fails:
```markdown
### Run #[N] — [YYYY-MM-DD HH:MM] ❌ FAILED
- **Error:** [What went wrong]
- **Impact:** [What was skipped or incomplete]
- **Recovery:** [What to do next run]
```

---

## Runs

(Entries will be appended here after each execution.)

