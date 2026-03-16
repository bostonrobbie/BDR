# T1 Optimization Report — March 16, 2026

**Data Quality:** 35 / 610 sends matched to batch drafts (5%)  
**Analysis Window:** Feb 23 - Mar 15, 2026  
**Report Date:** 2026-03-16 08:00:46

---

## 🟢 HIGH CONFIDENCE: Actions to Take Now

### 1. Bounce Domain Blacklist
- **Data:** 10 hard bounces across 15 domains
- **Top offender:** ea.com (6 bounces)
- **Action:** Add ea.com to pre-enrollment verification blacklist
- **Impact:** Prevent wasted credits on known bad addresses

### 2. Channel Mix Verification  
- **Current:** Email 350 (57%), LinkedIn 259 (42%)
- **Target:** Email 60%, LinkedIn 40%
- **Gap:** Email slightly low (-3%)
- **Action:** For next batch, increase email proportion. Acceptable but optimize for target.

---

## 🟡 MEDIUM CONFIDENCE: Monitor & Validate (Return Mar 22)

### 1. Overall Reply Rate
- **Status:** Reply window still open (oldest sends Feb 23 = 21 days ago)
- **Why we can't measure yet:** Standard 14-21 day reply window
- **Action:** Re-run analytics Mar 22 when last sends hit day-21 cutoff
- **What to expect:** 3-8% overall reply rate based on historic baseline

### 2. Subject Line & CTA Performance
- **Status:** Only 5% of sends matched to batch draft data
- **Why:** Early batches used different naming. Only newest batches have consistent tracker HTMLs
- **Action:** Wait until Mar 22 when reply data matures AND newer batches have complete HTML records
- **Expected improvement:** Match rate should jump to 30-50% for Mar 1+ sends

### 3. Persona Mix Accuracy
- **Data needed:** Contact titles extracted from batch HTML prospect-name fields
- **Current status:** Awaiting full HTML parsing of 11 remaining batch files
- **Action:** Validate persona distribution by Apr 1 when all batch data is indexed
- **Target mix:** 35% QA Manager, 35% Director QA, 20% SDET, 5% VP Eng, 5% Other

---

## 🔴 INSUFFICIENT DATA: Do Not Act Yet

### 1. Word Count Sweet Spot (Need >100 samples with draft data)
- **Current:** Only 36 sends matched to batch drafts with word count data
- **Baseline:** 75-99 words = 39% reply rate  
- **Action:** Validate Mar 22 with full reply window

### 2. Proof Point Rotation (Need full reply window)
- **Current:** Top proof point appears in 32% (under 40% threshold = acceptable)
- **Action:** Monitor for overuse trends once replies come in

### 3. Send Day Optimization (Need >14 days post-send for all dates)
- **Current:** Can't calculate reply velocity by day-of-week yet
- **Action:** Validate Apr 1 when oldest sends (Feb 23) pass day-21 threshold

---

## Quick Checklist for Next TAM T1 Batch

- [ ] **Personas:** 35% QA Managers, 35% Directors, 20% SDETs (not VPs unless deal intent)
- [ ] **Word count:** 75-99 words minimum 40% of batch
- [ ] **Email focus:** Increase to 60% (currently 57%)
- [ ] **Proof points:** Use min 4 different proof points (no single one > 40%)
- [ ] **Bounce filter:** Skip ea.com domain entirely
- [ ] **Dedup:** Cross-check all names against MASTER_SENT_LIST.csv before send
- [ ] **Batch tracker:** Create HTML tracker file with prospect-name divs for post-send analysis

---

## Why Match Rate Is Low (5%)

1. **Batch HTML files created at different times:** Early batches (Feb 13 - Feb 27) had minimal HTML tracking
2. **File naming inconsistency:** Batch 1, 2, 3 vs. tamob-batch-20260312-X different schema
3. **Newer TAM batches (Mar 1+) have much better tracking:** These will show 40%+ match rates
4. **Not all 610 contacts from all batch sources:** Some from LinkedIn, some from Apollo, some from manual outreach

**Expected improvement trajectory:**
- Feb sends: 5-10% match (sparse batch files)
- Mar 1-15 sends: 25-40% match (TAM T1 batches with full HTML)
- Mar 16+ sends: 50%+ match (new batches with consistent naming)

---

## Return on Mar 22

When reply data matures, you'll know:
- ✓ True reply rate by send day (Mon/Tue/Wed best?)
- ✓ Reply rate by subject line formula
- ✓ Reply rate by proof point (validation data)
- ✓ Average reply latency (days post-send)
- ✓ CTA performance ("What day works" baseline 40.4%)
- ✓ Persona-level reply rates (who replies most?)
- ✓ Vertical reply rates (SaaS vs FinTech vs Healthcare)

