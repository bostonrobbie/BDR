# Contact Lifecycle Tracker — Unified Contact History

## Description
Maintains `memory/contact-lifecycle.md` as the single source of truth for every contact from first enrichment through final outcome. Consolidates data from MASTER_SENT_LIST.csv (495+ rows as of Mar 12, 2026), batch tracker HTML files, Apollo, and Gmail. Append-only timeline — never delete history.

## Trigger
- Run after any enrollment: "update lifecycle tracker for [batch name]"
- Run after any T1 or T2 send: "log send for [name]"
- Run after any reply: "log reply from [name]"
- Run on-demand: "show lifecycle for [name]", "contact history for [company]"
- Called during session handoff (auto-update from session activity)

## ⛔ APPROVE SEND RULE
This skill tracks and logs. It does NOT send anything. If a lifecycle record shows a contact is at ENROLLED stage and the T2 window has opened, the next step is to draft via `skills/tam-t1-batch/SKILL.md` and get Rob's APPROVE SEND — not to send directly.

---

## Stage Reference

| Stage | Meaning |
|-------|---------|
| DISCOVERED | Found during prospecting, not yet enriched |
| ENRICHED | Apollo enrichment complete, email obtained |
| COMPLIANCE_CLEAR | Passed all 8 compliance gate checks |
| DRAFTED | T1 email drafted, pending QA |
| QA_PASS | Draft passed MQS ≥9/12 |
| ENROLLED | Added to Apollo sequence `69afff8dc8897c0019b78c7e` |
| T1_SENT | First touch sent (email via Apollo UI) |
| T1_REPLIED | Replied to first touch |
| T2_SENT | Second touch (email via Apollo, Variant A formula) |
| T2_REPLIED | Replied to second touch |
| T3_SENT | Third touch (LinkedIn connection request) |
| T3_REPLIED | Accepted or replied to T3 |
| MEETING_BOOKED | Meeting scheduled |
| MEETING_HELD | Meeting completed |
| OPPORTUNITY | Qualified opportunity created |
| CLOSED_WON | Deal closed |
| CLOSED_LOST | Deal lost |
| DORMANT | No response after full sequence, cooling down |
| DNC | Do Not Contact |
| BOUNCED | Email invalid, no alternate found |

---

## Data Model (per contact record)

```markdown
### {Full Name} — {Company}
| Field | Value |
|-------|-------|
| Company | {company} |
| Domain | {domain} |
| Title | {title} |
| Email | {email} |
| Email Status | verified / catchall / unverified |
| Apollo ID | {id} |
| Account Type | Factor / TAM HIGH / TAM MEDIUM |
| TAM Domain Verified | Yes (in tam-accounts-mar26.csv) |
| Source | Apollo People Search / Sales Nav / Inbound |
| First Contact Date | {date} |
| Current Stage | {stage} |

**Timeline:**
| Date | Event | Detail | Session |
|------|-------|--------|---------|
| {date} | ENRICHED | Found via Apollo People Search | S{N} |
| {date} | COMPLIANCE_CLEAR | Passed 8-point gate | S{N} |
| {date} | ENROLLED | Sequence: TAM Outbound (`69afff8dc8897c0019b78c7e`) | S{N} |
| {date} | T1_SENT | Email — subject: "{subject}" | S{N} |
| {date} | T2_SENT | Email — subject: "{subject}" — Variant A formula | S{N} |
| {date} | REPLIED | Type: {positive/referral/timing/etc.} — "{snippet}" | — |
| {date} | MEETING_BOOKED | {date/time} | S{N} |
```

---

## Active Warm Lead Records (High Priority — always keep current)

These are tracked in `memory/contact-lifecycle.md` under "Active Warm Leads":

### Namita Jain — OverDrive (P1)
- Stage: T1_SENT
- T1 sent: Feb 27, 2026 (coverage angle)
- Monitoring for reply
- Domain: overdrive.com (TAM) | Apollo Org ID: 54a11f0f69702d8cccc4bf01

### Pallavi Sheshadri — Origami Risk (P2)
- Stage: T1_REPLIED (replied to premature T3 — INC-001)
- Rob sent follow-up Mar 2 (Hansard proof point, "what day works" CTA)
- Monitoring for reply. Nudge if no reply by Mar 7.
- Domain: origamirisk.com

### Evely Perrella — Aetna/CVS Health (P0 inbound)
- Stage: T1_SENT (with error — INC-012 wrong body delivered)
- Rob sent correction via Gmail Mar 12
- SKIP T2 (Rob already followed up manually)
- First eligible re-contact: Mar 19 (personalize before sending, needs Rob approval)
- Apollo Contact ID: 69b1dae03e09b90001402481

---

## Process: Updating the Lifecycle Log

### After Enrollment (most common update)

For each newly enrolled contact, append a record to `memory/contact-lifecycle.md`:

```markdown
### {First Last} — {Company}
| Field | Value |
|-------|-------|
| Company | {company} |
| Domain | {domain} |
| Title | {title} |
| Email | {email} |
| Email Status | {verified/catchall} |
| Apollo ID | {id from enrollment response} |
| Account Type | {Factor/TAM HIGH/TAM MEDIUM from tam-accounts-mar26.csv} |
| TAM Domain Verified | Yes |
| Source | Apollo People Search |
| First Contact Date | {today's date} |
| Current Stage | ENROLLED |

**Timeline:**
| Date | Event | Detail | Session |
|------|-------|--------|---------|
| {date} | ENRICHED | Apollo People Match | S{N} |
| {date} | COMPLIANCE_CLEAR | 8-point gate passed | S{N} |
| {date} | ENROLLED | Sequence: TAM Outbound | S{N} |
```

### After T1 Send

Update the contact record: change `Current Stage` from ENROLLED to T1_SENT, add timeline event:
```
| {date} | T1_SENT | Email — subject: "{actual subject line}" | S{N} |
```

Also add T2 due date note:
```
| — | T2_DUE | Target: {T1 date + 5-8 days} = {calculated date} | — |
```

### After Reply (from reply-classifier)

Update stage and add timeline event:
```
| {date} | T1_REPLIED | Type: positive — "Tuesday works for me" | — |
```

Change `Current Stage` to T1_REPLIED (or T2_REPLIED, etc.)

### After DNC Addition

```
| {date} | DNC | Reason: {hostile reply / polite decline / mabl-era} | S{N} |
```

Change `Current Stage` to DNC.

---

## Querying the Lifecycle Tracker

**By contact:** "Show lifecycle for Seth Drummond"
→ Find and display full contact record from contact-lifecycle.md

**By company:** "All contacts at Fidelity"
→ Search contact-lifecycle.md for "Fidelity" entries

**By stage:** "All contacts at T1_SENT stage"
→ Grep for `Current Stage | T1_SENT`, calculate days since send

**T2 overdue check:** "Show contacts with T1 sent more than 8 days ago and no T2 yet"
→ Filter T1_SENT contacts where T1 date is >8 days ago and no T2_SENT event exists

**Stale contact detection:** "Show contacts with no activity in 7+ days"
→ Check for contacts where most recent timeline event is >7 days old

---

## Bulk Contact Records

The 495 contacts in MASTER_SENT_LIST.csv are tracked at batch level in contact-lifecycle.md:

```
Batch 1: ~50 contacts, Feb 23, LinkedIn Connection, T3_SENT stage
Batches 2-5B: ~200 contacts, Feb-Mar, mixed channels, T1/T2/T3
TAM Outbound Mar 12: ~40 contacts, Mar 12, Email, ENROLLED/T1_SENT
Inbound Leads (bulk): ~15 contacts, Mar 12, Email, ENROLLED
```

For full individual records on bulk contacts, cross-reference their batch tracker HTML files.

---

## Storage Rules

- File location: `memory/contact-lifecycle.md`
- APPEND-ONLY for timeline events — never delete or rewrite history
- Stage fields CAN be updated (e.g., ENROLLED → T1_SENT → T1_REPLIED)
- Timeline entries CANNOT be deleted
- DNC entries in `contact-lifecycle.md` mirror `CLAUDE.md` — if they diverge, `CLAUDE.md` is authoritative

---

## Integration Points
- Updated by: `skills/apollo-enroll/SKILL.md` (after enrollment), `skills/reply-classifier/SKILL.md` (after reply logging), `skills/handoff-auto/SKILL.md` (end-of-session update)
- Read by: `skills/batch-dashboard/SKILL.md`, `skills/analytics-engine/SKILL.md`, `skills/reply-router/SKILL.md`
- Sources: `MASTER_SENT_LIST.csv`, batch tracker HTML files, `memory/warm-leads.md`, Apollo MCP, Gmail MCP

*Source: `memory/playbooks/tam-t1-batch.md` + `memory/warm-leads.md` + `memory/pipeline-state.md`*
*Last updated: 2026-03-12 (initialized Session 30, 495 contacts tracked at batch level)*
