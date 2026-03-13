# Handoff Auto — Session Close & Handoff Docs

## Description
Auto-generates the end-of-session handoff documentation by analyzing the current session's activity. Produces the 5-file handoff from `memory/playbooks/session-handoff.md`: updates `handoff.md`, `work-queue.md`, `session-log.md`, clears `in-progress.md`, and deregisters from active sessions. The #1 cause of inter-session information loss is skipping or shortcutting handoff.md. This skill prevents that.

## Trigger
- Run at the END of every session: "close session", "handoff", "wrap up", "done for today"
- LAST skill called before deregistering
- Run even if the session was short — always document

## ⛔ APPROVE SEND RULE
Any outreach pending Rob's APPROVE SEND must be explicitly listed in the handoff summary and work-queue.md as a pending item. The next session must NOT send anything without going through the full approval process again. Pending sends do not carry over automatically.

---

## Priority Order (if running low on context)

Per `memory/playbooks/session-handoff.md`:
1. **handoff.md** — Most critical. Next session reads this first.
2. **work-queue.md** — New tasks discovered this session
3. **session-log.md** — Chronological record
4. **in-progress.md** — Clear it
5. **Active session deregister** — Clean up

---

## Step 1: Gather Session Activity

Scan the conversation history to extract:

**Contacts touched:**
- New contacts enriched (names, companies, titles, emails, Apollo IDs)
- Contacts enrolled in TAM Outbound sequence (`69afff8dc8897c0019b78c7e`)
- T1 emails sent (and whether Apollo auto-sent Step 1 — check for INC-009)
- T2 emails sent
- Replies handled, warm leads updated
- DNC additions (if any — verify Rob approved)
- Blocked/skipped contacts with reasons

**Files changed:**
- Batch tracker HTML files created or updated (`tamob-batch-*.html`)
- MASTER_SENT_LIST.csv rows added (verify count with `wc -l`)
- Memory files updated (`warm-leads.md`, `contact-lifecycle.md`, etc.)

**Apollo incidents to note:**
- Any auto-sends (INC-009: check `current_step_position` after enrollment)
- Any ownership-blocked contacts (cannot fix via API — must flag for Rob)
- Any override flags used (`sequence_active_in_other_campaigns`, `sequence_same_company_in_same_campaign`, etc.)

**Pending items:**
- Contacts enrolled but APPROVE SEND not yet given
- T2 due dates (calculate: T1 send date + 5-8 days = T2 due window)
- Warm lead follow-ups needed
- Any compliance flags that Rob needs to decide

---

## Step 2: Update handoff.md (MOST CRITICAL)

Read current `memory/session/handoff.md`, then append a new section.

```markdown
---

## Session {N} — {1-line title} ({date})

**What was done:**
{2-3 sentences covering what was accomplished}

### {Batch Name} (e.g., "TAM Outbound Batch 7 Mar12")
Enrolled {N} contacts in sequence `69afff8dc8897c0019b78c7e`, send-from `robert.gorham@testsigma.com`

| Name | Company | Apollo ID | Email | Stage | T2 Due | Notes |
|------|---------|-----------|-------|-------|--------|-------|
| {first last} | {company} | {apollo_id} | {email} | ENROLLED/T1_SENT | {date} | {any flags} |

**Override flags used:** {e.g., sequence_same_company_in_same_campaign: true for all contacts at Fidelity}
**Blocked contacts:** {name (company) — reason}
**Apollo auto-send check:** {Step 1 was/was NOT auto-sent — current_step_position was 1/2}

### Warm Leads Status
| Name | Company | Type | Last Touch | Next Step |
|------|---------|------|------------|-----------|
| Namita Jain | OverDrive | Warm inbound (webinar x2) | T1 Feb 27 | Monitor; T2 InMail if no reply by Mar 4 |
| Pallavi Sheshadri | Origami Risk | Reply to premature T3 | Rob's follow-up Mar 2 | Monitor; nudge if no reply by Mar 7 |
| Evely Perrella | Aetna/CVS Health | Inbound (INC-012) | Rob's correction Mar 12 | Skip T2. Re-contact Mar 19 earliest. |
| {any new additions} | | | | |

### Next Session Guidance
- **First priority:** {most urgent item — T2 due, warm lead, new batch, etc.}
- **Second priority:** {next item}
- **Pending APPROVE SEND:** {any contacts enrolled but not yet sent — MUST get Rob's APPROVE SEND before sending}
- **Blockers:** {ownership issues, catchall domains, unresolved decisions}
```

**Self-check:** Could a brand-new session execute T2 follow-ups for these contacts using ONLY this section of handoff.md? If not, add more detail before writing.

---

## Step 3: Update work-queue.md

Read current `memory/session/work-queue.md`. Mark completed tasks, add new ones.

**Format for completed tasks:**
```markdown
### TASK-{XXX}: {description}
**Status:** ✅ DONE ({date}, Session {N})
```

**Format for new tasks:**
```markdown
### TASK-{XXX}: {description}
**Status:** UNCLAIMED
**Priority:** P0/P1/P2/P3
**Effort:** ~{N} min
**Output:** {filename or "Report in chat"}

{Full context so next session can execute without asking questions.
Include: which contacts, which files, which sequence, what Rob approved, what's still pending.}
```

**Common new tasks generated by a TAM batch session:**
- "T2 drafts due {date} for {N} contacts from {batch name} — T1 sent {date}"
- "Warm lead follow-up: {name} at {company} — {next step}"
- "Pending APPROVE SEND: {batch name} — {N} contacts enrolled, awaiting Rob's go-ahead"
- "Apollo ownership: {name} at {company} — must reassign in UI before enrollment"
- "T2 Variant A: draft for {name} at {company} using {proof point} — different from T1 proof point {other story}"

---

## Step 4: Append to session-log.md

```markdown
## Session {N} — {1-line title} ({date})

**Task:** {TASK-XXX or "ad-hoc"}
**Duration:** ~{N} min
**What was done:**
- {accomplishment with specifics — how many contacts, which companies, what proof points}
- {files created/updated}
- {decisions or incidents}

**Files changed:**
- {tamob-batch-mar12-X.html — created, N contacts}
- {MASTER_SENT_LIST.csv — N rows added, now {total} rows total}
- {memory/warm-leads.md — updated Namita Jain record}

**Contacts enrolled:** {N}
| Name | Company | Apollo ID | Email | Status |
|------|---------|-----------|-------|--------|
| {data for each contact} |

**Incidents:**
- {INC-XXX if applicable}

**Notes:**
- {Catchall domain flags: company.com is catchall}
- {Override flags used}
- {Apollo auto-send: yes/no}

**Next:** {First thing next session should do}
```

---

## Step 5: Clear in-progress.md

```markdown
# In-Progress Checkpoint

**Status:** CLEAR
**Last completed task:** {description}
**Cleared by:** Session {N} on {date}
```

---

## Step 6: Deregister from Active Sessions

If you created a session registration in `memory/session/active/`:
```bash
rm /Work/memory/session/active/{session-number}.json

# Release any file locks
ls /Work/.locks/*.lock 2>/dev/null
rm /Work/.locks/*.lock 2>/dev/null
```

---

## Step 7: MASTER_SENT_LIST.csv Verification

Before writing the DONE/CLAIM message, always verify the row count:
```bash
wc -l /Work/MASTER_SENT_LIST.csv
```

State the EXACT count in the handoff. Never estimate. Per `memory/playbooks/dedup-protocol.md`: "Always run `wc -l MASTER_SENT_LIST.csv` and confirm the count matches expectations."

---

## Step 8: Summary to Rob

```
SESSION {N} HANDOFF COMPLETE — {date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DONE:
  ✅ {accomplishment 1 with specifics}
  ✅ {accomplishment 2}

MASTER_SENT_LIST: {N} total rows (verified)

⛔ PENDING APPROVE SEND:
  • {batch name} — {N} contacts enrolled, awaiting your APPROVE SEND to send T1s
  [OR: nothing pending — T1s were sent / APPROVE SEND was given]

WARM LEADS TO WATCH:
  • Namita Jain (OverDrive) — P1. Monitor for reply.
  • Pallavi Sheshadri (Origami Risk) — P2. Nudge if no reply by Mar 7.
  • {any new additions}

NEXT SESSION — First priority:
  1. {most urgent}
  2. {second priority}

FILES UPDATED:
  📝 memory/session/handoff.md — new section for Session {N}
  📝 memory/session/work-queue.md — {N} tasks completed, {N} new tasks
  📝 memory/session/session-log.md — entry appended
  📝 memory/session/in-progress.md — cleared

Reminder: Run `git add -A && git commit -m "Session {date}: {1-line summary}"` from your terminal.
```

---

## Common Mistakes (from `memory/playbooks/session-handoff.md`)

1. Updating only the handoff.md header — the BODY needs the detailed contact table too
2. Not adding T2 due dates to work-queue.md as new tasks
3. Forgetting to clear in-progress.md
4. Non-standard batch names: NEVER use "B7" or "W6B1" — always `TAM Outbound Batch {N} Mar{DD}`
5. Row count mismatch — always run `wc -l MASTER_SENT_LIST.csv` right before the DONE message
6. Wrong timestamps — use `date -u` from bash, not an estimate
7. Skipping handoff.md entirely because the session was short — even 1 contact enrolled needs a handoff

---

## Integration Points
- Called at: END of every session (last step)
- Reads: All session activity, `memory/session/*.md` files
- Writes: `memory/session/handoff.md`, `memory/session/work-queue.md`, `memory/session/session-log.md`, `memory/session/in-progress.md`
- Deletes: Active session file, file locks

*Source: `memory/playbooks/session-handoff.md` (10 common mistakes, 6-step checklist)*
*Last updated: 2026-03-12 (Session 30)*
