# Skill: Post-Meeting Automation

**Version:** 1.0 — Initialized 2026-03-15
**Purpose:** After prospect meetings end: capture call notes, analyze transcripts, extract buying signals, stage follow-up drafts for Rob approval.
**Key Rule:** NEVER send anything to prospects automatically. All outputs are internal records + draft follow-ups staged for Rob's APPROVE SEND.

---

## Overview

This skill runs 6 phases:

1. **Meeting Detection** — Scans Google Calendar for past meetings, matches contacts to pipeline
2. **Pre-Meeting Prep Card** — Runs BEFORE call (triggered manually or auto), generates 1-page briefing
3. **Post-Meeting Notes Capture** — After call, prompts Rob for outcome + key takeaways
4. **Transcript Analysis** — When Rob provides transcript, extracts signals, objections, pain points
5. **Follow-Up Draft Staging** — Generates T2 draft based on call outcome for Rob to APPROVE SEND
6. **Call Log Update** — Appends to memory/call-log.md for analytics pipeline

---

## Phase 1: Meeting Detection

**Trigger:** Automatic (runs as part of morning-briefing or stage-monitor), or manual call to this skill.

**Steps:**

1. Call `gcal_list_events` for past 24 hours:
   - `timeMin`: Now - 24 hours (ISO format)
   - `timeMax`: Now (ISO format)
   - Filter: events with `status = 'confirmed'` where end time < now

2. For each meeting found:
   - Extract attendee names and email domains
   - Search for attendee name/domain in:
     - `memory/warm-leads.md` (P0-P3 contacts)
     - `MASTER_SENT_LIST.csv` (all outreach history)
   - If matched: flag as "PROSPECT MEETING — call notes required"

3. For matched meetings, create a stub in `memory/call-notes/` with filename:
   ```
   YYYY-MM-DD-[company-short]-[contact-lastname].md
   ```
   Example: `2026-03-15-overdrive-jain.md`

   Use this template in the stub (user will edit after call):
   ```
   # Call Notes: [Contact First Last] at [Company]

   **Date:** [YYYY-MM-DD]
   **Time:** [HH:MM - HH:MM]
   **Call type:** [discovery / follow-up / meeting / discovery call]
   **Duration:** [X minutes]
   **Outcome:** [PENDING — Rob fills after call]

   ## Quick Summary
   [Rob fills after call]

   ## Status
   ⏳ Waiting for call notes and transcript
   ```

4. Log to run-log.md: "Meetings detected: [N], New call-notes stubs created: [N]"

---

## Phase 2: Pre-Meeting Prep Card

**Trigger:** Manual — Rob says any of:
- "prep me for my call with [name]"
- "generate prep for [name]"
- "call prep [name]"

**Steps:**

1. Parse Rob's request to extract contact name
2. Search `memory/warm-leads.md` + `MASTER_SENT_LIST.csv` for exact match
3. If found, read:
   - Contact's full company + domain
   - When first contacted (from MASTER_SENT_LIST.csv)
   - What was sent (Touch 1 subject + date)
   - Any replies (search memory/warm-leads.md and memory/contact-lifecycle.md)
4. Read company context:
   - Check `memory/context/` files for industry/vertical match
   - Check `memory/competitors/_index.json` and competitor .md files for relevant tools
   - Pull from `memory/warm-leads.md` if "OverDrive Intel" section exists
5. Read objection map: `memory/context/objection-map.json`
6. Generate a **Prep Card** output formatted as:
   ```
   # PREP CARD: [Contact Name] — [Company]
   **Date:** [today]
   **Your goal:** [specific outcome to target: 15-min discovery / meeting booked / understand stack]

   ## Contact Profile
   - **Title:** [role]
   - **Company:** [name] ([domain])
   - **Vertical:** [industry]
   - **Why in pipeline:** [first touch date, what triggered outreach]

   ## Interaction History
   - **First touch:** [date] — [Touch 1 subject] via [method: InMail/Email/LinkedIn]
   - **Last message:** [date] — [subject or brief description]
   - **Replies:** [number and tone: "2 replies, both positive" or "none yet"]
   - **Stage:** [P0 (hot) / P1 (warm) / P2 (objection) / P3 (deferred)]

   ## Their Company Context
   - **Size:** [employees]
   - **Revenue:** [if available]
   - **Recent news:** [funding, hiring, leadership changes — from memory/warm-leads.md intel section]
   - **Tech stack:** [current test automation tool, CI/CD, main languages]
   - **Current tools they use:** [paste from warm-leads or context intel]

   ## Likely Pain Points (from vertical research)
   - [1st common pain for their title/vertical]
   - [2nd common pain for their title/vertical]
   - [3rd common pain for their title/vertical]

   ## Talk Track Opener (natural, consultative)
   "[Personalized opener that references something about their company or role. Example: 'Hi [Name], thanks for taking the time. I know [Company] is scaling your testing, and I've been researching your team's approach to [specific pain]. Curious to hear how you're handling [pain area] today.']"

   ## 3 Discovery Questions (based on vertical + pain)
   1. [Question about their current process/tools]
   2. [Question about team size/structure/goals]
   3. [Question about timeline/constraints if looking to change]

   ## What a "Win" Looks Like This Call
   - [Specific outcome 1 — e.g., "understand their test coverage gaps"]
   - [Specific outcome 2 — e.g., "learn about their current vendor"]
   - [Specific outcome 3 — e.g., "set next conversation time"]

   ---
   **After the call:** Paste transcript or notes here, then ask Claude to analyze and stage follow-up.
   ```

7. Output the Prep Card to chat (display only, don't save yet — Rob saves to their notes if desired)
8. Log to run-log.md: "Prep card generated for [contact name]"

---

## Phase 3: Post-Meeting Notes Capture

**Trigger:** Manual — Rob says any of:
- "capture call notes from [name]"
- "log my call with [name]"
- "add call notes [name]"

**Steps:**

1. Prompt Rob with structured form in chat:
   ```
   ## Call Notes Capture — [Contact Name]

   **Did they connect?** yes / no / partial (voicemail, etc.)

   **Overall outcome:**
   - positive (interested, next step scheduled)
   - neutral (exploratory, no clear signal)
   - negative (objection, not interested)
   - no_show (they didn't join)

   **Key things they said** (1-3 bullets — Rob types):
   - [main point 1]
   - [main point 2]
   - [main point 3]

   **Commitments made:**
   - What I (Rob) promised: [specific deliverable or timeline]
   - What they promised: [next step, info to send, etc.]

   **Next step agreed:** [date] — [specific action]
   ```

2. Wait for Rob to fill in the form

3. Once submitted, open the call-notes file:
   `memory/call-notes/YYYY-MM-DD-[company-short]-[lastname].md`

4. Update the stub with Rob's responses:
   - Update `**Outcome:**` field
   - Add to `## Quick Summary` section
   - Update `## Status` to: "⏳ Waiting for transcript analysis"

5. Ask: "Got it. Do you have a transcript or recording to analyze? (You can paste transcript text, upload a file, or skip if none available)"

6. Log to run-log.md: "Call notes captured for [contact name], outcome: [positive/neutral/negative]"

---

## Phase 4: Transcript Analysis

**Trigger:** Rob provides transcript (paste or upload) after Phase 3

**Steps:**

1. Receive transcript text from Rob (paste or file upload)

2. Parse the transcript and extract:

   **A. Buying Signals** — Phrases indicating interest/urgency/pain acknowledgment
   - Look for: "we're looking at", "we need to", "this is killing us", "we'd love to", "timeline", "budget", "decision maker", "trial", "POC"
   - Extract exact quotes
   - Classify: Strong / Medium / Weak

   **B. Objections Raised** — Categorize against `memory/context/objection-map.json`
   - Read objection map to identify categories (Cost / Timeline / Competitor / Technical / Fit / Viability / etc.)
   - For each objection mentioned, note:
     - What they said (quote)
     - How Rob responded
     - Did it land (yes / partial / no)

   **C. Key Pain Points** — Specific problems they described
   - Extract and categorize: Maintenance / Velocity / Coverage / Cost / Scaling / Hiring / CI-CD integration / etc.
   - Note intensity: Annoying / Real problem / Critical

   **D. Commitments Made**
   - What Rob promised: [specific action, timeline]
   - What they promised: [next step, callback, info to send]

   **E. Risk Factors** — Concerns raised
   - Budget constraints
   - Timeline pressure
   - Competitors mentioned
   - Team size/skill constraints
   - Organizational constraints

   **F. Talk Ratio Estimate** — Rough % of speaking time
   - Rob: [X]%
   - Contact: [Y]%
   - (Ideal for discovery: 30% Rob, 70% contact)

   **G. Recommended Next Step**
   - Based on signals + outcome
   - Is T2 email recommended? (yes / no)
   - Suggested CTA: [Meeting booking / Info request / Trial / Follow-up call / etc.]

3. Create a **Transcript Analysis Card** formatted as:
   ```
   ## Transcript Analysis — [Contact Name]
   **Date:** [today]
   **Analyzed by:** [session]

   ### Buying Signals 🔥
   | Signal | Quote | Strength |
   |--------|-------|----------|
   | [Type] | "[exact quote]" | Strong / Medium / Weak |

   ### Objections Raised
   | Objection | Category | Their Quote | How You Responded | Landed? |
   |-----------|----------|-------------|-------------------|---------|
   | [type] | [from map] | "[quote]" | "[your response]" | yes/partial/no |

   ### Key Pain Points
   - **[Pain 1]** (Intensity: Critical) — "[quote]"
   - **[Pain 2]** (Intensity: Real) — "[quote]"
   - **[Pain 3]** (Intensity: Annoying) — "[quote]"

   ### Commitments
   - **Rob's commitment:** [action] — Due: [date]
   - **Their commitment:** [action] — Due: [date]

   ### Risk Factors
   - [Risk 1]
   - [Risk 2]
   - [Risk 3]

   ### Talk Ratio
   - Rob: [X]%
   - Contact: [Y]%

   ### Recommended Next Step
   - **Send T2 follow-up:** yes / no
   - **CTA:** [specific action]
   - **Timing:** [ASAP / within 24 hours / wait X days]
   - **Reason:** [why this next step fits the signal pattern]
   ```

4. Append this card to the call-notes file (append to bottom of the existing notes)

5. Log to run-log.md: "Transcript analyzed for [contact name], signals found: [count], recommended: [T2/follow-up/no action]"

---

## Phase 5: Follow-Up Draft Staging

**Trigger:** Automatic after Phase 4 (transcript analysis), if "Send T2 follow-up: yes"

**Steps:**

1. Read the Transcript Analysis output from Phase 4

2. Check the outcome and buying signals:
   - If outcome = "positive" + strong signals: Draft a brief action-oriented email
   - If outcome = "neutral" + medium signals: Draft a discovery-focused email
   - If outcome = "negative": Do NOT draft (note in log why)

3. Generate a follow-up email draft:
   - Subject: Personalized based on what was discussed
   - Body: Under 100 words, references specific things they said, confirms next step, one clear CTA
   - Tone: Consultative, not pushy. Reference their pain point(s).
   - Example:
     ```
     Subject: Quick thought on [specific pain they mentioned]

     [Name],

     Thanks again for the call yesterday. I was thinking about what you said regarding [specific pain point].

     We actually helped [similar company] solve this exact issue — they cut maintenance time by 50%. Happy to walk you through how they did it.

     What does your calendar look like [next 3 days] for a 15-min sync?

     Rob
     ```

4. Save to: `batches/t2-pending/post-call-[name-lowercase]-[YYYY-MM-DD].md`
   Example: `batches/t2-pending/post-call-namita-jain-2026-03-15.md`

5. File format:
   ```
   # T2 FOLLOW-UP — [Contact Name]

   **From:** Robert Gorham <robert.gorham@testsigma.com>
   **To:** [contact email]
   **Subject:** [email subject]
   **Status:** ⚠️ REQUIRES APPROVE SEND — Do not send automatically
   **Staged:** [date/time]
   **Call outcome:** [positive/neutral/negative]
   **Recommended timing:** [ASAP / 24 hours / wait X days]

   ---

   ## Email Body

   [full email text]

   ---

   ## Reasoning

   Based on the call:
   - **Key signal:** [what buying signal this follows up on]
   - **Their pain:** [specific pain mentioned]
   - **Proof point:** [which customer story this references]
   - **CTA:** [why this action makes sense]

   **Next step after approval:** Rob says "APPROVE SEND post-call [name]" → Claude sends via Apollo task queue.
   ```

6. Update memory/warm-leads.md for this contact:
   - Add new line in their "**Outreach Log:**" section:
     ```
     - [date] — Call (discovery): positive outcome, [key insight]. T2 follow-up staged in batches/t2-pending/.
     ```
   - Update their status to: **Stage:** Engaged or Post-Call Sequence (depending on outcome)

7. Log to run-log.md: "Follow-up draft staged: [name], file: [path], ready for APPROVE SEND"

---

## Phase 6: Call Log Update

**Trigger:** After Phase 3 (notes captured) — automatic

**Steps:**

1. Read `memory/call-log.md`

2. Append new entry:
   ```
   | [YYYY-MM-DD] | [Contact Name] | [Company] | [Persona] | [Vertical] | connects: [1/0] | outcome: [positive/neutral/negative] | meeting_booked: [yes/no] | notes: [brief 1-liner] |
   ```

3. Example:
   ```
   | 2026-03-15 | Namita Jain | OverDrive | QA Manager | Media | connects: 1 | outcome: positive | meeting_booked: yes | Discovery call, pain on test maintenance, interested in POC |
   ```

4. This feeds into weekly-analytics and system-diagnostics for pipeline metrics

5. Log to run-log.md: "Call log updated: [name]"

---

## Error Handling & Edge Cases

**Meeting not found in calendar:**
- If Rob's call wasn't on the calendar, ask Rob to provide: contact name, company, date/time
- Create call-notes stub manually

**Transcript too long:**
- If transcript > 5000 words, ask Rob if they want a summary first
- Proceed with full analysis but note in log: "Long transcript (N words)"

**Contact not in warm-leads or MASTER_SENT_LIST:**
- Log as "external contact (no prior outreach record)"
- Still capture notes + generate follow-up, but don't try to match in enrichment files

**Rob doesn't provide transcript:**
- Complete Phases 1-3 only
- Don't stage T2 draft without transcript signals
- Note in run-log: "No transcript provided, skipped Phase 4-5"

**Multiple meetings in one day:**
- Process each one separately
- Create separate call-notes files for each
- Log count: "Meetings processed: [N]"

---

## Self-Improvement Loop

### Learned Patterns
Read `learned-patterns.md` at the start of each run. Apply calibration adjustments noted there.

### Run Log
After every execution, append to `run-log.md` using standard format from `skills/_shared/learning-loop.md`.

**Key metrics to log:**
- Meetings detected: [N]
- Call-notes stubs created: [N]
- Prep cards generated: [N]
- Transcripts analyzed: [N]
- Follow-up drafts staged: [N]
- Call log entries appended: [N]
- Anomalies: [any unexpected behavior]

### Every 5th Run
Follow the pattern review protocol in `skills/_shared/learning-loop.md`. Extract patterns and propose SKILL.md updates if warranted.

---

## Privacy & Safety Rules

- Never log full email addresses or phone numbers in run-log.md (contact name only)
- Call-notes files are internal only — never share externally
- Transcripts stored locally only, not transmitted
- Never log prospect's personal details beyond name + company + title
- **NEVER auto-send anything** — all follow-up emails must have Rob's explicit APPROVE SEND

---

## Quick Reference: What to Ask Rob At Each Phase

| Phase | Rob Input | Format |
|-------|-----------|--------|
| 1 | None (auto) | Auto-detection |
| 2 | Trigger phrase | Voice (e.g., "prep me for [name]") |
| 3 | Call outcome + notes | Form submission |
| 4 | Transcript | Paste or file upload |
| 5 | Approval to send | Chat: "APPROVE SEND post-call [name]" |
| 6 | None (auto) | Auto-log |

---

## Success Criteria

- ✅ All prospect meetings detected and logged
- ✅ Pre-meeting prep cards run <1 minute from request
- ✅ Post-meeting notes capture structured and saved
- ✅ Transcripts analyzed for signals + objections + pain
- ✅ Follow-up drafts staged (never auto-sent)
- ✅ Call log updated weekly by analytics pipeline
- ✅ No sensitive data in logs
- ✅ Rob has full visibility + approval control
