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

Touch 2 is a reply-thread follow-up sent 3 days after Touch 1 via the Apollo task queue. It arrives in the same email thread, so the prospect sees both messages together. The goal is a new angle with a different proof point — not a rehash of Touch 1.

**Full Touch 2 writing standards, structure, QA checklist, and annotated example: see Section 11.**

### Touch 3: Final Touch

Touch 3 is a new-thread email sent 6 days after Touch 2 (9 days after Touch 1). It arrives as a standalone subject line — a clean slate. The tone shifts slightly: direct, confident, no apologies. It is not a "breakup email." It is a final, well-aimed shot with a fresh angle.

**Full Touch 3 writing standards, structure, QA checklist, and annotated example: see Section 12.**

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

---

## 11. Touch 2 Writing Standards: Pain-Focused Follow-Up

### Overview

Touch 2 is Step 2 in the Apollo Q1 Website Visitor - Tier 1 Intent sequence. It sends as a **reply to the original Touch 1 thread**, which means it arrives inside the same email conversation. The prospect sees both messages together. This is an advantage: the context is already established, so you do not need to re-introduce yourself or re-explain who Testsigma is.

Touch 2 is sent **3 days after Touch 1** via the Apollo task queue. Never send it manually outside Apollo.

The goal of Touch 2 is not to repeat what you said in Touch 1. It is to show up with something new: a different proof point, a different angle on the pain, or a company-specific insight you did not use in Touch 1. If Touch 1 was about test maintenance overhead and used the Hansard proof point, Touch 2 should approach from a different direction, such as release velocity or coverage scale, with a different customer story. The prospect should feel like you are adding value with each message, not just following up for the sake of following up.

---

### 11.1 Technical Parameters

| Parameter | Requirement |
|-----------|-------------|
| Apollo step | Step 2 (reply thread) |
| Send timing | 3 days after Touch 1 |
| Thread type | Reply to Touch 1 thread |
| Subject line | Inherits Touch 1 subject (no new subject needed) |
| Send channel | Apollo task queue ONLY |
| Word count | 40 to 70 words (strict) |
| Paragraphs | 3 to 4 short paragraphs, each separated by a blank line |
| Questions | 1 to 2 maximum |
| Sign-off | "Cheers, Rob" |

**Important:** Because Touch 2 is a reply thread, it does NOT need a new subject line. Apollo handles the threading automatically. Never write a new subject line field for Touch 2 — the field stays blank or inherits the original.

---

### 11.2 Required Opening Line

Touch 2 must open with a brief acknowledgment that you have reached out before, without being apologetic or pushy. The canonical opening is:

> "One more thought, [First Name],"

This is not a rule that can be swapped for something more creative. "One more thought" works because it frames the follow-up as value-additive rather than status-checking. It does not say "I wanted to follow up on my previous email" (a soft, passive opener), nor does it say "Did you get a chance to look at my last message?" (which asks the prospect to justify their silence).

Variations that are acceptable:
- "One more thing, [First Name],"
- "Quick addition, [First Name],"

Variations that are **not** acceptable:
- "Just circling back..." (passive, adds no value)
- "Wanted to follow up on my last email..." (asks them to explain why they did not reply)
- "Hope you had a chance to review my message..." (same problem)
- "I know you're busy, but..." (apologetic, undermines confidence)
- "Not sure if you saw my last email..." (implies they may have ignored you)

---

### 11.3 Structure

Touch 2 has three or four short paragraphs. Every paragraph is separated by a blank line. No paragraph exceeds two sentences.

**Paragraph 1: Opening + angle pivot**
Start with the canonical opening line ("One more thought, [First Name],") followed by one sentence that introduces the new angle. This is not a rehash of Touch 1 — it is a pivot to a different dimension of the same problem or a different problem altogether.

Example: "One more thought, [First Name], about what happens to test coverage when a team scales fast."

**Paragraph 2: Proof point**
One proof point — a named customer, a real number, a concrete outcome. This must be different from the proof point used in Touch 1. The proof point should be one sentence, never two. No introductory clause like "For example, one of our customers..." — just state it directly.

Example: "Medibuddy automated 2,500 tests and cut maintenance by 50% in under six months."

**Paragraph 3: Close**
The close must do two things: (a) connect the proof point outcome to the prospect's situation, and (b) use a "what day works" meeting ask. The close cannot be generic. If it could be pasted into a different prospect's message without editing a single word, it is not good enough. Reference something specific to them: their company name, their platform, their vertical, or their likely pain.

Example: "If that kind of test coverage improvement sounds relevant for the [Company] platform, what day works for a quick look?"

**Paragraph 4 (optional): Sign-off**
"Cheers, Rob" — no title, no phone number, no links.

---

### 11.4 Proof Point Selection

Touch 2 requires a proof point that is:
- **Different from Touch 1** — never repeat the same customer story
- **Named** — a specific company, not "a Fortune 500 company" or "one of our customers" (anonymous references underperform)
- **Specific** — includes a real number or measurable outcome
- **Matched to the prospect's pain** — pick from the rotation table based on what pain angle Touch 2 is addressing

**Proof point rotation table (use to avoid Touch 1 repeats):**

| If Touch 1 used... | Touch 2 should use... |
|--------------------|-----------------------|
| Hansard (regression 8wk to 5wk) | Medibuddy (2,500 tests, 50% maintenance cut) OR Sanofi (3 days to 80 minutes) |
| Medibuddy (2,500 tests, 50% cut) | Hansard (8wk to 5wk) OR CRED (90% regression, 5x faster) |
| CRED (90% coverage, 5x faster) | Sanofi (3 days to 80 min) OR Nagra DTV (2,500 tests, 4x faster) |
| Sanofi (3 days to 80 min) | Hansard OR Medibuddy |
| Fortune 100 (3x productivity) | Spendflo (50% manual testing cut) OR Medibuddy |
| Generic/no proof point in Touch 1 | Any named proof point works — pick based on vertical |

**Stat framing rule (same as Touch 1):** Always use reduction framing ("cut by X%", "from X to Y", "X fewer weeks") rather than multiplier framing ("X times faster"). Reduction framing is believable. Multiplier framing sounds like marketing copy.

---

### 11.5 What NOT to Write

The following patterns are banned in Touch 2. Each one has either a data penalty or a structural reason.

**Do not apologize for following up.**
Every apology signals that you do not believe your message is worth reading. "Sorry to bug you again" or "I know you're busy" or "I don't want to clog your inbox" all undermine the message before it starts. Touch 2 should arrive with the same confidence as Touch 1.

**Do not use bullet lists.**
HC5 (Hard Constraint 5): bullet points and numbered lists correlate with lower reply rates. Touch 2 is already short — there is no need to fragment it further with lists.

**Do not use "I noticed" or "I saw."**
HC1 (Hard Constraint 1): strongest negative signal in the data, -13.4 pp differential. "One more thought, [First Name]" is the replacement. It acknowledges the prior message without the surveillance framing of "I noticed."

**Do not rehash Touch 1.**
Touch 2 arriving as a reply thread means the prospect can scroll up to read Touch 1 anytime. There is no need to summarize it. Every sentence in Touch 2 should be new information or a new angle. If you find yourself writing a sentence that could have appeared in Touch 1, delete it.

**Do not use easy-out closes.**
"No worries if not," "if this isn't relevant, totally fine," "feel free to ignore this if the timing isn't right" — all banned. These train the prospect to dismiss your email before they consider it. The close should be confident and specific. If you are not certain enough in the value to ask directly, the email is not ready to send.

**Do not use an open-ended question as the close.**
Data: open-ended question closes = 14.0% reply rate. "What day works" = 40.4% reply rate. Close with a meeting ask, not a philosophical question.

**Do not go over 70 words.**
Touch 2 is a follow-up in an existing thread. The prospect already has context. More words do not add more value — they add more friction. If the draft exceeds 70 words, cut something.

**Specific banned phrases:**
- "Circling back" or "circling back quickly"
- "Just wanted to follow up" / "wanted to touch base"
- "As I mentioned in my last email"
- "Did you have a chance to review"
- "I know you're busy"
- "No worries if this isn't relevant"
- "Flaky tests" (toxic phrase, -11.9 pp)
- "CI/CD" (toxic phrase, -5.1 pp)

---

### 11.6 Touch 2 QA Checklist (Run Before Every Send)

Before marking the Apollo task complete and queuing the send, verify all of the following:

- [ ] Opens with "One more thought, [First Name]," (or accepted variant)
- [ ] Word count is 40 to 70 words
- [ ] No more than 2 question marks in the entire message
- [ ] Proof point is different from the one used in Touch 1
- [ ] Proof point is a named customer (not anonymous)
- [ ] Proof point includes a specific number or measurable outcome
- [ ] No HC1 violation ("I noticed," "I saw," "I see")
- [ ] No HC5 violation (no bullet points or numbered lists)
- [ ] No easy-out close ("no worries," "feel free to ignore," "totally fine if not")
- [ ] Close uses "what day works" pattern
- [ ] Close references the proof point outcome AND the prospect's specific situation
- [ ] Sign-off is "Cheers, Rob" (no title, no phone, no link)
- [ ] No more than 1 hyphen used as a mid-sentence dash in the body
- [ ] Every paragraph is separated by a blank line
- [ ] No placeholder text remains ([Company], [First Name] tokens resolved)
- [ ] Sent via Apollo task queue (not Gmail compose)

**If any item fails:** fix before sending. Do not send a Touch 2 that fails even one check.

---

### 11.7 Annotated Touch 2 Example

**Scenario:** Prospect is Director of QA at a mid-size SaaS company. Touch 1 used the Hansard proof point (regression 8 weeks to 5 weeks). Touch 2 pivots to coverage scale with the Medibuddy proof point.

---

**Email body:**

One more thought, [First Name], about what test coverage looks like when a team grows quickly.

Medibuddy automated 2,500 tests and cut maintenance by 50% in under six months — without rebuilding their test infrastructure.

If keeping coverage ahead of your release pace sounds like a real challenge at [Company], what day works for a quick look?

Cheers, Rob

---

**Why it works:**
- Opens with "One more thought" — acknowledges the prior message without asking them to explain the silence
- Pivots to a new angle (coverage scale) different from Touch 1 (regression time)
- Proof point is named (Medibuddy), specific (2,500 tests, 50% cut, 6 months), and framed as reduction
- Close references the proof point outcome ("coverage ahead of release pace") and ties it to their situation ("[Company]")
- Close uses "what day works" — direct meeting ask, no easy out
- 47 words — well within the 40-70 word target
- Sign-off is "Cheers, Rob" — no extras
- Zero em dashes, zero bullet lists, zero HC violations

---

### 11.8 Timing and Apollo Task Execution

Touch 2 becomes available in the Apollo task queue 3 days after Touch 1 is marked complete. It will appear as a "Reply thread" task — the interface shows the original thread context.

**Execution steps:**
1. Open Apollo task queue and filter for Touch 2 tasks
2. Review the task — it will show the prospect name, company, and original Touch 1 content
3. Read the Touch 1 copy to confirm what proof point and angle were used (so Touch 2 can use something different)
4. Write or paste the Touch 2 copy into the reply box
5. Verify line breaks are preserved (Apollo sometimes collapses them — fix manually)
6. Run the QA checklist (Section 11.6) before marking the task
7. Mark the task complete — Apollo sends the email

**Do not:** write the reply in Gmail and send manually. All sends must go through the Apollo task queue for tracking, sequence integrity, and engagement data capture.

---

## 12. Touch 3 Writing Standards: Final Touch

### Overview

Touch 3 is Step 3 in the Apollo Q1 Website Visitor - Tier 1 Intent sequence. It sends as a **new email thread** — a completely fresh subject line, not a reply to the Touch 1 or Touch 2 thread. The prospect's inbox shows it as a new conversation. This gives you one more clean shot after the prior two messages.

Touch 3 is sent **6 days after Touch 2** (Day 9 from Touch 1) via the Apollo task queue. The subject line is fixed: **"Should I close the loop?"**

Touch 3 is not a breakup email. The old template called it that, and the old template was wrong. A breakup email is apologetic, gives the prospect an easy out, and signals that you expect to be ignored. That framing produces weak closes ("either way, best of luck this quarter") that abandon the meeting ask entirely. Touch 3 should arrive with the same directness as Touch 1. It is short, it uses a new proof point, and it ends with a confident close. The only difference is that it is even shorter — because at this point, the prospect has seen your name twice, the context is built, and additional words do not help.

---

### 12.1 Technical Parameters

| Parameter | Requirement |
|-----------|-------------|
| Apollo step | Step 3 (new thread) |
| Send timing | 6 days after Touch 2 (9 days after Touch 1) |
| Thread type | New thread — NOT a reply |
| Subject line | "Should I close the loop?" (fixed) |
| Send channel | Apollo task queue ONLY |
| Word count | 40 to 60 words (strict) |
| Paragraphs | 2 to 3 short paragraphs, each separated by a blank line |
| Questions | 1 maximum |
| Sign-off | "Best, Rob" OR "Cheers, Rob" |

**Important:** Touch 3 arrives as a new thread. The subject line "Should I close the loop?" is a fixed value — it is already loaded in the Apollo sequence template. Do not change it. The subject line is deliberately short and personal; it has above-average open rates for a final touch because it does not read like a mass-send.

---

### 12.2 Tone and Approach

Touch 3 is the shortest message in the sequence. By the time it arrives, the prospect has had 9 days and two previous messages. They know who you are. Do not re-introduce yourself. Do not summarize what Testsigma does. Do not reference Touches 1 and 2 explicitly.

The tone is direct and confident. It is not apologetic, not passive, and not soft. Think of it as the final pitch from a colleague who has already made their case twice and is asking one more time with a new angle before moving on. That posture — confident, not desperate — is what makes Touch 3 work when it does work.

**What Touch 3 is:**
- A fresh angle on the problem (different from Touches 1 and 2)
- A new proof point (third different customer story)
- A clean, direct close with "what day works"
- Short enough to read in 10 seconds

**What Touch 3 is not:**
- A summary of the previous two messages
- A "last chance" guilt trip
- An apology for following up
- A resource dump ("here is a link to our case study")
- An easy-out close ("no worries if the timing isn't right")

---

### 12.3 Structure

**Paragraph 1: New angle + proof point**
One to two sentences. Open directly with a QA pain or outcome — no preamble. State the proof point in the same breath.

Example: "Sanofi cut regression from 3 days to 80 minutes after standardizing test execution on Testsigma."

**Paragraph 2: Prospect-specific relevance bridge**
One sentence. Connect the proof point outcome to something specific about the prospect's situation: their company, their vertical, their likely pain, or their recent company event. This sentence does the personalization work that makes the close land.

Example: "With [Company] scaling across [product/platform], regression overhead tends to grow faster than the QA team."

**Paragraph 3: Close**
One sentence, using the "what day works" pattern, tied to the proof point outcome. No easy out. No soft ask. The meeting ask should feel like a natural next step, not a last-ditch plea.

Example: "If going from 3 days to 80 minutes sounds worth exploring, what day works for a quick look?"

**Sign-off:** "Best, Rob" (Touch 3 can use "Best" as a slightly more formal close for the final message, though "Cheers, Rob" is also acceptable).

---

### 12.4 Proof Point Selection

Touch 3 requires a proof point that has not appeared in Touches 1 or 2. The proof point must be:
- A third different customer story
- Named (not anonymous)
- Specific (real number or measurable outcome)
- Matched to a pain angle not already used in the sequence

**Three-touch proof point planning (do this before drafting the sequence):**

| Touch | Angle | Proof Point |
|-------|-------|-------------|
| Touch 1 | Maintenance / test upkeep | Hansard (8wk to 5wk) |
| Touch 2 | Coverage scale | Medibuddy (2,500 tests, 50% cut) |
| Touch 3 | Execution speed / velocity | Sanofi (3 days to 80 min) OR CRED (90% coverage, 5x faster) |

Vary the starting point based on what fits the prospect's context. The key rule: no proof point repeats across the 3-touch sequence.

**Fallback if no third proof point fits naturally:** Cisco (35% regression reduction, enterprise scale) or Spendflo (50% manual testing cut, quick win for smaller teams).

---

### 12.5 Subject Line Context

The fixed subject "Should I close the loop?" does specific work. It:
- Implies a prior relationship (because there is one — two prior messages)
- Creates a micro-tension that prompts opens ("close the loop on what?")
- Signals finality without being passive-aggressive
- Is short enough to display fully on mobile

Do not change this subject line. Do not test variations of it within this sequence. If you want to test subject lines, do it on Touch 1.

---

### 12.6 What NOT to Write

**Do not use the old "breakup" framing.**
The old Touch 3 template from `website_visitor_sequence_drafts.md` said: "I don't want to be that person who keeps emailing, so I'll keep this short — if test automation isn't a priority for [Company] right now, totally understood." Every sentence in that template is wrong. "I don't want to be that person" is apologetic. "If test automation isn't a priority, totally understood" is an easy out that lets the prospect off without engaging. "Either way, wishing you a great quarter" abandons the CTA entirely. Do not write any of this.

**Do not summarize or reference prior messages.**
Touch 3 arrives as a new thread. The prospect does not need to be reminded that you sent two prior messages. Just bring the new proof point and close cleanly.

**Do not use "I noticed," "I saw," or "I came across."**
HC1 applies to Touch 3 as much as Touch 1.

**Do not use bullet points or lists.**
HC5 applies. Touch 3 is already 40-60 words — bullets would fragment it into something that looks like a feature advertisement.

**Do not offer a resource as a substitute for a meeting.**
"Feel free to bookmark this link" or "Here is a case study you can review" replaces the meeting ask with homework. The prospect's attention is most valuable now, when they are reading this email. Redirect that attention to a meeting, not a document.

**Do not use "no worries" or "totally fine" or "if not, all good."**
These are easy outs. They undercut the confidence of the close. Touch 3 ends with a meeting ask, same as Touch 1 and Touch 2. No apologies, no escape hatches.

**Banned phrases for Touch 3:**
- "I don't want to keep emailing"
- "I'll keep this short" (you are already keeping it short — no need to announce it)
- "Totally understood if the timing isn't right"
- "No worries if not"
- "Either way, best of luck"
- "Feel free to reach back out when the time is right"
- "Circling back"
- "Following up one last time"
- "Flaky tests" (toxic phrase, -11.9 pp)
- "CI/CD" (toxic phrase, -5.1 pp)

---

### 12.7 Touch 3 QA Checklist (Run Before Every Send)

Before marking the Apollo task complete and queuing the send, verify all of the following:

- [ ] Subject line is "Should I close the loop?" (no modification)
- [ ] Word count is 40 to 60 words
- [ ] Proof point is different from both Touch 1 and Touch 2
- [ ] Proof point is a named customer
- [ ] Proof point includes a specific number or measurable outcome
- [ ] Tone is direct and confident — no apologies, no easy outs
- [ ] No reference to prior messages ("as I mentioned," "in my last email," etc.)
- [ ] No HC1 violation ("I noticed," "I saw")
- [ ] No HC5 violation (no bullet points)
- [ ] Close uses "what day works" pattern
- [ ] Close is tied to the proof point outcome and the prospect's specific situation
- [ ] No easy-out language anywhere in the message
- [ ] Maximum 1 question mark in the entire email
- [ ] Sign-off is "Best, Rob" or "Cheers, Rob" — no title, no phone, no link
- [ ] No more than 1 hyphen as a mid-sentence dash in the body
- [ ] Every paragraph is separated by a blank line
- [ ] No placeholder text remains
- [ ] Sent via Apollo task queue (not Gmail compose)

---

### 12.8 Annotated Touch 3 Example

**Scenario:** Prospect is QA Manager at a healthcare SaaS company. Touch 1 used Hansard (regression 8wk to 5wk, maintenance angle). Touch 2 used Medibuddy (2,500 tests, 50% cut, scale angle). Touch 3 pivots to execution speed with Sanofi.

---

**Subject:** Should I close the loop?

**Email body:**

Sanofi cut regression testing from 3 days to 80 minutes after standardizing on Testsigma.

For a healthcare platform like [Company], where release delays carry real risk, that kind of time compression usually matters.

If cutting 2+ days out of every regression cycle sounds useful, what day works for a quick look?

Best, Rob

---

**Why it works:**
- Subject line does its job quietly — "Should I close the loop?" prompts opens without being manipulative
- No re-introduction, no preamble — arrives directly with the proof point
- Proof point is Sanofi (new, not used in Touches 1 or 2), named, specific (3 days to 80 minutes), reduction framing
- Relevance bridge connects healthcare compliance ("release delays carry real risk") to their world
- Close references the proof point outcome specifically ("2+ days out of every regression cycle")
- Close uses "what day works" — direct meeting ask, no escape hatch
- 53 words — within the 40-60 word target
- Sign-off is "Best, Rob" — clean and professional for a final touch
- Zero apologies, zero easy outs, zero HC violations

---

### 12.9 After Touch 3: Sequence Complete

When Touch 3 is sent, the Apollo sequence is complete for this contact. There are no more scheduled steps.

**Do not send a 4th touch** unless one of the re-engagement triggers fires (job posting at their company, funding announcement, leadership change, major product launch, Testsigma major feature release). Re-engagement requires a minimum 60-day gap from the last touch.

**Update the tracker:**
- Mark the contact's `cadence_status` as COMPLETE in any tracking doc
- Update `email_outreach_tracker.csv` if the contact appears there
- If the contact replied at any point in the sequence, move them to the reply handling workflow (Section 13)

If you need to resume outreach to this contact after the re-engagement window, treat it as a fresh sequence with a new angle and new proof points — never reference the prior sequence or ask why they did not reply.

---

## Section 13: Reply Handling — Response Frameworks by Reply Type

### Purpose of This Section

Every reply is a data point and an opportunity. The way Rob responds to a reply determines whether a conversation advances to a meeting, stalls, or dies. This section defines the complete response framework for every type of reply that can come from this sequence — positive, negative, referral, out-of-office, curiosity, timing objection, tool objection, wrong person, and auto-reply.

**The cardinal rule:** Respond the same day, ideally within two hours of receiving the reply. Reply speed is the single highest-leverage action after sending the initial message. A prompt response signals respect and keeps the conversation alive before the prospect moves on mentally.

All replies come into robert.gorham@testsigma.com. Monitor Gmail daily during the session audit (Phase 1 Intel Scan).

---

### 13.1 Reply Type Classification

Before drafting a response, classify the reply into one of these eight types. The classification determines which framework below applies.

| Type | Signals | Examples |
|------|---------|---------|
| **Positive / Interested** | They want to learn more, agree to a call, ask how it works, or signal timing alignment | "Happy to connect," "Let's set something up," "Good timing actually," "Tell me more" |
| **Negative / Not Interested** | Explicit decline, disqualified by role/scope, budget block | "Not interested," "Not a priority," "We don't do software testing," "We're fully staffed on this" |
| **Timing Objection** | In principle interested but blocked now | "Reach out in Q3," "Let's reconnect after the quarter," "Not the right time" |
| **Tool Objection** | Currently using a competing tool | "We use [Selenium / Playwright / Katalon / TOSCA / mabl]," "We already have a tool for this" |
| **Curiosity / Tell Me More** | Engagement but not commitment — asking a specific question or requesting detail | "How does the self-healing work?", "What does the pricing look like?", "Have you worked with [industry] companies?" |
| **Referral / Wrong Person** | Forwarding to someone else or redirecting | "You should talk to [Name]," "I'm not the right person, try [Name/team]" |
| **Out-of-Office / Auto-Reply** | Automated response triggered by send | "I'm out of the office until [date]," bounce notification, vacation responder |
| **Bounce / Deliverability Failure** | Hard bounce (address invalid) or soft bounce (mailbox full/temp error) | Mailer-Daemon notice, delivery failure notification |

---

### 13.2 Positive / Interested Replies

**Definition:** Any reply that indicates willingness to engage, learn more, or book a meeting. This includes enthusiastic replies ("Definitely interested!") and lukewarm acknowledgments ("OK, you can send me something").

**Target response time:** Same day, within 2 hours if possible.

#### Response Framework

**Step 1: Mirror their specific language.** Read the reply carefully. If they mentioned a specific pain or capability (e.g., "Yeah, regression testing has been painful"), your response should reference that specific thing — not a different feature or benefit. Mirroring signals you listened.

**Step 2: Offer two or three specific calendar options.** Do not say "let me know when you're free" — this puts the scheduling burden on them and creates friction. Offer 2-3 specific time slots in their likely time zone. Keep the time slots in the same week or early the following week. Do not offer more than 3 options.

**Step 3: One proof point maximum.** If the meeting ask is clear and clean, no proof point is needed. If the conversation needs one more hook to close to a meeting, add ONE proof point matched to what they said. Do not dump multiple proof points.

**Step 4: Keep it short.** The positive reply response should be 40-80 words maximum. The prospect has already said yes — don't talk them out of it with a wall of text.

#### Positive Reply Response Template

> Hi [First Name],
>
> Great to hear — [mirror their specific language or pain].
>
> [Optional: one proof point only if needed to reinforce the meeting.]
>
> I have [Day, Date] at [Time TZ] or [Day, Date] at [Time TZ] open — does either work? Happy to send a calendar invite.
>
> Rob

#### Annotated Example

**Their reply:** "Hey Rob, yes regression has been really painful lately. Open to a quick chat."

**Rob's response:**

> Hi Sarah,
>
> Regression pain is exactly where we tend to help the most.
>
> I have Thursday March 12 at 11 AM PT or Friday March 13 at 2 PM PT open — does either work? I'll send the invite once you confirm.
>
> Rob

**Why this works:**
- Mirrors "regression pain" specifically
- No proof point (not needed — she's already in)
- Two clear options, no open-ended "when are you free?"
- 50 words total

#### What NOT to Do

- **Do not say "Great!" or "Awesome!"** as the opener. These read as scripted and hollow.
- **Do not re-introduce Testsigma.** They know who you are. Starting with "As I mentioned, Testsigma is an AI-powered..." is a meeting-killer.
- **Do not say "I'd love to..." or "I'd be happy to..."** This is filler. Just offer the time.
- **Do not offer a "15-minute call."** This signals low value. Say "quick call" or just "call" without specifying time.
- **Do not dump the deck, case study PDF, or resource links.** This substitutes content for conversation. If they want the meeting, book the meeting first.
- **Do not wait to respond.** A positive reply that sits unanswered for 24+ hours loses 30-40% of its conversion potential. Schedule is not a reason to delay.

#### Apollo + Tracker Updates

After reply confirmed and meeting booked:
1. Update Apollo contact: Stage → "Replied / Demo Booked"
2. Update sequence status: Stop the contact in the Apollo sequence (no further automated tasks should fire)
3. Update `prospect_master_tracker.md` or batch tracker: Status → "Meeting Booked," log reply date, reply type = "Positive," reply trigger = [Opener / Pain Hook / Proof Point / Timing — whichever landed]
4. Generate Meeting Prep Card (see CLAUDE.md Meeting Booked Handoff section)

---

### 13.3 Negative / Not Interested Replies

**Definition:** An explicit decline, a disqualifier, or a flat "not interested." These are the most common replies and the most underused data source in the operation.

**Target response time:** Same day. A one-line professional close keeps the door open.

#### Response Framework

**Step 1: Thank them briefly.** One line. Not groveling, not defensive.

**Step 2: Leave the door open without begging.** End with one short sentence that plants a seed without asking for anything. This matters because "not now" and "not ever" are often the same reply — context you won't have.

**Step 3: Log the reason.** The reason for the decline is valuable data. Log it in the tracker with the specific objection type.

**Step 4: Set re-engagement criteria.** Most negative replies can become conversations in 60-90 days if a trigger event occurs. Log re-engagement criteria.

#### Negative Reply Response Template

> Hi [First Name],
>
> Totally understood — thanks for taking the time to reply.
>
> If anything changes on the testing side, feel free to reach back out. We'll be here.
>
> Rob

**Why this works:** It's short, professional, leaves zero pressure, and keeps the door open without begging for reconsideration. The phrase "feel free to reach back out" is active (they initiate) rather than passive ("I'll check back" = unwanted follow-up).

#### Variations Based on Decline Reason

**"Not a priority right now" (category: timing, not permanent):**

> Hi [First Name],
>
> Fair enough — timing matters. I'll leave it with you and circle back later in the year if it makes sense.
>
> Good luck with Q2.
>
> Rob

**"We have a tool for this" (category: tool objection — see Section 13.5 for full framework):**

> Hi [First Name],
>
> Appreciate the transparency. [One-line objection bridge.] Worth comparing at some point, but no pressure.
>
> Rob

**"I'm not the right person / wrong department" (category: referral — see Section 13.6):**

This is not a negative reply. It's a redirection. See Section 13.6.

**"We don't do software testing" or functional mismatch:**

> Hi [First Name],
>
> That makes sense — thanks for the context. I'll remove you from my list.
>
> Rob

Note: For functional mismatches (e.g., they do hardware QA, not software QA), mark in Apollo as "Disqualified — wrong function" and stop any further outreach immediately.

#### What NOT to Do

- **Do not argue.** "But have you considered..." is a conversion-negative move. Accept the no.
- **Do not ask "why?"** Asking the prospect to justify their decline adds friction and reads as pushy.
- **Do not send a follow-up email 2 days later.** If they've said no, the next contact window is the 60-day re-engagement window, and only if a trigger event occurs.
- **Do not mark them as "Do Not Contact" permanently unless:**
  - They used hostile language
  - They explicitly said "remove me from your list" or "don't contact me again"
  - They are outside your ICP permanently (wrong function, company dissolved, etc.)
- **Do not express disappointment.** "That's a shame" or "I really think we could help" are pressure tactics and will permanently close the door.

#### Apollo + Tracker Updates

1. Update Apollo contact: Stage → "Not Interested"
2. Stop contact in sequence immediately
3. Tracker: Status → "Not Interested," log reply date, log objection category
4. Set re-engagement reminder: +60 days, triggered only by qualifying trigger event (new QA job posting, leadership change, funding, product launch)
5. If explicitly asked to be removed: Status → "Do Not Contact," add to DNC list in CLAUDE.md

---

### 13.4 Timing Objection Replies

**Definition:** The prospect is not saying no — they're saying not now. There is implied interest but a current blocker (budget cycle, existing project, team bandwidth, etc.).

**Target response time:** Same day.

**Critically important distinction from negative replies:** A timing objection is an opening, not a close. Treat it accordingly — but do not push.

#### Response Framework

**Step 1: Validate the timing.** Acknowledge without arguing. Do not try to overcome the timing with urgency tactics.

**Step 2: Anchor a specific re-contact date.** If they say "Q3," say "Q3 works — I'll put a reminder for early July. Is [month] better for initial conversations?" This converts vague future interest into a specific calendar peg.

**Step 3: Leave one piece of value.** One proof point, one resource link maximum — something they can reference when the time comes. This keeps the conversation in their mind.

**Step 4: Create a calendar reminder.** Internal task for Rob only. Set a Google Calendar reminder at the specified date with the full context of this conversation.

#### Timing Objection Response Template

> Hi [First Name],
>
> That makes total sense — no pressure to force timing.
>
> I'll put a reminder on my end for [Month]. If early [Month] works better for a first conversation, let me know and I'll adjust.
>
> [Optional: one resource or proof point — e.g., "In the meantime, here's a quick overview of how [Customer] cut regression by [X] — might be useful context when you're ready."]
>
> Rob

#### Annotated Example

**Their reply:** "We're in the middle of a platform migration right now. Reach back out in Q3."

**Rob's response:**

> Hi Marcus,
>
> Completely understand — migration timing is the worst moment to add new tooling.
>
> I'll put a note for early July. If late June works better for a first conversation, let me know.
>
> One thing that might be relevant context when you're ready: Hansard cut their regression cycle from 8 weeks to 5 during a similar platform overhaul. Happy to share how if it's useful.
>
> Rob

**Why this works:**
- Validates their specific situation ("migration timing is the worst moment to add new tooling")
- Anchors July specifically
- Offers to adjust (June) — shows flexibility, not pressure
- Includes one context-appropriate proof point (Hansard during migration)
- Does not ask for anything

#### What NOT to Do

- **Do not try to overcome the timing.** "What if I could show you something in just 15 minutes before the migration?" reads as disrespectful of their stated constraint.
- **Do not say "I'll follow up."** Say "I'll put a reminder." Vague follow-up language creates anxiety, not goodwill.
- **Do not over-engineer the resource drop.** One link or one proof point maximum. Sending a deck, a case study PDF, and three links at once is overwhelming.

#### Apollo + Tracker Updates

1. Update Apollo contact: Stage → "Future Opportunity"
2. Stop contact in current sequence (no more Touch 3 if not yet sent)
3. Tracker: Status → "Timing — Dormant," log re-engage date, log their stated timing
4. Google Calendar: Create reminder on re-engage date titled "Re-engage: [Name] @ [Company] — said [Month] was right timing. Context: [one-line summary of their situation]"

---

### 13.5 Tool Objection Replies

**Definition:** The prospect already uses a competing or adjacent tool and is citing it as a reason not to meet.

**Target response time:** Same day.

**This is the second-most common positive signal in the entire reply data set.** When someone tells you what tool they use, they are engaged enough to respond AND to share context. The objection is an opening.

#### Response Framework

**Step 1: Acknowledge without dismissing.** Do not say "those tools have problems" or "that tool is inferior." This is defensive and puts the prospect in a position where they have to defend their tool choice.

**Step 2: Bridge to the specific gap.** Use the tool-specific objection response from CLAUDE.md Competitive Quick-Reference. Name one specific limitation without trash-talking the tool.

**Step 3: Ask a single question about gaps.** The goal is not to make the sale in the reply. The goal is to get them talking about what their current tool doesn't do well.

**Step 4: Re-ask for the meeting with a softer CTA.** After the gap question, offer a comparison specifically — not a generic demo.

#### Tool Objection Response Templates

**"We use Selenium":**

> Hi [First Name],
>
> Makes sense — a lot of teams we work with started on Selenium too.
>
> The gap we usually hear about is maintenance overhead once the UI starts changing. Are you running into that, or is your team keeping up with it OK?
>
> If not, worth a 20-minute compare. What day works?
>
> Rob

**"We use Playwright":**

> Hi [First Name],
>
> Totally fair — Playwright is solid for browser automation.
>
> The question we usually get is around Salesforce shadow DOM and no-code authoring for non-engineers. Is your team fully code-based, or do you have QA folks who aren't writing scripts?
>
> If there's a gap there, what day works for a quick look?
>
> Rob

**"We use TOSCA / Tricentis":**

> Hi [First Name],
>
> TOSCA is a solid choice for broad enterprise compliance testing.
>
> Teams typically come to us when they're feeling the friction on setup time and agile deployment cycles. Is that something you're running into, or is your team happy with the current velocity?
>
> If there's a gap, what day works for a side-by-side comparison?
>
> Rob

**"We already have a tool" (generic, tool not named):**

> Hi [First Name],
>
> That's a fair starting point. What are you running with?
>
> Most teams we talk to have a tool in place — the question is usually where it falls short when test suites scale or when the UI changes. Happy to compare if there's a gap.
>
> Rob

#### Key Objection Responses by Tool (Quick Reference)

| Tool | One-Line Bridge | Gap Question |
|------|----------------|-------------|
| Selenium | "Maintenance overhead is the usual pressure point once the UI starts changing" | "Are you seeing that at your team's scale?" |
| Playwright | "Playwright is strong for browser work, but Salesforce shadow DOM and no-code authoring are gaps" | "Does your team have QA folks who aren't writing scripts?" |
| Cypress | "Cypress is Chrome-only and doesn't cover mobile or API natively" | "Are you testing across multiple browsers and mobile?" |
| TOSCA/Tricentis | "TOSCA works for compliance-heavy enterprise; teams leave for agile speed and deployment friction" | "Is setup time and release velocity a pressure point?" |
| Katalon | "Katalon's self-healing doesn't generalize well to complex UI changes" | "How's your team handling flaky tests after UI updates?" |
| mabl | "mabl is lightweight ML healing; Testsigma adds plain-English authoring and cross-platform coverage" | "Is your team authoring tests in code, or do you have non-engineers involved?" |
| Provar | "Provar is Java-heavy and slow to adapt to DOM changes; setup vs. maintenance trade-off" | "How's your team finding setup time and CI/CD pipeline integration?" |
| Copado | "Copado handles deployments; Testsigma ensures what you're deploying actually works" | "Who owns test coverage validation in your DevOps pipeline?" |

#### What NOT to Do

- **Do not trash-talk their current tool.** "Selenium is outdated," "TOSCA is way too slow," or similar statements will cause them to defend their investment.
- **Do not assume they want to switch.** The question is whether there are gaps in their current setup. Ask first, pitch second.
- **Do not use "better" or "superior."** Comparison language should be about fit and specific capabilities, not a quality judgment.
- **Do not send a comparison PDF unsolicited.** Offer a meeting for the comparison. The document can follow the meeting.

#### Apollo + Tracker Updates

1. Update Apollo contact notes: log the tool they mentioned
2. Update tracker: Status → "Replied — Tool Objection," log tool name and any gap signals from their reply
3. If they agree to a comparison meeting: Stage → "Demo Booked," stop sequence, generate prep card noting their current tool

---

### 13.6 Referral / Wrong Person Replies

**Definition:** The prospect forwards to someone else, says they're not the decision-maker, or redirects to a specific name or role.

**Target response time:** Same day.

**This is the highest-value non-positive reply type.** A referral is a warm introduction via someone who opened your email. The referred person should receive outreach within the same day.

#### Response Framework: Two-Part Process

**Part 1: Reply to the referrer (thank + confirm)**

Keep this extremely short. Do not re-pitch. Just thank them and confirm the next step.

> Hi [Referrer Name],
>
> Really appreciate the redirect — I'll reach out to [Name] directly.
>
> Thanks for the intro.
>
> Rob

If they CC'd the referred person: Reply-all thanking both, then send a separate message to the referred person directly.

**Part 2: Reach out to the referred person**

This is a **warm outreach message** — not a cold sequence Touch 1. The referrer's name is your opening credential.

Research the referred person fully (LinkedIn, Apollo, company external research) before writing. Do not send a generic cold email. The referral gives you a warm opener but does not excuse a lazy message.

**Warm referral outreach structure:**

> Subject: [Referrer First Name] suggested I reach out

> Hi [Referred Name],
>
> [Referrer Name] from [their team] suggested I connect with you on the testing side of things.
>
> [One-line about what we do, matched to their role.]
>
> [One proof point matched to their vertical or likely pain.]
>
> [Referrer] thought it might be relevant to what your team is working on. What day works for a quick look?
>
> Rob

**Annotated Example:**

The referrer is David Chen (QA Manager, Binance). He replied: "Not really my area — you should talk to Jason Ruan, he owns engineering for this team."

**Reply to David:**

> Hi David,
>
> Thanks for the redirect — I'll reach out to Jason directly.
>
> Rob

**Outreach to Jason Ruan (Director of Engineering, Binance):**

> Subject: David Chen suggested I reach out

> Hi Jason,
>
> David Chen suggested I connect with you on test automation. He mentioned you own engineering for this team.
>
> We help engineering teams cut regression cycles and test maintenance — CRED automated 90% of their regression suite and sped up execution 5X.
>
> Thought it might be relevant given Binance's scale. What day works for a quick look?
>
> Rob

**Why this works:**
- Name-drops the referrer in the subject line (highest-open-rate subject in referral context)
- Does not over-explain the referral story
- Uses a proof point matched to FinTech scale
- Stays at 60 words

#### Special Case: "I'm CC'ing [Name]" or Group Reply

If the referrer CC'd the new person on their reply:
1. Reply-all with a short acknowledgment thanking the referrer
2. Address the referred person directly: "Hi [Referred Name] — thanks for the introduction, David. [One-sentence value prop.] I'll follow up with you directly to find a time."
3. Send a separate direct message shortly after to avoid the reply-all chain getting noisy

#### What NOT to Do

- **Do not immediately cold-pitch in the reply-all thread.** The referred person deserves their own message.
- **Do not skip research on the referred person.** The warm intro gives you access, not a pass on personalization.
- **Do not pitch both people at once.** Follow up with the referred person separately. The referrer is done.
- **Do not use the generic Touch 1 email for the referred person.** Write a fresh message using the referral as the opener. The HC1 ("I noticed/saw") rule still applies.

#### Apollo + Tracker Updates

1. Update original contact: Status → "Replied — Referral," log referred person's name and role
2. Research and create Apollo contact record for referred person
3. Add referred person to `prospect_master_tracker.md` with status "Warm Referral — Touch 1 Pending"
4. Do NOT enroll referred person in the Apollo sequence automatically — handle their outreach manually given the warm context

---

### 13.7 Curiosity / "Tell Me More" Replies

**Definition:** The prospect asks a specific question about the product, pricing, a case study, or how something works. This is genuine engagement — treat it as a warm signal even if they haven't said yes to a meeting.

**Target response time:** Same day.

**The risk:** Over-answering curiosity replies is one of the fastest ways to lose a warm prospect. The instinct is to send a full capabilities breakdown. The correct move is to answer directly, add one proof point, and immediately bridge back to a meeting.

#### Response Framework

**Step 1: Answer the question directly.** One to two sentences. No qualifications, no "great question," no preamble.

**Step 2: Add one proof point that reinforces the answer.** If they asked about self-healing, the proof point should demonstrate self-healing outcomes. If they asked about pricing, redirect to value first, then offer to discuss range on the call.

**Step 3: Bridge to the meeting.** Always. The goal of curiosity reply handling is to convert genuine interest into a scheduled conversation.

#### Response Templates by Question Type

**"How does the self-healing work?"**

> Hi [First Name],
>
> When the UI changes, the AI continuously tracks element attributes and auto-remaps the locators so tests keep passing without manual script fixes. No human intervention needed.
>
> Hansard cut their regression cycle from 8 weeks to 5 using exactly that — mostly because they stopped spending sprint time on broken locators.
>
> Happy to walk through it specifically for your stack. What day works?
>
> Rob

**"Do you have case studies from [their industry]?"**

> Hi [First Name],
>
> Yes — a few that are directly relevant to [their vertical]. [One specific customer name + one-line result, matched to their vertical.]
>
> I can walk you through the full detail on a call — there's usually a lot of context behind the numbers that doesn't fit in an email. What day works?
>
> Rob

**"What does pricing look like?"**

> Hi [First Name],
>
> Pricing is based on users and test volume, and it scales depending on the deployment model (cloud, private cloud, or on-prem). I don't quote ranges in email since the right model depends on your team's setup.
>
> Happy to put together a specific picture on a call. What day works?
>
> Rob

**"Have you worked with [type of company] / [tech stack]?"**

> Hi [First Name],
>
> Yes — [one sentence confirming with a specific customer if available]. [One-line result matched to their context.]
>
> The nuance usually comes out in a live conversation since every team's setup is different. What day works?
>
> Rob

#### What NOT to Do

- **Do not send a deck, PDF, or resources link in response to curiosity.** This substitutes content for conversation and creates a new decision point ("Do I read this?") that blocks the meeting.
- **Do not answer every possible angle of their question.** Answer what they asked, not what you wish they'd asked.
- **Do not say "Great question!"** No. Just answer it.
- **Do not forget the meeting bridge.** Answering the question and then closing with "Let me know if you have other questions" is a dead end. Every curiosity reply ends with "What day works?"
- **Do not quote pricing specifics in email.** Always bridge pricing questions to a call.

#### Apollo + Tracker Updates

1. Tracker: Status → "Replied — Curiosity," log specific question they asked
2. This is still an active thread — do NOT stop the sequence yet if Touch 3 hasn't been sent (use judgment: if they're clearly engaged, the Touch 3 may be unnecessary)
3. If meeting booked after curiosity reply: Stage → "Demo Booked," stop sequence, generate prep card with their specific question noted under "What triggered the reply"

---

### 13.8 Out-of-Office / Auto-Reply Handling

**Definition:** An automated response indicating the prospect is unavailable — either an OOO message, a vacation responder, or a generic auto-acknowledge.

**Target response time:** No response required. Follow the guidance below.

#### Response Framework

Out-of-office replies do not need a response. They need a decision: when to re-send or follow up based on the return date.

**Step 1: Read the OOO for return date.** If a return date is specified, calculate a follow-up window.

**Step 2: Set a calendar reminder for Day 1-2 after return.** Title it: "Resume outreach: [Name] @ [Company] — was OOO, [touch status]"

**Step 3: Decide whether to wait or proceed.** If Touch 1 was sent and they're OOO, do not proceed with Touch 2 until they're back. Touch 2 should land in their inbox when they're active, not while they're away.

| Situation | Action |
|-----------|--------|
| OOO received after Touch 1 | Wait until after their return date. Resume Touch 2 cadence starting from Day 1 of their return. |
| OOO received after Touch 2 | Wait until they're back. Send Touch 3 starting Day 1-2 after return. |
| Return date not specified | Default to 10-day wait. Then resume at the next touch in sequence. |
| OOO says "no longer at this company" or permanent redirect | This is a hard bounce (person left company). See Section 13.9. |

#### What NOT to Do

- **Do not reply to the OOO.** No one reads OOO replies and it looks like a bot.
- **Do not advance the sequence while they're out.** Touch 2 landing while they're on vacation gets buried.
- **Do not restart the sequence from Touch 1 after their return.** Pick up where you left off. If Touch 1 was sent, send Touch 2 when they're back — don't re-send Touch 1.

#### Apollo + Tracker Updates

1. Do not update Apollo status — this is a temporary hold, not a close
2. Tracker: add note "[OOO — returns approximately [date]. Resume Touch [N] starting [date].]"
3. Google Calendar: Create internal reminder for resume date

---

### 13.9 Bounce / Deliverability Failures

**Definition:** A hard bounce (email address invalid, domain non-existent, mailbox does not exist) or soft bounce (mailbox full, temporary server error).

**Target response time:** Immediate action to protect domain reputation.

#### Hard Bounce Protocol

A hard bounce means the email address is wrong or no longer exists. This is the most urgent deliverability issue because sending to hard-bounce addresses damages the sending domain's reputation.

**Step 1: Identify the bounce type.**
- "550 user unknown" or "User does not exist" = hard bounce
- "Mailbox full" or "temporarily unavailable" = soft bounce (see below)
- "Undeliverable" with a forwarding note = person may have left the company

**Step 2: Stop all further sends to this address immediately.**

**Step 3: Research the replacement.**
- Search LinkedIn for a current QA/Engineering contact at the same company
- Check Apollo for updated contact data (re-enrich the organization)
- If the original contact is still at the company but with a different email format, test the new format

**Step 4: Update Apollo contact record** — do not delete. Mark email as invalid. Add new email if found.

**Step 5: Update tracker.** Status → "Bounced," log bounce reason, log replacement if found.

**Bounced contact example from this sequence:** Kenny Liu, ModMed (confirmed hard bounce during Touch 1 send). Status in tracker: Bounced. Action: find replacement QA contact at ModMed.

#### Soft Bounce Protocol

A soft bounce (temporary failure) means try again in 48-72 hours. Apollo will typically retry automatically. If it fails three consecutive times, treat as a hard bounce and research replacement.

#### Domain Reputation Monitoring

If more than 2-3 hard bounces occur in a single send batch (greater than 3% bounce rate), pause further sends from that batch and audit the remaining email addresses before continuing. High bounce rates can cause Gmail / testsigma.com domain to be flagged as a spam sender.

#### What NOT to Do

- **Do not manually retry a hard bounce.** The address is invalid. Sending again does nothing but hurt your reputation.
- **Do not add a new email format and fire immediately.** Verify the new address first (Apollo enrichment or LinkedIn confirmation of current role) before sending.

---

### 13.10 Summary Table: Reply Type → Action

| Reply Type | Response Time | Response Required? | Apollo Update | Sequence Status |
|-----------|--------------|-------------------|---------------|-----------------|
| Positive / Interested | Same day, <2 hours | YES — offer calendar slots | Stage → "Demo Booked" | STOP sequence |
| Negative / Not Interested | Same day | YES — one-line close | Stage → "Not Interested" | STOP sequence |
| Timing Objection | Same day | YES — anchor date | Stage → "Future Opportunity" | STOP sequence |
| Tool Objection | Same day | YES — bridge to gap question | Add tool to notes | Continue if no reply |
| Curiosity / Tell Me More | Same day | YES — answer + bridge | Status → "Replied — Curiosity" | Use judgment |
| Referral / Wrong Person | Same day | YES (both parts) | Create new contact | STOP original; manual for referral |
| Out of Office | N/A | NO — set calendar reminder | Note OOO + return date | HOLD — resume post-return |
| Hard Bounce | Immediate | NO — research replacement | Mark email invalid | STOP — replace contact |
| Soft Bounce | 48-72 hours | NO — retry | Monitor | Hold and monitor |

---

### 13.11 Reply Tracking in Batch Tracker

Every reply (regardless of type) must be logged in the batch tracker within 24 hours of receipt. Required fields:

| Field | Options |
|-------|---------|
| `reply_date` | ISO date (YYYY-MM-DD) |
| `reply_type` | Positive / Negative / Timing / Tool / Curiosity / Referral / OOO / Bounce |
| `reply_trigger` | Opener / Pain Hook / Proof Point / Timing / Unknown |
| `reply_content_summary` | One-line summary of what they said |
| `next_action` | Meeting booked / Calendar reminder set / Referral outreach drafted / Replacement researched / None |
| `next_action_date` | Date of next action (if applicable) |

This data feeds the Batch Learning cycle — after 3+ batches, reply trigger data will show which proof points and angles are landing and which are getting ignored.

