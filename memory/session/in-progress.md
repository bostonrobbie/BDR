# In-Progress Checkpoint

**Status: ACTIVE**
*Started: 2026-03-11 Session 16 (continued)*

---

## Task: BATCH-001 — TAM Outbound Wave 3 (Factor accounts only, ~50 contacts, T1 drafts)

**What I'm doing:** Building a fresh 50-contact T1 batch from remaining untouched Factor accounts. Account selection → Apollo enrichment → Account Research → Contact Research → T1 drafts → QA gate → HTML tracker → BATCH SUMMARY.

## Steps

- [ ] Step 1: Account selection (remaining Factor accounts, prioritized) ← NEXT
- [ ] Step 2: Apollo contact search for each selected account
- [ ] Step 3: MASTER_SENT_LIST dedup check per contact
- [ ] Step 4: Account Research Block per account (triggers, angles, proof points)
- [ ] Step 5: Contact Research per person (LinkedIn scope, angle assignment)
- [ ] Step 6: Write T1 drafts (all contacts)
- [ ] Step 7: QA Gate — MQS >= 9/12 for each draft
- [ ] Step 8: Build batch tracker HTML (tamob-batch-20260311-1.html)
- [ ] Step 9: Post BATCH SUMMARY → wait for APPROVE SEND
- [ ] Step 10: Clear in-progress.md + update handoff.md + commit

## Files in progress

| File | Location | Current state |
|------|----------|---------------|
| tamob-batch-20260311-1.html | /Work/ | Not yet created |
| tam-coverage-tracker.csv | /Work/ | Exists. Updating as accounts claimed. |
| MASTER_SENT_LIST.csv | /Work/ | 338 rows. Adding after sends. |

## Last commit

`ef9bcaa` — Push-prep: CLAUDE.md date, handoff cleanup, SOP Part 10 template fix

## Resume instructions

**Start from:** Step 2 (Apollo contact search) — account list is locked below
**Critical context:**
- 10 target accounts selected (see Selected Accounts block below)
- All Factor accounts only (Rob's filter)
- Dedup Wave 1+2 contacts already sent (Cboe, Fidelity, Chase, Commvault, TruStage, YouTube, GEICO, Checkr, EA, Cetera, OneMain, Mindbody, HashiCorp)
- Apollo sequence: TAM Outbound - Rob Gorham (69afff8dc8897c0019b78c7e)
- Send email: robert.gorham@testsigma.com (.com ONLY)

## Selected Accounts (locked)

| # | Account | ICP | Signal Tier | Why |
|---|---------|-----|------------|-----|
| 1 | OSF HealthCare | HIGH | A (Signup x1, web x5, Jan 2025) | Healthcare system, strong intent |
| 2 | Yahoo | HIGH | B (Aug 2025) | Tech enterprise, good fit |
| 3 | Datamatics | HIGH | B (Oct 2025) | Tech services, recent activity |
| 4 | Successive Technologies | HIGH | B (Sep 2025) | Mid-market SaaS |
| 5 | Veradigm | HIGH | B | Healthcare IT, no Nektar date yet |
| 6 | Corewell Health | HIGH | B | Healthcare system, large |
| 7 | Charlie Health | HIGH | B | Mental health tech, HIGH ICP |
| 8 | TELUS | Medium | A (G2+Demo, Feb 2025) | Telecom, Tier A intent signal |
| 9 | GE | Medium | A (Pricing Page, Jul 2025) | Manufacturing, buying intent |
| 10 | Winsupply | Medium | A (Signup x1, Oct 2025) | Retail, signup signal |

*If contact count falls short of 50: add Microchip Technology, L3Harris, Charles River Labs.*
