# Outreach Operations Reference

This file contains the detailed operational procedures for batch building, tracking, and follow-up. The core writing rules and hard constraints live in CLAUDE.md. This file covers the mechanics.

## Deliverable Format

Single HTML file (or markdown in `work/`) with:
- Prospect tracker table sorted by priority score (descending)
- Columns: priority score, name, title, company, tags, profile research notes, company research notes, outreach angle, LinkedIn URL, status, reply tag, A/B group, personalization score
- Individual prospect cards with:
  - Copy-paste-ready messages for ALL written touches
  - Cold call snippets (3-line cheat sheets)
  - Predicted objection + pre-loaded response
  - Meeting prep card (when status = Meeting Booked)
- Status dropdown: Not Started, Touch 1 Sent, Call 1 Made, Touch 3 Sent, Call 2 Made, Touch 5 Sent, Touch 6 Sent, Replied, Meeting Booked, Not Interested, Bounced, Dormant, Re-Engaged
- Reply tag dropdown (see Reply Tagging below)
- Filename convention: `prospect-outreach-[batch#]-[date].html`

## Reply Tagging

When a prospect replies, tag WHAT triggered it:
- **Opener** - Referenced or reacted to the personalized opener
- **Pain hook** - Engaged with the problem hypothesis
- **Proof point** - Asked about the customer story or numbers
- **Timing** - Said "good timing" or "we're evaluating"
- **Referral** - Forwarded to someone else
- **Not interested** - Declined (still useful data)
- **Unknown** - Can't tell

Even negative replies are data.

## A/B Testing Within Batches

Split each 25-prospect batch into 2-3 sub-groups to test ONE variable:

Variables to test (one per batch, rotate):
1. Pain hook (maintenance vs velocity)
2. Proof point style (named customer vs anonymous)
3. Opener style (career-reference vs company-metric)
4. Ask intensity ("Would 15 minutes..." vs "Happy to share more if helpful")
5. Message length (70-80 words vs 100-120 words)

Rules:
- ONE variable per batch. Keep everything else constant.
- Split evenly by persona type and vertical.
- Need 3+ batches testing same variable to draw conclusions.

## Priority Scoring (1-5)

| Factor | Points |
|--------|--------|
| Buyer Intent signal | +2 |
| QA-titled leader (Director/Head/VP of QA) | +1 |
| Company in top vertical (FinTech, SaaS, Healthcare) | +1 |
| Recently hired in role (<6 months) | +1 |
| Company in active transformation/migration | +1 |
| Company uses known competitor tool | +1 |
| VP Eng at 50K+ company (no QA scope) | -1 |

Tiers:
- 5 (Hot): Work first every morning. Call + InMail same day.
- 4 (Warm): Start sequence within 24 hours.
- 3 (Standard): Normal cadence.
- 2 (Lower): Fill volume but low conversion.
- 1 (Long shot): Only if batch needs volume.

## Re-Engagement Triggers

After Touch 6 break-up, re-engage ONLY if:

| Trigger | Action |
|---------|--------|
| Buyer Intent reactivates | New sequence with fresh angle |
| New QA job posting at company | New outreach referencing QA hiring |
| Leadership change (new CTO/VP/QA Dir) | Reach out to NEW person |
| Company raises funding | New outreach about scaling QA |
| Company ships major product | New outreach about testing effort |
| Testsigma ships major feature | Re-engage with new capability |

Rules:
- Minimum 60 days between break-up and re-engagement
- Must have NEW reason. Never repeat old sequence.

## Meeting Booked Handoff

Prep card contents:
1. Company snapshot (what they do, size, products, news)
2. Prospect snapshot (title, tenure, responsibilities)
3. Known/likely tech stack
4. Pain hypothesis from outreach
5. What triggered the reply (from reply tag)
6. 3-5 tailored discovery questions
7. 2-3 relevant proof points with numbers
8. Predicted objection + response

Keep it to one screen. Rob reads it in 2 minutes before the call.

## Qualification Checklist

- [ ] Manager+ seniority
- [ ] ICP title match
- [ ] No prior interaction in Sales Navigator
- [ ] US-based (unless specified)
- [ ] Software QA/engineering (not pharma manufacturing, biotech lab QA)
- [ ] Company has software products or digital platforms
- [ ] Profile URL captured and logged

## Common Pitfalls

- Don't send messages. Rob copies/pastes manually.
- Don't use same proof point for every message. Rotate and match to pain.
- Don't use "I noticed" opener for more than ~3 messages in a batch.
- Don't include >2 prospects from same company in one batch.
- Don't include VP Eng at 50K+ companies unless Buyer Intent or QA-specific scope.
- Do prioritize QA-titled leaders over generic VP Eng.
- Do flag Buyer Intent signals prominently.
- Do use specific numbers in proof points.

## Prospect Mix Ratio (per 25-prospect batch)

- 12-15 QA-titled leaders (highest reply rate ~1.0-1.4%)
- 8-10 VP Engineering / VP SE (budget holders, ~0.5-0.8% reply rate)
- 2-3 Buyer Intent prospects (regardless of title, highest priority)
- No more than ~8 from same vertical per batch

## Personalization Scoring (1-3)

| Score | Meaning |
|-------|---------|
| 3 | Deep - References something only THIS person would recognize |
| 2 | Medium - References their company but could apply to anyone in role |
| 1 | Light - Mostly about company/industry, not the person |

## Feedback Loop

- Each batch includes status tracker, reply tags, A/B labels, personalization scores
- Rob updates as he sends and gets replies
- Before next batch, Claude reads all previous data and generates Pre-Brief
- Over time: compound advantage, each batch smarter than the last
- Use `work/reply-log.csv` and `work/results.json` for tracking
