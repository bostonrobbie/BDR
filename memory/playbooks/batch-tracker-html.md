# Playbook: Batch Tracker HTML

## When to Use
When building a new batch of outreach contacts. The tracker HTML is the single source of truth for each batch: it contains contact cards, email drafts, QA gates, status badges, and proof point rotation tracking.

---

## File Naming

Format: `tamob-batch-{YYYYMMDD}-{batch-number}.html`

Examples:
- `tamob-batch-20260312-4.html` (Wave 5, Batch 4, Mar 12)
- `tamob-batch-20260311-1.html` (Wave 3, Mar 11)
- `tamob-batch-20260311-2.html` (Wave 4, Mar 11)

For non-TAM batches:
- `outreach-sent-{date}-batch{N}.html`
- `tyler-referrals-outreach-mar10.html`

---

## HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
  <title>TAM Outbound Batch — {Date}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
    .card { background: white; border-radius: 8px; padding: 20px; margin: 16px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .card h3 { margin-top: 0; color: #1a1a2e; }
    .badge { display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; }
    .badge-draft { background: #fff3cd; color: #856404; }
    .badge-enrolled { background: #d4edda; color: #155724; }
    .badge-sent { background: #cce5ff; color: #004085; }
    .badge-blocked { background: #f8d7da; color: #721c24; }
    .email-draft { background: #f8f9fa; border-left: 4px solid #007bff; padding: 12px; margin: 12px 0; }
    .qa-gate { background: #f0f7ff; padding: 12px; border-radius: 6px; margin: 8px 0; font-size: 13px; }
    .proof-tracker { width: 100%; border-collapse: collapse; margin: 16px 0; }
    .proof-tracker th, .proof-tracker td { padding: 8px 12px; border: 1px solid #dee2e6; text-align: left; }
    .proof-tracker th { background: #e9ecef; }
    .summary { background: #e8f5e9; padding: 16px; border-radius: 8px; margin: 20px 0; }
    .backlog { background: #fff8e1; padding: 16px; border-radius: 8px; margin: 20px 0; }
    .meta { color: #666; font-size: 13px; }
  </style>
</head>
<body>

<h1>TAM Outbound — Wave {N} Batch {N}</h1>
<p class="meta">Created: {date} | Session: {N} | Contacts: {N} | Status: {status}</p>

<!-- BATCH SUMMARY -->
<div class="summary">
  <h2>Batch Summary</h2>
  <p><strong>Enrolled:</strong> {N} contacts across {N} companies</p>
  <p><strong>Sequence:</strong> TAM Outbound - Rob Gorham (69afff8dc8897c0019b78c7e)</p>
  <p><strong>Send-from:</strong> robert.gorham@testsigma.com</p>
  <p><strong>T2 due:</strong> {date} (Day 5-8 from T1 send)</p>
</div>

<!-- PROOF POINT ROTATION TRACKER -->
<h2>Proof Point Rotation</h2>
<table class="proof-tracker">
  <tr><th>Company</th><th>Contact</th><th>Proof Point</th><th>Customer</th><th>Numbers</th></tr>
  <!-- One row per contact -->
</table>

<!-- CONTACT CARDS -->
<!-- Repeat this block for each contact -->
<div class="card">
  <h3>{Full Name} — {Title}</h3>
  <span class="badge badge-draft">Draft Ready</span>
  <p><strong>Company:</strong> {Company} | <strong>Email:</strong> {email} | <strong>Location:</strong> {city, state}</p>
  <p><strong>Apollo ID:</strong> {id} | <strong>Email status:</strong> {verified/catchall/extrapolated}</p>
  <p><strong>Source:</strong> {Apollo/Sales Nav/Chrome Extension}</p>

  <div class="email-draft">
    <p><strong>Subject:</strong> {subject line}</p>
    <p>{email body — full text, ready to copy-paste into Apollo}</p>
  </div>

  <div class="qa-gate">
    <strong>QA Gate:</strong> WC: {N} | QM: {N} | Subject: SMYKM | Proof: {customer} (unique) | MQS: {N}/12 | <strong>PASS</strong>
  </div>
</div>

<!-- BACKLOG (contacts without emails, blocked, etc.) -->
<div class="backlog">
  <h2>Backlog ({N} contacts)</h2>
  <p>These contacts were found during sourcing but could not be included in this batch:</p>
  <ul>
    <!-- One item per backlog contact with reason -->
    <li><strong>{Name}</strong> ({Company}) — {reason: no verified email / not TAM / ownership blocked / etc.}</li>
  </ul>
</div>

</body>
</html>
```

---

## Status Badge Values

| Badge | CSS Class | Meaning |
|-------|-----------|---------|
| Draft Ready | `badge-draft` | Email drafted, QA passed, not yet enrolled |
| Enrolled | `badge-enrolled` | Contact enrolled in Apollo sequence, awaiting T1 send |
| T1 Sent {date} | `badge-sent` | T1 email sent successfully |
| Blocked | `badge-blocked` | Cannot send (ownership error, job change flag, etc.) |
| Bounced | `badge-blocked` | Email bounced after send |
| T2 Due {date} | `badge-draft` | T1 sent, T2 follow-up due |

**Update badges in real-time** as contacts progress through the workflow. The tracker should always reflect current state.

---

## Required Sections

Every tracker HTML MUST include:
1. **Batch summary** with enrollment count, sequence details, T2 due date
2. **Proof point rotation table** showing which customer story each contact gets
3. **Contact cards** with full email drafts (subject + body), QA gate results, Apollo ID
4. **Backlog section** for contacts that couldn't be included (with specific reason per contact)

---

## Updating the Tracker

### After enrollment:
- Change badge from "Draft Ready" to "Enrolled" (or "T1 Pending")
- Add Apollo ID to each card

### After T1 send:
- Change badge to "T1 Sent {date}"

### After T2 draft:
- Add T2 email draft section to each card (below T1 draft)
- Change badge to "T2 Due {date}" or "T2 Sent {date}"

### If blocked:
- Change badge to "Blocked"
- Add reason in red text below the badge

---

---
*Version: 1.0 — 2026-03-12*
*Change log: v1.0 (Mar 12, 2026) — template standardized from Waves 1-5 tracker formats*
*When updating: increment version, add change log entry with date and what changed.*
