# Outbound Intelligence System (Data-Driven Rules)

Source: Analysis of 1,326 LinkedIn conversations (381 replies, 945 no-replies, 4,786 messages). Data from Rob's BDR tenure at mabl (2021-2023). Patterns transfer directly to Testsigma (same product category, same personas).

## Core Benchmarks
| Metric | Value |
|--------|-------|
| Overall reply rate | 28.7% (381/1,326) |
| Messages per conversation (avg) | 3.0 |
| Avg msgs before first reply | 2.47 (median: 2) |
| Reply after 1 message | 25.3% |
| Reply by message 2 | 53.7% |
| Reply after 3+ messages | 31.1% |
| Same-day reply rate | 17.6% |
| Reply within 1 week | 42.0% |

## Hard Constraints (MUST NEVER violate — auto-rewrite if found)
| # | Constraint | Data |
|---|-----------|------|
| HC1 | No "I noticed" / "I saw" / "I see" | -13.4 pp (10.9% reply vs 24.3% no-reply) |
| HC2 | No leading with AI/ML/self-healing as headline | AI: -9.2 pp. Self-healing: -6.2 pp |
| HC3 | No messages over 120 words | 75-99w = 39.0%. 150+ = 21.2% |
| HC4 | No evening sends (after 6 PM) | 12.1% vs 56.5% lunch |
| HC5 | No bullet-point feature dumps | Bullets: -2.2 pp |
| HC6 | No "would it be unreasonable" as sole CTA | 12.8% rate |
| HC7 | No phone-number asks | 5.0% rate (worst CTA) |
| HC8 | No "reaching out" / "wanted to connect" | -2.4 pp |
| HC9 | No "I figure" / "would you like to share" / "enough about me" | 9.8% / 15.2% / 18.2% rates |
| HC10 | No 3+ question marks per message | 3 Qs: 14.3%. Optimal: exactly 2 (34.8%) |

## Strong Preferences (optimize for)
| # | Preference | Data |
|---|-----------|------|
| SP1 | 75-99 words | 39.0% rate (n=775), +10.3 pp |
| SP2 | Send 12-1 PM local | 56.5% rate (n=423) |
| SP3 | Send on Thursdays | 42.1% rate. Monday worst: 22.9% |
| SP4 | Exactly 2 question marks | 34.8% (n=1,038) |
| SP5 | "What day works?" CTA | 40.4% rate (n=782) |
| SP6 | Stats with specific numbers | 32.8% rate. "40% fewer bugs": 39.2% |
| SP7 | Outcome-framing phrases | "increase testing efficiency": +12.7 pp |
| SP8 | 3+ touches per prospect | 31.1% of replies come after 3+ msgs |
| SP9 | Target Architects + Manager/Leads | 39.3% / 26.8% |
| SP10 | Vary angle across touches | High-performer threads avg 4.9 msgs |

## Timing Matrix
| Time Slot | Reply Rate | Verdict |
|-----------|-----------|---------|
| Lunch (12-1 PM) | 56.5% | BEST — default send time |
| Afternoon (2-5 PM) | 24.0% | Acceptable |
| Evening (6-8 PM) | 12.1% | WORST — never send |

| Day | Reply Rate | Verdict |
|-----|-----------|---------|
| Thursday | 42.1% | BEST |
| Tuesday | 29.6% | Good |
| Friday | 29.6% | Good |
| Wednesday | 28.3% | Average |
| Monday | 22.9% | WORST — avoid Touch 1 |

## Word Count Curve
| Length | Reply Rate | Verdict |
|--------|-----------|---------|
| <50 words | 72.1% | Ultra-short (follow-ups only) |
| 75-99 words | 39.0% | OPTIMAL for Touch 1 |
| 100-124 words | 27.5% | Acceptable |
| 125-149 words | 23.4% | Trim it |
| 150+ words | 21.2% | Never for Touch 1 |

## Toxic Patterns (more in no-replies)
| Pattern | Diff | Impact |
|---------|------|--------|
| "I noticed/I saw" | -13.4 pp | Strongest negative |
| AI/ML mention | -9.2 pp | Features repel |
| Named customer drop | -9.2 pp | Overuse backfires |
| Self-healing mention | -6.2 pp | Technical feature, not pain hook |
| Role reference ("you're the") | -3.1 pp | Visible template |
| Bullet points | -2.2 pp | Feature lists kill engagement |

## Positive Patterns (more in replies)
| Pattern | Diff | Impact |
|---------|------|--------|
| "What day" CTA | +21.4 pp | Strongest positive |
| Direct meeting ask | +18.6 pp | Directness wins |
| Stats with numbers | +6.4 pp | Specific = credible |

## High-Performing Phrases
| Phrase | Reply Rate | vs Baseline |
|--------|-----------|-------------|
| "have you heard of" | 81.8% | +53.1 pp |
| "increase testing efficiency" | 41.4% | +12.7 pp |
| "thought it would be worth" | 41.3% | +12.6 pp |
| "exploring your options" | 39.7% | +10.9 pp |
| "test maintenance" | 37.8% | +9.0 pp |
| "release cycles" | 36.1% | +7.4 pp |

## Toxic Phrases (never use)
| Phrase | Reply Rate | vs Baseline |
|--------|-----------|-------------|
| "I figure" | 9.8% | -19.0 pp |
| "would you like to share" | 15.2% | -13.6 pp |
| "flaky tests" | 16.8% | -11.9 pp |
| "enough about me" | 18.2% | -10.6 pp |
| "CI/CD" | 23.6% | -5.1 pp |
| "low code" | 25.8% | -2.9 pp |

## CTA Rankings
| CTA Style | Reply Rate | Verdict |
|-----------|-----------|---------|
| "Heard of us?" | 52.4% | Best rate, niche use |
| "What day available" | 40.4% | BEST at scale — default |
| Question close (generic) | 14.0% | Underperforms |
| "Would it be unreasonable" | 12.8% | Bad |
| Phone ask | 5.0% | Worst |

## Stat/Claim Performance
| Stat | Reply Rate | Verdict |
|------|-----------|---------|
| "40% fewer bugs" | 39.2% | Best stat |
| Any percentage | 32.8% | Stats help |
| "85% maintenance reduction" | 32.6% | Good but overused |
| "300% test creation speed" | 16.3% | Sounds unbelievable — avoid |

## Persona Reply Rates
| Seniority | Reply Rate | Priority |
|-----------|-----------|----------|
| Architect | 39.3% | HIGH — undervalued |
| Senior IC | 30.0% | MEDIUM |
| Manager/Lead | 26.8% | HIGH — best volume+rate |
| Director | 26.0% | HIGH — has budget |
| VP | 11.9% | LOW |
| C-Level | 9.1% | VERY LOW |

## Message Quality Score (MQS) — 12 Points
4 dimensions, 1-3 each:
1. **Opener Clarity:** 3=insight-driven question, 2=company-specific generic, 1=template-visible
2. **CTA Confidence:** 3="what day works" tied to proof point+prospect, 2=weak tie, 1=generic/open-ended
3. **Personalization Density:** 3=only THIS person recognizes, 2=company-specific, 1=name/title swap
4. **Friction:** 3=80-110w, 1 proof, 1 CTA, 2 Qs, 4+ breaks, ≤1 hyphen. 2=110-120w. 1=120+w or bullets/multi-CTA

Thresholds: 10-12=ready, 7-9=improve, <7=MUST rewrite.

## QA Gate (14 checks — MANDATORY before presenting any batch)
1. Hard Constraint scan (all 10 HCs)
2. MQS score computation (show breakdown)
3. Threshold: MQS >= 9/12
4. Word count: Touch 1 = 80-120w, Follow-ups = 40-70w
5. Question count: exactly 2 for Touch 1
6. Structural dedup: no two messages structurally identical
7. Evidence check: every claim has a research source
8. Angle rotation: no same angle across touches
9. Phrase toxicity scan
10. CTA validation: "what day works" + proof point tie + prospect-specific
11. Hyphen audit: max 1, compound words only
12. Paragraph spacing: 4+ breaks, max 3 sentences per paragraph
13. Close structure dedup: rotate 5 close patterns
14. Research depth: all 3 sources present

## Reply Patterns (for response handling)
| Type | % | Action |
|------|---|--------|
| Polite ("thanks") | 34.5% | Follow up with value |
| Other/misc | 25.0% | Read carefully, respond contextually |
| Negative | 14.5% | Log reason. Re-engage 60+ days |
| Positive | 11.3% | Book meeting immediately |
| Referral | 8.2% | Reach out to referred person same day |
| Has tool | 2.6% | Objection handle: ask about gaps |
| Timing | 2.4% | Set reminder. Re-engage per triggers |
| Curiosity | 0.8% | Answer + proof point + bridge to meeting |
