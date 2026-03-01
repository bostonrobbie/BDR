# Sales Playbook - Testsigma BDR Outreach

This is the full outreach playbook referenced from CLAUDE.md. It contains templates, examples, objection handling, discovery frameworks, and channel-specific guidance.

---

## Positioning Statement (internal, never say this verbatim)

Testsigma is an agentic AI test automation platform that lets teams write tests in plain English. AI creates, runs, heals, and optimizes tests across web, mobile, API, desktop, Salesforce, and SAP. We sell to QA leaders and engineering VPs who are drowning in test maintenance, slow regression cycles, or can't scale coverage with their current team.

---

## Three Pain Hooks

Every outreach message anchors to one of these three pains. Pick the one most relevant to the prospect's situation.

### 1. Flaky/Brittle Tests (Maintenance Pain)
- **Trigger signals:** Uses Selenium/Cypress/Playwright, large legacy test suites, mentions "flaky tests" in job postings
- **Core message:** Tests break every time the UI changes. Your team spends more time fixing tests than writing new ones.
- **Proof:** Hansard cut regression 8 weeks to 5 weeks with AI auto-heal. 90% maintenance reduction with self-healing.
- **Best for:** Insurance, FinServ, enterprise, teams with long regression cycles

### 2. Too Much Time Creating/Running Tests (Velocity Pain)
- **Trigger signals:** Fast release cadence, CI/CD mentions, hiring SDETs, "shift left" language
- **Core message:** Creating tests takes too long. Running them takes longer. Your pipeline is the bottleneck.
- **Proof:** CRED hit 90% regression automation, 5x faster execution. Sanofi went from 3-day regression to 80 minutes.
- **Best for:** FinTech, SaaS, any team shipping weekly+

### 3. Can't Scale Coverage (Coverage Pain)
- **Trigger signals:** Growing product portfolio, new features/acquisitions, small QA team relative to eng, multiple platforms
- **Core message:** Your product is growing faster than your test coverage. Every release is a gamble on what you didn't test.
- **Proof:** Medibuddy automated 2,500 tests, cut maintenance 50%. Nagra DTV built 2,500 tests in 8 months, 4x faster.
- **Best for:** Healthcare, media, mid-size scaling teams

---

## Multi-Channel Sequence Blueprint

### Timing
| Touch | Channel | Day | Word Target |
|-------|---------|-----|-------------|
| 1 | InMail | 1 | 70-100 |
| 2 | Cold Call | 3 | 3-line snippet |
| 3 | InMail Follow-up | 5 | 40-70 |
| 4 | Cold Call #2 | 8 | 3-line snippet (different angle) |
| 5 | Email (if available) | 10 | 70-100 |
| 6 | Break-up InMail | 15 | 30-50 |

### Sequence Rules
- Each written touch uses a DIFFERENT proof point or angle
- Touches 3-6 do NOT need full C1 structure, they can be looser
- Touch 6 never pitches, it's a respectful close-out
- Buyer Intent prospects: Touch 3 can be more direct
- No email? Skip Touch 5, adjust spacing
- Rob manually executes calls. Claude provides snippets.

---

## Objection Handling Playbook

### Pre-Mapped Objections (detect during research, pre-load response)

| Research Signal | Likely Objection | Response |
|----------------|-----------------|----------|
| Uses TOSCA, Katalon, Testim, mabl | "We already have a tool" | "Totally fair. A lot of teams we work with had [tool] too. The gap they kept hitting was [specific limitation]. Worth comparing?" |
| 50K+ employees | "Security/procurement is complex" | "We offer on-prem, private cloud, and hybrid. SOC2/ISO certified. A few Fortune 500s run us behind their firewall." |
| No dedicated QA team visible | "QA isn't a priority" | "That's actually why teams like yours use us. Plain English means devs write tests without a dedicated QA team." |
| Recently hired QA leader | "Too early, still assessing" | "Makes sense. A lot of QA leaders in their first 90 days use our free trial to benchmark what's possible before committing." |
| Pharma/healthcare/finance | "Compliance requirements" | "We work with Sanofi, Oscar Health, and several banks. Happy to walk through our compliance story." |
| Startup/small team (<200) | "Budget is tight" | "Totally get it. One company your size (Spendflo) cut manual testing 50% and saw ROI in the first quarter." |

### Live Objection Responses (for calls and replies)

**"We're happy with our current tool"**
- "That's great. What are you using?" (Then listen for gaps)
- If Selenium: "A lot of Selenium teams tell us maintenance is the pain. Is that true for you?"
- If TOSCA: "TOSCA's solid for enterprise. Where teams usually hit a wall is scripting speed. Is that an issue?"

**"Send me some info"**
- "Happy to. What specifically would be most useful - the technical architecture, a customer case study in [their vertical], or pricing?"
- Then follow up with that specific asset + a meeting ask

**"Not the right person"**
- "Totally understand. Who on your team owns test automation decisions? Happy to reach out to them directly."
- Log as referral. Reach out to referred person immediately.

**"We're too busy right now"**
- "Makes sense. Would it be useful to do a quick 15-minute intro so when timing is better, you already know what we do?"
- If no: "Got it. When would be a better time to circle back?"

**"We build our own framework"**
- "Smart. A lot of engineering teams start there. Where they usually come to us is when the maintenance of that internal framework starts eating into feature work. Is that happening yet?"

---

## Discovery Framework (BANT + Techstack)

When a prospect agrees to a meeting, Rob runs discovery. These questions adapt to what we already know.

### Budget
- "Is there a budget allocated for testing tools, or would this be a new line item?"
- "What are you spending on test maintenance today in terms of engineer time?"

### Authority
- "Who else would be involved in evaluating a tool like this?"
- "Is this something you'd own the decision on, or is there a team evaluation process?"

### Need
- "Walk me through how your team tests [specific product from research]."
- "What's your current automation stack look like?"
- "Where are regression cycles hitting hardest?"
- "If you could fix one thing about your testing process tomorrow, what would it be?"

### Timeline
- "Is there a timeline or leadership mandate driving this?"
- "When does this need to be decided by?"

### Techstack
- "What tools are you using today for test automation?"
- "How does testing fit into your CI/CD pipeline?"
- "Are you running tests in cloud, on-prem, or hybrid?"

---

## Reply Handling Playbook

Based on analysis of 1,089 prospect replies across 7 categories:

### Polite Reply (37.9% of replies)
> "Thanks for reaching out"

**Action:** Follow up with value, not more pitch. Share a relevant case study or insight. Don't ask for a meeting yet - earn it.
> "Thanks [Name] - thought this might be relevant: [Proof point matched to their world]. Happy to dig in if useful."

### Positive Reply (22.8%)
> "Interested" / "Tell me more" / "Sure, let's chat"

**Action:** Book immediately. Don't over-explain. Send a calendar link within the hour.
> "Great - here's my calendar: [link]. Would [day] at [time] work? Happy to keep it to 15 minutes."

### Negative Reply (9.4%)
> "Not interested" / "No thanks"

**Action:** Log the objection reason. Respond graciously. May re-engage 60+ days later.
> "Totally get it - appreciate the reply. If anything changes down the road, I'm here."

### Curiosity Reply (8.3%)
> "How does it work?" / "What's different about your tool?"

**Action:** Answer directly in 2-3 sentences, then bridge to meeting.
> "Good question. In short, [one-sentence explanation]. The best way to see it is a quick demo - would 15 minutes work?"

### Referral Reply (7.4%)
> "Talk to [name]" / "CC'ing [name]"

**Action:** High value. Reach out to referred person immediately. Reference the referral.
> "Hi [Referred Name], [Original Prospect] suggested I reach out. [One-line context]. Would a quick chat make sense?"

### Has Tool Reply (2.3%)
> "We use [tool]"

**Action:** Objection handle by asking about gaps, not attacking their tool.
> "Nice - [tool] is solid. Where teams usually find a gap is [specific limitation]. Is that something you've run into?"

### Timing Reply (2.1%)
> "Not right now" / "Maybe later"

**Action:** Set calendar reminder. Re-engage per trigger events.
> "Totally understand. I'll circle back in [timeframe]. In the meantime, if anything changes, feel free to ping me."

---

## Meeting Prep Framework

When status = "Meeting Booked," auto-generate a prep card from existing tracker data.

### Prep Card Contents
1. **Company snapshot** - What they do, size, key products, recent news
2. **Prospect snapshot** - Title, tenure, responsibilities, career background
3. **Known/likely tech stack** - From profile, job postings, engineering blog
4. **Pain hypothesis** - The specific testing problem from our outreach
5. **What triggered the reply** - From reply tag (opener, pain hook, proof point, timing)
6. **Discovery questions** (3-5, tailored to their situation)
7. **Relevant proof points** - 2-3 customer stories matched to their vertical
8. **Predicted objection** - Pre-mapped objection + response

### Rules
- One screen max. Rob reads it in 2 minutes before the call.
- Generated from tracker data. No new research needed.
- Include "Copy Prep" button for CRM paste.

---

## Re-Engagement Triggers

After Touch 6 break-up, prospect goes dormant. Re-engage ONLY if:

| Trigger | Approach |
|---------|----------|
| Buyer Intent reactivates | "Noticed your team's been researching..." |
| New QA job posting | "Saw [Company] is hiring for QA - figured testing might be top of mind." |
| Leadership change | Reach out to the NEW person, not old contact |
| Funding round | "Congrats on the round - scaling usually means scaling QA too." |
| Major product launch | "Saw the launch of [product]. Curious if the testing effort was painful." |
| Testsigma ships major feature | "Since we last talked, we launched [X]." |

**Rules:**
- Minimum 60 days between break-up and re-engagement
- Must have a NEW reason. Never repeat old sequence.
- Log with "Re-engaged" status and trigger reason

---

## A/B Testing Framework

### What to Test (one variable per batch, rotate)
1. Pain hook - maintenance vs. velocity angle
2. Proof point style - named customer vs. anonymous
3. Opener style - career-reference vs. company-metric
4. Ask intensity - "Would 15 minutes make sense?" vs. "Happy to share more if helpful"
5. Message length - 70-80 words (tight) vs. 100-120 words (fuller)

### Rules
- ONE variable per batch. Everything else constant.
- Split groups evenly by persona and vertical.
- Need 3+ batches on same variable to draw conclusions.
- Track variable and group in HTML tracker.

---

## Competitive Intelligence

### Selenium / Cypress / Playwright
- **Gap:** Maintenance burden. Tests break constantly. Requires coding expertise.
- **Our edge:** No-code, self-healing, 70% less maintenance
- **Proof:** 70% maintenance reduction vs Selenium

### Tricentis TOSCA
- **Gap:** Expensive, complex implementation, heavy enterprise process
- **Our edge:** Faster setup, more intuitive, comparable coverage at lower cost
- **Proof:** Teams migrate from TOSCA for speed and simplicity

### Katalon / Testim / mabl
- **Gap:** Limited scale, less enterprise-ready, narrower platform coverage
- **Our edge:** Unified platform (web + mobile + API + desktop + Salesforce + SAP), AI agents
- **Proof:** Broader coverage in single platform

### In-house Frameworks
- **Gap:** Maintenance becomes a product in itself, pulls devs from feature work
- **Our edge:** No maintenance burden, plain English, anyone can write tests
- **Proof:** Teams migrate when internal framework maintenance exceeds 30%+ of QA time
