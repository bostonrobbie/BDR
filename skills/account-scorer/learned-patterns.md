# Account Scorer — Learned Patterns

_No patterns yet. Will populate after 5th run._

---

**Review Cycle:** Every 5 runs (typically ~5 weeks), this document is updated with:

1. **Effectiveness Analysis**
   - Reply rate among TIER 1 accounts (target: > 40%)
   - Reply rate among TIER 2 accounts
   - Factor vs. ICP-only: which performs better?
   - Trigger signal lift: do accounts with QA hiring signals reply faster?

2. **Weight Tuning Recommendations**
   - If pattern emerges (e.g., "Factor accounts consistently underperform when ICP=MEDIUM"), note here
   - Proposed adjustment to Phase 2 scoring model
   - Rationale and confidence level

3. **Seasonal or Vertical Insights**
   - Example: "SaaS QA hiring peaks Q1; FinTech peaks Q2 — consider seasonal adjustment"
   - Example: "Retail e-commerce verticals reply 2x faster than Pharma; increase vertical weight?"

4. **Warm Lead Correlation**
   - Do P0-P2 contacts in warm-leads.md actually convert faster?
   - +25 pts bonus justified or should it change?

---

## How This Works

At the end of run 5, 10, 15, etc., Claude will:

1. Review `skills/account-scorer/run-log.md` — the last 5 runs
2. Query `analytics/outreach.db` — extract:
   - For each top-10 account from last 5 weeks: reply_count, reply_date, reply_rate
   - For each TIER 2 account: same metrics
   - Factor flag correlation with reply rate
   - Trigger signal type correlation with reply rate
3. Document findings here
4. Propose weight adjustments to SKILL.md Phase 2 if evidence is strong (≥ 80% confidence)
5. Get Rob's approval before implementing any weight changes

---

## Audit Trail

| Date | Review | Findings | Weight Changes | Approved By |
|------|--------|----------|-----------------|------------|
| (after run 5) | TBD | — | None yet | — |
| (after run 10) | TBD | — | None yet | — |

---

**End of Learned Patterns**
