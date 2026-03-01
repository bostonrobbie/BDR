# Email Channel Operations

Operational procedures for email outreach - Apollo sequences, Gmail sends, tracking, and quality control.

---

## Email Accounts

| Account | Use |
|---------|-----|
| robert.gorham@testsigma.net | Primary send account (Apollo) |
| Apollo Email Account ID | 68f65bdf998c4c0015f3446a |

---

## Active Sequences

| Sequence | ID | Status |
|----------|----|----|
| Q1 Website Visitor - Tier 1 Intent | 69a1b3564fa5fa001152eb66 | Active |

---

## Email Send Workflow

### Pre-Send Checklist
1. Email drafted and QA-passed (all 7 Hard Constraints, MQS >= 9)
2. Subject line under 80 characters
3. Zero em dashes in message body
4. 4-6 sentences, company-specific opening
5. Low-friction CTA
6. Prospect not already in an active sequence
7. Prospect email verified (not bounce-prone)
8. Send time: 12-5 PM (afternoon window)

### Send Process (Apollo Sequence)
1. Navigate to Apollo > Sequences > [Sequence Name] > Tasks tab
2. Open prospect's task (Touch 1 email task)
3. Check activity tab - confirm no prior emails sent
4. Paste pre-written email from batch file
5. Set subject line as specified in draft
6. Send via Apollo task completion
7. Log send in email_outreach_tracker.csv

### Send Process (Gmail Direct)
1. Open Gmail compose
2. Paste pre-written email from batch file
3. Set To, Subject
4. Review for accuracy and tone (2 min max)
5. Send
6. Log send in email_outreach_tracker.csv

---

## Email Tracker Format

File: `data/trackers/email_outreach_tracker.csv`

| Column | Description |
|--------|-------------|
| date | Send date (YYYY-MM-DD) |
| prospect_name | Full name |
| company | Company name |
| title | Prospect's title |
| email | Email address |
| source | How found (website visitor, Sales Nav, referral) |
| angle | Pain hook used (maintenance, velocity, coverage, productivity) |
| personalization_level | 1-3 score |
| cta_type | Type of CTA used |
| touch_number | Which touch in sequence (1-6) |
| sequence_name | Apollo sequence name |
| status | sent, bounced, opened, replied, meeting_booked |
| reply_tag | opener, pain_hook, proof_point, timing, referral, not_interested, unknown |
| outcome | meeting_booked, not_interested, timing, referral, no_response |

---

## Catchall Domain Monitoring

These domains accept all emails but may not deliver. Monitor for engagement (opens, clicks) and be prepared for silent bounces.

Current watchlist:
- OppFi (Dawn Coen)
- Drata (Luis Sanchez)
- Epic Games (Michelle Mangio)
- Crestron (Chris Bell)
- OpSec (Ellie Ghodoosian)
- RedSail (Trent Walkup)
- Cedar Gate (Kamal Pokharel)
- FreedomPay (Jonathan Zarnosky)

---

## Excluded Contacts

| Name | Company | Reason |
|------|---------|--------|
| Pranitha Jasti | Validity Inc. | Stale email, not in sequence |
| Antony Cyriac | PTC | Hard bounce |
| Andy Roth | Teaching Strategies | Blocked by Connected stage |
| Renu Nair | - | Ownership block |

---

## Email Quality Rules

All rules from `memory/context/voice-rules.md` apply, plus these email-specific additions:

### Subject Lines
- 2-4 words preferred, max 80 characters
- Specific enough to open, not clickbaity
- Patterns that work: "[Topic] at [Company]," "[Topic], quick thought," "[Topic] at [Company], quick idea"
- Never use: "Quick question" more than once per batch, ALL CAPS, exclamation marks

### Body
- 4-6 sentences
- Company-specific opening (not generic)
- One sentence Testsigma value prop (outcome-framed, not feature-framed)
- Industry/role connection to testing pain
- Low-friction CTA
- Zero em dashes
- Sign off: "Cheers, Rob"

### Email vs InMail Differences
- Email can be slightly more direct (less intrusive channel)
- Email subject lines visible in inbox preview - optimize for curiosity
- Email allows reply threading - keep first email standalone, follow-ups can reference thread
- Email open tracking available in Apollo - use for timing follow-ups

---

## Batch Execution Process

### Batch Organization
Pre-written emails organized in `batches/email-sequences/` files by batch number.

### Execution Order
1. Start with highest priority prospects (score 5 Hot first)
2. Send in batches of 10 (avoid spam filter triggers)
3. Space sends 2-5 minutes apart
4. Complete one batch before starting next
5. Log each send immediately after sending

### Batch Schedule Template
```
Batch 1 (Prospects 1-10): [Date]
Batch 2 (Prospects 11-20): [Date]
Batch 3 (Prospects 21-30): [Date]
Batch 4 (Remaining): [Date]
```

---

## Follow-Up Sequence (Post Touch 1)

After Touch 1 email is sent via Apollo sequence:
- Apollo manages automated follow-up timing
- Touch 2 (if applicable): manual cold call
- Touch 3: Follow-up email with new angle (40-70 words)
- Monitor for opens and replies daily
- If reply received, immediately tag and handle per reply playbook

### Apollo Sequence Step Management
- Use Apollo Tasks tab to track pending actions per prospect
- Mark tasks as complete after execution
- Check for auto-generated follow-up tasks
- Adjust sequence timing if needed via Apollo UI

---

## Bounce Handling

| Bounce Type | Action |
|-------------|--------|
| Hard bounce | Remove from sequence, exclude from future batches, note in tracker |
| Soft bounce | Retry once after 48 hours, if fails again treat as hard bounce |
| Catchall (no engagement after 7 days) | Flag for review, may need alternative email or LinkedIn-only approach |

---

## Compliance and Deliverability

- CAN-SPAM compliant: business email to business contacts
- Unsubscribe: if requested, immediately remove and note in tracker
- Rate limiting: no more than 50 new emails per day per account
- Warm-up: new email accounts need 2-4 weeks of warm-up before full volume
- Domain health: monitor sender reputation, check blacklists monthly
