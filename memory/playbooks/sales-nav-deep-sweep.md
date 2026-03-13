# Playbook: Sales Navigator Deep Sweep

## When to Use
When Apollo's people search doesn't return enough QA contacts at a target account and you need to go deeper using LinkedIn Sales Navigator browser automation.

---

## Why Sales Nav Over Apollo

Apollo's people search is limited to its database. Sales Nav has LinkedIn's full network, which means:
- More contacts (especially at large enterprises where Apollo coverage is spotty)
- More current titles (LinkedIn profiles update faster than Apollo enrichment)
- Access to people who haven't been scraped into Apollo yet

The tradeoff: Sales Nav requires browser automation (slower) and doesn't give you emails directly (you need Apollo enrichment afterward).

---

## Process

### Step 1: Open Sales Navigator
Navigate to LinkedIn Sales Navigator (blue/work Chrome profile). URL: `https://www.linkedin.com/sales/`

### Step 2: Set Up Lead Search
1. Click "Lead filters" or "Advanced search"
2. Set filters:
   - **Current company:** Target company name (e.g., "Epicor")
   - **Title keywords:** `QA OR "Quality Assurance" OR "Quality Engineering" OR "Test" OR "SDET" OR "Automation"`
   - **Seniority level:** Manager, Director, VP, CXO
   - **Geography:** United States, Canada (per territory expansion)
3. Apply filters

### Step 3: Scan Results
For each result:
1. Note: Full name, title, location, headline
2. Check if they match our target personas (from CLAUDE.md):
   - QA Manager / QA Lead (Primary)
   - Director/VP of QA (Primary)
   - Software Eng Manager (Secondary)
   - VP Engineering / CTO (Secondary, only with buyer intent)
   - Senior SDET / Automation Lead (Influencer)
3. Skip anyone who is clearly not software QA (e.g., "QA Manager — Food Safety", "Quality Control — Manufacturing")

### Step 4: Collect Contact Info
For promising contacts:
1. Note their LinkedIn profile URL
2. Try to find their email via Apollo enrichment:
```
Tool: apollo_people_match
Parameters:
  first_name: "Jason"
  last_name: "Lieberman"
  organization_name: "Epicor"
  domain: "epicor.com"
```
3. If Apollo returns an email: great, add to batch
4. If Apollo doesn't return an email: add to the "backlog" section of the tracker (candidates for future Apollo Chrome extension import)

### Step 5: Verify Email Domain
For every email Apollo returns:
- Is the domain catchall? Check `email_domain_catchall` in the response.
- Is the email verified or extrapolated? Check `email_status` and `extrapolated_email_confidence`.
- Does the domain match the company? (Sometimes people have emails at parent companies or subsidiaries — e.g., `@cunamutual.com` for TruStage employees)

### Step 6: Run Full Dedup
Before adding any contact to the batch, run all 6 dedup checks (see `dedup-protocol.md`).

---

## Tips for Better Results

### Expand your title search
QA titles vary wildly across companies. Try these additional searches if your first pass is thin:
- "Software Test" (catches "Software Test Engineer", "Software Test Manager")
- "Release" OR "Build" (catches release engineering managers who own testing)
- "DevOps" with seniority=Director+ (some DevOps leaders own QA/testing)
- "Engineering Manager" with "test" in headline or summary

### Check subsidiary domains
Large companies often have multiple domains:
- Northern Trust: `northerntrust.com` AND `ntrs.com`
- TruStage: `trustage.com` AND `cunamutual.com`
- Fidelity: `fidelity.com` AND `fmr.com`
- Commvault: `commvault.com`

Search Apollo with all known domains for the company.

### Use LinkedIn profile details
Sales Nav profiles sometimes show:
- Team size managed (useful for gauging seniority)
- Previous companies (useful for finding trigger events)
- Endorsements/skills (confirms they're software QA, not ops QA)
- Posts about testing tools (signals they're actively thinking about the problem)

---

## Output Format

Add contacts to the batch tracker HTML in this format per card:
- Full name
- Title
- Company
- Email (verified/catchall/extrapolated)
- Location (city, state/country)
- LinkedIn URL
- Source: "Sales Nav Deep Sweep"
- Notes: any relevant profile details

Contacts without verified emails go in the "Backlog" section of the tracker.

---

## When to Use Chrome Extension Instead

If you find a Sales Nav profile and Apollo enrichment doesn't return an email:
1. Use the Apollo Chrome Extension on the LinkedIn profile page
2. This imports the contact into Apollo and attempts email enrichment
3. The contact will appear in Apollo contacts search afterward
4. This uses 1 Apollo enrichment credit per contact

Note: Claude cannot operate the Chrome extension directly. This is a manual step for Rob, or a future session task.

---

---
*Version: 1.0 — 2026-03-12*
*Change log: v1.0 (Mar 12, 2026) — consolidated from Sessions 18, 26 (Wave 3 + Wave 5 sourcing)*
*When updating: increment version, add change log entry with date and what changed.*
