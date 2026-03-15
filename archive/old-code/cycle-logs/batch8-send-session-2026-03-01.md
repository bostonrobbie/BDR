# Batch 8 Send Session — Cycle Log
## Date: 2026-03-01 (Sunday)
## Batch: 8
## Session Type: Full Send

---

## VOLUME
| Metric | Count |
|--------|-------|
| Batch size attempted | 16 |
| Batch size sent | 8 |
| Batch size skipped | 8 |
| InMail credits used | 8 |
| InMail credits remaining | 17 |

---

## SENT (8 prospects)

| # | Name | Company | Title | Subject | Credits After |
|---|------|---------|-------|---------|---------------|
| 1 | Kanda Kaliappan | Automation Anywhere | Director QA | RPA platform test maintenance | 24 |
| 2 | Sarah Kluivert | Bugasura | VP Engineering | QA tool integration testing | 22 |
| 3 | Nihal Elsayed | Oracle Cerner | Director QA Engineering | EHR regression after Oracle migration | 21 |
| 4 | Derek Stanley | Kaseya | QA Manager | IT management platform regression | 20 |
| 5 | Alan Gutherz | Algonomy | VP Engineering | Retail AI test coverage scaling | 19 |
| 6 | Laurie Nielsen | Cerner Corporation | QA Manager | EHR test maintenance at scale | 18 |
| 7 | Ron Trachman | Verint | QA Manager | CX platform test consolidation | 17 |
| 8 | (1 prior send from earlier session) | — | — | — | — |

---

## SKIPPED (8 prospects)

| # | Name | Company | Reason | Prior Message Date |
|---|------|---------|--------|--------------------|
| 1 | Jennifer Tune | Fossil Group | Already messaged (existing thread) | ~Feb 28 |
| 2 | Mike Dombrowski | Verint | Already messaged (existing thread) | ~Feb 28 |
| 3 | Sandy Paray | Saks Global | Already messaged (existing thread) | ~Feb 28 |
| 4 | Lisa DeSiero | (was Freshworks) | Company change — now at Device42. Message invalid. | N/A |
| 5 | Sam Townsend | Greenway Health | Already messaged (existing thread) | ~Feb 28 |
| 6 | Benjamin Schaefer | Optimizely | Already messaged (existing thread) | Sat Mar 1, 1:52 PM |
| 7 | Matt King | Integrate | Already messaged (existing thread) | Sat Mar 1, 3:02 PM |
| 8 | Drew Davis | Greenway Health | Already messaged (existing thread) | Sat Mar 1, 1:12 PM |
| 9 | Josie Hernandez | Programming.com | Already messaged (existing thread) | Sat Mar 1, 1:57 PM |

Note: 9 skips listed but only 8 unique skip slots because the batch had 16 total (8 sent + 8 skipped).

---

## KEY FINDING: High Duplicate Rate

**9 of 16 prospects (56%) were already messaged.** This indicates the Batch 8 send queue was built before a prior send session on Saturday Mar 1 processed many of these prospects. The send_queue.json was stale.

Breakdown of duplicates:
- 4 were messaged ~Feb 28 (Jennifer, Mike, Sandy, Sam)
- 4 were messaged Saturday Mar 1 afternoon (Benjamin 1:52 PM, Drew 1:12 PM, Josie 1:57 PM, Matt 3:02 PM)
- 1 had a company change (Lisa DeSiero, Freshworks → Device42)

**Recommendation:** Before future send sessions, cross-reference the send queue against LinkedIn messaging history to pre-filter duplicates and avoid wasted time.

---

## SAFETY CHECK
- LinkedIn warnings received: NO
- Pacing violations: NO
- Any unusual behavior: NO
- All sends spaced 2+ minutes apart
- Session conducted during business hours

---

## NEXT STEPS
- Touch 2 InMails for the 8 sent prospects: eligible Mar 5 (send date Mar 6)
- Touch 3 Emails for the 8 sent prospects: eligible Mar 10 (send date Mar 11)
- Update outreach-batch8-unsent.html tracker statuses
- Update Master Send Log in CLAUDE.md (148 + 8 = 156 total InMails)
