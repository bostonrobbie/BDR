# T2 Draft — Touch 2 Follow-Up Email Skill

## Description
Drafts Touch 2 (T2) follow-up emails for contacts who received T1 emails in the TAM Outbound sequence. T2 tasks typically surface in Apollo on Day 5 from T1 send. This skill wraps the `memory/playbooks/t2-followup.md` playbook into an invokable workflow.

## Trigger
- "draft T2s for Wave N"
- "write follow-ups for [batch name]"
- "T2 tasks are due, draft them"
- Apollo task queue has Step 2 tasks pending

---

## Prerequisites
1. T1 was sent at least 4 days ago (HARD RULE — no T2 before Day 4, per INC-001)
2. Batch tracker HTML exists with T1 email drafts and proof points logged
3. Contacts are in Apollo sequence at Step 2

---

## Full Process

### Step 1: Identify Which T2s Are Due

Check Apollo for Step 2 tasks OR calculate from MASTER_SENT_LIST.csv:
```
Tool: apollo_contacts_search
q_keywords: "TAM Outbound"
sort_by_field: contact_last_activity_date
```
Then filter for contacts with send_date 5-8 days ago.

Or check the handoff.md for the T2 due date table.

### Step 2: Cadence Safety Check (MANDATORY)

For EACH contact:
1. Look up their T1 send date in MASTER_SENT_LIST.csv or batch tracker
2. Verify today is >= Day 4 from T1 send (not Day 1, 2, or 3)
3. If any contact is not yet Day 4: mark as HOLD. Do not draft.

**HARD RULE:** Touch 2 NOT before Day 4. Violating this was INC-001.

### Step 3: Pull T1 Content for Each Contact

For each contact due for T2, open their batch tracker HTML card and note:
- Which proof point was used in T1
- T1 subject line and body angle
- Contact's company, title, research notes
- Location (city/state) for any personalization

### Step 4: Draft T2 Using the Formula

**Word count:** 50-70 words
**Structure:**
1. Light callback to T1 (1 sentence — NOT "following up", NOT "did you see my email")
2. New angle + DIFFERENT proof point from T1 (1-2 sentences)
3. Engagement question (1 sentence — NOT "What day works" — save that for T1/T3)
4. Optional soft close (1 sentence)

**Subject line options:**
- "Quick thought on [Company]'s testing"
- "One more angle on [specific T1 topic]"
- Reply-thread style: "Re: [T1 subject]"

**Proof point rotation rule:**
- If T1 used Hansard → T2 uses CRED, Medibuddy, or Cisco
- If T1 used CRED → T2 uses Hansard, Cisco, or Fortune 100
- If T1 used Medibuddy → T2 uses Hansard, CRED, or Samsung
- Never repeat the same customer story from T1

**HC violations (auto-fail):**
- "Following up" / "just checking in" / "I haven't heard back" — banned
- "Did you see my last email" — banned
- Feature-led opener (AI, self-healing, NLP) — banned
- Em dashes — banned

### Step 5: QA Gate (T2 Modified Rubric — 7/9 to pass)

| # | Check | Pass Criteria |
|---|-------|--------------|
| 1 | Word count | 50-70 words |
| 2 | Question marks | 1-2 (exactly) |
| 3 | Different proof point | Not the same customer story as T1 |
| 4 | Light callback | Does NOT use "following up / checking in / did you see" |
| 5 | Named customer with numbers | Yes |
| 6 | Engagement question CTA | Open-ended question about their situation (not "what day works") |
| 7 | No placeholder text | Zero [COMPANY], {name}, etc. |
| 8 | No em dashes | Zero — characters |
| 9 | Conversational tone | Sounds like a person, not a template |

**Pass threshold: 7/9**

### Step 6: Add T2 Draft to Batch Tracker

Add a T2 section below the existing T1 card in the batch tracker HTML:

```html
<div class="email-draft" style="border-left-color: #28a745;">
  <p><strong>T2 Subject:</strong> {subject}</p>
  <p><strong>T2 Body:</strong> {body}</p>
  <p><strong>T2 QA:</strong> WC: {N} | QM: {N} | Proof: {customer} (different from T1: {T1 customer}) | MQS: {N}/9 | PASS</p>
</div>
```

Update the contact's badge to: "T2 Due [date]" (if not yet sent) or "T2 Sent [date]" (after send).

### Step 7: Present BATCH SUMMARY for APPROVE SEND

Tell Rob:
- How many T2 drafts ready
- Wave/batch they belong to
- Any cadence holds (contacts not yet at Day 4)
- Any proof point rotation issues flagged

Wait for explicit **APPROVE SEND** before pasting into Apollo.

### Step 8: Send via Apollo Task Queue

Per `memory/playbooks/apollo-task-queue-sends.md`:
1. Open Apollo Tasks tab → TAM Outbound → Step 2 tasks
2. For each task: paste T2 subject and body from tracker
3. Run mandatory 4-step pre-send verification (INC-012 Rule 12-C)
4. Click Send Now
5. Update tracker badge to "T2 Sent [date]"

---

## Output

- T2 drafts in batch tracker HTML (one section per contact)
- Updated status badges in tracker
- MASTER_SENT_LIST.csv rows (channel: "Apollo Email", batch: "TAM Outbound Batch N T2 Mar{DD}")

---

*Source: `memory/playbooks/t2-followup.md` (core formula) + INC-001 (cadence enforcement)*
*Version: 1.0 — 2026-03-13*
*Change log: v1.0 (Mar 13, 2026) — new skill created; wraps t2-followup.md playbook as invokable Cowork skill*
*When updating: increment version, add change log entry with date and what changed.*
