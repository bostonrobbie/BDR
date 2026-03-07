# Q1 Website Visitor - Tier 1 Intent: MASTER SOP
## Standard Operating Procedure for Research, Prospecting & Sequence Management

**Version:** 8.0 — LinkedIn Sales Navigator ICP verification now a mandatory hard-stop gate before sequence enrollment
**Created:** March 1, 2026
**Last Updated:** March 6, 2026 (v8.0 — MANDATORY: LinkedIn Sales Navigator ICP verification gate added as Section 2.5; all contacts must be confirmed on Sales Nav before proceeding to Section 3 qualification checks; 7 contacts flagged and removed from Batch 10; 1 borderline contact flagged for Rob review; see Section 2.5 for full requirements and flag criteria)
**Owner:** Rob Gorham (robert.gorham@testsigma.com)

### Active Sequences
| Sequence | ID | Send Method | Status |
|----------|----|-------------|--------|
| Q1 Website Visitor - Tier 1 Intent | `69a1b3564fa5fa001152eb66` | Apollo task queue (email) | Active — 152 contacts (91 prior + 61 Batch 10), 90 Touch 1 sent, 61 Touch 1 pending (Batch 10 task queue), 70 at Step 2 |
| Q1 Priority Accounts | `69a05801fdd140001d3fc014` | Apollo task queue (LinkedIn InMail) | ⚠️ IDLE — 285 contacts enrolled, 0 InMails sent |
| Copy - AI Maturity Audit Campaign for QA | `6909f6b00f9bb2001d599d5e` | Apollo task queue (email) | ⚠️ NEEDS AUDIT — 142 contacts, ~255 tasks overdue |

> **⚠️ CRITICAL FINDING (March 6, 2026):** Q1 Priority Accounts has 285 contacts enrolled but ZERO InMails have ever been sent through Apollo. The 19 emails sent March 3 previously attributed to Priority Accounts were actually to AI Maturity Audit Campaign contacts sent via Gmail compose (outside Apollo) — a tracking gap now corrected. Priority Accounts task queue execution must begin immediately.

### Email Accounts
| Address | Account ID | Status |
|---------|-----------|--------|
| robert.gorham@testsigma.com | `68e3b53ceaaf74001d36c206` | **DEFAULT (current)** |
| robert.gorham@testsigma.net | `68f65bdf998c4c0015f3446a` | Deprecated (used for earlier batches) |

> **WRITING STYLE RULE (March 2, 2026):** Never use em dashes (the long dash character) in any outreach emails, SOPs, or written communications. Use commas, periods, parentheses, or restructure the sentence instead. This applies globally to all documents and email drafts.

---

## Table of Contents

1. [Intent Data Source](#1-intent-data-source)
2. [Prospect Identification](#2-prospect-identification)
2.5. [LinkedIn Sales Nav ICP Verification (MANDATORY)](#25-linkedin-sales-nav-icp-verification-mandatory) ⛔ HARD STOP — verify before Apollo checks
3. [Qualification Checklist (MANDATORY)](#3-qualification-checklist-mandatory)
4. [Contact Creation & Enrichment](#4-contact-creation--enrichment)
5. [Sequence Loading](#5-sequence-loading)
6. [Email Personalization](#6-email-personalization) ⛔ MANDATORY: Per-Company Research + Researched Subject Lines Required
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

**CRITICAL:** Website visitor data is the primary and preferred source for this sequence. The intent signal from a site visit is a meaningful buying signal that should drive sourcing decisions.

**EXCEPTION (approved March 6, 2026 -- Batch 10):** When the website visitor pipeline is thin (fewer than 20-30 qualified new visitors in a given week), ICP cold outreach via Apollo People Search is an approved supplemental source for this sequence. The sequence itself (messaging angle, tone, personalization standard) remains identical regardless of source. Document the source as "Apollo People Search" or "Apollo Website Visitors" in the tracker so engagement data can be compared over time.

Cold ICP outreach enrolled in this sequence should be held to the same or higher qualification bar: all 9 checks apply, title match must be exact, company must be a strong ICP fit (not just employee count).

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

## 2.5. LinkedIn Sales Nav ICP Verification (MANDATORY)

### ⛔ HARD STOP: Every prospect MUST be verified on LinkedIn Sales Navigator before proceeding to Section 3. NO EXCEPTIONS.

**WHY THIS EXISTS:** The Batch 10 audit (March 6, 2026) found that Apollo People Search returns contacts whose current role, title, or company status does not match ICP -- without any automatic signal that they have changed jobs, been downgraded in seniority, or moved to a non-QE function. Apollo enrichment data can be weeks or months stale. LinkedIn Sales Navigator reflects the person's current public profile and provides real-time buyer intent signals unavailable in Apollo.

**What the Batch 10 audit found:**
- 7 of 61 contacts (11%) were flagged for removal: 2 not found at all, 2 wrong title/seniority (Entry Level), 1 wrong function (IT not QE), 1 no current employer visible, 1 Manager level + possible job departure
- 6 contacts showed active buyer intent signals ("Account has moderate buyer intent") -- a prioritization layer Apollo alone cannot provide
- 1 contact showed a "recently hired" warm signal -- ideal timing for a new-role outreach angle

**Skipping this step means enrolling contacts who have left their company, changed to a non-QE role, or are below the Director+ threshold -- wasting sequence capacity and potentially damaging sender reputation with bad addresses.**

---

### ICP Definition (what you are verifying against)

| Criterion | Requirement |
|-----------|-------------|
| **Title / Seniority** | Director, Sr Director, VP, AVP, Executive Director (or equivalent senior leadership). NOT Manager, Engineer, Architect, or Associate Director without exception. |
| **Function** | Quality Engineering, Test Engineering, QA, DevEx, or closely related. NOT general IT, infrastructure, operations, or security. |
| **Company** | US-based software / SaaS / tech / hardware company. 200+ employees. |
| **Status** | Currently in role at the enrolled company. Active profile. |

---

### How to Verify Each Contact

**Step 1 — Navigate to LinkedIn Sales Navigator**

Always start at `https://www.linkedin.com/sales/home` before searching. This clears any persistent seniority filter artifacts (the "In Training / Entry Level" filter is a known session bug that can silently suppress correct results if you navigate directly to search).

**Step 2 — Search by name + company**

Use the Sales Navigator lead search URL pattern:
```
https://www.linkedin.com/sales/search/people?query=(keywords:[FIRSTNAME LASTNAME],filters:List((type:COMPANY_TYPE,values:List((id:C,text:Public+Companies,selectionType:INCLUDED)))))
```

For most contacts, a simpler approach works: go to Sales Nav > Search > People, type the person's full name in the search bar, and filter by company name. The first result card will show their current title, company, and tenure.

**Step 3 — Read the contact card**

For each contact, record:
- **Current title** (as shown on their LinkedIn profile)
- **Current company** (must match what Apollo enrolled)
- **Tenure in current role** (shown as "X yr Y mo" on Sales Nav)
- **Buyer intent signal** (Sales Nav shows "Account has moderate buyer intent" or similar as a badge on the card when present)
- **Any special signals** (recently hired, job change indicator, etc.)

**Step 4 — Assign a verification status**

| Status | Symbol | Criteria |
|--------|--------|----------|
| PASS | ✅ | Title, function, company, and tenure all confirmed against ICP |
| HOT | 🔥 | PASS + "Account has moderate buyer intent" badge shown on Sales Nav card |
| BORDERLINE | ⚠️ | Close to ICP but one criterion is soft (e.g., Associate Director, adjacent function) -- Rob to decide |
| FLAG | ❌ | Fails ICP on any hard criterion -- wrong title, wrong function, not found, no current employer shown, Manager or below, IT/ops function |

**Step 5 — Log results**

Create a verification log file (e.g., `BatchXX_ICP_Verification_Log.md`) with the following structure:
- ICP definition
- Status key
- Full results table: Name | Company | LinkedIn Title | Tenure | Status | Notes
- Summary table: count by status, list of flagged contacts
- Recommended actions

See `Batch10_ICP_Verification_Log.md` as the canonical reference for format.

---

### Flag Criteria (automatic ❌ removal from sequence)

Remove the contact from the sequence immediately if ANY of the following are true:

1. **Not found on LinkedIn Sales Navigator** -- no profile match for the name + company combination
2. **No current employer visible** -- profile shows no active company (possible recent job departure)
3. **Title is below ICP seniority threshold** -- Manager, Senior Manager, Engineer, Architect, Lead, Associate Director, Principal (unless explicitly approved)
4. **Wrong function** -- IT, infrastructure, security, operations, data engineering, or any non-QE/TE function
5. **Experience at enrolled company ends before present** -- profile shows an end date at the current company (clear job departure signal)
6. **Title is generic + no QE/TE signal** -- e.g., "Technical Area Manager" or "Operations Lead" with no quality engineering specificity

---

### Borderline Criteria (⚠️ Rob to decide)

Flag for human review (do not auto-remove, do not auto-enroll) if:
- Title is "Associate Director" -- one level below the ICP Director threshold
- Title includes QE function but company is in an adjacent vertical (healthcare device, defense, automotive)
- Tenure in current role is less than 3 months -- may still be onboarding, value of outreach is uncertain
- Function is adjacent (DevOps, Platform Engineering, Release Engineering) but not clearly QE

---

### HOT Contact Handling (🔥 buyer intent)

Contacts with the "Account has moderate buyer intent" badge in Sales Nav should be:
1. Enrolled in the sequence as normal
2. Flagged in the verification log and in `email_outreach_tracker.csv` with 🔥 status
3. Prioritized for personalized follow-up after Touch 1 -- if they open or click, move to direct LinkedIn InMail or phone outreach

---

### Known Session Bug: "In Training / Entry Level" Seniority Filter

LinkedIn Sales Navigator has a persistent session bug where a seniority filter ("In Training", "Entry Level") can silently reappear across searches within the same session, potentially hiding Director-level results. This was observed repeatedly during Batch 10 verification.

**Workaround:**
1. Navigate to `https://www.linkedin.com/sales/home` at the start of each verification session to clear session state
2. If search results look unexpectedly sparse for a known Director, check for any active seniority filters in the filter panel and clear them
3. If the filter reappears mid-session, navigate back to Sales Nav home and start a fresh search
4. When in doubt, use a company + name direct URL search rather than the filter-based search interface

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
- Create Gmail drafts for sequence emails (deprecated March 1)
- Send sequence emails directly from Gmail compose
- Use the Gmail API to send or draft sequence emails
- Send from robert.gorham@testsigma.net (deprecated as of March 3, 2026)
- Send to contacts owned by another team member without verifying ownership first

**ALWAYS:**
- Send from **robert.gorham@testsigma.com** (Apollo email account ID: `68e3b53ceaaf74001d36c206`)
- Switch the From dropdown in Apollo composer to testsigma.com (it defaults to testsigma.net)
- Verify contact ownership before sending (check owner_id matches Rob's user ID `68e16f05978e5e000d10a621`)

---

## 6. Email Personalization

> **VERSION 7.0 CHANGE -- MANDATORY:** Every Touch 1 email MUST be written from individual company account research. Generic vertical templates are prohibited. A researched subject line is required for every send. See below for the full mandatory research workflow.

---

### ⛔ MANDATORY GATE: Per-Company Research Before Writing Any Touch 1 Email

**No Touch 1 email may be sent without completing this research step first.** This is a hard gate -- the same standard as the qualification checklist in Section 3.

**Required research for every contact (use Claude/Cowork or manual web search):**

1. **Recent company news** -- product launches, acquisitions, funding rounds, leadership changes, contract wins (within last 6-12 months). Search: `[Company] news 2025 2026`, `[Company] product launch`, `[Company] acquisition`.
2. **Relevant product or platform signals** -- what are they actively shipping? What's changing in their tech stack? What's their most recent major release?
3. **Hiring signals** -- are they actively hiring QE/test engineers? If so, what level and what tools? (LinkedIn, Greenhouse, Lever, Workday, or Apollo enrichment data.) Hiring signals indicate a coverage gap.
4. **Industry/regulatory context** -- are they in a regulated space (FDA, GxP, FedRAMP, gaming compliance, financial services)? This determines the QE angle.
5. **Hardware vs. software test engineering** -- is the contact a software QA leader or a hardware/semiconductor/defense test engineer? Hardware-focused contacts need emails angled at the firmware, SDK, cloud management, or configuration software layers -- not at Selenium/UI automation.

**Minimum viable research = at least ONE specific, verifiable company fact** that could not be in a template sent to any other company.

---

### ⛔ MANDATORY: Researched Subject Lines

**Generic subject lines are prohibited.** Every Touch 1 subject line must reference something specific to that company or person.

**Subject line formula:**
`[Specific company signal or product name], [first name]`

Good examples:
- "Testing Calix One's agentic AI on Vertex AI, Sajay"
- "OTA software test coverage for Skyline OS, Paul"
- "QE coverage as AssetMark adds private markets access, Melissa"
- "Ground software test coverage for ViaSat-3 F2, Paul"

Bad examples (prohibited):
- "Quick question for you, [Name]"
- "Test automation for [Company]"
- "Improving QE at [vertical] companies"
- Any subject line that could be sent to more than one person without editing

**Why this matters:** Subject line open rates are the first conversion gate. A generic subject line signals that the email wasn't written for this person. A specific subject line signals that you did your homework -- which increases open rates and reply quality.

---

### Research-to-Email Workflow (Touch 1 Only)

1. Pull the batch of contacts from the Qualification gate (Section 3)
2. For each contact, open a Claude/Cowork session and run the account research checklist above (8-10 companies in parallel is efficient)
3. Document the key hook for each contact (one sentence -- the specific thing that makes the email not a template)
4. Write the subject line FIRST based on the hook
5. Write the email body (4-6 sentences) with the hook in sentence 1
6. Human review: does sentence 1 reference something that could NOT be in a template? If not, rewrite it.
7. Paste into Apollo task queue and send

**Time estimate:** 3-5 minutes of research per contact when using Claude/Cowork in parallel batches of 8-10. This is not optional -- it is the standard.

---

### Touch 1 Email Writing Standards

- **Sentence 1:** The specific company hook -- a named product, acquisition, contract win, funding event, or platform launch. Must be verifiable. Must not be generic.
- **Sentence 2:** The QE pain or challenge that hook creates -- why does that news create a test engineering problem?
- **Sentence 3:** How Testsigma addresses that specific pain
- **Sentence 4 (optional):** Proof point, context, or relevance bridge
- **Sentence 5:** Low-friction CTA (20-minute conversation, not a full demo)
- **Length:** 4 to 6 sentences max. Never longer.
- **ZERO em dashes** (major AI tell -- use commas, periods, or restructure)
- **No buzzwords:** "revolutionary", "game-changing", "cutting-edge", "best-in-class", "seamless", "robust"
- **No hollow openers:** "I noticed that...", "I came across your profile...", "Hope this finds you well"
- **Sign-off:** First name + "Testsigma" only (no title, no phone number in Touch 1)

---

### Touch 2: Pain-Focused Follow-Up
- Reference Touch 1 without being pushy
- Lead with a specific pain point for their industry
- Include a proof point (case study, metric, customer reference)

### Touch 3: Breakup
- Short and direct
- Offer value even if they are not interested (resource, insight)
- Clear final CTA

---

## 7. Daily Workflow

### Morning Block (30 min): Prospect Identification
1. Open Apollo Web Analytics > Website Visitors
2. Filter for high-intent pages (pricing, demo, features, comparison)
3. Filter: 200+ employees, US geography
4. Export list of visitor companies
5. For each company, find the right persona (see Section 2)

### ⛔ MANDATORY GATE: LinkedIn Sales Nav ICP Verification (20-30 min per batch)
5a. **Navigate to `https://www.linkedin.com/sales/home` first** (clears session filter artifacts)
5b. **Verify every candidate on LinkedIn Sales Navigator** (see Section 2.5 for full process):
   - Confirm title matches ICP seniority (Director, Sr Director, VP, AVP, Executive Director)
   - Confirm function is QE/TE (not IT, ops, security, or generic engineering)
   - Confirm person is currently at the enrolled company (no end date shown)
   - Note buyer intent badges (🔥 HOT) and recently hired signals
5c. **Assign status to each candidate** (✅ PASS, 🔥 HOT, ⚠️ BORDERLINE, ❌ FLAG)
5d. **Remove all ❌ FLAG contacts from the candidate list immediately** -- do not proceed them to Apollo qualification checks
5e. **Escalate ⚠️ BORDERLINE contacts to Rob** before proceeding
5f. **Log all results in a BatchXX_ICP_Verification_Log.md file** (see Batch10 log as reference)
**Only PASS and HOT contacts proceed to the Apollo qualification checklist below.**

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
11. **MANDATORY:** Use Claude/Cowork to run per-company account research for every contact (see Section 6 mandatory research checklist). No email may be written without completing this step first. Run 8-10 companies in parallel for efficiency.
12. **For contacts with prior outreach history (MEDIUM RISK):** customize messaging to acknowledge relationship, don't send generic templates
13. Human review each email (2 min each) for accuracy and tone
14. **Send via Apollo UI task queue ONLY** — open each task in Apollo > Sequences > Tasks, paste personalized email, click Complete to send. Do NOT use Gmail or Gmail API drafts.

### End of Day Block (15 min): Logging
15. Update `prospect_master_tracker.md` with new additions (include check results)
16. Update `email_outreach_tracker.csv` with sent emails (Date, Prospect, Company, Title, Email, Sequence, Channel, Touch Number, Angle, CTA Type)
17. **Update engagement tracking (NEW — March 6, 2026):** Check Apollo sequence analytics for open/reply status on all Touch 1 sends from the prior 7 days. In Apollo: Sequences → [Sequence] → Contacts tab → filter by step. Update the Opened?, Replied?, Positive Reply?, and Outcome Notes columns in email_outreach_tracker.csv accordingly.
18. Note any catchall domains to monitor
19. Flag any contacts that need team coordination (territory overlaps)
20. Push updates to workspace/repo

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
12. **`contacts_without_ownership_permission` skip reason means the contact was created by a different team member.** Apollo will not enroll them. Options: coordinate with the owner, or create a new contact record under your ownership using `run_dedupe: false`. Found March 6, 2026: Joe Klos (AdCellerant) and Carol Botsala (symplr) skipped for this reason.
13. **`contact_not_found` means the Apollo contact ID no longer resolves in the sequence API.** The contact may have been deleted or the ID is incorrect. Check the contact's Apollo profile directly. Found March 6, 2026: Rick Smith (Arrowhead Products) returned this error -- verify the correct Apollo contact ID before re-attempting enrollment.
14. **`contacts_active_in_other_campaigns` skips contacts already in an active sequence.** Apollo enforces this server-side even when the qualification check passes. Found March 6, 2026: Orone Laizerovich (Forescout) skipped for this reason. Check `contact_campaign_statuses` more carefully in the qualification pass.
15. **When running ICP cold outreach batches, use the 30-day cooldown rule strictly.** Even though contacts are cold, checking sequence history is still mandatory. Ramon Dominguez (Alarm.com) was held out of Batch 10 due to recent sequence activity -- 30-day cooldown applies.

**Batch 10 Results Summary (March 6, 2026 -- ICP Cold Outreach):**
- 69 contacts created in Apollo, sourced via Apollo People Search ICP filter
- 65 submitted for enrollment (4 manual exclusions: Ramon Dominguez -- cooldown, Phil Jones -- active sequence, Dickson Wu -- evaluation, Angela Liu -- evaluation)
- 61 enrolled successfully (active status in Tier 1 Intent sequence)
- 4 skipped by Apollo: Rick Smith (contact_not_found), Joe Klos (ownership), Orone Laizerovich (active in other campaign), Carol Botsala (ownership)
- 61 personalized Touch 1 emails drafted and saved to `touch1_emails_Q1_Tier1.md`
- All 61 contacts logged in `email_outreach_tracker.csv` and `prospect_master_tracker.md` (Section 8)

---

## 9. Troubleshooting & Edge Cases

### Apollo skip reason: `contacts_without_ownership_permission`
Apollo rejects enrollment when the contact was created by a different team member and your account lacks ownership. Two options:
1. **Preferred:** Contact the owner and ask them to enroll the person, or confirm they're not working the account.
2. **Alternative:** Create a new duplicate contact record using `run_dedupe: false` with your Apollo user ID as owner. This creates a parallel record -- acceptable when the original owner is not actively working the account.
Real examples (March 6, 2026): Joe Klos (AdCellerant), Carol Botsala (symplr).

### Apollo skip reason: `contact_not_found`
Apollo rejects enrollment when the contact ID doesn't resolve. This usually means the contact was deleted, or the ID was captured incorrectly.
**Fix:** Search for the person by name in `apollo_contacts_search`. If found under a different ID, re-attempt enrollment with the correct ID. If not found, re-create the contact.
Real example (March 6, 2026): Rick Smith (Arrowhead Products) -- ID `69ab2e421e3d4300191d7b26` returned `contact_not_found`.

### Apollo skip reason: `contacts_active_in_other_campaigns`
Apollo rejects enrollment when the contact already has an active sequence (even if the qualification check appeared to pass). This can happen when a contact was enrolled in a sequence between the time you ran checks and the time you submitted the enrollment call.
**Fix:** Check `contact_campaign_statuses` in real time immediately before submitting the enrollment batch. If the contact has an active sequence, hold them per the 30-day cooldown rule.
Real example (March 6, 2026): Orone Laizerovich (Forescout) -- skipped for this reason.

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
- **Tier 1 Intent Sequence:** `69a1b3564fa5fa001152eb66`
- **Priority Accounts Sequence:** `69a05801fdd140001d3fc014`
- **AI Maturity Audit Campaign for QA:** `6909f6b00f9bb2001d599d5e` *(Added March 6, 2026)*
- **Your User ID:** `68e16f05978e5e000d10a621`
- **Your Email Account (DEFAULT):** `68e3b53ceaaf74001d36c206` (robert.gorham@testsigma.com)
- **Your Email Account (DEPRECATED):** `68f65bdf998c4c0015f3446a` (robert.gorham@testsigma.net)
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

### Tier 1 Intent Sequence Stats (Updated March 6, 2026 -- v6.0)
- Total contacts: 152 (91 prior batches + 61 Batch 10 ICP cold outreach enrolled March 6)
- Touch 1 sent: 90 (prior batches -- all sent via Apollo task queue)
- Touch 1 PENDING: 61 (Batch 10 -- in Apollo task queue, awaiting Rob's manual send from touch1_emails_Q1_Tier1.md)
- At Step 2 (awaiting Touch 2): 70
- Step 2 blocked ("Reply to thread" error): 5 remaining (Tom Yang DNC'd; 5 errors addressed March 6)
- Finished / Stopped: 6
- Bounced: 1 (Kenny Liu, ModMed)
- NEW JOB flag: 1 (Pallavi Sheshadri, moved to Ampersand)
- Confirmed replies: 1 (Pallavi Sheshadri -- engaged 3x, then cold after demo ask)
- Open rate (Apollo): ~6% filtered / 53% unfiltered (as of March 1 snapshot; not updated since)
- Dual-sequencing violations resolved March 6: 3 (Scott Carruth, Ryan Aspleaf, Emre Ozdemir -- all stopped in Priority Accounts)
- Batch 10 source: Apollo People Search ICP cold outreach (approved supplemental source -- see Section 1)

### Priority Accounts Sequence Stats (Updated March 6, 2026 — CORRECTED)
- Total contacts enrolled: 285
- **InMails sent via Apollo task queue: 0 — SEQUENCE HAS NEVER BEEN EXECUTED**
- "New" at Step 1 (no prior activity anywhere): ~242
- "Attempted to Contact" at Step 1 (stage from prior sequences, NOT this one): ~36
- Finished (stopped): 3 (Rashad Fambro, Amir Aly, Vinayak Singh)
- **⚠️ NOTE (March 6 audit correction):** The "19 emails sent via Apollo manual composer March 3" previously recorded here were to AI Maturity Audit Campaign contacts, NOT Priority Accounts contacts. Those were sent via Gmail outside Apollo. Priority Accounts has had zero outreach. See `sequence_status_report_mar6.md` Section 9 for full reconciliation.

### AI Maturity Audit Campaign for QA Stats (as of March 6, 2026)
- Total contacts enrolled: 142
- Apollo task queue executions: Unknown (full audit not yet run)
- Gmail emails sent outside Apollo (March 3): 19 contacts (logged in email_outreach_tracker.csv, Apollo notes pending)
- Task backlog: ~255 overdue tasks (confirmed via Apollo daily digest, March 6)
- Full audit needed: Pull stage/step breakdown, check Step 2 errors, confirm send status per contact

### Related Files in Workspace
- `prospect_master_tracker.md` - Running tracker of all prospects and their status
- `Batch10_ICP_Verification_Log.md` - **LinkedIn Sales Nav ICP verification log for all 61 Batch 10 contacts** (March 6, 2026 -- 49 PASS, 7 HOT, 1 BORDERLINE, 7 FLAGGED for removal; canonical reference for Section 2.5 format)
- `tier1_sequence_audit_report.md` - Full sequence audit report (68 contacts, risk-tiered SF analysis)
- `BDR/data/trackers/engagement_audit_mar1.md` - Extended engagement audit (25 contacts, 5 CRITICAL removals)
- `email_outreach_tracker.csv` - Detailed outreach log with engagement data
- `daily_prospecting_workflow.md` - Daily workflow with time estimates
- `outreach_email_sop.md` - End-to-end email creation and send process (covers both sequences)
- `touch1_emails_Q1_Tier1.md` - **Batch 10 Tier 1 Intent Touch 1 emails** (61 personalized drafts, segmented by industry vertical, generated March 6)
- `batch8_touch1_drafts.md` - **Batch 8 Priority Accounts emails** (21 case-study personalized drafts, 19 sent Mar 3)
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

2. **"Verify these candidates on LinkedIn Sales Navigator"** ⛔ MANDATORY HARD STOP — NEVER SKIP
   - Claude will open LinkedIn Sales Navigator starting from `https://www.linkedin.com/sales/home`
   - Claude will search each candidate by name + company and read their current profile card
   - Claude will verify: title seniority (Director+), function (QE/TE), current employer, and note any buyer intent or recently hired signals
   - Claude will assign ✅ PASS, 🔥 HOT, ⚠️ BORDERLINE, or ❌ FLAG status to each contact
   - Claude will create a `BatchXX_ICP_Verification_Log.md` with full results, summary, and recommended actions
   - **❌ FLAG contacts are removed from the candidate list before any Apollo checks run**
   - **⚠️ BORDERLINE contacts are escalated to Rob before proceeding**
   - **Only PASS and HOT contacts advance to Step 3**

3. **"Run qualification checks on these prospects"** ⛔ MANDATORY — NEVER SKIP
   - Claude will run ALL 6 checks: existing sequences, active sequences, Salesforce ownership, email verification, duplicate contacts, job verification
   - Claude will check `contact_campaign_statuses` for prior outreach history and `inactive_reason` notes
   - Claude will check BOTH `owner_id` (Apollo) AND `crm_owner_id` (Salesforce) for territory conflicts
   - Claude will flag catchall domains and contacts with prior BDR outreach custom fields
   - **Only CLEAN contacts proceed. FLAG contacts need human review. FAIL contacts are rejected.**

4. **"Create contacts and add clean ones to the Tier 1 sequence"**
   - Claude will create contacts with `run_dedupe: true`
   - Claude will add to sequence `69a1b3564fa5fa001152eb66` via API
   - Claude will NOT add any contact that failed checks in steps 2 or 3

5. **"Write personalized Touch 1 emails for the new additions"**
   - Claude will enrich companies, research, and draft emails following the template guidelines
   - For MEDIUM-RISK contacts (prior outreach), Claude will customize messaging

6. **"Update the tracker"**
   - Claude will append to `prospect_master_tracker.md` and `email_outreach_tracker.csv`
   - Claude will include check results and flag notes for each contact

---

*This SOP is the single source of truth for the Q1 Website Visitor - Tier 1 Intent and Q1 Priority Accounts sequences. Update it whenever the process changes.*

*Changelog:*
- *v8.0 (March 6, 2026) -- LinkedIn Sales Navigator ICP verification gate added as mandatory Section 2.5, positioned between Prospect Identification (Section 2) and Qualification Checklist (Section 3). Gate requires verifying title, function, current employer, and tenure for every contact before Apollo checks run. Status codes: PASS, HOT (buyer intent), BORDERLINE, FLAG. Batch 10 audit found 7 of 61 contacts (11%) required removal; 6 had active buyer intent signals; 1 had recently hired warm signal. Daily Workflow updated with Sales Nav verification steps (5a-5f). Cowork Quick Start updated with new step 2 for Sales Nav verification. Known session bug (In Training / Entry Level filter) documented with workaround. Batch10_ICP_Verification_Log.md added to related files as canonical format reference.*
- *v6.0 (March 6, 2026) -- Batch 10 ICP cold outreach: 69 contacts created, 61 enrolled in Tier 1, 8 excluded. ICP cold outreach approved as supplemental source. New skip reasons documented (contacts_without_ownership_permission, contact_not_found, contacts_active_in_other_campaigns). Tier 1 total updated to 152 contacts. touch1_emails_Q1_Tier1.md added to related files.*
- *v5.0 (March 6, 2026) -- AI Maturity Audit Campaign sequence added; Priority Accounts corrected to 0 InMails sent; Mar 6 audit findings integrated; dual-sequencing violations documented; engagement tracking step added.*
- *v4.0 (March 3, 2026) -- Priority Accounts sequence added with manual email composer workflow; testsigma.com is now the default send address; Batch 8 results integrated (19/20 sent); ownership verification added as mandatory pre-send check; Sr SDET title deprioritization documented; case-study personalized email style documented for Priority Accounts.*
