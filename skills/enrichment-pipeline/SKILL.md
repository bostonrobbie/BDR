# Enrichment Pipeline — Batch Prep (TAM Account Sourcing to Ready-to-Draft)

## Description
Covers Steps 1-4 of the TAM T1 Batch workflow: source accounts by priority (Factor first, TAM HIGH, TAM MEDIUM), find contacts at each account using Apollo People Search, enrich to get emails, and run the compliance gate. Outputs a batch-ready contact list ready for drafting. This replaces doing Steps 1-4 manually from `memory/playbooks/tam-t1-batch.md`.

## Trigger
- Run at the start of any new batch: "prep next batch", "find contacts at [companies]", "enrich these accounts"
- Called as Steps 1-3 of `skills/tam-t1-batch/SKILL.md`
- Run on-demand: "enrich [company]", "find QA contacts at [domain]"

## ⛔ APPROVE SEND RULE
This skill does NOT draft or send anything. It finds and validates contacts only. Output goes to `skills/tam-t1-batch/SKILL.md` for drafting. All sends require Rob's explicit APPROVE SEND.

---

## Phase 1: Account Selection

**Priority order (from `memory/sop-tam-outbound.md` and `CLAUDE.md` operating directive):**
1. Factor accounts with buyer intent (38 accounts, `ICP = Factor` in `tam-accounts-mar26.csv`) — HIGHEST PRIORITY
2. TAM accounts with `ICP = HIGH` (not yet contacted or partially covered)
3. TAM accounts with `ICP = MEDIUM`

**Find coverage gaps:**
```bash
cd /Work

# See all companies already contacted (from master list)
awk -F',' 'NR>1 {print $1}' MASTER_SENT_LIST.csv | sort -u | head -50

# Check a specific domain is in TAM list
grep -i "company.com" tam-accounts-mar26.csv

# Find Factor accounts not yet in sent list
# (manual: compare tam-accounts-mar26.csv Factor rows vs MASTER_SENT_LIST.csv)
```

**Check `memory/target-accounts.md`** to see which accounts already have contacts enrolled. Skip fully-covered accounts (3+ contacts with T1s sent from the same company).

---

## Phase 2: Contact Discovery (Apollo People Search)

For each target account, search Apollo People Search. This returns names/titles/LinkedIn but NOT emails — enrichment is a separate step.

```
Tool: apollo_mixed_people_api_search
Parameters:
  q_organization_domains_list: ["epicor.com"]
  person_titles: ["QA Manager", "QA Lead", "Director of QA", "VP Quality",
                  "Test Manager", "SDET Lead", "Automation Lead", "Head of Quality",
                  "QA Director", "Test Automation Lead", "Director of Quality"]
  person_seniorities: ["manager", "director", "vp", "senior"]
  per_page: 25
```

**Priority scoring per contact (from `memory/scoring-feedback.md`):**

| Factor | Points |
|--------|--------|
| Factor account (buyer intent) | +2 |
| Director/Head/VP of QA (decision authority) | +1 |
| Top vertical: FinTech, SaaS, HealthTech | +1 |
| SDET/Automation Lead (39.3% reply rate in mabl era) | +1 |
| VP Eng at large company (no QA scope evident) | -1 |

Target: select top 1-3 contacts per company, max 3 (proof point rotation requires different stories per contact at same company).

---

## Phase 3: Enrichment (Apollo People Enrichment — uses credits)

Before running enrichment, check credit balance:
```
Tool: apollo_users_api_profile
include_credit_usage: true
```
Current credit pool: ~6,879 lead credits. Report usage to Rob.

For each selected contact, enrich to get email:
```
Tool: apollo_people_match
Parameters:
  first_name: "{first}"
  last_name: "{last}"
  organization_name: "{company}"
  domain: "{domain}"
```

**Email status handling:**

| Status | Action |
|--------|--------|
| verified | ✅ Proceed |
| likely to engage | ✅ Proceed |
| catchall | ⚠️ Flag — see `memory/playbooks/catchall-domains.md`. Note in tracker. Proceed but monitor open/click signals as deliverability proxy (per Wave 6 B2 learnings — 8/12 companies had catchall). |
| unverified | ⚠️ Flag — Rob decides |
| unavailable | ❌ Skip or find alternate |

**Catchall prevalence note:** Many TAM accounts use catchall domains (BeyondTrust, Jack Henry, Bluevine, SingleStore, EverBank from W6B2 batch). This is normal. Flag but don't block.

---

## Phase 4: Compliance Gate

Run `skills/compliance-gate/SKILL.md` for EVERY contact. All 8 checks must pass before a contact is added to the batch-ready list.

**Fast bulk check for MASTER_SENT_LIST.csv:**
```bash
cd /Work
for name in "Jason Lieberman" "Les Stickney" "Holly Shubaly"; do
  result=$(grep -i "$name" MASTER_SENT_LIST.csv)
  if [ -n "$result" ]; then
    echo "DUPLICATE: $name — $result"
  else
    echo "CLEAN: $name"
  fi
done
```

**Fast bulk TAM domain verification:**
```bash
for domain in "epicor.com" "beyondtrust.com" "northerntrust.com"; do
  result=$(grep -i "$domain" tam-accounts-mar26.csv)
  if [ -n "$result" ]; then echo "TAM OK: $domain"; else echo "NOT TAM: $domain — BLOCKED"; fi
done
```

Any contact that fails compliance → BLOCKED, flagged to Rob with reason. Do not add to batch-ready list.

---

## Phase 5: Output

Report per company, then summary:

```
━━━━ EPICOR (epicor.com) — TAM HIGH ━━━━
Contacts found: 4 (Apollo People Search)
Enriched: 3 (1 unavailable — no email)
Compliance: 3 CLEAR, 0 BLOCKED

BATCH-READY:
  ✅ Jason Lieberman — QA Manager — jason.lieberman@epicor.com (verified) — P4/5
  ✅ Holly Shubaly — SDET Lead — hshubaly@epicor.com (verified) — P3/5
  ✅ Les Stickney — Director of QA — lstickney@epicor.com (catchall ⚠️) — P4/5

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BATCH-READY TOTAL: 12 contacts across 5 companies
Credits used this run: 12 enrichment credits
Credits remaining: ~6,867

BLOCKED/SKIPPED:
  🚫 Sanjay Singh (ServiceTitan) — DNC list
  ⏭️ Mike Chen (Epicor) — No email available
  🚫 John Doe (Acme Corp) — acmecorp.com not in tam-accounts-mar26.csv

Proof point notes:
  • Epicor: 3 contacts — needs 3 different proof points. Suggest: Hansard (Jason), CRED (Holly), Cisco (Les)
  • All contacts confirmed unique in MASTER_SENT_LIST.csv
```

---

## Ownership Warning (from Wave 6 B2 learnings)
Some contacts in Apollo may be owned by other team members. These cannot be enrolled via API even with `contacts_without_ownership_permission: true`. If the Apollo record is owned by a teammate, flag to Rob — must transfer ownership in Apollo UI or enroll manually before proceeding.

---

## Integration Points
- Called by: `skills/tam-t1-batch/SKILL.md` Steps 1-3
- Calls: `skills/compliance-gate/SKILL.md` (Phase 4)
- Feeds into: `skills/draft-qa/SKILL.md` and `skills/apollo-enroll/SKILL.md`
- Reads: `tam-accounts-mar26.csv`, `memory/target-accounts.md`, `MASTER_SENT_LIST.csv`, `CLAUDE.md`
- Uses: Apollo People Search, People Match, Profile (credits check) MCPs

*Source: `memory/playbooks/tam-t1-batch.md` Steps 1-4 + `memory/playbooks/dedup-protocol.md`*
*Last updated: 2026-03-12 (Session 30)*

---

## Self-Improvement Loop

This skill maintains its own run log and learned-patterns file. Full protocol: `skills/_shared/learning-loop.md`

### Before Each Run
1. Read `skills/enrichment-pipeline/learned-patterns.md` if it exists — apply any documented calibration adjustments
2. Count entries in `skills/enrichment-pipeline/run-log.md` to determine current run number

### After Every Run — Append to run-log.md
```
### Run #[N] — [YYYY-MM-DD HH:MM]
- **Result:** [1-2 sentence summary]
- **Key metrics:** [skill-specific counts per _shared/learning-loop.md]
- **Anomalies:** [anything unexpected]
- **Adjustments made this run:** [any deviations from SKILL.md]
- **Output quality:** [Accurate / Mostly accurate / Needs calibration / Failed]
```

### Every 5th Run — Pattern Review
1. Read last 5 run-log.md entries
2. Extract recurring patterns, consistent edge cases, metric drift
3. Overwrite `skills/enrichment-pipeline/learned-patterns.md` with updated findings
4. If a pattern appears in 4+ of 5 runs: write a `## SKILL UPDATE PROPOSAL — enrichment-pipeline` entry to `memory/session/messages.md` for Rob's review

**Hard rule:** Never modify SKILL.md directly. Only propose updates via messages.md and wait for Rob's explicit approval.
