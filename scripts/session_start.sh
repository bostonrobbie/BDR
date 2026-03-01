#!/bin/bash
# BDR Session Start - Orients Claude on current state
# Runs automatically when a Cowork session opens

set -e

BDR_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BATCHES_DIR="$BDR_ROOT/batches"
WORK_DIR="$BDR_ROOT/work"
REPLY_LOG="$WORK_DIR/reply-log.csv"
RESULTS_FILE="$WORK_DIR/results.json"

echo "=== BDR SESSION START ==="
echo "Date: $(date '+%Y-%m-%d %H:%M')"
echo ""

# Current batch number
LATEST_BATCH=$(ls -d "$BATCHES_DIR"/batch-* 2>/dev/null | sort -V | tail -1 | grep -oP 'batch-\K\d+' || echo "0")
echo "Latest batch: #$LATEST_BATCH"

# Count batch deliverables
BATCH_COUNT=$(ls -d "$BATCHES_DIR"/batch-* 2>/dev/null | wc -l)
echo "Total batches: $BATCH_COUNT"

# Email sequences
SEQ_COUNT=$(ls "$BATCHES_DIR"/email-sequences/*.md 2>/dev/null | wc -l)
echo "Email sequence files: $SEQ_COUNT"
echo ""

# Reply log status
if [ -f "$REPLY_LOG" ]; then
    TOTAL_REPLIES=$(tail -n +2 "$REPLY_LOG" 2>/dev/null | grep -c '[^[:space:]]' || true)
    POSITIVE=$(grep -c ",positive," "$REPLY_LOG" 2>/dev/null || true)
    MEETINGS=$(grep -c ",meeting_booked," "$REPLY_LOG" 2>/dev/null || true)
    echo "Reply log: ${TOTAL_REPLIES:-0} replies tracked (${POSITIVE:-0} positive, ${MEETINGS:-0} meetings)"
else
    echo "Reply log: Not started yet (run /follow-up to initialize)"
fi

# Results file
if [ -f "$RESULTS_FILE" ]; then
    echo "Results file: exists"
else
    echo "Results file: Not started yet"
fi
echo ""

# Memory layer status
echo "--- Memory Layer ---"
COMPETITORS=$(ls "$BDR_ROOT"/memory/competitors/*.md 2>/dev/null | wc -l)
WINS=$(find "$BDR_ROOT/memory/wins" -name "*.md" ! -name "_template.md" 2>/dev/null | wc -l)
LOSSES=$(find "$BDR_ROOT/memory/losses" -name "*.md" ! -name "_template.md" 2>/dev/null | wc -l)
CALL_NOTES=$(find "$BDR_ROOT/memory/call-notes" -name "*.md" ! -name "_template.md" 2>/dev/null | wc -l)
echo "Battle cards: $COMPETITORS | Wins: $WINS | Losses: $LOSSES | Call notes: $CALL_NOTES"
echo ""

# Pending work
echo "--- Quick Actions ---"
echo "Available commands: /prospect, /write-batch, /follow-up, /reply-handle, /pre-brief, /score-message"
echo "===================="
