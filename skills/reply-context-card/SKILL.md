# Reply Context Card

**Version:** 1.0 — Created Mar 15, 2026

**Trigger:** Automatically invoked by `reply-classifier` when a P0/P1 reply is detected. Also callable on-demand via "context card for [name]" or "pull up [name]'s history"

**Output:** Inline response card (printed in conversation for Rob to read before responding)

---

## Purpose

The moment a warm reply lands, Rob should have everything in one place — who this person is, what was sent to them, what they said, what their company is doing, and exactly how to respond. Eliminates the mental overhead of reconstructing context from scattered files.

This skill is the **context enrichment layer** that sits between reply classification and reply routing:

```
Gmail Reply → reply-classifier (P0/P1?) → reply-context-card (enrich) → reply-router (draft)
```

---

## Trigger Integration with Reply Classifier

When `reply-classifier` detects a P0 or P1 reply:

1. **reply-classifier** detects reply → classifies P0/P1
2. **reply-context-card** (THIS SKILL) generates context card
3. **reply-router** drafts response with full context

This is a **blocking call** — the context card prints before Rob reads the reply, so he has full context before deciding how to respond.

---

## Phase 1 — Pull Send History

**Input:** Replier's name + email address (from reply-classifier output)

**Actions:**

1. Search `/mnt/Work/MASTER_SENT_LIST.csv` for this contact:
   - When were they first contacted?
   - Which sequence/batch?
   - Which touch number replied (T1? T2? T3?)?
   - Any prior replies, bounces, or stage changes?

2. Search `/mnt/Work/memory/contact-lifecycle.md` for additional history:
   - Has this contact been touched before (e.g., prior session)?
   - Any objections logged?
   - Prior outcomes?

3. Record findings:
   - First touch date
   - Current sequence/batch ID
   - Touch number (1, 2, 3, or 4+)
   - Reply status history

---

## Phase 2 — Pull Original Message Sent

**Input:** Batch ID + contact name from Phase 1

**Actions:**

1. Locate batch tracker HTML in `/mnt/Work/batches/active/`:
   - Look for `tamob-batch-*.html` matching the batch ID
   - If not in `active/`, check `archive/old-outreach-html/`

2. Parse the batch HTML for this contact's row:
   - Extract exact subject line
   - Extract exact email body sent
   - Extract CTA used (e.g., "What day works", "Curious if", etc.)
   - Extract send timestamp

3. Record:
   - Subject line (full, verbatim)
   - Email body (first 3-4 lines + CTA)
   - Send timestamp
   - Touch number and sequence position

**Why this matters:** Rob needs to see EXACTLY what the prospect is replying to. This context is critical for response strategy.

---

## Phase 3 — Read the Reply Thread

**Input:** Prospect's email address

**Actions:**

1. Use `gmail_search_messages` to find threads with this prospect:
   - Query: `from:[prospect email] to:robert.gorham@testsigma.com`
   - Limit to last 30 days

2. Use `gmail_read_thread` to pull full thread:
   - Get all messages in chronological order
   - Include timestamps, full body text, and any forwarding chains

3. Classify thread structure:
   - Direct reply to Touch 1/2/3?
   - Forwarded to someone else?
   - Chain of replies (mutual discussion)?
   - Any additional context in the thread?

4. Extract prospect's exact reply text (verbatim quote)

---

## Phase 4 — Live Company Enrichment (Apollo)

**Input:** Company domain from prospect's email address

**Actions:**

1. Use `apollo_organizations_enrich` with the company domain:
   - Extract: headcount, recent funding, funding stage, revenue if available
   - Extract: tech stack (especially CI/CD, test automation, DevOps tools)
   - Extract: any job postings (especially QA, SDET, automation engineering roles)

2. Use `apollo_people_match` to verify prospect's current title and seniority:
   - Input: prospect's first name, last name, company domain
   - Extract: current title, seniority level (IC/Manager/Director/VP/C-Suite)
   - Note: any changes since first touch

3. Record findings:
   - Company headcount and stage
   - Active QA hiring (Y/N — count if yes)
   - Key tech signals (test tools, CI/CD platforms)
   - Prospect's verified current title and seniority

---

## Phase 5 — Check Warm Leads + Profile Signals

**Input:** Prospect's email address and name

**Actions:**

1. Search `/mnt/Work/memory/warm-leads.md`:
   - Is this person already tracked?
   - What's their current priority (P0/P1/P2/P3)?
   - What was the last update date?
   - Any notes about their intent?

2. Check `/mnt/Work/memory/linkedin-signals.md` (if file exists):
   - Did they view Rob's profile recently?
   - Did they interact with Rob's posts?
   - Read an InMail?
   - Record date of most recent signal

3. Check `/mnt/Work/memory/pipeline-state.md`:
   - Is this contact logged as a recent reply?
   - Any stage or outcome recorded?

**Why this matters:** Profile views, post engagement, and prior warm-lead tracking all indicate genuine interest. These signals strengthen the case for immediate action.

---

## Phase 6 — Classify Reply Intent

**Input:** Prospect's reply text from Phase 3

**Actions:**

Analyze reply text and classify into one of five intents:

- **🟢 POSITIVE** — "Yes", "interested", "tell me more", "let's connect", "happy to chat", "send details"
  - Indicator: Active agreement or explicit interest

- **🟡 SOFT** — "Not right now", "maybe later", "send me info", "will reach out", "in a few weeks"
  - Indicator: Interested but timing is unclear or delayed

- **🔴 OBJECTION** — "We already have X", "not a priority", "no budget", "don't need this", "we use [competitor]"
  - Indicator: Active resistance or stated objection

- **⚫ OPT-OUT** — "Remove me", "not interested", "stop emailing"
  - Indicator: Explicit opt-out; do not re-contact

- **❓ AMBIGUOUS** — Unclear, needs interpretation, question asked without clear intent signal
  - Indicator: Neutral or clarification-seeking

Record: intent classification + 1-2 word rationale (e.g., "POSITIVE: Explicit yes")

---

## Phase 7 — Generate the Context Card

Output the following card in the conversation. This is what Rob reads first:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REPLY CONTEXT CARD
[Name] | [Title] | [Company]
Replied: [date/time, e.g., "Mar 15, 2:34 PM"] | Sequence: [batch name] | Touch: [T1/T2/T3]
Intent: [🟢 POSITIVE / 🟡 SOFT / 🔴 OBJECTION / ⚫ OPT-OUT / ❓ AMBIGUOUS]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THEIR REPLY:
"[Full reply text quoted verbatim]"

WHAT WAS SENT:
Subject: [subject line]
Sent: [date, e.g., "Mar 13, 2026"], Touch [N] of sequence
"[First 2-3 lines of original message body]..."

THEIR COMPANY RIGHT NOW:
- [Company]: [N] employees | [Vertical] | [Funding stage if known]
- Tech stack signals: [CI/CD tools, test automation tools if found — or "No signals"]
- QA hiring: [Yes, N open roles / No open QA roles]
- Recent news: [1 bullet if anything notable; otherwise omit]

CONTACT INTEL:
- Title: [Current title] | Seniority: [IC/Manager/Director/VP/C-Suite]
- LinkedIn: [Viewed your profile: Yes (date) / No]
- Prior contact: [First touch date] → [summary of touch history, e.g., "T1 Mar 13 → T2 sent (pending)"]
- In warm-leads: [Yes, Priority P0 / Yes, Priority P1 / No]

RECOMMENDED NEXT STEP:
[1-2 sentences describing what to do and suggested timing]
→ [One-sentence strategy suggestion for reply direction — not full copy]

HAND OFF TO: reply-router for full draft
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Card Design Notes:**

- Keep it dense but scannable (use section headers with `━` dividers)
- Use exact quotes from original send and reply (no paraphrasing)
- Bold key numbers (headcount, job counts, reply date)
- Use intent emoji consistently
- Recommendation should point to NEXT ACTION, not assume response strategy (that's reply-router's job)

---

## Phase 8 — Update Memory

After generating the card:

1. **Update warm-leads.md:**
   - If contact NOT in warm-leads.md: add with appropriate priority
     - POSITIVE → P0 (immediate response)
     - SOFT → P1 (response within 1 day)
     - OBJECTION → P2 (route to reply-router, consider objection handling)
     - OPT-OUT → Do not add; add to Do Not Contact list in CLAUDE.md
   - If already in warm-leads.md: update status field with reply date and new priority

2. **Append to contact-lifecycle.md:**
   ```
   [contact name] | [company] | [email]
   [date] — Reply received (Touch [N]), context card generated. Intent: [classification]. Priority: [P0/P1/P2].
   ```

3. **Append to session/messages.md:**
   ```
   [timestamp] — Reply Context Card: [Name] at [Company] replied to Touch [N]. Intent: [classification]. Priority: [P0/P1]. Handed off to reply-router.
   ```

4. **Log to run-log.md:**
   Record: contact name, company, intent, priority, timestamp

---

## Learning Loop Integration

Follow `/mnt/Work/skills/_shared/learning-loop.md`. Each run:

1. **Log the card:** Add to `reply-context-card/run-log.md`
   - Contact name, company, intent classification, priority, timestamp
   - Conversion outcome if known (e.g., "→ meeting booked", "→ no reply")

2. **Track intent-to-outcome correlation** in `learned-patterns.md`:
   - How often does POSITIVE intent result in a booked meeting?
   - How often does SOFT convert (vs. drop)?
   - How often do OBJECTIONS convert with right response?
   - Which intents have highest conversion?

3. **Every 5th run:** Review patterns
   - Which intent classifications are most predictive of meetings?
   - Are there any false positives (e.g., SOFT that converts as fast as POSITIVE)?
   - Should priority thresholds be adjusted?

4. **Update learned-patterns.md** monthly with findings and recommendations

---

## Dependencies

| Dependency | File/Service | Usage |
|------------|--------------|-------|
| reply-classifier | `skills/reply-classifier/` | Triggers this skill when P0/P1 detected |
| Gmail MCP | Connected tool | Read thread history |
| Apollo MCP | Connected tool | Enrich company data + verify contact info |
| MASTER_SENT_LIST.csv | `/mnt/Work/` | Find send history |
| contact-lifecycle.md | `/mnt/Work/memory/` | Check prior history |
| warm-leads.md | `/mnt/Work/memory/` | Check/update warm lead priority |
| pipeline-state.md | `/mnt/Work/memory/` | Check recent activity |
| Batch trackers | `/mnt/Work/batches/active/` | Pull original sent message copy |
| reply-router | `skills/reply-router/` | Receives enriched context + drafts response |

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Contact NOT in MASTER_SENT_LIST | Log warning; note as "cold inbound" in card. Check warm-leads separately. |
| Batch tracker HTML not found | Use Gmail thread as source of truth for original message. |
| Apollo enrichment fails (e.g., invalid domain) | Omit company intel section; flag as "Manual company research needed" |
| Gmail thread not found | Log warning; only pull reply from classifier output. |
| Contact already in Do Not Contact list | Do not generate card; alert Rob immediately. |

---

## Success Metrics

- **Card generation time:** < 45 seconds per reply
- **Completeness:** All 8 sections populated (or explicitly marked "N/A" with reason)
- **Accuracy:** Contact name, title, company, and send history verified against source files
- **Intent classification accuracy:** Track in learned-patterns.md; target 95%+ accuracy
- **Conversion impact:** POSITIVE intents should result in 60%+ meeting rate (track monthly)

---

## Automation Boundary

This skill **does not** send anything. It only:
- Reads from files and APIs
- Prints the context card to conversation
- Updates memory files (warm-leads, contact-lifecycle, session messages)

The **reply-router** skill receives this enriched context and drafts the response. Rob must still approve the response before it's sent.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Mar 15, 2026 | Initial creation. 8-phase enrichment pipeline, intent classification, warm-lead integration. |

