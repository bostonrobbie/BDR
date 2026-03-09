# Salesforce Dashboards & Reports — Rob Gorham

*Catalogued Mar 9, 2026 — Cowork-8*

---

## Home Page Live Widgets (SF Home → https://d2v000000sgbdea0.lightning.force.com/lightning/page/home)

These charts render automatically on the SF Sales home page. Each has a "View Report" link.

| Widget | What It Shows | Notes |
|--------|--------------|-------|
| **Open Leads** | Bar chart by Lead Status (New, Attempted to Contact, Connected) | ~100+ leads total |
| **Open Contacts** | Bar chart by Contact Status (New ~850, Attempted to Contact ~700, Connected ~75) | 1,200+ contacts total |
| **My Accounts (Non Customers) - All Time** | Donut by Business Type — **314 prospect accounts** | SMB: 41, Commercial: 47, Mid Market: 221, Enterprise: ~5 |
| **My Customer Accounts** | Donut by Business Type — **10 farming accounts** | Enterprise: 8, Mid Market: 1, Commercial: 1 |
| **Factors Identified Accounts** | Bar chart by Engagement Level | HOT ~38, Cool ~10, Ice ~8, Warm ~8 |
| **Accounts w/o Recent Activity** | Donut — **506 accounts** | Ice: 204, Hot: 71, Cool: 24, Warm: 28, Unknown: 179 |
| **BD SAL This Month** | Count of SALs created this month | Currently **0** — no SALs yet Mar 2026 |
| **Disco Calls Completed - This Month** | Count of discovery calls | Ties to Activity tracking |
| **Demo Completed this month** | Count of demos | Pipeline health indicator |
| **Demo Completed but not Qualified** | Count | Tracks conversion gap |

---

## Key Reports (Rob's Recently Used)

| Report Name | Folder | URL / ID | Notes |
|-------------|--------|----------|-------|
| **Untapped Factors Accounts** | Sales Strategy Reports | [View](https://d2v000000sgbdea0.lightning.force.com/lightning/r/Report/00OOX00000HOtHh2AL/view) | Rob's 38 HOT Factor accounts — use this constantly |
| **Active Customers** | Public Reports | [View](https://d2v000000sgbdea0.lightning.force.com/lightning/r/Report/00OOX000009bkmt2AA/view) | Rob's 10 farming accounts |
| **Robert - TAM Accounts - OCT 2025** | Public Reports | [View](https://d2v000000sgbdea0.lightning.force.com/lightning/r/Report/00OOX00000H3IwL2AV/view) | Primary named account list |
| **TAM Contacts (enriched)** | Public Reports | [View](https://d2v000000sgbdea0.lightning.force.com/lightning/r/Report/00OOX00000H8ucj2AB/view) | ICP contacts enriched by LDR team |
| **Manual Testers TAM** | Public Reports | [View](https://d2v000000sgbdea0.lightning.force.com/lightning/r/Report/00OOX00000HGoa92AD/view) | Supplemental TAM list |
| **My Accounts (Non Customers) - All Time** | Public Reports | (Home Page widget) | All 314 prospect accounts |
| **RH Intro Calls - This Month** | Home Page Reports | (Home Page widget) | Rob's outbound intro call activity |
| **Open Leads** | Home Page Reports | (Home Page widget) | Pipeline of open leads |
| **Open Contacts** | Home Page Reports | (Home Page widget) | All contacts Rob owns |
| **Accounts w/o Recent Activity** | LDR Home Page | (Home Page widget) | Flag stale accounts |
| **BD SAL This Month** | Home Page Reports | (Home Page widget) | SALs created this month |
| **BD Leads Created - This Month** | Public Reports | — | New leads created by Rob |
| **Disco Calls Completed - This Month** | Accounts Reports | — | Discovery call tally |
| **Demo Completed this month** | Home Page Reports | — | Demo pipeline check |
| **Active Deals** | Home Page Reports | — | Open pipeline |
| **BD Owned Park Opportunities** | Home Page Reports | — | Parked/stalled deals |
| **Factors New Accounts - BDRs** | SDR Board | — | New accounts added to Factor list for BDRs |
| **Lead Reconversion Flag Report** | Public Reports | — | Flags leads for re-engagement |
| **Raview - All disco calls booked** | Daily standup leads review dashboard | — | All disco calls booked |
| **Opps with IB/OB - Current FQ** | Reports | — | Inbound vs. outbound opps this FQ |

---

## Key Dashboards — BDR Relevant (97 total in org)

97 dashboards exist in the org. The ones most relevant to Rob as a BDR:

### Tier 1 — Use Regularly

| Dashboard | Folder | URL | Notes |
|-----------|--------|-----|-------|
| **BDR: Daily standup review** | Sales Operations - Active | [View](https://d2v000000sgbdea0.lightning.force.com/lightning/r/Dashboard/01ZOX000000XJVJ2A4/view) | Rob's primary daily check — outbound activity, leads, contacts |
| **BDR: Outbound Dashboard** | Sales Operations - Active | [View](https://d2v000000sgbdea0.lightning.force.com/lightning/r/Dashboard/01ZOX000000y7cv2AA/view) | Outbound pipeline tracking |
| **BDR: Inbound Dashboard** | Sales Operations - Active | — (inactive creator) | Inbound leads view |
| **Opportunities: funnel view by BD** | Sales Operations - Active | — | Rob's pipeline funnel by BDR |

### Tier 2 — Useful Context

| Dashboard | Folder | Notes |
|-----------|--------|-------|
| **BDR Dashboard** | Private to Ops | General BDR attainment (may not be visible to Rob) |
| **BDR Manager - Home Page** | Sales Ops - Mithun | Mithun's manager view — know what he sees |
| **Mithun BD Dashboard Q4 (OctNovDec24)** | Public Dashboards | BD attainment by quarter — manager's scorecard |
| **JAN 25 - TAM Impact Dashboard** | Sales Ops - Mithun | TAM activity and impact |
| **Factors - Entire Funnel - Since April25** | Marketing Update (Factors) | Factor accounts full funnel view |
| **Factors Contacts - From Jan 2025** | Only LDR Team | Factor contacts pipeline |
| **Factors Leads Created** | BDs Outbound Leads | Leads generated from Factor accounts |
| **Factors - SQL/SAL/Closed Won** | Only LDR Team | Factor account conversion rates |
| **Sales Forecasting Dashboard - FY25** | LDR Dashboards | Weekly review, forecast |
| **Sales Pipeline Analysis** | Sales Operations - Active | Pipeline health |
| **Salesforce Opportunities: Review Dashboard** | Sales Operations - Active | Opportunity review |

### Tier 3 — FYI / Not Rob's Primary Focus

| Dashboard | Notes |
|-----------|-------|
| AE - HomePage / AE Manager - Home Page | AE view — useful for context on AE partners |
| KR Marketing Dashboard - Full Funnel | CEO-level marketing funnel |
| ABM Dashboard | Account-Based Marketing |
| Einstein Lead Scoring Dashboard | Lead scoring model |
| Gong competitive analysis / pipeline analysis | Gong-based insights |
| Aircall Metrics Dashboard V2 | Call metrics |

---

## Dashboard Folders (Org Structure)

| Folder | What's In It |
|--------|-------------|
| **Sales Operations - Active** | All active BDR/AE operational dashboards — most relevant |
| **Sales Ops - Mithun** | Mithun's manager-level dashboards |
| **LDR Dashboards** | LDR team views (pipeline funnel, forecasting) |
| **Only LDR Team** | LDR-restricted views (Factor account funnel) |
| **Public Dashboards** | Broadly shared across Testsigma |
| **Home Page Reports** | Feeds home page widgets |
| **BDs Outbound Leads** | Outbound-specific |
| **Private to Ops** | Ops-only (may not be viewable by Rob) |
| **Default Dashboards** | Salesforce defaults (Sales Pipeline, Service Performance) |
| **Gong Dashboards** | Gong conversation analytics |

---

## Quick-Access Links

| Purpose | Link |
|---------|------|
| SF Home (live widgets) | https://d2v000000sgbdea0.lightning.force.com/lightning/page/home |
| All Reports | https://d2v000000sgbdea0.lightning.force.com/lightning/o/Report/home?queryScope=everything |
| All Dashboards | https://d2v000000sgbdea0.lightning.force.com/lightning/o/Dashboard/home?queryScope=everything |
| BDR: Daily standup review | https://d2v000000sgbdea0.lightning.force.com/lightning/r/Dashboard/01ZOX000000XJVJ2A4/view |
| BDR: Outbound Dashboard | https://d2v000000sgbdea0.lightning.force.com/lightning/r/Dashboard/01ZOX000000y7cv2AA/view |
| HOT Factors Report | https://d2v000000sgbdea0.lightning.force.com/lightning/r/Report/00OOX00000HOtHh2AL/view |
| Active Customer Report | https://d2v000000sgbdea0.lightning.force.com/lightning/r/Report/00OOX000009bkmt2AA/view |
| TAM Account List | https://d2v000000sgbdea0.lightning.force.com/lightning/r/Report/00OOX00000H3IwL2AV/view |
