#!/bin/bash
# Daily Pipeline Scan & Hot Intent Prospecting
# Schedule: 0 6 * * * (6AM daily, local timezone)
# Created: March 2, 2026
#
# Usage:
#   ./run-daily-pipeline-scan.sh          # Run the daily scan
#   crontab -e → 0 6 * * * /path/to/run-daily-pipeline-scan.sh
#
# This script invokes Claude with the full self-contained SOP prompt
# to scan the pipeline, find hot intent accounts, qualify prospects,
# and produce a daily briefing report.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORK_DIR="$(dirname "$SCRIPT_DIR")"
PROMPT_FILE="$WORK_DIR/daily_pipeline_scan_prompt.md"
REPORT_DIR="$WORK_DIR/daily_scan_reports"
TODAY=$(date +%Y-%m-%d)
LOG_FILE="$REPORT_DIR/scan_${TODAY}.log"

# Ensure output dir exists
mkdir -p "$REPORT_DIR"

echo "[$(date)] Starting daily pipeline scan..." | tee "$LOG_FILE"

# Run Claude with the full prompt in non-interactive mode
claude -p \
  --dangerously-skip-permissions \
  --add-dir "$WORK_DIR" \
  "$(cat "$PROMPT_FILE")

IMPORTANT: Today's date is ${TODAY}. Save the daily report to: daily_scan_reports/scan_${TODAY}.md

Read the prior day's report from daily_scan_reports/ (if it exists) for day-over-day comparison. If no prior report exists, establish today as the baseline.

After completing the scan, update prospect_master_tracker.md with any new prospects found." \
  2>&1 | tee -a "$LOG_FILE"

echo "[$(date)] Daily pipeline scan complete." | tee -a "$LOG_FILE"
