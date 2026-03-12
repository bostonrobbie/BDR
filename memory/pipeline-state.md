# Pipeline State & Send History

---

## Mar 10 Status — Tyler Referrals T1 Complete

**Date:** 2026-03-10
**Action:** All 7 Tyler Kapeller referral T1 messages sent.
- 6 emails via Apollo UI (LinkedIn Outbound sequence, robert.gorham@testsigma.com ✅)
- 1 InMail via Sales Navigator (Vernon Bryant, Tractor Supply) — 1 credit used, 3 remaining
**T2 due:** Mar 14 (Day 5) for all 7
**Batch tracker:** `tyler-referrals-outreach-mar10.html`
**MASTER_SENT_LIST.csv:** Updated (299 rows → 299 + 7 = 300 total, including header = 300 lines)

---

## Mar 9 Status — T2 Drafts Approved (APPROVE SEND Granted)

**Date:** 2026-03-09
**Action:** Rob granted APPROVE SEND for all 28 T2 email drafts built this session.
**File:** `/Work/t2-email-drafts-mar9.html`
**Formula:** Locked Variant A (company fact → "I'd imagine..." → LinkedIn callback → customer story + tie-back → engagement CTA). Full spec in `memory/sop-email.md`.
**Send from:** robert.gorham@testsigma.com ONLY. Rob executes sends manually.

| Batch | Drafts ready | Notes |
|-------|-------------|-------|
| B9 | 16 | Kylie Summer (Quizizz) + Yuliya A (Planview) missing emails — pending Rob decision |
| B10 | 9 | Sravanti Krothapalli email domain qbsol.com ⚠️ may be prior employer — verify before sending |
| B11 | 3 | Dan Heintzelman (Prevail Legal) missing email — pending Rob decision |
| **Total** | **28** | |

**B9 is overdue (Day 5+ as of Mar 9). Send B9 first.**
**B10/B11 T2 due Mar 11 (Day 5 from Mar 6 T1 sends).**

---

## Mar 7 Audit Findings (Apollo Full Cross-Channel Audit)

**Conducted:** Mar 7, 2026. Full Apollo sequence audit + Gmail cross-channel double-send check.

### Key Findings

**Email tracking gap — partially resolved (Mar 7 update):**
- Apollo "Email Outbound - Website Visitor Tier 1" sequence shows **81 delivered** in Apollo UI. Gap between Apollo stat (81) and Gmail-confirmed WV emails (28: 19 Mar 3 + 7 Mar 6 + 2 Mar 7) is unexplained — may be pre-campaign sends or different counting period.
- Gmail (robert.gorham@testsigma.com) shows **201 total sent messages** — includes calendar invites, internal forwards, and non-outreach. Confirmed outreach emails: **49** (see Email Send History).
- All 19 Mar 3 Website Visitor batch emails now logged in Email Send History.
- **⚠️ Double-channel flag: Jason Schwichtenberg (WebMD)** received both a Mar 3 email AND a Batch 8 Day 3 InMail same day.
- **⚠️ Amir Aly (Procore)** received "One more thought" Mar 6 but not in original 9-person Buyer Intent email cohort. Touch 1 was InMail only.
- Remaining 5 Buyer Intent Touch 2 status (Jose Moreno, Tom Yang, Eyal Luxenburg, Jeff Barnes, Todd Willms, Jason Ruan) — not confirmed sent via email. May have been InMail-only. ⚠️ Needs follow-up.

**B10 enrollment gaps — partial resolution:**
- 10 gap contacts approved by Rob for enrollment.
- **Gil Taub (Kahuna)**: ✅ ENROLLED in Q1 Priority Accounts (Mar 7).
- **Sasa Lazarevic, Christian Melville, Jason Poole, Tim Wiseman**: ❌ BLOCKED — Apollo API rejects with `contacts_without_ownership_permission` even with override flag set. These contacts are owned by a different Apollo team member. **Need manual UI enrollment by Rob, or ownership reassignment in Apollo.**
- 6 B10 skipped contacts (Kristyn Burke, Tim Hartgrave, Vince Delfini, Padmanaban Vadivelu, Ravi Nag) — enrollment NOT YET ATTEMPTED (interrupted by email discovery).

**Mystery sequence identified:**
- Sequence ID `6904f70577baa100190e4858` = **"Outbound Calls (tyler) Only"** (created Oct 31, 2025, NOT archived).
- **Tom Goody (Ncontracts)** and **Mohan Guruswamy (Tavant)** were enrolled in this sequence Mar 7 by a prior Claude instance in the same session.
- Rule clarification from Rob: "we can add people who I have called before as long as we never spoke." These two had Tyler's call-only outreach, no conversation. Safe to also enroll in LI Outbound.
- Action: Verify Tom Goody + Mohan Guruswamy are also enrolled in LinkedIn Outbound - Q1 Priority Accounts.

**Cross-channel double-send check:**
- Buyer Intent cohort (9 people): ✅ CLEAN — no InMail overlap.
- INC-001 overlap (Irfan, Katie, Rachana, Giang): confirmed double-channel but known/documented.
- Yassi Dastan Batch 6 entry: **MISSING from MASTER_SENT_LIST.csv** (only Batch 8 shown). CSV updated Mar 7 to add B6 entry (Feb 28, InMail, credit used).
- B3-B9 enrollment spot-check (Irfan Syed, Christie Howard, Yassi Dastan, Samata Yarlagadda, Mohan Guruswamy, Rick Kowaleski): ✅ All correctly enrolled in Q1 Priority Accounts.
- Total confirmed InMail-only double-sends: **6** (Chuck Smith, Abe Blanco, Rick Kowaleski, Christie Howard, Mohan Gummadi, Yassi Dastan).
- **⚠️ NEW: 4 cross-channel (InMail + email) double-contacts discovered Mar 7 email audit:**
  - **Jason Schwichtenberg (WebMD)**: Batch 8 InMail Mar 3 + Website Visitor email Mar 3 — SAME DAY.
  - **Lyle Landry (Availity)**: Batch 5B InMail Feb 27 + Website Visitor email Mar 3.
  - **Kerri McGee (Sapiens)**: Batch 5A InMail Feb 27 + Website Visitor email Mar 3.
  - **Jamie Kurt (Vertafore)**: Batch 5B InMail Feb 27 + Website Visitor email Mar 3.
  - These cannot be unsent. Monitor for replies. Treat as multi-touch contacts.
- MASTER_SENT_LIST.csv updated Mar 7: added 28 email-only contacts (15 Mar 3 WV batch + 4 Buyer Intent T2 + 7 Mar 6 WV batch + 2 Mar 7 WV batch). CSV now 278 rows.

**Full audit report:** `/Work/audit-report-mar6.html`

---

## Master Send Log (Updated Mar 6 — post Batch 11 sends)

### Lifetime Totals
| Date | Batch | Sends | Cumulative |
|------|-------|-------|------------|
| Feb 13 | Earlier batches | 8 | 8 |
| Feb 25 | Batch 3 (pilot: Irfan, Katie) | 2 | 10 |
| Feb 26 | Batch 3 (remaining 22) | 22 | 32 |
| Feb 27 | Batch 5B | 23 | 55 |
| Feb 27 | Batch 5A (partial: 5) | 5 | 60 |
| Feb 28 | Batch 5A (remaining 20) | 20 | 80 |
| Feb 28 | Batch 6 (all 27) | 27 | 107 |
| Feb 28 | Batch 7 (41 sent, 1 NOT FOUND) | 41 | 148 |
| Mar 1 | Overflow (7) | 7 | 155 |
| Mar 2 | Batch 8 (7 sent, 1 NOT FOUND) | 7 | 162 |
| Mar 3 | Batch 8 Day 2 (6 sent, 1 SKIPPED) | 6 | 168 |
| Mar 3 | Batch 8 Day 3 (6 sent, 2 SKIPPED) | 6 | 174 |
| Mar 3 | Batch 8 Day 4 (8 sent, 1 disabled comms) | 8 | 182 |
| Mar 3 | Batch 8 Day 5 (8 sent) | 8 | 190 |
| Mar 3 | Batch 8 Day 6 (8 sent, 1 NOT FOUND, 2 FREE) | 8 | 198 |
| Mar 3 | Batch 9 (6 sent UNTRACKED — see audit note below) | 6 | 204 |
| Mar 6 | Q1 QA Outreach → LI Outbound migration (26 enrolled) | 0 InMails | — |
| Mar 6 | Batch 10 created (25 drafts ready, not yet sent) | 0 | 204 |
| Mar 6 | Batch 10 Module A2 preflight complete (22 CLEAN, 1 BLOCKED, 1 UNVERIFIABLE) | 0 sends | 204 |
| Mar 4 | Batch 9 — 11 sent UNTRACKED (discovered Mar 6 via inbox sweep) | 11 | 215 |
| Mar 6 | Batch 10 — 9 sent (3 free + 6 credit InMails) | 9 | 224 |
| Mar 6 | Batch 11 — 4 sent (4 credit InMails) | 4 | 228 |
| Mar 10 | Tyler Referrals T1 — 6 emails + 1 InMail (Vernon Bryant/Tractor Supply) | 7 | 235 |
| Mar 10 | TAM Outbound Wave 1 T1 — 23 sent via Apollo Tasks (⚠️ INC-007: all placeholder sends. Recovery: 24/25 real emails sent via Gmail Chrome same day) | 23 placeholder + 24 recovery | 282 |
| Mar 10 | TAM Outbound Wave 2 T1 — 16 sent via Apollo Tasks (robert.gorham@testsigma.com) | 16 | 298 |
| Mar 11 | TAM Outbound Wave 3 T1 — 35 enrolled, 33 sent via Apollo Tasks + 2 future-dated (Christine Gamache/TELUS, Brooks Foley/GE HealthCare). ⚠️ INC-008: 2 placeholder sends (Michael Cahill L3Harris, Manpreet Burmi Veradigm) — recovery emails sent. | 33 (+2 pending) | 331 |
| Mar 11 | TAM Outbound Wave 4 T1 — 48 enrolled. 37 sent (35 via Apollo Tasks + 2 auto-sent by Apollo: Glen Hudson + Sibghatullah Veedy). 2 blocked (Valerie Jefferies job change, Yvonne Oliver ownership error). **10 bounced** (Ksenia Shchelkonogova + Jessica Harris, William Xie, David Schraff, Mike Seal, Koushal Ram, Sakib Alam, Samatha Gangyshetty, Ahmet Cakar — all discovered Mar 12 Gmail scan). 9 step 1 tasks pending in Apollo queue. | 37 | 368 |
| Mar 12 | TAM Outbound Batch 5 — 5 enrolled (of 13 drafted). 5 non-TAM (DocuSign, Bentley) removed per INC-010. 2 Infor contacts (Mirza Hasan, Daniela Young) excluded (prior phone contact). 1 (Yogesh Garg, Check Point) enrollment blocked by Apollo ownership error — needs manual fix. | 5 enrolled (pending T1 send) | 368 |

### Email Send History
| Date | Time | Recipients | Type | Status |
|------|------|-----------|------|--------|
| Feb 27 | ~1:30 PM | Andy Nelsen, Jose Moreno, Tom Yang, Eyal Luxenburg, Hibatullah Ahmed, Jeff Barnes, Eduardo Menezes, Todd Willms, Jason Ruan | Buyer Intent Touch 1 | SENT (HC1 violations, needs C2 rewrite) |
| Feb 28 | 6:30-6:33 AM | Irfan Syed, Katie Hotard, Rachana Jagetia, Giang Hoang, Pallavi Sheshadri, Gunasekaran Chandrasekaran | PREMATURE Touch 3 | SENT IN ERROR (INC-001) |
| Feb 28 | ~2:54 PM | Sergey, Mobin, Dino, Matthew, Joshua, Pete | Touch 3 Draft | NOT SENT (premature, delete) |
| Mar 2 | 12:41 PM | Pallavi Sheshadri | In-thread reply | SENT (warm lead follow-up) |
| Mar 3 | 4:10–6:46 PM UTC | Shivaleela Devarangadi (rxsense), Stephen Starnaud (biberk), Kyung Kim (webmd), Jason Schwichtenberg (webmd.net) ⚠️DOUBLE-CHANNEL, Geoffrey Juma (solera), Olivia Pereiraclarke (sapiens), Nabil Ahmed (progyny), Sneha Bairappa (aamc), Jim Lenihan (waystar), Courtney Corbin (vizientinc), Jamie Kurt (vertafore), Avijit Sur (solera), Kerri McGee (sapiens), Konstantin Diachenko (paymentus), Morya Moyal (hippo), Priya Khemani (getinsured), Keith Schofield (fullsteam), Emre Ozdemir (theocc), Lyle Landry (availity) | Website Visitor Tier 1 Touch 1 | SENT — 19 emails. ⚠️ WERE UNTRACKED. Added Mar 7 audit. ⚠️ Jason Schwichtenberg also received Batch 8 Day 3 InMail same day. |
| Mar 4 | 1:24 PM ET | Jason Dudley (RW Baird) | Warm follow-up "Testsigma Trial" | SENT |
| Mar 6 | 4:01–6:35 PM UTC | Mark Townsend (Silvaco), Kanwar Sangwan (DISQO), Alex Wong (Qualified), Prateek Negi (CData), Misty Pesek (Marigold), Katrina Walker (FreeWill), Joe Biggert (Marigold) | Website Visitor Tier 1 Touch 1 "Quick question" | SENT — 7 emails. ⚠️ Were untracked. |
| Mar 6 | 12:50–12:52 PM ET | Andy Nelsen (Rightworks), Eduardo Menezes (Fulgent Genetics), Hibatullah Ahmed (SPS Commerce), Amir Aly (Procore) ⚠️ANOMALY | Buyer Intent Touch 2 "One more thought" | SENT — 4 emails. ⚠️ Amir Aly NOT in original 9-person Buyer Intent cohort. No prior email thread — Touch 1 was InMail only. Other 5 Buyer Intent prospects (Jose Moreno, Tom Yang, Eyal Luxenburg, Jeff Barnes, Todd Willms, Jason Ruan) Touch 2 status unknown. |
| Mar 7 | 2:01–2:02 AM UTC | Chris Bell (Crestron), Davor Milosevic (IQVIA) | Website Visitor Tier 1 Touch 1 | SENT — 2 emails. Sent automatically by Apollo overnight. |
| Mar 9 | ~2:00–3:06 PM ET | **B9 T2 (16 sent):** Georgii Petrosian (AuditBoard), Mohan Guruswamy (Tavant), Lueanne Fitzhugh (Cerner), Jeremy Cira (Kaseya), Chandana Ray (Persistent Systems), Martha Horns (Greenway Health), David Gustafson (HG Insights), Jiaping Shen (HackerRank), Sravanti Krothapalli (Quorum Software, sent to qbsol.com), Cooper Morrow (Jama Software), Manigandan Kanagasabai (Mediaocean), Leah Coates (Perforce), Kanan Hasanzade (Datto), Azam Quraishi (MTX Group), Grant Anderson (Lucid), Denise Barnett (Progress Software) | B9 Touch 2 — Variant A formula via Apollo UI | SENT — 16 emails. ⚠️ Drafts 1-16 sent from **robert.gorham@testsigma.net** (Apollo default was incorrectly .net — not caught until Draft 26). Rob aware. |
| Mar 9 | ~2:00–3:06 PM ET | **B10 T2 (6 sent):** Josh Thayer (Jenius Bank), Elena Lysenko (CFSB), Tom Goody (Ncontracts), Francesco Leising (Fairfax Software), Chet West (Tempworks), Clint Parker (Simpro Group) | B10 Touch 2 — Variant A formula via Apollo UI | SENT — 6 emails. ⚠️ Drafts 18, 19, 21, 23, 24, 25 sent from **robert.gorham@testsigma.net** (same .net issue as B9 batch). **3 skipped:** Tim Wiseman (Draft 17) wrong owner/sequence; Jason Poole (Draft 20) wrong owner; LP Guo (Draft 22) no sequences in Apollo. |
| Mar 9 | ~2:00–3:06 PM ET | **B11 T2 (3 sent):** Brad Askins (Trimble), Dan Heintzelman (Prevail Legal), Madhu Nedunuri (IDB Bank) | B11 Touch 2 — Variant A formula via Apollo UI | SENT — 3 emails from **robert.gorham@testsigma.com** ✅ (From address corrected starting with Draft 26). |
| Mar 10 | Tyler Referrals T1 — 6 emails: Gopi Subramaniam (Staples), Pranati Thankala (Aetna), Roy Life (Sandia), Devin Griffin (FCB), Jason Berube (FCB), Skie Kagulire (FCB). 1 InMail: Vernon Bryant (Tractor Supply, 1 credit). | Tyler Kapeller referral T1 — LinkedIn Outbound sequence (email) + Sales Nav InMail | SENT — 6 emails via Apollo (robert.gorham@testsigma.com ✅), 1 InMail via Sales Nav. T2 due Mar 14. InMail credits: 3 remaining. Batch tracker: tyler-referrals-outreach-mar10.html |

### Mar 2 Batch 8 InMails (confirmed)
| # | Name | Company | Title (Sales Nav) | Subject | Time | Credits |
|---|------|---------|-------------------|---------|------|---------|
| 1 | Venkata Upputuri | InvoiceCloud | Sr SDET | Billing platform test upkeep | 6:39 PM | 1 used (67→66) |
| 2 | Affan Rashid | Applied Systems | Sr SDET | Insurance platform regression | 6:39 PM | 1 used (66→65) |
| 3 | Roni Kaya | Pathward | — | — | SKIPPED | NOT FOUND on Sales Nav |
| 4 | Anandbabu Singadurai | Elevate | Senior SDET | Credit product test coverage | 6:42 PM | Free to Open Profile |
| 5 | Mohammad Mian | Acorns | Sr. SDET | Investment app test upkeep | 6:45 PM | 1 used (65→64) |
| 6 | Jake Durand | Phreesia | Senior SDET | Healthcare intake platform testing | 6:52 PM | 1 used (64→63) |
| 7 | Subrato Sarkar | DrFirst | Principal SDET (promoted) | E-prescribing platform regression | 6:55 PM | 1 used (63→62) |
| 8 | Vishesh Bagga | Okta | Senior SDET | Identity platform test scale | 6:59 PM | 1 used (62→61) |

### Mar 3 Batch 8 Day 2 InMails (confirmed)
| # | Name | Company | Title | Subject | Time | Credits |
|---|------|---------|-------|---------|------|---------|
| 9 | Lidia Utesheva | SonderMind | QA Engineering Manager | Telehealth regression testing | 7:14 PM | 1 used (61→60) |
| 10 | Autumn Kennedy | Tala | QA Engineering Manager | Global lending test coverage | 7:17 PM | 1 used (60→59) |
| 11 | Chris O'Neill | Jack Henry | QA Engineering Manager | — | SKIPPED | Already messaged |
| 12 | Clayton Gould | OpenX | QA Engineering Manager | Programmatic ad test coverage | 7:28 PM | 1 used (59→58) |
| 13 | Olga Norton | Popmenu | QA Manager | — (1st degree, free msg) | 8:03 PM | Free (58) |
| 14 | Kaitlyn Kirchhausen | Hometap | QA Engineering Manager | Fintech regression cycles | ~8:45 PM | 1 used (58→57) |
| 15 | Niveditha Bharadwaj | Lendbuzz | QA Engineering Manager | Auto lending test coverage | ~8:50 PM | 1 used (57→56) |
| 16 | Abe Blanco | Kapitus | QA Engineering Manager | SMB lending test upkeep | ~8:55 PM | 1 used (56→55) |

### Mar 3 Batch 8 Day 3 InMails (confirmed)
| # | Name | Company | Title | Subject | Time | Credits |
|---|------|---------|-------|---------|------|---------|
| 17 | Sara Triehy | Dynata | QA Engineering Manager | Survey data platform testing | ~9:19 PM | 1 used (55→54) |
| 18 | Victor Ionin | Aurora Solar | — | — | SKIPPED | NOT FOUND on Sales Nav |
| 19 | Sowjanya Palleti | Roku | QA Engineering Manager | Streaming platform regression | ~9:24 PM | 1 used (54→53) |
| 20 | Renata Jundo-Scensnovic | Centerfield | — | — | SKIPPED | NOT FOUND on Sales Nav |
| 21 | Lizmarie Pantoja | Insulet | QA Engineering Manager | Medical device software testing | ~9:32 PM | 1 used (53→52) |
| 22 | Priya Sethuvinayakam | AliveCor | Software QA Engineering Manager | Cardiac monitoring platform testing | ~9:34 PM | 1 used (52→51) |
| 23 | Monica Taduru | Aya Healthcare | (QA role) | Healthcare staffing platform testing | ~9:37 PM | 1 used (51→50) |
| 24 | Jason Schwichtenberg | WebMD | (headline: Quality not Quantity) | Health content platform regression | ~9:43 PM | 1 used (50→49) |

### Mar 3 Batch 8 Day 4 InMails (confirmed)
| # | Name | Company | Title | Subject | Time | Credits |
|---|------|---------|-------|---------|------|---------|
| 25 | Crystal Howard | DeliverHealth | SW Test Engineering Manager | Healthcare platform test coverage | ~5:30 AM | 1 used (49→48) |
| 26 | Geoffrey Juma | Solera Holdings | Manager SQE | — | SKIPPED | Disabled comms |
| 27 | Jorge Garcia | Commure | Senior QA Manager | Healthcare interop regression | ~5:35 AM | 1 used (48→47) |
| 28 | Christie Howard | LastPass | Sr Director Quality Engineering | Security product regression | ~5:40 AM | 1 used (47→46) |
| 29 | Kenny Liu | ModMed | Sr Director SW Development | EHR platform test coverage | ~5:45 AM | 1 used (46→45) |
| 30 | Yuehli DeWolf | Vertafore | Sr Director SW QA | Insurance platform regression | ~5:50 AM | 1 used (45→44) |
| 31 | Sridharan Gopal | Bottomline | Sr. Director SW Engineering | Payment platform testing | ~5:55 AM | 1 used (44→43) |
| 32 | Scott Carruth | Abrigo | Senior Director QA | Financial compliance testing | ~6:00 AM | 1 used (43→42) |

### Mar 3 Batch 8 Day 5 InMails (confirmed)
| # | Name | Company | Title | Subject | Time | Credits |
|---|------|---------|-------|---------|------|---------|
| 33 | Karen Motyka | Quickbase | Sr Director Quality Engineering | Low-code platform regression | ~6:05 AM | 1 used (42→41) |
| 34 | Jeff Chartos | Early Warning/Paze | Sr. Director Quality Engineering | Payment platform testing | ~6:10 AM | 1 used (41→40) |
| 35 | Tracy Grooms | Buildertrend | Sr. Director QA | Construction platform testing | ~6:15 AM | 1 used (40→39) |
| 36 | Shana Johnson | Quest Analytics | QA Leader & Advocate | Healthcare data test coverage | ~6:20 AM | Free to Open Profile |
| 37 | Dickson Wu | AuditBoard | Director Quality & Localization | Audit platform regression | ~6:25 AM | 1 used (39→38) |
| 38 | Yassi Dastan | Cvent | Senior Director Quality Engineering | Testing at Cvent's scale | ~6:30 AM | 1 used (38→37) |
| 39 | Akshaya Ponnappa | Vitech | Technology & Product Platform Exec | Insurance platform regression cycles | ~6:33 AM | 1 used (37→36) |
| 40 | Shefali Singh | ON24 | Sr. Director QA | Testing speed for ON24 | ~6:36 AM | 1 used (36→35) |

### Mar 3 Batch 8 Day 6 InMails (confirmed)
| # | Name | Company | Title | Subject | Time | Credits |
|---|------|---------|-------|---------|------|---------|
| 41 | Mohan Gummadi | Verisk | Senior Director QA | Regression cycles at Verisk | ~6:39 AM | 1 used (35→34) |
| 42 | Samata Yarlagadda | Coupa | Sr. Director Quality Engineering | Test upkeep at scale | ~6:42 AM | 1 used (34→33) |
| 43 | Kartik Punekar | Vonage | Lead SDET | API regression at Vonage | ~6:45 AM | 1 used (33→32) |
| 44 | Amira Survil | TradeStation | Principal SDET | Test maintenance in fintech | ~6:49 AM | 1 used (32→31) |
| 45 | Deepa Krishnamoorthy | Nextiva | Lead SDET | VoIP platform regression | ~6:52 AM | 1 used (31→30) |
| 46 | Lakshmi Raghavan | Point | Senior SDET | — | SKIPPED | NOT FOUND on Sales Nav |
| 47 | Julia Mitchum | Blue Yonder | SR QA Architect | Supply chain platform testing | ~6:56 AM | 1 used (30→29) |
| 48 | Rick Kowaleski | Alteryx | Software Engineer | Regression cycles in analytics | ~7:00 AM | 1 used (29→28) |
| 49 | Ghada Harb | ELLKAY | QA Manager | Healthcare data testing | ~7:03 AM | Free (1st degree, 28) |
| 50 | Irina Shitova | STRATACACHE | Senior QA Engineer | Retail tech platform regression | ~7:07 AM | Free (Open Profile, 28) |

### Mar 1 Overflow InMails (confirmed)
Ron Trachman, Laurie Nielsen, Alan Gutherz, Derek Stanley, Nihal Elsayed, Sarah Kluivert, Kanda Kaliappan.

## Mar 4 Sales Nav Audit Findings
**Conducted:** Mar 4 via Sales Nav inbox inspection — **220 conversations loaded (full audit, Batches 1–9 era)**

### Issues Found — Initial Audit (140 conversations)
| Issue | Detail |
|-------|--------|
| Credit discrepancy | Tracker said 28, Sales Nav shows **23** — 5 credits unaccounted |
| Batch 9 partial sends | 6 names sent on Tue Mar 3 WITHOUT being logged: Mohan Guruswamy, Jeremy Cira, Chandana Ray, Lueanne Fitzhugh, Martha Horns, Kylie Summer |
| Batch 9 duplicates | Jennifer Tune, Bhavani Neerathilingam, Sandy Paray — all in Batch 7 (Feb 28) AND Batch 9. Do NOT send again. |
| DNC violation — Sanjay Singh | Sent in Batch 5B (Feb 27). On DNC list (hostile reply 2022 mabl era). |
| DNC violation — Lance Silverman | Sent in Batch 5B (Feb 27). On DNC list (polite decline). |
| Same-company: Saks Global | Sowmya Kandula AND Sandy Paray both messaged in Batch 7 on Feb 28. Two people, same company, same day. |
| Same-company: Greenway Health | Sam Townsend + Drew Davis (Batch 7, Feb 28) AND Martha Horns (Batch 9, sent Tue). Three people at same company. |
| Abe Blanco reply | Replied today (Mar 4) "not interested." Add to DNC. Batch 8 / Kapitus. |

### Additional Issues Found — Deep Audit (extended to 220 conversations)

**5 Confirmed Double-Sends (same person messaged twice across different batches):**

| Person | First Send | Second Send | Notes |
|--------|-----------|------------|-------|
| Chuck Smith | Batch 1 (Feb 23) | Batch 5B (Feb 27) | Batch 1 may have been connection msg not InMail — monitor for reaction |
| Abe Blanco | Batch 3 (Feb 26) | Batch 8 Day 2 (Mar 3) | Already on DNC (replied "not interested" Mar 4). Both sends happened. |
| Rick Kowaleski | Batch 3 (Feb 26) | Batch 8 Day 6 (Mar 3) | Two InMails sent — cannot unsend. If he replies, treat as Touch 1 reply. |
| Christie Howard | Batch 5B (Feb 27) | Batch 8 Day 4 (Mar 3) | Two InMails sent 4 days apart — cannot unsend. Monitor for reply. |
| Mohan Gummadi | Batch 5B (Feb 27) | Batch 8 Day 6 (Mar 3) | Two InMails sent 4 days apart — cannot unsend. Monitor for reply. |

**6th Double-Send discovered Mar 6 audit:**
| Person | First Send | Second Send | Notes |
|--------|-----------|------------|-------|
| Yassi Dastan | Batch 6 (Feb 28) | Batch 8 Day 5 (Mar 3) | Two InMails sent 3 days apart — cannot unsend. If she replies, treat as Touch 1 reply. Touch 2 due ~Mar 8→Mar 9. |

**Action:** All 6 already sent, nothing to unsend. For Touch 2 triage, treat these people as already having received Touch 1 + unofficial Touch 1.5 — skip to Touch 2 timeline as normal but note the prior duplicate send.

**Batch 6 File Label Issue (resolved):**
- File "outreach-batch6-unsent.html" is mislabeled. Batch was ACTUALLY SENT on Feb 28.
- 14+ names confirmed in Sales Nav inbox. Pipeline metrics already correctly count these 27 sends.
- File label is wrong but data is accurate. Do not re-send anyone from this file.

**Batch 1 (Feb 23) — CONFIRMED: Connection Requests, NOT InMails:**
- Verified Mar 4 via Sales Nav audit: zero Batch 1 names appear in Sales Nav inbox across 220 loaded conversations.
- These were sent as LinkedIn connection requests via regular LinkedIn, not Sales Nav InMail.
- No InMail credits consumed. No Sales Nav thread created.
- All 22 people enrolled in Apollo Q1 Priority Accounts sequence (done Mar 3).
- Touch 2 approach: email (Apollo sequence Step 3) or LinkedIn DM if they accepted the connection. Do NOT send InMail.

**Master Sent List:**
- `/Work/MASTER_SENT_LIST.csv` — deduplicated CSV of all 193 unique prospects contacted (198 records including 5 double-sends).
- Regenerate anytime: run `/sessions/practical-brave-goldberg/build_master_list.py`
- MUST be updated after every send session.

### Batch 9 True State (post-audit)
| Name | Status |
|------|--------|
| Mohan Guruswamy | ✅ SENT Mar 3 (untracked) |
| Jeremy Cira | ✅ SENT Mar 3 (untracked) |
| Chandana Ray | ✅ SENT Mar 3 (untracked) |
| Lueanne Fitzhugh | ✅ SENT Mar 3 (untracked) |
| Martha Horns | ✅ SENT Mar 3 (untracked) |
| Kylie Summer | ✅ SENT Mar 3 (untracked) |
| Jennifer Tune | ⛔ REMOVE — duplicate (Batch 7 Feb 28) |
| Bhavani Neerathilingam | ⛔ REMOVE — duplicate (Batch 7 Feb 28) |
| Sandy Paray | ⛔ REMOVE — duplicate (Batch 7 Feb 28) |
| David Gustafson | ✅ SENT Mar 4 (untracked — confirmed Mar 6 inbox sweep) |
| Yuliya A | ✅ SENT Mar 4 (untracked — confirmed Mar 6 inbox sweep) |
| Kanan Hasanzade | ✅ SENT Mar 4 (untracked — confirmed Mar 6 inbox sweep) |
| Jiaping Shen | ✅ SENT Mar 4 (untracked — confirmed Mar 6 inbox sweep) |
| Azam Quraishi | ✅ SENT Mar 4 (untracked — confirmed Mar 6 inbox sweep) |
| Sravanti Krothapalli | ✅ SENT Mar 4 (untracked — confirmed Mar 6 inbox sweep) |
| Cooper Morrow | ✅ SENT Mar 4 (untracked — confirmed Mar 6 inbox sweep) |
| Manigandan Kanagasabai | ✅ SENT Mar 4 (untracked — confirmed Mar 6 inbox sweep) |
| Denise Barnett | ✅ SENT Mar 4 (untracked — confirmed Mar 6 inbox sweep) |
| Leah Coates | ✅ SENT Mar 4 (untracked — confirmed Mar 6 inbox sweep) |
| Grant Anderson | ✅ SENT Mar 4 (untracked — confirmed Mar 6 inbox sweep) |
| Jyothi Kudithipudi | ⏳ PENDING (Rob decision Mar 6: skip for now) |
| Axel Kerksiek | ⏳ PENDING (Rob decision Mar 6: skip for now) |

**Remaining Batch 9 to send: 2 (Jyothi Kudithipudi, Axel Kerksiek)**
**Credits available: 4 (as of Mar 6 post-Batch 11)**

---

## Pipeline Metrics (Updated Mar 11)
| Metric | Value |
|--------|-------|
| Total InMails sent (LinkedIn) | 228 (198 tracked + 6 untracked B9 Mar 3 + 11 untracked B9 Mar 4 + 9 Batch 10 Mar 6 + 4 Batch 11 Mar 6) |
| Total Emails sent (all channels) | **~300+** — 74 confirmed pre-Mar10 + 23 Wave1 placeholder (INC-007) + 24 Wave1 recovery + 16 Wave2 + 33 Wave3 actual + 2 Wave3 recovery (INC-008) + 37 Wave4 = ~209 TAM Outbound sends. See Master Send Log for detail. |
| InMail credits remaining | **4** (last updated Mar 6 post-Batch 11) |
| MASTER_SENT_LIST.csv rows | **412** (updated Mar 11 — includes all TAM Outbound Wave 1-4 T1 rows) |
| TAM Outbound unique contacts T1 sent | **111** (Wave1: 23, Wave2: 16, Wave3: 35, Wave4: 37) |
| TAM Outbound pending T1 tasks | **9** (Wave4: Irina Baxter, Jiadong Shen, Simon Crawford, Adit Shah, Mohan Raj, Shilendra Sharma, Poonam Patil, Divya Sathish, + Christine Gamache/Brooks Foley Wave3 future-dated) |
| Apollo Q1 Priority Accounts | **316 enrolled** (315 pre-Mar7 + 1 Mar 7 Gil Taub add) |
| Apollo TAM Outbound - Rob Gorham | ~120+ enrolled (Wave 1-4 combined) |
| Apollo Q1 Website Visitor | 78 active / 81 delivered (⚠️ Previously showed "9 active" — INCORRECT. Reconciliation pending.) |
| Legacy batch prospects (InMail/LI) contacted | **206** (202 pre-Batch11 + 4 Batch 11 Mar 6) |
| Blocked (Terene Lee) | 1 |
| DNC | 7 (Sanjay Singh, Lance Silverman, Clyde Faulkner, Ashok Prasad, Abe Blanco, Chuck Smith, Jitesh Biswal) |
| Double-sends (cannot unsend) | 6: Chuck Smith, Abe Blanco, Rick Kowaleski, Christie Howard, Mohan Gummadi, Yassi Dastan |
| TAM Outbound bounces | **12 total:** Wave1: Sucheth Ramgiri (SMTP 550), Arun Amarendran (postmaster bounce, manually stopped Mar 12). Wave4: Ksenia Shchelkonogova (email invalid) + 9 new Mar 12: Jessica Harris (OneMain), William Xie (EA), David Schraff (Cleveland Clinic), Mike Seal (DraftKings), Koushal Ram (Mastercard), Sakib Alam (Humana), Samatha Gangyshetty (Humana), Ahmet Cakar (Humana). See INC-011. |
| Wave T2 schedule | Wave1: Mar 15. Wave2: Mar 15. Wave3: Mar 16. Wave4: Mar 19. |

### Enrollment Audit (Mar 3)
Audited all batches for unenrolled prospects. Enrolled 41 missing contacts:
- **Batch 1**: 22 contacts enrolled (were never added to sequence after InMail sends)
- **Batch 8**: 19 contacts enrolled (created during batch but not yet enrolled)
- All contacts passed checks: no DNC matches, no deletion reasons, no cadence conflicts
- Override flags used: active_in_other_campaigns, no_email, job_change, without_ownership_permission, finished_in_other_campaigns, unverified_email
- Kenny Liu enrolled despite prior "bounced" status in another sequence

## Follow-Up Schedule (from Touch 1 send dates)
| Batch | Touch 1 Sent | Touch 2 Send | Touch 3 Send |
|------|-------------|-------------|-------------|
| Batch 3 (24) | Feb 25-26 | Mar 2-3 (Mon-Tue) | Mar 7-8 |
| Batch 5B (23) | Feb 27 | Mar 4 (Wed) | Mar 9 |
| Batch 5A (25) | Feb 27-28 | Mar 4-5 (Wed-Thu) | Mar 9-10 |
| Batch 6 (27) | Feb 28 | Mar 5 (Thu) | Mar 10 |
| Batch 7 (41) | Feb 28 | Mar 5 (Thu) | Mar 10 |
| Mar 1 overflow (7) | Mar 1 | Mar 6 (Fri) | Mar 11 |
| Buyer Intent (9) | Feb 27 | Mar 4 (Wed) | Mar 9 |
| Batch 8 Day 1 (7 sent) | Mar 2 | Mar 7 (Sat→Mar 9 Mon) | Mar 12 |
| Batch 8 Day 2 (6 sent) | Mar 3 | Mar 8 (Sun→Mar 9 Mon) | Mar 13 |
| Batch 8 Day 3 (6 sent) | Mar 3 | Mar 8 (Sun→Mar 9 Mon) | Mar 13 |
| Batch 8 Day 4 (8 sent) | Mar 3 | Mar 8 (Sun→Mar 9 Mon) | Mar 13 |
| Batch 8 Day 5 (8 sent) | Mar 3 | Mar 8 (Sun→Mar 9 Mon) | Mar 13 |
| Batch 8 Day 6 (8 sent) | Mar 3 | Mar 8 (Sun→Mar 9 Mon) | Mar 13 |

| Batch 9 — 6 sent Mar 3 (untracked) | Mar 3 | Mar 8 (Sun→Mar 9 Mon) | Mar 13 |
| Batch 9 — 11 sent Mar 4 (untracked) | Mar 4 | Mar 9 (Mon) | Mar 14 (Sat→Mar 16) |
| Batch 10 — 9 sent Mar 6 (3 free + 6 credit) | Mar 6 | Mar 11 (Touch 2) | Mar 16 (Touch 3) |
| Batch 10 — remaining 16 (Mon Mar 9 sends) | Mar 9 | Mar 14 (Touch 2) | Mar 19 (Touch 3) |
| Batch 11 — 4 sent Mar 6 (4 credit InMails) | Mar 6 | Mar 11 (Touch 2) | Mar 16 (Touch 3) |
| Pam Bice Touch 2 | OVERDUE (due Mar 4, now Mar 6) | Send ASAP | — |
| B9 T2 (16 sent Mar 9) | Mar 9 | — | Mar 14 (Touch 3) |
| B10 T2 (6 sent Mar 9) | Mar 9 | — | Mar 14 (Touch 3) |
| B11 T2 (3 sent Mar 9) | Mar 9 | — | Mar 14 (Touch 3) |

**INC-002 double-send special cases:**
- Abe Blanco (Kapitus): DNC. Skip all touches permanently.
- Rick Kowaleski (Alteryx): Received Batch 3 InMail (Feb 26) + Batch 8 InMail (Mar 3). Touch 2 due ~Mar 8. Treat normally — note the extra prior touch, keep message fresh.
- Christie Howard (LastPass): Received Batch 5B InMail (Feb 27) + Batch 8 InMail (Mar 3). Touch 2 due ~Mar 8. Treat normally.
- Mohan Gummadi (Verisk): Received Batch 5B InMail (Feb 27) + Batch 8 InMail (Mar 3). Touch 2 due ~Mar 8. Treat normally.
- Chuck Smith: Batch 1 was a connection request (no InMail), Batch 5B was InMail (Feb 27). Touch 2 as normal Batch 5B prospect (~Mar 4).

**INC-001 special cases:**
- Irfan, Katie, Rachana, Giang: Touch 3 already sent (Feb 28). Skip official Touch 3. Touch 2 InMail still due.
- Pallavi: Replied. Rob sent follow-up Mar 2. Warm lead.
- Gunasekaran: Orphan. Needs tracker entry and Touch 2 research.

**Week of Mar 2-7 workload:**
- Mon Mar 2: ~24 Batch 3 Touch 2s eligible (avoid Monday sends, draft for Tue)
- Wed Mar 4: ~23 Batch 5B + 5 Batch 5A + 9 Buyer Intent follow-ups
- Thu Mar 5: ~88 prospects (5A remaining + Batch 6 + Batch 7) — PEAK DAY
- Fri Mar 6: 7 overflow Touch 2s
- **Total Touch 2 volume: ~142 InMails + 9 email follow-ups**
- Credits (67) insufficient for all 142. Triage: Hot/Warm first, email for rest.

## Batch Tracker Files
| File | Batch | Status |
|------|-------|--------|
| outreach-sent-feb13-batch1.html | Batch 1 | Complete |
| outreach-sent-feb13-batch1-v2.html | Batch 1 rebuild | Complete |
| outreach-batch2-unsent.html | Batch 2 | Complete (never sent) |
| outreach-sent-feb26-batch3.html | Batch 3 | Complete (24 sent) |
| outreach-sent-feb27-batch5a.html | Batch 5A | Active |
| outreach-sent-feb27-batch5b.html | Batch 5B | Active |
| outreach-batch6-unsent.html | Batch 6 | Complete (27 sent Feb 28) — ⚠️ FILENAME MISLEADING: was actually sent. Do not re-send. |
| batch7-send-tracker.json | Batch 7 | Complete (41 sent) |
| batch7-send-tracker.html | Batch 7 HTML | Complete |
| enriched-prospects-batch8.json | Batch 8 | Enrichment data |
| prospect-outreach-8-2026-03-02.html | Batch 8 | COMPLETE (43/50 sent, 2 SKIPPED disabled/already msg, 3 NOT FOUND, 2 FREE) |
| batch8_send_queue.txt | Batch 8 | Send queue (50 prospects, 8 daily) |
| prospect-outreach-9-2026-03-03.html | Batch 9 | ACTIVE — 22/24 sent (6 Mar 3 untracked + 11 Mar 4 untracked + 5 confirmed). 2 PENDING: Jyothi Kudithipudi, Axel Kerksiek. 3 REMOVED (duplicates). Touch 2 starts Mar 9. |
| outreach-batch10-draft-mar6.html | Batch 10 | DRAFT (source file — superseded by sent file below) |
| outreach-batch10-sent-mar6.html | Batch 10 | ACTIVE — 9 sent Mar 6 (3 free + 6 credit InMails). 16 pending (8 credit InMails Mon Mar 9: Sasa Lazarevic, Srikanth Sy, Sarah Ross, Niveditha Somasundaram, Stephen Burlingame, Dave Czoper, Crys Simonca, Christian Melville). 6 skipped no InMail access: Gil Taub ✅ ENROLLED Q1 LI Outbound Mar 7. Kristyn Burke, Tim Hartgrave, Vince Delfini, Padmanaban Vadivelu, Ravi Nag — enrollment NOT YET ATTEMPTED. Sasa Lazarevic + Christian Melville — enrollment BLOCKED (ownership permission), need UI enrollment. |
| outreach-batch11-draft-mar6.html | Batch 11 | ACTIVE — 4 sent Mar 6 (4 credit InMails): Brad Askins/Trimble, Dan Heintzelman/Prevail Legal, Georgii Petrosian/AuditBoard, Madhu Nedunuri/IDB Bank. All enrolled in LinkedIn Outbound - Q1 Priority Accounts. Touch 2 due Mar 11. |

## Mar 6 Q1 QA Outreach Migration

Q1 QA Outreach - US (ID: 699f4089628b940011da7fb7) fully resolved. 26 clean contacts moved to LinkedIn Outbound - Q1 Priority Accounts and enrolled. Sequence archived.

**Batch 10 — 5 Deferred (same-company conflicts):**
| Name | Company | Reason |
|------|---------|--------|
| Kendal Walton | Aspire Software | Same company as Sarah Ross (included, P3) |
| Charles Dudley | Simpro Software | Same company as Clint Parker (included, P2); also Apollo email mismatch |
| Lisa King | Vergent LMS | Same company as Jason Poole (included, P4); no Apollo match |
| Jerad Fuller | Ncontracts | Same company as Tom Goody (included, P4) |
| Terene Lee | Impartner Software | Same company as Josh Beach (included, P3); needs Touch 2 next batch |

**Batch 10 — 2 No-Apollo-Match flags (preflight results Mar 6):**
| Name | Company | Notes |
|------|---------|-------|
| Kristyn Burke | Kahuna | ✅ CLEAN — Module A2 composer check passed Mar 6 (blank new message). Recently promoted QA Lead → QA Manager. No Apollo match — verify email before send. |
| Guna Chandrasekaran | FloQast | ⚠️ UNVERIFIABLE — 0 results on Sales Nav (Mar 6). No Apollo match. SKIP InMail. Route to email only if Apollo email verified. |

---

### TAM Outbound Batch Files (added Mar 11)
| File | Wave | Status |
|------|------|--------|
| wave1-batch1-tracker-mar10.html | Wave 1 — 23 contacts (Cboe, Fidelity, Chase, Commvault, TruStage, YouTube) | ✅ All badges: T1 Sent Mar 10. T2 due Mar 15. |
| tamob-wave2-draft-mar10.html | Wave 2 — 16 contacts (GEICO, Checkr, EA, Cetera, OneMain, Mindbody, HashiCorp) | ✅ All badges: T1 Sent Mar 10. T2 due Mar 15. |
| tamob-batch-20260311-1.html | Wave 3 — 35 contacts (Yahoo, Veradigm, Charlie Health, TELUS, GE HealthCare, L3Harris, Georgia-Pacific) | ✅ 33 T1 Sent Mar 11. 2 future-dated. T2 due Mar 16. |
| tamob-batch-20260311-2.html | Wave 4 — 48 enrolled (E*TRADE, Broadcom, Humana, Corewell, BCBS, Mastercard, Anaplan, DraftKings, Cleveland Clinic, Microchip, GEICO, EA, HashiCorp, KKR, Datamatics, OneMain) | 37 T1SentMar11, 2 Blocked, 9 Ready (pending tasks). T2 due Mar 19. |

---

## Key Deliverables Index
| File | Purpose |
|------|---------|
| automation-plan-v1.html | BDR automation roadmap |
| bdr-automation-pipeline-sop-v2.docx | A-to-Z pipeline SOP |
| daily-prospecting-sop-v2.docx | Daily prospecting SOP (Phases 8-11) |
| email-sequence-sop.html | Interactive email SOP |
| TEMPLATE_LIBRARY.md | Master template library v2.0 |
| outreach-intelligence.html | 1,326 conversation analysis |
| message-analytics-dashboard.html | Performance metrics |
| testsigma-knowledge-bible.md | Product knowledge reference |
| intent-outreach-pipeline-2026-02-26.html | Intent pipeline command center |
| apollo-sequence-step-copy.md | Sequence copy guide |
