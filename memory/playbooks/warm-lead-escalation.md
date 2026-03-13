# Playbook: Warm Lead Escalation

## When to Use
When a prospect replies to any outreach with interest, curiosity, or a positive signal. This covers: "tell me more," "what does this look like for us?", "I've been looking at tools like this," "can we chat?", or any reply that is NOT a clear no.

---

## Reply Classification (What Counts as a Warm Lead?)

| Reply Type | Example | Action |
|-----------|---------|--------|
| Positive / Curious | "Sounds interesting, what's involved?" | Move to warm-leads.md immediately. Draft same-day response. |
| Meeting ask | "Can we set up a call?" | Book meeting. Confirm in reply. Add to calendar. |
| Referral | "You should talk to our QA lead, Jane" | Thank referrer. Research Jane. Draft outreach mentioning referrer — same day. |
| Timing | "Good timing, we're evaluating tools" | Log in warm-leads.md. Draft response. Set follow-up reminder. |
| Curiosity | "What specifically have you done in our space?" | Answer with vertical proof point. Bridge to meeting ask. |

**Any positive or non-negative reply = warm lead. Move it into `memory/warm-leads.md` before doing anything else.**

---

## Step-by-Step Process

### Step 1: Log in warm-leads.md
Add the contact to `memory/warm-leads.md` with:
- Name, Company, Title
- Date of reply
- Reply type (Positive / Referral / Timing / Curiosity)
- Reply summary (1-2 sentences)
- Next action + due date

### Step 2: Draft Response (same session)
Response formula depends on reply type:

**Positive / Curious:**
- 2-3 sentences max
- Acknowledge their interest briefly (don't be effusive)
- Add one new piece of value (different proof point from the one that triggered their reply)
- Direct meeting ask: "What day works for a 25-min call?"

**Meeting ask:**
- Accept immediately
- Propose 2 specific time slots (Tue/Thu, 10am or 2pm local)
- Confirm the Google Meet link
- Do NOT send the meeting invite until Rob approves the response

**Referral:**
- Thank the referrer with one sentence
- Research the referred person (LinkedIn + Apollo enrichment)
- Draft outreach mentioning the referrer: "I was speaking with [referrer] and they mentioned you might be the right person to connect with on this."
- This outreach counts as a T1. Run through QA gate.

**Timing:**
- Validate their timeline: "That timing makes sense given..."
- Brief context: what's typically driving teams to evaluate at this stage
- Meeting ask: "Given the timing, would it make sense to compare notes? What day works?"

**Curiosity:**
- Answer the question directly and specifically (1-2 sentences)
- Add the matching proof point for their vertical
- Bridge: "Would it make sense to walk through what this looks like for [Company]? What day works?"

### Step 3: Present to Rob
ALL response drafts require Rob's review before sending. This is covered by the APPROVE SEND rule — no exceptions, even if the reply is obviously positive.

### Step 4: Send via Apollo (if warm lead is in Apollo sequence)
Or via Gmail MCP (if it's an inbound lead or direct email thread). Per CLAUDE.md: ALL outreach emails go through Apollo UI using robert.gorham@testsigma.com. Never reply directly from Gmail.

### Step 5: Update warm-leads.md
After Rob approves and response is sent:
- Update the contact's status: "Response sent [date]"
- Add the next follow-up date (typically 3-5 days if no reply)

---

## Meeting Booked: What to Do

When a warm lead confirms a meeting:
1. Create the Google Calendar event (use gcal_create_event with a Google Meet link)
2. Generate a meeting prep card (see meeting-prep.md playbook for format)
3. Update warm-leads.md status: "Meeting booked — [date]"
4. Log in MASTER_SENT_LIST.csv if not already logged (channel: "Apollo Email" or "LinkedIn InMail")
5. Tell Rob: meeting confirmed, prep card ready

---

## Common Mistakes

1. **Waiting to respond.** Warm leads go cold in 24 hours. If it's in the warm-leads.md, it needs a drafted response before the session ends.
2. **Over-explaining in the response.** 2-3 sentences max. The goal is a meeting, not a demo in the reply.
3. **Using the same proof point as the original email.** The reply triggered their interest — now add something new. If T1 used Hansard, the warm lead response uses CRED or Medibuddy.
4. **Sending without Rob's approval.** Even for "yes, let's chat" replies. The APPROVE SEND rule applies to every outgoing email.
5. **Not updating warm-leads.md.** This is the only place tracking warm lead follow-up dates. If it's not there, it gets forgotten.

---

---
*Version: 1.0 — 2026-03-13*
*Change log: v1.0 (Mar 13, 2026) — new playbook created; covers gap identified in repo audit (no warm lead escalation process documented)*
*When updating: increment version, add change log entry with date and what changed.*
