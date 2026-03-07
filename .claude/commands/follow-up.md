# Follow-Up - Check what's due and draft follow-up touches

You are Rob's BDR assistant. The user wants to see what follow-ups are due and draft them.

## Files to Load
- `work/follow-up-schedule.json` — computed follow-up dates per batch
- `work/pipeline-state.json` — credit count, batch statuses, warm leads
- `work/dnc-list.json` — check before drafting any follow-up
- `.claude/rules/message-structure.md` — writing rules, proof points, close construction
- `.claude/rules/safety.md` — cadence enforcement (date-gating rules)

## Process

### Step 1: Load pipeline state
Read `work/pipeline-state.json` and `work/follow-up-schedule.json`. Compute:
- Which prospects are due for Touch 2 today (Day 5 from Touch 1)?
- Which prospects are due for Touch 3 today (Day 10 from Touch 1)?
- Check credit budget: how many InMail credits remain?

### Step 2: Check the reply log
Read `work/reply-log.csv`. Identify:
- Prospects who replied (need response handling, suggest `/reply-handle`)
- Prospects with no reply whose next touch is due

### Step 3: Check DNC list
Read `work/dnc-list.json`. Exclude any prospect on the DNC list from follow-ups.

### Step 4: Check cadence safety
Read `.claude/rules/safety.md`. For each prospect:
- Verify today >= touch2_eligible_date (touch1_sent + 4 days) before drafting Touch 2
- Verify today >= touch3_eligible_date (touch1_sent + 9 days) before drafting Touch 3
- **If today < eligible date, do NOT draft. Report as "not yet eligible."**

### Step 5: Generate the due list
Show Rob a table:
| Prospect | Company | Batch | Last Touch | Last Sent | Next Due | Next Touch Type | Eligible? |
Sort by priority score, then by days overdue.

### Step 6: Draft follow-up touches

**Touch 2 (InMail Follow-up, Day 5):** 40-70 words
- Read the original Touch 1 from the batch tracker to ensure DIFFERENT angle/proof point
- Reference reaching out before but keep it light ("Circling back quick...")
- New proof point or capability match
- Lighter close tied to the new proof point, still uses "what day works"
- Run through QA gate (load `.claude/rules/outbound-intelligence.md` for HC/MQS checks)

**Touch 3 (Email, Day 10):** 60-100 words
- Fresh approach, DIFFERENT proof point from Touches 1 and 2
- Slightly more direct than InMail
- Subject line: 5-6 words, problem-framed
- Only draft if prospect has a verified email address

### Step 7: Score each draft
Run: `python scripts/score_message.py --text "MESSAGE_TEXT"` or use the inline QA gate.
All drafts must score MQS >= 9/12. Auto-rewrite if below threshold.

### Step 8: Update tracking
After Rob confirms which follow-ups to send:
- Update `work/follow-up-schedule.json` with new touch status
- Update `work/pipeline-state.json` with credit count changes
- Log to `work/reply-log.csv` if any status changes

## Rules
- Each follow-up MUST use a DIFFERENT proof point than the previous touch
- Touch 2 should reference "circling back" lightly but add NEW value
- If a prospect replied at any point, STOP the sequence (suggest `/reply-handle`)
- If credits < 10, only draft Touch 2 for Hot/Warm prospects. All Touch 3 emails proceed (free).
- 3-touch cadence: Touch 1 (InMail Day 1) → Touch 2 (InMail Day 5) → Touch 3 (Email Day 10). No cold calls.
