# Subject Line Optimizer

**Version:** 1.0 — Created Mar 15, 2026

**Schedule:** Fridays 5:20 PM (runs after weekly-analytics) + on-demand

**Output:**
- `analytics/reports/subject-line-performance-[YYYY-MM-DD].md` (detailed analysis report)
- Appends 3-bullet summary to `memory/session/messages.md` under today's date

---

## Purpose

Analyze email subject line performance across all active batches and outreach sends. Correlate subject lines with reply rates, opens, and sentiment by persona and vertical to surface what's working and what isn't. Generate actionable recommendations for next batch optimization.

---

## Trigger

Run when:
- Rob says "subject line analysis", "what subject lines are working", "optimize subject lines", or similar
- Scheduled Friday 5:20 PM (after weekly-analytics)
- On-demand at any time during session

---

## Phase 1 — Extract Subject Lines from Batch Trackers

**Steps:**

1. Read all HTML files in `batches/active/` directory (tamob-batch-*.html)
2. Parse each tracker table to extract the "Email Subject" column
3. Also scan `batches/t2-pending/` for T2 subject lines
4. For historical context, check `archive/old-outreach-html/` for older batch files if DB contains matching reply data

**Data captured for each subject line:**
```
{
  contact_name,
  company,
  persona,
  vertical,
  subject_line,
  touch_number,
  send_date,
  batch_id,
  archive_status (active | pending | archived)
}
```

5. Store extracted data in memory during analysis (no file write yet)

---

## Phase 2 — Pull Reply Correlation from DB

**Steps:**

1. Query `analytics/outreach.db` table `outreach_sends`:
   ```sql
   SELECT contact_name, company, replied, reply_sentiment FROM outreach_sends
   WHERE email_subject IS NOT NULL
   ```

2. **Schema validation:** If `email_subject` column does NOT exist in `outreach_sends` table:
   - Note as a schema gap in the report
   - Add the column via: `ALTER TABLE outreach_sends ADD COLUMN email_subject TEXT`
   - Add placeholder note to report recommending future enrichment

3. Cross-reference subject lines from Phase 1 with DB reply records by `contact_name + company` match

4. Build correlation map: subject_line → {reply_count, reply_rate, sentiment_distribution}

---

## Phase 3 — Pattern Analysis

Analyze all subject lines across these dimensions:

### 3.1 Length Analysis
- **Under 40 characters** — reply rate %
- **40-60 characters** — reply rate %
- **60+ characters** — reply rate %
- Note: optimal range by persona + vertical

### 3.2 Formula Type Classification

Classify each subject line into one or more formula types:

1. **Question Format** — starts with "Quick question" or ends with "?"
   - Example: "Quick question about your QA stack?"
2. **Name Personalization** — contains contact's first name
   - Example: "Sarah, your test suite needs this"
3. **Company Personalization** — contains company name
   - Example: "Acme's test automation approach"
4. **Pain-Point Lead** — leads with known pain (flaky tests, maintenance, coverage)
   - Example: "Flaky tests costing you hours?", "Test maintenance at Cisco"
5. **Proof-Point Lead** — references customer success or metric
   - Example: "How Cisco cut regression time by 8 weeks", "How Medibuddy scaled to 2,500 tests"
6. **Role-Specific** — targets decision-maker role explicitly
   - Example: "For QA leads at Fortune 500 firms", "Attention: QA automation engineers"
7. **Curiosity/Open Loop** — hooks with intrigue or pattern observation
   - Example: "Something I noticed at your stack", "Thought on your tech debt approach"
8. **Urgency/Deadline** — implies time sensitivity
   - Example: "Your migration timeline", "Before Q2 releases start"
9. **Benefit/Value Clear** — explicitly states benefit
   - Example: "Cut test maintenance in half", "Recover 20 hours per week"

### 3.3 Persona Correlation

Cross-tabulate formula types with persona success rates:
- QA Manager
- QA Lead
- Director/VP of QA
- VP Engineering / CTO
- SDET / Automation Engineer

Example output:
```
Formula Type              | QA Manager | QA Lead | Director | VP Eng | SDET
Question Format          | 28% reply  | 35%    | 22%     | 18%   | 42%
Pain-Point Lead         | 42% reply  | 48%    | 38%     | 25%   | 52%
Proof-Point Lead        | 35% reply  | 40%    | 51%     | 48%   | 38%
```

### 3.4 Vertical Correlation

Cross-tabulate formula types with vertical success rates:
- SaaS/Tech
- FinTech
- Retail/E-Commerce
- Healthcare/Digital Health
- Telecom
- Pharma

---

## Phase 4 — Surface Recommendations

Generate a ranked output with four sections:

### 4.1 🥇 Top 3 Performing Formulas
- Ranked by reply rate (minimum 5 sends per formula)
- Include: formula type, exact subject line example, reply rate %, winning persona + vertical
- Note any patterns (length, personalization, tone)

### 4.2 🚫 Bottom 3 Underperformers
- Ranked by lowest reply rate (minimum 5 sends)
- Include: formula type, exact example, reply rate %, which personas avoided
- Hypothesis on why they underperformed

### 4.3 💡 3 Recommended New Variants to Test
- Based on gap analysis (high-performing formulas not yet tested)
- Suggest new subject line copy blending top formulas
- Include: formula blend, suggested subject line, target persona, rationale

### 4.4 ⚠️ Schema Gaps
- List any DB columns missing that would improve tracking
- Recommended additions: `email_subject`, `subject_formula_type`, `open_rate`, `click_rate`

---

## Phase 5 — Write Report

**File:** `analytics/reports/subject-line-performance-[YYYY-MM-DD].md`

**Structure:**

```markdown
# Subject Line Performance Analysis

_Generated [DATE] by Subject Line Optimizer_

## Executive Summary

- 🥇 **Top Formula:** [Type] achieves [X]% reply rate across [N] sends
- 📊 **Total Subjects Analyzed:** [N] across [M] active batches
- 💡 **Key Insight:** [1-2 sentence insight on biggest opportunity or pattern]

## Full Performance Data

| Subject Line | Formula Type | Sends | Replies | Reply Rate | Top Persona | Top Vertical |
|---|---|---|---|---|---|---|
| [exact copy] | [type] | N | N | X% | [persona] | [vertical] |
| [exact copy] | [type] | N | N | X% | [persona] | [vertical] |
| ... | ... | ... | ... | ... | ... | ... |

## Length Analysis

- **Under 40 chars:** X% reply rate (N sends)
- **40-60 chars:** X% reply rate (N sends)
- **60+ chars:** X% reply rate (N sends)

## Formula Type Performance

| Formula Type | Sends | Replies | Reply Rate | Best Persona | Best Vertical |
|---|---|---|---|---|---|
| Question Format | N | N | X% | [persona] | [vertical] |
| Pain-Point Lead | N | N | X% | [persona] | [vertical] |
| Proof-Point Lead | N | N | X% | [persona] | [vertical] |
| ... | ... | ... | ... | ... | ... |

## Persona Correlation

[Cross-tab table of formulas vs personas with reply rates]

## Vertical Correlation

[Cross-tab table of formulas vs verticals with reply rates]

## Recommendations

### 🥇 Top 3 Performing Formulas

1. **[Formula Type]** — [X]% reply rate
   - Example: "[subject line]"
   - Winning Persona: [persona]
   - Pattern: [what makes it work]

2. **[Formula Type]** — [X]% reply rate
   - Example: "[subject line]"
   - Winning Persona: [persona]
   - Pattern: [what makes it work]

3. **[Formula Type]** — [X]% reply rate
   - Example: "[subject line]"
   - Winning Persona: [persona]
   - Pattern: [what makes it work]

### 🚫 Bottom 3 Underperformers

1. **[Formula Type]** — [X]% reply rate
   - Example: "[subject line]"
   - Why it underperformed: [hypothesis]
   - Recommendation: [shift to X formula instead]

2. **[Formula Type]** — [X]% reply rate
   - Example: "[subject line]"
   - Why it underperformed: [hypothesis]
   - Recommendation: [shift to X formula instead]

3. **[Formula Type]** — [X]% reply rate
   - Example: "[subject line]"
   - Why it underperformed: [hypothesis]
   - Recommendation: [shift to X formula instead]

### 💡 3 Recommended New Variants to Test Next Batch

1. **Blend:** [Formula 1] + [Formula 2]
   - Suggested: "[new subject line]"
   - Target Persona: [persona]
   - Target Vertical: [vertical]
   - Rationale: [why this combo should work]

2. **Blend:** [Formula 1] + [Formula 2]
   - Suggested: "[new subject line]"
   - Target Persona: [persona]
   - Target Vertical: [vertical]
   - Rationale: [why this combo should work]

3. **Blend:** [Formula 1] + [Formula 2]
   - Suggested: "[new subject line]"
   - Target Persona: [persona]
   - Target Vertical: [vertical]
   - Rationale: [why this combo should work]

### ⚠️ Schema Gaps

- **Missing Columns in `outreach_sends` table:**
  - `email_subject` — store actual subject line per send
  - `subject_formula_type` — classify formula type
  - `open_rate` — track opens (requires email provider integration)
  - `click_rate` — track clicks (requires email provider integration)
- **Action:** Recommend enriching DB schema in next analytics infrastructure sprint

## Next Actions

1. Test recommended new variants in next T1 batch (Mon/Wed/Fri auto-prospect)
2. Monitor reply rates for new formulas over 2-week window
3. Re-run this analysis in 3 weeks to measure impact
4. Consider A/B testing top 2 formulas in parallel next batch
```

**After report is saved:**

1. Append a 3-bullet summary to `memory/session/messages.md` under today's date:
   ```
   **Subject Line Optimizer Run — [DATE]**
   - [Bullet 1: Top formula type + reply rate]
   - [Bullet 2: Key insight/opportunity]
   - [Bullet 3: Recommended next action]
   ```

---

## Learning Loop Integration

Follow `skills/_shared/learning-loop.md` protocol:

1. **Run Log:** Maintain `subject-line-optimizer/run-log.md`
   - Log each run: date, number of subjects analyzed, batches scanned, key finding
   - Track confidence level (low/medium/high) based on sample size

2. **Learned Patterns:** Maintain `subject-line-optimizer/learned-patterns.md`
   - After 5 runs, consolidate recurring patterns
   - Document which formula types consistently outperform
   - Note persona + vertical surprises
   - Document seasonal/temporal patterns

3. **Instant Approval Protocol:**
   - Every 5th run (Run #5, #10, #15, etc.), append proposed SKILL.md improvements to run-log.md
   - Include: new formula types to track, DB schema additions, phase improvements
   - Rob reviews and approves/rejects via inline comment (no formal meeting needed)

4. **Self-Improvement Triggers:**
   - If a new formula type emerges that doesn't fit current 9 types, document in learned-patterns.md
   - If a persona shows unexpected pattern, flag for deeper analysis in next run
   - If reply rates shift significantly month-over-month, investigate market/seasonal factors

---

## Technical Requirements

**Dependencies:**
- `analytics/outreach.db` (SQLite) with `outreach_sends` table
- `batches/active/*.html` batch tracker files
- `batches/t2-pending/*.html` T2 batch files
- `archive/old-outreach-html/*.html` historical batches (optional)
- `memory/session/messages.md` for summary append

**Data Outputs:**
- Primary: `analytics/reports/subject-line-performance-[YYYY-MM-DD].md`
- Secondary: append to `memory/session/messages.md`
- Internal: run-log.md update

**Error Handling:**
- If `batches/active/` is empty: report "No active batches to analyze" and skip
- If `outreach_sends` table is empty: report "No reply data yet" and skip
- If schema gaps detected: note in Phase 2 and still run analysis (use available columns)
- If HTML parsing fails: log which file failed and continue with remaining files

**Performance Note:**
- Expected runtime: 2-5 minutes for 50+ active subjects
- If > 200 subjects, may take 10+ minutes — notify Rob if long-running

---

## Example Use Cases

**Rob asks in session:**
> "What subject lines are working best?"

Claude:
1. Runs Phase 1-5 end-to-end
2. Generates report
3. Displays summary in chat + provides file path

**Scheduled Friday 5:20 PM:**
1. Auto-runs after weekly-analytics completes
2. Generates report
3. Appends 3-bullet summary to memory/session/messages.md
4. No chat notification needed (runs silently)

**Rob says mid-week:**
> "Subject line analysis"

Claude:
1. Runs Phase 1-5
2. Reports findings for new batches sent this week
3. Offers to generate variants for next T2 draft or new T1 batch

---

## Integration with Other Skills

- **TAM T1 Batch:** Uses top-performing formulas from this report for new batch subject lines
- **T2 Draft Generator:** (when unlocked) references proven formulas by persona
- **Analytics Engine:** feeds back formula performance metrics to weekly dashboard
- **Weekly Analytics:** this skill runs immediately after, using fresh reply data
- **System Diagnostics:** monitors this skill's output for schema gaps + performance trends

---

## Instant Approval Protocol

When Instant Approval Protocol triggers (every 5th run), append to run-log.md:

```markdown
## Run #[N] — Proposed SKILL.md Improvements

**Date:** [date]
**Context:** After [N] runs, identified these improvements:

### New Formula Types to Track
- [Formula type]: [rationale]

### DB Schema Additions
- [Column name]: [type] — [why]

### Phase Improvements
- [Phase X]: [change]

**Status:** _Pending Rob review and approval_
```

Rob approves via inline comment in run-log.md. No formal meeting needed.

---

## Version History

- **1.0** (Mar 15, 2026) — Initial release. 9 formula types, 5-phase analysis, Friday + on-demand scheduling.
