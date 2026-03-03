# Q1 Website Visitor - Tier 1 Intent: MASTER SOP
## Standard Operating Procedure for Research, Prospecting & Sequence Management

**Version:** 3.0 — Apollo UI Send Standard + Extended Audit
**Created:** March 1, 2026
**Last Updated:** March 1, 2026 (v3.0 — Apollo UI is now the ONLY send method; extended engagement audit integrated; enhanced qualification checks)
**Owner:** Rob Gorham (robert.gorham@testsigma.net)
**Sequence ID:** `69a1b3564fa5fa001152eb66`
**Email Account ID:** `68f65bdf998c4c0015f3446a`

---

## Table of Contents

1. [Intent Data Source](#1-intent-data-source)
2. [Prospect Identification](#2-prospect-identification)
3. [Qualification Checklist (MANDATORY)](#3-qualification-checklist-mandatory)
4. [Contact Creation & Enrichment](#4-contact-creation--enrichment)
5. [Sequence Loading](#5-sequence-loading)
6. [Email Personalization](#6-email-personalization)
7. [Daily Workflow](#7-daily-workflow)
8. [Audit Process for Existing Prospects](#8-audit-process-for-existing-prospects)
9. [Troubleshooting & Edge Cases](#9-troubleshooting--edge-cases)
10. [Reference Data](#10-reference-data)

---

## 1. Intent Data Source

### Where Tier 1 Prospects Come From

**Primary Source: Apollo Web Analytics (Website Visitor Tracking)**

The "Q1 Website Visitor - Tier 1 Intent" sequence is sourced from companies that have visited the Testsigma website. This is NOT cold ICP prospecting -- these are intent-driven leads.

**How to access:**
1. Log in to Apollo (app.apollo.io)
2. Navigate to **Engage > Website Visitors** (or **Analytics > Website Visitors**)
3. Filter for high-intent page visits:
   - Pages: Pricing, Demo Request, Features, Comparison pages, Case Studies
   - Company size: 200+ employees
   - Geography: US (primary), then expand

**What qualifies as "Tier 1 Intent":**
- Visited pricing page OR demo request page
- Company has 200+ employees
- Multiple page views or return visits
- Company matches ICP vertical (software, SaaS, enterprise tech, healthcare IT, fintech, etc.)

**CRITICAL:** Do NOT substitute cold Apollo People Search results for website visitor data. The whole point of this sequence is that these companies have shown buying intent by visiting our site. Cold ICP matches should go into a different sequence.

### Alternative Intent Sources (if Apollo Web Analytics is unavailable)
- Clearbit Reveal / 6sense / Demandbase (if integrated)
- Google Analytics reverse IP lookup
- Internal marketing qualified lead (MQL) lists
- Event attendee lists with website follow-up behavior

---

## 2. Prospect Identification

### Finding the Right Person at Each Visitor Company

Once you have a list of companies from Apollo Web Analytics, find the decision-maker:

**Target Titles (in priority order):**
1. VP of Engineering / VP of QA
2. Director of QA / Director of Engineering
3. Sr. Director QA Engineering
4. QA Architect / Test Engineering Manager
5. Head of Quality / Head of Engineering
6. Engineering Manager (if 200-500 employee company)

**Apollo People Search Filters:**
- `person_titles`: ["Director of QA", "VP Engineering", "QA Architect", "Test Engineering Manager", "Director of Engineering", "Sr Director QA", "Head of Quality"]
- `person_seniorities`: ["director", "vp", "c_suite"]
- `organization_num_employees_ranges`: ["201,500", "501,1000", "1001,5000", "5001,10000"]
- Scope to the specific company domains from website visitor data

**One person per company** -- pick the most senior QA/Engineering leader. If there's a dedicated QA Director, prefer them over a general Engineering Director.

---

## 3. Qualification Checklist (MANDATORY — NEVER SKIP)

### ⛔ GATE: Every prospect MUST pass ALL 6 checks before being added to the sequence. NO EXCEPTIONS.

**WHY THIS EXISTS:** The full sequence audit on March 1, 2026 found:
- **3 FAIL contacts** that had to be stopped (duplicate sequences, job changes)
- **4 HIGH-RISK territory conflicts** (contacts owned by other BDRs in Apollo AND Salesforce)
- **4 MEDIUM-RISK contacts** with unreviewed prior outreach history (including one who was "talked on phone" — a warm lead that nearly got a cold generic email)
- **19 catchall domains** that could damage sender reputation

**Skipping these checks wastes emails, damages deliverability, creates territory conflicts, and can burn warm leads with generic messaging.**

#### Check 1: Not Already in This Sequence
**How:** Search Apollo contacts for the person. Look at their `emailer_campaign_ids`. If `69a1b3564fa5fa001152eb66` is listed, they're already in Tier 1.
**API:** `apollo_contacts_search` with `q_keywords` = person name. Check response for `emailer_campaign_ids`.
**FAIL action:** Skip this person. They're already being worked.

#### Check 2: Not in Any Other Active Sequence
**How:** Check the person's `contact_campaign_statuses` array. If they have ANY active sequence status, they should not be added.
**API:** Same contact search. Look for any entries in `contact_campaign_statuses` with `status: "active"`.
**FAIL action:** Skip. Adding someone to two sequences simultaneously causes email fatigue and damages deliverability.

#### Check 3: Not in Salesforce with Existing BDR Ownership
**How:** Check if the contact has a `salesforce_id` or `salesforce_lead_id`. If they do, check `crm_owner_id` to see who owns them.
**FAIL action:** If owned by another BDR, skip. If owned by you or unassigned, proceed with caution.

#### Check 4: Email is Verified (Not Catchall)
**How:** After enrichment, check `email_status`. Must be "verified". Also check `email_domain_catchall`.
**FAIL action:** If catchall domain, add but flag for deliverability monitoring. If email status is "unavailable" or "invalid", do NOT add.

#### Check 5: Not a Duplicate Contact (Different Owner)
**How:** Check `owner_id` on the contact record. If it belongs to another team member (not your user ID `68e16f05978e5e000d10a621`), this is someone else's contact.
**FAIL action:** Skip unless you can confirm with the owner that the contact is unworked.

#### Check 6: Person Still at the Company
**How:** Check the enrichment data for `employment_history`. Make sure their current role matches what you expect.
**FAIL action:** If they've changed jobs, find the new QA/Engineering leader at the original company instead.

#### Check 7: Not Triple-Sequenced (NEW — March 1, 2026)
**How:** Count ALL sequences the contact appears in (not just active ones). Check `emailer_campaign_ids` array length.
**WHY:** The March 1 engagement audit found Katie Hotard and Giang Hoang were in 3 ACTIVE sequences simultaneously (Tier 1 + `699f4089628b940011da7fb7` + `69a05801fdd140001d3fc014`). This is a spam/unsubscribe risk.
**FAIL action:** If contact is in 2+ active sequences, remove from Tier 1. They're already being worked by other motions.

#### Check 8: No Prior Appointments or Warm Status (NEW — March 1, 2026)
**How:** Check `contact_campaign_statuses` for `inactive_reason` values. Critical values:
- `"scheduled appointment"` or `"interested"` = someone booked a meeting. This is a HOT lead.
- `"talked on phone"` = prior phone conversation. This is a WARM lead.
- Also check `contact_stage_id` — if it's not the default "New" stage (e.g., "Connected", "Attempted to Contact"), the contact has been worked.
**WHY:** The March 1 engagement audit found Andy Roth had a `"scheduled appointment / interested"` finish reason from another BDR (Meimozhi Vendhan). Sending a cold generic email to someone who already had an appointment would damage the relationship.
**FAIL action:** If prior appointment or warm status exists, DO NOT add to any cold sequence. Coordinate with the original BDR.

#### Check 9: No Recent Sequence Completion (NEW — March 1, 2026)
**How:** Check `contact_campaign_statuses` for recently finished sequences. If a contact completed a full sequence within the last 30 days, they should NOT be re-sequenced.
**WHY:** Mark Freitag completed Raghava's 7-step sequence just 18 days before being added to Tier 1. Re-sequencing this quickly is aggressive.
**FAIL action:** If a sequence finished within the last 30 days, skip. Wait at least 30 days before re-engaging.

### Quick Reference: Disqualification Summary

| Check | What to Look For | Action if Fail |
|-------|-----------------|----------------|
| Already in Tier 1 | `emailer_campaign_ids` contains sequence ID | Skip |
| In other sequences | `contact_campaign_statuses` has active entries | Skip |
| Salesforce owned | `salesforce_id` exists + `crm_owner_id` is another BDR | Skip |
| Email not verified | `email_status` != "verified" | Skip or flag |
| Catchall domain | `email_domain_catchall` = true | Add but monitor |
| Wrong owner | `owner_id` != your ID | Skip |
| Changed jobs | `employment_history[0].current` = false | Find replacement |
| Triple-sequenced | `emailer_campaign_ids` count >= 2 (active) | Remove from Tier 1 |
| Prior appointment/warm | `inactive_reason` = "scheduled appointment" or "talked on phone" | DO NOT cold-sequence |
| Recent sequence finish | Any sequence finished within last 30 days | Wait 30 days |

---

## 4. Contact Creation & Enrichment

### Creating New Contacts

For prospects who pass all checks and don't exist as contacts yet:

**Apollo API call:** `apollo_contacts_create`
- `first_name`, `last_name`, `email`, `title`, `organization_name`
- `website_url` (company domain)
- `present_raw_address` (city, state, country)
- **ALWAYS set `run_dedupe: true`** to prevent duplicates

### Enrichment

**For single contacts:** `apollo_people_match` with first_name, last_name, domain
**For batches (up to 10):** `apollo_people_bulk_match` with details array

Enrichment returns: verified email, phone numbers, employment history, company data. This consumes credits -- confirm with Rob before enriching large batches.

---

## 5. Sequence Loading

### Adding Contacts to the Sequence

**API call:** `apollo_emailer_campaigns_add_contact_ids`

**Required parameters:**
- `id`: `69a1b3564fa5fa001152eb66` (sequence ID)
- `emailer_campaign_id`: `69a1b3564fa5fa001152eb66` (same as above)
- `send_email_from_email_account_id`: `68f65bdf998c4c0015f3446a` (Rob's email)
- `contact_ids`: array of Apollo contact IDs

**Safety flags (recommended defaults):**
- `sequence_no_email: false` -- don't add people without email
- `sequence_active_in_other_campaigns: false` -- don't add if in another sequence
- `sequence_finished_in_other_campaigns: false` -- don't add if finished elsewhere
- `sequence_same_company_in_same_campaign: false` -- don't double up from same company

### Sequence Structure

The Tier 1 sequence has 3 steps:
1. **Step 1 (Position 1):** Manual email - Touch 1 (initial outreach). Wait: 30 minutes after add.
2. **Step 2 (Position 2):** Manual email - Touch 2 (follow-up reply thread). Wait: 3 days after Step 1.
3. **Step 3 (Position 3):** Manual email - Touch 3 (breakup/final touch). Wait: 6 days after Step 2.

All steps are manual emails -- they show up as tasks in Apollo for you to personalize and send.

### ⚠️ SEND METHOD: APOLLO UI ONLY (MANDATORY — effective March 1, 2026)

**ALL emails MUST be sent through the Apollo UI task queue. NO exceptions.**

**Why this change was made:** Through the Feb 27 - Mar 1 workflow evolution, we tested multiple send methods:
1. Gmail manual compose (Feb 27) — worked but no sequence tracking, emails not logged in Apollo
2. Gmail API drafts via Cowork (Mar 1) — created 46 drafts but they were disconnected from Apollo task queue, leading to confusion about what was sent vs. not sent
3. Apollo task queue sends (Mar 1) — 16 emails sent this way; these properly tracked in the sequence, logged deliverability, and advanced contacts to the next step automatically

**Problems with non-Apollo send methods:**
- Gmail sends do NOT register in the Apollo sequence. Contacts appear stuck at their current step even after receiving Touch 1.
- Gmail drafts create a parallel workflow that conflicts with Apollo tasks, causing double-send risk.
- Deliverability tracking (opens, clicks, bounces) only works for emails sent through Apollo.
- Sequence cadence (wait times between touches) only triggers when emails are sent via Apollo tasks.

**The correct workflow:**
1. Use Cowork/Claude to research companies and write personalized email copy
2. Navigate to Apollo UI > Sequences > Q1 Website Visitor - Tier 1 Intent > Tasks tab
3. Open each prospect's task (Touch 1, Touch 2, or Touch 3)
4. Paste the pre-written personalized email into the Apollo task editor
5. Send via the Apollo task "Complete" button
6. Apollo automatically logs the send, tracks engagement, and queues the next touch

**DO NOT:**
- Create Gmail drafts for sequence emails (this was deprecated March 1)
- Send sequence emails directly from Gmail compose
- Use the Gmail API to send or draft sequence emails
- Send from any email other than robert.gorham@testsigma.net (the Apollo-linked account)

---

## 6. Email Personalization

### Touch 1 Template Guidelines

- Company-specific opening (reference their product, industry, or a recent event)
- One sentence Testsigma value prop tied to their specific pain
- Industry/role connection to testing challenges
- Low-friction CTA (15-min call, not a full demo)
- 4 to 6 sentences max
- **ZERO em dashes** (major AI tell)
- No buzzwords ("revolutionary", "game-changing", "cutting-edge")

### Touch 2: Pain-Focused Follow-Up
- Reference Touch 1 without being pushy
- Lead with a specific pain point for their industry
- Include a proof point (case study, metric, customer reference)

### Touch 3: Breakup
- Short and direct
- Offer value even if they're not interested (resource, insight)
- Clear final CTA

---

## 7. Daily Workflow

### Morning Block (30 min): Prospect Identification
1. Open Apollo Web Analytics > Website Visitors
2. Filter for high-intent pages (pricing, demo, features, comparison)
3. Filter: 200+ employees, US geography
4. Export list of visitor companies
5. For each company, find the right persona (see Section 2)

### ⛔ MANDATORY GATE: Qualification (15-20 min per batch)
6. **Run ALL 6 qualification checks (Section 3) on EVERY candidate — NO EXCEPTIONS**
7. For each candidate, document the check results:
   - ✅ Check 1: Not in Tier 1 (`emailer_campaign_ids`)
   - ✅ Check 2: Not in other active sequences (`contact_campaign_statuses`)
   - ✅ Check 3: Not SF-owned by another BDR (`crm_owner_id`, `salesforce_id`)
   - ✅ Check 4: Email verified, not catchall (`email_status`, `email_domain_catchall`)
   - ✅ Check 5: Not duplicate/different owner (`owner_id` = `68e16f05978e5e000d10a621`)
   - ✅ Check 6: Still at the company (`employment_history`, LinkedIn headline)
8. **If ANY contact has a Salesforce record or prior sequence history**, check:
   - What happened in the prior sequence? (finished, failed, talked on phone?)
   - Who owns the contact in SF? (same BDR or different?)
   - Were there prior conversations? (check `contact_campaign_statuses` notes)
9. **Only contacts that pass ALL 6 checks proceed to enrichment**

### Midday Block (60-90 min): Research, Write, Send
10. Batch enrich CLEAN contacts via Apollo API (up to 10 at a time)
11. Use Claude/Cowork to research companies and write personalized emails
12. **For contacts with prior outreach history (MEDIUM RISK):** customize messaging to acknowledge relationship, don't send generic templates
13. Human review each email (2 min each) for accuracy and tone
14. **Send via Apollo UI task queue ONLY** — open each task in Apollo > Sequences > Tasks, paste personalized email, click Complete to send. Do NOT use Gmail or Gmail API drafts.

### End of Day Block (15 min): Logging
15. Update `prospect_master_tracker.md` with new additions (include check results)
16. Update `email_outreach_tracker.csv` with sent emails
17. Note any catchall domains to monitor
18. Flag any contacts that need team coordination (territory overlaps)
19. Push updates to workspace/repo

---

## 8. Audit Process for Existing Prospects

### When to Audit
- Before adding any new batch of prospects
- Weekly health check on the full sequence
- When sequence performance drops (bounce rate rises, open rate falls)

### Full Sequence Audit Checklist

For EVERY contact in the sequence (including already-emailed):

1. **Verify email is still valid** - check `email_status` via enrichment
2. **Confirm person is still at the company** - check `employment_history`
3. **Check for duplicate sequences** - look at `emailer_campaign_ids`
4. **Review deliverability** - flag catchall domains, monitor bounce rates
5. **Check Salesforce sync** - ensure CRM records are clean

### Audit Results from March 1, 2026

**Initial Candidate Audit (10 candidates for batch addition):**

| # | Name | Company | Status | Issue |
|---|------|---------|--------|-------|
| 1 | Rachana Jagetia | Housecall Pro | FAIL | Already in 2 of your sequences |
| 2 | Tim Wiseman | Upland Software | FAIL | Already in Tier 1 + another sequence. Salesforce tagged |
| 3 | Joe Pember | Riverbed | FAIL | Already in Tier 1. Prior BDR outbound in Salesforce |
| 4 | Sneha Prabhakar | Aria Systems | FAIL | Already in Tier 1. In Salesforce |
| 5 | Patrick Southall | GoodRx | FAIL | Already in Tier 1. Catchall domain |
| 6 | Christie Howard | LastPass | FLAG | In your other sequence, not Tier 1. No Salesforce |
| 7 | Pallavi Sheshadri | Origami Risk | FLAG | Different owner, CSV import. No sequences, catchall |
| 8 | Marc Jarvis | PAR Technology | CLEAN | Was already a contact, added to sequence |
| 9 | Joel Brent | Kiddom | CLEAN | Net new, created and added |
| 10 | Scott Winzenread | DRB | CLEAN | Net new, created and added |

**Full Sequence Audit (68 of ~80 contacts):**
See `tier1_sequence_audit_report.md` for complete results:
- 36 CLEAN, 29 FLAG, 3 FAIL
- 3 FAIL contacts resolved (duplicate sequences stopped, job change removal)
- 4 HIGH-RISK territory conflicts identified (contacts owned by other BDRs)
- 4 MEDIUM-RISK prior outreach contacts (including 1 "talked on phone" warm lead)
- 19 catchall domains flagged for monitoring

**Extended Engagement Audit (25 additional contacts, March 1, 2026):**
See `BDR/data/trackers/engagement_audit_mar1.md` for complete results:
- 5 CRITICAL removals: Andy Roth (scheduled appointment with another BDR), Katie Hotard (triple-sequenced), Giang Hoang (triple-sequenced), Mark Freitag (finished full 7-step sequence 18 days ago), Khalid Aziz (prior outbound + Salesforce contact+lead)
- 4 MODERATE flags: Scott Carruth (ABM/TAM campaigns), Yuehli Dewolf (dual-sequenced), Rashad Fambro (Salesforce CRM contact), Felix Tanh (prior outbound email)
- 4 MINOR flags: Pre-existing contacts with no concerning signals
- 12 CLEAN: Net new contacts created by us

**Key Lessons:**
1. Apollo People Search returns ICP matches from the entire database. It does NOT filter out people you're already working. Always run qualification checks.
2. Contacts with `contact_campaign_statuses` showing "talked on phone" are WARM LEADS — never send generic sequence emails to them.
3. **Contacts with "scheduled appointment" or "interested" finish reasons are HOT leads** — another BDR has booked a meeting. Sending cold outreach to them is destructive.
4. Check BOTH `owner_id` (Apollo) AND `crm_owner_id` (Salesforce) — they can be different, and both matter.
5. Catchall domains are more common than expected (19 out of 68 contacts). Monitor bounce rates from Day 1.
6. Job changes happen silently in Apollo — the contact record doesn't auto-update when someone leaves a company. Always verify LinkedIn headlines for Director+ titles.
7. **Triple-sequencing is a real risk.** Katie Hotard and Giang Hoang were in 3 active sequences simultaneously. Always count ALL active sequences, not just check for Tier 1.
8. **Check `email_source` field.** If it says `"emailer_message_outbound"`, the contact was previously emailed from Apollo by someone on the team.
9. **Check `contact_stage_id`.** If it's not the default "New" stage (values like "Connected" or "Attempted to Contact"), the contact has been worked before.
10. **30-day re-sequence cooldown.** Mark Freitag finished a 7-step sequence just 18 days before being added to Tier 1. This is too aggressive and risks spam complaints.
11. **ALL emails must be sent through Apollo UI** (not Gmail, not Gmail API drafts). See Section 5 for the full rationale.

---

## 9. Troubleshooting & Edge Cases

### "Ownership blocked" contacts
If Apollo says you can't add a contact because of ownership, create a NEW contact record under your ownership with the same person's details. Use `run_dedupe: false` in this case.

### Catchall domains to monitor (19 domains as of March 1, 2026)
These domains accept any email address, so delivery is uncertain:
- veeva.com, redsailtechnologies.com, opploans.com (OppFi), goodrx.com
- flywire.com, bynder.com, drata.com, g2.com
- medimpact.com, freedompay.com, csgi.com (CSG), cedargate.com
- iteris.com, quickbase.com, connectwise.com, modmed.com
- opsecsecurityonline.com, crestron.com, epicgames.com
- origamirisk.com

### Contact changed jobs
If enrichment shows a person left the company, do NOT email their old address. Find the new QA/Engineering leader at the original (visitor) company. **Real example:** Harsha Navaratne showed Interactions LLC in Apollo but LinkedIn confirmed SoundHound AI. Laura Riley moved from Origami Risk to Ampersand. Both were stopped and replacements identified.

### Sequence "finished" contacts
If someone is marked "finished" in another sequence, they may have already been fully worked. **CRITICAL:** Check the `inactive_reason` field:
- `"talked on phone"` = WARM LEAD — do not send generic emails. Get call notes first.
- `"user_deleted"` or `"manually finished"` = May or may not have been worked. Check engagement data.
- No reason = Completed full sequence with no response. Safe to re-engage in a different sequence.

### Territory conflict contacts (NEW)
If a contact has a different `owner_id` in Apollo AND a different `crm_owner_id` in Salesforce, this is a hard territory conflict. Do NOT email these contacts. Coordinate with the other owner first. The March 1 audit found 4 such contacts that were actively being emailed by Rob while owned by other BDRs.

### Contacts with prior BDR outreach history
Check custom fields like `"Outbound_BDR"`, `"Senthil_TAM_Oct24th_Valid"`, `"Factors_BDRs"` — these indicate prior outbound campaigns. The contact may have received emails from another BDR. Review prior engagement before sending your sequence emails.

---

## 10. Reference Data

### Key Apollo IDs
- **Sequence:** `69a1b3564fa5fa001152eb66` (Q1 Website Visitor - Tier 1 Intent)
- **Your User ID:** `68e16f05978e5e000d10a621`
- **Your Email Account:** `68f65bdf998c4c0015f3446a` (robert.gorham@testsigma.net)
- **Team ID:** `5e6be7ced287310106f43b90`

### ICP Filters for Apollo People Search
```
person_titles: ["Director of QA", "VP Engineering", "QA Architect", "Test Engineering Manager", "Director of Engineering", "Sr Director QA", "Head of Quality", "Director of QA Engineering"]
person_seniorities: ["director", "vp", "c_suite"]
organization_num_employees_ranges: ["201,500", "501,1000", "1001,5000", "5001,10000"]
```

### Sequence Step Details
| Step | Type | Wait | Position |
|------|------|------|----------|
| Touch 1 | Manual email (new thread) | 30 min | 1 |
| Touch 2 | Manual email (reply thread) | 3 days | 2 |
| Touch 3 | Manual email (new thread) | 6 days | 3 |

### Current Sequence Stats (as of March 1, 2026 EOD)
- Total contacts: ~80 (confirmed via API)
- Step 1: 22 active | Step 2: 53 active | Step 3: 0 active (after 4 HIGH-RISK stops)
- Audit 1: 68 contacts (36 CLEAN, 29 FLAG, 3 FAIL) — all FAIL resolved, 4 HIGH-RISK stopped
- Audit 2: 25 additional contacts (12 CLEAN, 4 MINOR, 4 MODERATE, 5 CRITICAL) — 5 CRITICAL pending removal
- Unique delivered: 49
- Open rate (filtered): 6.1%
- Open rate (unfiltered): 53.1%
- Reply rate: 0%
- Bounce rate: 0%
- Click rate (unfiltered): 8.2%
- 16 Touch 1 emails sent via Apollo task queue (Mar 1)
- 46 Gmail drafts created (Mar 1) — **DEPRECATED: these should be deleted. Future sends via Apollo UI only.**

### Related Files in Workspace
- `prospect_master_tracker.md` - Running tracker of all prospects and their status
- `tier1_sequence_audit_report.md` - **Full sequence audit report** (68 contacts, risk-tiered SF analysis, all resolutions)
- `BDR/data/trackers/engagement_audit_mar1.md` - **Extended engagement audit** (25 additional contacts, 5 CRITICAL removals)
- `email_outreach_tracker.csv` - Detailed outreach log with engagement data
- `daily_prospecting_workflow.md` - Daily workflow with time estimates
- `outreach_email_sop.md` - End-to-end email creation and send process
- `website_visitor_sequence_drafts.md` - Email template library
- `personalized_sequence_emails.md` - Personalized emails for specific contacts
- `workflow-notes.md` - Quick reference notes and process decisions
- `email_send_execution_plan.md` - **ARCHIVED** (Feb 28 plan; superseded by Apollo UI workflow)
- `Apollo_Sequence_SOP.pdf` - Original Apollo sequence SOP (pre-audit version)
- `Q1_Website_Visitor_Tier1_Sequence_Playbook.docx` - Full playbook

---

## Cowork Quick Start

When starting a new Cowork session for this sequence, tell Claude:

1. **"Pull today's website visitors from Apollo and find QA/Engineering leaders"**
   - Claude will use Apollo Web Analytics data (you may need to provide the visitor list if API access is limited)
   - Claude will search for decision-makers at each company

2. **"Run qualification checks on these prospects"** ⛔ MANDATORY — NEVER SKIP
   - Claude will run ALL 6 checks: existing sequences, active sequences, Salesforce ownership, email verification, duplicate contacts, job verification
   - Claude will check `contact_campaign_statuses` for prior outreach history and `inactive_reason` notes
   - Claude will check BOTH `owner_id` (Apollo) AND `crm_owner_id` (Salesforce) for territory conflicts
   - Claude will flag catchall domains and contacts with prior BDR outreach custom fields
   - **Only CLEAN contacts proceed. FLAG contacts need human review. FAIL contacts are rejected.**

3. **"Create contacts and add clean ones to the Tier 1 sequence"**
   - Claude will create contacts with `run_dedupe: true`
   - Claude will add to sequence `69a1b3564fa5fa001152eb66` via API
   - Claude will NOT add any contact that failed checks in step 2

4. **"Write personalized Touch 1 emails for the new additions"**
   - Claude will enrich companies, research, and draft emails following the template guidelines
   - For MEDIUM-RISK contacts (prior outreach), Claude will customize messaging

5. **"Update the tracker"**
   - Claude will append to `prospect_master_tracker.md` and `email_outreach_tracker.csv`
   - Claude will include check results and flag notes for each contact

---

*This SOP is the single source of truth for the Q1 Website Visitor - Tier 1 Intent sequence. Update it whenever the process changes. Last updated: March 1, 2026 (v3.0 — Apollo UI is now the ONLY email send method; 3 new qualification checks added (triple-sequencing, prior appointments, 30-day cooldown); extended engagement audit integrated (5 CRITICAL removals); Gmail draft workflow officially deprecated).*
