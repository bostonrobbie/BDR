# Reply Classifier — Gmail Reply Check & Classification

## Description
Checks Gmail for new replies to robert.gorham@testsigma.com, classifies each one by type, updates `memory/warm-leads.md` and `memory/contact-lifecycle.md`, and surfaces priority items for Rob. Designed to run at session start and on-demand. The scheduled version runs every 2 hours on weekdays.

## Trigger
- Run at START of every session (referenced in `skills/session-start/SKILL.md` Phase 5)
- Scheduled: weekdays 9am, 11am, 1pm, 3pm, 5pm (taskId: `reply-classifier`)
- Run on-demand: "check replies", "any warm leads?", "inbox check"

## ⛔ APPROVE SEND RULE
This skill is READ-ONLY. It classifies replies and drafts suggested responses. It does NOT send anything. All drafted responses must be reviewed and approved by Rob before sending. Claude drafts, Rob approves, Rob sends via Apollo UI. NEVER use Gmail MCP to send outreach.

---

## Step 1: Fetch New Replies

```
Tool: gmail_search_messages
q: "to:robert.gorham@testsigma.com newer_than:2d"
maxResults: 50
```

Also check unread:
```
Tool: gmail_search_messages
q: "to:robert.gorham@testsigma.com is:unread"
maxResults: 20
```

For each message, read the thread:
```
Tool: gmail_read_thread
threadId: {thread_id}
```

Extract: sender name + email, company (from domain or signature), original outreach message for context, reply content, timestamp.

Cross-reference sender against `MASTER_SENT_LIST.csv` to identify which batch/touch this reply is from.

---

## Step 2: Classify Each Reply

Apply these signal patterns in order:

**P0 — Positive (wants meeting or is genuinely interested)**
- Contains: "meeting", "schedule", "calendar", "demo", "call", "chat", "talk", "discuss"
- Contains: "interested", "tell me more", "sounds good", "let's connect"
- Specific day/time: "Tuesday works", "next week works", "send me a time"
- Asks a product question: "how does it handle...", "does it work with..."

**P0 — Curiosity (engaged, not yet committing to meeting)**
- "how does", "what is", "can it", "does it support", "what's the difference"
- "pricing", "cost", "compared to X"

**P1 — Referral (pointing to someone else)**
- "reach out to", "talk to", "contact", "you should speak with", "cc'd", "looping in"
- "better person", "right person", "handles that", "not my area"
- New email address appears in body that wasn't the original recipient

**P2 — Timing objection (not now, but not a no)**
- "not right now", "maybe later", "next quarter", "revisit in", "circle back"
- "busy with", "in the middle of", "wrapping up", "after we finish"
- Response time: log re-engagement date

**P2 — Polite acknowledgment (soft reply, no clear next step)**
- Short reply (<20 words), "thanks", "thank you", "appreciate the outreach"
- No question asked, no next step. If this follows T1, draft T2 with new angle.

**P3 — Has a tool (using a competitor)**
- Tool names: selenium, playwright, cypress, testcomplete, katalon, tricentis, browserstack, sauce labs, mabl, applitools, perfecto, qtest, zephyr, tosca
- "we already use", "we have X", "happy with our current", "we're set"

**P3 — Negative (explicit decline)**
- "not interested", "no thanks", "please remove", "unsubscribe", "stop emailing", "don't contact"
- Hostile tone
- Explicit decline → recommend DNC addition to Rob (Rob must approve any DNC change)

**P4 — OOO / Auto-reply**
- "out of office", "OOO", "away from", "returning on", "auto-reply", "automatic reply", "on leave", "on vacation"
- Extract return date if stated

**P4 — Bounce / Delivery failure**
- "undeliverable", "bounced", "not found", "mailbox full", "address rejected", "SMTP 550"

---

## Step 3: Action Per Category

**P0 Positive — Immediate:**
1. Add/update entry in `memory/warm-leads.md` with full details (name, company, email, reply snippet, date, which touch triggered it)
2. Update `memory/contact-lifecycle.md` stage to T1_REPLIED or T2_REPLIED
3. Surface to Rob: "🔥 WARM LEAD: [Name] at [Company] replied with interest. Here's what they said: '[first 80 chars]'. Draft a response?"
4. Do NOT draft or send without Rob's go-ahead.

Real examples for reference:
- Namita Jain (OverDrive) — P1 warm inbound (webinar engagement x2). T1 sent Feb 27. Currently monitoring.
- Pallavi Sheshadri (Origami Risk) — Replied to premature Touch 3 (INC-001 incident). Rob sent manual follow-up Mar 2.

**P1 Referral — Same day:**
1. Extract referred person's name and contact info
2. Add referral entry to `memory/warm-leads.md`
3. Research referred person via Apollo: `apollo_contacts_search` q_keywords="{name} {company}"
4. Draft: (a) thank-you reply to referrer (1-2 lines), (b) outreach to referred person mentioning referrer
5. Present BOTH drafts to Rob for approval. Do NOT send.

**P2 Timing — Log and schedule:**
1. Log in `memory/warm-leads.md` with expected re-engagement date
2. Add task to `memory/session/work-queue.md`: "Re-engage [Name] after [date] — timing objection"
3. Tell Rob: "⏰ TIMING: [Name] at [Company] says '[summary]'. Re-engage after [date]. Logged."

**P2 Polite — Follow up:**
1. Identify which touch number this was (from MASTER_SENT_LIST)
2. If T1 reply → note that T2 is due (check timing: not before Day 4 from T1)
3. Update `contact-lifecycle.md` stage

**P3 Has Tool — Objection handling:**
1. Identify the tool mentioned
2. Pull relevant doc from Google Drive:
   - Competitor comparisons: `1yFYzrb1FdCOzI9FoVcN2MyfI_vfLOqGy-79SLgjJ0Kc`
   - Product objections: `1EDmrZO9ZK1rpYTMlZD1oL2DxtZIYrJY3UO9B_MRQkJU`
3. Draft objection-handling response using the battle card for that tool
4. Present to Rob for review. Do NOT send.

**P3 Negative — Log and recommend:**
1. Tell Rob: "❌ DECLINE: [Name] at [Company] — '[summary]'. Recommend DNC addition?"
2. Wait for Rob's explicit yes before modifying `CLAUDE.md` DNC list
3. If explicit removal request, note urgency

**P4 OOO — Auto-log:**
1. Extract return date if available ("returning [date]")
2. Log: "📅 OOO: [Name] returning [date]. Next touch after [date]."
3. Note in `contact-lifecycle.md` if contact has a record

**P4 Bounce:**
1. Flag email as bad in `contact-lifecycle.md`
2. Search Apollo for alternate email: `apollo_contacts_search` q_keywords="{name} {company}"
3. Log: "📪 BOUNCE: [Name] at [Company] — [email] invalid. Alternate: [if found]"
4. If SMTP 550 hard bounce and enrolled in Apollo sequence → tell Rob to remove from sequence manually

---

## Step 4: Summary Report

```
📬 REPLY CHECK — Mar 12, 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 P0 — IMMEDIATE (1)
  • Seth Drummond @ Northern Trust — Positive — "Tuesday works, send me a calendar link"

📬 P1 — SAME DAY (1)
  • Nithya Arunkumar @ Fidelity — Referral to Chris Pendergast (pendergast@fidelity.com)

⏰ P2 — FOLLOW UP (2)
  • Jason Lieberman @ Epicor — Timing — "circling back after Q1 planning"
  • Les Stickney @ Epicor — Polite ack — "thanks for reaching out"

📋 P3 — REVIEW (1)
  • Holly Shubaly @ Epicor — Has tool — "we use Playwright, happy with it"

📅 P4 — AUTO (2)
  • Mike Chen @ BeyondTrust — OOO returning Mar 18
  • Dan Ramos @ Jack Henry — Bounce (SMTP 550)

Total: 7 new replies | 2 require immediate action | 5 logged
```

---

## Scheduled Task Config
```
taskId: reply-classifier
cronExpression: "0 9,11,13,15,17 * * 1-5"
description: "Check Gmail for new replies every 2 hours on weekdays, classify and surface warm leads"
```

---

## Output Files Updated
- `memory/warm-leads.md` — append new P0/P1 entries
- `memory/contact-lifecycle.md` — update stage for replied contacts
- `memory/session/work-queue.md` — add follow-up tasks for P2/P3

## Safety Rules
- ⛔ NEVER send any reply. READ-ONLY via Gmail MCP.
- ⛔ NEVER modify DNC list in `CLAUDE.md` without Rob's explicit approval
- All drafted responses are presented to Rob for review, never sent autonomously
- NEVER use rgorham369@gmail.com — always check robert.gorham@testsigma.com

*Source: `memory/warm-leads.md` + `memory/playbooks/dedup-protocol.md` + `memory/sop-email.md`*
*Last updated: 2026-03-12 (Session 30)*
