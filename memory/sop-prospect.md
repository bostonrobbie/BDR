# Prospecting SOP — Sales Nav Batch Build

---

## ⛔ AUTHORIZED PROSPECTING UNIVERSE — HARD RULE (Effective Mar 9, 2026)

ALL prospects MUST be sourced from Rob's two authorized account lists ONLY:

1. **Factor Accounts** (38 accounts) — `memory/target-accounts.md`
2. **TAM Accounts — Oct 2025** (312 accounts) — `/Work/tam-accounts-mar26.csv`

**This is an absolute restriction.** If a prospect's company is not on one of these two lists, DO NOT add them to any batch — regardless of how strong their buyer intent signal, title match, or vertical fit appears. No open Sales Navigator searches sourcing net-new companies outside these lists are authorized.

**How to verify:** Check `memory/target-accounts.md` for Factor accounts. Check `/Work/tam-accounts-mar26.csv` for TAM accounts. Every single prospect added to a batch must trace back to one of these two files. When building a batch, scope all Sales Nav searches to accounts within one of these two lists (use the Account filter in Sales Nav).

---

## Scope
This SOP covers the full prospecting workflow: finding prospects on LinkedIn Sales Navigator, qualifying them, enriching via Apollo, and building a batch tracker HTML file ready for Rob's review and APPROVE SEND.

This is Phase 1 of the end-to-end sequence. Everything after batch approval runs in `sop-outreach.md` (research + draft), `sop-send.md` (T1 send, T2 send, T3 send), and `sop-email.md` (T2 formula).

---

## Named Account Priority — The ONLY Authorized Sources

Rob's two assigned account lists are the ONLY authorized prospecting sources. There is no "open Sales Nav" prospecting. Every batch must trace every prospect back to one of these lists.

1. **Factor Accounts (HOT)** — 38 accounts (Rob's assigned accounts — Shakeel has departed as of Mar 9, 2026, all Factor accounts are Rob's). Highest priority. Check for unworked Director+ contacts before any other sourcing. Full enriched contact roster: `memory/target-accounts.md`.
2. **TAM Accounts (Oct 2025)** — Rob's primary named NAMER account universe (312 accounts). ICP-curated by LDR team with enriched contacts already in CRM. File: `/Work/tam-accounts-mar26.csv`.
3. **Manual Testers Footprint TAM** — Supplemental TAM for all BDRs, focused on companies with manual testers. Work in coordination with AEs Tyler + Eshwar. Must be verified against the TAM list.
4. **Farming Accounts** — ~10 active customers for upsell/cross-sell. NOT cold outreach. Coordinate with AE/CSM first. Separate motion.

**Rule:** If a company is not in Factor or TAM, it is not an authorized prospect target. Do not source from open Sales Nav searches. See the AUTHORIZED PROSPECTING UNIVERSE gate at the top of this SOP.

---

## When to Build a New Batch

Run the batch sourcing decision framework from `sop-daily.md`:
- Queue < 10 prospects awaiting T1 send, AND
- InMail credits > 10, AND
- No unsent batch trackers already exist, AND
- Not Monday or weekend

If any gate fails: defer to follow-up processing instead.

---

## Step 1: Pre-Batch Checks (MANDATORY — before touching Sales Nav)

### A. Read DNC List
Open `CLAUDE.md` → Do Not Contact List. Load all names into working memory for the session.

### B. Load MASTER_SENT_LIST.csv
Read `/Work/MASTER_SENT_LIST.csv`. Note the most recent entries so you can fuzzy-match against new prospects quickly.

### C. Run Pre-Brief
Read all batch trackers from the last 3-4 batches. Note:
- Best-performing persona (title)
- Best-performing vertical
- Best-performing proof point
- Any pattern to drop

This pre-brief informs which prospects to prioritize in the upcoming batch.

### D. Calculate Batch Size
```
MAX_BATCH = (CREDITS_REMAINING - FOLLOWUP_RESERVE - 5) / 1
```
Default batch size: 20-25 prospects. Never exceed 25 in one build session — quality degrades.

---

## Step 2: Sales Navigator Search

### Browser Setup
Use Rob's **blue/work Chrome browser** (Testsigma profile). Never use the red/personal browser.
Open LinkedIn Sales Navigator → Leads search.

### Search Filters (Standard Saved Search)

**Required filters:**
| Filter | Value |
|--------|-------|
| Geography | United States |
| Job Title (include) | QA Manager, QA Lead, Director of QA, Head of QA, VP of Quality, Director of Quality Assurance, VP of Engineering (only if Buyer Intent), Software Development Manager, Senior SDET, Automation Lead, Test Automation Lead |
| Seniority | Manager, Director, VP, CTO (VP/CTO only with buyer intent flag) |
| Current Company Headcount | 50-10,000 (avoid <50 = no QA budget; >10K = procurement too slow) |
| Industry | Computer Software, Internet, Information Technology and Services, Financial Services, Insurance, Hospital & Health Care, Retail |
| Languages | English |

**Recommended filters (when available):**
| Filter | Value |
|--------|-------|
| Buyer Intent | Use Tier 1 first (active intent signals) |
| Posted in last 30 days | Check if available — indicates active person |
| Changed jobs (last 90 days) | Trigger event — high priority |

**Key exclusion filters:**
| Filter | Exclude |
|--------|---------|
| Industry | Biotechnology, Pharmaceuticals, Medical Devices (unless software QA, not lab QA) |
| Job Title (exclude) | QA Analyst (too junior), Software QA Engineer (IC, not decision maker) |
| Geography (exclude) | India, Philippines, Eastern Europe (unless they manage US teams — confirm) |

### Two-Pass Search Strategy (Credit Optimization)

Run searches in two passes to maximize free Open Profile InMails before spending credits:

**Pass 1 — Open Profile prospects (free InMails):**
Add filter: "Premium LinkedIn member" (left panel). These prospects have a gold badge on their profile. Confirm for free in the composer (shows "Send for free" instead of "Use 1 of X credits"). Target: fill 10-20 Open Profile slots per batch. These don't count against credit budget.

**Pass 2 — All remaining prospects (credit InMails):**
Remove Premium filter. Pull the remaining credit InMail slots. Target: 8 per day, using credit budget as the governor.

Tag each prospect in the batch tracker as "Open Profile (free)" or "Credit InMail" so credit tracking stays accurate in pipeline-state.md.

### Using Saved Searches
Check for existing saved searches in Sales Nav. Click "Saved searches" in the left nav. Use "Show X new results since last checked" to pull only new prospects — do NOT re-pull the entire search.

---

## Step 3: Prospect Screening (Per-Profile Qualification)

For each profile in search results, run this 60-second screen before adding to the batch:

### Quick Screen (from search results page — no click-through yet)
| Check | Criteria | Action if fails |
|-------|----------|-----------------|
| Title | QA/Testing/Quality scope or SEM with testing ownership | Skip |
| Seniority | Manager or above (or Senior IC with org influence) | Skip |
| Company | Has software products to test (not pure services/consulting) | Skip |
| Location | US-based | Skip |
| Activity | Profile photo present, recent role date visible | Flag but include |

If passes quick screen: click through to full profile.

### Full Profile Screen (30-60 seconds)
| Check | Criteria | Notes |
|-------|----------|-------|
| QA scope | Their current role involves test automation, QA processes, or release quality | Required |
| Company ICP | SaaS, FinTech, Healthcare IT, Retail tech, Telecom software | Required |
| DNC check | NOT on DNC list, NOT already in MASTER_SENT_LIST | Auto-disqualify if found |
| Prior contact | Check for "Messaged" indicator on profile | Auto-disqualify if present |
| InMail available | "Message" button visible (not greyed out) | Required for T1 InMail |
| Degree | 2nd or 3rd degree (1st degree OK but will cost credit) | Note for credit budget |

### Persona Priority (higher = include first)
| Priority | Persona | Avg Reply Rate |
|----------|---------|---------------|
| P5 (Hot) | Sr. SDET / Automation Lead with buyer intent | 39.3% |
| P4 (Warm) | QA Manager / QA Lead | 26.8% |
| P4 (Warm) | Director/Head of QA | 26.0% |
| P3 (Standard) | Sr. Director / VP of QA (pure QA scope) | ~20% |
| P2 (Lower) | Software Eng Manager (QA in scope) | ~18% |
| P1 (Long shot) | VP Eng / CTO (only with buyer intent signal) | 9.1-11.9% |

Target mix per 25-prospect batch (from `sop-daily.md`):
- 10-12 QA Manager/Lead
- 4-6 Director/Head of QA
- 3-5 Architect/Sr SDET
- 2-3 Buyer Intent (any title)
- MAX 2 VP/CTO
- No more than 8 from same vertical

---

## Step 4: Data Collection (Per Accepted Prospect)

Capture these fields for every prospect you qualify:

| Field | Source | Notes |
|-------|--------|-------|
| Full name | Sales Nav profile | Exact as displayed |
| Title | Sales Nav profile | Current role title |
| Company | Sales Nav profile | Current company |
| Company size (employees) | Sales Nav profile | Approximate range |
| Industry | Sales Nav / company page | Use ICP vertical labels |
| Sales Nav URL | Browser URL bar | Copy while on profile |
| LinkedIn URL | Profile "LinkedIn" button | Format: linkedin.com/in/... |
| Location | Sales Nav profile | City, State |
| Connection degree | Sales Nav profile | 1st/2nd/3rd |
| Buyer intent signal | Sales Nav intent tab | Yes/No + signal type if yes |
| Priority score | Scoring rubric | 1-5 (calculate manually) |
| Vertical | Assigned by you | SaaS/FinTech/Healthcare/etc |

---

## Step 5: Apollo Enrichment (MCP)

After collecting all profiles, run Apollo enrichment for each prospect using MCP tools.

### Standard Enrichment Call
```
apollo_people_match(
  first_name="[First]",
  last_name="[Last]",
  organization_name="[Company]",
  domain="[company.com]"
)
```

### Extract from Apollo Response
| Field | Use |
|-------|-----|
| email | T2 email address (PRIMARY) |
| email_status | Must be "verified" or "likely to engage". Do NOT use "unavailable" |
| technologies | Feeds proof point selection (Selenium/Playwright/Cypress = maintenance angle) |
| organization.industry | Cross-checks vertical assignment |
| organization.estimated_num_employees | Refines company size |
| linkedin_url | Cross-check against Sales Nav URL |

### No Apollo Match Handling
If `apollo_people_match` returns null or no email:
1. Try search by email domain: `apollo_mixed_people_api_search(q_keywords="[Name]", q_organization_domains_list=["company.com"])`
2. If still no match: flag as "⚠️ NO APOLLO MATCH" in tracker. Include if LinkedIn research supports ICP fit. Cap MQS at 9/12. Email must be verified before T2 can be sent.
3. NEVER guess or construct an email address.

### Create Contact in Apollo (if not already there)
If the prospect isn't in Apollo yet:
```
apollo_contacts_create(
  first_name="[First]",
  last_name="[Last]",
  title="[Title]",
  organization_name="[Company]",
  email="[email from enrichment]"
)
```
Note the returned `id` — this is the Apollo contact ID used for sequence enrollment and T2 send navigation.

---

## Step 6: Pre-Batch Dedup (MANDATORY)

### A. DNC Cross-Reference (again — final check)
One final pass against CLAUDE.md DNC list. Zero tolerance.

### B. MASTER_SENT_LIST Cross-Reference
For every prospect in the batch, fuzzy-match against MASTER_SENT_LIST.csv:
- Strip parentheticals, middle names, credentials
- Normalize: lowercase, remove punctuation
- Any fuzzy match = FLAG. Do not include unless Rob explicitly approves.

### C. Same-Company Check
Scan batch for 2+ people at the same company.
Use the tiebreaker hierarchy from `sop-outreach.md` → Same-Company Conflict Resolution:
1. Higher priority score wins
2. Same score: QA manager/lead beats SDET
3. Still tied: confirmed Apollo email wins
4. Deferred contacts: document in batch tracker Deferred section

### D. Within-Batch Dedup
Check for the same person appearing twice (different name formats, LinkedIn vs. Sales Nav URL discrepancy). Remove the duplicate.

---

## Step 7: Research (3 Sources Per Prospect)

Per `sop-outreach.md` Research Requirements:

**Source 1 — LinkedIn Profile (from Sales Nav):**
Extract: QA scope, team signals, tech stack clues, activity/posts (pain signals).
Do NOT use: years at company, education, certifications, endorsement counts.

**Source 2 — Apollo Enrichment (already done in Step 5):**
Use: tech stack, company size, industry vertical, confirmed email.

**Source 3 — Company External Research (web search):**
Target: product pages, engineering blog, job postings (especially QA/SDET roles), press releases, news, Glassdoor.
Extract: Release frequency, testing stack evidence, recent migrations, QA hiring growth, integration complexity, platform scope.

Tag each research bullet with the message element it feeds: `[OPENER]`, `[CONTEXT]`, `[PROOF POINT]`, `[CLOSE]`.

---

## Step 8: T1 InMail Draft (C2 Style)

Per `sop-outreach.md` Message Structure. Quick rules:

- Start with a **QA situation question** (NOT a company fact). Company facts are for T2 openers.
- 80-99 words (39.0% reply rate sweet spot). Absolute ceiling 120.
- Exactly 2 question marks.
- Close: "what day works" pattern tied to proof point outcome.
- Subject: 3-6 words, domain or QA situation reference (e.g., "Test coverage at Kaseya")
- No em dashes. No "I noticed." No "I saw." No "following up."
- Run MQS (Message Quality Score) — must be ≥ 9/12 to include in batch.

**Proof point selection — do NOT repeat T1 proof point in T2:**
| Vertical | Best T1 Proof Point |
|----------|-------------------|
| FinTech/Payments | CRED (90% coverage, 5x faster) |
| Healthcare IT | Sanofi (3 days → 80 min test creation) |
| Insurance/Compliance | Hansard (8 weeks → 5 weeks regression) |
| Enterprise SaaS (M&A) | Medibuddy (50% test maintenance reduction) |
| Large Enterprise Platform | Cisco (35% regression reduction) |

**T2 proof point must differ from T1.** Log which proof point was used in T1 so T2 can use a different one.

---

## Step 9: Build Batch HTML Tracker

Output file format: `outreach-batchN-draft-MMMDD.html`

Required fields per prospect card:
- Name, Title, Company, Company Size, Industry
- Sales Nav URL, LinkedIn URL
- Apollo Contact ID
- Email (from Apollo enrichment)
- Priority Score (1-5)
- T1 Subject + Message Body
- T2 Subject + Message Body (draft — Variant A formula, `sop-email.md`)
- T3 Connection Note (draft — per `sop-outreach.md` T3 templates)
- MQS score (T1)
- Proof Point T1 (logged so T2 uses different story)
- Research notes (tagged by message element)
- A/B group assignment
- Status field (Draft / Awaiting Approval / Approved / Sent)
- Predicted objection + response
- Next step due date (T2 = Day 5, T3 = Day 10)

**Important:** Build T2 and T3 drafts at the same time as T1 — all three touches go into the HTML together. This prevents the "orphaned T1" problem where T1 is sent but T2/T3 drafts were never built.

---

## Step 10: Apollo Enrollment

Enroll prospects AFTER Rob approves the batch tracker (not before).

**Enrollment step-by-step (MCP):**

1. Batch prospects into groups of 5 (larger batches cause 500 errors in Apollo)

2. For each group of 5, call:
```
apollo_emailer_campaigns_add_contact_ids(
  id="69a05801fdd140001d3fc014",               # LinkedIn Outbound - Q1 Priority Accounts
  emailer_campaign_id="69a05801fdd140001d3fc014",
  contact_ids=["id1", "id2", "id3", "id4", "id5"],
  send_email_from_email_account_id="68f65bdf998c4c0015f3446a",  # robert.gorham@testsigma.net (enrollment default — OK for enrollment, NOT for T2 sends)
  sequence_no_email=True,
  sequence_active_in_other_campaigns=True,
  sequence_finished_in_other_campaigns=True,   # include if any finished prior sequences
  sequence_job_change=True                     # include if any recent job changes
)
```

3. Confirm each contact shows as "Active" in the LinkedIn Outbound - Q1 Priority Accounts sequence.

4. Log enrollment date in the batch tracker and pipeline-state.md.

**Note on the enrollment email account ID:** The `send_email_from_email_account_id` in the enrollment call uses the `.net` account (the Apollo default). This is for enrollment tracking only. All ACTUAL T2 email sends are executed manually via the Apollo UI using the `.com` account. See `sop-send.md` → Apollo UI Manual Email Send for the T2 send flow.

---

## Step 11: Rob Review & Batch Approval

Present the batch HTML to Rob with:
- Prospect count (confirmed sends vs. deferred/flagged)
- DNC / dedup results (any removals)
- Same-company flags (any conflicts resolved)
- Credit budget impact
- Any Apollo no-match flags
- A/B group breakdown

Rob reviews and gives **APPROVE SEND** (full batch) or **EDIT** (specific prospects).

Do NOT send any InMail until Rob gives APPROVE SEND. Do NOT send any T2 email until Rob gives APPROVE SEND for that specific touch.

---

## Step 12: Update MASTER_SENT_LIST.csv After Sends

After T1 sends are complete, re-run `build_master_list.py` to update MASTER_SENT_LIST.csv.
```bash
python /sessions/[session-id]/build_master_list.py
```
This MUST happen before the session ends. Do not defer.

---

## End-to-End Sequence Timeline (per prospect)

| Day | Touch | Channel | Action |
|-----|-------|---------|--------|
| Day 1 | T1 | LinkedIn InMail | Send approved InMail (1 credit for 2nd/3rd degree) |
| Day 5 | T2 | Email | Send Variant A email via Apollo UI (robert.gorham@testsigma.com) |
| Day 10 | T3 | LinkedIn | Send connection request (200-250 chars, warm/human tone) |

If T1 sends on a Friday, T2 is Day 5 = Wednesday. T3 is Day 10 = the following Monday.

---

## File Naming Convention

| Stage | Filename Pattern |
|-------|-----------------|
| Draft (pre-approval) | `outreach-batchN-draft-MMMDD.html` |
| Sent (post T1) | `outreach-batchN-sent-MMMDD.html` |
| T2 drafts file | `t2-email-drafts-MMMDD.html` (separate file) |

---

## Reference Map

| Task | SOP to read |
|------|------------|
| Research requirements (per prospect) | `sop-outreach.md` → Research Requirements |
| T1 InMail draft formula | `sop-outreach.md` → Message Structure (C2 Style) |
| T1 InMail Sales Nav live send | `sop-send.md` → 10-Step Procedure |
| T2 email draft formula | `sop-email.md` → Locked Formula Variant A |
| T2 email Apollo UI send | `sop-send.md` → Apollo UI Manual Email Send |
| T3 connection request send | `sop-send.md` → T3 LinkedIn Connection Request Send |
| Apollo enrollment | This file → Step 10, and `apollo-config.md` → Enrollment Rules |
| Daily workflow + batch sourcing | `sop-daily.md` |
| Proof points, objections | `memory/proof-points.md` |
| Priority scoring | `scoring-feedback.md` |
