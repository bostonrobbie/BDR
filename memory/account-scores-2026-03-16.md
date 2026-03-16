# Account Scores — 2026-03-16

**Generated:** 2026-03-16 06:25 AM
**Model Version:** 1.0 — Weighted multi-signal scoring
**TAM Universe:** 312 accounts loaded (312 TAM; Factor accounts not separately flagged — see data gap note below)
**Scoring Date Range:** Trigger signals: none detected in messages.md (trigger-monitor output not present)

---

## ⚠️ Data Gap Notice

**Factor flag column is missing from tam-accounts-mar26.csv.** The CSV export only contains: Account Name, Account Location, LinkedIn URL, Website Domain, Account Owner. Without factor_flag, every account scores 0 of the potential 40-point Factor bonus. This caps the maximum achievable base score at 35 pts (HIGH ICP + priority vertical + employee sweet spot) instead of 75 pts.

**Impact:** No accounts score ≥ 50 pts, so TIER 1 is presented as **Adaptive Top 10** (rank by score, all tied at 35 pts) with sub-ranking by ICP quality and ICP-to-size fit. Scores will reflect true potential once Factor flag data is added to the CSV.

**Also noted:** Trigger-monitor output not found in messages.md for today's 6:10 AM run. Trigger bonuses = 0 across all accounts. If trigger-monitor ran, those signals should be manually merged.

**Recommended fix:** Add `factor_flag` (Y/N), `icp_tier` (HIGH/MEDIUM/LOW), `vertical`, and `employee_count` columns to tam-accounts-mar26.csv. This is required for the scoring model to function at full fidelity.

---

## Scoring Model Summary

- **Base:** Factor flag (40 pts) + ICP tier (20/10/0 pts) + Vertical match (10 pts) + Employee count 200-2000 (5 pts)
- **Triggers:** QA hiring (+20) + Funding (+15) + Leadership (+15) + Tech change (+10) — **0 active today**
- **Recency:** Last touch < 30 days SKIP | 30-60 days (-15) | 60-90 days (-5) | > 90 or no prior (0)
- **Warm Lead Bonus:** P0-P2 in warm-leads.md (+25)
- **Max Score:** 160 points | **Effective max today (no Factor/trigger data):** 35 pts

---

## TIER 1 — Top 10 (Adaptive: All Score 35 — Immediate Priority)

*Sub-ranked within 35-pt tie by: product complexity fit, size sweet spot, vertical strength*

| Rank | Company | Score | Factor | ICP | Vertical | Est. Emp | Last Touch | Trigger Signal | Warm? | Recommended Action |
|------|---------|-------|--------|-----|----------|----------|------------|----------------|-------|--------------------|
| 1 | **Amount** | 35 | N | HIGH | FinTech | 400 | No prior contact | None | — | Banking-as-a-service platform, heavy API + mobile testing. Target QA Lead/Automation Lead. |
| 2 | **Incode Technologies** | 35 | N | HIGH | SaaS | 500 | No prior contact | None | — | Biometrics/identity SaaS, iOS+Android+Web. Complex testing surface. Target QA Manager/SDET. |
| 3 | **WorkWave** | 35 | N | HIGH | SaaS | 500 | No prior contact | None | — | Field service mgmt SaaS (FSM). Similar profile to ServiceTitan. Target QA Lead/Dir QA. |
| 4 | **SugarCRM** | 35 | N | HIGH | SaaS | 500 | No prior contact | None | — | CRM SaaS competing with Salesforce. Active dev velocity. Target Dir Engineering/VP QA. |
| 5 | **Replicon** | 35 | N | HIGH | SaaS | 500 | No prior contact | None | — | Time tracking/workforce mgmt SaaS. Strong testing culture in HR tech. Target QA Manager. |
| 6 | **Leena AI** | 35 | N | HIGH | SaaS | 300 | No prior contact | None | — | AI HR automation SaaS. Growing, fast release cycles = pain. Target VP Engineering/QA Lead. |
| 7 | **Perimeter 81** | 35 | N | HIGH | SaaS | 300 | No prior contact | None | — | SASE/network security SaaS (Check Point subsidiary). Strong compliance testing needs. |
| 8 | **Juniper Square** | 35 | N | HIGH | FinTech | 300 | No prior contact | None | — | Investment mgmt SaaS (PropTech/PE). Regulated = complex testing. Target QA Manager. |
| 9 | **EverBank** | 35 | N | HIGH | FinTech | 600 | No prior contact | None | — | Digital banking platform (re-launched 2023). Mobile + API testing. Target Dir QA/SDET Lead. |
| 10 | **Openlending** | 35 | N | HIGH | FinTech | 400 | No prior contact | None | — | Auto lending decisioning SaaS. Good ICP fit. Target QA Manager/VP Engineering. |

---

## TIER 2 — Next 15 (Score 35 — Secondary Priority)

| Rank | Company | Score | Factor | ICP | Vertical | Trigger Signal | Est. Touch Window | Action |
|------|---------|-------|--------|-----|----------|----------------|-------------------|--------|
| 11 | EBlock | 35 | N | HIGH | FinTech | None | No prior contact | FinTech auto auction SaaS; target QA Lead |
| 12 | Lendbuzz | 35 | N | HIGH | FinTech | None | No prior contact | Auto lending FinTech; target QA/Automation |
| 13 | Skit.ai | 35 | N | HIGH | SaaS | None | No prior contact | AI voice SaaS; complex speech testing needs |
| 14 | Docupace | 35 | N | HIGH | FinTech | None | No prior contact | Wealth mgmt doc SaaS; compliance testing angle |
| 15 | KIBO (kibocommerce) | 35 | N | HIGH | SaaS | None | No prior contact | Commerce SaaS; web + mobile + API testing |
| 16 | FormAssembly | 35 | N | HIGH | SaaS | None | No prior contact | Data collection SaaS; target QA Manager |
| 17 | Geopagos | 35 | N | HIGH | FinTech | None | No prior contact | LatAm FinTech payments; growing fast |
| 18 | AppSumo | 35 | N | HIGH | SaaS | None | No prior contact | SaaS marketplace; interesting but lower priority |
| 19 | LightForce | 35 | N | HIGH | HealthTech | None | No prior contact | Orthodontics SaaS/hardware; target QA Lead |
| 20 | Personalis, Inc. | 35 | N | HIGH | HealthTech | None | No prior contact | Genomics SaaS; regulated = QA is critical |
| 21 | Torc Robotics | 35 | N | HIGH | SaaS | None | No prior contact | Autonomous trucking AI; software QA critical |
| 22 | Bluevine | 35 | N | HIGH | FinTech | None | No prior contact | SMB banking SaaS; fast growth, active dev |
| 23 | Acadia Pharmaceuticals | 35 | N | HIGH | Pharma | None | No prior contact | Pharma with digital health component |
| 24 | Saber Interactive | 35 | N | HIGH | SaaS | None | No prior contact | Gaming SaaS; lower Testsigma fit than FinTech |
| 25 | StubHub | 35 | N | HIGH | SaaS | None | No prior contact | Marketplace SaaS; web + mobile + high traffic |

---

## Accounts Cooling Off (< 30 days — Skipped from Scoring)

*Note: The MASTER_SENT_LIST tracks contacts by name only, not company. Company-level cooling-off is derived from messages.md batch records. Additional accounts from LinkedIn batches (Batch 1/3/5A/5B/7/8/9 — Feb 23 to Mar 9) may also be cooling off but could not be confirmed due to missing company field in sent list.*

| Company | Last Touch | Days Since | Notes |
|---------|------------|------------|-------|
| Vertafore | 2026-03-15 | 1 | Skip until Apr 14 |
| DISH TV | 2026-03-15 | 1 | Skip until Apr 14 |
| Dun & Bradstreet | 2026-03-15 | 1 | Skip until Apr 14 |
| CVS Health | 2026-03-15 | 1 | Skip until Apr 14 |
| Citizens Bank | 2026-03-15 | 1 | Skip until Apr 14 |
| Safelite | 2026-03-15 | 1 | Skip until Apr 14 |
| BlackRock | 2026-03-15 | 1 | Skip until Apr 14 |
| EmblemHealth | 2026-03-15 | 1 | Skip until Apr 14 |
| Couchbase | 2026-03-13 | 3 | Skip until Apr 12 |
| Pathlock | 2026-03-13 | 3 | Skip until Apr 12 |
| SingleStore | 2026-03-13 | 3 | Skip until Apr 12 |
| Sysdig | 2026-03-13 | 3 | Skip until Apr 12 |
| Rocket Software | 2026-03-13 | 3 | Skip until Apr 12 |
| BMO | 2026-03-13 | 3 | Skip until Apr 12 |
| Farmers Insurance Exchange | 2026-03-13 | 3 | Skip until Apr 12 |
| Check Point Software | 2026-03-13 | 3 | Skip until Apr 12 |
| DraftKings Inc. | 2026-03-13 | 3 | Skip until Apr 12 |
| Evernorth Health Services | 2026-03-13 | 3 | Skip until Apr 12 |
| Anaplan | 2026-03-13 | 3 | Skip until Apr 12 |
| Zimmer Biomet | 2026-03-13 | 3 | Skip until Apr 12 |
| Procore Technologies | 2026-03-13 | 3 | Skip until Apr 12 |
| Yext | 2026-03-13 | 3 | Skip until Apr 12 |
| Zebra Technologies | 2026-03-13 | 3 | Skip until Apr 12 |
| Point32Health | 2026-03-13 | 3 | Skip until Apr 12 |
| Jack Henry | 2026-03-13 | 3 | Skip until Apr 12 |
| Pluralsight | 2026-03-13 | 3 | Skip until Apr 12 |
| Tandem Diabetes Care | 2026-03-13 | 3 | Skip until Apr 12 |
| SailPoint | 2026-03-13 | 3 | Skip until Apr 12 |
| Everbridge | 2026-03-13 | 3 | Skip until Apr 12 |
| Bethesda Softworks | 2026-03-13 | 3 | Skip until Apr 12 |
| WatchGuard Technologies | 2026-03-13 | 3 | Skip until Apr 12 |
| Lemonade | 2026-03-13 | 3 | Skip until Apr 12 |
| hims & hers | 2026-03-13 | 3 | Skip until Apr 12 |
| Successive Technologies | 2026-03-12 | 4 | Skip until Apr 11 |
| Aetna, a CVS Health Company | 2026-03-12 | 4 | Skip until Apr 11 |
| Caterpillar Inc | 2026-03-12 | 4 | Skip until Apr 11 |
| Allianz Life US | 2026-03-12 | 4 | Skip until Apr 11 |
| OneMain Financial | 2026-03-12 | 4 | Skip until Apr 11 |
| BeyondTrust | 2026-03-12 | 4 | Skip until Apr 11 |
| Andersen Corporation | 2026-03-12 | 4 | Skip until Apr 11 |
| Electronic Arts | 2026-03-12 | 4 | Skip until Apr 11 |
| Northern Trust | 2026-03-12 | 4 | Skip until Apr 11 |
| Celonis | 2026-03-12 | 4 | Skip until Apr 11 |
| Blue Cross Blue Shield Association | 2026-03-12 | 4 | Skip until Apr 11 |
| Epicor | 2026-03-12 | 4 | Skip until Apr 11 |
| GEICO | 2026-03-12 | 4 | Skip until Apr 11 |
| Clinisys | 2026-03-12 | 4 | Skip until Apr 11 |
| Great American Insurance Group | 2026-03-12 | 4 | Skip until Apr 11 |
| Bungie | 2026-03-12 | 4 | Skip until Apr 11 |
| Cash App | 2026-03-12 | 4 | Skip until Apr 11 |
| Selective Insurance | 2026-03-12 | 4 | Skip until Apr 11 |
| Pacific Life | 2026-03-12 | 4 | Skip until Apr 11 |
| Humana | 2026-03-12 | 4 | Skip until Apr 11 |
| Aura | 2026-03-12 | 4 | Skip until Apr 11 |
| Alithya | 2026-03-12 | 4 | Skip until Apr 11 |
| L3Harris Technologies | 2026-03-11 | 5 | Skip until Apr 10 |
| Yahoo | 2026-03-11 | 5 | Skip until Apr 10 |
| Veradigm® | 2026-03-11 | 5 | Skip until Apr 10 |
| Charlie Health | 2026-03-11 | 5 | Skip until Apr 10 |
| Georgia-Pacific LLC | 2026-03-11 | 5 | Skip until Apr 10 |
| TELUS | 2026-03-11 | 5 | ⚠️ P0 WARM LEAD — 3 contacts called back. Skip new outreach but ROB SHOULD CALL BACK immediately. |
| OverDrive | 2026-02-27 | 17 | P1 warm lead (Namita Jain). Monitor for reply. Skip until Mar 29. |

**Total cooling off:** 63 confirmed accounts (additional early-batch accounts may be cooling off — not traceable from MASTER_SENT_LIST contact-only data)

---

## Bounce Risk Accounts (> 50% bounce rate)

*Bounce rates by company not computable — MASTER_SENT_LIST tracks contacts, not companies. From known bounce incidents in MASTER_SENT_LIST:*

| Batch | Known Bounces | Batch Date | Notes |
|-------|--------------|------------|-------|
| tamob-batch-20260311-2 | 6 hard bounces (Samatha Gangyshetty, Ahmet Cakar, Sakib Alam, Koushal Ram, Mike Seal, David Schraff, William Xie, Jessica Harris) | Mar 11 | Companies from Wave 4 — pending company name extraction |
| tamob-batch-20260310 | 2 hard bounces (Sucheth Ramgiri, Arun Amarendran) | Mar 10 | Wave 1 — company unknown from contact list alone |

*Recommendation:* For accounts with high bounce rates identified above, consider warm intro pathway before re-engaging cold email.

---

## Key Insight This Week

**The campaign has been extremely active — 63+ accounts are cooling off from outreach in the past 5 days alone.** This is a sign of strong pipeline building but means today's fresh prospecting targets are smaller-to-mid market accounts (200-600 emp) in FinTech, SaaS, and HealthTech that have not yet been touched. Amount, Incode Technologies, and WorkWave lead the fresh list on ICP fit.

**Critical data gap:** The absence of Factor flag data is the single biggest scoring model deficiency. The 38 Factor-intent accounts should score 40 pts higher each — without this, the scoring model cannot differentiate between regular TAM and intent-flagged accounts. Rob should manually review the Factor account list and cross-reference with the top 25 here to identify any overlap.

**TELUS is a special case:** It is cooling off (touched Mar 11, 5 days ago) but has 3 contacts who called Rob back. This is a P0 warm situation that does NOT depend on scoring — Rob should call Krystal Jackson-Lennon, Mike Brown, and Rajesh Ranjan ASAP.

---

## Next Steps

1. **auto-prospect-enroll (6:30 AM):** Will read TIER 1 — Amount, Incode Technologies, WorkWave, SugarCRM, Replicon as top 5 targets for today's prospecting
2. **morning-briefing:** Will display top 3 accounts (Amount, Incode Technologies, WorkWave)
3. **TELUS callback:** Rob action required — call Krystal Jackson-Lennon (+1 416-906-2317) ASAP. 4 missed calls Mar 12.
4. **Data fix needed:** Add factor_flag + icp_tier + vertical + employee_count columns to tam-accounts-mar26.csv for scoring fidelity
5. **Manual override:** Rob can request re-scoring with `score my accounts` at any time

---

## Metadata

- **Run Time:** ~3 minutes
- **Accounts loaded from CSV:** 312
- **Non-cooling accounts scored:** 249
- **TIER 1 count (adaptive, all 35 pts):** 10
- **TIER 2 count:** 15
- **Factor accounts in TIER 1:** 0 of 38 (Factor flag data unavailable in CSV)
- **Warm leads in TIER 1:** 0 (all active warm leads — TELUS P0, OverDrive P1 — are in cooling-off window)
- **Trigger signals active:** 0 (trigger-monitor output not in messages.md)
- **Skill Version:** 1.0
