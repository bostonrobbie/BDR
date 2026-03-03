# Incidents & Draft Safety Rules

## INC-001: Premature Touch 3 Emails (2026-02-28)
**Severity:** HIGH

### What Happened
6 Touch 3 emails sent Feb 28 at 6:30-6:33 AM ET, 7-8 days early, skipping Touch 2 entirely.

### Affected Prospects
| Name | Company | Batch | Touch 1 Sent | Days Early |
|------|---------|-------|-------------|------------|
| Irfan Syed | Progress Software | Batch 3 | Feb 25 | 7 |
| Katie Barlow Hotard | Lucid Software | Batch 3 | Feb 25 | 7 |
| Rachana Jagetia | Housecall Pro | Batch 3 | Feb 26 | 8 |
| Giang Hoang | Employee Navigator | Batch 3 | Feb 26 | 8 |
| Pallavi Sheshadri | Origami Risk | ORPHAN | Unknown | N/A |
| Gunasekaran Chandrasekaran | FloQast | ORPHAN | Unknown | N/A |

### Root Cause (3 stacked failures)
1. Gmail drafts created WITHOUT date-gating logic
2. Drafts used old pre-C2 templates with HC1 violations
3. Two prospects not in any batch tracker (orphans)

### Remediation
- 4 Batch 3: Treat premature email as extra touch. Skip official Touch 3. Continue Touch 2 on schedule.
- 2 orphans: Add retroactively. Research + proper follow-ups.

---

## Draft Safety & Cadence Enforcement Rules

### Rule 1: Date-Gating
- Touch 2 drafts: NOT before Day 4
- Touch 3 drafts: NOT before Day 9
- Premature drafts saved as `[DRAFT-HOLD]` with date gate, NOT in Gmail.

### Rule 2: TOUCH_ELIGIBLE_DATE Fields
Every tracker must have: touch1_sent_date, touch2_eligible_date (+4d), touch2_send_date (+5d), touch3_eligible_date (+9d), touch3_send_date (+10d). **Check today's date before creating ANY draft.**

### Rule 3: No Orphan Prospects
Every prospect must exist in a tracker BEFORE any draft is created.

### Rule 4: Template Version Enforcement
All drafts must use C2 structure. MQS >= 9/12. No C1 or pre-C2 templates.

### Rule 5: Draft Naming Convention
- `[READY] [Name] @ [Company] - Touch [N] - Send on [date]`
- `[HOLD] [Name] @ [Company] - Touch [N] - NOT BEFORE [date]`
- `[SENT] [Name] @ [Company] - Touch [N] - Sent [date]`

### Rule 6: Daily Gmail Draft Audit
Every daily session: search drafts, cross-reference eligible dates, flag orphans/premature/old-template/unscored. Delete or hold-tag flagged drafts.

### Rule 7: Batch 7+ Tracker Requirements
Must include: touch1_sent_date, touch2/3_eligible_date, current_touch, cadence_status (ON_TRACK/AHEAD/BEHIND/COMPLETE).
