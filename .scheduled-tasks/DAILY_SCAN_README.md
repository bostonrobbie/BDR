# Daily Pipeline Scan — How to Run

## Option 1: Start a New Cowork Session (Recommended)
Open a new Cowork session and paste this:

```
Read the file daily_pipeline_scan_prompt.md and execute the full daily scan process. Today's date is [TODAY]. Save the report to daily_scan_reports/scan_[TODAY].md. Compare against yesterday's report if it exists.
```

This triggers the full pipeline scan using all the SOPs and processes we've built.

## Option 2: CLI Script
Run from terminal:
```bash
./path/to/.scheduled-tasks/run-daily-pipeline-scan.sh
```

## Option 3: Cron (Automated 6AM Daily)
```bash
crontab -e
# Add this line:
0 6 * * * /path/to/.scheduled-tasks/run-daily-pipeline-scan.sh
```

## What the Scan Does

1. **Pipeline Health** — Pulls sequence metrics (contacts, step distribution, open/reply/bounce rates) and compares to yesterday
2. **Hot Intent Discovery** — Searches Apollo for new companies matching Tier 1 ICP (200+ employees, US, SaaS/enterprise/healthcare/fintech)
3. **Prospect Identification** — Finds QA/Engineering decision-makers at discovered companies
4. **9-Point Qualification** — Runs ALL checks (sequence dedup, ownership, email, job verification, triple-sequence, warm lead, 30-day cooldown)
5. **Email Drafting** — Writes personalized Touch 1 emails for all CLEAN prospects
6. **Quality Checks** — 0 em dashes, 0 buzzwords, correct subject/CTA/signature
7. **Daily Report** — Saves to `daily_scan_reports/scan_YYYY-MM-DD.md`
8. **SOP Tracking** — Notes which checks caught disqualifications, edge cases, and refinement suggestions

## Daily Target: 10-25 Qualified Prospects

## Files
- `daily_pipeline_scan_prompt.md` — The full self-contained SOP prompt
- `daily_scan_reports/` — All daily reports (day-over-day tracking)
- `run-daily-pipeline-scan.sh` — CLI runner script
- `daily-pipeline-scan.json` — Task configuration
