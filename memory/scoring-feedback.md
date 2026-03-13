# Scoring, A/B Testing & Feedback Loops

## Priority Scoring (1-5)
| Factor | Points |
|--------|--------|
| Buyer Intent signal | +2 |
| QA-titled leader (Director/Head/VP of QA) | +1 |
| Top vertical (FinTech, SaaS, Healthcare) | +1 |
| Recently hired (<6 months) | +1 |
| Active digital transformation/migration | +1 |
| Uses known competitor tool | +1 |
| VP Eng at 50K+ (no QA scope) | -1 |

**Tiers:** 5=Hot (first every morning), 4=Warm (within 24hr), 3=Standard (normal cadence), 2=Lower (fill batch), 1=Long shot (only if needed).

## Message Personalization Score (1-3)
| Score | Meaning |
|-------|---------|
| 3 | Deep — only THIS person would recognize it |
| 2 | Medium — company-specific but could be anyone there |
| 1 | Light — mostly company/industry, not the person |

## A/B Testing Rules
Split each batch into 2-3 groups. Test ONE variable per batch:
1. Pain hook (maintenance vs velocity)
2. Proof point style (named vs anonymous)
3. Opener style (career vs company-metric)
4. Ask intensity
5. Message length (70-80 vs 100-120)
6. Email subject (Standard vs SMYKM) — highest priority test
7. Email structure (Standard vs SMYKM challenge-narrative)

Rules: Only ONE variable per batch. Even splits by persona/vertical. Need 3+ batches per variable for conclusions.

## Reply Tagging
| Tag | Meaning |
|-----|---------|
| Opener | Referenced the personalized opener |
| Pain hook | Engaged with the problem hypothesis |
| Proof point | Asked about customer story/numbers |
| Timing | "Good timing" or "we're evaluating" |
| Referral | Forwarded to someone else |
| Not interested | Declined (still data) |
| Unknown | Can't determine trigger |

## Pre-Brief (before each new batch)
Read all previous batch files and generate 5-line summary:
1. **Best persona** — which title replies most
2. **Best proof point** — which story in most replies
3. **Best vertical** — warmest industry
4. **Best pattern** — opener/ask/length standing out
5. **Stop doing** — one thing to drop

## Cycle Logging
Each send session generates a log with: volume, timing, friction events, tools used, safety check, process improvements.

Per-prospect log: pre-flight checks, send data, outcome, next step.

Weekly metrics: sends/week (target 20-25), success rate (>90%), avg time per prospect (<3 min), friction rate (<10%), reply rate (>25% target), meeting rate (>5% target).

## Proof Point Rotation Effectiveness Tracking

Track which proof points are driving replies vs. being ignored. Update this after every batch of 10+ replies comes in.

### Current Tracking (update as reply data accumulates)

| Proof Point | Customer | Key Stat | Times Used | Replies | Reply Rate | Verdict |
|-------------|----------|----------|-----------|---------|-----------|---------|
| Regression speed | Hansard | 8→5 weeks | — | — | — | Pending data |
| Test coverage | CRED | 90% coverage, 5x faster | — | — | — | Pending data |
| Test maintenance | Medibuddy | 2,500 tests, 50% cut | — | — | — | Pending data |
| Enterprise regression | Cisco | 35% time reduction | — | — | — | Pending data |
| Scale coverage | Fortune 100 | 3x coverage in 4 months | — | — | — | Pending data |
| Cross-platform | Samsung | cross-platform coverage | — | — | — | Pending data |
| Healthcare compliance | Oscar Health | compliance-critical coverage | — | — | — | Pending data |
| Retail regression | NTUC Fairprice | retail regression | — | — | — | Pending data |

**How to update:** After each batch, count emails per proof point (`Times Used`). When a reply comes in, check the T1 email in the batch tracker to see which proof point was used. Increment `Replies` for that row. `Reply Rate = Replies / Times Used`.

**Why this matters:** If CRED drives 3x more replies than Hansard per send, CRED should lead T1s for high-priority accounts. This converts proof point rotation from a fairness rule into a performance lever.

### Vertical Best-Fit (update from reply data — current best guess)

| Vertical | Best Proof Point | Second Choice | Rationale |
|----------|-----------------|---------------|-----------|
| FinTech / Financial Services | Hansard | CRED | Insurance/FS regression cycles resonate |
| HealthTech / Healthcare | Medibuddy | Oscar Health | Test scale + compliance |
| SaaS / Tech | CRED | Cisco | Speed + coverage framing |
| Enterprise (>10K employees) | Fortune 100 | Cisco | Enterprise scale proof |
| Retail / E-Commerce | NTUC Fairprice | CRED | Retail regression cycles |
| Telecom | Nokia (if available) | Samsung | Hardware/platform depth |

---

## Meeting Booked Handoff
When status = Meeting Booked, auto-generate prep card:
1. Company snapshot
2. Prospect snapshot
3. Known/likely tech stack
4. Pain hypothesis
5. What triggered the reply (from reply tag)
6. Suggested discovery questions (3-5, tailored)
7. Relevant proof points (2-3, matched)
8. Predicted objections + responses

Keep to one screen. Include "Copy Prep" button.
