# Pipeline Tracker

**Version:** 1.0 — Created Mar 15, 2026

**Trigger Keywords:** "show pipeline", "pipeline board", "where are my deals", "pipeline view", "pipeline status"

**Optional Add-on:** Can be appended to morning-briefing (weekday 6:00 AM)

**Output:** `analytics/dashboards/pipeline-board-[YYYY-MM-DD].html` (self-contained, opens in browser)

---

## Purpose

Generate a visual HTML pipeline board that reads warm-leads.md and pipeline-state.md, renders a clean HTML kanban-style view with contacts grouped by stage, color-coded by priority, with action flags for who needs attention today.

Rob books meetings for Testsigma's sales team. This is his CRM substitute (no Salesforce due to 2FA). The board shows all active warm prospects in one place, ranked by engagement temperature and action urgency.

---

## Workflow

### Phase 1 — Parse Pipeline Data

**Read `memory/warm-leads.md`:**
- Extract all P0, P1, P2, P3 contacts from the structured list
- For each contact, capture:
  - Name
  - Company
  - Title / Role
  - Priority (P0–P3)
  - Last contact date
  - Status notes (1–2 sentence context)
  - Next action (e.g., "Follow up T2", "Schedule meeting", "Awaiting reply")
  - Re-engage date (if applicable for P2/P3)

**Read `memory/pipeline-state.md`:**
- Supplement with additional stage info
- Extract meeting outcomes / call notes
- Identify contacts with recent wins or blockers
- Track meetings booked this calendar month

### Phase 2 — Stage Classification

Map each contact to a pipeline stage based on last activity and next action:

| Stage | Criteria | Priority | Color |
|-------|----------|----------|-------|
| **Replied — Hot** | Reply received in last 3 days, positive signal, meeting being scheduled | P0 | Green border |
| **Meeting Booked** | Calendar invite sent/confirmed, not yet happened | P0 | Green border |
| **Meeting Held** | Call or meeting completed, follow-up in progress | P0/P1 | Green or yellow border |
| **Engaged — Nurturing** | Replied with interest, no meeting scheduled yet, active thread | P1 | Yellow border |
| **Soft Interest** | Mild engagement (opened email, soft reply), re-engage window coming | P2 | Orange border |
| **Monitor** | Cold lead, declined, or no reply after T1. Watch for trigger events | P3 | Gray border |
| **Re-Engage Window Open** | P2 re-engage date has passed, ready to re-contact with new trigger | P2 | Orange border + "RE-ENGAGE NOW" badge |

### Phase 3 — Generate HTML Board

Build a self-contained HTML file with the following design:

**Styling:**
- Dark background: `#0f1117` (GitHub dark)
- Card-based layout with horizontal swimlanes (stage rows)
- Font: system sans-serif for readability
- Responsive width (min 1200px recommended)

**Structure:**
- Header: "Pipeline Board — [date]"
- Snapshot stats bar (total, P0, P1, P2, P3, meetings booked this month)
- 6 swimlanes, one per stage (top to bottom: Replied — Hot, Meeting Booked, Meeting Held, Engaged — Nurturing, Soft Interest, Monitor)
- Each card = one contact

**Card Layout (per contact):**
```
┌─────────────────────────────────────┐
│ ⭐ P0 BADGE (if applicable)         │
│ NAME (bold, 16px)                   │
│ Company Title — Role                │
│ Last contact: 3 days ago            │
│ Status: "Replied positively..."     │
│ Next action: [Follow up T2] [•••]   │
└─────────────────────────────────────┘
```

**Card Features:**
- **Top-left badge:** P0 (green), P1 (yellow), P2 (orange), P3 (gray)
- **Left border:** Colored stripe matching priority (3px wide)
- **Action Needed Badge:** Red "ACTION NEEDED" pill if:
  - Last contact > 5 days ago AND
  - No scheduled follow-up in next 7 days
- **Next Action Pill:** Tag showing next step (e.g., "Follow up T2", "Schedule meeting", "Re-engage now", "Awaiting reply")
- **Hover effect:** Slight shadow increase, subtle background shift

**Header Stats Bar:**
```
Total Warm Leads: 47 | P0 (Hot): 8 | P1 (Engaged): 12 | P2 (Soft): 18 | P3 (Monitor): 9 | Meetings Booked (this month): 5
```

**No Scrolling:** All content fits on one page (adjust swimlane height if needed).

### Phase 4 — Action Flags (Text Output)

After rendering the board, generate a plain-text summary for inline response:

```
📌 TODAY'S PIPELINE ACTIONS

🔴 ACTION NEEDED (overdue, no follow-up scheduled):
1. [Name] at [Company] — Days since last contact: 7 | Next: Follow up T2
2. [Name] at [Company] — Days since last contact: 9 | Next: Schedule meeting

🟢 HOT (P0 — reply received, meeting pending):
1. [Name] at [Company] — Reply 2 days ago | Next: Schedule meeting

🟡 ENGAGED (P1 — warm thread, no meeting yet):
1. [Name] at [Company] — Last contact 3 days ago | Next: Await reply

🟠 RE-ENGAGE READY (P2 — re-engage window open):
1. [Name] at [Company] — Re-engage date: TODAY | Trigger: [reason]

Total warm leads: 47 | Meetings booked this month: 5 | Avg days to booking: 4.2
```

This summary is printed to chat so Rob sees action items without opening the HTML file.

### Phase 5 — Save and Link

- Save HTML to: `/Work/analytics/dashboards/pipeline-board-[YYYY-MM-DD].html`
- Use today's date in filename
- Provide clickable link in response: `file:///sessions/funny-nifty-dirac/mnt/Work/analytics/dashboards/pipeline-board-[YYYY-MM-DD].html`
- Confirmation: "Pipeline board ready. X contacts tracked, Y action items flagged."

---

## Data Source Rules

**Primary sources (in order of precedence):**
1. `memory/warm-leads.md` — source of truth for P0–P3 contact status, last contact dates, next actions
2. `memory/pipeline-state.md` — supplemental meeting outcomes, call notes, stage history
3. `memory/call-log.md` — recent call activity (if available) to update "last contact" dates

**Enrichment (optional):**
- Read `MASTER_SENT_LIST.csv` if needing company domain / send date validation
- Cross-reference `memory/contact-lifecycle.md` if needing full history timeline

**Deduplication:**
- If a contact appears in both warm-leads.md and pipeline-state.md, use warm-leads.md as primary and pipeline-state.md as supplement
- Ignore contacts not in warm-leads.md (not active warm leads)

---

## Learning Loop Integration

Follow `skills/_shared/learning-loop.md`:

**Per-run logging:**
- Date + time of execution
- Total contacts tracked
- Contacts per stage (P0, P1, P2, P3)
- Action flags count
- Meetings booked count (current month)
- Any notes (e.g., "3 new P0s from Factor batch", "1 re-engage window opened")

**Every 5th run (milestone):**
- Review stage definitions: Are they still accurate? Do contacts flow logically?
- Check if new stages needed (e.g., "RFP In Progress", "Demo Scheduled")
- Analyze which stages convert fastest to meetings
- Survey action-flag accuracy: Are overdue flags correct?
- Log findings to `learned-patterns.md`

**Entry template for run-log.md:**
```
## Run #N — [YYYY-MM-DD HH:MM UTC]
- Total warm leads tracked: 47
- P0 (Hot): 8 | P1 (Engaged): 12 | P2 (Soft): 18 | P3 (Monitor): 9
- Action flags: 3
- Meetings booked (month): 5
- Notes: [any anomalies or insights]
```

---

## Technical Implementation Notes

**HTML Structure:**
- Self-contained (no external CSS or JS libraries)
- Inline `<style>` with dark theme
- Inline `<script>` for any interactivity (optional: card click to copy contact name, filter by priority)
- Generator: Parse JSON/CSV → loop through stages → render cards → save file

**Stage-to-Swimlane Mapping:**
- Swimlane 1: Replied — Hot (P0 with recent reply)
- Swimlane 2: Meeting Booked (P0 with calendar invite)
- Swimlane 3: Meeting Held (P0/P1 post-call)
- Swimlane 4: Engaged — Nurturing (P1)
- Swimlane 5: Soft Interest (P2)
- Swimlane 6: Monitor (P3)

**Card Count per Swimlane:**
- Display count in swimlane header (e.g., "Replied — Hot (3 contacts)")
- If swimlane is empty, show placeholder: "No contacts in this stage."

**Date Calculations:**
- "Last contact: 3 days ago" = today - last_contact_date
- "Re-engage: TODAY" if re_engage_date <= today
- "ACTION NEEDED" badge if (today - last_contact_date > 5) AND (no follow-up in next 7 days)

**Colors & Badges:**
- P0: `#28a745` (green)
- P1: `#ffc107` (yellow)
- P2: `#fd7e14` (orange)
- P3: `#6c757d` (gray)
- ACTION NEEDED: `#dc3545` (red)
- RE-ENGAGE NOW: `#fd7e14` with bold text

---

## Example Output Structure

```html
<!DOCTYPE html>
<html>
<head>
  <title>Pipeline Board — Mar 15, 2026</title>
  <style>
    /* Dark theme, card layout, swimlanes */
  </style>
</head>
<body>
  <h1>Pipeline Board — Mar 15, 2026</h1>

  <div id="stats-bar">
    Total Warm Leads: 47 | P0 (Hot): 8 | P1 (Engaged): 12 | ...
  </div>

  <div id="pipeline">
    <!-- Swimlane: Replied — Hot -->
    <div class="swimlane">
      <h2>Replied — Hot (3 contacts)</h2>
      <div class="card p0">
        <!-- contact card -->
      </div>
    </div>

    <!-- ... more swimlanes ... -->
  </div>
</body>
</html>
```

---

## Execution Checklist

- [ ] Read `memory/warm-leads.md` → extract P0–P3 list
- [ ] Read `memory/pipeline-state.md` → supplement stage info
- [ ] Classify each contact to a stage (Phase 2)
- [ ] Generate HTML board with cards, colors, badges (Phase 3)
- [ ] Create "Today's Pipeline Actions" text summary (Phase 4)
- [ ] Save to `analytics/dashboards/pipeline-board-[YYYY-MM-DD].html`
- [ ] Log run details to `run-log.md`
- [ ] Print summary to chat with link to board

---

## Triggers & Scheduling

**Manual triggers:**
- "show pipeline"
- "pipeline board"
- "where are my deals"
- "pipeline view"
- "pipeline status"

**Scheduled triggers:**
- Optional Monday morning add-on to `morning-briefing` (6:00 AM weekdays)
- Can be called ad-hoc anytime Rob asks

**Standalone execution:**
- Run independently, or
- Nested within morning-briefing routine (output goes to same analytics/dashboards/ folder)

---

## Related Skills

- `batch-dashboard/SKILL.md` — Consolidated view of active outreach batches (T1, T2, pending)
- `lifecycle-tracker/SKILL.md` — Unified contact history from discovery to outcome
- `stage-monitor/SKILL.md` — Daily T2/T3 due-date check + warm lead surface
- `reply-classifier/SKILL.md` — Scan Gmail for new replies, classify, update warm-leads.md

---

## Files Updated by This Skill

**Writes:**
- `/Work/analytics/dashboards/pipeline-board-[YYYY-MM-DD].html` (new file each run)
- `/Work/skills/pipeline-tracker/run-log.md` (append run metadata)

**Reads:**
- `/Work/memory/warm-leads.md` (primary)
- `/Work/memory/pipeline-state.md` (supplemental)
- `/Work/memory/call-log.md` (optional)
- `/Work/MASTER_SENT_LIST.csv` (optional validation)

**Does NOT modify:**
- warm-leads.md, pipeline-state.md, call-log.md, or any other existing files
- Only appends to run-log.md for learning-loop tracking

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Mar 15, 2026 | Initial release. 6-stage swimlane board, dark theme, action flags, daily summary. |

---

## Questions & Support

For issues with:
- **Stage classification:** Check `memory/warm-leads.md` status fields and last-contact dates
- **Missing contacts:** Verify they are in warm-leads.md with a priority (P0–P3)
- **Board styling:** Edit inline CSS in generated HTML or request theme refresh
- **Learning loop:** See `skills/_shared/learning-loop.md` for full protocol
