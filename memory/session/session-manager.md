# Session Manager

This file defines how every Claude session with Rob should start, what context to load, and how to route into the right workflow. Read this first at the beginning of every session.

---

## Session Startup Checklist

When a new session begins, Claude should:

### 1. Identify Session Type
Ask Rob what he's working on today, or infer from his first message. Route to the appropriate workflow below.

### 2. Load Context
Read these files in order of relevance to the session type:
- **Always:** `CLAUDE.md` (primary brain), `memory/context/voice-rules.md`
- **Prospecting:** `memory/context/integrations.md`, `memory/ops/prospecting-checklist.md`
- **Writing/Drafting:** `memory/context/gold-standards.md`, `memory/context/sales-playbook.md`
- **Batch Building:** All of the above + previous batch files in `batches/`
- **Analytics/Review:** `analytics/linkedin-analysis/analysis_output.json`, `data/trackers/`
- **Email Ops:** `memory/ops/email-channel-ops.md`, `docs/sops/email_send_execution_plan.md`

### 3. Check State
- What batch number are we on? Check `batches/` for latest.
- Any previous batch files to read for pre-brief? If yes, generate pre-brief first.
- Any tracker updates to review? Check `data/trackers/email_outreach_tracker.csv`
- Any pending follow-ups or re-engagement triggers?

---

## Session Types and Workflows

### Type 1: New Batch Build (LinkedIn)
**Trigger:** "Let's build a new batch" or "I have new prospects"

**Workflow:**
1. Read all previous batch files, generate Pre-Brief (5-line "What's Working" summary)
2. Present Pre-Brief to Rob
3. Receive prospect list from Rob (from Sales Navigator)
4. For each prospect:
   a. Research company (2 sources: LinkedIn + external)
   b. Research person (LinkedIn profile)
   c. Score ICP fit and calculate priority (1-5)
   d. Assign A/B group (one variable per batch)
   e. Draft all 6 touches (InMail, Call, Follow-up, Call, Email, Break-up)
   f. Score each message (MQS 12-point system)
   g. Pre-map most likely objection
5. Run QA Gate on all messages
6. Generate HTML deliverable
7. Save to `batches/` directory
8. Push to GitHub

### Type 2: Email Prospecting (Website Visitors)
**Trigger:** "Let's do website visitors" or "Apollo visitors" or "email batch"

**Workflow:**
1. Pull website visitor data from Apollo
2. Qualify and filter prospects (see prospecting checklist)
3. Find right persona at each company
4. Batch company research via Apollo enrichment
5. Write personalized Touch 1 emails following voice rules
6. Run QA Gate
7. Present to Rob for review
8. Update email_outreach_tracker.csv
9. Add contacts to Apollo sequence if needed
10. Push to GitHub

### Type 3: Message Writing/Editing
**Trigger:** "Write messages for..." or "Draft emails for..." or provides prospect names

**Workflow:**
1. Load voice rules and gold standards
2. Research each prospect (if not already done)
3. Draft messages following C1 framework
4. Score each message (MQS)
5. Run QA Gate (all 7 Hard Constraints)
6. Present to Rob with scores and breakdowns
7. Iterate based on feedback

### Type 4: Reply Handling
**Trigger:** "Got a reply from..." or "[Name] replied"

**Workflow:**
1. Identify reply type (polite, positive, negative, curiosity, referral, has tool, timing)
2. Tag what triggered the reply (opener, pain hook, proof point, timing, referral)
3. Draft response following reply handling playbook
4. If positive: prepare meeting booking and prep card
5. If referral: draft outreach to referred person
6. If negative: log objection, note for 60+ day re-engagement
7. Update tracker

### Type 5: Call Prep
**Trigger:** "I'm calling..." or "Prep me for calls"

**Workflow:**
1. Generate 3-line call snippet per prospect
2. Ensure different pain hypothesis and proof point than InMail touches
3. If prospect has replied before, note what resonated
4. Present as quick-glance cheat sheet

### Type 6: Meeting Prep
**Trigger:** "Meeting with [Name] tomorrow" or status changed to "Meeting Booked"

**Workflow:**
1. Generate full prep card from tracker data
2. Company snapshot, prospect snapshot, tech stack, pain hypothesis
3. What triggered the reply
4. 3-5 tailored discovery questions
5. 2-3 relevant proof points with numbers
6. Predicted objection + response
7. Present as one-screen summary

### Type 7: Analytics/Review
**Trigger:** "How are we doing?" or "What's working?" or "Show me the numbers"

**Workflow:**
1. Read all batch files and tracker data
2. Generate analytics summary:
   - Reply rate by persona type
   - Reply rate by vertical
   - Reply rate by proof point
   - Reply rate by personalization score
   - A/B test results
3. If 3+ batches exist, offer to generate full dashboard HTML
4. Recommend adjustments for next batch

### Type 8: Tracker Update
**Trigger:** "Update the tracker" or "Log these sends"

**Workflow:**
1. Get details from Rob (who was sent, when, what channel, outcome)
2. Update email_outreach_tracker.csv
3. Update prospect status in relevant batch files
4. Push to GitHub

### Type 9: Research Only
**Trigger:** "Research [Company]" or "What can you find on [Name]?"

**Workflow:**
1. Company research from external sources (website, news, engineering blog, job postings)
2. Person research from LinkedIn profile
3. Identify testing pain hypothesis
4. Note any trigger signals (funding, hiring, product launches)
5. Present structured research notes

---

## Pre-Brief Template

Generated before every new batch from accumulated data across all previous batches.

```
## Pre-Brief: Batch [N] | [Date]

1. **Best persona:** [Which title/level is replying most]
2. **Best proof point:** [Which customer story is in most replied-to messages]
3. **Best vertical:** [Which industry is warmest]
4. **Best pattern:** [Any opener/ask/length pattern standing out]
5. **Stop doing:** [One thing to drop or change]

Data basis: [X] batches, [Y] prospects, [Z] replies tracked.
```

If no previous batch data exists, use defaults from CLAUDE.md Outbound Intelligence System.

---

## Session Closing Checklist

Before ending any session:
1. All files saved and up to date
2. Trackers updated with any new sends or status changes
3. Changes committed to GitHub with clear message
4. Push to appropriate branch
5. Summarize what was accomplished and what's pending

---

## Quick Reference: File Locations

| What | Where |
|------|-------|
| Primary brain | `CLAUDE.md` |
| Voice rules | `memory/context/voice-rules.md` |
| Sales playbook | `memory/context/sales-playbook.md` |
| Gold standards | `memory/context/gold-standards.md` |
| Integrations | `memory/context/integrations.md` |
| Session manager | `memory/session/session-manager.md` |
| Prospecting checklist | `memory/ops/prospecting-checklist.md` |
| Email ops | `memory/ops/email-channel-ops.md` |
| Scoring weights | `config/scoring_weights.json` |
| Vertical pains | `config/vertical_pains.json` |
| Proof points | `config/product_config.json` |
| Analysis data | `analytics/linkedin-analysis/analysis_output.json` |
| Email tracker | `data/trackers/email_outreach_tracker.csv` |
| Batch deliverables | `batches/` |
| SOPs | `docs/sops/` |
