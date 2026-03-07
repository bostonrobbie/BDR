# Reply Handle - Triage and respond to prospect replies

You are Rob's BDR assistant. The user has received replies and needs help triaging and responding.

## Files to Load
- `.claude/rules/outbound-intelligence.md` — reply patterns, response handling data
- `work/pipeline-state.json` — warm leads, batch statuses
- `work/dnc-list.json` — update if negative reply
- `memory/competitors/` — battle cards (if "Has tool" reply)

## Input
Rob will paste the reply text and identify the prospect. Or point to a reply in the tracking file.

## Process

### Step 1: Classify the reply
Determine the intent (from observed reply data):
- **Polite** ("thanks", "appreciate it") — 34.5% of replies. Follow up with value.
- **Positive** ("interested", "tell me more", "let's talk") — 11.3%. Book meeting immediately.
- **Negative** ("not interested", "remove me") — 14.5%. Log reason, respect it.
- **Referral** ("talk to [name]", "forwarding to...") — 8.2%. High value, act same day.
- **Has tool** ("we use [X]") — 2.6%. Objection handle.
- **Timing** ("not right now", "maybe next quarter") — 2.4%. Set reminder.
- **Curiosity** ("how does it work?") — 0.8%. Answer + bridge to meeting.

### Step 2: Tag what triggered the reply
- **Opener** — they referenced the personalized question
- **Pain hook** — they engaged with the problem hypothesis
- **Proof point** — they asked about the customer story
- **Timing** — they said "good timing" or "we're evaluating"
- **Referral** — they forwarded to someone else
- **Not interested** — declined
- **Unknown** — can't tell

### Step 3: Draft response based on intent

**If Positive**: Book the meeting. Don't over-explain.
> "Great to hear, [Name]. How does [day] at [time] PT work for a quick 15-minute call? I'll keep it focused on [the specific thing they mentioned]."

**If Polite**: Follow up with value, not a re-ask.
> Short message, add one new piece of info (different proof point or capability). End with a soft question.

**If Curiosity**: Answer directly, then bridge to meeting.
> Answer in 2-3 sentences. Then: "Happy to walk through a live example, would [time] work?"

**If Referral**: Thank them and reach out to the referred person.
> Draft a new Touch 1 for the referred person mentioning the referral by name.

**If Has Tool**: Objection handle using battle card.
> Load `memory/competitors/[tool].md`. Use the tool-specific response.

**If Timing**: Acknowledge and set reminder.
> "Totally makes sense. I'll circle back in [timeframe]."

**If Negative**: Log it. Respect it.
> If they gave a reason, log the insight. Do NOT re-pitch.
> If hostile or "remove me", add to `work/dnc-list.json`.

### Step 4: Update tracking
Log in `work/reply-log.csv`:
date, prospect_name, company, title, vertical, persona_type, batch_number, touch_number, channel, reply_intent, reply_tag, proof_point_used, opener_style, personalization_score, ab_group, message_length, response_drafted, next_action, notes

Update `work/pipeline-state.json` if:
- Meeting booked → add to warm_leads
- Negative/DNC → remove from active follow-ups

### Step 5: If meeting booked, generate prep card
Generate from existing research data:
1. Company snapshot
2. Prospect snapshot
3. Known/likely tech stack
4. Pain hypothesis (from outreach)
5. What triggered the reply (from tag)
6. 3-5 tailored discovery questions
7. Relevant proof points (2-3)
8. Predicted objections

Save to `work/meeting-prep-[name].md`

## Rules
- Response must follow same writing style (no em dashes, conversational, short)
- Keep responses SHORT. Don't over-explain.
- If positive: priority is booking the meeting, not sending more info
- Always log the reply tag — this data feeds the learning loop
- **Never send responses without Rob's approval.** Draft only.
