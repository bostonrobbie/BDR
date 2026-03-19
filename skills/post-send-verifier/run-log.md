# Post-Send Verifier — Run Log

### Run #2 — 2026-03-18 21:36
- **Result:** EOD final check. 88 total sends in Gmail today. 80 expected (B13: 32, B14: 37, B15: 11). 24 confirmed (all B13, executed 21:03–21:28 UTC). 56 unconfirmed: 8 B13 (possible Apollo skip/cutoff), 37 B14 (task queue not yet started), 11 B15 (task queue not yet started). 64 unexpected: 56 T2 follow-ups (all legitimate prior-wave sends) + 8 unexpected T1s (JetBlue x4, Square x2, BlackRock x1, Epicor x1 — Epicor bounced). Gmail account: work (robert.gorham@testsigma.com ✅).
- **Key metrics:** Expected: 80 | Confirmed: 24 | Unconfirmed: 56 | Unexpected T2: 56 | Unexpected T1: 8 | Gmail account: work ✅
- **Anomalies:** (1) Apollo task execution for B13 was still in progress at EOD check time (21:03–21:28 UTC vs check at 21:36 UTC). B14/B15 had not yet started sending — timing issue, not a failure. (2) 8 unexpected T1 sends from prior batch pending tasks. (3) Alan Spindel (Epicor) unexpected T1 bounced. (4) B13 subject lines differ from sends.json — "QA coverage at" vs "QA work/team/program at" — Apollo template updated mid-day; recipients match correctly.
- **Adjustments made this run:** Noted timing context (sends actively executing at EOD check time). Classified B14/B15 unconfirmed as timing-related rather than failures.
- **Output quality:** Accurate

### Run #1 — 2026-03-18 12:09
- **Result:** Found 2 sends.json files modified today (batch13: 32 contacts, batch14: 37 contacts — both TAM Outbound T1 enrollments). Gmail Sent returned 31 emails, all T2 follow-ups from robert.gorham@testsigma.com. Zero of the 69 expected T1 sends confirmed in Gmail.
- **Key metrics:** Expected sends: 69 | Confirmed: 0 | Unconfirmed: 69 | Unexpected: 31 | Gmail account: work (robert.gorham@testsigma.com ✅)
- **Anomalies:** 31 unexpected sends (T2 follow-ups to BeyondTrust, Epicor, Zebra, Check Point, Anaplan, Zimmer Biomet, Lemonade, Rocket Software, hims & hers, Bethesda, SailPoint contacts) — appear legitimate, not in today's sends.json. 69 T1 sends unconfirmed — classified as "send not executed yet" since pipeline-state has no sent entry and enrollment was recent (0.5–1.5 hrs before noon check).
- **Adjustments made this run:** batch14_sends.json entries lack subject lines (format inconsistency vs batch13) — noted subjects as "(subject not in JSON)" in report.
- **Output quality:** Accurate
