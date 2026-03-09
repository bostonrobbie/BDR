# LinkedIn Outreach SOP — Message Drafting & Research

## Scope
- This SOP is **LinkedIn-only** (InMail + LinkedIn follow-up touches).
- Do not apply this SOP to email drafting or email sends.
- Email process lives in `memory/sop-email.md` and should be run independently.

## Writing Style Rules
- **NO em dashes (—).** Use commas or short hyphens (-) only. Prefer commas.
- **Minimize hyphens.** Mid-sentence dashes are an AI signature. Replace with commas. Only use hyphens in true compound words (e.g., "self-healing"). Max 1 hyphen in message body.
- Must sound like Rob wrote it personally. Not AI-generated, not templated.
- Warm, conversational, low-pressure, specific, respectful.
- No feature dumping. Focus on a specific solution to something the prospect is already doing.
- Mobile-friendly: 80-99 words for Touch 1 (data-proven sweet spot). Max 6-8 short lines. Absolute ceiling 120 words.
- **Paragraph spacing:** Every message must have clear visual breaks. Opener, context, proof point, and close each get their own paragraph. No paragraph exceeds 3 sentences.
- **Never "show your work."** Do NOT reference LinkedIn, profiles, resume facts, or years at a company.
- No "I noticed" or "I saw" or "based on your profile." (DATA: -13.4 pp differential)
- No generic assertions like "you must be doing manual testing." Ask, don't assert.
- Simple words, short sentences, no corporate phrasing or buzzwords.
- Exactly TWO question marks in Touch 1 messages (DATA: 2 questions = 34.8% vs 23.4% for 1)
- **Close must use "what day works" pattern AND tie to the proof point.** (DATA: 40.4% vs 14.0% open-ended)
- **No easy-out lines.** No "no worries," "if not, all good."
- Do not frame anything as benefiting us. No "I want to show you."
- **No generic closes.** BANNED: "Worth comparing notes?", "Worth a quick chat?", "Would exploring that be worth your time?"

## Message Structure (C2 Style)
Every message must read like a single human idea, not three AI-generated blocks glued together.

### Pre-Draft Step 1: Single Theme Rule
State the message theme in ONE sentence: "This message is about ______."
Every sentence must support this theme. Delete anything that doesn't connect.

### Pre-Draft Step 2: QA-Relevant Research Filter
Only use research from these categories:
- **Release process signal:** frequency, stability, migrations, refreshes
- **Testing stack:** Selenium/Playwright/Cypress, CI tools, device matrix
- **QA org pressure:** hiring for QA/SDET, layoffs, team scaling, compliance
- **Integration complexity:** number of integrations, platform permutations, regulated workflows

AVOID: general revenue stats, generic "AI strategy," funding rounds, user counts — unless they directly create testing workload.

### Pre-Draft Step 3: Plain Language Pass
- Replace buzzwords: velocity→speed, bottleneck→blocker, maintenance sprawl→test upkeep, bandwidth→capacity, leverage→use
- Replace filler connectors: "That's where teams hit the wall"→cut it or say what actually happens
- Sentences under 15 words when possible. Read it out loud.

### Pre-Draft Step 4: Close Construction
Answer these 3 questions before writing the close:
1. What specific outcome did the proof point achieve?
2. What is the prospect's version of that problem?
3. How do I connect #1 to #2 and end with "what day works"?

Close patterns (rotate across batch):
- "If [outcome] would help [their situation], what day works for a quick look at how they did it?"
- "What day works to see how [customer] [achieved outcome] while [solving their problem]?"
- "If [outcome] before [their event/deadline] sounds useful, what day works for a quick look?"
- "What day works to compare how [customer] [achieved outcome] without [their constraint]?"
- "If getting [specific number] back in your [their process] would help, what day works for a quick chat?"

### Message Elements (5 parts, invisible as structure)
1. **Subject line** (3-6 words for InMail) — domain or QA-situation reference
2. **Opener** (1-2 lines) — Start with a QA situation question. Not company facts or background.
3. **Context** (1-2 lines) — One direct sentence explaining why this matters. No filler.
4. **Proof point** (0-1 lines) — ONE verified customer example with real numbers. Mention Testsigma once.
5. **Close** (1-2 lines) — Reference proof point outcome + "what day works" meeting ask.

### Anti-Pattern: "Stitched Template" Detection
Before sending, check for:
- Opener has 2+ disconnected company facts
- Context uses "That's the [noun] most [type] teams hit/feel/face"
- Proof point is interchangeable (not tied to theme)
- Close is generic or doesn't reference proof point outcome
- Close uses open-ended question instead of "what day works"
- 2+ hyphens as mid-sentence dashes
- No paragraph breaks between sections

## 3-Touch Multi-Channel Sequence (Updated Mar 8, 2026)

Every prospect gets 3 touches across 2 channels:

**Day 1 — Touch 1 (LinkedIn InMail):** Full 5-element message, 80-120 words. Costs 1 InMail credit for 2nd/3rd degree.
**Day 5 — Touch 2 (Email):** 60-90 words. Uses locked Variant A formula (approved Mar 9, 2026). 5-part structure: opening company fact → "I'd imagine..." empathy bridge → LinkedIn callback naming the T1 topic → customer story + tie-back → engagement CTA tied to opening tension. NOT a meeting ask in T2. Full formula, examples, and hard rules: `memory/sop-email.md`.
**Day 10 — Touch 3 (LinkedIn Connection Request):** Short note, 200-250 chars max. Goal is to get accepted (1st degree) — not to pitch. See Connection Request rules below.

Rules:
- Each touch uses a DIFFERENT proof point/angle
- T2 email DOES reference the T1 LinkedIn topic — via the LinkedIn callback (Part 3 of Variant A). The callback names the T1 topic, explains the channel switch, and creates continuity across touches. This is intentional.
- T2 CTA is an engagement question tied to the opening tension. Meeting ask is reserved for T3 or after a reply.
- T3 connection request is a relationship move, NOT another sales ask
- No break-up message
- Sequence lives in Apollo: "LinkedIn Outbound - Q1 Priority Accounts" (steps 1-3)
- See `memory/sop-email.md` for full T2 email drafting rules (Variant A formula)

### Why Email for T2 (not a second InMail)
InMail T2s cost 1 credit each for 2nd/3rd degree prospects (confirmed via live testing Mar 8). With limited credits (reset monthly), using them for T2 follow-ups has poor ROI. Email is free, multi-channel lift is +37% per Gong data, and T2 email response rates are well-documented. Credits are reserved for fresh T1 InMails to new prospects.

### Touch 3 — LinkedIn Connection Request Rules
- **Limit: 200-250 characters** (under the 300 char hard limit, leaves buffer)
- **Tone: warm, human, not salesy** — the goal is to get accepted, nothing else
- **Do NOT repeat the pitch** — they've seen it in T1 and T2
- **Do NOT reference your previous messages explicitly** ("I sent you an InMail..." = awkward)
- **Light callback is fine:** a brief nod to the topic, not a rehash
- Once accepted: they become 1st degree, future DMs are FREE

**Connection request note template patterns:**
- "Hi [First], been following [Company]'s work in [relevant space] — thought it made sense to connect. Rob"
- "Hi [First], reached out about QA automation a couple weeks back. Either way, good to be connected. Rob"
- "Hi [First], [Company]'s [relevant initiative/product] caught my attention — would love to stay connected. Rob"

## InMail Credit Mechanics — Reference (Mar 8, 2026)

T2 InMails are no longer the active strategy (see 3-Touch Sequence above). This section is kept for reference on InMail credit rules when sending T1s or any future InMails.

### Credit Cost by Degree
| Connection Degree | Reply Box Shows | Cost |
|-------------------|-----------------|------|
| **1st degree** (connected) | "Type your message here..." | **FREE** |
| **2nd or 3rd degree** (not connected) | "New InMail / Use 1 of X credits" | **1 credit** |

This applies even inside an existing thread. Degree determines cost — thread history does not.

### Checking Degree Before Sending
1. Sales Navigator → Messages (Inbox)
2. Search by first name (full name sometimes fails)
3. Open thread → check right panel for "· 1st", "· 2nd", or "· 3rd" next to their name
4. Reply box label confirms cost

### Credit Strategy
Reserve InMail credits for fresh T1 outreach to new prospects. Do not spend credits on T2 follow-ups — use email instead (free, multi-channel lift). Credits reset monthly.

## Research Requirements (3 Sources Per Prospect)

### Source 1: LinkedIn Profile (Sales Navigator)
Extract: QA scope, team signals, tech stack clues, pain signals in their posts. 
Do NOT use in messages: years at company, education, certifications, endorsement counts.

### Source 2: Apollo Enrichment
Extract: Tech stack, company size, industry, funding, verified email.
Use for: proof point matching, objection mapping, multi-channel sequence.

### Source 3: Company External Research
From: product pages, engineering blog, job postings, press releases, news, Glassdoor reviews.
Extract: Release process, testing stack evidence, QA hiring, integration complexity, recent events.
NOT just LinkedIn company page.

### Research-to-Message Pipeline
1. LinkedIn → identifies person's QA scope → feeds **opener**
2. Apollo → confirms tech stack, industry → feeds **proof point selection** and **objection mapping**
3. Company research → QA-relevant events → feeds **context** and **theme**
4. All combined → feeds **close construction**

Tag each research bullet with which message element it feeds.

## Qualification Checklist
- [ ] Manager+ seniority
- [ ] ICP title match
- [ ] No prior interaction in Sales Navigator
- [ ] US-based
- [ ] Software QA/engineering (not pharma manufacturing, biotech lab QA)
- [ ] Company has software products to test
- [ ] Profile URL captured and logged

## Deliverable Format
Single HTML file with: prospect tracker table (sorted by priority), individual prospect cards with copy-paste messages for all touches, "Copy Message" and "Copy Subject" buttons, predicted objection + response, status dropdowns, reply tags, A/B groups, personalization scores, priority scores, color-coded badges, priority filter.

Filename: `prospect-outreach-[batch#]-[date].html`


## LinkedIn Live Send Procedure (Manual)
1. Open Sales Navigator profile from tracker.
2. Run dedup check using composer-first method (blank "New message" = clean).
3. Verify identity: name/title/company alignment.
4. Paste approved InMail exactly, preserving paragraph breaks.
5. Run final QA (2 question marks, no placeholders, CTA present).
6. Pause for explicit approval before any send action.
7. After send, log status + date + conversation URL in LinkedIn tracker.

## Apollo + Local DB Update Procedure (Required)
Every LinkedIn touch must be logged in BOTH systems so sequence context and reporting stay aligned:

1. **Apollo update (campaign context + ownership visibility)**
   - Update contact status/disposition in Apollo after each LinkedIn touch.
   - Add note for outcome (sent, replied, no-response, do-not-contact, role mismatch).
   - If contact should move to email sequence, queue/assign that next action in Apollo.
2. **Local DB update (channel analytics + audit trail)**
   - Record LinkedIn touch in local DB with channel=`linkedin` and touch number.
   - Update message draft/touch state (`drafted`/`sent`/`replied`/`blocked`).
   - Log reply intent and attribution when replies come in.
   - Append activity timeline entry for each send/reply/disposition action.

### Minimum fields to track per LinkedIn touch
- contact identifier (id + linkedin_url)
- channel (`linkedin`)
- touch number
- message/draft id
- state (`drafted`/`sent`/`replied`/`blocked`)
- timestamp
- Apollo note/disposition reference
- owner/operator
- next action + due date

### Reconciliation check (end of run)
- LinkedIn sends/replies in tracker == Local LinkedIn DB touch/reply logs.
- Apollo disposition notes exist for every completed LinkedIn send.
- Any mismatch is flagged as `sync_gap` and fixed before run close.

## Data & Tracking (LinkedIn DB)
LinkedIn records are isolated in the LinkedIn database:
- **DB path:** `api/data/outreach_linkedin.db`
- Typical objects to audit: contacts, message drafts, touchpoints, replies, activity timeline
- Keep LinkedIn operational metrics and logs in this channel DB only

If database bootstrap/reset is needed, run:
```bash
python scripts/init_isolated_channel_dbs.py \
  --source api/data/outreach_seed.db \
  --email-db api/data/outreach_email.db \
  --linkedin-db api/data/outreach_linkedin.db
```

## No-Apollo-Match Handling

When Apollo bulk_match returns `null` or no result for a prospect:

1. **Do NOT skip the prospect** — still include them if web research supports their ICP fit.
2. **Web research only:** Use LinkedIn profile + company external research for 3-source requirement. Document the gap explicitly.
3. **Flag in the HTML tracker:** Add `"flagged": True` and a warning note: "⚠️ NO APOLLO MATCH — verify identity + email via Module A2 before send."
4. **Score MQS conservatively:** Cap at 9/12 since tech stack and email can't be confirmed without Apollo.
5. **Module A2 is mandatory at send time:** Because email can't be verified ahead of time, the composer check is critical. If the profile can't be found on Sales Nav, route to email outreach only if a verified email exists.
6. **Log the gap:** Note "no Apollo match" in research notes field of the tracker.

**Root cause note (Mar 6):** Kristyn Burke (Kahuna) and Guna Chandrasekaran (FloQast) returned no Apollo match. Likely causes: uncommon name variants, recently changed employer, or contact not in Apollo database. Both included in Batch 10 with full ⚠️ flags.

---

## Same-Company Conflict Resolution

When the pre-batch dedup scan finds 2+ people from the same company, resolve autonomously using this tiebreaker hierarchy (do NOT pause to ask Rob unless truly ambiguous):

1. **Higher priority score wins.** P4 beats P3, P3 beats P2, etc.
2. **If same priority: QA manager/lead beats SDET.** Primary persona > influencer persona.
3. **If still tied: confirmed Apollo email wins.** Email mismatch (wrong domain) = defer.
4. **Deferred contacts:** Document them in the batch tracker's Deferred section with reason. They become candidates for the next batch or a future Touch 2/3 window.

**Special case — Terene Lee rule (Mar 6):** If the deferred person is in a later stage of the sequence (needs Touch 2/3 while the included person is getting Touch 1), note this explicitly: "Needs Touch [X] — schedule in next batch."

**Document all deferrals** in `memory/pipeline-state.md` under the batch's migration/dedup notes.

---

## Common Pitfalls
- Don't send messages (Rob copy/pastes manually)
- Don't update only Apollo or only local DB, both must be updated each touch
- NEVER write "I noticed" or "I saw" in ANY message
- Don't include 2+ prospects from same company per batch
- Don't use VPs/C-level without strong signal (11.9% / 9.1% reply rates)
- Don't use "300% faster" (16.3% rate). Use reduction framing ("40% fewer bugs" = 39.2%)
- Don't use "flaky tests" as hook (16.8% rate). Use "test maintenance" (+9.0 pp)
- Don't send after 6 PM (12.1%) or on Mondays (22.9%)
- Don't write generic closes (14.0%). Always "what day works" (40.4%)
- Do prioritize Architects (39.3%) and Manager/Leads (26.8%)
- Do send at lunch 12-1 PM local (56.5%)
- Do send on Thursdays (42.1%)
