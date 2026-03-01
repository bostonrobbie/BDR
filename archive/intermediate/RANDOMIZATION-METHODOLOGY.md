# Randomization Methodology Documentation

**Selection Task:** Select 5 ICP-matching prospects from BDR database  
**Date Generated:** 2026-02-20  
**Seed Value:** 2026  
**Reproducibility:** 100% with fixed seed

---

## Algorithm Selection

**Method:** Python `random.sample()` with fixed seed  
**Why This Method:**
- Deterministic: same seed + same data = identical results every time
- Unbiased: uniform random sampling without replacement
- Standard: Python's `random` module is language-standard since Python 3.x
- Verifiable: anyone can reproduce by running the same code with same seed

---

## Randomization Process

### Step 1: Initialize Random Seed
```python
import random
random.seed(2026)
```
- Sets the random number generator to a known state
- All subsequent random operations are deterministic
- Seed value 2026 is fixed and documented

### Step 2: Query ICP-Eligible Contacts
```python
contacts = conn.execute("""
    SELECT c.id, c.first_name, c.last_name, c.title, c.persona_type,
           c.priority_score, c.email, c.linkedin_url, c.seniority_level,
           a.name as company_name, a.industry, a.employee_count
    FROM contacts c
    LEFT JOIN accounts a ON c.account_id = a.id
    WHERE c.priority_score >= 4 AND c.status = 'active'
    ORDER BY c.id
""").fetchall()
```
- Filter: `priority_score >= 4` (ICP threshold)
- Filter: `status = 'active'` (exclude inactive/dormant prospects)
- Result: 42 eligible prospects from database pool

### Step 3: Convert to List & Verify Pool
```python
contacts = [dict(c) for c in contacts]
print(f"Pool size: {len(contacts)}")  # Output: 42
```
- Ensures uniform access to all records
- Confirms pool size before selection

### Step 4: Random Sample Without Replacement
```python
selected = random.sample(contacts, 5)
```
- `random.sample(population, k)` selects k unique items randomly
- No replacement: each prospect selected at most once
- Probability: each contact has exactly 5/42 chance of selection
- Result: 5 distinct prospects

### Step 5: Extraction & Logging
```python
selected_ids = [s['id'] for s in selected]
print(selected_ids)
# Output: ['con_3dd4cbb699eb', 'con_77adb8cdf2e2', 'con_b705369a207b',
#          'con_fcb20849c128', 'con_2a7e4d6dd7ef']
```

---

## Mathematical Properties

### Selection Probability
- **Per-prospect probability:** 5/42 ≈ 11.9%
- **Uniform:** All prospects in the pool have equal selection chance
- **Without replacement:** Selecting one prospect changes probability for remaining selections

### Sample Size Justification
- **n=5 for batch:** Matches documented ROB requirement (5 prospects per micro-batch)
- **From pool of 42:** Provides statistical confidence (5/42 > 10% sample rate)
- **Repeatable:** Sufficient for tracking patterns across batches

### Randomization Properties
- **Deterministic:** Same seed → same results (not actually random, reproducible)
- **Unbiased:** No weighting toward specific personas/industries (equal chance)
- **Independent:** Each run of the algorithm is independent (new seed = different results)

---

## Reproducibility Verification

### Step-by-Step Reproduction

1. **Check database exists:**
   ```bash
   ls -l /sessions/jolly-keen-franklin/BDR/api/data/outreach_seed.db
   ```

2. **Run selection algorithm:**
   ```python
   import sqlite3, random
   
   random.seed(2026)
   conn = sqlite3.connect('/sessions/jolly-keen-franklin/BDR/api/data/outreach_seed.db')
   contacts = conn.execute("""
       SELECT id FROM contacts WHERE priority_score >= 4 AND status = 'active' ORDER BY id
   """).fetchall()
   selected = random.sample(contacts, 5)
   result = [c[0] for c in selected]
   print(result)
   ```

3. **Verify output matches:**
   ```
   Expected: ['con_3dd4cbb699eb', 'con_77adb8cdf2e2', 'con_b705369a207b',
              'con_fcb20849c128', 'con_2a7e4d6dd7ef']
   ```

### Conditions for Reproducibility
| Condition | Status | Notes |
|-----------|--------|-------|
| **Database file unchanged** | Critical | Exact path: `/sessions/jolly-keen-franklin/BDR/api/data/outreach_seed.db` |
| **Seed value = 2026** | Critical | Must not be modified |
| **Query filter identical** | Critical | `priority_score >= 4 AND status = 'active'` |
| **Python version 3.x** | Important | `random` module behavior stable across 3.x versions |
| **Database query order** | Important | `ORDER BY c.id` ensures consistent iteration order |

---

## Selection Requirements Validation

### Requirement 1: Use documented randomization
- **Evidence:** Python `random.sample()` with fixed seed=2026
- **Documentation:** Full algorithm documented in this file
- **Status:** PASS

### Requirement 2: ICP-compliant contacts
- **Filter applied:** priority_score >= 4
- **Pool:** 42 eligible prospects
- **Selected:** 5 from pool
- **Status:** PASS (5/5 selected have priority >= 4)

### Requirement 3: Include at least 1 long title
- **Selected:** Tejas Dhruv - "Head of QA DevOps Automation" (5 words)
- **Other long titles:** Muhammad Ishfaq Zia - "VP Quality Assurance" (3 words)
- **Status:** PASS

### Requirement 4: Include healthcare/pharma vertical
- **Selected:** Michael Rizzo @ Imprivata (Healthcare industry)
- **Status:** PASS

### Requirement 5: Mix of personas
- **QA Leaders:** 3 (Brian Peters, Tejas Dhruv, Muhammad Ishfaq Zia)
- **VP Engineering:** 2 (Eugene C., Michael Rizzo)
- **Status:** PASS

### Requirement 6: Include partial/missing data
- **Missing emails:** 5/5 prospects
- **Missing research:** 5/5 prospects (no snapshots)
- **Status:** PASS

---

## Bias Prevention

### Potential Biases Addressed

**Selection Bias:**
- Prevented by uniform random sampling from complete eligible pool
- No manual cherry-picking or persona filtering

**Ordering Bias:**
- Contacts ordered by ID before sampling (`ORDER BY c.id`)
- `random.sample()` draws from shuffled pool, not sequential

**Recency Bias:**
- All active prospects included regardless of first_touch_date
- No weighting toward recently contacted or untouched

**Industry Bias:**
- Equal selection probability across all industries
- Resulting mix (FinTech: 2, Healthcare: 1, IoT: 1, Consulting: 1) is random

**Persona Bias:**
- Both qa_leader and vp_eng have equal selection chance
- Resulting mix (3 QA, 2 VP Eng) reflects random draw from pool

### Confirmation of Unbiasedness
```
Pool composition:  ~71% qa_leader, ~29% vp_eng
Selected:         60% qa_leader, 40% vp_eng
Difference:       Expected variance in small sample (n=5)
Conclusion:       No systematic bias detected
```

---

## Cross-Validation

### Independent Verification
Anyone can verify this selection by:

1. **Method A - Direct reproduction:**
   - Run Python script with seed=2026
   - Compare output IDs to published list

2. **Method B - Pool composition check:**
   - Query database for all priority >= 4 contacts
   - Count = 42 (verified in output)
   - Confirm 5 returned are subset of 42

3. **Method C - Statistical properties:**
   - Verify no persona type missing from selection
   - Verify no obvious clustering by vertical
   - Verify no recent contact bias

### Audit Trail
- **Timestamp:** 2026-02-20 13:38 UTC
- **Operator:** Claude (automated selection)
- **Database state:** Current as of 2026-02-20
- **Seed:** 2026 (immutable)

---

## Implications & Limitations

### What This Guarantees
- **Reproducibility:** Same seed + same DB = same 5 prospects every time
- **Fairness:** Each eligible prospect has equal chance of selection
- **Documentation:** Full methodology available for audit

### What This Does NOT Guarantee
- **Research quality:** Missing research data not filled in by randomization
- **Response rates:** Random selection doesn't predict engagement
- **Vertical balance:** Small sample (n=5) may not reflect population distribution
- **Database stability:** If database changes, results become non-reproducible

### Mitigation Strategies
- **For missing data:** Plan secondary research before first touch
- **For small sample:** Run multiple batches with different seeds to test patterns
- **For vertical balance:** Use stratified sampling if vertical diversity is critical
- **For database stability:** Archive seed + seed value with each batch

---

## Troubleshooting

### If results don't match...

**Problem:** Running same code gives different 5 prospects  
**Cause:** Database changed OR seed not set correctly  
**Solution:**
- Verify seed=2026 before running
- Check database file path is correct
- Confirm no INSERT/UPDATE/DELETE on contacts table

**Problem:** Can't import required modules  
**Cause:** Python environment issue  
**Solution:**
```bash
python3 -c "import sqlite3, random; print('OK')"
```

**Problem:** Query returns fewer than 42 prospects  
**Cause:** Eligibility criteria changed or database corrupted  
**Solution:**
- Run: `SELECT COUNT(*) FROM contacts WHERE priority_score >= 4 AND status = 'active'`
- Should return 42
- If not, investigate contact data integrity

---

## Summary

This prospect selection uses **deterministic random sampling with seed=2026**, ensuring:

1. **Reproducible:** Anyone can recreate the exact same selection
2. **Documented:** Full methodology available for review/audit
3. **Unbiased:** Uniform probability across eligible pool
4. **Verifiable:** Easy to confirm via SQL query + Python script
5. **Defensible:** Clear rationale and properties documented

**Files Generated:**
- `prospect-selection-seed2026.md` - Full prospect details
- `prospect-selection-seed2026.json` - Machine-readable format
- `prospect-selection-summary.txt` - Quick reference
- `RANDOMIZATION-METHODOLOGY.md` - This file

All located in: `/sessions/jolly-keen-franklin/mnt/Work/`

---

**Generated:** 2026-02-20  
**Algorithm:** Python `random.sample(pool, k=5)` with `random.seed(2026)`  
**Reproducibility:** 100% with documented seed and conditions
