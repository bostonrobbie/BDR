# Compliance Gate — Pre-Enrollment Safety Check

## Description
6-point dedup check (from `memory/playbooks/dedup-protocol.md`) plus 2 additional safety checks before any contact goes into the TAM Outbound Apollo sequence. Run this for every contact, every time. No exceptions. Since March 10, 2026 (protocol active), zero duplicates in TAM Outbound. This skill keeps it that way.

**Two-Phase Dedup Protocol:** Run the 8 checks during batch build (Phase 1). Then immediately before each enrollment API call, re-run Check 1 (MASTER_SENT_LIST grep) as Phase 2. Concurrent sessions can enroll the same contact between Phase 1 and Phase 2. Phase 2 takes under 2 seconds and prevents race-condition duplicates.

## Trigger
- Before enrolling ANY contact in Apollo
- Called from `skills/enrichment-pipeline/SKILL.md` (Step 4) and `skills/apollo-enroll/SKILL.md` (Step 1)
- Run manually: "run compliance gate for [name]" or "check [name] before enrolling"

## ⛔ APPROVE SEND RULE
This skill does NOT send anything. But it gatekeeps enrollment, which leads to sends. No contact passes this gate unless all 8 checks are CLEAR. Any BLOCKED contact must be flagged to Rob with the reason before any further action.

---

## The 8 Checks (Run ALL — stop and report on any failure)

### Check 1: MASTER_SENT_LIST.csv
The central record of every contact ever sent outreach. CSV columns: `name,batch,send_date,channel,credits,file,norm`

```bash
grep -i "jason lieberman" /Work/MASTER_SENT_LIST.csv
```

**If found:** BLOCKED. Already contacted. Do NOT enroll again unless Rob explicitly approves re-engagement AND it's been 60+ days since last touch.

Edge cases:
- Name variations ("Jason A. Lieberman" vs "Jason Lieberman"): verify same company before calling it a match
- Same name, different company: check the batch column to confirm different person before clearing

### Check 2: DNC List
**⚠️ ALWAYS read the live DNC list from `CLAUDE.md` — do NOT rely on any cached copy.** The list below was accurate as of Mar 12, 2026 but new entries are added after every negative reply. The authoritative source is `CLAUDE.md` → "Do Not Contact List" section. Read it fresh every session.

Current entries as of Mar 12, 2026 (verify against CLAUDE.md):
- Sanjay Singh (ServiceTitan) — hostile reply. Permanent.
- Lance Silverman (Batch 5B) — polite decline, re-engage after 60+ days with new trigger only
- Clyde Faulkner (CAMP Systems) — mabl-era customer. Permanent.
- Ashok Prasad (ZL Technologies) — mabl-era contact. Permanent.
- Abe Blanco (Kapitus) — replied "not interested" Mar 4. Permanent.
- Chuck Smith (Aventiv Technologies) — double-send incident. Permanent.
- Jitesh Biswal (JPMorgan Chase) — declined InMail Nov 4. Permanent.

**If found:** BLOCKED. Do not contact. For "re-engage after 60+ days" entries, verify the last contact date in MASTER_SENT_LIST before proceeding.

### Check 3: Apollo Contacts Search
```
Tool: apollo_contacts_search
q_keywords: "{First Last} {Company}"
per_page: 5
```

Look at `emailer_campaign_ids` and `contact_campaign_statuses[].status` in the response.

Decisions:
- In TAM Outbound sequence `69afff8dc8897c0019b78c7e`, status active → BLOCKED (already enrolled)
- In a different sequence, active → FLAG to Rob; will need `sequence_active_in_other_campaigns: true` override at enrollment
- Finished/failed in another sequence → PROCEED with `sequence_finished_in_other_campaigns: true`
- Found in Apollo, no sequence → PROCEED; note their Apollo ID for enrollment (skip create step)
- Not found in Apollo → PROCEED; create new contact with `run_dedupe: true`

### Check 4: Current Batch Duplicate Check
Before adding a contact to the batch, confirm they're not already on your current working list. Catches copy-paste errors.

Scan the batch tracker HTML currently in progress for the same name or email.

**If found:** BLOCKED. Do not add twice.

### Check 5: Same-Company Check
Not a hard block, but required before proceeding:
- How many contacts from this company are already enrolled in TAM Outbound?
- Each contact at the same company MUST get a different proof point (enforced in draft-qa Check 11)
- If 5+ contacts already targeted at one company, flag to Rob before adding more

### Check 6: TAM Domain Verification (MANDATORY — INC-010)
This caused a real incident (INC-010). Every contact's email domain MUST appear in `tam-accounts-mar26.csv`.

```bash
grep -i "epicor.com" /Work/tam-accounts-mar26.csv
```

**If NOT found:** HARD BLOCKED. This contact is not from a TAM or Factor account. Do NOT enroll in TAM Outbound. Period.

**If found:** Note whether it's a Factor account (38 accounts) or TAM account (312 accounts). Factor = higher priority.

For bulk domain verification:
```bash
cd /Work
for domain in "epicor.com" "beyondtrust.com" "northerntrust.com"; do
  result=$(grep -i "$domain" tam-accounts-mar26.csv)
  if [ -n "$result" ]; then
    echo "TAM OK: $domain"
  else
    echo "NOT TAM: $domain — DO NOT ENROLL"
  fi
done
```

### Check 7: Reply History Check
Before enrolling, check Gmail for any prior replies from this contact's email domain:
```
Tool: gmail_search_messages
q: "from:domain.com to:robert.gorham@testsigma.com"
maxResults: 5
```

- Prior negative reply or "not interested" → BLOCKED, escalate to Rob
- OOO reply → Note and proceed (flag for timing awareness)
- Positive/curious reply from a different person at same company → Flag to Rob; they may need warm-lead handling instead

### Check 8: Cadence Safety Check
Applies when re-enrolling a contact or evaluating T2/T3 timing:
- T2 email: NOT before Day 4 from T1 send date (INC-001)
- T3 connection request: NOT before Day 9 from T1 send date (INC-001)
- Re-enrollment: 60+ days from last outreach before starting a new T1

Check `MASTER_SENT_LIST.csv` for the last send date and `contact-lifecycle.md` if the contact has a record.

---

## Bulk Dedup (10+ contacts)

```bash
cd /Work

# Check all names at once against master list
for name in "Jason Lieberman" "Les Stickney" "Holly Shubaly"; do
  result=$(grep -i "$name" MASTER_SENT_LIST.csv)
  if [ -n "$result" ]; then
    echo "DUPLICATE: $name — $result"
  else
    echo "CLEAN: $name"
  fi
done
```

---

## Decision Matrix

| Check 1 | Check 2 | Check 3 | Check 6 | Result |
|---------|---------|---------|---------|--------|
| Not found | Not found | Not found | Found | PROCEED — create + enroll |
| Not found | Not found | Found, no sequence | Found | PROCEED — enroll existing |
| Not found | Not found | Found, in TAM seq (active) | Found | BLOCKED — already enrolled |
| Not found | Not found | Found, in other seq (active) | Found | PROCEED with `sequence_active_in_other_campaigns: true` |
| Not found | Not found | Found, finished other seq | Found | PROCEED with `sequence_finished_in_other_campaigns: true` |
| Found | — | — | — | BLOCKED — already contacted |
| — | Found | — | — | BLOCKED — DNC list |
| — | — | — | Not found | BLOCKED — not a TAM account |

---

## Output Format (report per contact)

```
COMPLIANCE GATE: Jason Lieberman (Epicor, jason.lieberman@epicor.com)
Check 1 — MASTER_SENT_LIST: CLEAR (not found)
Check 2 — DNC list: CLEAR
Check 3 — Apollo: Found (ID: 5e66b638...), no active sequence — PROCEED, use existing ID
Check 4 — Batch dedup: CLEAR
Check 5 — Same-company: 1 other contact at Epicor (Seth Drummond) — different proof point required
Check 6 — TAM domain: epicor.com → found in tam-accounts-mar26.csv (TAM HIGH) — CLEAR
Check 7 — Reply history: No prior replies from epicor.com — CLEAR
Check 8 — Cadence: First contact — CLEAR

VERDICT: ✅ CLEAR — proceed to enrollment
Apollo record: existing (ID: 5e66b638...) — enroll directly, skip create step
Override flags needed: sequence_same_company_in_same_campaign: true (Seth Drummond at same company)
```

Or if blocked:
```
COMPLIANCE GATE: Sanjay Singh (ServiceTitan)
Check 2 — DNC: BLOCKED — hostile reply (mabl era 2022), added Feb 27. Permanent.

VERDICT: ❌ BLOCKED — do not enroll, do not contact
```

---

## Phase 2 Dedup — Run Immediately Before Each Enrollment API Call

This is the second dedup check. Phase 1 (the 8 checks above) runs during batch build. Phase 2 runs at commit time — right before the `apollo_emailer_campaigns_add_contact_ids` call — to catch concurrent-session conflicts.

For each contact in the enrollment batch:
```bash
grep -i "jason lieberman" /Work/MASTER_SENT_LIST.csv
```

If any name is now found (wasn't found in Phase 1): **STOP. Skip that contact. Post `[WARN]` in messages.md.** Another session enrolled them since your Phase 1 check. Continue enrolling the rest of the batch without them.

This adds ~5 seconds per batch and prevents the worst-case duplicate: two sessions simultaneously building batches from the same account pool.

---

## Batch Name Validation Gate (Pre-Log Check)

Before logging any row to MASTER_SENT_LIST.csv, validate the batch name you're about to write:

**Valid format:** `TAM Outbound Batch {N} {Mon}{DD}`
- ✅ `TAM Outbound Batch 8 Mar13`
- ✅ `TAM Outbound Batch 8 T2 Mar18`
- ❌ `B8` — abbreviation, rejected
- ❌ `Wave6B1` — non-standard, rejected
- ❌ `Mar13 Batch` — wrong order, rejected

```bash
# Quick self-check: does your batch name match this pattern?
# TAM Outbound Batch [number] [Mon][DD] (optionally " T2")
echo "TAM Outbound Batch 8 Mar13" | grep -E "^TAM Outbound Batch [0-9]+ (T[0-9]+ )?[A-Z][a-z]{2}[0-9]{1,2}$"
# Output should be non-empty. If empty, the name is invalid — fix before logging.
```

**If the batch name is invalid:** Correct it before writing the row. Never log with an abbreviation.

---

## After Enrollment: Post-Logging (Required)

Once enrollment succeeds, immediately:
1. Validate batch name format (see gate above)
2. Append row to `MASTER_SENT_LIST.csv`: `name,company_domain,batch,send_date,channel,credits,file,norm`
   - Batch name format: `TAM Outbound Batch {N} Mar{DD}` — NEVER abbreviations like "B7" or "W6B1"
   - `company_domain` = email domain extracted from contact's email (e.g., `epicor.com` from `jason@epicor.com`) — **required for all new rows as of 2026-03-13**
   - `norm` column = lowercase full name (for grep matching)
   - Example row: `Jason Lieberman,epicor.com,TAM Outbound Batch 8 Mar13,2026-03-13,Apollo Email,0,tamob-batch-20260313-1.html,jason lieberman`
3. Verify row count: `wc -l MASTER_SENT_LIST.csv` and state the exact count in the DONE/CLAIM message

---

*Source: `memory/playbooks/dedup-protocol.md` (6-point core) + cadence + reply history checks*
*Last updated: 2026-03-12 (Session 30)*
