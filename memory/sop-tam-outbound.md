# SOP: TAM Outbound — End-to-End Process
## Version 1.0 — Built during Wave 1 execution (Mar 10, 2026)

This SOP governs all outreach to named TAM accounts. It is the authoritative guide for any Claude agent executing the TAM outbound process. Read this file in full before starting any TAM batch.

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

## Part 1: Wave Architecture

Accounts are processed in waves. Each wave is a cohort of accounts worked simultaneously.

| Wave | Type | Source | Count | Status |
|------|------|---------|-------|--------|
| Wave 1 | Factor accounts (HOT intent signals) | `memory/target-accounts.md` | 6 | IN PROGRESS |
| Wave 2+ | Non-Factor TAM accounts | `tam-accounts-mar26.csv` filtered by ICP=HIGH | ~130+ | NOT STARTED |

**Rules:**
- Do not start Wave 2 while Wave 1 has unresolved accounts (T1 not yet sent, or in active sequence below Day 35)
- Exception: If a Wave 1 account is permanently blocked (DNC, bounced email, wrong contact), skip it and move on
- Process accounts within a wave simultaneously — no staggering needed

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

### Non-Factor TAM Accounts (Wave 2+)
Source: `tam-accounts-mar26.csv` — read the full file, filter by:
- `icp` = HIGH (priority) or Medium (secondary)
- `status` = ✅ Untouched
- Not government, competitor, or bad data
- Enterprise size (verify via Apollo org enrichment — target 500+ employees minimum)

Order: ICP=HIGH first, then Medium. Within each tier, alphabetical by company name.

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
- Per Rob's instruction: No limit on simultaneous contacts per company
- Each message will be so tailored it won't appear mass-produced
- HOWEVER: enroll contacts in prioritized order — most senior first
- If two contacts have the same seniority: prefer QA-specific title over Engineering generic title
- Mark additional same-company contacts as "Secondary — enroll after primary's T1 is sent"

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

## Part 5: Research Protocol (SMYKM-Level)

This is not a quick skim. Enterprise contacts require real research. Set aside 5-10 minutes per person.

### Research Sources (3 required, in this order)

**Source 1: LinkedIn Profile (via Sales Nav)**
Find and extract:
- Current role scope (what they own: mobile? API? specific platform?)
- Team size signals (any "team of X" language in profile or posts)
- Recent posts or activity (have they commented on testing tools, written about CI challenges, posted about a launch?)
- Tech stack signals (framework names in skills, job descriptions mentioning Playwright, Selenium, etc.)
- Duration in role (recent hire = building new processes = openness to new tools)
DO NOT use in messages: years at company, education, endorsements, certifications

**Source 2: Apollo Org Enrichment**
Run `apollo_organizations_enrich` for the company domain. Extract:
- Tech stack (under `current_technologies`) — testing tools, CI/CD tools, cloud platform
- Employee count (confirms enterprise tier)
- Funding/revenue (context for proof point selection)
- Industry classification (use for proof point matching)

**Source 3: Company External Research**
Check in this order:
1. Company engineering blog (Substack, Medium, tech.companyblog.com) — release velocity, testing culture, recent migrations
2. Recent job postings on LinkedIn/Greenhouse — open QA/SDET roles = team scaling pain
3. Recent news (press releases, TechCrunch, CrunchBase) — product launches, acquisitions, platform migrations
4. Glassdoor QA reviews — team morale, tool pain, process complaints (rare but gold)
5. GitHub (if available) — test framework presence, contribution velocity

### Research-to-Message Mapping
| Research Finding | Feeds |
|------------------|-------|
| LinkedIn: QA scope (e.g., "owns mobile + API regression") | Opener — make it specific to their scope |
| Apollo: Tech stack (e.g., Selenium + Jenkins) | Context — frame maintenance pain with known tools |
| Job posting: "5 QA automation engineers" hiring | Theme — scaling challenge = right timing |
| Company news: "Launched new mobile app" | Theme — new coverage = regression expansion |
| Engineering blog: "our CI pipeline takes 4 hours" | Proof point angle — velocity reduction |

### Research Quality Gate
Before drafting, confirm you have:
- [ ] One QA-relevant detail from their LinkedIn (NOT just "QA Manager at X")
- [ ] Company's tech stack OR industry vertical confirmed
- [ ] One external trigger OR vertical match for theme
- [ ] Proof point selected and tied to their specific pain

If any are missing: do more research. Do not draft from title + company alone.

---

## Part 6: T1 Draft Decision Tree

```
Does the account have Tier A Factor signals (Demo or Signup)?
├── YES → Use InMail T1 (Sales Nav) if InMail credits available
│         → 80-120 words, SMYKM or problem-framed subject
│         → After send: enroll in TAM Outbound, SKIP Step 1 (already done)
└── NO → Use Email T1 via TAM Outbound Step 1
          → 75-100 words, enterprise email formula (see below)
          → Enroll in TAM Outbound, Step 1 email is the T1

InMail credits = 0?
└── Force email for ALL T1s, regardless of signal tier
```

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

## Part 7: T2 Draft Rules

T2 sends on Day 5 from T1. Via Apollo TAM Outbound Step 2 (manual email task).

**Rules:**
- 40-70 words
- NEW angle — different from T1 theme
- NEW proof point — do not repeat T1's customer story
- Light reference to T1: "Circling back quick..." or "Different angle from my last note..."
- CTA options: engagement question OR lighter "what day works" ask
- Subject: keep short (4-5 words), can reference their name or company
- Follow sop-email.md Variant A formula for full structure

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

Before writing ANY draft, create the batch tracker HTML file.

**Filename:** `wave[N]-batch[N]-tracker-[date].html`

**Required fields per contact:**
- Name, title, company, email (with verification status), LinkedIn URL
- T1 draft placeholder (type: InMail or Email)
- T2 draft placeholder
- Breakup draft placeholder
- Status: [Draft Ready / Awaiting Approval / Sent / Replied / Bounced / DNC]
- Send date (filled after send)
- MASTER_SENT_LIST entry (pre-formatted for copy-paste)
- Proof points assigned (T1 / T2)
- Any flags (⚠️ Verify email / ⚠️ Confirm prior outreach / etc.)

**MASTER_SENT_LIST entry format (new columns added Mar 10):**
```
[Full Name], [email], [Company], [Title], [Channel: LinkedIn InMail or Email], [Send Date], [B_Wave1 or Wave2_BatchN]
```

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

| # | Account | Contact | Email | T1 Type | Status |
|---|---------|---------|-------|---------|--------|
| 1 | Cboe Global Markets | Rick Brandt, Sr. Dir QA | rbrandt@cboe.com ✓ | InMail | ✅ Draft ready — clear to send |
| 2 | Fidelity Investments | Seth Drummond, VP QA | seth.drummond@fidelity.com ✓ | InMail | ✅ Draft ready — clear to send |
| 3 | JPMorgan Chase | Rose Serao, VP QA Manager | rose.serao@chase.com ⚠ extrapolated | InMail | ⚠️ Verify email before sending |
| 4 | Commvault | Brahmaiah Vallabhaneni, VP Eng | bvallabhaneni@commvault.com ✓ | InMail | ✅ Draft ready — clear to send |
| 5 | TruStage | Chamath Guneratne, IT Dir QE | chamath.guneratne@trustage.com ✓ | InMail | ⚠️ HOLD — Rob must confirm prior outreach was Shakeel's |
| 6 | YouTube/Google | US contact TBD | None verified | InMail | ❌ BLOCKED — need US Director |

**T1 drafts:** All 4 clear-to-send accounts have complete drafts in `wave1-prospecting-plan-mar9.html` (MQS 9-10/12). Drafts are InMail format, Sales Nav send.

**IMPORTANT — Sequence update:** After Wave 1 T1 sends, enroll contacts in **TAM Outbound - Rob Gorham** (`69afff8dc8897c0019b78c7e`). The old wave1-prospecting-plan-mar9.html says "LinkedIn Outbound Q1" — that is WRONG for TAM accounts. Use TAM Outbound for all Wave 1 accounts.

**Credit situation:** 4 InMail credits remaining (as of Mar 6). Wave 1 needs 6. Options:
- Option A: Send top 4 (Cboe, Fidelity, Chase, Commvault) now via InMail, wait for monthly reset for TruStage + YouTube
- Option B: Send TruStage via email (verified email exists — chamath.guneratne@trustage.com), save InMail for YouTube US contact once found
- Recommended: Option A for first 4, then reassess. Check credit reset date in Sales Nav.

**Fidelity backup contacts (same-company, defer per wave1 plan):**
- Nithya Arunkumar, Director QA — n.arunkumar@fidelity.com ✓
- Chris Pendergast, Director QA — chris.pendergast@fidelity.com ✓
- Per Rob's "no max per company" instruction: these can be enrolled AFTER Seth's T1 is sent — include in Wave 1 Batch 2

**Chase backup contact:**
- Neeraj Tati, Director SW Eng — neeraj.tati@chase.com ✓ (Engineering title, not QA — secondary persona, enroll after Rose)

**TruStage backup:**
- Maggie Redden, Dir SW Eng — maggie.redden@cunamutual.com ⚠ OLD DOMAIN (try @trustage.com pattern unverified)

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

*Created by Claude during Wave 1 execution, Mar 10, 2026. Update this file as the process evolves.*
*Next review: After Wave 1 completes (est. Apr 14, 2026 — Day 35 from first T1 send)*
