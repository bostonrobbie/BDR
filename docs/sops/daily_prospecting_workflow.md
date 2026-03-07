# Daily High Intent Prospecting Workflow
## Maximizing Tier 1 Website Visitor Outreach Volume

**Goal:** Prospect, personalize, and send as many high intent Tier 1 emails as possible each day.
**Target throughput:** 10 to 20 new personalized Touch 1 emails per day.
**Last Updated:** March 1, 2026 (v2.0 — Apollo UI send standard, enhanced qualification checks)

---

## The Bottleneck Analysis

Based on the SOP, here is where time is spent per contact:

| Step | Manual Time | With AI Assist | Can Be Batched? |
|------|------------|----------------|-----------------|
| Identify and qualify (Apollo) | 3 min | 1 min | Yes |
| Research company | 5 to 10 min | 1 to 2 min | Yes |
| Write Touch 1 email | 5 to 8 min | Under 1 min | Yes |
| Verify email address | 1 to 2 min | Under 1 min | Yes |
| Send via Gmail | 2 min | Under 1 min | Partially |

**Manual total per contact:** ~20 min (12 contacts per 4 hour block)
**AI assisted total per contact:** ~5 min (48 contacts per 4 hour block)

The biggest leverage point is batching the research and writing steps with AI.

---

## Daily Workflow: Step by Step

### Morning Block (30 min): Prospect Identification

**Step 1: Pull website visitor data from Apollo**
Open Apollo > Visitors. Filter for:
- Pages visited: Pricing, Demo Request, Features, Comparison pages
- Company size: 200+ employees
- Geography: US (primary), then expand

**Step 2: Cross reference against existing sequences (ALL 9 CHECKS — see Master SOP Section 3)**
Before adding anyone, run the FULL qualification checklist:
- Not already in Tier 1 sequence
- Not in any other active sequence
- Not in 2+ active sequences (triple-sequencing check)
- Not Salesforce-owned by another BDR (check BOTH Apollo `owner_id` AND SF `crm_owner_id`)
- Email verified, not catchall (flag catchalls for monitoring)
- Not a duplicate contact with different owner
- Person still at the company (verify LinkedIn headline)
- No prior appointment or warm status (`inactive_reason` = "scheduled appointment", "talked on phone", "interested")
- No sequence completed within the last 30 days (30-day cooldown)
- Check `email_source` — if "emailer_message_outbound", they were previously emailed from Apollo
- Check `contact_stage_id` — if not "New", the contact has been worked before

**Step 3: Find the right persona at each company**
Use Apollo People Search with filters:
- Titles: QA Architect, Test Engineering Manager, Director of QA, Director of Engineering, VP Engineering, Sr Director QA Engineering
- Seniority: Director, VP, C Suite
- Company: matched from visitor data

**Step 4: Batch create contacts**
For any prospects not already in Apollo as contacts, create them. Record Apollo Contact IDs.

**Deliverable:** A list of 10 to 20 qualified contacts with name, title, company, email, and Apollo Contact ID.

---

### Midday Block (60 to 90 min): Research, Write, and Send

**Step 5: Batch company research with AI**
Provide the contact list to Claude (Cowork). Claude will:
1. Enrich all companies via Apollo bulk enrichment (up to 10 at a time)
2. Pull key data: industry, employee count, founding year, product description, keywords
3. Identify the unique angle for each contact (what makes their company's testing challenges specific)

**Step 6: AI writes personalized Touch 1 emails**
Claude drafts all Touch 1 emails following the SOP:
- Company specific opening (not generic)
- One sentence Testsigma value prop
- Industry/role connection to testing pain
- Low friction CTA
- Zero em dashes
- 4 to 6 sentences

**Step 7: Human review (2 min per email)**
Rob reviews each email for:
- Accuracy of company references
- Tone and natural feel
- CTA appropriateness
- Any AI tells (em dashes, buzzwords, generic phrasing)

**Step 8: Send via Apollo UI task queue (ONLY approved method)**
1. Open Apollo > Sequences > "Q1 Website Visitor - Tier 1 Intent" > Tasks tab
2. For each prospect's pending task, paste the personalized email
3. Click Complete to send
4. Apollo logs the send, tracks engagement, and queues the next touch automatically

**DO NOT** send via Gmail compose or Gmail API drafts. This was deprecated on March 1, 2026. See Master SOP Section 5 for full rationale.

---

### End of Day Block (15 min): Logging and Sequence Management

**Step 9: Update the outreach tracker**
Add all sent emails to email_outreach_tracker.csv with:
- Date, name, company, title, email, source, angle, personalization level, CTA type, touch number, sequence name

**Step 10: Add contacts to Apollo sequence**
If not already added, bulk add contacts to the Q1 Website Visitor Tier 1 Intent sequence.

**Step 11: Backup to GitHub**
Push updated files to the BDR repo:
- touch1 email drafts
- outreach tracker
- any new SOPs or workflow updates

---

## Scaling Levers

### What We Can Automate Today (with Claude in Cowork)

1. **Company research in bulk:** Apollo enrichment + AI synthesis. 10 companies in under 5 minutes.
2. **Email writing in bulk:** 10 personalized Touch 1 emails in under 10 minutes.
3. **Tracker updates:** Claude can append to the CSV directly.
4. **Apollo contact creation:** Claude can create contacts via Apollo API.
5. **Apollo sequence search:** Claude can find and reference existing sequences.
6. **Full 9-point qualification checks:** Claude can run all checks via Apollo API (sequence membership, ownership, Salesforce, email status, etc.)
7. **Engagement audits:** Claude can audit existing sequence contacts for risk factors (territory conflicts, triple-sequencing, prior appointments, job changes)
8. **Slack cross-referencing:** Claude can search Slack for team conversations about flagged contacts/companies

### What Still Requires Human Action

1. **Reviewing email drafts:** Quick scan for accuracy and tone (~2 min each).
2. **Sending via Apollo UI:** Paste personalized email into each Apollo task and click Complete. (Cannot be automated — Apollo UI is required.)
3. **Apollo website visitor review:** Identifying which visitors are high intent based on page behavior.
4. **Territory conflict resolution:** When a contact is owned by another BDR, coordinate with them before proceeding.
5. **Warm lead handling:** Contacts with "talked on phone" or "scheduled appointment" status need personalized outreach, not generic sequences.

### Future Automation Opportunities

1. **Apollo webhook for new visitors:** Auto notify when a Tier 1 company visits the site.
2. **Templated but personalized:** Build a library of industry specific angles so research time drops further.
3. **Scoring model:** Weight visitor behavior (pricing page = high, blog = low) to auto prioritize.
4. **Automated pre-send audit:** Have Claude run the full 9-point check on all pending tasks before each send session.

---

## Quick Start Checklist for Each Session with Claude

When you open a new Cowork session, give Claude:

1. "Here are today's prospects:" followed by a list of names, titles, companies, and emails
2. "Run qualification checks on all of them" (Claude runs all 9 checks via Apollo API)
3. "Write Touch 1 emails for the CLEAN contacts following the SOP"
4. "Update the tracker"
5. Then YOU send via Apollo UI — paste each email into the Apollo task queue and click Complete

Claude handles research, enrichment, qualification checks, writing, and file management. You handle review and Apollo UI send.

---

## Realistic Daily Targets

| Scenario | Contacts per Day | Time Investment |
|----------|-----------------|-----------------|
| Minimum viable | 5 | 45 min |
| Standard pace | 10 | 90 min |
| High volume day | 20 | 2.5 hours |
| Sprint (with backlog) | 30 | 3.5 hours |

These estimates assume AI handles research and writing, and Rob handles review and send.
