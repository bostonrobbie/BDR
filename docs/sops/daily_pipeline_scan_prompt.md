# Daily Pipeline Scan & Hot Intent Prospecting — Reusable Task Prompt
## Version 1.0 | Created March 2, 2026

This is the master prompt for the daily 6AM scheduled scan. It is self-contained and references all SOPs, IDs, and processes needed to run autonomously.

---

## OBJECTIVE

Run a daily performance scan of the Q1 Website Visitor - Tier 1 Intent Apollo sequence pipeline and identify 10-25 new qualified prospects from Apollo's website analytics. Produce a daily briefing report with pipeline health metrics, new hot intent accounts, and a qualified prospect list ready for outreach.

---

## REFERENCE IDS

- Sequence: "Q1 Website Visitor - Tier 1 Intent" (ID: `69a1b3564fa5fa001152eb66`)
- Email Account: robert.gorham@testsigma.net (ID: `68f65bdf998c4c0015f3446a`)
- User ID: `68e16f05978e5e000d10a621`
- Team ID: `5e6be7ced287310106f43b90`

---

## REFERENCE FILES (in workspace)

- `Tier1_Intent_Sequence_SOP_MASTER.md` — Single source of truth (v3.0)
- `outreach_email_sop.md` — Email creation and send SOP (v2.0)
- `daily_prospecting_workflow.md` — Daily workflow (v2.0)
- `workflow-notes.md` — Quick reference knowledge base (v2.0)
- `prospect_master_tracker.md` — Running prospect tracker
- `tier1_sequence_audit_report.md` — Audit report (68 contacts)
- `BDR/data/trackers/engagement_audit_mar1.md` — Extended audit (25 contacts)

---

## DAILY SCAN PROCESS (execute in order)

### PART 1: PIPELINE PERFORMANCE SCAN (sequence health)

1. Search for the sequence using `apollo_emailer_campaigns_search` with `q_name: "Q1 Website Visitor"`.
2. Record from the sequence data: total contacts, active contacts per step, emails sent, opens, clicks, replies, bounces.
3. Search contacts in the sequence using `apollo_contacts_search` to get current step distribution (Step 1/2/3 counts).
4. Calculate and report these KPIs:
   - Total contacts in sequence
   - Contacts at each step (Step 1, Step 2, Step 3, Finished)
   - Open rate (filtered and unfiltered if available)
   - Reply rate
   - Bounce rate
   - Click rate
   - New contacts added since last scan
   - Contacts that advanced steps since last scan
5. Compare today's metrics against the baseline from the prior day's report (read from `daily_scan_reports/` folder).
6. Flag any anomalies: bounce rate spike, open rate drop, unusual step distribution.

### PART 2: HOT INTENT ACCOUNT DISCOVERY

7. Use `apollo_mixed_companies_search` to find companies matching Tier 1 ICP criteria:
   - `q_organization_keyword_tags`: ["SaaS", "software", "enterprise technology", "healthcare IT", "fintech"]
   - `organization_num_employees_ranges`: ["201,500", "501,1000", "1001,5000", "5001,10000"]
   - `organization_locations`: ["United States"]
   - Sort by most recent activity
   - Pull up to 50 companies per search

8. For promising companies, use `apollo_mixed_people_api_search` to find decision-makers:
   - `person_titles`: ["Director of QA", "VP Engineering", "QA Architect", "Test Engineering Manager", "Director of Engineering", "Sr Director QA", "Head of Quality", "Director of QA Engineering", "VP of Quality Engineering"]
   - `person_seniorities`: ["director", "vp", "c_suite"]
   - Scope to the target company domains
   - One person per company — prefer dedicated QA leaders over general Engineering Directors

9. Target: identify 15-30 raw candidates to qualify down to 10-25 clean prospects.

### PART 3: 9-POINT QUALIFICATION (MANDATORY — NEVER SKIP)

For EVERY candidate, run ALL 9 checks. No exceptions.

**Check 1: Not Already in Tier 1 Sequence**
- Search `apollo_contacts_search` with `q_keywords` = person name
- Check `emailer_campaign_ids` for `69a1b3564fa5fa001152eb66`
- FAIL if found → Skip

**Check 2: Not in Any Other Active Sequence**
- Check `contact_campaign_statuses` array for any `status: "active"`
- FAIL if found → Skip

**Check 3: Not Salesforce-Owned by Another BDR**
- Check for `salesforce_id` or `salesforce_lead_id`
- Check `crm_owner_id` — if different from Rob's, skip
- Also check Apollo `owner_id` — if different from `68e16f05978e5e000d10a621`, investigate

**Check 4: Email Verified**
- Check `email_status` must be "verified"
- Check `email_domain_catchall` — if true, flag for monitoring but can proceed
- If email_status = "unavailable" or "invalid" → SKIP

**Check 5: Not a Duplicate Contact (Different Owner)**
- Check `owner_id` on contact record
- If belongs to another team member → Skip

**Check 6: Person Still at Company**
- Check `employment_history` — current role must match expected company
- If job change detected → find replacement at original company

**Check 7: Not Triple-Sequenced**
- Count ALL sequences in `emailer_campaign_ids`
- If 2+ active sequences → SKIP (spam/unsubscribe risk)

**Check 8: No Prior Appointments or Warm Status**
- Check `contact_campaign_statuses` for `inactive_reason`:
  - "scheduled appointment" or "interested" = HOT lead → DO NOT cold-sequence
  - "talked on phone" = WARM lead → DO NOT cold-sequence
- Check `contact_stage_id` — if not "New", contact has been worked

**Check 9: No Recent Sequence Completion (30-Day Cooldown)**
- Check `contact_campaign_statuses` for recently finished sequences
- If any sequence finished within last 30 days → SKIP

**Additional Data Points:**
- `email_source`: if "emailer_message_outbound", previously emailed from Apollo
- Custom fields: "Outbound_BDR", "Senthil_TAM_Oct24th_Valid", "Factors_BDRs" = prior campaigns

### PART 4: ENRICHMENT & EMAIL DRAFTING

10. For all CLEAN prospects (passed all 9 checks), enrich via `apollo_people_match` (single) or `apollo_people_bulk_match` (batch up to 10). NOTE: This consumes credits — only enrich CLEAN prospects.

11. For each enriched prospect, research the company and draft a personalized Touch 1 email following this template:

```
Subject: Quick question, [First Name]

Hi [First Name],

Noticed some folks at [Company] have been exploring test automation solutions
lately and figured it might be worth a quick intro.

I'm Rob with Testsigma. We help engineering teams cut test maintenance by up to
80% with AI powered test automation that works across web, mobile, and API from
a single platform. [1-2 sentences connecting Testsigma value to their specific
company/role/industry challenges.]

Would it be worth a 15 minute call to see if there's a fit? Happy to share a
quick overview doc instead if that's easier.

Best,
Rob
```

12. Run quality checks on every draft:
   - ZERO em dashes (—) anywhere in body
   - ZERO buzzwords: synergy, leverage, cutting-edge, game-changer, revolutionary, disruptive, paradigm, holistic, robust, seamless, seamlessly, turnkey, best-in-class, world-class, next-gen, bleeding edge, innovative
   - Subject line must be exactly "Quick question, [First Name]"
   - Body must reference website visitor intent signal
   - Must contain low-friction CTA (15 min call or overview doc)
   - Must end with "Best, Rob"
   - 4-6 sentences in body

### PART 5: OUTPUT — DAILY BRIEFING REPORT

13. Create a daily report file at: `daily_scan_reports/scan_YYYY-MM-DD.md`

The report must include these sections:

**A. Pipeline Health Dashboard**
- Date and scan timestamp
- Total contacts in sequence (vs. yesterday)
- Step distribution: Step 1 / Step 2 / Step 3 / Finished (vs. yesterday)
- Open rate, reply rate, bounce rate, click rate (vs. yesterday)
- Any anomalies or alerts

**B. New Hot Intent Accounts**
- Table of companies discovered with: Company Name, Domain, Employee Count, Industry, Intent Signal, Page Visits (if available)

**C. Qualified Prospect List**
- Table with: Name, Title, Company, Email, All 9 Check Results (PASS/FLAG/FAIL), Catchall Status
- Summary: X candidates screened → Y qualified → Z flagged → W failed

**D. Email Drafts Ready**
- Full personalized Touch 1 email for each CLEAN prospect
- Quality check pass rate

**E. Action Items for Rob**
- Prospects ready to add to sequence (list contact IDs)
- Emails ready to send via Apollo UI task queue
- Any FLAG contacts needing human review
- Any territory conflicts requiring team coordination
- Catchall domains to monitor

**F. SOP Performance Tracking**
- Which qualification checks caught the most disqualifications today
- Any new edge cases or patterns observed
- Suggestions for SOP refinement based on today's data

14. Also update `prospect_master_tracker.md` with any new prospects identified.

### PART 6: VERIFICATION

15. Re-read the generated report and verify:
   - All 9 qualification checks were actually run (not skipped)
   - Email drafts pass all quality checks
   - Metrics are consistent (numbers add up)
   - No FAIL or FLAG contacts slipped into the CLEAN list
   - Daily goal of 10-25 qualified prospects is addressed (note if under/over target)

---

## KNOWN CATCHALL DOMAINS (flag but don't skip)

veeva.com, redsailtechnologies.com, opploans.com, goodrx.com, flywire.com, bynder.com, drata.com, g2.com, medimpact.com, freedompay.com, csgi.com, cedargate.com, iteris.com, quickbase.com, connectwise.com, modmed.com, opsecsecurityonline.com, crestron.com, epicgames.com, origamirisk.com

---

## SEND METHOD REMINDER

ALL emails are sent via Apollo UI task queue ONLY. This daily scan prepares the email copy and prospect list. Rob will manually paste emails into Apollo tasks and click Complete. Do NOT create Gmail drafts. Do NOT send via Gmail API.

---

## SUCCESS CRITERIA

- Pipeline health dashboard generated with day-over-day comparison
- 10-25 qualified prospects identified (all passing 9-point qualification)
- Personalized Touch 1 email drafted for each qualified prospect
- All drafts pass quality checks (0 em dashes, 0 buzzwords, correct subject/CTA/signature)
- Report saved to daily_scan_reports/ folder
- Tracker updated
- SOP performance notes captured for continuous improvement
