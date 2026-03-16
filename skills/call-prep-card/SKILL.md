# Call Prep Card Generator

**Version:** 1.0 — Created Mar 15, 2026

**Trigger:** On-demand — "prep my calls", "call prep for [name/company]", "what do I say to [persona]", "voicemail script for [name]"

**Output:** Inline response card (not saved to file unless Rob asks)

---

## Purpose

Generate personalized 3-line openers + voicemail scripts for cold calls. Persona-specific, conversational, backed by proof points. Designed to reverse the Feb 2026 win rate collapse (18% → 0% on 61 connects). Each card includes discovery questions and objection pivots.

---

## Trigger Detection

| Trigger Pattern | Action |
|-----------------|--------|
| "prep my calls for today" | Pull today's call targets from call-log.md or ask Rob for list |
| "call prep for [Name]" | Look up in MASTER_SENT_LIST.csv + warm-leads.md for context |
| "voicemail for [Name/Company]" | Generate voicemail script only |
| "opener for [persona] at [vertical]" | Generate opener only |
| "what do I say to a [Persona] at [Vertical]" | Generate full card for persona/vertical combo |
| "batch prep: [list of 3+ names]" | Generate abbreviated cards (opener + voicemail) for fast scanning |

---

## Phase 1: Gather Context

**If a specific name is given:**
1. Check `memory/warm-leads.md` for current P0-P3 status and prior interaction notes
2. Check `MASTER_SENT_LIST.csv` for send history (what touch, when, sequence)
3. Check `memory/contact-lifecycle.md` for timeline and any notes
4. Infer persona from job title, vertical from company domain
5. Surface prior outreach summary in the card

**If no specific name (persona + vertical combo):**
- Use Rob's standard ICP profiles from CLAUDE.md
- Generate generic but targeted card for that persona/vertical

---

## Phase 2: Output Format

Clean, scannable card (inline response, plaintext):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CALL PREP: [Name] | [Title] | [Company]
[Persona Label] | [Vertical]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPENER (live call):
"[Name], [3-line opener — conversational, not scripted, ties to their specific pain]"

VOICEMAIL (30 sec):
"Hey [Name], [Name] here from Testsigma — [1 sentence value prop specific to their pain]. [Proof point in 1 sentence]. Happy to share how — [callback line]. Talk soon."

DISCOVERY QUESTIONS (top 3):
1. [Question targeting their likely pain / current state]
2. [Question to uncover timeline / urgency / budget]
3. [Question to identify decision process / buying committee]

OBJECTION PREP:
• "Not interested" → [1-line pivot]
• "We use [Competitor]" → [1-line differentiator]
• "Send me info" → [1-line redirect to meeting]

PRIOR CONTACT:
[Summary of send history if applicable, or "No prior outreach"]

NOTES:
[Any account intelligence or vertical-specific context]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 3: Persona-Specific Messaging Matrix

Reference matrix for Claude during card generation. All messaging ties to proof points and value props.

### QA Manager / QA Lead (Primary Persona)

**Core Pain:** Flaky tests eating sprint time, manual regression backlog growing, testing slowing release cycles

**Opener Hook:** "regression cycles" or "test maintenance overhead"

**Best Proof Point:** Medibuddy (2,500 tests, 50% maintenance cut)

**Opener Template:**
"[Name], I saw you're leading QA at [Company]. Most QA managers I talk to are spending 40-50% of sprint on test maintenance and regression. We helped Medibuddy cut that in half by using AI self-healing. Curious if that's a pain point for you?"

**Voicemail Template:**
"Hey [Name], Rob here from Testsigma. We help QA teams cut test maintenance in half using AI self-healing — one of our customers cut 2,500 tests' maintenance by 50%. Happy to show you how that'd work for your team. Shoot me a time that works — [callback]. Talk soon."

**Discovery Q1:** "How much of your sprint is going to test maintenance right now?"
**Discovery Q2:** "What does your regression cycle look like before a major release?"
**Discovery Q3:** "Who else owns the automation roadmap with you?"

**Objections:**
- "Not interested" → "Totally get it. If regression cycles ever become a bottleneck, I'd love to chat."
- "We use [Competitor]" → "Smart. Most teams using [Competitor] are still doing 30-40% manual regression. Self-healing is different — I'd be curious if you've looked at that angle."
- "Send me info" → "Happy to, but honestly a 15-min call would be way faster. What day works?"

---

### Director / VP of QA (Primary Persona)

**Core Pain:** Scaling coverage without growing headcount, reporting gaps to eng leadership, release confidence pressure

**Opener Hook:** "coverage gaps before releases" or "QA team capacity"

**Best Proof Point:** CRED (90% regression coverage, 5x faster)

**Opener Template:**
"[Name], I was looking at [Company]'s scale. One of our customers, CRED, needed to hit 90% regression coverage without adding headcount. They did it in 5x less time with our AI test generation. Does coverage depth ever come up in your roadmap conversations?"

**Voicemail Template:**
"Hey [Name], Rob from Testsigma. We help QA leaders hit regression coverage targets without growing headcount — CRED got to 90% coverage 5x faster. Worth a quick chat to see if that maps to where you're headed. Let me know what day works — [callback]. Talk soon."

**Discovery Q1:** "What does your coverage look like going into a major release?"
**Discovery Q2:** "How much of your budget or headcount is tied to coverage improvements?"
**Discovery Q3:** "Who's your engineering counterpart when you talk about QA roadmap?"

**Objections:**
- "Not interested" → "Understood. When coverage does become a board conversation, I'll reach back out."
- "We use [Competitor]" → "Got it. Most teams I talk to using [Competitor] still struggle with plain-English test generation. Self-healing is the real unlock. Open to a quick look?"
- "Send me info" → "I will. But 15 minutes live would beat a deck — you could see it on your app. What day?"

---

### Senior SDET / Automation Lead (Influencer, 39.3% reply rate)

**Core Pain:** Brittle locators, flaky Selenium/Playwright tests, maintenance hell, pressure to reduce tech debt

**Opener Hook:** "locator maintenance" or "self-healing"

**Best Proof Point:** Hansard (regression 8→5 weeks)

**Opener Template:**
"[Name], I was checking out [Company]'s automation stack. Most SDETs I talk to are spending 40%+ of time on test maintenance and locator updates. We helped Hansard cut their regression cycle from 8 weeks to 5 by fixing that. Ring any bells?"

**Voicemail Template:**
"Hey [Name], Rob from Testsigma. We work with automation leads on self-healing — basically AI that fixes broken locators when the UI changes. One of our customers cut regression from 8 weeks to 5. Happy to show you how it works. What day works for a quick call — [callback]? Talk soon."

**Discovery Q1:** "How much time is your team spending on test maintenance vs new coverage?"
**Discovery Q2:** "What's your biggest pain with locator brittleness right now?"
**Discovery Q3:** "Who do you report automation ROI to?"

**Objections:**
- "Not interested" → "Fair. If brittle locators ever become a bigger headache, I'll reach back."
- "We use [Competitor]" → "Cool. Most SDETs using [Competitor] still do manual locator fixes. Self-healing is different — built for Playwright and Selenium. Open to seeing it?"
- "Send me info" → "I will. Quick demo on your test stack would be way more useful though. What day?"

---

### VP Engineering / CTO (Secondary, intent-only)

**Core Pain:** Dev velocity slowed by QA bottleneck, release confidence gaps, QA cost/headcount pressure

**Opener Hook:** "release confidence" or "QA bottleneck"

**Best Proof Point:** Cisco + Samsung brand credibility, or CRED/Hansard story if not a peer

**Opener Template:**
"[Name], I was looking at [Company]'s engineering scale. Most VPs I talk to say QA is a bottleneck in their release cycle. We work with companies like Cisco and Samsung to turn that around with AI test automation. Is that on your roadmap?"

**Voicemail Template:**
"Hey [Name], Rob from Testsigma. We help VP Engineering teams unblock QA bottlenecks using AI test automation — companies like Cisco and Samsung use us to ship faster with confidence. Worth a quick conversation? [Callback]. Talk soon."

**Discovery Q1:** "Is QA a bottleneck in your current release cycle?"
**Discovery Q2:** "What's your biggest pressure point when it comes to release velocity?"
**Discovery Q3:** "Who owns QA/test automation strategy on your side?"

**Objections:**
- "Not interested" → "Understood. When release velocity comes up, I'll check back in."
- "We use [Competitor]" → "Got it. Most VP Engineering teams using [Competitor] still have QA cycle time issues. We solve that with self-healing AI. Open to a conversation?"
- "Send me info" → "I will. But a 15-min call to map your release cycle would be more useful. What day works?"

---

## Phase 4: Batch Mode

**If Rob says "prep my calls for today" with 3+ names:**
- Generate abbreviated card (opener + voicemail only) for each
- Number them 1-5 for fast reference while dialing
- Full card only if Rob asks for specific person

**Example batch output:**

```
BATCH PREP — [Date] — [Count] Calls

1. Sarah Chen | QA Manager | TechCorp
   OPENER: "Sarah, most QA managers are spending 40-50% on test maintenance. We helped..."
   VOICEMAIL: "Hey Sarah, Rob here from Testsigma. We cut test maintenance in half with self-healing..."

2. Mike Rodriguez | Director QA | FinServe
   OPENER: "Mike, I was looking at FinServe's scale. Coverage gaps before release are..."
   VOICEMAIL: "Hey Mike, Rob from Testsigma. One customer hit 90% coverage 5x faster..."

[... 3, 4, 5 ...]
```

---

## Phase 5: Learning Loop Integration

Follow `skills/_shared/learning-loop.md`.

**After each call Rob takes:**
1. Ask: "How'd that call go? Any notes?"
2. Log outcome (positive/neutral/negative, persona, any useful intel) to `run-log.md`
3. If Rob reports an opener or voicemail worked, note which one in `learned-patterns.md`
4. Every 5th run: review which openers/voicemails are winning vs losing. Propose refinements.

**Feedback Questions:**
- "Did the opener land?"
- "Did they engage on the pain point you led with?"
- "What objection came up (if any)?"
- "What discovery questions got the best response?"
- "Would you use this prep card again?"

**Refinement Triggers:**
- If 3 of 5 runs report "opener didn't land," propose new hook
- If voicemail callback rate is 0%, propose new structure
- If objection prep isn't hitting, add new objection type
- Every quarter: re-validate proof points (pull latest case study data)

---

## Key Rules

1. **Never scripted-sounding.** All openers and voicemails are conversational, short sentences, tie directly to their pain.
2. **Always source proof points.** Never make up metrics. Hansard, Medibuddy, CRED are verified. If Rob asks about a prospect's vertical and you don't have a proof point, use Cisco/Samsung for brand credibility.
3. **Persona-first.** Persona determines hooks and discovery questions. Title > company when inferring persona.
4. **Check context first.** Always check warm-leads.md and MASTER_SENT_LIST.csv before generating a card. If they're already P0 or recently sent a touch, adjust messaging.
5. **No more than 3 discovery Qs.** Keep cards scannable. Best 3 only.
6. **Voicemail always 30 sec or less.** Count words if needed.
7. **Objection prep is optional.** Skip if Rob is calling someone warm or already in an active sequence.

---

## Files to Reference

| File | Use |
|------|-----|
| `CLAUDE.md` | Persona profiles, proof points, value props |
| `memory/warm-leads.md` | Check P0-P3 status before generating |
| `MASTER_SENT_LIST.csv` | Send history (what touch, when) |
| `memory/contact-lifecycle.md` | Contact timeline and notes |
| `memory/call-log.md` | Rob's daily call activity |
| `skills/_shared/learning-loop.md` | Feedback + refinement protocol |
| Google Drive "Full-Funnel BDR Scripts" | Reference for talk track consistency |
| `memory/sop-post-call-followup.md` | Context on discovery questions |

---

## Example Invocations

**"Prep call for Sarah Chen at TechCorp (QA Manager)"**
→ Lookup Sarah in MASTER_SENT_LIST.csv and warm-leads.md. If no history, generate full card for QA Manager + TechCorp (SaaS). If recent send, note "Touch 1 sent [date]" in PRIOR CONTACT.

**"What do I say to a Director QA at a FinTech?"**
→ No specific person. Generate generic card for Director/VP QA persona at FinTech vertical. Use CRED proof point if FinTech, else Cisco.

**"Voicemail script for Mike Rodriguez"**
→ Lookup Mike in MASTER_SENT_LIST.csv. Infer persona from title. Generate voicemail only (no opener/discovery/objections).

**"Prep my calls for today"**
→ Ask Rob: "Who's on your call list today?" Or check memory/call-log.md for today's date. Generate batch cards.

**"Batch prep: [list of 5 names]"**
→ Loop through each. Generate abbreviated cards (opener + voicemail only). Output as numbered list for fast dialing.

---

## Success Metrics

- Openers that lead to engagement (prospect asks a question vs "send me info")
- Voicemail callbacks (call back from VM vs silence)
- Discovery questions that uncover real pain vs flat responses
- Objection pivots that keep the conversation alive vs dead-end "we're all set"

Track in run-log.md. Report to learning-loop every 5 runs.

---

_Created Mar 15, 2026. Last updated: [auto-populate on run]_
