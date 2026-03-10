# SOP: TAM Outbound — End-to-End Process
## Version 2.0 — Updated Mar 10, 2026 (50/day rolling cadence)

This SOP governs all outreach to named TAM accounts. It is the authoritative guide for any Claude agent executing the TAM outbound process. Read this file in full before starting any TAM batch.

**Target:** 50 T1 sends per day, enrolled in TAM Outbound sequence, at highest personalization quality.
**Method:** Rolling daily batches. Account-first research (one company pass covers all contacts at that company). Continuous pipeline — no wave gating.
**Sequence:** TAM Outbound - Rob Gorham (`69afff8dc8897c0019b78c7e`) — enrollment email: `robert.gorham@testsigma.com`

---

## Overview

The TAM outbound process works accounts from a prioritized list, identifies the right contacts, researches them deeply, drafts tailored outreach, gets Rob's approval, enrolls in the Apollo TAM Outbound sequence, and follows up systematically until reply, meeting booked, or breakup.

**Scope:** All accounts in `tam-accounts-mar26.csv` (312 total) — enterprise only. No SMB or commercial.

**Apollo Sequence:** TAM Outbound - Rob Gorham (`69afff8dc8897c0019b78c7e`)
- 7 steps, all manual, 35-day cadence
- Step 1: Email T1 (Day 1) · Step 2: Email T2 (Day 5) · Step 3: LinkedIn connection request (Day 10) · Steps 4-6: Phone calls (Day 15/21/28) · Step 7: Breakup email (Day 35)
- Enrollment email: `robert.gorham@testsigma.com` (.com ONLY — never .net, .in, or .com.in)

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
- **Daily goal: 50 T1 sends enrolled in TAM Outbound sequence.** This is the target, not a hard cap — if 45 or 55 are ready, that's fine.
- Each day = one or more batch tracker files (e.g., `tamob-batch-20260310-1.html`). If a day's 50 contacts span many accounts, a single tracker file is fine. Split only if the file gets unwieldy (>60 rows).
- Tier A contacts always go in the current batch alongside Tier B/C — no separate queue.
- Do NOT hold Tier B accounts waiting for Tier A to finish. They run concurrently in the same daily batch.
- The Apollo task queue manages all follow-up for enrolled contacts. Claude only needs to draft new T1s daily and draft follow-up messages when Apollo tasks come due.

### What "50/day" means in practice
50 T1 emails sent = approximately 15-20 accounts per day at ~3 contacts/account average.

| Component | Estimated time |
|-----------|---------------|
| Account sourcing + dedup (15-20 accounts) | ~30 min |
| Account research blocks (15-20 companies × 5 min) | ~75 min |
| Contact-level LinkedIn scans (50 contacts × 2 min) | ~100 min |
| T1 + T2 draft writing (50 × ~3-4 min with shared company context) | ~150 min |
| QA gate + batch summary | ~30 min |
| **Total per session** | **~6.5 hours** |

In practice Claude does research + drafting; Rob reviews and sends. These can run async — Claude builds the batch, presents it, Rob approves and sends when ready.

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

If dedup clean: proceed. If any flag: document in batch tracker notes, ask Rob before proceeding.

---

## Part 5: Research Protocol (SMYKM-Level) — At Scale

**Efficiency principle at 50/day:** Research the ACCOUNT once, then research each CONTACT briefly. Company context is shared across all contacts at the same account — do not repeat it for each person.

### The Account Research Block (5-8 min per company — done once, covers all contacts)

**Step 1 — Apollo Org Enrichment (run once per company)**
Call `apollo_organizations_enrich` for the company domain. Extract and note:
- Tech stack (`current_technologies`) — testing tools, CI/CD tools, cloud platform
- Employee count — confirms enterprise tier, sets persona rule (Part 3)
- Funding / revenue / industry — selects proof point from Part 15 table

**Step 2 — External Research (5 min per company max)**
Check in priority order — stop when you have enough for the email:
1. LinkedIn job postings for open QA/SDET/Automation roles (signals team scaling pain — best trigger)
2. Engineering blog or tech pages (any velocity, testing culture, migration signals)
3. Recent news (product launches, acquisitions, platform expansions — implies new test coverage needed)
4. Glassdoor QA reviews (rare but high signal — mention if highly specific to their pain)

**Stop criteria:** Once you have one strong trigger (job posting OR news item OR tech signal), stop. You do NOT need all four sources if you already have a good hook.

**Account Research Output (document once, apply to all contacts at that company):**
```
Account: [Company]
Domain: [domain.com]
Industry: [vertical]
Employees: [count]
Tech stack: [Selenium / Playwright / Jenkins / etc.]
Trigger: [e.g., "3 open QA Automation Engineer roles as of Mar 10" OR "launched mobile app Jan 2026"]
Proof point (T1): [Hansard / CRED / Fortune 100 / etc.]
Proof point (T2): [rotation from Part 15]
Notes: [any special flags — Selenium-heavy, has compliance requirements, etc.]
```

### Contact-Level Research (2-3 min per person — LinkedIn only)

**Source: LinkedIn Profile (via Sales Nav)**
Find and extract ONE of:
- Role scope signal (what they own: mobile QA? API testing? platform regression? specific product area?)
- Recent post or activity (commented on testing tools, posted about a launch or a pain point)
- Tech stack signal in skills or summary (Playwright, Selenium, JIRA-first team vs. mature automation)
- Duration in role (recent hire under 6 months = building new processes = very open to tools)

**That one detail is your opener.** You do NOT need all four. One specific, role-relevant detail is more powerful than four generic facts.

**DO NOT use in messages:** years at company, education, endorsements, certifications, LinkedIn follower count, company tenure.

### Research-to-Message Mapping
| Research Finding | Feeds Into |
|------------------|-------|
| LinkedIn: QA scope (e.g., "owns mobile + API regression") | Opener — make it specific to their scope |
| Apollo: Tech stack (e.g., Selenium + Jenkins) | Challenge sentence — frame maintenance pain around their tools |
| Job posting: open QA automation roles | Theme — scaling challenge = right timing for a conversation |
| Company news: product launch or platform migration | Theme — new coverage need = natural timing |
| Engineering blog: CI pipeline pain, test flakiness posts | Proof point angle — tie proof point to their stated problem |

### Research Quality Gate (same for all batch sizes)
Before drafting any T1, confirm:
- [ ] One QA-relevant account trigger (tech stack + one external signal)
- [ ] One contact-specific detail (scope, focus area, or platform)
- [ ] Proof point assigned and matches vertical (Part 15 table)
- [ ] No duplicate with MASTER_SENT_LIST.csv

If the account trigger is missing: run Apollo org enrichment + 5-min web check.
If the contact detail is missing: do a LinkedIn profile read via Sales Nav.
Do NOT draft from title + company alone — that produces generic mail that gets ignored.

---

## Part 6: T1 — Email Only (Updated Mar 10)

**CONFIRMED: T1 is email only for TAM Outbound.** Old InMail T1 decision tree is deprecated.

Step 1 of the TAM Outbound sequence is always an email sent via Apollo (robert.gorham@testsigma.com). Old Wave 1 InMail drafts (wave1-prospecting-plan-mar9.html) are deprecated and deleted. Start fresh prospecting for all accounts.

### Enterprise Email T1 Formula

Use this for ALL email T1 sends (TAM Outbound Step 1):

**Subject:** SMYKM personal ("[Name]'s QA coverage at [Company]") OR specific problem-framed ("Testing [Company's specific platform]" or "Regression coverage for [product line]")
- NOT generic: "Quick question" "Regression eating your time" — those are SMB patterns
- Enterprise subjects are specific to THEM, not to a pain category

**Opener:** MUST use HC1-compliant SMYKM opening:
> "We have yet to be properly introduced, but I'm Rob with Testsigma."

Then immediately pivot to a QA-relevant challenge observation tied to their specific role/company. Do NOT comment on their profile, LinkedIn activity, or career history. Do NOT say "I noticed" or "I saw."

**Challenge-Narrative (2-3 sentences):**
Embed context about what their type of team typically deals with, tied to something research-verified about their company/vertical. Then bridge to proof point.
Pattern: "The challenge [type of org] hits is [specific problem]. [Customer] was dealing with the same [thing] and [outcome + Testsigma]."

**Close:**
Same "what day works" close as InMail. Tie to proof point outcome. NOT open-ended.

**Word limit:** 75-100 words body (enterprise = inbox-zero culture, shorter wins). Absolute max 120 words.

**Example structure:**
```
Subject: Seth's QA coverage at Fidelity

We have yet to be properly introduced, but I'm Rob with Testsigma.

At Fidelity's scale, financial platform updates ripple through hundreds of test cases. Most QA leaders at large institutions say test maintenance is what limits coverage growth, not headcount.

Hansard cut their regression cycle from 8 to 5 weeks with our AI self-healing. Tests fix themselves when the UI changes.

If cutting that overhead would help your team scale coverage, what day works for a quick look at how they did it?

Rob Gorham
Testsigma
```

---

## Part 7: T2 Draft Rules (Unified Email-First Formula — Updated Mar 10)

T2 sends on Day 5 from T1. Via Apollo TAM Outbound Step 2 (manual email task).

**Unified T2 Formula (4 parts, 50-70 words) — Designed from scratch for email-first sequences:**

1. **Bridge** (1 sentence): Light reference to T1 without "following up" or "circling back." Use: "One more angle from my last note." or "Different lens on the same problem." or "Thought this was worth adding."
2. **New trigger/observation** (1 sentence): Completely different angle from T1. If T1 = maintenance/self-healing, T2 = test creation speed or coverage gaps. If T1 = speed, T2 = maintenance.
3. **New proof point** (1-2 sentences): Different customer story from T1. Tie back to the new angle.
4. **Engagement question CTA** (1 sentence): NOT "what day works" — ask a qualifying question that lets them confirm their own pain. Examples: "Is test creation time or maintenance more of the pain point right now?" / "Are you mostly Selenium-based, or have you moved to something newer?"

**Rules:**
- 50-70 words
- NO "following up" / "circling back" — use bridge language above
- NO LinkedIn callback (this is email-first)
- NEW angle — different from T1 theme
- NEW proof point — do not repeat T1's customer story
- CTA = engagement question, NOT "what day works" (save meeting ask for breakup)
- No em dashes

**Proof point rotation (T1 → T2):**
- T1: Hansard (regression 8→5 weeks) → T2: CRED (90% coverage, 5x faster) or MediBuddy (50% maintenance cut)
- T1: Fortune 100 / 3x productivity → T2: Cisco (35% regression reduction) or Hansard
- T1: Nagra DTV (2,500 tests, 4x faster) → T2: CRED or MediBuddy

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
- Name, title, company, email (with ✅ verified / ⚠️ extrapolated / 🔴 unverified flag)
- LinkedIn URL
- Targeting level (Standard / Medium / High per Part 3)
- Account trigger used (one phrase — what made this company timely)
- T1 subject line
- T1 body draft
- T2 body draft
- Status: `📝 Draft Ready` / `⏳ Awaiting APPROVE SEND` / `📤 T1 Sent [date]` / `✅ Enrolled` / `↩️ Replied` / `🔴 Bounced` / `⛔ DNC`
- T1 send date (fill after send)
- T2 send date (fill after T2 send)
- Proof points used (T1 / T2)
- MASTER_SENT_LIST entry pre-formatted (copy-paste ready)
- Flags: any dedup concerns, extrapolated email warnings, ops QA concerns

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
Email verification: [N] verified / [N] extrapolated (flagged)
Credit budget: [N] InMail credits needed / [N] remaining
InMail vs Email split: [N] InMails / [N] emails

Ready for review: [link to HTML tracker file]
Reply APPROVE SEND to send all, or APPROVE SEND — [name] only, or EDIT [name] with changes.
```
3. Wait for Rob's "APPROVE SEND" (all or specific names)
4. Claude notes each name approved — never sends unapproved contacts
5. After each send (Rob executes or gives explicit authority): update MASTER_SENT_LIST.csv, update batch tracker status

---

## Part 11: Apollo Enrollment

**For contacts whose T1 was sent as InMail (outside the sequence):**
1. Add contact to Apollo (or confirm they exist as a contact)
2. Enroll in TAM Outbound - Rob Gorham (`69afff8dc8897c0019b78c7e`)
3. Email account: `robert.gorham@testsigma.com` (NOT .net or .in)
4. After enrollment: in Apollo, manually skip Step 1 (InMail was T1, already sent)
5. Step 2 manual email task will appear — due Day 5 from enrollment date

**For contacts whose T1 is email via Step 1:**
1. Enroll in TAM Outbound sequence with Step 1 as the scheduled action
2. Email account: `robert.gorham@testsigma.com`
3. Apollo flags to use: `sequence_no_email: true`, `sequence_active_in_other_campaigns: true`
4. For finished sequences: add `sequence_finished_in_other_campaigns: true`

**Enrollment timing:** Enroll immediately after T1 send (same session). Do NOT wait.

**Batch size:** Enroll max 5 contacts at a time (larger batches cause 500 errors per prior testing).

---

## Part 12: Follow-up Loop (Daily)

Run each day per `memory/sop-daily.md`. TAM-specific additions:

1. Open Apollo → TAM Outbound sequence → check "Tasks Due Today"
2. For each task due: identify contact, confirm status (no reply yet), draft message per Step rules above
3. Present draft to Rob before sending (wait for APPROVE SEND)
4. After send: log date in batch tracker HTML
5. Check Gmail for replies to `robert.gorham@testsigma.com` from any TAM contact
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
2. Click "Tasks" tab → filter by "Due Today" or "Due This Week"
3. For each task: identify the contact, look up their draft in the batch tracker HTML
4. Present draft to Rob (or confirm it's ready) → Rob gives APPROVE SEND → send
5. Mark task complete in Apollo → Apollo auto-advances the contact to the next step
6. After sending: log send date in batch tracker HTML (Status column)

**What to do if Apollo shows 0 tasks:** Either no contacts are enrolled yet, or all active contacts are between steps. Check enrolled contacts list in sequence. This is normal on Day 2-4 (between T1 and T2).

**Apollo enrollment flags for TAM Outbound:**
```
sequence_no_email: true
sequence_active_in_other_campaigns: true
sequence_finished_in_other_campaigns: true (if contact was in a prior sequence)
```
Email account: `robert.gorham@testsigma.com` (.com ONLY — not .net, .in, or .com.in)
Batch enrollment: max 5 at a time to avoid 500 errors.

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

## Part 20: Daily Batch Cadence — 50/Day Target

This is the repeating daily workflow. Run it every working day to build and execute the 50-contact batch.

### Phase 1: Account Sourcing (30 min)

**Goal:** Identify 15-20 accounts for today's batch. These accounts should yield ~50 contacts total.

1. Open `tam-coverage-tracker.csv`
2. Filter: `icp = HIGH`, `status = ✅ Untouched` — sort by employee count descending
3. Pull the next 15-20 accounts in that ordered list
4. For each: run a quick Apollo people search to estimate contact count:
   - If 1-2 QA contacts found → include (Standard targeting)
   - If 3-6 contacts → include (Medium targeting)
   - If 7+ contacts → include only the top 5-6 by seniority (High targeting) — do not include 10+ people from one company in a single batch
5. Mark each selected account in `tam-coverage-tracker.csv` as "🔄 In Progress — [date]" immediately (prevents double-claim across sessions)
6. Count estimated contacts. If under 45: pull 2-3 more accounts. If over 55: drop the last account or defer lower-seniority contacts to next day's batch.

**Checkpoint:** Target ~50 contacts sourced before moving to Phase 2.

### Phase 2: Dedup (20 min — parallel with Phase 1)

For every contact identified in Phase 1:
1. MASTER_SENT_LIST.csv check (name + company)
2. DNC list check (CLAUDE.md)
3. Apollo contact search — check `emailer_campaign_ids` and `last_activity_date`
4. Remove any flagged contacts from the batch. Replace from the same account's bench if available. If no bench, pull a new account.

**Dedup result:** Clean list of ~50 contacts, zero duplicates.

### Phase 3: Account Research Blocks (5-8 min per company — do all accounts before drafting)

Run every account through the Account Research Block (Part 5) sequentially:
1. `apollo_organizations_enrich` for domain → log tech stack + employee count + vertical
2. Quick external scan (job postings first — single Apollo or Google search) → identify 1 strong trigger

Document each account's research block in the batch tracker HTML (create the tracker file now, before drafting).

**Checkpoint:** Tracker file exists with all 50 contacts. Account research complete for all companies. No drafts yet.

### Phase 4: Contact LinkedIn Scans (2-3 min per person)

For each contact in the tracker:
1. Pull their LinkedIn profile via Sales Nav (or Apollo contact record)
2. Extract one specific detail (role scope, tech signal, recent post)
3. Add to their row in the tracker as "Contact note: [detail]"
4. Assign targeting level (Standard / Medium / High based on company contact count from Phase 1)
5. Assign proof point from Part 15 table — ensure no two contacts at the same company get the SAME proof point

**Checkpoint:** Every contact row in the tracker has: company trigger + contact detail + proof point assigned.

### Phase 5: T1 + T2 Draft Writing (150-180 min total)

Draft in account batches, not random order. Write all contacts at one company consecutively:
- Keeps the company context fresh in working memory
- Makes it easy to spot if two contacts at the same company are too similar

**Per contact (~4-5 min):**
1. Write T1 subject (SMYKM format — specific to person/company, NOT generic pain category)
2. Write T1 body (HC1 intro → challenge observation → proof point → "what day works" CTA, 75-100 words)
3. Write T2 body (bridge → new angle → new proof point → engagement question, 50-70 words)
4. Quick self-check: would this read as mass-produced if compared to the next contact at the same company? If yes, revise.

**Draft speed target:** ~4-5 min per contact including both T1 and T2 when account research is already done.

### Phase 6: Quality Gate (20-30 min for full batch of 50)

Before presenting to Rob, run the batch through the QA Gate:

**Per-message checks:**
- [ ] No "following up" / "circling back" language in T1 (HC violation)
- [ ] HC1 compliant opener: "We have yet to be properly introduced, but I'm Rob with Testsigma."
- [ ] T1 subject is person/company-specific (NOT generic pain phrase)
- [ ] T1 body 75-100 words (hard cap 120)
- [ ] T2 body 50-70 words
- [ ] T1 and T2 use different proof points
- [ ] No em dashes anywhere
- [ ] No two contacts at same company have same opener angle, same proof point, or same CTA phrasing
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

For each approved contact:
1. Rob sends T1 email via Apollo task or direct send from robert.gorham@testsigma.com
2. Claude (or Rob) enrolls contact in TAM Outbound immediately after send (same day — never defer enrollment)
3. Enrollment: batch of max 5 via `apollo_emailer_campaigns_add_contact_ids`, flags: `sequence_no_email: true`, `sequence_active_in_other_campaigns: true`
4. After enrollment: update tracker HTML row → Status = "📤 T1 Sent [date] / ✅ Enrolled"
5. Add row to MASTER_SENT_LIST.csv

**Enrollment tempo:** Enroll in batches of 5 (Apollo limit). For 50 contacts: 10 batches of 5. Takes ~10-15 min.

### Phase 9: Coverage Tracker + Session Close

After enrollment:
1. Update `tam-coverage-tracker.csv`: all enrolled accounts → "📤 In Sequence — [date]"
2. Update `memory/session/handoff.md` with today's batch count and any flagged contacts
3. Update `memory/session/work-queue.md` with next batch number
4. Git add + commit → Rob git pushes from terminal

### Daily Metrics to Track

| Metric | Target |
|--------|--------|
| New T1s sent | 50/day |
| New enrollments | 50/day |
| Accounts covered | 15-20/day |
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

*Version 2.0 — Updated Mar 10, 2026 — 50/day rolling cadence added*
*Next review: After first 250 contacts enrolled (est. 5 days at 50/day)*
