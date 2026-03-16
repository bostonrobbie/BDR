# Morning Briefing — Scannable HTML Dashboard Skill

## Description

Generates a comprehensive, self-contained HTML dashboard that Rob opens every weekday morning at 6 AM. Replaces plain-text messages.md output with a visual, card-based interface showing overnight activity, warm leads, pending tasks, and pipeline status. The dashboard is designed for fast scanning — color-coded status pills, collapsible sections, and priority-ordered content.

**Output:** `analytics/dashboards/morning-briefing-YYYY-MM-DD.html` (published every weekday at 6 AM)

---

## Trigger

Scheduled daily at 6:00 AM (Mon–Fri). Can be run ad-hoc at any time during work hours.

---

## Dependencies & Data Sources

This skill reads from:
- `memory/warm-leads.md` — P0/P1 contacts
- Gmail MCP — overnight replies (unread, last 24h)
- Google Calendar — today's events
- `memory/contact-lifecycle.md` OR `memory/session/handoff.md` — T2/T3 due dates
- `MASTER_SENT_LIST.csv` — active pipeline row count
- `memory/session/work-queue.md` — task queue
- `batches/t2-pending/` and `batches/sends-json/` — staged T2/T3 batches
- `memory/apollo-config.md` (optional) — Slack channel list for future section

---

## Steps

### Phase 1: Gather Warm Leads

1. Read `memory/warm-leads.md`
2. Extract all P0 and P1 contacts (by checking their Priority field)
3. For each, collect:
   - Full name
   - Company
   - Title
   - What they said / last action (first 100 chars of their reply text)
   - Days since last touch (calculate from date in log vs. today)
   - Recommended response type (infer from context: "Positive Reply", "Referral", "Intent Signal", etc.)
4. Sort by days since last touch (most overdue first)
5. If P0/P1 list is empty: prepare fallback text "No warm leads — inbox is clear"

**Error handling:**
- If warm-leads.md doesn't exist: log as "File not found" and skip section
- If no P0/P1 contacts exist: show the "clear" message
- If a contact has no last-touch date: show "?" for days since touch

---

### Phase 2: Scan Overnight Replies

1. Use Gmail MCP `gmail_search_messages`:
   ```
   q: "to:robert.gorham@testsigma.com is:unread newer_than:1d"
   maxResults: 20
   ```
2. For each result, extract:
   - Sender name and company (parse from email domain if needed)
   - Subject line
   - Snippet (first 80 characters of body)
   - Classification (classify as P0/P1/P2/P3/P4 using heuristics from `memory/context/objection-map.md` if available; else use basic rules: all-caps complaint = P1, mentions meeting = P0, etc.)
3. Sort by priority (P0 first, then P1, P2, P3, P4)
4. Limit display to top 10 replies
5. If no unread replies: show "No new replies overnight"

**Error handling:**
- If Gmail MCP unavailable: log error and show "Gmail unavailable" placeholder
- If snippet retrieval fails for a message: show "[Message body unavailable]"
- If sender domain cannot be parsed: use email address as fallback

---

### Phase 3: Scan Today's Calendar

1. Use Google Calendar MCP `gcal_list_events`:
   ```
   calendarId: "primary"
   timeMin: "YYYY-MM-DDTHH:MM:SS" (start of today)
   timeMax: "YYYY-MM-DDTHH:MM:SS" (end of today)
   ```
2. For each event, extract:
   - Summary (title)
   - Time (HH:MM format)
   - Attendees list
3. Cross-reference attendees against `memory/warm-leads.md` and `MASTER_SENT_LIST.csv`:
   - If attendee name matches a warm lead: flag as "PROSPECT MEETING — prep card needed"
   - If attendee name matches a sent contact: flag as "SENT PROSPECT MEETING"
4. For flagged prospect meetings, auto-generate a 3-line prep card:
   ```
   Company: [X]
   Last sent: [proof point / subject]
   Days since: [N]
   ```
5. If no events today: show "Clear calendar"

**Error handling:**
- If Calendar MCP unavailable: log error and show placeholder
- If attendee name cannot be parsed: skip that attendee in lookup
- If prep card data is missing: show "[Data unavailable]"

---

### Phase 4: Extract T2/T3 Due Dates

1. Read `memory/contact-lifecycle.md`
   - OR fallback: read `memory/session/handoff.md` for `## Pipeline State` section
2. Extract all contacts with T2 or T3 due dates
3. Identify which have due_date <= today
4. For each, collect:
   - Name
   - Company
   - Batch ID
   - Days overdue (negative = due in future, positive = overdue)
5. Sort by days overdue (most overdue first)
6. Group by batch for display
7. If no T2/T3 due: show "No overdue follow-ups"

**Error handling:**
- If contact-lifecycle.md has parsing errors: try handoff.md
- If date fields are malformed: show "?" for days overdue
- If batch ID is missing: label as "Untracked"

---

### Phase 5: Build Pipeline Snapshot

1. Count rows in `MASTER_SENT_LIST.csv` (exclude header) = **Active contacts in sequence**
2. Count contacts in contact-lifecycle.md with stage = "T2_WINDOW_OPEN" = **T2 window open**
3. Count contacts in warm-leads.md with Priority in [P0, P1, P2, P3] = **Warm leads (P0-P3)**
4. List all files in `batches/t2-pending/` (*.html) and `batches/sends-json/` (*.json) = **Batches staged for APPROVE SEND**
   - Extract batch name from filename
   - For each .html file, count row count (proxy for contact count)
   - For each .json file, parse contact_count field or array length
5. Compile snapshot:
   ```
   Active contacts: [N]
   T2 window open: [N]
   Warm leads (P0-P3): [N]
   Batches staged: [N]
     - [batch-name]: [N contacts]
     - [batch-name]: [N contacts]
   ```

**Error handling:**
- If MASTER_SENT_LIST.csv not found: show "0"
- If contact-lifecycle.md parsing fails: show "?" and note in anomalies
- If t2-pending or sends-json directories don't exist: show "None staged"

---

### Phase 6: Work Queue Section

1. Read `memory/session/work-queue.md`
2. Extract all tasks with status = UNCLAIMED or IN_PROGRESS
3. For UNCLAIMED tasks:
   - Show priority, task_id, description (first 80 chars)
   - Limit to top 3
4. For IN_PROGRESS tasks from OTHER sessions:
   - Show session ID, task_id, which session has it
   - Note: "Another session is working on this"
5. If no unclaimed or in-progress: show "Work queue empty"

**Error handling:**
- If work-queue.md not found: show "Work queue unavailable"
- If YAML parsing fails: show "Parse error — please check work-queue.md"

---

### Phase 7: Slack Updates Placeholder (Not Yet Connected)

1. Check if `memory/apollo-config.md` contains a `slack_channels:` list
2. If not found or no channels listed:
   - Show a placeholder section with static text:
     ```
     "Slack integration not yet configured.
      To enable: add slack_channels: ['#announcements', '#product', '#general']
      to memory/apollo-config.md"
     ```
3. If channels ARE listed:
   - Read last 24 hours from each channel using Slack MCP `slack_read_channel`
   - Pull announcements, product updates, mentions of "Rob" or "QA"
   - Format as bullet list
   - If no updates: show "No relevant updates in Slack"

**Error handling:**
- If apollo-config.md not found: show placeholder
- If Slack MCP unavailable: show placeholder
- If channel_id lookup fails: skip that channel

---

## HTML Generation

### Template Structure

The output file is a single, self-contained HTML file with no external dependencies except a single Google Fonts CDN link.

**Key design elements:**
- **Header bar:** Date, day of week, "Good morning Rob", status pill (color-coded)
- **Status pill colors:**
  - GREEN: 0 warm leads, 0 overdue T2/T3, calendar clear
  - YELLOW: 1-2 warm leads OR 1-2 overdue OR calendar has prospect meetings
  - RED: 3+ warm leads OR 3+ overdue OR >5 unread replies
- **Sections:** Each is a collapsible card with icon, title, color accent
- **Card colors:** Warm leads (red accent), replies (blue), calendar (green), T2/T3 (orange), pipeline (gray), work queue (purple)
- **Mobile-friendly:** Flex layout, responsive fonts, touch-friendly buttons
- **Footer:** "Generated at HH:MM | Next update: tomorrow 6:00 AM"

### HTML Structure (Pseudo-Code)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Morning Briefing — YYYY-MM-DD</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    [Dark card CSS + color scheme]
    [Flex layout for responsive design]
    [Card collapsible toggle CSS]
    [Color-coded pill styles: red/yellow/green]
    [Mobile-friendly breakpoints]
  </style>
</head>
<body>
  <!-- Header Bar -->
  <div class="header">
    <div class="header-left">
      <h1>Good morning Rob</h1>
      <p>YYYY-MM-DD (Day of Week)</p>
    </div>
    <div class="header-right">
      <span class="status-pill [color]">[Status text]</span>
    </div>
  </div>

  <!-- Main Content -->
  <div class="dashboard-container">
    <!-- 1. Warm Leads (always first) -->
    <div class="card warm-leads-card">
      <div class="card-header">
        <span class="icon">🔴</span>
        <h2>Warm Leads — Action Required</h2>
        <button class="toggle-btn">−</button>
      </div>
      <div class="card-content">
        [List of P0/P1 contacts, or fallback "No warm leads"]
      </div>
    </div>

    <!-- 2. Overnight Replies -->
    <div class="card replies-card">
      <div class="card-header">
        <span class="icon">📬</span>
        <h2>Overnight Replies</h2>
        <button class="toggle-btn">−</button>
      </div>
      <div class="card-content">
        [List of unread messages, sorted by priority]
      </div>
    </div>

    <!-- 3. Today's Calendar -->
    <div class="card calendar-card">
      <div class="card-header">
        <span class="icon">📅</span>
        <h2>Today's Calendar</h2>
        <button class="toggle-btn">−</button>
      </div>
      <div class="card-content">
        [Events with prospect meeting flags and prep cards]
      </div>
    </div>

    <!-- 4. T2/T3 Due Today -->
    <div class="card t2t3-card">
      <div class="card-header">
        <span class="icon">⏰</span>
        <h2>T2/T3 Due Today</h2>
        <button class="toggle-btn">−</button>
      </div>
      <div class="card-content">
        [T2/T3 contacts grouped by batch, color-coded by overdue days]
      </div>
    </div>

    <!-- 5. Pipeline Snapshot -->
    <div class="card pipeline-card">
      <div class="card-header">
        <span class="icon">📊</span>
        <h2>Pipeline Snapshot</h2>
        <button class="toggle-btn">−</button>
      </div>
      <div class="card-content">
        [Pipeline metrics and staged batches list]
      </div>
    </div>

    <!-- 6. Slack Updates (placeholder or live) -->
    <div class="card slack-card">
      <div class="card-header">
        <span class="icon">💬</span>
        <h2>Company & Team Updates</h2>
        <button class="toggle-btn">−</button>
      </div>
      <div class="card-content">
        [Placeholder or live Slack updates]
      </div>
    </div>

    <!-- 7. Work Queue -->
    <div class="card workqueue-card">
      <div class="card-header">
        <span class="icon">📋</span>
        <h2>Work Queue</h2>
        <button class="toggle-btn">−</button>
      </div>
      <div class="card-content">
        [Top 3 unclaimed tasks + any in-progress from other sessions]
      </div>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    <p>Generated at HH:MM UTC | Next update: tomorrow 6:00 AM</p>
  </div>

  <script>
    // Toggle card collapse/expand
    document.querySelectorAll('.toggle-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const content = e.target.parentElement.nextElementSibling;
        content.style.display = content.style.display === 'none' ? 'block' : 'none';
        e.target.textContent = e.target.textContent === '−' ? '+' : '−';
      });
    });
  </script>
</body>
</html>
```

### CSS Guidelines

- **Card background:** Light neutral (#f9f9f9) with subtle shadow
- **Text colors:** Dark gray (#333) for body, darker (#111) for headings
- **Accent colors by section:**
  - Warm leads: Red (#e74c3c)
  - Replies: Blue (#3498db)
  - Calendar: Green (#27ae60)
  - T2/T3: Orange (#f39c12)
  - Pipeline: Gray (#95a5a6)
  - Work queue: Purple (#9b59b6)
- **Status pills:**
  - GREEN: #d4edda background, #155724 text
  - YELLOW: #fff3cd background, #856404 text
  - RED: #f8d7da background, #721c24 text
- **Font:** Inter from Google Fonts (fallback: system sans-serif)
- **Spacing:** 16px padding per card, 24px gap between cards
- **Mobile:** Stack all cards vertically, reduce padding on small screens

---

## Data Formatting Rules

### Warm Leads Table
```
| Name | Company | Title | Last Said | Days Since | Action Type |
| Alice Smith | Acme Corp | QA Manager | "Sounds great, let's talk" | 2 | Positive Reply |
| Bob Jones | TechCorp | SDET | "When are you available?" | 5 | Referral Follow-up |
```

### Replies Table
```
| Sender | Company | Subject | Snippet | Priority |
| Charlie Brown | DataCo | RE: Testsigma demo | "Thanks for the intro. Interested in..." | P0 |
| Diana Prince | DevShop | RE: AI test automation | "Can you send pricing?" | P1 |
```

### Calendar Prospect Meetings
```
EVENT: Weekly Standup (10:00 AM – 10:30 AM)
Status: SENT PROSPECT MEETING
Attendee: Alex Johnson (AlexCorp)
Prep Card: Company: AlexCorp | Sent: "Self-healing for flaky tests" | 3 days ago
```

### T2/T3 Table
```
| Contact | Company | Batch | Days Overdue | Action |
| Emma Davis | FinTech Inc | TAMOB-Batch-5 | 2 days | SEND T2 NOW |
| Frank Miller | RetailCo | TAMOB-Batch-3 | 0 days | Due today |
```

---

## Error Handling

### File Missing
- If warm-leads.md missing: log as "File missing" and skip section
- If contact-lifecycle.md missing: log as "File missing" and use handoff.md fallback
- If MASTER_SENT_LIST.csv missing: show "0" for pipeline count
- If work-queue.md missing: show "File unavailable"

### Tool Errors
- If Gmail MCP fails: log error, show "[Gmail unavailable]" in replies section
- If Calendar MCP fails: log error, show "[Calendar unavailable]" in calendar section
- If CSV parsing fails: show "[Data parsing error]" and log the line number

### Data Parsing Errors
- If date format unrecognized: show "?" for days since / days overdue
- If contact name malformed: show as-is and log anomaly
- If batch ID missing: label as "Untracked"
- If priority field invalid: default to P3

### Recovery Rules
- Always complete the HTML output file, even if one section fails
- Failed sections show a gray card with error message
- Log all errors to run-log.md with section name, error type, and impact
- If 3+ sections fail: still output file but add warning banner at top

---

## Output File

**File path:** `analytics/dashboards/morning-briefing-YYYY-MM-DD.html`
- Where YYYY-MM-DD = today's date in the system timezone
- Always overwrite the previous day's file (same filename)
- File size: typically 80–120 KB (single HTML, no external assets)
- Encoding: UTF-8

---

## Self-Improvement Loop

This skill maintains its own run log and learned-patterns file. Full protocol: `skills/_shared/learning-loop.md`

### Before Each Run
1. Read `skills/morning-briefing/learned-patterns.md` if it exists — apply any documented calibration adjustments
2. Note the current date/time for accurate "Generated at" timestamp

### After Every Run — Append to run-log.md
```markdown
### Run #[N] — [YYYY-MM-DD HH:MM]
- **Result:** [1-2 sentence summary of what dashboard was built]
- **Key metrics:** [Overnight replies: N | Calendar events: N prospect meetings | T2/T3 due: N | Work queue: N unclaimed]
- **Anomalies:** [Missing files, parse errors, unexpected edge cases]
- **Adjustments made this run:** [Any deviations from SKILL.md]
- **Output quality:** [Accurate / Mostly accurate / Needs calibration / Failed]
- **File generated:** [path or error]
```

### Every 5th Run — Pattern Review
1. Read last 5 run-log.md entries
2. Extract recurring patterns:
   - Data gaps (which sections fail most often?)
   - Metric drift (are warm lead counts consistently higher/lower than expected?)
   - Edge cases (date formatting issues, missing attendee names, etc.)
3. Overwrite `skills/morning-briefing/learned-patterns.md` with findings
4. If a pattern appears in 4+ of 5 runs: write a `## SKILL UPDATE PROPOSAL` to `memory/session/messages.md`

---

## Key Metrics

These are tracked in the run log after every execution:

| Metric | Notes |
|--------|-------|
| Overnight replies | Count of unread emails found |
| Calendar events | Total events today |
| Prospect meetings | Flagged events (matched to warm-leads or MASTER_SENT_LIST) |
| T2/T3 due | Contacts with T2/T3 due today or overdue |
| Work queue items | Unclaimed + in-progress tasks displayed |
| File generation | Success / error message |
| Data sources available | Which files/tools succeeded vs. failed |
| Status pill color | GREEN / YELLOW / RED |

---

## Quick Checklist

```
[ ] Read learned-patterns.md if it exists
[ ] Gather warm leads from memory/warm-leads.md (P0/P1)
[ ] Search Gmail for overnight replies (is:unread newer_than:1d)
[ ] Fetch calendar events for today
[ ] Extract T2/T3 due dates from contact-lifecycle.md or handoff.md
[ ] Count pipeline metrics from MASTER_SENT_LIST.csv
[ ] List staged batches from t2-pending/ and sends-json/
[ ] Build work queue from memory/session/work-queue.md
[ ] Determine status pill color (green/yellow/red)
[ ] Generate HTML file to analytics/dashboards/
[ ] Verify file was created and is readable
[ ] Append to run-log.md with metrics
[ ] Every 5th run: update learned-patterns.md
```

---

## Notes for Implementation

- **Timezone handling:** Use system timezone for "today" and "Generated at" timestamp. Show times in user's local format.
- **Date math:** For "days since last touch", calculate as `today - last_date`. If result is 0, show "Today". If negative (future date), show "0".
- **Batch parsing:** For HTML batch files in t2-pending/, count `<tr>` elements to estimate contact count. For JSON files, parse the array length or "contact_count" field.
- **Attendee matching:** Use fuzzy name matching (first initial + last name) to catch variations like "A. Smith" vs. "Alice Smith".
- **Warm lead status:** Use the "Priority" field from warm-leads.md to identify P0/P1. Other fields: Name, Company, Title, Last Said (from outreach log), Last Date (for days calculation).
- **Collapsible cards:** By default, all cards start OPEN except "Slack Updates" (show placeholder). Rob can click to collapse any section.
- **Persistent state:** Store collapse/expand state in browser localStorage so Rob's preferences persist across daily reloads.

