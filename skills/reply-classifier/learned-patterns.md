# Reply Classifier — Learned Patterns

_Updated after Run #15 (2026-03-18) following 15th-run (3rd five-run) pattern review protocol._
_Covers Runs #11–#15. Prior reviews covered Runs #1–#5 and #6–#10._
_Following protocol in skills/_shared/learning-loop.md_

---

## Status
**Runs completed:** 15 (third pattern review conducted)

---

## Pattern Categories

### What Works Well
- Gmail `newer_than:2d` + `is:unread` dual-query approach efficiently surfaces all relevant messages without duplication — confirmed reliable across all 10 runs.
- System/automated message identification is reliable: Apollo, LinkedIn, Slack, and mail delivery subsystem senders are consistently correctly classified as non-prospect.
- Bounce NDR identification is reliable across multiple mail systems (Google mailer-daemon, Office 365 postmaster, pphosted MAILER-DAEMON, citizensbank.com postmaster).
- Internal Testsigma emails are correctly filtered — never misclassified as prospect replies.
- Apollo call summary threads: timing-out was a one-time issue (Run #6 only) — not a recurring problem across Runs #7–#10.
- Deal thread CC detection (Aetna, Lexia Learning) has been reliable — correctly classified as "Active Deal Thread (CC)" and not treated as prospect replies.

### What Causes Problems
- **Run-log duplicate numbering:** Pre-existing cosmetic issue (two "Run #3" entries from Run #5 review). Still present, still no functional impact.
- **19 consecutive runs with zero prospect replies:** This is the most significant cumulative finding (escalated from 10 at last review). The inbox continues to be dominated by internal Slack notifications, Apollo system emails, and bounce NDRs. This is not a skill failure — it reflects current outreach reply reality. Proposal #3 (zero-reply alert) was queued in messages.md after Run #10 and remains outstanding for Rob's review.
- **Missed call identification gap:** Multiple unidentified missed calls have been logged across runs. +13218377968 and +13152756209 (TASK-044/045) remain unidentified. +17632288324 (area code 763, NW Twin Cities MN, TASK-055) is new from Run #14. +19319221680 (area code 931, TN) called TWICE on Mar 17 (2:16 PM and 4:42 PM EDT) — two callbacks from same number is an elevated warm signal. All remain pending human identification.
- **Bounce NDR volume pattern:** Large batches of bounces tend to arrive in clusters after send days, sometimes spanning multiple 2-hour windows. Run #11 was a significant catch (33 bounces) that prior runs missed. The dual-query approach successfully captures these when they arrive.

### Calibration Notes
- **Citizens Bank domain:** 2 consecutive bounces (Zahidh Zubair B9 + Usman Khan B10). Confirmed domain-level filtering. No new @citizensbank.com enrollments until alternate contacts/emails are verified.
- **Kibo Commerce domain block:** 5/5 bounces from kibocommerce.com. Full domain block confirmed — avoid new enrollments permanently.
- **Replicon SMTP 550 pattern:** 5/5 Replicon contacts bounced with SMTP 550. Domain filter confirmed — avoid new enrollments permanently.
- **infor.com domain firewall:** 5/5 Infor contacts bounced with "5.4.1 Recipient address rejected: Access denied" — hard domain firewall. Avoid new enrollments.
- **RSM US (rsmus.com):** 5/5 bounced (Brian Brennan, Philcy Morales, Rupasri Soman, Kristina Pozzi, Christina Jimenez). Email format issue confirmed — avoid new rsmus.com enrollments until correct format verified.
- **Check Point domain:** Now 5 total bounces (Tomer Weinberger, Yogesh Garg, Shlomo Yeret + 2 pre-logged). Full domain block confirmed — avoid new enrollments permanently.
- **Celonis .de domain:** 4 total bounces (brian.oppenheim, bogdan.minciu + 2 prior). Avoid new celonis.de enrollments.
- **FormAssembly:** 3 bounces (julieta.abacha, massimo.modena, shilpa.nayak). Avoid until correct format verified.
- **Batch 11/12 bounce volume:** 33 bounces from Mar 17 batch send — significant miss-and-catch pattern (Run #11 caught what Runs #9/#10 missed). Email format verification before send would reduce bounce rate.
- **Apollo call summaries** arrive as large threads and can cause gmail_read_thread timeouts (Run #6). When encountered, classify from snippet only — this is acceptable.
- **+19319221680 (TN, 931 area code):** Called twice on Mar 17 within 2.5 hours (2:16 PM and 4:42 PM EDT). Two callbacks from same unidentified number is an elevated warm signal. Flagged in TASK-047.

### Active Deal Threads (CC — awareness only)
- **Aetna (Dwight Scull, Christopher Rees):** Tyler Kapeller AE thread — AI-Native Testing webinar. Rob CC'd. Monitor for hot signals.
- **Lexia Learning (Joe Casale, Megan Morris):** Tyler Kapeller AE thread. Rob CC'd. Monitor for hot signals.

### Pending SKILL.md Update Proposals
_Improvements identified — to be proposed via messages.md per hard rule (never modify SKILL.md directly)._

1. **Add "Apollo Missed Call" as explicit signal type** (carried forward from Runs #5/#10 review) — inbound calls to Rob's Apollo number are warm signals and should have their own P0-adjacent "Inbound Call" category. Status: still outstanding for Rob's approval.

2. **Add "Active Deal Thread (CC)" as a signal type** (carried forward from Runs #5/#10 review) — emails where Rob is CC'd on a deal thread are worth surfacing with a distinct label. Status: still outstanding.

3. **"Zero-reply streak alert" as a periodic signal** (originally proposed at Run #10, queued in messages.md): After N consecutive runs with zero prospect replies, surface a pipeline health notice to Rob. Current state: 19 consecutive runs (escalated from 10). Status: proposal queued in messages.md — awaiting Rob's review. No new proposal needed; escalation note added here.

4. **NEW — Add "Domain block confirmed" tracking shorthand:** When 5+ contacts from the same domain bounce, add a permanent "BLOCKED DOMAIN" note to the relevant batch tracker HTML so future prospect builds skip those domains automatically. Current blocked list: kibocommerce.com, replicon.com, infor.com, checkpoint.com, citizensbank.com (2-contact sample), rsmus.com (format unknown), celonis.de (format unknown), formassembly.com (format unknown). Propose adding a canonical blocked-domain list to memory/ for cross-skill use.

---

### Pattern Counts (Runs #11–#15)
| Pattern | # Runs Present |
|---------|---------------|
| Zero prospect replies | 5/5 |
| Internal Slack notifications dominant | 5/5 |
| Apollo system email noise | 5/5 |
| New bounce NDRs surfaced | 2/5 (Run #11: 33 new; Run #14: 2 new Check Point) |
| Missed calls (new) | 3/5 (Run #11: +19319221680 first call; Run #12: +19319221680 second call; Run #14: +17632288324) |
| Deal thread CCs present | 0/5 |
| gmail_read_thread timeout | 0/5 |
| FactorsAI token issue | 1/5 (Run #13) |
| AE deal pipeline signal | 1/5 (Run #12: Coupa intro calendar acceptance by William Dalley) |

**Trigger for new SKILL.md proposal:** Missed calls have now appeared in 3/5 runs. Combined with 5/5 zero-reply runs, Proposal #1 (Apollo Missed Call as explicit signal type) has increased urgency — carries forward. Proposal #4 (blocked domain list) is NEW this review cycle.

**Cumulative zero-reply streak:** 19 consecutive runs as of Run #15. This is now the longest streak by far. Proposal #3 message remains outstanding in messages.md.

---

_Next pattern review: after Run #20._
