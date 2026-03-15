# Deliverable Format

## HTML Deliverable Structure

Single HTML file containing:

### Prospect Tracker Table
- Sorted by priority score (descending)
- Columns: priority score, name, title, company, tags, profile research notes, company research notes, outreach angle, LinkedIn URL, status, reply tag, A/B group, personalization score
- Color-coded badges for persona type (QA, VP Eng), vertical (FinServ, Tech), and signals (Buyer Intent, Recently Hired)
- Priority filter: show only Hot (5) and Warm (4) prospects

### Individual Prospect Cards
- Copy-paste-ready messages for ALL written touches (Touch 1, 3, 5, 6) with "Copy Message" and "Copy Subject" buttons
- Cold call snippet for Touch 2 and Touch 4 with "Copy Script" button
- Predicted objection + pre-loaded response (expandable)
- Meeting prep card (auto-populated when status = Meeting Booked)

### Status Tracking
Status dropdown per prospect:
Not Started, Touch 1 Sent, Call 1 Made, Touch 3 Sent, Call 2 Made, Touch 5 Sent, Touch 6 Sent, Replied, Meeting Booked, Not Interested, Bounced, Dormant, Re-Engaged

### Metadata Per Prospect
- Reply tag dropdown
- A/B group label
- Message personalization score (1-3)
- Priority score badge (1-5)

## File Naming
`prospect-outreach-[batch#]-[date].html`
Example: `prospect-outreach-3-2026-02-18.html`

Save to `batches/batch-[#]/` directory.

## Batch Comparison Dashboard

After 3+ batches, generate `outreach-dashboard.html` with:
- Reply rate by persona type (bar chart)
- Reply rate by vertical (bar chart)
- Reply rate by proof point used (bar chart)
- Reply rate by personalization score (bar chart)
- A/B test results (comparison table)
- Trend over time (line chart)
- Top 5 best-performing messages (full text)
