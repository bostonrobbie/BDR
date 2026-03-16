# BDR Outreach Incident Log

## Purpose
This log tracks operational errors, near-misses, and lessons learned from the BDR outreach pipeline. Every incident gets a root cause analysis, corrective actions, and prevention rules added to CLAUDE.md.

---

## INC-001: Premature Touch 3 Emails (2026-02-28)

**Severity:** HIGH
**Detected by:** Rob (manual review) + Claude (audit)
**Date occurred:** 2026-02-28, 6:30-6:33 AM ET
**Date resolved:** 2026-03-01

### What Happened
6 Touch 3 emails were sent from Gmail (robert.gorham@testsigma.com accounts) 7-8 days ahead of schedule, completely skipping the Touch 2 InMail step.

### Affected Prospects
| # | Name | Company | Batch | Touch 1 Sent | Touch 3 Sent | Days Early | Orphan? |
|---|------|---------|-------|-------------|-------------|------------|---------|
| 1 | Irfan Syed | Progress Software | Batch 3 | Feb 25 | Feb 28 | 7 | No |
| 2 | Katie Barlow Hotard | Lucid Software | Batch 3 | Feb 25 | Feb 28 | 7 | No |
| 3 | Rachana Jagetia | Housecall Pro | Batch 3 | Feb 26 | Feb 28 | 8 | No |
| 4 | Giang Hoang | Employee Navigator | Batch 3 | Feb 26 | Feb 28 | 8 | No |
| 5 | Pallavi Sheshadri | Origami Risk | N/A | Unknown | Feb 28 | N/A | YES |
| 6 | Gunasekaran Chandrasekaran | FloQast | N/A | Unknown | Feb 28 | N/A | YES |

### Root Cause Analysis (3 Stacked Failures)
1. **No date-gating logic:** Gmail drafts were created in a prior Cowork session without any check on whether the prospect was eligible for that touch based on cadence timing.
2. **Old template content:** All 6 emails used pre-C2 templates with multiple quality violations (HC1 "I noticed" phrasing, wrong CTAs, no proof points, career trajectory references).
3. **Orphan prospects:** 2 of the 6 prospects (Pallavi, Gunasekaran) had no entry in any batch tracker, bypassing all cadence checks and QA gates.

### Content Quality Violations Found
- HC1 violation: "I noticed" phrasing in multiple emails
- Wrong CTA: "quick 15-minute chat" instead of "what day works" (DATA: 14.0% vs 40.4%)
- No proof points in several emails
- Katie's email used career trajectory reference (banned "show your work" pattern)
- None of the 6 emails passed QA Gate or MQS scoring
- All used C1-era or pre-C2 template structure

### Additional Findings During Audit
- 6 additional Gmail drafts (Sergey Matetskiy, Mobin Thomas, Dino Gambone, Matthew Smith, Joshua Greig, Pete Draheim) were created ~2:54 PM Feb 28 but NOT sent. Also premature, old templates, and for ownership-blocked contacts who were replaced in Batch 3. Action: DELETE.
- 9 buyer intent emails sent Feb 27 (~1:30 PM) used identical "Noticed some folks at [Company]" template with HC1 violations. These were Touch 1 emails (in sequence), but the template quality was below C2 standard.

### Corrective Actions Implemented
| # | Action | Where | Status |
|---|--------|-------|--------|
| 1 | Date-Gating Rule: No Touch 2 draft before Day 4, no Touch 3 draft before Day 9 | CLAUDE.md § Draft Safety Rules | DONE |
| 2 | TOUCH_ELIGIBLE_DATE fields required in all trackers | CLAUDE.md § Draft Safety Rules | DONE |
| 3 | No Orphan Prospects Rule: tracker entry required before any draft | CLAUDE.md § Draft Safety Rules | DONE |
| 4 | Template Version Enforcement: C2 + QA Gate required for all drafts | CLAUDE.md § Draft Safety Rules | DONE |
| 5 | Draft Naming Convention: [READY]/[HOLD]/[SENT] prefix | CLAUDE.md § Draft Safety Rules | DONE |
| 6 | Daily Gmail Draft Audit added to Phase 1 Intel Scan | CLAUDE.md § Run the Daily | DONE |
| 7 | Batch 7+ Tracker Requirements (cadence fields) | CLAUDE.md § Draft Safety Rules | DONE |

### Remediation Plan
- Irfan, Katie, Rachana, Giang: Treat premature email as unplanned extra touch. Skip official Touch 3 on Day 10. Continue with Touch 2 InMail on schedule (Mar 2-3).
- Pallavi, Gunasekaran: Add to active tracker. Complete 3-source research. Draft proper C2 Touch 2 follow-ups.
- 6 unsent drafts (Sergey, Mobin, Dino, Matthew, Joshua, Pete): DELETE from Gmail. These contacts were ownership-blocked and replaced.

### Lessons Learned
1. Gmail drafts are indistinguishable from ready-to-send emails. Any draft that exists CAN and WILL be sent. Treat draft creation as seriously as sending.
2. Orphan prospects (not in any tracker) are invisible to all safety checks. The tracker is the single source of truth — nothing happens without a tracker entry.
3. Template version drift is dangerous. Old sessions may leave behind artifacts (drafts, data) that don't meet current quality standards.
4. The cadence is a contract with the prospect. Sending out of order signals desperation or disorganization, exactly the opposite of the consultative BDR brand we're building.

---

## INC-002: Weekend Send Override (2026-02-28)

**Severity:** LOW (Known override)
**What happened:** 88 InMails sent on Saturday Feb 28. SOP says "Weekend: Research + batch build only. No sends."
**Why it happened:** Rob explicitly authorized weekend sends during the session to clear the backlog.
**Impact:** DATA shows Monday is worst day (22.9%). Saturday sends may have similar below-average performance. Monitor reply rates for Feb 28 sends vs weekday sends.
**Action:** No SOP change needed. Weekend sends remain non-default but can be authorized by Rob explicitly.

---

## Template: New Incident Entry

```
## INC-XXX: [Title] (YYYY-MM-DD)

**Severity:** HIGH / MEDIUM / LOW
**Detected by:** [who]
**Date occurred:** [date]
**Date resolved:** [date]

### What Happened
[Description]

### Affected Prospects
[Table or list]

### Root Cause Analysis
[Numbered list of contributing factors]

### Corrective Actions
[Table with action, location, status]

### Lessons Learned
[Numbered insights]
```
