# SOP: TAM Outbound — End-to-End Process
## Version 4.3 — Updated Mar 14, 2026 (T1 formula upgraded: HC1 opener retired, new 3-para non-assumptive structure locked. Reply-first CTA replaces "what day works" meeting ask in T1. Full spec in Part 6. Previous: v4.2 Mar 13 — Daily target corrected 50 → 50-100; INC-012 two-gate send protocol mandatory; T2 formula v4 locked Mar 12.)

This SOP governs all outreach to named TAM accounts. It is the authoritative guide for any Claude agent executing the TAM outbound process. Read this file in full before starting any TAM batch.

**Target:** 50-100 T1 sends per day (25 minimum on light days), enrolled in TAM Outbound sequence, at highest personalization quality.
**Method:** Rolling daily batches. Account-first research (one company pass covers all contacts at that company). Continuous pipeline — no wave gating.
**Sequence:** TAM Outbound - Rob Gorham (`69afff8dc8897c0019b78c7e`) — enrollment email: `robert.gorham@testsigma.com`

**Daily priority directive (Mar 13, 2026):** New T1 batch work is the #1 daily priority. Start every session by sourcing and sending new contacts. T2s are handled after T1 batch is complete. Apollo manages the follow-up cadence automatically — the T1 pipeline is what requires active daily effort.

---

## Overview

The TAM outbound process works accounts from a prioritized list, identifies the right contacts, researches them deeply, drafts tailored outreach, gets Rob's approval, enrolls in the Apollo TAM Outbound sequence, and follows up systematically until reply, meeting booked, or breakup.

**Scope:** All accounts in `tam-accounts-mar26.csv` (312 total) — enterprise only. No SMB or commercial.

**Apollo Sequence:** TAM Outbound - Rob Gorham (`69afff8dc8897c0019b78c7e`)
- 7 steps, **ALL MANUAL** — zero auto-send steps. Nothing ever goes out automatically.
- Step 1: Email T1 (Day 1) · Step 2: Email T2 (Day 5) · Step 3: LinkedIn connection request (Day 10) · Steps 4-6: Phone calls (Day 15/21/28) · Step 7: Breakup email (Day 35)
- Enrollment email: `robert.gorham@testsigma.com` (.com ONLY — never .net, .in, or .com.in)
- **Verify before every session:** Apollo → Sequences → TAM Outbound → Edit → confirm all 7 steps = Manual Task. If any step shows "Automated," stop and alert Rob.

**Key constraint:** NEVER send any message without Rob's "APPROVE SEND." Claude drafts. Rob approves. Rob sends (or Claude sends after explicit APPROVE SEND per specific message).

---

## Part 1: Rolling Pipeline Architecture

TAM outbound runs as a continuous daily pipeline. No wave gating. Batches go out every working day until the full TAM list is covered.

### Pipeline Tiers (priority order — all run concurrently)

| Tier | Type | Source | Count | Priority |
|------|------|---------|-------|----------|
| Tier A | Factor HOT accounts (intent signals) | `memory/target-accounts.md` | ~38 | Always first. Clear these before moving to Tier B/C. |
| Tier B | TAM ICP=HIGH accounts | `tam-accounts-mar26.csv` — `icp=HIGH` | ~130 | Primary daily volume source. Work in account priority order. |
| Tier C | TAM ICP=Medium accounts | `tam-accounts-mar26.csv` — `icp=Medium` | ~130+ | Start when Tier B backlog < 20 accounts remaining. |

**Wave 1** (current active batch) = Tier A Factor accounts. Already enrolled — see Part 14.
**Wave 2+** = Tier B/C TAM accounts from `tam-accounts-mar26.csv`. Start building immediately.

### Rolling Batch Rules
- **Daily goal: 50-100 T1 sends enrolled in TAM Outbound sequence (25 minimum on light days).** This is the target range, not a hard cap — aim for 50 as baseline, push to 100 on full sessions.
- Each day = one or more batch tracker files (e.g., `tamob-batch-20260310-1.html`). If a day's 50 contacts span many accounts, a single tracker file is fine. Split only if the file gets unwieldy (>60 rows).
- Tier A contacts always go in the current batch alongside Tier B/C — no separate queue.
- Do NOT hold Tier B accounts waiting for Tier A to finish. They run concurrently in the same daily batch.
- The Apollo task queue manages all follow-up for enrolled contacts. Claude only needs to draft new T1s daily and draft follow-up messages when Apollo tasks come due.

### What "50/day" means in practice
50 T1 sends = however many accounts it takes to get to 50 clean, researched contacts. That number varies:
- Standard-targeting accounts (1-2 contacts each) → need ~25-50 accounts
- Mixed batch (Standard + Medium) → typically 20-35 accounts
- Medium/High-heavy batch → could be 10-15 accounts with 3-6 contacts each

**Never target a number of accounts. Target 50 contacts.** Pull accounts until the contact count reaches 50.

| Component | Estimated time |
|-----------|---------------|
| Account sourcing + dedup (variable accounts until 50 contacts hit) | ~30 min |
| Account Research Blocks (variable × 8-12 min each) | ~90-180 min |
| Contact LinkedIn scans + angle assignment (50 × 5-8 min) | ~250-400 min |
| ALL research complete → T1 + T2 draft writing (50 × 4-5 min) | ~200-250 min |
| QA gate + batch summary | ~30 min |
| **Total per session** | **~10 hours (full batch)** |

**In practice:** Claude does research + drafting; Rob reviews and approves. Split across two sessions if needed — research session first, drafting session second. Never draft until all 50 contacts are fully researched and the research menu is complete for every company.

---

## Part 2: Account Selection

### Factor Accounts (Wave 1)
Source: `memory/target-accounts.md` — Factor accounts table

Priority order:
1. 🔥 Tier A Factor (Demo + Signup signals) — most recent signal date first
2. 🔥 Tier A Factor (G2 + Use-case signals)
3. Tier B Factor (web sessions only)
4. Tier A/B with ⚠️ "Check First" flag — only after Rob confirms prior outreach situation

Skip permanently: `⛔ SKIP` (ACCELQ = competitor), `🏛️ Gov — Skip`, `🗑️ Bad Data`

### Non-Factor TAM Accounts (Tier B/C — Daily Volume Source)
Source: `tam-accounts-mar26.csv` — read the full file, filter by:
- `icp` = HIGH (Tier B) or Medium (Tier C)
- `status` = ✅ Untouched (not already in sequence, not bounced, not DNC)
- Not government, competitor, or bad data
- Enterprise size (verify via Apollo org enrichment — target 500+ employees minimum)

**Order:** ICP=HIGH first, then Medium. Within each tier, sorted by employee count descending (larger companies first — higher TAM value per account). Within same employee band: alphabetical.

**Daily account selection target (to hit 50 contacts):**
- Pull 15-20 new accounts per daily batch
- Check `tam-coverage-tracker.csv` to see which are still Untouched
- Mark each account as "🔄 In Progress — [date]" in the tracker as soon as you start working it (prevents double-claiming across sessions)
- After T1 send: update to "📤 In Sequence — [date]"

### Account Validation Checklist
Before adding any account to a batch:
- [ ] Is the account in `tam-accounts-mar26.csv` or `memory/target-accounts.md`? If no: STOP
- [ ] Is status ✅ Untouched or 🎯 HOT Factor? If "Check First": pause and confirm with Rob
- [ ] Is it enterprise-sized (not SMB/commercial)?
- [ ] Is it in a viable software-testing vertical (not pharma lab QA, not government, not non-profit)?

---

## Part 3: Contact Identification

### Target Personas (in priority order)
1. QA Manager / QA Lead
2. Director of QA / Director of Quality Engineering
3. VP of QA / VP of Engineering (secondary — only solo if no QA-specific title found)
4. IT Director, Quality Engineering (exact ICP match)
5. Senior SDET / Automation Lead (influencer — secondary touch, not primary T1)
6. VP Engineering / CTO (buyer-intent accounts only)

### Enterprise Persona Rule — Company Size Changes the Target Level (Updated Mar 10)
- Mid-size enterprise (<2,000 employees): QA Manager / Director is primary target
- Large enterprise (2,000–20,000 employees): Director or above preferred
- Mega-enterprise (20,000+ employees — Google, YouTube, Fidelity, Chase, etc.): VP-level required. At this scale, Directors are often too many layers from budget authority. Go as high as the verified email will allow.
- Rule of thumb: bigger company = higher up the org chart for initial T1

### Finding Contacts

**Step 1 — Apollo People Search**
```
Search parameters:
- q_organization_domains_list: [company domain from tracker]
- person_titles: ["QA Manager", "QA Lead", "Director of QA", "Director of Quality", "VP Quality", "VP QA", "Quality Engineering Manager", "Test Engineering Manager"]
- person_seniorities: ["manager", "director", "vp"]
- contact_email_status: ["verified"] (preferred) — also include unverified if no verified found
- person_locations: ["United States"] (unless EMEA account confirmed)
```

**Step 2 — Sales Nav (if Apollo returns nothing or email unverified)**
- Use Rob's saved TAM list → search by company → filter by QA/Engineering titles
- Note: Sales Nav contact found = 1 InMail credit if 2nd/3rd degree
- Sales Nav is required for LinkedIn InMail sends regardless

**Contact Selection Rules:**
- **Get every decision-maker you can find.** The goal is maximum account coverage, not just one contact. Pull ALL QA/Engineering Director+ contacts with findable emails.
- No limit on simultaneous contacts per company. Enroll all decision-makers together.
- Each message must be personalized enough that if two colleagues compare notes, the emails read as distinct and role-specific — not mass-produced.
- Enroll in order: most senior first, but do NOT hold backups. If Fidelity has a VP and two Directors, all three go in the same batch.
- If two contacts have the same seniority: prefer QA-specific title over Engineering generic title.

### Contact Depth Rule — Targeting Formula

The number of decision-makers found at an account determines how personalized each message must be. More contacts available = higher risk of internal comparison = higher personalization required.

| Contacts Found | Personalization Level | What "Personalized" Means |
|----------------|----------------------|--------------------------|
| 1-2 at company | Standard | Enterprise formula (HC1 + SMYKM) is sufficient. Role + vertical + proof point. No need for hyper-specific detail. |
| 3-5 at company | Medium | Each email must reference their specific role scope (e.g., "mobile QA" vs "API testing" vs "platform regression"). Different proof points per person. |
| 6+ at company | High | Each email must be written as if sent only to that individual. Unique opener tied to their team/scope, unique proof point, unique angle. Treat each as a standalone campaign. |

**How to find contact count:** Run the Apollo search (see Part 3 steps above) and count verified + unverified results before drafting. Let the count determine how deep you go on research per person.

**Mega-enterprise note (Google, JPMorgan, Fidelity, EA, etc.):** At 10,000+ employees, you will often find 10-20+ QA/Eng contacts. Still enroll all decision-makers, but group them by subteam/platform if possible (e.g., YouTube Music vs. YouTube Studio vs. YouTube Infrastructure). Each subteam gets a distinct angle.

---

## Part 4: Dedup Protocol

Run before every batch, for every contact:

1. **MASTER_SENT_LIST.csv check:** Search by full name + company. If found: SKIP this contact permanently (prior outreach exists). Note in batch tracker.

2. **DNC check:** Cross-reference CLAUDE.md DNC list. If found: SKIP. Note as "DNC."

3. **Apollo contact search:** Search by name + company in Apollo contacts. Check `emailer_campaign_ids` — if not empty, they're in an active sequence. Check `last_activity_date`. If activity exists from Nov 2025 onward by another BDR: STOP and ask Rob. If prior activity is Rob's own: safe to re-enroll if >6 months since last touch.

4. **Gmail search:** Search for prior threads at their verified email. `from:their@email.com OR to:their@email.com`. If thread exists: classify as warm lead, handle per `memory/warm-leads.md`, do NOT cold-enroll.

5. **Sales Navigator inbox check:** Search their name in Sales Nav messages. If an existing thread exists: check if prior message was T1 InMail. If yes and unanswered within 14+ days: T2 email may be appropriate. If a reply exists: handle as warm lead.

6. **Apollo Stage + Sequence history check (MANDATORY — Added Mar 14, 2026):** Open the contact's Apollo profile. Check two things:
   - **Stage field:** If Stage = "Connected", "Meeting Booked", "Meeting Held", "Opportunity", "Customer", or any non-cold stage, STOP — do NOT enroll. These stages mean prior engagement or an active relationship exists. Ask Rob before taking any action.
   - **Sequences tab:** If the contact has ANY prior sequence (even [Archived Sequence] marked Finished), check with Rob before enrolling in a new cold sequence. A finished sequence means they were previously touched — Rob may have spoken with them.
   - **Activities tab:** Scan for any logged meetings, calls, or demos. If any exists: treat as warm lead, SKIP cold enrollment, alert Rob.

   **Lesson learned (Mar 14, 2026 — Bret Wiener, Farmers Insurance):** Contact was enrolled in Batch 9 TAM Outbound despite having a prior [Archived Sequence] Finished and Stage = "Connected." Rob had previously met with him. Email was caught before send — but only because Rob flagged it manually. Root cause: dedup check did not include Apollo Stage or sequence history review. Prevention: always run Step 6 above before enrollment.

If dedup clean on all 6 checks: proceed. If any flag: document in batch tracker notes, ask Rob before proceeding.

---

## Part 5: Research Protocol (SMYKM-Level) — At Scale

**Two-layer model:** Company research happens once per account and produces a full research menu. Contact research happens once per person and selects from that menu. Neither replaces the other. Both are required. The efficiency gain is that company-level work (Apollo enrichment, job scan, news scan) is not repeated for each individual at the same company — but each person still gets a thorough individual read.

---

### Layer 1: Account Research Block (8-12 min per company — done once, used for all contacts at that company)

The goal of this block is to produce enough raw material that each contact at the company can pull a distinct, non-overlapping angle. If you only find one trigger and one proof point, two people at the same company will end up with the same email. Build a menu.

**Step 1 — Apollo Org Enrichment**
Call `apollo_organizations_enrich` for the company domain. Log:
- Tech stack (`current_technologies`) — identify any testing tools (Selenium, Playwright, Cypress, TestNG, etc.), CI/CD tools (Jenkins, GitHub Actions, CircleCI), cloud platform (AWS, GCP, Azure)
- Employee count — confirms enterprise tier and sets the persona level rule (Part 3)
- Funding stage / revenue — context for proof point framing (growth stage vs. established)
- Industry classification — maps directly to proof point table (Part 15)

**Step 2 — Job Posting Scan (required — this is the #1 signal source)**
Search LinkedIn for open QA/SDET/Automation/Quality Engineering roles at the company. Log:
- How many open QA roles? (1-2 = growing, 3-5 = scaling hard, 6+ = major expansion)
- What level? (SDET = automation gap, QA Lead = building team infrastructure, QA Manager = headcount addition)
- What skills required? (Playwright? Selenium? Mobile testing? API testing? Specific frameworks?) — this tells you their current tooling and gaps
- What teams are hiring? (mobile, API, platform, frontend, etc.) — maps to specific contacts at that company

**Step 3 — Engineering / Tech Signal Scan (required where available)**
Check in this order, stop when you have a signal:
1. Company engineering blog (tech.company.com, company.substack.com, company.medium.com) — test infrastructure posts, CI/CD posts, release velocity discussions, test framework mentions
2. Recent news (last 6 months): product launches, acquisitions, platform migrations, public engineering posts
3. Glassdoor QA/SDET reviews: any specific complaints about flaky tests, slow pipelines, manual overhead
4. GitHub (if public): test framework presence, test file volume, CI config files

**Step 4 — Build the Research Menu (what you produce from the above)**
For each company, document this before moving to contact research:
```
Account: [Company]
Domain: [domain.com]
Industry: [vertical]
Employees: [count] — Persona tier: [Mid / Large / Mega]
Tech stack confirmed: [Selenium / Playwright / Jenkins / etc. — or "unknown"]
Funding/stage: [Series X / Public / Revenue range]

TRIGGERS (build at least 2-3 different ones):
  Trigger A: [e.g., "4 open QA Automation Engineer roles — mobile + API level" → scaling pain]
  Trigger B: [e.g., "Launched new iOS app Dec 2025 — new coverage surface"]
  Trigger C: [e.g., "Engineering blog post Feb 2026: 'Our CI pipeline takes 3+ hours'"]

ANGLES AVAILABLE (each contact pulls one):
  Angle 1: Test maintenance / self-healing (if Selenium-heavy tech stack)
  Angle 2: Test creation speed / scaling coverage (if hiring SDETs at scale)
  Angle 3: Regression cycle compression (if release velocity signal found)
  Angle 4: Coverage expansion for new platform/product (if product launch found)

PROOF POINTS AVAILABLE (assign one to each contact — no repeats per company):
  T1 options: [Hansard / CRED / MediBuddy / Fortune 100 / Cisco / Nagra DTV]
  T2 rotations: [Per Part 15 table]

Notes: [Compliance flag, ops vs. software QA concern, domain catchall, etc.]
```

**Minimum to proceed:** You must have at least 2 distinct triggers and 2 distinct angles before drafting any contact at this company. If you only have 1 trigger, do more research before moving on. Generic company context = generic emails = ignored.

---

### Layer 2: Contact Research (5-8 min per person — LinkedIn + Apollo contact record)

**This is separate from company research and still required for every individual.** The Account Research Block tells you what angles are available. Contact research tells you which angle fits this specific person.

**Source 1 — LinkedIn Profile (via Sales Nav, always required)**
Find and extract ALL of the following:
- **Role scope:** What do they own? (Mobile QA? API testing? Platform regression? Full-stack quality?) — this determines which company angle they get
- **Team signals:** Any "team of X" language, org chart hints in summary or job description
- **Recent posts or activity:** Have they posted about testing tools, CI challenges, a product launch, a role change? If yes: directly reference the topic (not the post) in the opener
- **Tech stack signals:** Framework names in skills section, mentions of tools in past roles
- **Tenure in role:** Under 6 months = actively building new processes = highest receptivity. 1-3 years = established but open to optimization. 3+ years = needs a strong reason to change.
- **Title parsing:** "QA Manager" at a 500-person company vs. a 50,000-person company = very different scope. Parse accordingly.

**Source 2 — Apollo Contact Record**
Check the contact in Apollo:
- `email_status` (verified vs. catchall vs. extrapolated)
- `job_change_date` if flagged — recent job change = building from scratch = very receptive
- Prior `emailer_campaign_ids` — if populated, flag for Rob before including
- `direct_dial` or `mobile_phone` — note for call steps later

**Contact Research Output (add to the contact row in the batch tracker):**
```
Contact note: [Role scope — e.g., "Owns mobile QA and API testing at Commvault"]
Tenure signal: [e.g., "8 months in role — likely still setting up automation stack"]
Tech signal: [e.g., "Selenium + TestNG in skills, no Playwright listed"]
Assigned trigger: [Trigger A / B / C from company menu]
Assigned angle: [Angle 1 / 2 / 3 / 4 from company menu]
Proof point T1: [Specific customer story]
Proof point T2: [Rotation from Part 15]
Email note: [✅ verified / ⚠️ catchall / ⚠️ extrapolated]
```

**Differentiation check (required for Medium and High targeting):**
Before finalizing the contact's angle, check against all other contacts at the same company. No two contacts should have:
- The same trigger used in their opener
- The same proof point in T1
- The same CTA phrasing
If there's overlap: go back to the company menu and pull a different angle for one of them.

---

### Research-to-Message Mapping
| Research Finding | Where It Goes |
|------------------|-------|
| LinkedIn: role scope ("owns mobile + API regression") | Challenge sentence — frame pain around their specific area |
| Apollo: tech stack (Selenium + Jenkins) | Challenge sentence — maintenance framing specific to their tools |
| Job posting: 4 open QA automation roles | Theme — scaling challenge, right timing |
| Company news: new product launch or platform migration | Theme — new coverage surface = natural timing |
| Engineering blog: CI pipeline pain | Proof point angle — tie proof point to their stated problem |
| Tenure: under 6 months in role | Opener — "building out your automation approach" framing |
| Recent LinkedIn post on testing tools | Opener — reference the topic (not the post) as shared context |

---

### Research Quality Gate (required before any contact moves to drafting)
- [ ] Account Research Block complete — at least 2 triggers and 2 angles documented
- [ ] LinkedIn profile read for this specific contact — role scope extracted
- [ ] Angle assigned (distinct from other contacts at the same company)
- [ ] Proof point assigned (distinct from other contacts at the same company)
- [ ] Email status reviewed case-by-case:
  - ✅ Verified → proceed
  - ⚠️ Catchall → evaluate account fit and contact strength; if strong fit, send and flag ⚠️ catchall in tracker; if uncertain, skip and note reason
  - ⚠️ Extrapolated → same case-by-case judgment; flag in tracker; on any hard bounce, remove and re-enrich
  - Tracker flag format: `Email note: [✅ verified / ⚠️ catchall — send / ⚠️ catchall — skip / ⚠️ extrapolated — send / ⚠️ extrapolated — skip]`
- [ ] MASTER_SENT_LIST.csv check passed (no prior send to this person)

If any check fails: fix it before drafting. Do not draft from title + company alone.

---

## Part 6: T1 — Email Only (Updated Mar 14)

**CONFIRMED: T1 is email only for TAM Outbound.** Old InMail T1 decision tree is deprecated.

Step 1 of the TAM Outbound sequence is always an email sent via Apollo (robert.gorham@testsigma.com). Old Wave 1 InMail drafts (wave1-prospecting-plan-mar9.html) are deprecated and deleted. Start fresh prospecting for all accounts.

### Enterprise Email T1 Formula (v2 — Locked Mar 14, 2026)

**⚠️ HC1 opener ("We have yet to be properly introduced...") is RETIRED as of Mar 14. Do not use it in T1 emails.**

Use this 3-paragraph structure for ALL TAM Outbound T1 sends:

---

**Subject:** "[Name]'s [role/pain angle] at [Company]"
- Specific to the person and pain, not a generic category
- Examples: "Cory's engineering scale at SailPoint", "Suresh's QA leadership at Farmers Insurance"
- NOT: "Quick question", "Regression eating your time", or any generic pain phrase

---

**Greeting:** Hi [First], (plain — no bold)

**Para 1 — Non-assumptive role observation + check-in question**
Opens with a non-assumptive observation about what their role/context "usually means" for QA/testing, tied to their specific company or vertical. Must end with a diagnostic check-in question that invites a reply and confirms whether the pain applies.
- Use "usually means" or "tends to" as the opener. Never assume — observe.
- The check-in question must be specific to the pain named, not generic ("Is that something your team is navigating?" is too weak — name the specific pain).
- ✅ "Running senior engineering across an identity governance platform usually means test suite brittleness finds its way into your release cycle before you have time to fix it. Is your team spending more sprint cycles chasing broken tests than building new coverage?"
- ❌ "I know how busy QA teams are. Is this a priority for you?" (generic, assumptive)

**Para 2 — Bridge + customer metric + outcome sentence**
Opens with a bridge phrase that EXPLICITLY NAMES the specific pain word/phrase used in Para 1 (not a generic "ran into the same bottleneck"). Names the customer, the metric, and what their team stopped doing.
- Bridge must echo the exact pain term from Para 1: "was dealing with the same brittleness problem", "was dealing with the same catch-up problem", "was dealing with the same maintenance drain"
- Structure: "[Customer] was dealing with the same [exact pain term from Para 1] and [outcome metric] on Testsigma, [efficiency note]. Their team stopped [specific behavior they had to stop doing]."
- ✅ "Cisco was dealing with the same brittleness problem and cut regression runtime by 35% on Testsigma, without adding engineers. Their team stopped manually patching broken locators every sprint."
- ❌ "Cisco ran into the same bottleneck and achieved great results." (generic bridge, no specific outcome)

**Para 3 — Stakes line + open-ended reply question**
A brief stakes sentence about what the pain costs at their company's scale. Ends with an open-ended question that invites a reply (NOT a meeting ask). The question must relate directly to the specific pain in this email.
- Stakes line pattern: "At [Company]'s scale, [specific consequence of the pain]." OR "[Vertical] [companies/platforms] can't afford [the pain]."
- Reply question: Open-ended, diagnostic, related to the pain. Ask what their situation actually looks like — not whether they want a meeting.
- ✅ "At SailPoint's scale, that drag compounds across every release. Is test brittleness something your team is actively trying to get ahead of?"
- ❌ "What day works for a quick call?" (DO NOT use — this is a meeting ask, not a reply question)
- ❌ "Would love to connect!" (too salesy)

---

**Hard Rules:**
- Word count: 75-99 words (body text only, not greeting/signature)
- Exactly 2 question marks in the full email (check-in question + reply question)
- "Testsigma" must appear at least once in the body
- No em dashes anywhere
- No ` - ` separators (use commas instead)
- No "following up", "circling back", "I noticed", "I saw"
- No meeting ask in T1. Reply-first CTA only.
- Paragraph breaks: use explicit blank lines between each para (renders as 3 distinct paragraphs)
- Named customer required (Cisco, CRED, Hansard, Medibuddy, Samsung, or Fortune 100 firm)

---

**Example:**
```
Subject: Cory's engineering scale at SailPoint

Hi Cory,

Running senior engineering across an identity governance platform usually means test suite brittleness finds its way into your release cycle before you have time to fix it. Is your team spending more sprint cycles chasing broken tests than building new coverage?

Cisco was dealing with the same brittleness problem and cut regression runtime by 35% on Testsigma, without adding engineers. Their team stopped manually patching broken locators every sprint.

At SailPoint's scale, that drag compounds across every release. Is test brittleness something your team is actively trying to get ahead of?

Cheers,
Rob Gorham
Business Development · Testsigma
robert.gorham@testsigma.com
```

**Proof point rotation (T1 — use each story once per batch per company):**
| Story | Metric | Best pain match |
|-------|--------|----------------|
| Cisco | 35% regression time cut | Brittleness, broken locators, false failures |
| CRED | 90% coverage, 5x faster | Coverage gaps, catch-up debt, scale |
| Hansard | 8 → 5 week regression | Cycle length, deadline pressure, shipping cadence |
| Medibuddy | 2,500 tests, 50% maintenance cut | Maintenance drain, sprint capacity |
| Samsung | Cross-platform consistent coverage | Multi-platform, device fragmentation, hardware-software |
| Fortune 100 firm | 3x coverage in 4 months | Portfolio coverage gap, QA constraint on velocity |

**Para 3 Engagement Question CTA — Angle Mapping (Updated Mar 16, 2026):**

Para 3 ends with a relevant diagnostic engagement question tied to the specific pain angle, NOT a meeting ask like "What day works for a quick look at how they got there?" The question invites the prospect to share their current situation.

| Proof Point | Pain Angle | Recommended CTA Question |
|-----------|-----------|-------------------------|
| Cisco | Brittleness / Broken Locators | "How often are false failures from broken locators showing up in your runs right now?" |
| CRED | Coverage Gaps / Scale | "How much of your critical regression scope does your current suite cover today?" |
| Hansard | Cycle Length / Regression Timeline | "What does your current regression-to-release timeline look like for major releases?" |
| Medibuddy | Test Maintenance / Sprint Capacity | "How much of your current sprint capacity is going to test maintenance versus building new coverage?" |
| Samsung | Multi-Platform Consistency | "How are you currently managing regression consistency across your different platforms?" |
| Fortune 100 | Portfolio Coverage Gap | "How much of your test coverage is still keeping up with your product velocity?" |

---

## Part 7: T2 Draft Rules (Deep-Dive Formula v4 — Updated Mar 12)

T2 sends on Day 5 from T1. Via Apollo TAM Outbound Step 2 (manual email task).

**Threading:** T2 should be sent as a reply to the T1 thread when possible. The T2 builds directly on T1 content, so having T1 visible in the thread adds context and improves open rates.

**Word count:** 140-190 words. This is intentionally longer than T1. The T2 goes deeper on pain, pitches the solution, and tells a customer story. Every word must earn its spot.

**Tone:** Casual, direct, plain language. No enterprise-speak. Write like a real person, not a template.

**BANNED phrases:**
- "Different lens from my last note" / "One more angle worth adding/sharing"
- "Following up" / "Circling back" / "Reaching back out"
- "Thought this was worth adding"
- Any bridge/opener that apologizes for taking up space

---

### T2 Structure (4 parts, every email follows this)

**Part 1 — "I imagine" + deeper pain speculation (~2-3 sentences)**
Build directly on the T1 angle but go one level deeper. T1 named the problem; T2 describes what that problem actually feels like day-to-day for THIS person in THIS role at THIS company. Use "I imagine" to show you've thought about their specific situation.
- Reference specific details from T1 (their tech stack, migration, team structure)
- Speculate on the downstream consequences they're living with
- Make it specific enough that they think "yeah, that's exactly right"

**Part 2 — Testsigma solution pitch (~2 sentences)**
NOT a generic pitch. Directly answer the specific pain from Part 1. Explain what Testsigma does that solves THEIR problem, in plain language. Connect the feature to the pain so the "why" is obvious.
- Plain English tests (no framework lock-in) — use when pain is framework migration or dual-stack maintenance
- AI self-healing (auto-fixes locators) — use when pain is maintenance overhead or test brittleness
- NLP test creation (write tests in English) — use when pain is test creation speed or coverage gaps
- Unified platform (web, mobile, API, desktop) — use when pain is toolchain fragmentation

**Part 3 — Customer story (~2 sentences)**
Name a specific Testsigma customer that maps to their situation. Explain WHY this customer is relevant (similar industry, similar challenge, similar scale), give the outcome, and add one insight about what changed for them beyond the headline metric.

**Part 4 — Tie-back CTA (~1-2 sentences)**
Connect T1 + T2 together. Reference "what I mentioned last time" or the T1 topic explicitly. Then ask for 15 minutes to walk through the customer story and see if it applies to their situation.

---

### CTA phrasing (15-minute meeting ask)
- "Would 15 minutes make sense to walk through how [Customer] made that shift and see if it applies?"
- "Would 15 minutes be worth it to see how [Customer] handled [their exact problem] and whether there's a fit?"
- "If [pain from Part 1] is real for your team, would 15 minutes make sense to walk through what [Customer] did?"

---

### Rules
- 140-190 words — substantially longer than T1, every part must be present
- Reply in same thread as T1 (when possible)
- Must reference T1 content explicitly (the pain, the tech stack, the trigger)
- "I imagine" opener to go deeper on pain — NOT a repeat of T1
- Testsigma pitch must be specific to their pain (not generic product overview)
- Customer story must explain WHY that customer is relevant to them
- CTA = 15 minutes, tied to customer story + their situation
- NEW proof point — do not repeat T1's customer story
- No em dashes
- Plain language throughout
- Sign-off: Rob Gorham / Testsigma

**Proof point rotation (T1 → T2):**
- T1: Hansard (regression 8→5 weeks) → T2: CRED (90% coverage, 5x faster) or MediBuddy (50% maintenance cut)
- T1: Fortune 100 / 3x productivity → T2: Cisco (35% regression reduction) or Hansard
- T1: Nagra DTV (2,500 tests, 4x faster) → T2: CRED or MediBuddy
- T1: CRED → T2: Hansard or MediBuddy
- T1: MediBuddy → T2: CRED or Cisco

---

### Reference Example (validated Mar 12)

**Rick Brandt — Director of QA, Cboe Global Markets**
T1 angle: Dual Selenium/Playwright migration, maintenance overhead peaking, hiring for Playwright on newer clearing systems
T1 proof point: Hansard (8→5 week regression)

**T2 (threaded reply, 168w):**

Rick,

I imagine running two frameworks at once at Cboe means your team is fighting two separate maintenance queues that never sync up. Locator breaks from the Selenium side don't line up with Playwright issues on the newer clearing systems, and your engineers are context-switching between both every sprint instead of building new coverage.

That's exactly the kind of problem Testsigma was built for. Tests are written in plain English instead of framework-specific code, so there's no Selenium vs. Playwright split to maintain. And AI self-healing handles locator changes automatically, which is what keeps both queues from piling up.

CRED, a financial platform dealing with a similar coverage-to-complexity ratio, hit 90% regression coverage 5x faster after switching to Testsigma. The big shift for them wasn't just speed, it was getting their team off the maintenance treadmill and back to building net-new tests.

Between the dual-stack pressure I mentioned last time and the coverage demands that come with Cboe's product breadth, I think there's a real parallel to what CRED was facing. Would 15 minutes make sense to walk through how they made that shift and see if it applies?

Rob Gorham
Testsigma

---

## Part 8: Breakup Email Rules (Step 7, Day 35)

Last touch. No hard pitch. Direct, human, low-pressure.

**Rules:**
- 40-60 words
- Acknowledge the silence without guilt-tripping
- One closing question: is this on their radar this quarter?
- Leave the door open: "If not the right time, happy to reconnect later — just let me know."
- Subject: "Still worth a look?" or "[Company] QA — one last note"
- No new proof points needed at this stage

**Example:**
```
Subject: Still worth a look?

Hi [Name],

I've sent a few notes over the past few weeks. If test maintenance isn't a priority right now, no worries at all.

If it is on your radar for this quarter, what day works to take a quick look at how [Customer] approached it?

Rob Gorham
Testsigma
```

---

## Part 9: Batch Tracker Creation

Before writing ANY draft, create the batch tracker HTML file. Tracker files hold draft content and serve as the audit trail. They are NOT the follow-up controller — Apollo is.

**Filename:** `tamob-batch-[YYYYMMDD]-[N].html` (e.g., `tamob-batch-20260311-1.html`)
- Increment N within the same day if you split a large batch (e.g., `-1.html` and `-2.html`)
- Old naming (`wave1-batch1-tracker-mar10.html`) is still valid for Wave 1 specifically

**Required fields per contact row:**
- Name, title, company, email (with ✅ verified / ⚠️ catchall / ⚠️ extrapolated / 🔴 unverified flag + send/skip decision)
- LinkedIn URL
- Targeting level (Standard / Medium / High per Part 3)
- Account trigger used (one phrase — what made this company timely)
- T1 subject line
- T1 body draft
- Status: `📝 Draft Ready` / `⏳ Awaiting APPROVE SEND` / `📤 T1 Sent [date]` / `✅ Enrolled` / `↩️ Replied` / `🔴 Bounced` / `⛔ DNC`
- T1 send date (fill after send)
- Proof point used (T1)
- MASTER_SENT_LIST entry pre-formatted (copy-paste ready)
- Flags: any dedup concerns, email status notes, ops QA concerns

Note: T2 drafts are NOT pre-built. Draft T2 when Apollo surfaces the task as due (TASK-017). Proof point T2 rotation is tracked per contact in TASK-017 draft files.

**Company grouping:** Group contacts by account within the tracker file. Color-code by account — makes it easy to verify that all contacts at one company have distinct angles.

**Large batches (50 contacts):** A 50-row tracker in a single HTML file is fine. Use collapsible sections per account if it helps readability. Do not split into multiple files unless you need to (i.e., context limit forces it).

**MASTER_SENT_LIST entry format:**
```
[Full Name], [email], [Company], [Title], Email, [Send Date], [tamob-batch-YYYYMMDD-N]
```

**Apollo task queue is the primary follow-up controller.** The batch tracker HTML is the audit trail and draft storage. After each T1 send, enroll the contact in TAM Outbound (Step 1 complete) and Apollo auto-generates all remaining tasks on the correct days. See Part 18 for full Apollo task control SOP.

---

## Part 10: Approval Flow

1. Create batch tracker HTML file
2. Post BATCH SUMMARY block in chat:
```
TAM WAVE [N] BATCH SUMMARY — [Date]
Accounts: [N] included, [N] deferred, [N] flagged
Contacts: [N] total across [N] accounts
DNC check: Clean / [N removed]
Dedup check: Clean / [N removed — names]
Email verification: [N] verified / [N] catchall (case-by-case flagged) / [N] extrapolated (case-by-case flagged)
Send method: Apollo UI direct — Step 1 email (robert.gorham@testsigma.com)

Ready for review: [link to HTML tracker file]
Reply APPROVE SEND to send all, or APPROVE SEND — [name] only, or EDIT [name] with changes.
```
3. Wait for Rob's "APPROVE SEND" (all or specific names)
4. Claude notes each name approved — never sends unapproved contacts
5. After each send (Rob executes or gives explicit authority): update MASTER_SENT_LIST.csv, update batch tracker status

---

## Part 11: Apollo Enrollment

### ⛔ Pre-Enrollment Domain Verification Gate (MANDATORY — Added Mar 12, 2026)
Before enrolling ANY contact, verify their company domain exists in the authorized account universe:
1. Extract the contact's email domain (e.g., `jsmith@acme.com` → `acme.com`)
2. Check domain against `/Work/tam-accounts-mar26.csv` (column 4: Website Domain)
3. Also check subsidiary/alternate domains: some TAM companies use different email domains than their primary (e.g., Fidelity = `fidelity.com` but employees use `fmr.com`, YouTube employees use `google.com`, OneMain uses `omf.com`). If the organization name clearly maps to a TAM account, it passes.
4. If the domain does NOT match any TAM or Factor account: **STOP. Do not enroll. Remove from batch.**
5. Log any removed contacts in the batch tracker with reason "NON-TAM COMPANY — removed before enrollment."

**Lesson learned (Mar 12, 2026):** Batch 5 contained 5 contacts from DocuSign and Bentley Systems, which are NOT in Rob's TAM list. Caught during pre-enrollment verification. All 5 excluded before any enrollment API call. Root cause: Apollo People Search returned contacts from non-TAM companies when searching by title/location without restricting to TAM organization IDs.

**Prevention:** When using Apollo People Search to find prospects, ALWAYS filter by `organization_ids` or `q_organization_domains_list` from the TAM/Factor account lists. Never use open title+location searches that could return contacts from any company.

**For contacts whose T1 was sent as InMail (outside the sequence):**
1. Run Pre-Enrollment Domain Verification Gate (above)
2. Add contact to Apollo (or confirm they exist as a contact)
3. Enroll in TAM Outbound - Rob Gorham (`69afff8dc8897c0019b78c7e`)
4. Email account: `robert.gorham@testsigma.com` (NOT .net or .in)
5. After enrollment: in Apollo, manually skip Step 1 (InMail was T1, already sent)
6. Step 2 manual email task will appear — due Day 5 from enrollment date

**For contacts whose T1 is email (all TAM Outbound T1s — standard protocol):**
0a. **Pre-enrollment domain verification:** Run the Domain Verification Gate above. Do not proceed if domain is not in TAM/Factor list.
0b. **Pre-enrollment email quality check:** Before enrolling, check if the Apollo contact record has custom field `678901dcd836ab01b09a6110 = "invalid"`. This is Apollo's internal email quality flag and reliably predicts hard bounces (see INC-009). If present: **do NOT enroll in email sequence.** Add note in batch tracker. Use LinkedIn InMail when credits are available instead.
1. Enroll in TAM Outbound - Rob Gorham (`69afff8dc8897c0019b78c7e`) via API
2. Email account: `robert.gorham@testsigma.com` (ID: `68e3b53ceaaf74001d36c206`)
3. Apollo flags: `sequence_no_email: true`, `sequence_active_in_other_campaigns: true`
4. After enrollment: open the Step 1 task in Apollo → send via Apollo UI (see Part 23)
5. Step 2 task will auto-generate, due ~24 hours after Step 1 is marked done (via Send Now)

**Enrollment timing:** Enroll and send in the same session. Do NOT enroll and leave the Step 1 task unsent.

**Batch size:** Enroll max 5 contacts at a time (larger batches cause 500 errors per prior testing).

---

## Part 12: Follow-up Loop (Daily)

Run each day per `memory/sop-daily.md`. TAM-specific additions:

1. Open Apollo → TAM Outbound sequence → check "Tasks Due Today"
2. For each task due: identify contact, confirm status (no reply yet), draft message per Step rules above
3. Present draft to Rob before sending (wait for APPROVE SEND)
4. After send: log date in batch tracker HTML
5. Check Gmail MCP for replies to `robert.gorham@testsigma.com` from any TAM contact
6. Classify reply (Positive / Timing / Negative / Curiosity) per reply SOP in `Tier1_Intent_Sequence_SOP_MASTER.md` Section 13
7. If positive or curious: immediately move to warm lead handling (`memory/warm-leads.md`)
8. Update `memory/pipeline-state.md` with any new meetings booked or sequences completed

---

## Part 13: Updating the Coverage Tracker

After each batch is complete:

1. Open `tam-coverage-tracker.csv`
2. For each account touched: update `status` from "✅ Untouched" → "📤 In Sequence" (or "✅ Done" if sequence complete)
3. Add notes field with contact name, send date, and sequence step
4. Do NOT delete any rows — append only
5. Save and commit with work-queue update

---

## Part 14: Wave 1 Current State (as of Mar 10, 2026)

**STATUS: Enrollment complete. T1 + T2 drafts pending.**

All 23 clean contacts enrolled in TAM Outbound - Rob Gorham (69afff8dc8897c0019b78c7e) via robert.gorham@testsigma.com. Full roster and enrollment statuses live in `memory/target-accounts.md`. Batch tracker: `wave1-batch1-tracker-mar10.html`.

| Account | Enrolled | HOLD | Notes |
|---------|----------|------|-------|
| Cboe Global Markets | 3 (Rick Brandt, Maurice Saunders, Snezhana Ruseva) | 0 | Standard targeting. Needs T1 drafts. |
| Fidelity Investments | 8 (Seth, Nithya, Chris P, Christopher B, Eric P, Richelle, Sourabh, Padma) | 0 | Medium targeting. 8 contacts = differentiate by role scope. Needs T1 drafts. |
| JPMorgan Chase | 1 (Neeraj Tati) | 3 (Rose — extrapolated email; Justin + Nikki — ops QA concern) | Rob to decide on HOLD contacts. |
| Commvault | 5 (Brahmaiah, Arun, Prasad, Sucheth + Jennifer D) | 0 | Medium targeting. Needs T1 drafts. |
| TruStage | 3 (Chamath, Maggie @cunamutual.com, Jennifer D @cunamutual.com) | 1 (Shawn Woods — below Director threshold) | Standard targeting. Needs T1 drafts. |
| YouTube / Google | 3 (John Harding, Des Keane, Hrishikesh Aradhye — both with job_change bypass) | 0 | High targeting — product-area specific per contact. Needs T1 drafts. |

**Next action:** TASK-014 Steps C+D — draft T1 + T2 for 23 enrolled contacts. Use wave1-batch1-tracker-mar10.html as the draft storage. Present batch summary → APPROVE SEND.

**Wave 2+:** Start building immediately. Do not wait for Wave 1 T1s to be sent first. Use Part 20 daily batch cadence starting with Tier B ICP=HIGH accounts from tam-coverage-tracker.csv.

---

## Part 15: Proof Point Reference for TAM Accounts

| Vertical | T1 Proof Point | T2 Rotation |
|----------|---------------|-------------|
| FinTech / Banking | Hansard: Regression 8→5 weeks (financial services, self-healing) | CRED: 90% regression coverage, 5x faster |
| Insurance | Hansard: Regression 8→5 weeks (compliance-heavy) | MediBuddy: 50% maintenance cut |
| Enterprise SaaS | Fortune 100: 3X productivity from QA team | Cisco: 35% regression reduction |
| Media / Streaming | Nagra DTV: 2,500 tests in 8 months, 4X faster execution | MediBuddy: 2,500 tests, 50% cut |
| Healthcare | MediBuddy: 50% test maintenance cut | Hansard (if financial/compliance angle) |
| Retail / E-comm | CRED: 90% coverage, 5X faster | Fortune 100 (if enterprise-scale) |
| Telecom | Nagra DTV: Multi-platform (web, mobile, API) | CRED |
| General Enterprise | Fortune 100: 3X productivity | Hansard or CRED depending on pain angle |

**Framing rules:**
- Always use REDUCTION framing: "cut regression from 8 to 5 weeks" NOT "3 weeks faster"
- Always use REDUCTION framing: "5X faster execution" is OK (it's a speed multiplier, not false inflation)
- CRED: "90% regression coverage" NOT "90% more coverage" (absolute vs. relative)
- Fortune 100: "3X productivity" NOT "300% improvement"

---

## Part 16: LinkedIn Connection Request (Step 3, Day 10)

Step 3 is MANUAL — Rob writes the note personally. Claude may draft a suggestion but Rob must customize.

**Rules:**
- 200-250 characters max
- Goal: get accepted, NOT to pitch
- Light callback to T1 topic is fine, but do NOT rehash the pitch
- Templates from sop-outreach.md apply

**Example for TAM accounts:**
- "Hi [Name], reached out about QA testing a couple weeks back. Either way, good to stay connected. Rob"
- "Hi [Name], [Company]'s [platform] work is interesting space — thought it made sense to connect. Rob"

Once accepted: 1st degree. Future DMs free. No more InMail credits needed.

---

## Part 17: Phone Calls (Steps 4-6, Days 15/21/28)

Fully manual. Claude does NOT assist with call execution.

Claude's role for calls:
- Note the call task due date in daily follow-up loop
- Alert Rob: "[Contact] at [Company] — TAM Outbound Step [4/5/6] call task due today"
- If Rob asks for a call prep brief: run `sales:call-prep` skill
- After call: update batch tracker with call outcome (VM / No answer / Connected / Follow-up)

---

---

## Part 18: Apollo Task Queue — Primary Follow-up Controller

**Apollo is the source of truth for what to do next.** Not the batch tracker HTML. Not the work-queue. Apollo.

When a T1 email is sent and the contact is enrolled in TAM Outbound (Step 1 complete), Apollo auto-schedules every subsequent task:
- Step 2 task auto-created for Day 5 (T2 email)
- Step 3 task auto-created for Day 10 (LinkedIn connection request)
- Steps 4-6 auto-created for Days 15/21/28 (calls)
- Step 7 auto-created for Day 35 (breakup email)

**How to use Apollo as the daily controller:**
1. Open Apollo → Sequences → TAM Outbound - Rob Gorham
2. Click "Tasks" tab → sorted by "Due Date" ascending
3. For each task: identify the contact, look up their T2 draft in the batch tracker HTML
4. Present draft to Rob → Rob gives APPROVE SEND
5. **Send via Apollo UI (Part 23) — manually paste content into task composer, then click "Send Now"**
6. Confirm send. Apollo automatically marks the task done and advances the contact to the next step.
7. After sending: update Status in batch tracker HTML → "T2 Sent [date]"

**What to do if Apollo shows 0 tasks:** Either no contacts are enrolled yet, or all active contacts are between steps. Check enrolled contacts list in sequence. This is normal on Day 2-4 (between T1 and T2).

**Apollo enrollment flags for TAM Outbound:**
```
sequence_no_email: true
sequence_active_in_other_campaigns: true
sequence_finished_in_other_campaigns: true (if contact was in a prior sequence)
```
Email account: `robert.gorham@testsigma.com` (.com ONLY — not .net, .in, or .com.in)
Batch enrollment: max 5 at a time to avoid 500 errors.

**Apollo auto-send behavior (observed Wave 4, Mar 11):** In rare cases, Apollo may automatically advance a contact to Step 2 immediately upon enrollment, sending Step 1 without generating a Task. This appears to happen when Apollo detects certain conditions (possibly CRM sync or prior contact history). Signs: contact shows `current_step_id` = Step 2 ID (not Step 1) shortly after enrollment, no Step 1 task ever appeared. When this happens: the T1 email WAS sent (check Gmail sent folder to confirm). Log as "auto-sent" in batch tracker, add to MASTER_SENT_LIST, and treat T2 due date from auto-send date.

**After each T1 send:**
1. Enroll in TAM Outbound immediately (same session, same day)
2. Mark Step 1 complete in Apollo
3. Update batch tracker HTML: Status → "T1 Sent [date]"
4. Add row to MASTER_SENT_LIST.csv: [Name, email, Company, Title, Email, Send Date, B_Wave1]
5. Do NOT wait to enroll — if you wait, the task calendar shifts and T2 will be late

**Credit note:** TAM Outbound enrollment uses zero InMail credits. All steps are manual email or phone. Credits are only spent on LinkedIn InMails sent OUTSIDE the sequence.

---

## Part 19: Session Recovery Protocol

Sessions break. When a new session starts mid-wave, this is the exact recovery sequence:

### Step 1 — Always run first (every session)
```
git pull origin main
Read: AGENTS.md
Read: memory/session/handoff.md
Read: memory/session/work-queue.md
```

### Step 2 — Check Apollo task queue
1. Use Apollo MCP: search contacts in TAM Outbound sequence
2. Check which steps are due today or overdue
3. Cross-reference batch tracker HTML (wave[N]-batch[N]-tracker-[date].html) for draft content
4. If task is due and draft exists → present to Rob for APPROVE SEND
5. If task is due and draft does NOT exist → draft it now, present, wait for approval

### Step 3 — Check for new replies
1. Search Gmail for replies from any TAM contact (search by company domain or from:email addresses in batch tracker)
2. Classify: Positive / Timing / Negative / Curiosity
3. If positive/curious: update warm-leads.md, hold sequence, handle per reply SOP

### Step 4 — Confirm where TASK-014 stands
Read work-queue.md TASK-014 status. The task has sub-steps. Check which accounts have:
- T1 drafted but not sent → re-present batch summary for APPROVE SEND
- T1 sent but not enrolled in Apollo → enroll immediately
- T2 task due in Apollo → draft and present
- No contact found yet → run Apollo search

### What NOT to do on session recovery
- Do NOT re-research contacts already in the batch tracker
- Do NOT re-draft T1s already marked "Draft Ready" in the batch tracker
- Do NOT enroll contacts a second time (check Apollo first — search by name + company)
- Do NOT re-send emails already sent (check MASTER_SENT_LIST.csv first)

### State is stored in 4 places (in priority order)
1. **Apollo task queue** — what's due today. Check this first.
2. **Batch tracker HTML** (wave[N]-batch[N]-tracker-[date].html) — contact details, draft status, email content
3. **memory/session/handoff.md** — high-level state snapshot from last session
4. **MASTER_SENT_LIST.csv** — what has already been sent (dedup check)

When in doubt: Apollo + batch tracker HTML will tell you everything you need to continue.

---

---

## Part 20: Daily Batch Cadence — 50-100/Day Target

This is the repeating daily workflow. **Critical rule: complete ALL research for all contacts before writing a single draft.** Do not draft as you go. Research the full batch first, then draft everything.

### Phase 1: Account Sourcing — Pull Until You Have 50-100 Contacts (30 min)

**Goal:** Source enough accounts to produce 50-100 clean contacts for today's batch (25 minimum on light days).

1. Open `tam-coverage-tracker.csv`
2. Filter: `icp = HIGH`, `status = ✅ Untouched` — sort by employee count descending
3. Pull the first account in that list. Run a quick Apollo people search to count QA/Engineering Director+ contacts:
   - 1-2 contacts found → Standard targeting. Add to batch.
   - 3-6 contacts found → Medium targeting. Add all (cap at 6 per company per batch).
   - 7+ contacts found → High targeting. Take only top 5-6 by seniority. Defer the rest to a future batch.
4. Mark that account in `tam-coverage-tracker.csv` as "🔄 In Progress — [date]" immediately (prevents double-claim if session breaks)
5. Keep a running count. Pull the next account, repeat steps 3-4.
6. **Stop when your running count hits 50.** If the last account would push you to 52-55, defer the lower-seniority contacts from that account to tomorrow's batch.

**The count is the target, not the number of accounts.** Some days you'll need 10 accounts (all Medium/High). Some days you'll need 45 accounts (all Standard 1-contact).

**Checkpoint:** Exactly ~50 contacts listed across however many accounts it took. Every account marked 🔄 In Progress in the tracker.

### Phase 2: Dedup (20 min — parallel with Phase 1)

For every contact identified in Phase 1:
1. MASTER_SENT_LIST.csv check (name + company)
2. DNC list check (CLAUDE.md)
3. Apollo contact search — check `emailer_campaign_ids` and `last_activity_date`
4. Remove any flagged contacts from the batch. Replace from the same account's bench if available. If no bench, pull a new account.

**Dedup result:** Clean list of ~50 contacts, zero duplicates.

### Phase 3: Account Research Blocks — ALL Companies Before Any Drafting (8-12 min per company)

**Do not start drafting until every account in the batch has a complete research menu.** Research all companies first, then move to contact research, then draft.

For each account:
1. Run `apollo_organizations_enrich` for the domain → log tech stack, employee count, vertical, funding
2. LinkedIn job posting scan → count open QA/SDET roles, note levels and skills required
3. Engineering blog / news scan → find 1-2 additional signals
4. Build the Research Menu (Part 5 Layer 1 format): document at least 2 triggers and 2 angles
5. Pre-assign proof point options (T1 and T2) from Part 15 table — list options, don't assign to specific contacts yet

Create the batch tracker HTML file now. Add all 50 contact rows with company sections. Research menu for each company goes in the account header row — shared by all contacts at that company.

**Checkpoint:** Tracker file exists. All accounts have a complete research menu (min 2 triggers, 2 angles, proof point options). No contact research yet. No drafts yet.

### Phase 4: Contact Research — ALL Contacts Before Any Drafting (5-8 min per person)

Now research each contact individually. For each person in the tracker:
1. Pull their LinkedIn profile via Sales Nav — extract: role scope, tenure, tech signals, recent posts
2. Check their Apollo contact record — verify email status, check prior emailer_campaign_ids
3. Pull one angle from the company's research menu that fits their specific role scope
4. Assign proof point T1 and T2 from the company options — confirm no two contacts at the same company share the same proof point
5. Document in their tracker row: role scope note, assigned trigger, assigned angle, assigned proof points, email status flag

**Differentiation check after all contacts at one company are done:** Scan all contacts at that company side by side. If any two have the same trigger or the same proof point, swap one of them to a different menu option before moving on.

**Checkpoint:** Every contact row in the tracker has: role scope note + assigned trigger + assigned angle + proof point T1 + proof point T2 + email flag. All 50 contacts complete. No drafts yet.

### Phase 5: T1 + T2 Draft Writing — ALL Research Complete First (200-250 min total)

**Start drafting ONLY after Phases 3 and 4 are fully complete for all 50 contacts.** This ensures each draft is written from a complete, differentiated research set — not partially assembled on the fly.

Draft in account batches, not random order. Write all contacts at one company consecutively to catch any overlap:

**Per contact (~4-5 min):**
1. Write T1 subject ("[Name]'s [role/pain angle] at [Company]" — specific to this person, not a generic pain category)
2. Write T1 body (3-para formula v2 — Para 1: "usually means" observation + check-in question → Para 2: bridge naming specific pain + customer metric + outcome → Para 3: stakes line + open-ended reply question. 75-99 words, exactly 2 question marks. See Part 6 for full spec and example.)
3. Write T2 body (Deep-Dive v4 — "I imagine" pain deepening → Testsigma pitch → customer story → 15-min CTA, 140-190 words. See Part 7 for canonical formula and reference example.)
4. Self-check: if the next contact at this same company read both their T1 and yours side by side, would they think it was the same template? If yes: revise the Para 1 observation or Para 2 bridge.

**Draft speed is fast here because all research is pre-done.** You're not thinking "what angle do I use?" — you're filling in a pre-mapped structure.

### Phase 6: Quality Gate (20-30 min for full batch of 50)

Before presenting to Rob, run the batch through the QA Gate:

**Per-message checks:**
- [ ] No "following up" / "circling back" / "I noticed" / "I saw" language anywhere
- [ ] T1 subject is person/company-specific — "[Name]'s [role/pain] at [Company]" format
- [ ] T1 Para 1 uses "usually means" or "tends to" opener (non-assumptive) + check-in question
- [ ] T1 Para 2 bridge explicitly names the same pain word/phrase used in Para 1 (not generic "same bottleneck")
- [ ] T1 Para 3 ends with an open-ended REPLY question (NOT a meeting ask — no "what day works")
- [ ] T1 body 75-99 words (hard cap 99)
- [ ] Exactly 2 question marks in T1 body
- [ ] "Testsigma" named in T1 body
- [ ] Named customer (Cisco, CRED, Hansard, Medibuddy, Samsung, or Fortune 100) in T1 body
- [ ] No em dashes anywhere
- [ ] No ` - ` separators (use commas)
- [ ] T2 body 140-190 words (Deep-Dive v4 — Part 7 canonical formula)
- [ ] T1 and T2 use different proof points
- [ ] No two contacts at same company have same Para 1 observation, same proof point, or same reply question
- [ ] Extrapolated emails flagged in tracker

**MQS check (spot-check minimum 5 contacts):** Run MQS scoring from sop-outreach.md on at least 10% of the batch. Target: all spot-checked contacts at 9/12 or above. If any score below 9: revise before presenting.

**Checkpoint:** Batch passes QA gate. Extrapolated emails flagged. MQS spot-check done.

### Phase 7: APPROVE SEND Presentation

Post the BATCH SUMMARY block per Part 10 format. Include:
- Total contacts: [N]
- Accounts covered: [N]
- Dedup removed: [N names]
- Email verification: [N] verified, [N] extrapolated (flagged)
- Targeting levels: [N] Standard, [N] Medium, [N] High
- MQS spot-check: [N] checked, [N] passing
- Link to tracker HTML file

Wait for Rob's APPROVE SEND. Do NOT enroll or send anything before approval.

### Phase 8: Send + Enroll (after APPROVE SEND)

**For each approved contact, three things must happen in this order: Send → Enroll in Apollo → Log everywhere.**

**Step 1 — Send via Apollo UI**

All emails send directly through Apollo's task composer. See Part 23 for the full protocol. Summary:
1. Enroll contact in TAM Outbound sequence (creates the Step 1 task)
2. Open the Step 1 task in Apollo → task composer panel opens
3. MANDATORY subject correction: triple-click subject field → type correct SMYKM subject (Part 24 — Apollo auto-populates wrong subject every time)
4. Inject body via JS execCommand insertText (Part 23 — clipboard paste via automation returns "Placeholder"; execCommand is the confirmed working method)
5. Verify: run `editor.textContent.slice(0,25)` to confirm correct body injected. Re-check subject field.
6. Click **"Send Now"** — wait for "Changes saved" toast to confirm send fired
7. Apollo marks Step 1 done automatically and generates Step 2 task

> ⚠️ **Send method note (V4.0 correction):** Computer-automation clipboard paste does NOT update Apollo's Quill internal model — the payload falls back to the sequence template. JS `document.execCommand('insertText', false, body)` correctly triggers Quill's React event bindings and updates the outbound payload. This is the confirmed working method across Sessions 15-20. See Part 23 for full JS block.

T1 email sends from robert.gorham@testsigma.com via Apollo. Note the exact send date/time.

**Step 2 — Apollo Enrollment (same session, same day — never defer)**
1. Confirm the contact exists in Apollo (search by name + company)
2. Enroll in TAM Outbound - Rob Gorham (69afff8dc8897c0019b78c7e) via `apollo_emailer_campaigns_add_contact_ids`
3. Flags: `sequence_no_email: true`, `sequence_active_in_other_campaigns: true`, `sequence_job_change: true` (if flagged as recent job change)
4. Email account: `robert.gorham@testsigma.com` (ID: `68e3b53ceaaf74001d36c206`) — .com ONLY
5. Batch size: max 5 per API call. For 50 contacts: 10 calls of 5. Do not rush — send batches sequentially.
6. Verify enrollment returned no `skipped_contact_ids`. If any skipped: diagnose reason and retry with appropriate flag before closing the session.

**Step 3 — Log in all three databases (do not skip any)**

**Database 1 — Batch Tracker HTML (primary audit trail):**
- Update contact row Status → `📤 T1 Sent [date] / ✅ Enrolled`
- Fill in T1 Send Date column
- Note any enrollment flags (job_change override, catchall email, etc.)

**Database 2 — MASTER_SENT_LIST.csv (dedup source of truth):**
Add one row per contact:
```
[Full Name], [email], [Company], [Title], Email, [YYYY-MM-DD send date], [tamob-batch-YYYYMMDD-N]
```
Do this for every contact without exception. This is what prevents double-sends in future batches.

**Database 3 — tam-coverage-tracker.csv (pipeline visibility):**
For each account where at least one contact was sent:
- Update status: `✅ Untouched` → `📤 In Sequence — [YYYY-MM-DD]`
- Add note field: contact name(s) enrolled, sequence step, batch ID

**Enrollment tempo:** 10 batches of 5 for 50 contacts takes ~15-20 min. Do not rush. Verify each batch's response before sending the next.

### Phase 9: Session Close — Confirm All Three Databases Updated

Before ending the session, run this checklist:

**Apollo (Sequence Tasks):**
- [ ] All approved contacts show as enrolled in TAM Outbound sequence
- [ ] Zero `skipped_contact_ids` unresolved
- [ ] Apollo task queue will show Step 2 tasks auto-generated for Day 5 from each T1 send date
- [ ] If any contacts were NOT sent today (held for Rob): do NOT enroll them yet — enrollment triggers the sequence timer

**MASTER_SENT_LIST.csv:**
- [ ] One new row added per contact sent today
- [ ] Batch ID column filled for all rows
- [ ] No blank email fields

**tam-coverage-tracker.csv:**
- [ ] All accounts with sends today updated to "📤 In Sequence — [date]"
- [ ] Accounts where all contacts were deduped out: update to "⛔ Checked — no clean contacts" with note

**Batch tracker HTML:**
- [ ] All sent contacts: Status = T1 Sent + Enrolled
- [ ] HOLD contacts: Status = 🚫 HOLD with reason
- [ ] File saved and committed

**Session memory files:**
1. Update `memory/session/handoff.md`: new batch count, enrolled total, any flags
2. Update `memory/session/work-queue.md`: mark today's batch done, queue next batch date
3. Git add + commit all changed files → Rob git pushes from terminal

### Daily Metrics to Track

| Metric | Target |
|--------|--------|
| New T1s sent | 50/day |
| New enrollments | 50/day |
| Accounts covered | However many it takes to hit 50 contacts (typically 10-50) |
| Extrapolated emails in batch | < 10% of batch (max 5 out of 50) |
| MQS spot-check pass rate | 100% of checked contacts at 9+ |
| Dedup removal rate | Track for pattern detection |

### Managing the Growing Follow-up Load

As the enrolled base grows, Apollo will generate more follow-up tasks per day (T2s, LinkedIn connects, calls). Here's the rough daily task load:

| Days Since Launch | Approx. Apollo Tasks Due Daily |
|-------------------|-------------------------------|
| Days 1-4 | Low — only T2s if any T1s were sent 4-5 days ago |
| Days 5-15 | Growing — T2s + LinkedIn connects accumulating |
| Days 15-28 | High — T2s + calls + new enrollments all active |
| Steady state (Day 28+) | ~50-70 tasks/day (new T1s + follow-ups for prior batches) |

**Priority order when task load is high:**
1. T2 email drafts (Day 5 from T1) — highest leverage, highest reply probability window
2. New T1 batch drafts — keeps pipeline full
3. LinkedIn connection requests (Day 10) — quick, minimal drafting
4. Call alerts to Rob (Days 15/21/28) — Claude flags, Rob executes
5. Breakup emails (Day 35) — draft and queue

If daily task volume feels overwhelming: reduce new T1 batch to 25-30/day temporarily until follow-up clears. Do not skip follow-up tasks — they are where meetings get booked.

---

## Part 21: Batch Naming Convention

All TAM Outbound batch files use this naming system going forward:

| Type | Format | Example |
|------|--------|---------|
| Daily batch tracker | `tamob-batch-YYYYMMDD-N.html` | `tamob-batch-20260311-1.html` |
| Legacy Wave 1 tracker | `wave1-batch1-tracker-mar10.html` | (existing file — do not rename) |
| Daily draft file (if separate) | `tamob-drafts-YYYYMMDD.md` | `tamob-drafts-20260311.md` |

N = batch number within the same day (usually 1; split into 2 if session breaks mid-batch).

**Git commit message format for batch commits:**
```
TAM batch [YYYYMMDD]-[N]: [N] contacts across [N] accounts enrolled

- Accounts: [Company A, Company B, ...]
- Dedup removed: [N]
- Enrolled: [N] / [total batch size]
- Next batch: [date]
```

---

*Version 2.1 — Updated Mar 10, 2026 — Research depth hardened, batch-first drafting enforced, logging protocol airtight*
*Next review: After first 250 contacts enrolled (est. 5 days at 50/day)*

---

## Part 22: Automated QA Gate + Enrollment Pipeline

*Added Mar 10, 2026 — End-to-end automation from batch tracker HTML to Apollo enrollment*

This section documents the automated pipeline built for TAM Outbound T1 emails. It covers the Python QA gate script, the automated trim process, and the Apollo enrollment flow. Run this pipeline on every T1 batch after Rob gives APPROVE SEND.

---

### Step 1 — Run QA Gate (automated)

The QA gate script checks every email in the batch tracker HTML and flags any that fail. It lives at `/sessions/determined-sharp-keller/qa_gate_v3.py` but should be regenerated from the spec below each session (the VM resets between sessions — only `/Work/` persists).

**Script spec — `qa_gate_v3.py`:**

```python
import re
from bs4 import BeautifulSoup

html_path = "/sessions/determined-sharp-keller/mnt/Work/[BATCH_FILE].html"
with open(html_path, "r") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
cards = soup.find_all("div", class_="email-body")

BANNED_EXACT = ["AI"]           # checked with word boundary \b
BANNED_SUB = ["self-healing", "flaky test", "CI/CD", "I noticed", "I saw", "what day works"]
BANNED_CHAR = ["—"]             # em dash
NAMED_CUSTOMERS = ["Cisco", "Samsung", "Honeywell", "Bosch", "Nokia", "Nestle",
                   "KFC", "DHL", "Zeiss", "NTUC", "Oscar Health", "Sanofi",
                   "Spendflo", "Nagra", "Hansard", "Medibuddy", "CRED", "APA"]
# NAMED_CUSTOMERS: use word boundary \b (case-insensitive) to avoid
#   substring false positives (e.g. "APA" inside "capacity")
```

**What it checks per email:**
- Body core word count: 80-97 words (body core = text AFTER "Hi [Name],\n\n" AND BEFORE "Rob Gorham | Testsigma")
- Exactly 2 question marks in the full email
- No banned exact words (whole-word "AI", not "automation" or "maintaining")
- No banned substrings (self-healing, flaky test, CI/CD, I noticed, I saw, what day works)
- No em dashes (—)
- No named customers (word boundary, case-insensitive)
- Required phrase: "thought it would be worth" present in body core
- Opener format: "Hi [First Name]," present

**Known edge cases:**
- "Yu Jin" is a two-part first name. The opener "Hi Yu Jin," is correct. If the script uses `name.split()[0]` it produces "Yu" which fails the opener check. Use full first name "Yu Jin" for this contact, or hard-code the check.
- "APA" named customer check must use `\b` word boundary to avoid matching inside "capacity," "Japan," etc.
- "AI" must use `\b` word boundary — substring match would flag "automation," "maintaining," "detailing," etc.

**Pass threshold:** All 12 criteria. Any failure = fix before enrolling.

---

### Step 2 — Trim Failing Emails (if needed)

If any emails fail the word count check (>97 words), trim them before enrolling. Never send an over-limit email.

**Trim methodology:**
1. For each failing email, identify the body core (text after greeting, before signature)
2. Count words: `len(body_core.split())`
3. Trim to ≤97 words while preserving: challenge narrative, Q1, vertical proof point, "thought it would be worth," Q2 close, 2 question marks, no banned words
4. Common trim targets: redundant prepositional phrases, "right now," "tend to," "a lot of" → "significant," "in the same release window" → "at that pace," extra adjectives in P3
5. After trimming all emails, write a replace script (`trim_emails.py`) that updates both the `<div class="email-body">` content (real newlines) AND the `onclick="copyText(...)"` attribute (escaped `\n` sequences)
6. Re-run QA gate to confirm all pass before proceeding

**trim_emails.py template:**
```python
html_path = "/sessions/determined-sharp-keller/mnt/Work/[BATCH_FILE].html"
with open(html_path, "r") as f:
    html = f.read()

edits = [
    (first_name, sig_tail, old_core, new_core),
    # one entry per trimmed email
]
for (first_name, sig_tail, old_core, new_core) in edits:
    old_full = f"Hi {first_name},\n\n{old_core}\n\nRob Gorham | Testsigma\n{sig_tail}"
    new_full = f"Hi {first_name},\n\n{new_core}\n\nRob Gorham | Testsigma\n{sig_tail}"
    if old_full in html:
        html = html.replace(old_full, new_full, 1)
    # Also update onclick copy text (escaped newlines)
    old_js = old_full.replace("'", "\\'").replace("\n", "\\n")
    new_js = new_full.replace("'", "\\'").replace("\n", "\\n")
    if old_js in html:
        html = html.replace(old_js, new_js, 1)

with open(html_path, "w") as f:
    f.write(html)
```

---

### Step 3 — Extract Prospect Details from Batch Tracker

Parse the overview table in the HTML to get all 16 (or N) contacts with their Apollo enrollment data:

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
table = soup.find("table", class_="overview")
rows = table.find("tbody").find_all("tr")

prospects = []
for row in rows:
    cells = row.find_all("td")
    if len(cells) >= 4:
        name = cells[0].get_text(strip=True)
        title = cells[1].get_text(strip=True)
        company = cells[2].get_text(strip=True)
        email = cells[3].get_text(strip=True)
        priority_span = cells[4].find("span") if len(cells) > 4 else None
        priority = priority_span.get_text(strip=True) if priority_span else ""
        prospects.append({"name": name, "title": title, "company": company,
                          "email": email, "priority": priority})
```

---

### Step 4 — Create / Verify Apollo Contacts

For each prospect:
1. Search Apollo contacts by email: `apollo_contacts_search(q_keywords=email)`
2. If not found: create via `apollo_contacts_create` with `run_dedupe=true`
3. Track the returned `id` for enrollment
4. Multi-word first names (e.g. "Yu Jin"): pass `first_name="Yu"`, `last_name="Jin"` — NOT `first_name="Yu Jin"` which doubles the name

**Required fields for create:**
- `first_name`, `last_name` (split from full name)
- `email` (verified business email from tracker)
- `title` (from tracker)
- `organization_name` (from tracker)
- `website_url` (company domain)
- `run_dedupe=true`

---

### Step 5 — Enroll in TAM Outbound Sequence

**Sequence:** TAM Outbound - Rob Gorham (`69afff8dc8897c0019b78c7e`)
**Email account:** `robert.gorham@testsigma.com` (`68e3b53ceaaf74001d36c206`) — .com ONLY

Enroll HIGH → MED → LOW order. Batch by priority tier (6+9+1 = 16 for Wave 2). Batches up to 10 are fine for email-only contacts. Larger batches (50+) should be split into groups of 10 to avoid timeouts.

```python
apollo_emailer_campaigns_add_contact_ids(
    id="69afff8dc8897c0019b78c7e",
    emailer_campaign_id="69afff8dc8897c0019b78c7e",
    contact_ids=[id1, id2, ...],
    send_email_from_email_account_id="68e3b53ceaaf74001d36c206",
    sequence_no_email=False,
    sequence_active_in_other_campaigns=False
)
```

Verify response: check that `emailer_campaign_ids` contains `69afff8dc8897c0019b78c7e` for each enrolled contact.

---

### Step 6 — Log and Update Status

After all contacts enrolled:

**MASTER_SENT_LIST.csv — append one row per contact:**
```
[Full Name], TAM Outbound Wave[N] T1 [Date], [YYYY-MM-DD], Email (Apollo TAM Outbound T1), 0, [batch-file.html], [lowercase full name]
```

**Batch tracker HTML — update status badges:**
```python
old_badge = '<span class="badge badge-high">Draft Ready</span>'
new_badge = '<span class="badge badge-sent">T1 Sent [Mon DD]</span>'
html = html.replace(old_badge, new_badge)
```

Add `.badge-sent` CSS if not present:
```css
.badge-sent { background: #d4edda; color: #155724; padding: 3px 8px;
              border-radius: 4px; font-size: 0.8em; font-weight: 600; }
```

---

### Full Pipeline Summary (T1 Email Batch)

```
APPROVE SEND received
        ↓
1. Run QA gate (qa_gate_v3.py) on batch HTML
        ↓
2. Any failures? → Trim emails (trim_emails.py) → Re-run QA gate → All pass
        ↓
3. Extract prospects from batch HTML overview table
        ↓
4. Search Apollo for each contact → create if missing (run_dedupe=true)
        ↓
5. Enroll HIGH → MED → LOW in TAM Outbound sequence (ID: 69afff8dc8897c0019b78c7e)
   Send email from account: robert.gorham@testsigma.com (ID: 68e3b53ceaaf74001d36c206)
        ↓
6. *** SEND T1 VIA APOLLO UI (Part 23) — one contact at a time ***
   Open Step 1 task in Apollo Tasks tab
   → MANDATORY: Triple-click subject field → type correct SMYKM subject (Part 24 — Apollo ALWAYS auto-populates wrong subject)
   → Inject body via JS execCommand insertText (Part 23 — clipboard paste returns "Placeholder", DO NOT use)
   → Verify: editor.textContent.slice(0,25) confirms correct opener, re-check subject
   → Click "Send Now" → confirm "Changes saved" toast appears
   → Apollo marks Step 1 done + generates Step 2 task automatically
   → Repeat for all contacts in batch — one at a time
        ↓
7. Verify all contacts show sequence ID in emailer_campaign_ids
        ↓
8. Append rows to MASTER_SENT_LIST.csv (one row per contact sent)
        ↓
9. Update HTML status badges: Draft Ready → T1 Sent [Date]
        ↓
10. Update handoff.md, work-queue.md, session-log.md
        ↓
11. Git commit + push
```

**T2 follow-up schedule:** T2 due ~1 day after Step 1 sent in Apollo (Apollo auto-generates task). Check daily per sop-daily.md. T2 also sends via Apollo UI (Part 23).

---

*Part 22 added Mar 10, 2026 — documents automation pipeline built during Wave 2 T1 send session*
*Part 22 updated Mar 11, 2026 (v3.1) — pipeline reordered: enroll first, then send via Apollo UI. Gmail Chrome method retired.*

---

## Part 23: Apollo UI Send Protocol — Canonical Reference

*Version 4.0 — Mar 11, 2026. This section supersedes all prior versions. Confirmed working method: JS execCommand insertText. Clipboard paste via computer automation returns "Placeholder" — do NOT use. See Part 24 for mandatory subject correction step.*

---

### Why Apollo UI (not Gmail MCP or Gmail Chrome)

Sending from Gmail directly bypasses Apollo's tracking entirely. Emails sent outside Apollo don't register as sequence activity — no open tracking, no click tracking, no sequence analytics. Apollo's task queue also stays in an incorrect state (Step 1 still showing pending after Gmail send).

**The only correct send path:** Apollo Tasks tab → open composer → inject body via JS execCommand insertText → verify → click "Send Now." This keeps all sequence tracking intact and fires the correct personalized content.

---

### Send Method: JS execCommand insertText (CONFIRMED WORKING)

**Why this method, not keyboard paste:** In Apollo's Quill editor, clipboard paste triggered via computer automation (Ctrl+A + Ctrl+V) does NOT update Quill's internal document state. Apollo reads the outbound payload from Quill's internal model, not from what is visually displayed. Computer-automation paste injects a literal "Placeholder" or falls back to template text in the payload. The `document.execCommand('insertText')` method fires the correct browser input events that Quill's React bindings listen to, so it DOES update the internal model and DOES update the outbound payload.

**The confirmed working JS block (run in browser console for each email):**

```javascript
var editor = document.querySelector('.ql-editor');
editor.focus();
document.execCommand('selectAll', false, null);
document.execCommand('insertText', false, BODY_TEXT_HERE);
```

Where `BODY_TEXT_HERE` is the full email body string, starting with `Hi [First Name],\n\n` and ending with `\n\nRob Gorham | Testsigma\n[phone] · testsigma.com`.

**Verification before clicking Send Now:**
```javascript
editor.textContent.slice(0, 25)
```
Confirm this returns the start of "Hi [First Name]," — not "Hi {{" or template text. If it returns placeholder content, the injection failed — do NOT send.

**Python lookup for subject + body from wave3_drafts.json:**
```python
import json
data = json.load(open('/sessions/determined-sharp-keller/wave3_drafts.json'))
[print(c['subject'], '\n', c['body']) for c in data if c['id'] == 'L04']
```
Replace `'L04'` with the contact's Wave ID. This gives you the exact SMYKM subject and personalized body to inject.

> ⚠️ **INC-007 note (historical):** INC-007 involved a different type of programmatic injection — direct DOM manipulation or innerHTML assignment — that updated the visual display without updating Quill's internal model. The `document.execCommand('insertText')` method is distinct: it triggers Quill's registered event handlers and correctly updates the internal document state. Sessions 15-20 have confirmed execCommand insertText as the reliable method across all sends.

---

### Pre-Send Requirements

Before starting any send session:
- [ ] Blue/work Chrome profile (Testsigma account). Never red/personal.
- [ ] Logged into app.apollo.io as `robert.gorham@testsigma.com`
- [ ] Draft reference file open (batch tracker HTML, wave3_drafts.json, or equivalent)
- [ ] Rob has given **APPROVE SEND** for this specific batch

---

### Protocol: Sending One Email via Apollo Task

For each contact in the batch (T1 or T2):

**Step 1 — Open the task in Apollo**
1. Go to Apollo → Sequences → TAM Outbound - Rob Gorham → Tasks tab
2. Find the contact's Step 1 (T1) or Step 2 (T2) task
3. Click the task to expand the composer panel

**Step 2 — Fix the subject line (MANDATORY — Apollo always populates the wrong subject)**

> ⚠️ **Critical:** Apollo auto-populates a generic subject like "[First Name]'s QA coverage at [Company]" or "[First Name]'s software testing at [Company]" every time. This is NOT the SMYKM subject. You MUST correct it before every send. See Part 24 for full subject correction protocol.

1. Triple-click the subject field (selects all text)
2. Type the correct SMYKM subject from wave3_drafts.json or the batch tracker
3. Confirm the subject field now shows the personalized subject exactly

**Step 3 — Inject the body via JS execCommand insertText**
1. Click the body editor area once (focus it)
2. Open browser console (F12 → Console)
3. Run the JS block from the section above, substituting the correct body text
4. Run the verification: `editor.textContent.slice(0, 25)` — confirm it starts with "Hi [First Name],"
5. If verification fails: run the injection again. If still fails, reload Apollo and retry.

**Step 4 — Final pre-send checklist (mandatory)**
Visually confirm ALL before clicking Send Now:
- [ ] **Stage check:** Contact's Apollo Stage is cold (New, Prospect, etc.) — NOT "Connected", "Meeting Held", "Opportunity", or any warm/active stage. If warm stage: STOP, do not send, alert Rob.
- [ ] Subject: personalized SMYKM subject, matches draft reference exactly
- [ ] Subject: does NOT contain "QA coverage" unless that is correct for this specific person
- [ ] Body: starts with "Hi [First Name]," — correct first name for THIS contact
- [ ] Body: does NOT contain "Placeholder" anywhere
- [ ] Body: does NOT contain `[` or `]` bracket placeholders
- [ ] Sending from: `robert.gorham@testsigma.com` (confirm in Apollo account dropdown if unsure)

If ANY check fails: STOP. Do not click Send Now. Fix first.

**Step 5 — Send**
1. Click **"Send Now"**
2. "Changes saved" toast appears — this confirms the send fired
3. Task disappears from the active Tasks list — Apollo marks Step 1 done and generates Step 2 task automatically

**Step 6 — Log the send**
1. Note the send time
2. Update the contact's status in the batch tracker HTML: "T1 Sent [date]" or "T2 Sent [date]"
3. Do NOT proceed to the next contact until the current send is confirmed via the "Changes saved" toast

---

### Error Scenarios

| Situation | Action |
|-----------|--------|
| JS injection fails (textContent shows placeholder) | Reload Apollo, re-open task, re-run execCommand injection. Verify before sending. |
| Subject auto-corrects back to generic after paste | Triple-click subject → retype correct subject → immediately click body area to lock it |
| "Send Now" sends wrong content | STOP. Log in incidents.md. Inform Rob immediately. Do not continue batch. |
| Task not visible in Apollo Tasks tab | Contact may not be enrolled yet. Check enrollment status (Part 11). |
| Hard bounce (SMTP 550) after send | Log in incidents.md as a bounce. Remove contact from Apollo sequence. Re-enrich email before retrying. |
| Wrong email account in Apollo sender | Go to Apollo account settings → confirm outbound email is robert.gorham@testsigma.com |
| "Changes saved" toast does not appear | Check network tab in DevTools. If send did not fire, retry. Do not double-send — verify first. |

---

### Recovery: If a Send Error Occurs Mid-Batch

If you accidentally send wrong content (wrong contact, wrong draft, or placeholder text):
1. STOP immediately — do not continue sending
2. Log the error in `memory/incidents.md` (INC-XXX) with full detail: which contact, what was sent, what should have been sent
3. Check Apollo sequence activity log to understand the exact scope
4. Update `memory/session/handoff.md` with the incident flag
5. Commit current state immediately
6. Do NOT attempt self-recovery — surface to Rob in the session response so he decides remediation

---

*Part 23 rewritten V4.0 — Mar 11, 2026. Confirmed working method is JS execCommand insertText, not clipboard paste. Subject correction is mandatory per Part 24. Gmail Chrome method permanently retired.*

---

## Part 24: Subject Line Correction Protocol (MANDATORY)

*Added V4.0 — Mar 11, 2026. This step is required before EVERY T1 and T2 send. Apollo always auto-populates the wrong subject.*

---

### The Problem

Apollo auto-populates the subject field every time you open a task composer. The auto-populated subject uses a generic pattern: **"[First Name]'s [generic descriptor] at [Company]"** — e.g. "Suchith's QA coverage at PTC" or "Rachel's software testing at Bosch." This is never the correct SMYKM subject.

Apollo's auto-subject does NOT match the hyper-personalized SMYKM subject you drafted. If you send without correcting it, the recipient gets a generic, interchangeable subject that undermines the entire SMYKM personalization strategy. This has been observed on every single send across Sessions 15-20.

**The generic subject Apollo uses:**
- "[Name]'s QA coverage at [Company]" — most common
- "[Name]'s software testing at [Company]" — second most common
- "[Name]'s test automation at [Company]" — occasional

**The correct SMYKM subject (example):**
- "Suchith's test automation decisions at PTC"
- "Rachel's engineering coverage at Bosch"
- "Garrick's software testing velocity at [Company]"

The SMYKM subject is hyper-personalized to the individual's role and the specific angle of the email. It is NEVER interchangeable.

---

### How to Correct the Subject

**Step 1 — Find the correct subject**

Source priority:
1. `wave3_drafts.json` — look up by contact ID: `python3 -c "import json; data=json.load(open('/sessions/determined-sharp-keller/wave3_drafts.json')); [print(c['subject']) for c in data if c['id']=='L04'"`
2. Batch tracker HTML — find the contact's row, copy subject from the Subject column
3. Memory: check the send table in `memory/session/handoff.md` for previously confirmed subjects

**Step 2 — Fix the subject field in Apollo**
1. Triple-click the subject field (selects all auto-populated text)
2. Type the correct SMYKM subject — do NOT paste (paste may not clear the existing text cleanly)
3. Visually confirm the subject field shows the correct personalized subject
4. Click the body area once to lock the subject before moving on

**Step 3 — Verify after body injection**
After injecting the body (Part 23 Step 3), scroll back up to the subject field and confirm it still shows the correct subject. Apollo has been observed re-populating the subject in some edge cases after interacting with the body field.

---

### Subject Correction Failures Observed (Sessions 15-20)

| Contact | Apollo Auto-Subject | Correct SMYKM Subject |
|---------|--------------------|-----------------------|
| Suchith Ramgiri / PTC | "Suchith's QA coverage at PTC" | "Suchith's test automation decisions at PTC" |
| Garrick Doell | "Garrick's software testing at [Co]" | "Garrick's software testing velocity at [Co]" |
| Ashwin Ramesh | "Ashwin's QA coverage at [Co]" | "Ashwin's test automation at [Co]" |
| Rachel Toffoli | "Rachel's QA coverage at Bosch" | "Rachel's engineering coverage at Bosch" |
| Madina Zabran | "Madina's QA coverage at [Co]" | "Madina's test coverage at [Co]" |

Pattern: Apollo always defaults to "QA coverage" regardless of the contact's actual role or angle. SMYKM subjects use role-specific language (test automation decisions, engineering coverage, testing velocity, etc.).

---

### SMYKM Subject Formula (for reference)

Format: `[First Name]'s [role-specific 2-3 word descriptor] at [Company]`

| Persona | Good descriptors |
|---------|-----------------|
| QA Manager / QA Lead | test automation decisions · QA coverage strategy · testing roadmap |
| Director/VP of QA | testing org scale · QA team efficiency · quality engineering decisions |
| SDET / Automation Lead | automation stack decisions · test maintenance load · flaky test problem |
| Software Eng Manager | engineering test coverage · release confidence · QA velocity |
| VP Eng / CTO | engineering quality bar · test automation ROI · release velocity |

The descriptor should match the EMAIL ANGLE, not just the title. If the email is about maintenance time, use "test maintenance load." If about coverage gaps, use "test coverage strategy."

---

*Part 24 added V4.0 — Mar 11, 2026. Subject correction is mandatory on every send. Apollo's auto-population is never correct.*

---

## Part 25: T2 Send Protocol

*Added V4.0 — Mar 11, 2026. Wave 2 T2s are now in the Apollo task queue. Wave 1 T2s due Mar 12. This part governs T2 drafting, QA, and send.*

---

### ALL STEPS ARE MANUAL SEND — NO AUTO-SEND EVER

> ⚠️ **Critical sequence configuration rule:** The TAM Outbound - Rob Gorham sequence has ALL 7 steps configured as **manual tasks**. Apollo NEVER sends anything automatically. Every step — T1, T2, LinkedIn, calls, breakup — requires Claude to open the task, inject personalized content, verify, and manually click "Send Now."
>
> **NEVER change any sequence step from Manual to Automated.** If you see a step showing "Automated" in Apollo sequence settings, STOP and alert Rob immediately — do not send. Check sequence settings before every session: Apollo → Sequences → TAM Outbound - Rob Gorham → Edit Sequence → confirm all 7 steps show "Manual Task."
>
> **What "auto-generates" means:** When a contact's Step 1 task is completed (after you click Send Now), Apollo automatically queues the Step 2 task in the Tasks tab. This is a task NOTIFICATION — not an email send. The email does not go out until you manually open the Step 2 task, compose it, and click Send Now yourself. This applies to every step in the sequence.

---

### When T2 Tasks Appear

Apollo queues the Step 2 (T2) task automatically after Step 1 is marked complete. The task appears in the Apollo Tasks tab with the label "Step 2: Follow-up email" and will show as Due once the Day 5 window arrives. T2 tasks surface per-contact, not per-batch. Nothing is sent until you manually open the task and click Send Now.

**Current T2 pipeline status (as of Mar 11, 2026):**
- **Wave 1 T2:** Due Mar 12 (tomorrow). ~16 contacts from the Wave 1 batch sent Feb 26-27 area.
- **Wave 2 T2:** Now in Apollo task queue — 12 contacts: Karen Teng, Maalika Tadinada, Sambhav Taneja, Anton Aleksandrov, Roberto Bouza, Sarah Kneedler, Chandni Jain, Cristian Brotto, Marcela Fetters, Henry Rose, Krista Moroder, Yu Jin.
- **Wave 3 T2:** Due Mar 16 (33 contacts from Wave 3 T1 sends Mar 6-11).

---

### T2 Formula

⚠️ **CANONICAL SOURCE IS PART 7 (Deep-Dive v4, Updated Mar 12).** The section below is superseded. Use Part 7 for all T2 drafting. Playbook: `memory/playbooks/t2-followup.md`.

**T2 Summary (from Part 7 v4):**
- **Word count:** 140-190 words (intentionally longer than T1)
- **Structure (4 parts):** (1) "I imagine" + deeper pain speculation, (2) Testsigma solution pitch, (3) customer story + WHY relevant, (4) 15-minute CTA
- **CTA:** 15-minute meeting ask ("Would 15 minutes make sense to walk through how [Customer] made that shift and see if it applies?") — NOT an engagement question
- **BANNED:** "Circling back" / "Following up" / "One more angle worth adding" / "Different lens from my last note"
- **Threading:** Send as a reply to T1 thread when possible
- **New proof point:** Must be different from T1 customer story

---

### T2 QA Gate (Part 7 v4)

| Check | Pass |
|-------|------|
| Word count | 140-190 words |
| "I imagine" opener in Part 1 | Yes |
| Different proof point from T1 | Yes |
| No banned phrases ("Circling back" etc.) | Zero |
| Named customer with specific metric | Yes |
| WHY customer story is relevant to them | Yes |
| 15-minute CTA (not engagement question) | Yes |
| No placeholder text | Zero |
| No em dashes | Zero |

Minimum passing score: 7/9. Fix before sending.

---

### T2 Drafting Workflow

**Before drafting:**
1. Pull up the T1 email sent to this contact (from batch tracker HTML or handoff.md send table)
2. Note: what challenge angle did T1 use? What proof point? What CTA?
3. T2 must use a DIFFERENT angle, a DIFFERENT proof point

**Drafting in batches:**
- Draft all T2s for a given wave in one session before sending any
- Use the wave batch tracker HTML as the reference (same contact list, same research)
- Add a "T2 Draft" section to the tracker or create a separate `tamob-t2-drafts-YYYYMMDD.md` file
- Get Rob's APPROVE SEND before sending any T2

**After APPROVE SEND:**
- Send via Apollo Tasks tab (same protocol as Part 23)
- Subject: T2 uses a DIFFERENT subject than T1. Same SMYKM format but different descriptor angle.
- Body injection: same JS execCommand insertText method (Part 23)
- Subject correction: same mandatory triple-click fix (Part 24) — Apollo auto-populates wrong subject for T2 just as for T1
- Log each send: update batch tracker status to "T2 Sent [date]"
- Append rows to MASTER_SENT_LIST.csv with "T2" notation

---

### T2 Send Sequence Lookup

Apollo Step 2 tasks appear in the Tasks tab under the sequence. Filter by:
- Sequence: "TAM Outbound - Rob Gorham"
- Step: "Step 2"
- Status: "Pending" or "Due"

If the task tab shows mixed T1 and T2 tasks, check the Step column carefully. T1 = Step 1, T2 = Step 2. Do not send T2 content into a T1 task or vice versa.

---

### T2 Priority Order When Volume Is High

**⚠️ Operating directive (Mar 12, 2026): New T1 batch work comes before T2s every day.** T2s are handled after T1 batch is complete, or in remaining session time. The only exception: 20+ T2s overdue simultaneously — in that case, clear the backlog first, then resume T1 batching.

When multiple waves have T2s due simultaneously:
1. **Wave with oldest T1 send date first** — longest wait = highest reply risk if not followed up
2. Within the same wave: HIGH priority contacts first (same as T1 batch order)
3. Breakup emails (Step 7) do NOT take priority over active follow-up steps

If T2 volume exceeds session capacity (> 20 contacts), send the oldest/highest-priority contacts first and log the remainder as "T2 pending" in handoff.md with exact count.

---

*Part 25 added V4.0 — Mar 11, 2026. Updated Mar 12, 2026: T1 batch prospecting takes daily priority over T2 processing per current pipeline volume directive.*


---

## Part 26: Process Logging and Activity Tracking

*Added V4.0 — Mar 11, 2026. Log everything, every session. This is the data layer that enables performance analysis, error recovery, and continuous improvement.*

---

### Why Log Everything

Every send, every reply, every bounce, every decision point generates data that compounds over time. The goal is a complete audit trail so that any future Claude session can reconstruct exactly what happened, why, and what comes next — without having to re-derive state from Apollo or Gmail.

The logging system has six components: session log, send log (MASTER_SENT_LIST), batch trackers, handoff/work-queue, incidents log, and reply/warm lead tracking.

---

### Component 1: Session Log — `memory/session/session-log.md`

**Updated:** End of every session, without exception.
**What to log per session:**

```
## Session [N] — [Date] — [Focus area]

### Sends This Session
| Contact | ID | Company | Subject | Send Time | Step |
|---------|----|---------|---------|-----------|------|
| [Name]  | [Wave ID] | [Co] | [Subject] | [HH:MM] | T1/T2 |

### Wave Totals
- Wave 1 T1: [N]/[total] sent
- Wave 2 T1: [N]/[total] sent
- Wave 3 T1: [N]/[total] sent
- Wave 1 T2: [N] sent this session
- Wave 2 T2: [N] sent this session

### Enrollments
- [N] contacts enrolled in Apollo sequence
- Any skipped_contact_ids: [list or "none"]

### Key Decisions
- [Any judgment calls made, dedup decisions, hold decisions, etc.]

### Errors / Incidents
- [Any INC created, or "none"]

### Session Technical Notes
- [Any JS failures, Apollo UI quirks, send method observations]

### Next Priority
- [Exact task for next session, with count and due date]
```

**Retention:** Never delete session log entries. Session log is a permanent record.

---

### Component 2: Send Log — `MASTER_SENT_LIST.csv`

**Updated:** After every send, same session. Never defer.
**Schema:** `Full Name, Batch Label, Send Date (YYYY-MM-DD), Channel+Step, Open Count, Batch File, Search Key`

**Example rows:**
```
Karen Teng, TAM Outbound Wave2 T1 Mar6, 2026-03-06, Email (Apollo TAM Outbound T1), 0, wave2-batch-mar6.html, karen teng
Karen Teng T2, TAM Outbound Wave2 T2 Mar11, 2026-03-11, Email (Apollo TAM Outbound T2), 0, wave2-t2-mar11.html, karen teng t2
```

**Rules:**
- One row per send event (T1 and T2 are separate rows for the same contact)
- Batch Label format: `TAM Outbound Wave[N] T[step] [MonDD]`
- Search Key = lowercase full name (used for dedup lookups)
- Open Count starts at 0; update when Apollo shows opens (future enhancement)
- Never delete rows — append only

**Pre-batch dedup query:** Before building any new batch, run:
```bash
grep -i "[prospect name]" /sessions/determined-sharp-keller/mnt/Work/MASTER_SENT_LIST.csv
```
If a match exists: do NOT add to batch. Skip with note in handoff.md.

---

### Component 3: Batch Tracker HTML — Per-Batch File

**File naming:** `tamob-batch-YYYYMMDD-N.html` (e.g. `tamob-batch-20260311-1.html`)
**Location:** `/Work/`
**What it captures per contact:**
- Name, Title, Company, Email, Apollo ID
- Priority tier (HIGH / MED / LOW)
- T1 Subject (SMYKM)
- T1 Body (full personalized draft)
- T1 Challenge hook / angle used (for T2 reference)
- Status badge: Draft Ready → T1 Sent [date] → T2 Sent [date] → Reply → Bounced → DNC
- Enrollment status and any flags (job_change override, catchall, etc.)
- T2 draft section (added when T2 is written)
- Notes field for anything unusual

**Status badge progression:**
```
Draft Ready → T1 Sent [Mon DD] → T2 Drafted → T2 Sent [Mon DD] → 
[Reply ✅] or [LinkedIn Sent] or [Call Attempted] or [Breakup Sent] or [DNC ⛔]
```

**The batch tracker is the primary per-contact audit trail.** Everything about what was sent to a specific person lives here.

---

### Component 4: Handoff + Work Queue — `memory/session/handoff.md` + `memory/session/work-queue.md`

**Updated:** End of every session, before git commit.
**Purpose:** Handoff carries the live state so the NEXT Claude session can start without any re-derivation.

**handoff.md must always contain:**
- Current session number
- Wave 1/2/3 T1 and T2 send counts with exact totals
- Any contacts in HOLD, PENDING, or future-dated state
- Next due date and task (exact — not vague)
- Any open incidents or errors
- Last commit hash

**work-queue.md must always contain:**
- Active tasks with priority and due date
- Completed tasks (marked done, not deleted)
- Blocked tasks with explicit blocker reason

---

### Component 5: Incidents Log — `memory/incidents.md`

**Updated:** Immediately when an error occurs. Never defer.
**Format per incident:**

```
## INC-[NNN]: [Short title]
**Date:** YYYY-MM-DD
**Severity:** P0 (send error) / P1 (data error) / P2 (process deviation)
**What happened:** [Exact description — what was sent, to whom, what was wrong]
**Scope:** [How many contacts affected]
**Root cause:** [Technical or process cause]
**Immediate action taken:** [What Claude did]
**Rob decision:** [What Rob decided, if consulted]
**Prevention:** [What SOP rule was added or updated to prevent recurrence]
**Status:** Open / Resolved
```

**What gets an INC:**
- Any send with wrong content (wrong body, placeholder, wrong recipient)
- Any double-send (same contact, same step, sent twice)
- Any enrollment with wrong email account (.net, .in instead of .com)
- Any sequence step inadvertently set to Automated
- Any data modification (record deleted, email updated) not explicitly approved by Rob
- Any bounce or deliverability event

**What does NOT need an INC:**
- Contacts skipped for dedup (log in handoff.md instead)
- Apollo enrollment skips due to `skipped_contact_ids` (log in session log and handoff)
- Future-dated tasks (normal state — log in handoff.md)

---

### Component 6: Reply and Warm Lead Tracking — `memory/warm-leads.md`

**Updated:** When any reply is received or a warm signal observed.
**What to track:**

```
## [Name] — [Company]
**Status:** [Active warm lead / Monitoring / Replied / Booked / DNC]
**Last Action:** [Most recent thing Claude or Rob did]
**Reply:** [Full reply text or summary, with date]
**Thread:** [Gmail thread ID if available]
**Context:** [Sequence step when they replied, time since T1, tone]
**Next Action:** [Exact next step, who does it, by when]
**Notes:** [Anything relevant — referral, pain signals, objections raised]
```

**Monitoring cadence:** Check Gmail MCP for replies at start of each session.
**Trigger:** Any reply — positive, negative, or neutral — gets a warm-leads entry.

---

### Activity Metrics to Track (Per Session)

Log these in the session log. They build a dataset over time for performance analysis.

| Metric | How to capture |
|--------|---------------|
| T1 sends this session | Count from send table |
| T2 sends this session | Count from send table |
| Session duration (approx.) | Note start/end time if known |
| Dedup removal rate | Contacts researched ÷ contacts skipped for prior sends |
| QA gate failures | How many emails needed revision before passing |
| Subject corrections made | Count of times Apollo auto-subject was wrong (should always be 100%) |
| JS injection retries | Count of times execCommand needed a second attempt |
| Enrollments with flags | job_change override, catchall, etc. |
| Skipped_contact_ids | From Apollo enrollment response |
| Bounces detected | From Gmail MCP or Apollo |
| Replies detected | From Gmail MCP reply check |

---

### Weekly Rollup (to run every Friday or end of week)

Pull from session logs and MASTER_SENT_LIST to generate:
- Total T1s sent MTD / WTD
- Total T2s sent MTD / WTD
- Reply rate (replies ÷ T1 sends, 14-day window)
- Bounce rate (bounces ÷ T1 sends)
- T2 coverage rate (T2s sent ÷ T1s where T2 was due)
- Accounts touched vs. accounts in TAM total
- Meetings booked (from warm-leads.md)

File: create `tamob-weekly-rollup-YYYYMMDD.md` in `/Work/memory/` when running.

---

### Log-as-You-Go Rule

**During every send session:** After each send is confirmed ("Changes saved" toast), immediately log it in the session send table before moving to the next contact. Do not batch-log at the end — the risk of missing a send or mis-recording the time is too high.

**During research/drafting sessions:** Log each contact processed (researched, drafted, held, skipped) with reason in the session log. This gives a complete picture of work done even for contacts not yet sent.

**Golden rule:** If it happened, it is logged. If it is not logged, it did not happen.

---

*Part 26 added V4.0 — Mar 11, 2026. Logging is the foundation of the feedback loop. No data = no improvement.*

