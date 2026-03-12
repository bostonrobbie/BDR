# SOP: Post-Call Follow-Up Email from Gong Transcript
**Created:** 2026-03-11
**Author:** Claude (Cowork session)
**Trigger:** After any sales/discovery call recorded in Gong, when Rob needs to send a follow-up email summarizing what was discussed.

---

## When to Use This SOP
- Rob had a call with a prospect that was recorded by Gong
- Rob needs a follow-up email recapping what was discussed and confirming next steps
- Prompt will typically sound like: "write a follow-up to Elias based on our call", "draft a recap email for my call with [name]", "get the transcript from my call with [name] and write them an email"

---

## Step 1: Find the Gong Transcript in Gmail

Gong sends call summaries to robert.gorham@testsigma.com immediately after a recorded call ends.

**Gmail search query to use (via Gmail MCP):**
```
from:gong.io [FirstName]
```
If that returns no results, try:
```
from:gong.io after:[YYYY/MM/DD]
```
Or search by company/deal name:
```
from:gong.io [CompanyName]
```

**What the email contains:**
- Call title, date, duration, participants
- Key points (numbered summary of what was discussed)
- Next steps (action items assigned to each person)
- Interaction tips (talk ratio, etc.)

**Read the full message body** using `gmail_read_message` with the message ID. The snippet in `gmail_search_messages` is truncated.

---

## Step 2: Extract the Relevant Information

From the Gong email, pull:

| Field | Where to Find It |
|-------|-----------------|
| Prospect's name | Key points or Next steps section |
| Prospect's title/company | Key points or participants list |
| What the prospect mentioned (pain points, goals, current tools) | Key points |
| What Rob covered/explained | Key points |
| Agreed next steps | Next steps section |
| Scheduled meeting date/time | Key points or Next steps |

**⚠️ CRITICAL — Gong summary email is NOT sufficient for follow-up drafts.**

The Gong summary email is a 10-point AI interpretation of the call. It captures high-level topics but routinely misses specific questions the prospect asked, specific concerns they raised, and the nuance of what they actually want to know. **Always retrieve the full verbatim transcript from the Gong app before drafting.**

Lesson from Elias call (Mar 11, 2026): The summary email captured CI/CD, self-healing, and coverage, but completely missed that Elias's main question was about AI correlating test failures with code changes and system state (Google Cloud/services) to surface root cause. The v2 draft built from the summary email missed this entirely. Only after reading the full transcript was v3 drafted correctly.

**To get the full transcript:**
1. Navigate to us-37530.app.gong.io
2. Log in via JumpCloud Enterprise SSO (robert.gorham@testsigma.com → Enterprise SSO → JumpCloud MFA)
3. Go to Calls → find the call → open Transcript tab
4. Click "Copy all" to get the full verbatim text

Gong's summary is an AI interpretation of the call, not a verbatim transcript. Use judgment — if a detail seems off, ask Rob to clarify before including it in the email.

---

## Step 3: Look Up the Prospect in Apollo (Optional but Recommended)

If you need the prospect's email address or more context:
1. Use `apollo_contacts_search` with `q_keywords: "[FirstName] [LastName or Company]"`
2. Or use `apollo_mixed_people_api_search` with `q_keywords: "[FirstName]"` and `person_titles` filter

If the call was a **cold call made during a prospecting/coaching session**, the prospect may NOT yet be in Apollo as a contact. In that case, flag this to Rob — he'll need to provide the email address before the draft can be sent.

---

## Step 4: Draft the Follow-Up Email

### Email Formula (Post-Call)
Post-call follow-ups are warmer than cold outreach. Still follow Rob's writing rules, but the structure is different:

1. **Opener:** Quick "good talking with you" + reason for email ("wanted to follow up while things are fresh")
2. **Recap what the prospect said:** Reference their specific goals/pain points/context they shared. This shows you listened and personalizes the recap.
3. **Recap what Testsigma solves:** Only include features/capabilities Rob actually mentioned on the call. Don't add new info.
4. **Confirm next steps:** Meeting date, calendar invite, any actions Rob committed to.
5. **Keep it short:** 90-130 words. This is a recap, not a pitch.

### Writing Rules (same as all Rob outreach)
- No em dashes (—). Use commas.
- No "I noticed" or "based on our call, I wanted to..."
- Conversational, not corporate
- Short sentences, short paragraphs (blank line between each block)
- One CTA only

### Subject Line Options for Post-Call Follows
- `Following up + [Date of Meeting]`
- `Quick recap + [Next Step]`
- `[Their Name] + recap`

---

## Step 5: Present to Rob for Review

**NEVER send without Rob's explicit "APPROVE SEND."**

Present the draft with:
- Subject line
- Full email body
- Note: prospect's email address (confirm Rob has it if not found in Apollo)
- Note: any details you're uncertain about (e.g., meeting time if not confirmed in transcript)

---

## Example (March 11, 2026 — Elias call)

**Source:** Gong email `19cde607c93884d5` — "calls: Call recording and analysis is ready" (Mar 11, 2026)

**What Gong captured about Elias (second cold call in joint session with Williamw Dalley):**
- QA Engineering Manager
- Testsigma was already on his evaluation list (prior awareness)
- Needs to rethink testing approach due to rapid AI changes
- Aiming for continuous deployment
- Rob covered: CI/CD integration, web/API/mobile/Salesforce testing, auto-healing, test docs/analysis
- Scheduled 15-minute follow-up meeting for April 13th

**Draft produced:** See `drafts/post-call-elias-mar11.md`

---

## Related Files
- `memory/sop-outreach.md` — Cold outreach writing rules (still apply to style/tone)
- `memory/warm-leads.md` — Track prospects who become warm after calls
- `memory/pipeline-state.md` — Update with call outcome + scheduled meeting
