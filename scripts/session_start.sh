#!/bin/bash
# BDR Session Start - Actionable intelligence for each Cowork session
# Reads structured state files instead of parsing large documents

set -e

BDR_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK_DIR="$BDR_ROOT/work"
PIPELINE_STATE="$WORK_DIR/pipeline-state.json"
DNC_LIST="$WORK_DIR/dnc-list.json"
FOLLOWUP_SCHEDULE="$WORK_DIR/follow-up-schedule.json"
REPLY_LOG="$WORK_DIR/reply-log.csv"
RESULTS_FILE="$WORK_DIR/results.json"

echo "=== BDR SESSION START ==="
echo "Date: $(date '+%Y-%m-%d %H:%M')"
echo ""

# --- Pipeline State ---
if [ -f "$PIPELINE_STATE" ]; then
    CREDITS=$(python3 -c "import json; d=json.load(open('$PIPELINE_STATE')); print(d.get('inmail_credits_remaining', '?'))" 2>/dev/null || echo "?")
    TOTAL_SENDS=$(python3 -c "import json; d=json.load(open('$PIPELINE_STATE')); print(d.get('total_sends_all_time', 0))" 2>/dev/null || echo "0")
    LATEST_BATCH=$(python3 -c "import json; d=json.load(open('$PIPELINE_STATE')); print(d.get('latest_batch_number', '?'))" 2>/dev/null || echo "?")
    CREDIT_ALERT=$(python3 -c "import json; d=json.load(open('$PIPELINE_STATE')); print(d.get('credit_alert', ''))" 2>/dev/null || echo "")
    UNSENT=$(python3 -c "import json; d=json.load(open('$PIPELINE_STATE')); print(d.get('unsent_prospects', 0))" 2>/dev/null || echo "0")

    echo "Credits: $CREDITS InMails remaining"
    if [ -n "$CREDIT_ALERT" ]; then
        echo "  *** $CREDIT_ALERT"
    fi
    echo "Sends: $TOTAL_SENDS all-time | Latest batch: #$LATEST_BATCH | Unsent: $UNSENT"

    # Warm leads
    WARM_COUNT=$(python3 -c "import json; d=json.load(open('$PIPELINE_STATE')); print(len(d.get('warm_leads', [])))" 2>/dev/null || echo "0")
    if [ "$WARM_COUNT" -gt 0 ]; then
        echo "Warm leads: $WARM_COUNT active"
        python3 -c "
import json
d = json.load(open('$PIPELINE_STATE'))
for lead in d.get('warm_leads', []):
    print(f\"  - {lead['name']} @ {lead['company']}: {lead.get('status', '?')} | Next: {lead.get('next_action', '?')}\")
" 2>/dev/null
    fi
else
    echo "Pipeline state: Not initialized (run a skill to create work/pipeline-state.json)"
fi
echo ""

# --- Follow-Up Queue ---
if [ -f "$FOLLOWUP_SCHEDULE" ]; then
    echo "--- Follow-Ups Due ---"
    python3 -c "
import json
from datetime import date
d = json.load(open('$FOLLOWUP_SCHEDULE'))
today = date.today().isoformat()
for batch_name, batch in d.get('batches', {}).items():
    t2 = batch.get('touch2_send', '')
    t3 = batch.get('touch3_send', '')
    n = batch.get('prospects', 0)
    notes = batch.get('special_cases', '')
    if today >= t2.split('/')[0] and today <= (t2.split('/')[-1] if '/' in t2 else t2):
        print(f'  Touch 2 due: {batch_name} ({n} prospects) - target {t2}')
    if today >= t3.split('/')[0] and today <= (t3.split('/')[-1] if '/' in t3 else t3):
        print(f'  Touch 3 due: {batch_name} ({n} prospects) - target {t3}')
summary = d.get('week_summary', {})
for week, data in summary.items():
    t2_due = data.get('touch2_inmail_due', 0)
    note = data.get('note', '')
    if t2_due > 0:
        print(f'  Week {week}: {t2_due} Touch 2 InMails due')
        if note:
            print(f'    *** {note}')
" 2>/dev/null
else
    echo "Follow-up schedule: Not initialized"
fi
echo ""

# --- DNC List ---
if [ -f "$DNC_LIST" ]; then
    DNC_COUNT=$(python3 -c "import json; d=json.load(open('$DNC_LIST')); print(len(d.get('contacts', [])))" 2>/dev/null || echo "0")
    echo "DNC list: $DNC_COUNT contacts"
fi

# --- Reply Log ---
if [ -f "$REPLY_LOG" ]; then
    TOTAL_REPLIES=$(tail -n +2 "$REPLY_LOG" 2>/dev/null | grep -c '[^[:space:]]' || true)
    POSITIVE=$(grep -c ",positive," "$REPLY_LOG" 2>/dev/null || true)
    MEETINGS=$(grep -c ",meeting_booked," "$REPLY_LOG" 2>/dev/null || true)
    echo "Replies: ${TOTAL_REPLIES:-0} tracked (${POSITIVE:-0} positive, ${MEETINGS:-0} meetings)"
else
    echo "Replies: None tracked yet"
fi
echo ""

# --- Memory Layer ---
COMPETITORS=$(ls "$BDR_ROOT"/memory/competitors/*.md 2>/dev/null | wc -l)
WINS=$(find "$BDR_ROOT/memory/wins" -name "*.md" ! -name "_template.md" 2>/dev/null | wc -l)
echo "Memory: $COMPETITORS battle cards | $WINS wins logged"
echo ""

# --- Quick Actions ---
echo "--- Commands ---"
echo "/prospect     Source new prospects"
echo "/write-batch  Research + draft all touches"
echo "/follow-up    Check due follow-ups"
echo "/reply-handle Triage replies"
echo "/pre-brief    Analyze past batch performance"
echo "/score-message Score a draft message"
echo "===================="
