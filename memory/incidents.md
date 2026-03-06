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

---

## INC-002: Five Double-Sends Across Batches (Discovered 2026-03-04)
**Severity:** HIGH

### What Happened
Five prospects were sent LinkedIn InMails twice — once in an early batch and once in Batch 8 (Mar 3). All five sends already occurred and cannot be unsent. Discovered during full Sales Nav inbox audit (220 conversations).

### Affected Prospects
| Name | First Send | Second Send | Gap |
|------|-----------|------------|-----|
| Chuck Smith | Batch 1, Feb 23 (connection msg) | Batch 5B, Feb 27 | 4 days |
| Abe Blanco | Batch 3, Feb 26 | Batch 8, Mar 3 | 5 days |
| Rick Kowaleski | Batch 3, Feb 26 | Batch 8, Mar 3 | 5 days |
| Christie Howard | Batch 5B, Feb 27 | Batch 8, Mar 3 | 4 days |
| Mohan Gummadi | Batch 5B, Feb 27 | Batch 8, Mar 3 | 4 days |

Note: Abe Blanco also replied "not interested" Mar 4. Added to DNC. Double-send is moot for him but logged for accuracy.

### Root Cause
No cross-batch dedup check performed before Batch 8 was built. Batch 8 pull from Apollo Q1 Priority Accounts sequence included prospects already messaged in Batches 1/3/5B without any name-level verification against prior send history.

### Remediation (applied 2026-03-04)
- All 5 double-sends logged in pipeline-state.md under "Double-sends (cannot unsend)"
- MASTER_SENT_LIST.csv created: single deduplicated CSV of all sends across all batches
- Pre-batch dedup check added to sop-send.md as mandatory Step A/B before any batch is built
- For Touch 2: treat double-send people as normal Touch 2 candidates. Note the extra prior touch. Abe Blanco = DNC, skip entirely.
- For Chuck Smith: first send was a connection request (not InMail, no Sales Nav thread). Touch 2 still due on normal timeline.

---

## INC-003: Batch 9 Untracked Sends (2026-03-03)
**Severity:** MEDIUM

### What Happened
6 Batch 9 InMails sent on Mar 3 in a session that ended without logging. Discovered via Sales Nav audit the following day. 5-credit discrepancy between tracker (28) and actual (23) also traced to same-session logging gap.

### Affected Prospects
Mohan Guruswamy, Jeremy Cira, Chandana Ray, Lueanne Fitzhugh, Martha Horns, Kylie Summer.

### Root Cause
Send session ended mid-batch without updating pipeline-state.md. Credits not decremented. No same-session logging discipline.

### Remediation (applied 2026-03-04)
- All 6 logged retroactively in pipeline-state.md Batch 9 True State table
- Credits corrected to 23
- Same-session logging rule added to sop-send.md Step 9

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
