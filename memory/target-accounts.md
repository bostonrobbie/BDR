# Target Accounts — Rob Gorham NAMER

## ⚡ PROSPECTING RULES (Effective Mar 10, 2026)

**The TAM list (312 accounts) + Factor accounts (38) are the ONLY authorized prospecting universe.**
No open Sales Nav prospecting outside these lists. Goal: systematic full coverage of every account to hit intro meeting → demo quota.

All Factor accounts are a subset of the TAM (37 of 38 appear in TAM CSV; PGA of America is Factor-only).

### Multi-Contact Rule (Effective Mar 10, 2026)
**Find and enroll EVERY decision-maker at each account.** The goal is maximum account coverage — not just one primary contact. Pull ALL QA/Engineering Director+ contacts with findable emails and enroll them in the TAM Outbound sequence in the same batch.

Decision-maker titles (in priority order):
1. VP/Director of QA, Quality Assurance, Quality Engineering
2. VP/Director of Engineering (if no QA-specific title found)
3. QA Manager / Engineering Manager (for mid-size accounts <2,000 employees)
4. IT Director, Quality Engineering (exact ICP match)

**Targeting formula — personalization scales with account contact count:**
| Contacts Found | Personalization Level Required |
|----------------|-------------------------------|
| 1-2 contacts | Standard — enterprise formula is fine |
| 3-5 contacts | Medium — unique role scope + different proof points per person |
| 6+ contacts | High — treat each as an individual campaign; group by subteam if possible |

**No "hold backup contacts" rule.** Old SOP said to defer backup contacts until primary's T1 is sent. This is REMOVED. Enroll all decision-makers in the same batch. Personalize each email to their specific role/scope so they don't read as identical if colleagues compare.

**Coverage tracker:** `/Work/tam-coverage-tracker.html` — interactive dashboard with filters by status, ICP, region
**Data file:** `/Work/tam-coverage-tracker.csv` — machine-readable version
**Session recovery:** If starting fresh, check Apollo (TAM Outbound sequence → Tasks tab) for what's currently due, then cross-reference batch tracker HTML files in `/Work/` for draft content. Do NOT re-research contacts already in the enriched roster below.

**Coverage summary as of Mar 9, 2026:**
| Status | Count |
|--------|-------|
| 🎯 HOT Factor (ready to work) | 33 |
| ⚠️ Factor — Check Prior Outreach First | 1 (Tailored Brands only — TruStage confirmed clear Mar 9) |
| 🔥 Warm Lead (active) | 1 (OverDrive) |
| ✅ Untouched TAM (clean to prospect) | 259 |
| ⛔ Skip (DNC / Competitor) | 2 (Kapitus, ACCELQ) |
| 🏛️ Government — Out of ICP | 11 |
| 🗑️ Bad Data | 4 |
| **TOTAL** | **312** |

**ICP breakdown:** HIGH = 142 · Medium = 153 · Low/Gov = 17

---

## Overview
Rob has three distinct account lists assigned by Testsigma leadership, all stored in Salesforce.

**Priority hierarchy:** Factors (HOT) > TAM Named Accounts > Manual Testers TAM
*(Open Sales Nav prospecting outside these lists is no longer authorized as of Mar 9, 2026)*

---

## 1. Factor Accounts (HOT — Highest Priority)

**What they are:** Existing Testsigma prospect accounts that Salesforce has flagged as HOT Factors — accounts showing strong buying signals or intent, previously worked by AE Shakeel who has since left/transferred.

**Rob's assignment:** 38 accounts (current as of Mar 9, 2026 — originally 7 from Shakeel A, expanded since)

**Salesforce Report:** [HOT Factors Untapped Report](https://d2v000000sgbdea0.lightning.force.com/lightning/r/Report/00OOX00000HOtHh2AL/view)

**Channel:** LDR_SDR channel (LinkedIn + email outreach)

**Context:** These are HOT — act on them first. They had prior AE activity (Shakeel) so contacts may already exist in CRM. Check for prior touches before outreach. Most have recent Nektar activity signals (website sessions, G2 visits, demo page visits).

**Status:** 38 accounts confirmed via SF report Mar 9, 2026. Cross-check MASTER_SENT_LIST before prospecting each one.

**⚠️ NOTE: ACCELQ (row 7) is a test automation competitor to Testsigma.** Confirm with Rob before any outreach — they may be in the list by mistake or for competitive monitoring only.

### All 38 Factor Accounts (read from SF report Mar 9, 2026)

**Signal Tier key:** A = demo/pricing/signup/G2 page visit (buying-intent actions) · B = website/blog sessions only · C = no recent Nektar signal
**Last Activity** = last Nektar-tracked interaction date (blank = no recorded date; recently-added accounts may not have Nektar history yet)

| # | Account Name | Size | Engagement | Industry | ICP Fit | Signal Tier | Last Activity |
|---|-------------|------|-----------|----------|---------|-------------|---------------|
| 1 | TELUS | Enterprise[1000+] | Warm | Telecommunications | Medium | **A** (G2, Demo) | Feb 24 2025 |
| 2 | GE | Enterprise[1000+] | Hot | Manufacturing | Medium | **A** (Pricing Page) | Jul 18 2025 |
| 3 | Microchip Technology Inc. | Enterprise[1000+] | Hot | Manufacturing | Medium | B (Review sites, web) | Dec 16 2024 |
| 4 | Mindbody | Enterprise[1000+] | Hot | Healthcare | **HIGH** | B (web sessions) | Sep 12 2024 |
| 5 | Datamatics | Enterprise[1000+] | Hot | Technology | **HIGH** | B (web sessions) | Oct 15 2025 |
| 6 | OneMain Financial | Enterprise[1000+] | Warm | Finance | **HIGH** | **A** (G2 x4) | Feb 20 2025 |
| 7 | ACCELQ | Commercial[100-499] | Hot | Software | ⚠️ COMPETITOR | A (G2 x19!) | May 5 2025 |
| 8 | KKR | Enterprise[1000+] | Warm | Finance | Medium | B (web sessions) | Feb 5 2025 |
| 9 | Cboe Global Markets | Enterprise[1000+] | Hot | Finance | **HIGH** | **A** (Signup x2, Demo x2) | Jan 9 2026 🔥 |
| 10 | Centers for Disease Control | Enterprise[1000+] | Hot | Government | Low | B (web sessions) | — |
| 11 | Cetera Financial Group | Enterprise[1000+] | Warm | Finance | **HIGH** | C (no signals) | Nov 4 2025 |
| 12 | Charles River Laboratories | Enterprise[1000+] | Hot | Other | Medium | B (web sessions) | — |
| 13 | Enterprise Mobility Inc | Enterprise[1000+] | Hot | Entertainment | Medium | B (web sessions) | — |
| 14 | OSF HealthCare | Enterprise[1000+] | Hot | Healthcare | **HIGH** | **A** (Signup x1, web x5) | Jan 27 2025 |
| 15 | Electronic Arts | Enterprise[1000+] | Hot | Entertainment | **HIGH** | B (web x4, blog x3) | — |
| 16 | Fidelity Investments | Enterprise[1000+] | Warm | Finance | **HIGH** | **A** (G2, Use-case pg) | Aug 8 2025 |
| 17 | Commvault | Enterprise[1000+] | Hot | Technology | **HIGH** | **A** (G2, Signup x2, web x6) | Jun 12 2025 |
| 18 | bp | Enterprise[1000+] | Warm | Energy | Low | B (web sessions) | — |
| 19 | Chase | Enterprise[1000+] | Hot | Finance | **HIGH** | **A** (Pricing, Signup x2, Use-case x3, web x7) | Oct 15 2025 🔥 |
| 20 | Successive Technologies | Mid Market[500-999] | Warm | Technology | **HIGH** | B (web sessions) | Sep 25 2025 |
| 21 | HashiCorp | Enterprise[1000+] | Hot | Technology | **HIGH** | B (web sessions) | Aug 13 2025 |
| 22 | TruStage | Enterprise[1000+] | Hot | Finance | **HIGH** | **A** (Demo x1, Outbound Completed x11) | Feb 3 2026 ⚠️ |
| 23 | GEICO | Enterprise[1000+] | Hot | Insurance | **HIGH** | B (web sessions) | Feb 5 2025 |
| 24 | Winsupply | Enterprise[1000+] | Hot | Retail | Medium | **A** (Signup x1, blog) | Oct 9 2025 |
| 25 | Laboratorios Sanfer | Enterprise[1000+] | Hot | Healthcare | Medium | **A** (Signup x2, Demo x1) | Jun 20 2025 |
| 26 | YouTube | Enterprise[1000+] | Hot | Technology | **HIGH** | **A** (Signup x1, alt page, web x4) | Sep 17 2025 |
| 27 | Yahoo | Enterprise[1000+] | Hot | Technology | **HIGH** | B (web sessions) | Aug 11 2025 |
| 28 | Checkr, Inc. | Enterprise[1000+] | Hot | Technology | **HIGH** | B (web sessions) | — |
| 29 | Tailored Brands, Inc. | Enterprise[1000+] | Hot | Apparel | Low | A (Outbound Completed x7) | Feb 4 2026 ⚠️ |
| 30 | Veradigm® | Enterprise[1000+] | Hot | Healthcare | **HIGH** | B (web sessions) | — |
| 31 | Plenty® | Commercial[100-499] | Hot | Agriculture & Mining | Low | **A** (Signup x3, Demo x2) | — |
| 32 | Corewell Health | Enterprise[1000+] | Hot | Healthcare & Life Sciences | **HIGH** | B (web sessions) | — |
| 33 | Charlie Health | Enterprise[1000+] | Hot | Healthcare & Life Sciences | **HIGH** | B (web sessions) | — |
| 34 | Georgia-Pacific LLC | Enterprise[1000+] | Hot | Manufacturing, Automotive & Energy | Low | B (web sessions) | — |
| 35 | Market of Choice | Commercial[100-499] | Hot | Retail & CG | Low | **A** (Pricing Page x1) | — |
| 36 | Springboard | Enterprise[1000+] | Hot | Education | Low | **A** (Pricing Page, Case Study) | — |
| 37 | L3Harris Technologies | Enterprise[1000+] | Hot | Manufacturing | Medium | B (web sessions x9) | — |
| 38 | PGA of America | Enterprise[1000+] | Hot | Communications & Media | Low | **A** (G2, Review sites) | — |

---

### ⚠️ Prior Outreach Flags — Check Before Contacting

| Account | Flag | What to Do |
|---------|------|-----------|
| **TruStage** | ✅ **CONFIRMED CLEAR (Mar 9, 2026)** — 11 prior outreach signals confirmed as Shakeel's (former AE, departed). Apollo audit: all 3 TruStage contacts have zero Rob campaign activity (`emailer_campaign_ids: []`, `last_activity_date: null`). Clear to prospect. | Contact Chamath Guneratne. See Wave 1 contact roster below. |
| **Tailored Brands, Inc.** | "Outbound Engagement Completed 7" — 7 prior outreach touches tracked. ICP fit Low (Apparel). | Likely Shakeel's (same pattern). Deprioritize — Low ICP. Check Apollo contacts if needed. |
| **ACCELQ** | Competitor — G2 Event x19 = they are intensively monitoring Testsigma on G2 | Do NOT reach out without checking with leadership/AE first. |

---

### Enriched Contact Roster — Factor Accounts (Director+ only)

> **PURPOSE:** Permanent lookup table. Any session can read this to know exactly who to reach out to without re-running Apollo. Updated as contacts are researched. Always cross-check MASTER_SENT_LIST before sending.
>
> **Email status key:** ✅ Verified (Apollo confirmed) · ⚠️ Extrapolated (domain-pattern, not confirmed) · ❌ Old domain / likely stale
>
> **Outreach status:** 🟡 Drafted · ✅ Sent · ⛔ DNC · ⏸ On Hold

---

#### Wave 1 — Enriched Mar 9, 2026

**Cboe Global Markets** (Finance, HIGH ICP, Jan 2026 — Demo x2 + Signup x2)

| Name | Title | Email | Email Status | Priority | Outreach Status |
|------|-------|-------|-------------|----------|-----------------|
| Rick Brandt | Senior Director, Quality Assurance Engineering | rbrandt@cboe.com | ✅ Verified | PRIMARY | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Maurice Saunders | Senior Manager, Quality Assurance | msaunders@cboe.com | ✅ Verified | Same batch | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Snezhana Ruseva | Manager, DnA Software Engineering, Test | sruseva@cboe.com | ✅ Verified | Same batch | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |

---

**Fidelity Investments** (Finance, HIGH ICP, Aug 2025 — G2 + Use-case page)

| Name | Title | Email | Email Status | Priority | Outreach Status |
|------|-------|-------|-------------|----------|-----------------|
| Seth Drummond | Vice President, Quality Assurance | seth.drummond@fidelity.com | ✅ Verified | VP tier — PRIMARY | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Chris Pendergast | Vice President, Quality Engineering | chris.pendergast@fidelity.com | ✅ Verified | VP tier — same batch | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Christopher Bilcz | Vice President, Quality Engineering | christopher.bilcz@fmr.com | ✅ Verified | VP tier — same batch | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Eric Pearson | VP, Quality Assurance — Asset Allocation Technology | ep@fidelity.com | ✅ Verified | VP tier — same batch | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Nithya Arunkumar | Director, Quality Assurance | n.arunkumar@fidelity.com | ✅ Verified (Apollo shows stale "Principal SE" title) | Director tier — same batch | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Richelle Lacamera | Director, QA Management | richelle.lacamera@fidelity.com | ✅ Verified | Director tier — same batch | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Sourabh Roy | Director of QA — Green Meadows | sourabh.roy2@fmr.com | ✅ Verified | Director tier — same batch | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Padma Srikanth | Chapter Leader — Director of Quality Assurance | padma.srikanth@fmr.com | ✅ Verified | Director tier — same batch | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |

---

**JPMorgan Chase** (Finance, HIGH ICP, Oct 2025 — Pricing + Signup x2 + Use-case x3 + web x7)

| Name | Title | Email | Email Status | Priority | Outreach Status |
|------|-------|-------|-------------|----------|-----------------|
| Neeraj Tati | Director, Software Engineering | neeraj.tati@chase.com | ✅ Verified | Clean — enrolled | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Rose Serao | VP Quality Assurance Manager | rose.serao@chase.com | ⚠️ Extrapolated | PRIMARY — HOLD: email not Apollo-confirmed | ⏸ Hold (Rob must approve extrapolated email) |
| Justin Hutchinson | Executive Director — Quality Analysis | justin.hutchinson@jpmchase.com | ✅ Verified | HOLD: "Quality Analysis" may be ops QA not software QA | ⏸ Hold (Rob must verify role is software testing) |
| Nikki Urlaub | VP Quality Analysis Manager | nikki.urlaub@chase.com | ✅ Verified | HOLD: Same ops QA concern as Justin | ⏸ Hold (Rob must verify role is software testing) |

> DNC note: Jitesh Biswal (DNC) is at @jpmorgan.com — different domain from @chase.com. No conflict.

---

**Commvault** (Technology, HIGH ICP, Jun 2025 — G2 + Signup x2 + web x6)

| Name | Title | Email | Email Status | Priority | Outreach Status |
|------|-------|-------|-------------|----------|-----------------|
| Brahmaiah Vallabhaneni | Vice President of Engineering | bvallabhaneni@commvault.com | ✅ Verified | PRIMARY — VP tier | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Arun Amarendran | Vice President of Engineering | aamarendran@commvault.com | ✅ Verified | VP tier — same batch | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Jennifer Wang | Director of Engineering | jenniferwang@commvault.com | ✅ Verified | Director tier — same batch | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Prasad Alapati | Senior Software QA Manager | palapati@commvault.com | ✅ Verified | Manager tier — same batch | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Sucheth Ramgiri | Principal QA Engineer III — AI & Automation Strategy | sramgiri@commvault.com | ✅ Verified | IC influencer — AI & Automation Strategy role | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |

---

**TruStage** (Finance/Insurance, HIGH ICP, Feb 3 2026 — Demo x1 + Outbound x11)

> ✅ **CONFIRMED CLEAR Mar 9, 2026** — Shakeel (former AE, departed) sent the 11 prior outreach signals. Apollo shows zero Rob campaign activity. Clear to prospect.

| Name | Title | Email | Email Status | Priority | Outreach Status |
|------|-------|-------|-------------|----------|-----------------|
| Chamath Guneratne | IT Director, Quality Engineering | chamath.guneratne@trustage.com | ✅ Verified | PRIMARY | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Maggie Redden | Director, Software Engineering | maggie.redden@cunamutual.com | ✅ Verified (Apollo confirmed @cunamutual.com — old domain still active) | Same batch | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Jennifer Drangstveit | IT Director, Solution Delivery | jennifer.drangstveit@cunamutual.com | ✅ Verified | Same batch | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| Shawn Woods | QA / Release Manager | shawn.woods@trustage.com | ✅ Verified | HOLD: below Director threshold (3 Directors already enrolled) | ⏸ Hold (Rob must decide) |
| Amanda Hambly | QA Manager | (no email found) | — | Below-Director — skip | ⏸ Hold |

---

**YouTube / Google** (Technology, HIGH ICP, Sep 2025 — Signup + alt page + web x4)

| Name | Title | Email | Email Status | Priority | Outreach Status |
|------|-------|-------|-------------|----------|-----------------|
| Ramona Bobohalma | Director of Engineering | bobohalma@youtube.com | ✅ Verified but DISQUALIFIED — Zürich, Switzerland. Non-US fails ICP criterion. | DO NOT CONTACT | ❌ Disqualified (non-US) |
| **John Harding** | VP Engineering, YouTube Music & Premium | jharding@youtube.com | ✅ Catch-all verified. Apollo ID: 685908e0ad153600113e33a1 | PRIMARY | 📤 In Sequence (TAM Outbound, enrolled Mar 10) |
| **Des Keane** | Engineering Director, Video Infrastructure | des@google.com | ✅ Verified (Apollo headline stale "Coach" — real role confirmed) | Same batch — infrastructure/reliability angle | 📤 In Sequence (TAM Outbound, enrolled Mar 10 — job_change flag bypassed) |
| **Hrishikesh Aradhye** | Sr. Director, Music & Podcasts | hrishi@google.com | ✅ Verified | Same batch — Music & Podcasts angle | 📤 In Sequence (TAM Outbound, enrolled Mar 10 — job_change flag bypassed) |

> **Note:** YouTube/Google is a mega-enterprise (100,000+ employees). Targeting level = HIGH. Each contact must be written to their specific product area. Run expanded Apollo search for additional US-based QA/Eng Directors at YouTube specifically (not just Google broadly).

---

**Proof Point Assignments (Wave 1) — for reference:**

| Account | T1 Proof Point | T2 Proof Point (rotation) |
|---------|---------------|--------------------------|
| Cboe | Hansard: regression 8→5 weeks | CRED: 90% coverage + 5x velocity |
| Fidelity | Hansard: regression 8→5 weeks | CRED: 90% coverage + 5x velocity |
| Chase | Hansard: regression 8→5 weeks | CRED: 90% coverage + 5x velocity |
| TruStage | Hansard: regression 8→5 weeks | CRED: 90% coverage + 5x velocity |
| Commvault | Fortune 100: 3X QA productivity | Cisco: 35% regression reduction |
| YouTube | Nagra DTV: 2,500 tests, 4X faster | Medibuddy: 50% maintenance cut |

---

#### Wave 2 — ✅ T1 SENT Mar 10, 2026 (16 contacts)

**File:** `tamob-wave2-draft-mar10.html` | **T2 due:** Mar 15 | **Sequence:** TAM Outbound - Rob Gorham

| Contact | Company | Apollo ID | Status |
|---------|---------|-----------|--------|
| Marcela Fetters | GEICO | 69b077c4c0da4900152bb736 | ✅ T1 Sent Mar 10 |
| Roberto Bouza | GEICO | 69b0780dc0da4900152bb7d2 | ✅ T1 Sent Mar 10 |
| Sambhav Taneja | GEICO | 69b07814d45f4e00155d218b | ✅ T1 Sent Mar 10 |
| Chandni Jain | Checkr | 68f512c8398b310001070cb1 | ✅ T1 Sent Mar 10 |
| Sarah Kneedler | Checkr | 6992d954404e44000165dd64 | ✅ T1 Sent Mar 10 |
| Krista Moroder | Checkr | 68f512c8398b310001070cad | ✅ T1 Sent Mar 10 |
| Cristian Brotto | Checkr | 69b07821e4be74000d6bb911 | ✅ T1 Sent Mar 10 |
| Yu Jin | EA | 69b07827c0da49000dc24361 | ✅ T1 Sent Mar 10 |
| Maalika Tadinada | EA | 69b0783bd45f4e00155d21a4 | ✅ T1 Sent Mar 10 |
| Richelle Paulsen | Cetera | 68e69f9fb4d41000012370b0 | ✅ T1 Sent Mar 10 |
| Anton Aleksandrov | Cetera | 68caf92e67f171002139f184 | ✅ T1 Sent Mar 10 |
| Saeyed Shamlou | OneMain | 69371da04a3327000178a607 | ✅ T1 Sent Mar 10 |
| Karen Teng | Mindbody | 69b077ebc0da4900152bb77c | ✅ T1 Sent Mar 10 |
| Henry Rose | Mindbody | 69b07848c0da4900152bb7fd | ✅ T1 Sent Mar 10 |
| Bipin Bhoite | Mindbody | 69b0784fc0da49000dc24371 | ✅ T1 Sent Mar 10 |
| Shyamendra Singh | HashiCorp | 68af1cf6944539000183af4c | ✅ T1 Sent Mar 10 |

*Successive Technologies, OSF HealthCare — deferred to future wave*

---

#### Wave 3 — ✅ T1 SENT Mar 11, 2026 (35 contacts, 7 accounts)

**File:** `tamob-batch-20260311-1.html` | **T2 due:** Mar 16 | **Sequence:** TAM Outbound - Rob Gorham
⚠️ INC-008: Michael Cahill (L3Harris) + Manpreet Burmi (Veradigm) received placeholder sends — recovery emails sent same day. Recovery counts as real T1.

| Account | Contacts | Status |
|---------|----------|--------|
| Yahoo (YHQ + Sports) | 7 (Y01 Sarah Huang, Y02 Ash Pedgaonkar, Y03–Y07) | ✅ All T1 Sent Mar 11 |
| Veradigm | 6 (V01 Ted Barker, V02 Matthew Bennett, V03–V06 incl Manpreet Burmi recovery) | ✅ All T1 Sent Mar 11 |
| Charlie Health | 4 (CH01 Sampson Reider, CH02 Madina Zabran, CH03 Madison Waterman, CH04 Ashwin Vaswani) | ✅ All T1 Sent Mar 11 |
| TELUS | 2 (T01 Christine Gamache — future-dated, T02) | T01 pending (auto-surface) |
| GE HealthCare | 2 (GE01, GE02 Brooks Foley — future-dated) | GE02 pending (auto-surface) |
| L3Harris Technologies | 9 (L01–L09 incl Michael Cahill recovery) | ✅ All T1 Sent Mar 11 |
| Georgia-Pacific | 5 (GP01–GP05) | ✅ All T1 Sent Mar 11 |

#### Wave 4 — ✅ T1 SENT Mar 11, 2026 (37/48 confirmed, 19 accounts)

**File:** `tamob-batch-20260311-2.html` | **T2 due:** Mar 19 | **Sequence:** TAM Outbound - Rob Gorham

| Account | Contacts sent | Notes |
|---------|--------------|-------|
| E*TRADE / Morgan Stanley | Brett Linde, Chyehar Tyler | ✅ Sent |
| Broadcom | Hai Su, Jeremy Sabin | ✅ Sent |
| Humana | Justin Yune, Piyamas Sattaboot | ✅ Sent |
| Corewell Health | Aswini Nagabooshanam, Vibha Singh, Samatha Gangyshetty | ✅ Sent |
| Blue Cross MN | Ahmet Cakar | ✅ Sent |
| BCBS Texas | Sakib Alam, Ganesh Mallina | ✅ Sent |
| Blue Cross KC | Kris Berg, Ranjith Reddy | ✅ Sent |
| Mastercard | Yvonne Stephen, Vijay Durairaj, Ketan Rathod, Geethavani Dodda, Koushal Ram, Glen Hudson (auto), Sibghatullah Veedy (auto) | ✅ 7 sent. Yvonne Oliver blocked (ownership). Ksenia Shchelkonogova bounced. |
| Anaplan | Mike Seal + Irina Baxter (pending task) | 1 sent, 1 pending |
| DraftKings | Francky Sergile, David Schraff | ✅ Sent |
| Cleveland Clinic | Ted Machicek, Satish Krishnan | ✅ Sent |
| Microchip Technology | April Brenay, Manohar Shrestha | ✅ Sent |
| GEICO (W4 contacts) | Ketan Peddabachi | ✅ Sent |
| Electronic Arts (W4 contacts) | Ed Yiu, William Xie + Divya Sathish/Jiadong Shen/Simon Crawford (pending tasks) | 2 sent, 3 pending |
| HashiCorp (W4 contacts) | Janel Jolly + Adit Shah (pending task) | 1 sent, 1 pending |
| KKR | Devashish Patel, Josh Klesel | ✅ Sent |
| Datamatics (W4 contacts) | Kenny Qi, Michelle Crawford + Mohan Raj/Shilendra Sharma/Poonam Patil (pending tasks) | 2 sent, 3 pending |
| OneMain Financial (W4 contacts) | Jessica Harris | ✅ Sent |
| BCBS Illinois | Valerie Jefferies | 🚫 Blocked — job change flag |

---

Start with HIGH ICP + Tier A signals + most recent activity. Cross-check each against MASTER_SENT_LIST first.

**Wave 1 — Start here (HIGH ICP + strong buying signals):**
1. **Chase** — Finance/Enterprise, 5 distinct signal types (Pricing + Demo + Signup + Use-case + 7 web sessions). Freshly active Oct 2025. Highest signal volume of any account.
2. **Cboe Global Markets** — Finance/Enterprise, Signup x2 + Demo x2. Last activity Jan 9, 2026 — freshest of all 38.
3. **Commvault** — Tech/Enterprise, G2 + Signup x2 + 6 web sessions. Active Jun 2025.
4. **Fidelity Investments** — Finance/Enterprise, G2 + Use-case page visit. Active Aug 2025.
5. **YouTube** — Tech/Enterprise, Signup + 4 web sessions. Active Sep 2025.
6. **TruStage** — Finance/Enterprise, Demo + recent Feb 2026 activity. ✅ Confirmed clear Mar 9 — prior outreach was Shakeel's (former AE, departed). Contact: Chamath Guneratne, IT Director QE.

**Wave 2 — ✅ SENT Mar 10 (16 contacts):**
7. **HashiCorp** — 1 contact (Shyamendra Singh). T2 due Mar 15.
8. **Datamatics** — covered in Wave 4 (separate contacts). Wave 2 = HashiCorp + GEICO + Checkr + EA + OneMain + Mindbody + Cetera.
9. ~~Successive Technologies~~ — deferred.
10. **Electronic Arts** — 2 contacts Wave 2 (Yu Jin, Maalika Tadinada). Additional 5 in Wave 4.
11. **GEICO** — 3 contacts Wave 2 (Marcela Fetters, Roberto Bouza, Sambhav Taneja). 1 more in Wave 4.
12. **Checkr, Inc.** — 4 contacts (Chandni Jain, Sarah Kneedler, Krista Moroder, Cristian Brotto). T2 due Mar 15.

**Wave 3 — ✅ SENT Mar 11 (35 contacts):**
13. Veradigm (6 contacts). T2 due Mar 16.
14. Corewell Health — covered in Wave 4 (3 contacts). Wave 3 Corewell = zero; Wave 3 had Yahoo, Charlie Health, TELUS, GE HealthCare, L3Harris, Georgia-Pacific.
15. Charlie Health (4 contacts). T2 due Mar 16.

**Wave 4 — ✅ SENT Mar 11 (37/48 sent, 9 pending, 19 accounts):**
16+ E*TRADE/Morgan Stanley, Broadcom, Humana, Corewell Health, Blue Cross MN/TX/KC, Mastercard, Anaplan, DraftKings, Cleveland Clinic, Microchip, GEICO (W4), EA (W4), HashiCorp (W4), KKR, Datamatics (W4), OneMain (W4), BCBS IL. T2 due Mar 19.

**Deprioritize / skip for now:**
- ACCELQ — competitor, needs clearance
- Tailored Brands — Low ICP, prior outreach flag
- bp, KKR, CDC, Georgia-Pacific, PGA of America — Low/Medium ICP fit
- Plenty, Market of Choice, Springboard — commercial/low-fit

---

**ICP Priority Summary (HIGH fit = 18 accounts):**
Chase, Fidelity Investments, Cetera Financial Group, Cboe Global Markets, TruStage, GEICO, OneMain Financial (Finance/Insurance) · Mindbody, OSF HealthCare, Veradigm, Corewell Health, Charlie Health (Healthcare) · HashiCorp, Commvault, Datamatics, Checkr Inc., Successive Technologies, YouTube, Yahoo, Electronic Arts (Technology/SaaS)

---

## 2. TAM Accounts — Oct 2025 (Named Account List)

**What they are:** Testsigma's Total Addressable Market accounts for Rob's NAMER region. Built and assigned by the LDR team using ICP criteria (industry, employees, business type). This is Rob's primary named account universe.

**Total:** 312 accounts (exported Mar 9, 2026)
**Full list:** `/Work/tam-accounts-mar26.csv` (Account Name, Location, LinkedIn URL, Domain, Owner)

**Salesforce Reports:**
- [TAM Account List](https://d2v000000sgbdea0.lightning.force.com/lightning/r/Report/00OOX00000H3IwL2AV/view?queryScope=userFolders) — company list
- [TAM Contacts (enriched)](https://d2v000000sgbdea0.lightning.force.com/lightning/r/Report/00OOX00000H8ucj2AB/view?queryScope=userFolders) — ICP contacts already enriched and uploaded by LDR team

**Context:** Contacts were enriched by the LDR team in batches (confirmed Oct 21, 2025 follow-up from Muthu). These contacts should already be in Salesforce/CRM. Additional contacts can be requested from ldr-team@testsigma.com.

**Status:** Assigned Oct 2025. Full list captured Mar 9, 2026.

### ⚠️ Known Flags in TAM List

| Account | Flag |
|---------|------|
| ACCELQ | Competitor — DO NOT contact without leadership clearance |
| Kapitus | DNC — Abe Blanco replied "not interested" Mar 4 |
| OverDrive | Active warm lead — Namita Jain (Touch 1 sent Feb 27) |
| trailblazercgl, Samozatrudnienie, Confidencial, gnc-hq.com | Data quality issues — likely bad records, skip |
| Government orgs (DC Gov, State of NJ, Texas DOT, Michigan DHHS, City of Hamilton, LA Metro, Service New Brunswick, Govt of Canada, Buenos Aires, Godoy Cruz) | Out of ICP — government entities |

### High-ICP TAM Accounts NOT Already in Factor List

These are the best untouched accounts to target next (not in the 38 Factor accounts):

**Finance / Insurance (HIGH priority):**
Morgan Stanley, BMO, BlackRock, Mastercard, Allianz Life US, Farmers Insurance, Blue Cross Blue Shield, Humana, Great American Insurance, Pacific Life, Selective Insurance, EmblemHealth, Definity, AssuredPartners, Jack Henry, Bluevine, Lemonade, SailPoint, Everbridge, ID.me

**Healthcare / Life Sciences (HIGH priority):**
Cleveland Clinic, Memorial Sloan Kettering, Dana-Farber Cancer Institute, Children's Hospital of Philadelphia, HonorHealth, Evernorth Health Services, Point32Health, Vaya Health, Health Net, hims & hers, Johnson & Johnson MedTech, Acadia Pharmaceuticals, Zimmer Biomet, Tandem Diabetes Care, Clinisys, Incyte, Radiology Partners

**Tech / SaaS / Security (HIGH priority):**
Broadcom, Check Point Software, BeyondTrust, WatchGuard Technologies, Sysdig, Procore Technologies, Anaplan, Yext, Epicor, Infor, Celonis, SingleStore, Couchbase, Pathlock, AppLovin, Bungie, Bethesda Softworks, DraftKings, Square / Cash App, Pluralsight, Incode Technologies, Zipline, Dark Matter Technologies, Webex, Aura

---

## 3. Manual Testers Footprint TAM (Supplemental — Oct 2025)

**What they are:** A second TAM list shared with ALL BDRs and AEs, focused specifically on companies with significant manual testing footprints (highest Testsigma conversion potential). These are OVER AND ABOVE the Oct 2025 TAM.

**Salesforce Report:** [Manual Testers TAM](https://d2v000000sgbdea0.lightning.force.com/lightning/r/Report/00OOX00000HGoa92AD/view?queryScope=userFolders)

**AE POD for Rob (NAMER):** Tyler Kapeller + Eshwar
**Strategy:** Sync with Tyler/Eshwar to develop a coordinated attack plan. Outbound only (not inbound).

**Context:** Assigned Oct 28, 2025. Manual testers angle = prime fit for Testsigma's NLP test creation pitch (write tests in plain English, reduce manual testing burden).

**Status:** Unknown — check MASTER_SENT_LIST for any contacts already worked from these accounts.

---

## 4. Farming Accounts (Active Customers — Feb 2026)

**What they are:** ~10 existing Testsigma customers assigned to Rob for upsell/cross-sell expansion. These are NOT cold prospects — they are current paying customers.

**Salesforce Report:** [Active Customer List](https://d2v000000sgbdea0.lightning.force.com/lightning/r/Report/00OOX000009bkmt2AA/view?queryScope=userFolders)

**Strategy:** NOT a cold approach. Before outreach, sync with the assigned AE/CSM to understand the current use case and build a pitch in liaison with them.

**Context:** Assigned Feb 10, 2026. Mithun followed up Mar 5, 2026 reminding AE team to work with their BDRs on upsell/cross-sell.

**Status:** Unknown — check with AE/CSM before any outreach.

---

## Using Named Accounts in Prospecting

All batches must be built from within the TAM + Factor universe. No open prospecting.

**Batch build order:**
1. Factor accounts Wave 1 first (Chase, Cboe, Commvault, Fidelity, YouTube, TruStage — see section above)
2. Factor accounts Wave 2 (HIGH ICP + Tier B signals)
3. Factor accounts Wave 3 (newly added, no Nektar history)
4. Untouched TAM — HIGH ICP first (142 accounts), then Medium (153)
5. Manual Testers TAM — supplement after TAM coverage is underway
6. Farming accounts — separate motion, always coordinate with AE/CSM. Do NOT cold-pitch.

**⚠️ MASTER_SENT_LIST limitation:** The sent list tracks people (names only), not companies. This makes programmatic cross-referencing against TAM account names impossible. **Fix going forward:** When adding to MASTER_SENT_LIST, also log the company name in a new column. This will enable dedup by account (not just by person).

→ See `memory/sop-daily.md` → Batch Sourcing Decision Framework for the full waterfall.

---

## Key Contacts

| Person | Role | Relevance |
|--------|------|-----------|
| Muthu (Muthazhagu Sevugen) | LDR Team | Assigned TAM accounts, enriched contacts. Contact for additional enrichment. |
| Mithun Dharanendraiah | Sales Manager/Ops | Oversees BDR team, assigned Factors + Farming accounts |
| Tyler Kapeller | AE (NAMER) | Rob's primary AE POD partner. Coordinate on NAMER outbound. |
| Eshwar | AE (NAMER) | Rob's secondary AE POD partner |
