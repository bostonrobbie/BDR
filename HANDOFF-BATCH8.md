# Batch 8 Handoff — Session Continuation Instructions

**Created:** 2026-03-02
**Purpose:** Everything a new Claude session needs to pick up Batch 8 processing from where we left off.

---

## WHAT'S DONE

1. **Prospect sourcing & dedup:** 44 prospects sourced → dedup sweep → Rob approved 32, skipped 6, parked 6.
2. **Apollo contact creation:** All 32 proceeding prospects created as Apollo contacts.
3. **Apollo sequence enrollment:** All 32 enrolled in "Q1 Priority Accounts" sequence (ID: `69a05801fdd140001d3fc014`). 185 total active at Step 1.
4. **Company research:** 3-source research completed for all ~30 unique companies across 6 verticals. Research summaries below.
5. **Memory restructure:** CLAUDE.md trimmed to ~159 lines. 10 on-demand reference files live in `memory/` directory.
6. **Jake Durand (Phreesia) flagged:** Company uses mabl (direct competitor). Needs Rob's decision: skip or competitor-displacement angle.

---

## WHAT'S LEFT (in order)

### Step 1: Draft C2 Messages (Touch 1, 2, 3) for all 31 prospects
This is the BIG task. Each prospect needs:
- **Touch 1 (Day 1 InMail):** 80-120 words, full C2 5-element structure, exactly 2 question marks
- **Touch 2 (Day 5 InMail follow-up):** 40-70 words, new angle/proof point, lighter close
- **Touch 3 (Day 10 Email):** 60-100 words if email available, fresh approach, different proof point
  - 2 prospects have NO email (Animesh Roy/Majesco, Christopher Page/Everbridge) → Touch 3 not possible
  - 1 prospect has extrapolated email (Amrita Jha/Majesco) → flag as lower confidence

### Step 2: Run 14-Point QA Gate on Every Message
Check every drafted message against:
1. HC scan (all 10 Hard Constraints from data-rules.md)
2. MQS score computation (must be >= 9/12)
3. Word count: Touch 1 = 80-120w, Touch 2 = 40-70w, Touch 3 = 60-100w
4. Question count: exactly 2 for Touch 1
5. Structural dedup: no two messages structurally identical
6. Evidence check: every claim sourced
7. Angle rotation: different angle per touch
8. Phrase toxicity scan (no "flaky tests", "CI/CD", "low code", "I figure", etc.)
9. CTA validation: "what day works" + proof point tie
10. Hyphen audit: max 1 per message, compound words only
11. Paragraph spacing: 4+ breaks, max 3 sentences per paragraph
12. Close pattern rotation (5 patterns, rotated across batch)
13. Research depth: 3 sources present
14. No "I noticed/saw" anywhere

### Step 3: Build Batch 8 HTML Tracker
Single HTML file: `prospect-outreach-batch8-20260302.html`
Must include:
- Prospect tracker table (sorted by priority score)
- Individual prospect cards with copy-paste messages for all touches
- "Copy Message" and "Copy Subject" buttons
- Predicted objection + pre-loaded response
- Status dropdowns, reply tags
- A/B group assignments
- Personalization scores (1-3) and MQS scores
- Priority scores (1-5) with color-coded badges
- Priority filter
- touch1_sent_date, touch2_eligible_date (+4d), touch3_eligible_date (+9d) fields
- cadence_status field (ON_TRACK/AHEAD/BEHIND/COMPLETE)

### Step 4: Present Final Report to Rob
Summary covering:
- Batch composition (31 active, 1 flagged competitor, 6 parked)
- Research highlights by vertical
- Message quality stats (avg MQS, pass/fail counts)
- Enrollment confirmation
- Flags for Rob's decision (Jake Durand, 2 no-email prospects, 1 extrapolated email)
- Parked prospects awaiting decision

---

## CRITICAL FILES TO READ BEFORE STARTING

**Always read these memory files first. Do NOT rely on cached knowledge.**

| File | Path | What It Contains |
|------|------|-----------------|
| CLAUDE.md | `/mnt/Work/CLAUDE.md` | Identity, hard rules, preferences, DNC list, tool stack |
| Outreach SOP | `/mnt/Work/memory/sop-outreach.md` | C2 message structure, writing rules, pre-draft steps, 3-touch sequence |
| Data Rules | `/mnt/Work/memory/data-rules.md` | HC constraints, SP preferences, timing, word count, toxic/positive patterns, MQS, QA Gate |
| Proof Points | `/mnt/Work/memory/proof-points.md` | Customer proof points, rotation logic, objection mapping, competitor reference |
| Incidents | `/mnt/Work/memory/incidents.md` | Draft safety rules, cadence enforcement, INC-001 details |
| Scoring | `/mnt/Work/memory/scoring-feedback.md` | Priority scoring (1-5), A/B testing, MQS rubric, reply tagging |
| Pipeline State | `/mnt/Work/memory/pipeline-state.md` | Send log, batch index, follow-up schedule |
| Enriched Prospects | `/mnt/Work/enriched-prospects-batch8.json` | All 44 prospects with Apollo enrichment data |

---

## PROSPECT GROUPS FOR DRAFTING

Organize drafting into 6 groups (can be parallelized with Task agents):

### Group 1: Insurance (6 prospects)
| Name | Title | Company | Email Status |
|------|-------|---------|-------------|
| Kerri McGee | Director of QA | Sapiens | verified |
| Olivia Pereiraclarke | QA Manager | Sapiens | verified |
| Vinayak Singh | Director of QA | PURE Insurance | verified |
| Morya Moyal | QA Manager | Hippo Insurance | verified |
| Stephen Starnaud | QA Manager | biBerk Business Insurance | verified |
| Jamie Kurt | QA Manager | Vertafore | verified |

**Research findings:**
- **Sapiens:** Major mainframe-to-Azure cloud migration underway. 4,900 employees. Insurance software. Migration = massive test regression surface. Use maintenance angle (Hansard).
- **PURE Insurance:** Multi-platform (web + mobile + agent portal). 1,200 employees. High-value personal lines. Use scale/coverage angle (Medibuddy).
- **Hippo Insurance:** 3+ QA roles hiring, SwingDev acquisition integration. 480 employees. Use velocity angle (CRED).
- **biBerk:** Berkshire Hathaway subsidiary. Regulatory compliance (workers comp, liability). 630 employees. Use maintenance angle (Hansard) + compliance.
- **Vertafore:** AI/ML expansion in insurtech. 2,500 employees. Use velocity angle (Sanofi).

### Group 2: Healthcare IT (6 prospects)
| Name | Title | Company | Email Status |
|------|-------|---------|-------------|
| Christopher Brown | Director of QA | Simplify Healthcare | verified |
| Priya Khemani | Director of QA | GetInsured | verified |
| Rashad Fambro | Director, QA | MedeAnalytics | verified |
| Shivaleela Devarangadi | Head of Quality Engineering | RxSense | verified |
| Jim Lenihan | QA Manager | Waystar | verified |
| Lyle Landry | QA Manager | Availity | verified |

**Research findings:**
- **Simplify Healthcare:** 5 products (MemberHub, ProviderHub, etc.), recent AI feature launches. 910 employees. Use scale/coverage angle (Medibuddy).
- **GetInsured:** Powers 10 state health insurance exchanges. 650 employees. Enrollment periods = massive testing surges. Use velocity angle (Sanofi).
- **MedeAnalytics:** 300+ pre-built healthcare reports. 430 employees. Use scale/coverage angle (Nagra DTV).
- **RxSense:** QA hiring signals, pharmacy benefits platform. 300 employees. Use velocity angle (CRED).
- **Waystar:** 5 billion transactions/year. 1,500 employees. Transaction volume = test coverage pressure. Use maintenance angle (Hansard).
- **Availity:** 13 billion transactions/year, multiple QA roles hiring. 1,600 employees. Use maintenance angle (90% reduction).

### Group 3: Health/Edu/Other (6 prospects)
| Name | Title | Company | Email Status |
|------|-------|---------|-------------|
| Sonya Laplante | QA Manager | Claritev | verified |
| Joseph Lee | QA Manager | Hinge Health | verified |
| Courtney Corbin | QA Manager | Vizient, Inc | verified |
| Nabil Ahmed | Senior SDET | Progyny, Inc. | verified |
| Sneha Bairappa | Sr SDET | AAMC | verified |
| Christopher Page | Sr Software Quality Engineer | Everbridge | **NO EMAIL** |

**Research findings:**
- **Claritev:** Oracle Cloud + Azure migration. 2,700 employees. Healthcare cost management. Migration = regression spike. Use maintenance angle (Hansard).
- **Hinge Health:** QA hiring, FDA-regulated digital therapeutics, mobile + web. 1,600 employees. Use compliance angle (Sanofi).
- **Vizient:** GenAI platform launch ("Vizient Iris"). 4,000 employees. AI rollout needs test coverage. Use velocity angle (CRED).
- **Progyny:** AI investment in fertility benefits platform. 680 employees. Healthcare compliance. Use scale/coverage angle (Medibuddy).
- **AAMC:** Cloud migration, medical education platform. 1,400 employees. Use maintenance angle (Hansard).
- **Everbridge:** 99.99% SLA, critical communications. 1,600 employees. NO EMAIL, so Touch 1 + 2 only. Use maintenance angle (90% reduction).

### Group 4: FinServ/Construction/Media (6 prospects)
| Name | Title | Company | Email Status |
|------|-------|---------|-------------|
| Konstantin Diachenko | QA Manager | Paymentus | verified |
| Keith Schofield | QA Manager | Fullsteam | verified |
| Emre Ozdemir | Associate Principal, SDET | OCC | verified |
| Amir Aly | Director, QA Engineering | Procore Technologies | verified |
| Jason Schwichtenberg | QA Manager / Sr QA Lead | WebMD | verified |
| Kyung Kim | Director QA | WebMD | verified |

**Research findings:**
- **Paymentus:** PCI Level 1 compliance, 2,000+ biller clients. 1,400 employees. Use compliance + maintenance angle (Hansard).
- **Fullsteam:** 50+ M&A integrations, rapid portfolio consolidation. 1,700 employees. Post-acquisition testing pressure. Use scale/coverage angle (Medibuddy).
- **OCC:** ENCORE→Ovation platform migration. 2,600 employees. Financial clearing house, regulatory. Use maintenance angle (Hansard).
- **Procore:** 250+ integrations, construction management SaaS. 4,300 employees. Integration complexity. Use scale/coverage angle (Nagra DTV).
- **WebMD:** 2,000+ integrations, health content platform. 3,100 employees. Two prospects at same company, use different angles. Jason: velocity (CRED). Kyung: scale/coverage (Medibuddy).

### Group 5: Auto/InsurTech (7 prospects)
| Name | Title | Company | Email Status |
|------|-------|---------|-------------|
| Larry Sutton | QA Manager | Solera | verified |
| Geoffrey Juma | Software QA Engineering Manager | Solera | verified |
| Avijit Sur | Sr. Director, Quality/Performance/Risk | Solera | verified |
| Brian Liu | Sr SDET | CCC Intelligent Solutions | verified |
| Rian Musial | Lead SDET | CCC Intelligent Solutions | verified |
| Amrita Jha | QA Lead | Majesco | **EXTRAPOLATED email** |
| Animesh Roy | Software Test Architect | Majesco | **NO EMAIL** |

**Research findings:**
- **Solera:** ML/computer vision for auto claims, 4,000 employees. 3 prospects at same company, MUST use different angles. Larry: maintenance (Hansard). Geoffrey: velocity (CRED). Avijit (Sr. Director): productivity (Fortune 100).
- **CCC Intelligent Solutions:** Oracle→PostgreSQL migration. 2,400 employees. 2 prospects. Brian: maintenance (Hansard, migration angle). Rian: velocity (CRED).
- **Majesco:** 120+ insurance carriers on platform. 2,500 employees. Amrita: scale/coverage (Medibuddy). Flag extrapolated email. Animesh: NO EMAIL, Touch 1 + 2 only. Use maintenance (90% reduction).

### Group 6: Tech/Security (6 prospects)
| Name | Title | Company | Email Status |
|------|-------|---------|-------------|
| William Busch | QA Manager | Zynga | verified |
| Raye Rivera | QA Manager | VIAVI Solutions | verified |
| Balwinder Singh | Staff QA Engineer | iManage | verified |
| Jeremy Haage | Senior SDET | Virtru | verified |
| Shobha Gunupuru | Senior SDET | CyberArk | verified |
| Mikhail Nekhaenok | Senior SDET | Together AI | verified |

**Research findings:**
- **Zynga:** QA hiring, mobile gaming (frequent releases). 3,000 employees. Use velocity angle (CRED).
- **VIAVI Solutions:** Protocol testing, telecom. 3,600 employees. Use maintenance angle (Hansard).
- **iManage:** 200+ integrations, legal document management. 1,300 employees. Use scale/coverage angle (Nagra DTV).
- **Together AI:** Rapid AI releases, fast-growing startup. 360 employees. Use velocity angle (Sanofi).
- **Virtru:** FedRAMP compliance, data encryption. 230 employees. Use compliance + maintenance angle (Hansard).
- **CyberArk:** Quarterly releases, privileged access security. 3,800 employees. Use maintenance angle (90% reduction).

---

## SAME-COMPANY RULES

Multiple prospects at same company MUST get different angles and different proof points:

| Company | Prospects | Angle Assignment |
|---------|-----------|-----------------|
| Sapiens | Kerri McGee, Olivia Pereiraclarke | Kerri: maintenance/Hansard. Olivia: velocity/CRED |
| WebMD | Jason Schwichtenberg, Kyung Kim | Jason: velocity/CRED. Kyung: scale/Medibuddy |
| Solera | Larry Sutton, Geoffrey Juma, Avijit Sur | Larry: maintenance/Hansard. Geoffrey: velocity/CRED. Avijit: productivity/Fortune 100 |
| CCC | Brian Liu, Rian Musial | Brian: maintenance/Hansard (migration). Rian: velocity/CRED |
| Majesco | Amrita Jha, Animesh Roy | Amrita: scale/Medibuddy. Animesh: maintenance/90% reduction |

---

## CLOSE PATTERN ROTATION

5 patterns, rotate across the batch so no more than ~7 prospects share the same close pattern:

1. "If [outcome] would help [their situation], what day works for a quick look at how they did it?"
2. "What day works to see how [customer] [achieved outcome] while [solving their problem]?"
3. "If [outcome] before [their event/deadline] sounds useful, what day works for a quick look?"
4. "What day works to compare how [customer] [achieved outcome] without [their constraint]?"
5. "If getting [specific number] back in your [their process] would help, what day works for a quick chat?"

---

## EXCLUDED PROSPECTS (do NOT draft for these)

### Parked (6) — awaiting Rob's decision
| Name | Company | Reason |
|------|---------|--------|
| Niraj Pandey | TraceLink | Parked during dedup |
| Meraj Mohammed | BlackLine | Parked during dedup |
| Rick Jasper | Infoblox | Parked during dedup |
| Christina Fullbright | Eptura | Parked during dedup |
| Mihir Kumar | Netskope | Parked during dedup |
| Jared McHaffie | Realtor.com | Parked during dedup |

### Flagged (1)
| Name | Company | Reason |
|------|---------|--------|
| Jake Durand | Phreesia | Uses mabl (direct competitor). Needs Rob's decision. |

### Skipped (6) — removed during initial screening
These were Rob's skip decisions during prospect review. Do not include.

---

## C2 MESSAGE TEMPLATE REFERENCE

### Touch 1 (InMail, Day 1)
```
Subject: [3-6 words, domain or QA-situation reference]

[Opener: 1-2 lines. QA situation question. NOT company facts.]

[Context: 1-2 lines. Why this matters. No filler.]

[Proof point: 1 line. ONE customer example with real numbers. Mention Testsigma once.]

[Close: 1-2 lines. Reference proof point outcome + "what day works" ask.]
```
- 80-120 words (target 80-99 sweet spot)
- Exactly 2 question marks
- Max 1 hyphen (compound words only)
- NO em dashes
- 4+ paragraph breaks
- NO "I noticed/saw", NO "reaching out", NO bullets, NO feature dumps

### Touch 2 (InMail Follow-up, Day 5)
```
Subject: Re: [Touch 1 subject] or [new 3-6 word subject]

[Short follow-up, different angle/proof point]

[Lighter close with "what day works"]
```
- 40-70 words
- Different proof point than Touch 1
- Doesn't need full 5-element structure

### Touch 3 (Email, Day 10)
```
Subject: [5-8 words, fresh angle]

[Fresh approach, third proof point]

[Close with "what day works"]
```
- 60-100 words
- Different proof point than Touch 1 AND Touch 2
- Only if verified/extrapolated email available

---

## PRIORITY SCORING FORMULA

Score each prospect 1-5:
- Buyer Intent signal: +2
- QA-titled leader (Manager/Director/Head): +1
- Top vertical (SaaS, FinTech, Healthcare, Retail, Telecom, Pharma): +1
- Recently hired (<6 months): +1
- Active transformation (migration, M&A, platform change): +1
- Competitor tool detected: +1
- VP at 50K+ company with no QA scope: -1

Base score = 1. Add factors. Cap at 5.

---

## A/B TESTING

Current highest priority test: **Email subject line — SMYKM ("Something you might know us for") vs Standard**
- Apply to Touch 3 emails only
- Split 50/50 within the batch
- One variable per batch

---

## HOW TO EXECUTE

### Recommended approach: Parallel Task agents
Launch 6 Task agents (one per group) with:
1. The prospect data for that group (from enriched-prospects-batch8.json)
2. The company research findings (from this document)
3. The full C2 rules (from sop-outreach.md, data-rules.md, proof-points.md)
4. Instructions to produce Touch 1 + Touch 2 + Touch 3 (if email available) for each prospect
5. MQS self-scoring for each message
6. Pre-Draft Steps 1-4 completed for each

### After drafting:
1. Collect all outputs
2. Run the 14-point QA Gate across all messages
3. Fix any failures (rewrite if MQS < 9)
4. Assign close pattern rotation across full batch
5. Assign A/B groups for Touch 3 emails
6. Build the HTML tracker file
7. Present final report to Rob

### Draft safety reminders:
- Do NOT create Gmail drafts. All messages go in the HTML tracker for Rob to copy/paste.
- Touch 2 drafts: NOT before Day 4 of sequence
- Touch 3 drafts: NOT before Day 9 of sequence
- Every prospect MUST exist in tracker BEFORE any draft
- All drafts must use C2 structure and pass QA Gate (MQS >= 9/12)

---

## HARD RULES (from CLAUDE.md — NEVER violate)

1. **Chrome:** Always use blue/work Chrome browser.
2. **Coworker visibility:** NEVER take any action visible to Rob's coworkers. No Slack.
3. **Data protection:** NEVER modify/delete existing company data without per-item approval.
4. **Send approval:** NEVER send outreach without Rob's explicit "APPROVE SEND."
5. **Draft safety:** Follow all cadence enforcement rules from incidents.md.
6. **Gmail:** ALWAYS send from robert.gorham@testsigma.com, NEVER rgorham369@gmail.com.
7. **DNC List:** Do NOT contact Sanjay Singh (ServiceTitan) or Lance Silverman (Batch 5B, 60-day cool-off until ~May 1).

---

## PROMPT FOR NEW SESSION

Copy/paste this to kick off the work:

```
Read CLAUDE.md, then read the handoff file at /mnt/Work/HANDOFF-BATCH8.md.

Your task: Complete Batch 8 message drafting and QA for 31 prospects. Everything you need is in the handoff file, including prospect groups, company research, C2 rules, and the exact steps to follow.

Before drafting, read these memory files: memory/sop-outreach.md, memory/data-rules.md, memory/proof-points.md, memory/incidents.md, memory/scoring-feedback.md.

Then read enriched-prospects-batch8.json for all prospect data.

Draft Touch 1, Touch 2, and Touch 3 (where email exists) for all 31 prospects following C2 structure. Run the 14-point QA gate on every message. Build the HTML tracker. Present a final report.

Use parallel Task agents (6 groups defined in the handoff) to draft efficiently. Do not ask questions, just execute.
```
