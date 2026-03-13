# Playbook: T2 Follow-Up Drafting

## When to Use
When T2 (Touch 2) tasks surface in Apollo's task queue, typically Day 5-8 after T1 was sent.

---

## Cadence Rules

| Touch | Earliest | Typical | Latest |
|-------|----------|---------|--------|
| T2 | Day 4 from T1 | Day 5 from T1 | Day 8 from T1 |

**HARD RULE:** Touch 2 NOT before Day 4 of the sequence. Violating this was INC-001.

---

## T2 Email Formula (from sop-tam-outbound.md Part 7)

### Structure (4 parts, 50-70 words):

1. **Light callback to T1** (1 sentence): Reference your previous email without being pushy. Do NOT say "I haven't heard back" or "Did you get my last email."
   - Good: "Circling back on the testing challenge I mentioned last week."
   - Good: "One more thought on {Company}'s regression coverage."
   - Bad: "Just following up on my previous email."
   - Bad: "I wanted to check if you saw my message."

2. **New angle or proof point** (1-2 sentences): Must be DIFFERENT from the T1 email. Check the batch tracker for which proof point was used in T1 and pick a different one.

3. **Engagement question** (1 sentence): Ask a question that's easy to answer and relevant to their role. NOT "What day works" (that's T1's CTA).
   - Good: "How are you handling regression testing as your team scales?"
   - Good: "Is test maintenance eating into your team's sprint velocity?"
   - Good: "Curious, how much of your test suite runs on every PR?"

4. **Soft close** (optional, 1 sentence): Brief. "Happy to share what we're seeing" or just let the question hang.

### Word count: 50-70 words

### Subject line: Lighter tone
- "Quick thought on {Company}'s testing"
- "One more angle on {specific thing from T1}"
- Reply-style: "Re: {T1 subject}" (only if the email thread supports it)

---

## Process

### Step 1: Check which T2s are due
Open Apollo Tasks tab. Filter by sequence "TAM Outbound" and look for Step 2 tasks.

Or calculate from MASTER_SENT_LIST.csv:
- Find all contacts with send_date 5-8 days ago
- Those are due for T2

### Step 2: Pull T1 content for each contact
Open the relevant batch tracker HTML. For each contact due for T2:
- Read their T1 subject and body
- Note which proof point was used
- Note their company, title, and any research notes

### Step 3: Draft T2 for each contact
Using the formula above:
- Pick a DIFFERENT proof point from T1
- Write the 4-part structure
- Keep to 50-70 words
- Use an engagement question CTA

### Step 4: QA Gate the T2
Modified QA gate for T2:

| # | Check | Points |
|---|-------|--------|
| 1 | Word count 50-70 | 1 |
| 2 | 1-2 question marks | 1 |
| 3 | Different proof point from T1 | 1 |
| 4 | Light callback (not "following up") | 1 |
| 5 | Named customer with numbers | 1 |
| 6 | Engagement question CTA | 1 |
| 7 | No placeholder text | 1 |
| 8 | No em dashes | 1 |
| 9 | Conversational tone | 1 |

**Pass threshold:** 7/9

### Step 5: Add to tracker or create T2 draft file
Either:
- Add T2 draft section to the existing batch tracker HTML (below each contact's T1 draft)
- Or create a separate T2 draft file: `tamob-wave{N}-t2-drafts-{date}.html`

### Step 6: Present for APPROVE SEND
Same as T1: show Rob the drafts, wait for APPROVE SEND, then paste into Apollo and send.

---

## T2 Proof Point Selection

If T1 used Hansard, T2 should use one of: CRED, Medibuddy, Cisco, Fortune 100, Samsung
If T1 used CRED, T2 should use one of: Hansard, Cisco, Medibuddy, Fortune 100
(etc.)

**Rule of thumb:** Different customer story, different metric, but relevant to the same industry if possible.

---

## Batch Processing Tips

For large T2 batches (20+ contacts):
- Group by company first (all Fidelity T2s together, all Commvault T2s together)
- Ensure no company gets the same T2 proof point twice
- Process in order: highest-priority accounts first
- Commit after every 5 drafts (mid-session commit protocol)

---

---
*Version: 1.0 — 2026-03-12*
*Change log: v1.0 (Mar 12, 2026) — consolidated from Sessions 11, 20, 22, sop-tam-outbound.md Part 7*
*When updating: increment version, add change log entry with date and what changed.*
