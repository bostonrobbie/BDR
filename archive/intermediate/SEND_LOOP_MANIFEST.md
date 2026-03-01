# Batch 5B Send Loop Data Extraction - Complete Summary

## Extraction Status: ✓ SUCCESS

**File Generated:** `/sessions/quirky-zen-planck/mnt/Work/send-loop-data-5b.json`  
**File Size:** 83 KB (84,655 bytes)  
**Generation Date:** 2026-02-27  
**Source File:** prospect-outreach-5b-2026-02-26.html  

---

## Metadata

| Field | Value |
|-------|-------|
| **Batch ID** | 5b |
| **Total Prospects** | 25 |
| **Generated Date** | 2026-02-26 |
| **Updated Date** | 2026-02-27 |
| **Sequence ID** | 69a05801fdd140001d3fc014 |
| **Sequence Name** | Q1 Priority Accounts |
| **Email Account** | robert.gorham@testsigma.net (68f65bdf998c4c0015f3446a) |

---

## Send Schedule Configuration

### Pacing Rules
- **Max per day:** 8 prospects
- **Max per week:** 20 prospects
- **Min gap between sends:** 3 minutes
- **Break after:** 10 sends
- **Break duration:** 10 minutes

### Preferred Timing
- **Send window:** 12:00-13:00 local time (lunch window, 56.5% reply rate)
- **Preferred days:** Thursday, Tuesday, Friday, Wednesday
- **Avoid:** Monday (22.9% reply rate vs 42.1% Thursday)

### Send Order (Priority-Sorted)
Ordered by: Priority (descending) → Persona (Architect > Director > Manager) → Name (alphabetical)

**Priority 5 (Hot - 1 prospect):**
1. Lyle Landry (QA Manager, Availity, Healthcare IT)

**Priority 4 (Warm - 10 prospects):**
2. Iftikhar Hussain (Architect, Sabre Corporation, Travel Tech)
3. Rahul Pandey (Architect, CareFirst BCBS, Health Insurance)
4. Christie Howard (Director, LastPass, Cybersecurity/SaaS)
5. Mohan Gummadi (Director, Verisk, Data Analytics/Insurance)
6. Sebren Green (Director, Riot Games, Gaming)
7. Konduru Srinivasulu (Manager, Kaleris, Healthcare)
8. Amanda Mao (Manager, Veeva Systems, Life Sciences SaaS)
9. Sanjay Singh (Manager, ServiceTitan, Field Service SaaS)
10. Rachael Schroeder (Manager, Epic Games, Gaming)
11. Anthony Kent (Manager, Apiture, FinTech)

**Priority 3 (Standard - 14 prospects):**
12. Edwin Gozun (Architect, Arm, Semiconductors)
13. Lance Silverman (Architect, Healthfirst, Healthcare)
14. Rich Kowalski (Architect, Genesys, Contact Center SaaS)
15. Chuck Smith (Director, Aventiv Technologies, GovTech/Corrections)
16. Ryan Aspleaf (Director, VIZIO, Consumer Electronics)
17. Arun Bhatia (Director, Aspen Technology, Industrial Software)
18-25. Managers at: Teradata, GoGuardian, Vertafore, Plume, Impartner Software, Legion Technologies, 10Pearls, Lucid Software

---

## Prospect Distribution

### By Priority
| Priority | Count | Focus |
|----------|-------|-------|
| **5 (Hot)** | 1 | Work first every morning. Call + InMail same day. |
| **4 (Warm)** | 10 | High priority. Start sequence within 24 hours. |
| **3 (Standard)** | 14 | Normal cadence. Start sequence within batch cycle. |

### By Persona
| Persona | Count | Reply Rate* |
|---------|-------|-------------|
| **Architects** | 5 | 39.3% |
| **Directors** | 6 | 26.0% |
| **Managers/Leads** | 14 | 26.8% |

*Based on historical mabl outreach data (1,326 conversations)

### By Vertical (24 Unique)
- **Gaming:** 2 (Epic Games, Riot Games)
- **Healthcare/HealthTech:** 4 (Availity, CareFirst BCBS, Healthfirst, Verisk)
- **Other unique verticals:** 19 (Financial, SaaS, InsurTech, Workforce, etc.)

### By A/B Test Group
| Group | Count | Variable |
|-------|-------|----------|
| **A** | 12 | Control (baseline messaging) |
| **B** | 13 | [Test variable TBD - tracked separately] |

---

## Data Quality Metrics

| Metric | Result |
|--------|--------|
| **All 25 prospects extracted** | ✓ 100% |
| **All have valid emails** | ✓ 25/25 |
| **All have Touch 1 messages** | ✓ 25/25 |
| **All have Touch 2 messages** | ✓ 25/25 |
| **All have Touch 3 messages** | ✓ 25/25 |
| **All have MQS scores** | ✓ 25/25 (avg: 10.2/12) |
| **All have Personalization scores** | ✓ 25/25 (avg: 2.8/3) |
| **All have predicted objections** | ✓ 25/25 |
| **All have objection responses** | ✓ 25/25 |

### Message Quality Distribution
- **MQS 11-12 (Excellent):** 16 prospects (64%)
- **MQS 9-10 (Good):** 9 prospects (36%)
- **Personalization 3 (Deep):** 21 prospects (84%)
- **Personalization 2 (Medium):** 4 prospects (16%)

---

## JSON Structure

Each prospect record contains:

```json
{
  "prospectId": 1,
  "name": "Lyle Landry",
  "title": "QA Manager @ Availity",
  "company": "Availity",
  "location": "Baton Rouge, LA",
  "email": "lyle.landry@availity.com",
  "linkedinUrl": "[URL if available]",
  "priority": 5,
  "abGroup": "a",
  "mqsScore": 11,
  "personalizationScore": 3,
  "vertical": "Healthcare IT",
  "persona": "Manager",
  "status": "not_started",
  "touch1": {
    "subject": "FHIR compliance deadline",
    "body": "[Full message text, HTML entities decoded]",
    "wordCount": 61
  },
  "touch2": {
    "subject": "[Subject]",
    "body": "[Full message text]",
    "wordCount": 50
  },
  "touch3": {
    "subject": "[Subject]",
    "body": "[Full message text]",
    "wordCount": 61
  },
  "predictedObjection": "Compliance requirements",
  "objectionResponse": "[Pre-loaded response]"
}
```

---

## 4-Touch Cadence (Intent Account Sequence)

Each prospect follows this sequence in the Q1 Priority Accounts Apollo sequence:

| Touch | Day | Channel | Priority | Duration |
|-------|-----|---------|----------|----------|
| **1** | Day 1 | LinkedIn InMail | High | 80-120 words |
| **2** | Day 5 | LinkedIn InMail (Follow-up) | High | 40-70 words |
| **3** | Day 10 | Email | Medium | 60-100 words |
| **4** | Day 15 | Phone Call | Medium | Discovery call |

---

## Usage Instructions for Rob

### 1. **Send Loop Execution**
Use this JSON with CoWork browser automation to execute sends:
- Load prospect data from `send-loop-data-5b.json`
- Sort by `sendSchedule.sendOrder` to determine execution sequence
- Follow LinkedIn Sales Navigator Live Send SOP
- Respect pacing rules: max 8 per day, 3-minute gap between sends, 10-minute break every 10 sends

### 2. **Approval Workflow**
Before sending each prospect:
1. Review the prospect card in the HTML tracker
2. Verify all 3 touches are ready (all have MQS ≥ 9/12)
3. Check objection prediction and pre-loaded response
4. Confirm priority level and send order
5. Respond "APPROVE SEND" for each prospect in chat

### 3. **Timing**
- **Send window:** 12:00-13:00 PM local time (best reply rate: 56.5%)
- **Days:** Thu, Tue, Fri, Wed preferred; avoid Monday
- **Batch pace:** Start with Priority 5 (Lyle Landry), then Priority 4, then Priority 3
- **Daily limit:** 8 max per day to avoid LinkedIn detection

### 4. **Post-Send Logging**
After each prospect is sent:
- Log timestamp and confirmation to cycle log
- Update status in HTML tracker to "Touch 1 Sent"
- Set "nextStepDue" to +5 days for Touch 2 follow-up
- Track InMail credits remaining

### 5. **Sequence Enrollment**
Once all messages are approved and ready to send:
- Enroll prospects in Apollo "Q1 Priority Accounts" sequence (ID: 69a05801fdd140001d3fc014)
- All steps are MANUAL - Rob executes each touch, no auto-sends
- Use email account: robert.gorham@testsigma.net (68f65bdf998c4c0015f3446a)

---

## Key Insights from Batch 5B

- **Hot prospect:** Lyle Landry @ Availity (Priority 5) - FHIR compliance deadline is the trigger
- **Strongest team:** 5 Architects + 6 Directors + 14 Managers = excellent persona mix
- **Best verticals:** Healthcare IT and InsurTech are well-represented (need compliance + scaling)
- **Message quality:** 64% of prospects have MQS 11-12 (excellent), 84% have deep personalization
- **Split test ready:** 12 in Group A (control), 13 in Group B for next A/B iteration

---

## Apollo Integration

- **Sequence ID:** 69a05801fdd140001d3fc014 (Q1 Priority Accounts)
- **Sequence type:** Intent-based, manual all-steps (no auto-sends)
- **Email account:** robert.gorham@testsigma.net (ID: 68f65bdf998c4c0015f3446a)
- **Max students per batch:** 25 prospects per cycle
- **Dedup lookback:** 6 months (check for other BDR activity before enrollment)

---

## Files in This Delivery

1. **send-loop-data-5b.json** - Structured prospect data (THIS FILE)
   - Contains all 25 prospects with 3 touches each
   - Ready for send loop automation
   - Includes pacing rules and schedule config

2. **prospect-outreach-5b-2026-02-26.html** - Human-readable tracker
   - Interactive cards for each prospect
   - Copy-paste-ready message buttons
   - Status dropdowns and reply tags
   - Objection handling cards

3. **SEND_LOOP_MANIFEST.md** - This document
   - Executive summary
   - Usage instructions
   - Quality metrics
   - Insights

---

**Ready to send:** 2026-02-27  
**Next review:** After 3+ replies to identify reply triggers  
**Estimated send duration:** 2-3 hours (25 prospects × 3-5 min per prospect + breaks)

