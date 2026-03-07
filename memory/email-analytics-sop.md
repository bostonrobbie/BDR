# Email Analytics SOP
**Version:** 1.0 — Created Mar 7, 2026
**Owner:** Rob Gorham · BDR, Testsigma
**Cadence:** Update weekly (every Monday AM)

---

## Purpose

This SOP defines how to track email outreach performance, keep the SQLite DB current, interpret metrics, and iterate on strategy. It complements the LinkedIn InMail tracking in `pipeline-state.md`.

---

## 1. Weekly Update Checklist

Run the following every Monday morning before sending new emails:

### Step 1 — Pull New Gmail Sent Emails

Ask Claude (in Cowork mode) to run the sync:

> "Sync our Gmail sent emails to the BDR DB — pull all emails sent since [last update date], classify them, and insert into email_outreach."

Claude will:
- Search Gmail for `in:sent after:[date]`
- Filter cold outbound emails (exclude internal Testsigma, calendar/scheduling, bounces)
- Classify: subject_type, pain_hook, vertical, word_count
- Insert new records into `email_outreach` table (deduplicates by gmail_id)

### Step 2 — Check for New Replies

Ask Claude:

> "Check Gmail inbox for any new replies from cold prospects since [last update date] and update the DB."

Claude will:
- Search `in:inbox from:NOT(@testsigma.com) after:[date]`
- Match replies to sent emails by thread/sender
- Update `replied=1`, `reply_intent`, `reply_tag` on the `email_outreach` record
- Insert into `email_replies` with summary + intent

### Step 3 — Update pipeline_stats

Claude will re-calculate and upsert the weekly pipeline_stats row:
```
stat_date = today
channel = 'email'
total_sent = COUNT(email_outreach)
total_replied = COUNT(DISTINCT to_email WHERE replied=1)
reply_rate = total_replied / total_sent * 100
```

### Step 4 — Refresh the Dashboard

Ask Claude:

> "Regenerate the BDR email analytics dashboard with the latest data."

The HTML file at `/Work/BDR/email-analytics-dashboard.html` will be updated with all new data.

---

## 2. DB Schema Reference

**Database:** `/Work/BDR/outreach.db` (SQLite)

### `email_outreach` — One row per cold outbound email sent
| Field | Type | Notes |
|---|---|---|
| id | INTEGER PK | Auto |
| gmail_id | TEXT UNIQUE | Gmail message ID (dedup key) |
| thread_id | TEXT | Gmail thread ID |
| to_email | TEXT | Recipient email |
| to_name | TEXT | Recipient name |
| subject | TEXT | Full subject line |
| subject_type | TEXT | quick_question / custom_descriptive / follow_up / one_more_thought |
| touch_number | INTEGER | 1=cold, 2=follow-up, 3=second follow-up |
| sent_at | TEXT | ISO timestamp |
| day_of_week | TEXT | Monday–Sunday |
| hour_sent | INTEGER | Hour in UTC (0–23) |
| pain_hook | TEXT | test_maintenance / release_velocity / coverage_scale / migration_compliance / regression_quality / unknown |
| vertical | TEXT | FinTech / Healthcare / SaaS / Insurance / Enterprise / Other |
| word_count | INTEGER | Email body word count |
| replied | INTEGER | 0/1 |
| bounced | INTEGER | 0/1 |
| dnc | INTEGER | 0/1 — Do Not Contact |
| meeting_booked | INTEGER | 0/1 |

### `email_replies` — One row per unique replying contact
| Field | Type | Notes |
|---|---|---|
| id | INTEGER PK | Auto |
| to_email | TEXT | Replier email |
| intent | TEXT | engaged / objection / not_interested / out_of_office / referral |
| tag | TEXT | pain_hook / timing / wrong_person / positive / negative |
| summary | TEXT | Free-text summary of reply |
| reply_count | INTEGER | Number of back-and-forth messages |

### `pipeline_stats` — Weekly summary snapshots
| Field | Type | Notes |
|---|---|---|
| stat_date | TEXT | YYYY-MM-DD |
| channel | TEXT | email / linkedin_inmail |
| total_sent | INTEGER | Cumulative sends |
| total_replied | INTEGER | Unique repliers |
| reply_rate | REAL | Percentage |

---

## 3. Key Metrics and Benchmarks

| Metric | Current | Benchmark (data-rules.md) | Target |
|---|---|---|---|
| Overall reply rate | 1.8% | 28.7% (historical) | 5%+ at 200 sends |
| Quick Question reply rate | 16% (Pallavi thread) | — | 8–12% sustained |
| Custom Descriptive reply rate | 0% | — | 4%+ |
| Email volume / week | 17–35 | — | 50+ |
| Bounce rate | 1.8% | <5% | <2% |
| Meeting conversion | 0% | — | 10% of replies |

**Note:** The 28.7% benchmark is from LinkedIn InMail analysis (1,326 conversations, mabl 2021–2023). Email cold reply rates for SaaS/tech products typically run 2–8% for cold sends. Aim for 5–8% as a strong benchmark.

---

## 4. Subject Type Classification Rules

Use this logic to classify each email's subject line:

| Type | Pattern | Example |
|---|---|---|
| `quick_question` | Subject = "Quick question, [Name]" OR very short ≤4 words | "Quick question, Pallavi" |
| `custom_descriptive` | Subject references company name + pain area (7–12 words) | "Origami Risk regression coverage as you scale, Pallavi" |
| `one_more_thought` | "One more thought on [Company]..." | "One more thought on Vertafore's test coverage, Chen" |
| `follow_up` | "Follow-up:", "Re:", "Following up on..." | "Follow-up: Slalom QA automation strategy" |

---

## 5. Pain Hook Classification Rules

Extracted from subject line + context:

| Hook | Keywords |
|---|---|
| `test_maintenance` | maintenance, cutting maintenance, maintenance time |
| `release_velocity` | release velocity, release speed, deploy faster, ship faster |
| `coverage_scale` | coverage, scale, expansion, grow, platform expansion |
| `migration_compliance` | migration, compliance, SOC, regulatory, HIPAA |
| `regression_quality` | regression, quality, flaky, regression debt |
| `unknown` | none of the above (typically quick_question format) |

---

## 6. Reply Intent Classification

When logging a reply, classify the intent:

| Intent | Description |
|---|---|
| `engaged` | Prospect shows interest, asks questions, or shares context (like Pallavi) |
| `objection` | Not the right time / happy with current tool / budget freeze |
| `not_interested` | Direct "no thank you" or opt-out |
| `out_of_office` | Auto-reply / OOO message |
| `referral` | Directed to another person at the company |

---

## 7. A/B Testing Protocol

Based on `scoring-feedback.md` and `outreach-operations.md` rules:

### Current Active A/B Test
- **Test A:** Quick Question subject line (`"Quick question, [Name]"`)
- **Test B:** Custom Descriptive subject line (`"[Company] [Pain] at [Scale], [Name]"`)
- **Status:** Test A winning — 16% vs 0% (low sample, n=25 vs 26)
- **Next action:** Run 50+ of each for statistical significance

### How to Track New A/B Tests
1. Add test tag to `sequence_name` field in email_outreach
2. After 30+ sends per variant: query reply rates by sequence_name
3. Document winning variant in `scoring-feedback.md`

---

## 8. Vertical Strategy (Current Data)

| Vertical | Emails Sent | Replies | Strategy |
|---|---|---|---|
| Insurance | 8 | 1 (Pallavi) | **Double down.** Strong signal. Add more Origami Risk, Vertafore, Zurich contacts with QQ format. |
| SaaS | 13 | 0 | Convert to QQ format. Test shorter 28-word emails. |
| Enterprise | 13 | 0 | Heavy on custom_descriptive. Switch 50% to QQ. |
| FinTech | 7 | 0 | All custom_descriptive. Test QQ. Priority: compliance hook. |
| Healthcare | 7 | 0 | All custom_descriptive. Test QQ. Priority: release velocity hook. |
| Other | 8 | 0 | Low priority. Deprioritize SI/consulting firms. |

---

## 9. DNC and Bounce Management

Always check before sending:

**Active DNC list** (from `pipeline-state.md`):
- Shan Hossain
- Kaushal Parikh
- Rajesh Bhatt
- Pradeep Nair
- Sudharshan K

**Bounced emails** (mark bounced=1, do not re-send):
- nethrasheebi@email.com — hard bounce (invalid)

**Before sending any email:**
1. Search `email_outreach` for existing record with same `to_email`
2. If `dnc=1` or `bounced=1` → skip
3. If `touch_number=1` already sent → use follow-up template (touch_number=2)

---

## 10. Weekly Review Questions

Ask these every Monday:

1. **Volume:** Did we hit our send target last week? (Target: 50/week)
2. **Reply rate:** Any new replies? What was the intent?
3. **Follow-up cohort:** Which Week N emails need a T+7 follow-up this week?
4. **Warm leads:** What's the next action for Pallavi and Namita?
5. **A/B test:** Do we have 30+ sends per variant to read results?
6. **Vertical:** Are we over-indexing on any single vertical?
7. **Pain hooks:** Are we testing enough variety or defaulting to QQ?

---

## 11. Monthly Reporting

At the end of each month, generate:
- Summary stats (total sent, reply rate, meetings booked, pipeline created)
- Subject type A/B test results
- Vertical performance ranking
- Top performing pain hooks
- Next month's sequencing plan

Ask Claude: "Generate our monthly BDR email performance report from the outreach DB and save it to `/Work/BDR/memory/`."

---

## 12. Files Reference

| File | Purpose |
|---|---|
| `/Work/BDR/outreach.db` | Main SQLite database |
| `/Work/BDR/email-analytics-dashboard.html` | Interactive analytics dashboard |
| `/Work/BDR/memory/pipeline-state.md` | Master pipeline state (LinkedIn InMail primary) |
| `/Work/BDR/memory/warm-leads.md` | Active warm leads tracking |
| `/Work/BDR/memory/data-rules.md` | Message writing rules + benchmarks |
| `/Work/BDR/memory/scoring-feedback.md` | A/B test results + priority scoring |
| `/Work/BDR/memory/email-analytics-sop.md` | This file |
| `/Work/BDR/TEMPLATE_LIBRARY.md` | All message templates by type/hook/persona |

---

*Last updated: Mar 7, 2026 · Auto-generated by Claude (Cowork mode)*
