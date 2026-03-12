# Playbook: Dedup Protocol

## When to Use
Before adding ANY contact to a batch, enrolling in a sequence, or sending any outreach. This is a safety-critical workflow. Skipping any step risks double-sends (which damage sender reputation and waste credits).

---

## The 6-Point Dedup Check

Run ALL 6 checks for every contact. A failure at any step means STOP.

### Check 1: MASTER_SENT_LIST.csv

The central record of every contact ever sent outreach. CSV format: `name,batch,send_date,channel,credits,file,norm`

**How to check:**
```bash
grep -i "jason lieberman" MASTER_SENT_LIST.csv
```

Also check the normalized name column (last column, lowercase):
```bash
grep -i "jason lieberman" MASTER_SENT_LIST.csv
```

**If found:** STOP. This contact has already been contacted. Do NOT send again unless Rob explicitly approves re-engagement AND it's been 60+ days.

**Edge cases:**
- Name spelling variations: Try partial matches. "Lieberman" and "Liberman" are different people, but "Jason Lieberman" and "Jason A. Lieberman" might be the same.
- Same name, different company: Confirm by checking the batch column. If it's a different company, it's likely a different person, but verify email/LinkedIn before proceeding.

### Check 2: DNC (Do Not Contact) List

Located in `CLAUDE.md` under "Do Not Contact List."

**Current DNC entries (as of Mar 12, 2026):**
- Sanjay Singh (ServiceTitan) — hostile reply
- Lance Silverman (Batch 5B) — polite decline, re-engage after 60+ days
- Clyde Faulkner (CAMP Systems) — mabl-era customer
- Ashok Prasad (ZL Technologies) — mabl-era contact
- Abe Blanco (Kapitus) — replied "not interested"
- Chuck Smith (Aventiv Technologies) — double-send incident
- Jitesh Biswal (JPMorgan Chase) — declined InMail

**If found:** STOP. Permanently skip (unless the entry says re-engage after a time period AND that time has passed).

### Check 3: Apollo Contacts Search

Search Apollo for existing records:
```
Tool: apollo_contacts_search
Parameters:
  q_keywords: "Jason Lieberman Epicor"
  per_page: 5
```

**What to check if found:**
- `emailer_campaign_ids`: If non-empty, they're in a sequence. Check which one.
- `contact_campaign_statuses`: Look at `status` (active/paused/finished/failed) and `emailer_campaign_id`.
- If they're active in the TAM Outbound sequence: STOP, they're already enrolled.
- If they're in a different sequence: Note it. You may need `sequence_active_in_other_campaigns: true` override during enrollment.
- If they're finished/failed in another sequence: OK to enroll with `sequence_finished_in_other_campaigns: true`.

### Check 4: Current Batch Check

If you're building a batch with multiple contacts, check that you haven't already added this person to the current batch. This catches copy-paste errors.

Check the batch tracker HTML file you're building. Also check against other contacts in your working list.

### Check 5: Same-Company Check

Not a hard block, but important for awareness:
- How many contacts from this company are already in the sequence?
- Are you about to exceed 4-5 contacts at one company? Rob should be aware if you're hitting a company heavily.
- Each contact at the same company MUST get a different proof point and angle.

### Check 6: Email Domain Verification

For TAM Outbound specifically, verify the contact's email domain appears in `tam-accounts-mar26.csv`:
```bash
grep -i "epicor.com" tam-accounts-mar26.csv
```

**If NOT found:** This contact is NOT from a TAM account. Do NOT enroll in TAM Outbound. (Per TAM-ONLY rule, INC-010.)

---

## Dedup Decision Matrix

| Check 1 (MASTER) | Check 2 (DNC) | Check 3 (Apollo) | Check 6 (TAM) | Decision |
|-------------------|---------------|-------------------|---------------|----------|
| Not found | Not found | Not found | Found | PROCEED — create contact and enroll |
| Not found | Not found | Found, no sequence | Found | PROCEED — enroll existing contact |
| Not found | Not found | Found, in TAM seq | Found | STOP — already enrolled |
| Not found | Not found | Found, in OTHER seq | Found | PROCEED with override flags |
| Found | Any | Any | Any | STOP — already contacted |
| Any | Found | Any | Any | STOP — on DNC list |
| Any | Any | Any | Not found | STOP — not a TAM account |

---

## Tools for Bulk Dedup

For batches of 10+ contacts, use bash for speed:
```bash
# Check all names at once against MASTER_SENT_LIST.csv
for name in "Jason Lieberman" "Les Stickney" "Holly Shubaly"; do
  result=$(grep -i "$name" MASTER_SENT_LIST.csv)
  if [ -n "$result" ]; then
    echo "DUPLICATE: $name — $result"
  else
    echo "CLEAN: $name"
  fi
done
```

For domain verification:
```bash
for domain in "epicor.com" "beyondtrust.com" "northerntrust.com"; do
  result=$(grep -i "$domain" tam-accounts-mar26.csv)
  if [ -n "$result" ]; then
    echo "TAM OK: $domain"
  else
    echo "NOT TAM: $domain — DO NOT ENROLL"
  fi
done
```

---

## Post-Dedup Logging

After all checks pass and the contact is enrolled:
1. Immediately add a row to `MASTER_SENT_LIST.csv`
2. This creates the dedup record for all future sessions
3. Format: `name,batch,send_date,channel,credits,file,norm`
4. The `norm` column is the lowercase full name for grep matching

---

*Last updated: 2026-03-12 — consolidated from Sessions 7-27, INC-001 through INC-010*
