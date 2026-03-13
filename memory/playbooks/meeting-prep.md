# Playbook: Meeting Prep

## When to Use
When a prospect has confirmed a meeting. Auto-generate this prep card as soon as the meeting is booked. Rob should have it before the call — same day if possible.

---

## Prep Card Format (one card per meeting)

```markdown
## Meeting Prep: {First Name} {Last Name} — {Company}
**Date/Time:** {Day, Month DD at HH:MM AM/PM TZ}
**Duration:** 25-30 min
**Platform:** Google Meet

---

### Prospect Snapshot
- **Title:** {title}
- **Tenure at company:** {N years / N months}
- **Background:** {1-2 sentences on their career path, relevant prior roles}
- **LinkedIn:** {URL}

---

### Company Snapshot
- **Company:** {name}
- **Size:** {employee count}
- **Vertical:** {industry}
- **HQ:** {city, state}
- **Tech stack (known):** {any QA tools, test frameworks, CI/CD from Apollo or job postings}

---

### Why They Replied
**Reply type:** {Positive / Curiosity / Referral / Timing}
**Reply text:** "{exact quote or close paraphrase}"
**Triggered by:** {which proof point or angle in the T1 email}

---

### Pain Hypothesis
Based on their role, company stage, and what triggered the reply:
{1-3 specific hypotheses about what QA pain they're experiencing. E.g.: "Team grew from 15→40 engineers in 18 months — test suite is probably scaling faster than they can maintain it."}

---

### Discovery Questions (3-5, tailored)
1. {Question — specific to their situation, not generic}
2. {Question — digs into the hypothesis above}
3. {Question — uncovers timeline/budget/decision process}
4. (Optional) {Question — understands the current tool landscape}
5. (Optional) {Question — who else is involved in the decision?}

---

### Best Proof Points for This Call (2-3, matched to vertical)
| Customer | Proof | Why Relevant |
|----------|-------|-------------|
| {Customer} | {stat} | {1-sentence match to their situation} |
| {Customer} | {stat} | {1-sentence match to their situation} |

---

### Predicted Objections + Responses
| Objection | Response |
|-----------|---------|
| "We already use {competitor}" | {1-2 sentence handle: acknowledge, bridge to gap/limitation} |
| "We don't have budget right now" | {1-2 sentence handle: explore timeline, ask what would need to change} |
| "We're happy with our current setup" | {1-2 sentence handle: curiosity question about coverage gaps, maintenance time} |

---

### What Rob Wants Out of This Call
- Confirm the pain hypothesis
- Understand the current testing setup (tools, team size, how tests are written and maintained)
- Identify timeline and decision process
- Warm close: "Does it make sense to get our technical team together to show you what this looks like for your specific stack?"
```

---

## How to Generate the Prep Card

### Step 1: Pull company + prospect data
Use Apollo enrichment for company data:
```
Tool: apollo_organizations_enrich
domain: {company domain}
```

Use Apollo people match for contact enrichment:
```
Tool: apollo_people_match
first_name: {first}
last_name: {last}
organization_name: {company}
domain: {domain}
```

### Step 2: Check the batch tracker for what was sent
- Open the relevant batch tracker HTML
- Find the contact's card
- Note: which proof point was used in T1, what the subject line was, what triggered the reply

### Step 3: Scan for tech stack signals
Sources to check:
- Apollo's `technology_names` on the company record
- LinkedIn job postings mentioning specific tools (Selenium, TestNG, Cypress, etc.)
- Company engineering blog if available (search "[company name] engineering blog")

### Step 4: Fill in the discovery questions
Tailor to the pain hypothesis. Generic questions like "What's your current testing process?" are a last resort. Specific questions like "You mentioned you're scaling the QA team — are most of your tests written manually or do you have some automation coverage?" show prep.

### Step 5: Present to Rob
- Paste the prep card in chat
- Note anything you couldn't find (unknown tech stack, unclear tenure, etc.)
- Offer to do additional research if time allows

---

## Key Sources for Prep Research

| What | Where |
|------|-------|
| Company size, funding, revenue | Apollo org enrichment |
| Current tech stack | Apollo technology_names field |
| QA tooling signals | LinkedIn job postings ("QA Engineer — must know Selenium/Cypress") |
| Recent company news | Apollo org record + news scan |
| Prospect background | LinkedIn profile (tenure, prior roles) |
| What triggered their reply | Batch tracker HTML (T1 email draft + which proof point) |

---

---
*Version: 1.0 — 2026-03-13*
*Change log: v1.0 (Mar 13, 2026) — new playbook created; fills gap identified in repo audit (sop-daily.md referenced prep card generation but no execution path existed)*
*When updating: increment version, add change log entry with date and what changed.*
