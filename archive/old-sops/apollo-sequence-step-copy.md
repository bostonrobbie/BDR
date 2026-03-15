# Apollo Sequence Step Copy Guide
**Last Updated:** Feb 27, 2026
**Sequences Covered:** Q1 Priority Accounts, Q1 QA Outreach, Email-Only (new)

---

## Sequence 1: Q1 Priority Accounts (ID: 69a05801fdd140001d3fc014)

**Purpose:** Intent-based and transferred account outreach. All steps MANUAL.
**Cadence:** 4 touches over 15 days (2 InMail + 1 Email + 1 Phone Call)

### Step 1: LinkedIn InMail (Day 1, High Priority)
**Template Source:** TEMPLATE_LIBRARY.md — LI- series (select by pain hook)
**Word Count:** 80-120 words
**Structure:** C2 Message Structure (5 elements: subject, opener, context, proof point, close)

**Template Selection Guide:**
| Prospect Signal | Use Template | Pain Hook |
|----------------|-------------|-----------|
| On Selenium/Cypress/Playwright | LI-1 (Maintenance) | Test Maintenance |
| Fast-shipping, release pressure | LI-2 (Velocity) | Release Velocity |
| Scaling team, growing product | LI-3 (Coverage) | Coverage/Scale |
| On TOSCA/Katalon/Provar | LI-4 (Migration) | Tool Migration |
| Recent migration/acquisition/hiring | LI-5 (Trigger) | Trigger Event |

**Personalization Variables:**
- `[Name]` — First name
- `[their_change_event]` — Specific company event from research (migration, launch, rebuild)
- `[their_situation]` — Their product, platform, or team context
- `[their_deadline]` — Any known timeline (quarter end, launch date, compliance deadline)
- `[CurrentTool]` — Their current test tool (from Apollo tech stack enrichment)

**Copy-Paste Instructions:**
1. Select template by pain hook (match to research)
2. Fill all personalization variables from prospect card
3. Run Pre-Draft Steps 1-4
4. Verify MQS >= 9/12
5. Paste into LinkedIn Sales Navigator InMail composer

---

### Step 2: LinkedIn InMail Follow-up (Day 5, High Priority)
**Template Source:** TEMPLATE_LIBRARY.md — LI-FU series
**Word Count:** 40-70 words
**Structure:** Loose (no full 5-element required)

**Rules:**
- DIFFERENT proof point than Step 1
- Reference prior outreach lightly ("Circling back quick...")
- New angle or new customer story
- Close still ties to proof point outcome + "what day works"

**Template Framework:**
```
Hi [Name],

Circling back quick. [New_angle_one_sentence].

[Different_customer] [different_outcome_with_number] after [what_they_did].

If [outcome_reframed_for_them] would help, what day works for a quick look?

Rob
```

---

### Step 3: Manual Email (Day 10, Medium Priority)
**Template Source:** TEMPLATE_LIBRARY.md — EM- series (select by pain hook, DIFFERENT from Step 1)
**Word Count:** 60-100 words
**Structure:** Problem question → Context → Proof point → "What day works" close

**Template Selection Guide:**
| If Step 1 Used | Step 3 Should Use |
|---------------|-------------------|
| LI-1 (Maintenance) | EM-2 (Velocity) or EM-3 (Coverage) |
| LI-2 (Velocity) | EM-1 (Maintenance) or EM-4 (Migration) |
| LI-3 (Coverage) | EM-1 (Maintenance) or EM-2 (Velocity) |
| LI-4 (Migration) | EM-3 (Coverage) or EM-5 (Trigger) |
| LI-5 (Trigger) | EM-1 (Maintenance) or EM-3 (Coverage) |

**Email-Specific Rules:**
- Subject: 5-6 words, problem-framed
- No "circling back" or "following up on my LinkedIn message" (channel switch, fresh start)
- Can be slightly more direct than InMail
- 1-2 question marks

**Copy-Paste Instructions:**
1. Select template (different pain hook from Step 1)
2. Fill personalization variables
3. Send from one of Rob's 4 Apollo email accounts (rotate)
4. Send window: 11:30 AM - 1:30 PM recipient local time

---

### Step 4: Phone Call (Day 15, Medium Priority)
**Template Source:** Meeting Prep Card from batch tracker
**Purpose:** Discovery call, reference previous 3 touches

**Call Script Framework:**
```
"Hey [Name], this is Rob from Testsigma. I sent you a couple notes about
[proof_point_topic] and wanted to see if that resonated.

[Pause for response]

If yes: "Great, can I ask what your team's setup looks like right now?"
If no/cold: "No worries. Quick question, what's your biggest testing challenge right now?"
If voicemail: "Hey [Name], Rob from Testsigma. Sent you a note about
[outcome_from_proof_point]. If [their_situation] is on your radar,
I'd love 15 minutes. My number is [Rob's number]."
```

---

## Sequence 2: Q1 QA Outreach (ID: 699f4089628b940011da7fb7)

**Purpose:** Cold outbound sequence for batch prospects. 3-touch cadence.
**Cadence:** 3 touches over 10 days (2 InMail + 1 Email)
**Status:** Currently INACTIVE/Draft — to be activated with updated copy

### Step 1: LinkedIn InMail (Day 1)
Same as Q1 Priority Accounts Step 1. Use LI- template series.

### Step 2: LinkedIn InMail Follow-up (Day 5)
Same as Q1 Priority Accounts Step 2. Use LI-FU template framework.

### Step 3: Email (Day 10)
Same as Q1 Priority Accounts Step 3. Use EM- template series (different pain hook from Step 1).

---

## Sequence 3: Email-Only (NEW — for BDR-wide Apollo use)

**Purpose:** Standalone email sequence for team-wide prospecting. No InMail dependency.
**Cadence:** 5 touches over 21 days (all email)
**Apollo Configuration:**
- Send window: 11:30 AM - 1:30 PM recipient local time
- Daily limit per mailbox: 25 emails
- Mailbox rotation: All 4 accounts
- Open tracking: ON | Click tracking: OFF

### Step 1: Problem Hook (Day 1)
**Template Source:** EM-1 through EM-5 (select by pain hook)
**Word Count:** 60-100 words

Select template based on prospect research:
| Pain Signal | Template |
|-------------|----------|
| Test maintenance overhead, broken locators | EM-1 |
| Release delays, regression bottleneck | EM-2 |
| Growing product, coverage gaps | EM-3 |
| Tool frustration (Selenium, TOSCA, etc.) | EM-4 |
| Recent trigger event (migration, hiring, etc.) | EM-5 |

### Step 2: Value Add (Day 4)
**Template Source:** EM-FU-1
**Word Count:** 40-70 words

Reply to original thread. New proof point, different customer story.
Must NOT repeat the pain hook from Step 1.

### Step 3: Social Proof (Day 9)
**Template Source:** EM-FU-2
**Word Count:** 60-100 words

Fresh subject line. Customer story focus with specific numbers.
Match proof point to prospect's vertical.

### Step 4: Trigger/Timely (Day 14)
**Template Source:** EM-FU-3
**Word Count:** 40-70 words

Reference recent company event, industry trend, or new Testsigma feature.
Lighter tone, still ends with "what day works."

### Step 5: Direct Ask (Day 21)
**Template Source:** EM-FU-4
**Word Count:** 40-60 words

Shortest touch. One sentence of value. Confident close.
"Wanted to give this one more try. If [stat] would help [situation], what day works?"

---

## Proof Point Rotation Matrix (Across Touches)

Never repeat a proof point within the same prospect's sequence.

| Touch 1 Proof Point | Touch 2 | Touch 3 | Touch 4-5 |
|---------------------|---------|---------|-----------|
| Hansard (8wk → 5wk) | Medibuddy (2,500 tests, 50% cut) | CRED (90% automation, 5X faster) | Spendflo (50% manual cut) |
| Sanofi (3 days → 80 min) | Hansard (8wk → 5wk) | Spendflo (50% manual cut) | Cisco (35% regression reduction) |
| Medibuddy (2,500 tests) | Sanofi (3 days → 80 min) | 70% maintenance vs Selenium | Nagra DTV (2,500 in 8mo) |
| 70% vs Selenium | CRED (90% automation) | Hansard (8wk → 5wk) | Medibuddy (2,500 tests) |
| Spendflo (50% cut) | 70% vs Selenium | Sanofi (3 days → 80 min) | Fortune 100 (3X productivity) |

---

## QA Gate Reminder (All Sequences)

Every message across all 3 sequences must pass before sending:
1. HC1-HC10 scan (zero violations)
2. MQS >= 9/12
3. Word count within range
4. Exactly 2 question marks (Touch 1) or 1-2 (follow-ups)
5. No structural duplicates across the batch
6. Close ties proof point outcome to prospect's situation + "what day works"
7. Max 1 hyphen in body (excluding sign-off)
8. 4+ paragraph breaks for readability
9. No toxic phrases
10. Research from all 3 sources (LinkedIn, Apollo, Company external)
