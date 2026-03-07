# LinkedIn & Email Outreach SOP v4

Extracted from operational SOP documents. This is the canonical reference for day-to-day outreach execution.

---

## Overview

Rob runs multi-channel outbound across LinkedIn InMail, email, and cold calls to book meetings with QA and engineering leaders for Testsigma. Claude handles research, drafting, QA, and analytics. Rob handles review, editing, and manual execution.

---

## Channel Priority

1. **LinkedIn InMail** - Primary channel. Higher visibility, lower volume.
2. **Email** - Secondary channel. Higher volume, more direct.
3. **Cold Call** - Supplementary. Best for hot/warm prospects.

---

## Daily Workflow

### Morning Block (30 min): Prospect Identification

**Step 1: Pull prospect data**
- LinkedIn batches: Sales Navigator saved searches, "Show new results"
- Email batches: Apollo > Visitors > filter high-intent pages

**Step 2: Cross-reference**
- Not already in active sequence (Apollo or Sales Nav)
- Not contacted in last 30 days
- Not in another BDR's territory

**Step 3: Find right persona**
- Titles: QA Architect, Test Engineering Manager, Director of QA, Director of Engineering, VP Engineering, Sr Director QA Engineering
- Seniority: Director+
- Match to visitor company

**Step 4: Batch create contacts**
- Create in Apollo if not existing
- Record Contact IDs
- Deliverable: 10-20 qualified contacts

### Midday Block (60-90 min): Research, Write, Send

**Step 5: Batch company research with AI**
- Enrich via Apollo bulk enrichment (up to 10 at a time)
- Pull: industry, employee count, founding year, product description, keywords
- Identify unique angle per contact

**Step 6: AI writes personalized Touch 1**
- Company-specific opening (not generic)
- One sentence Testsigma value prop
- Industry/role connection to testing pain
- Low-friction CTA
- Zero em dashes, 4-6 sentences

**Step 7: Human review (2 min per email)**
- Accuracy of company references
- Tone and natural feel
- CTA appropriateness
- AI tells (em dashes, buzzwords, generic phrasing)

**Step 8: Send**
- Email: paste into Gmail or complete Apollo task
- InMail: paste into LinkedIn compose
- Log every send

### End of Day Block (15 min): Logging

**Step 9: Update trackers**
- email_outreach_tracker.csv
- Prospect status in batch files

**Step 10: Add to Apollo sequence**
- Bulk add if not already in sequence

**Step 11: Push to GitHub**
- Email drafts, tracker updates, workflow changes

---

## InMail-Specific Rules

### Sending
- Rob copies from deliverable, pastes into LinkedIn InMail compose
- One InMail at a time (no bulk send)
- Afternoon window (12-5 PM)
- Space sends 5+ minutes apart

### Character Limits
- InMail body: 600 characters max
- InMail subject: optional but recommended (2-4 words)

### Follow-up Timing
- Touch 1: Day 1
- Touch 3 (follow-up): Day 5
- Touch 6 (break-up): Day 15

### Tracking
- Log in Sales Navigator interaction history
- Note in batch tracker (status dropdown)
- Tag replies when received

---

## Email-Specific Rules

### Sending
- Via Apollo sequence task completion (preferred) or Gmail manual
- Send from: robert.gorham@testsigma.net
- Afternoon window (12-5 PM)
- Max 50 per day per account

### Character Limits
- Email body: 1200 characters max
- Subject line: 80 characters max

### Follow-up Timing (Apollo-managed)
- Touch 1: Day 1
- Touch 3: Day 5 (if not via InMail)
- Touch 5: Day 10

### Tracking
- email_outreach_tracker.csv
- Apollo sequence dashboard
- Tag replies and outcomes

---

## Cold Call Rules

### Preparation
- Claude generates 3-line call snippet per prospect
- Different angle and proof point than written touches
- Rob glances at snippet before dialing

### Best Call Windows
- Morning: 8-11 AM PT
- Afternoon: 3-6 PM PT
- Avoid: lunch hour (11 AM - 1 PM), Friday afternoons

### Call Snippet Format
```
Opener: "Hey [Name], this is Rob from Testsigma - [personalized hook]."
Pain: "[Specific testing problem tied to context]."
Bridge: "We helped [proof point]. Worth 60 seconds to see if it's relevant?"
```

### Call Outcomes to Log
- Connected: had conversation (note outcome)
- Voicemail: left message (note what was said)
- No answer: no VM left
- Gatekeeper: spoke to someone else (note who)
- Callback requested: schedule follow-up

---

## Scaling Levers

### What Claude Automates Today
1. Company research in bulk (Apollo enrichment + synthesis, 10 companies in 5 min)
2. Email writing in bulk (10 personalized emails in 10 min)
3. Tracker updates (append to CSV directly)
4. Apollo contact creation (via API)
5. Apollo sequence search (via API)

### What Still Requires Rob
1. Reviewing email drafts (2 min each)
2. Sending from Gmail/LinkedIn (click send)
3. Apollo website visitor review (judging intent from page behavior)
4. Territory checks (confirming no BDR overlap)

### Future Automation
1. Gmail draft creation via API (pre-populate drafts)
2. Apollo webhook for new visitors (auto-notify on Tier 1 visit)
3. Industry-specific angle library (reduce research time)
4. Scoring model for visitor behavior (pricing page = high, blog = low)

---

## Quality Gates

### Before Any Message Is Sent
1. Zero Hard Constraint violations (all 7 checked)
2. MQS >= 9/12
3. Under 100 words (120 absolute max)
4. At least one question mark
5. No structural duplicates in batch
6. Every personalization claim backed by research
7. Angle differs from previous touches for same prospect

### Before Any Batch Is Presented
1. Rule violation scan on every message
2. MQS computed with full breakdown
3. Only messages scoring >= 9/12 presented
4. Structural dedup across batch
5. Evidence check on all personalization
6. Angle rotation verified per prospect

---

## Batch File Naming

- LinkedIn batches: `prospect-outreach-[batch#]-[date].html`
- Email sequences: `touch1_batch[#]_emails.md`
- Hyper-personalized: `hyper_personalized_touch1_emails.md`
- Website visitor: `website_visitor_sequence_drafts.md`

---

## Metrics to Track

| Metric | Target | Current Baseline |
|--------|--------|-----------------|
| Email reply rate | > 1.5% | ~1% |
| QA persona reply rate | > 1.4% | ~1.4% |
| VP Eng reply rate | > 0.8% | ~0.5% |
| Touches before reply | 3-5 | 2.47 avg |
| Messages per day | 10-20 | varies |
| Meeting conversion | > 40% | tracking |
| MQS average | >= 10 | tracking |
