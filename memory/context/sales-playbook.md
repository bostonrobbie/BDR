# Sales Playbook - Quick Reference

This is the condensed, action-oriented reference for daily outreach. The full SOP lives in CLAUDE.md. This file is for glance-and-go.

## The 3 Pain Hooks (Pick One Per Prospect)

### 1. Maintenance / Flaky Tests
- **The pain:** UI changes break tests. Team spends more time fixing than writing.
- **The question:** "Is test maintenance growing faster than your team can keep up with?"
- **Best proof points:** Hansard (8wk to 5wk), 70% reduction vs Selenium, 90% with self-healing
- **Best for:** Selenium shops, large regression suites, regulated industries

### 2. Velocity / Speed
- **The pain:** Regression takes days. Releases wait on QA. CI/CD pipeline is bottlenecked.
- **The question:** "How long is your regression cycle holding up releases?"
- **Best proof points:** Sanofi (3 days to 80 min), CRED (5x faster), Fortune 100 (3X productivity)
- **Best for:** FinTech, fast-shipping teams, weekly release cadences

### 3. Coverage / Scale
- **The pain:** Coverage is flat while features grow. Team can't keep up. Manual testing persists.
- **The question:** "Is your test coverage keeping pace with how fast the product is shipping?"
- **Best proof points:** Medibuddy (2,500 tests, 50% maintenance cut), Nagra DTV (2,500 in 8 months), Spendflo (50% manual cut)
- **Best for:** Mid-size teams scaling, healthcare, SaaS, teams without dedicated QA headcount

## Proof Point Quick Reference

| Story | Number | Best Vertical | Best Pain |
|-------|--------|--------------|-----------|
| Hansard | 8 weeks to 5 weeks | Insurance, FinServ | Maintenance |
| Medibuddy | 2,500 tests, 50% maintenance cut | Healthcare, mid-size | Coverage |
| CRED | 90% regression, 5x faster | FinTech | Velocity |
| Sanofi | 3 days to 80 minutes | Pharma, healthcare | Velocity |
| Fortune 100 | 3X productivity | Enterprise, VP-level | Productivity |
| Nagra DTV | 2,500 tests in 8 months, 4X faster | Media, API + UI | Coverage |
| Spendflo | 50% manual testing cut | SaaS, small teams | Coverage |
| vs Selenium | 70% maintenance reduction | Any Selenium shop | Maintenance |
| Self-healing | 90% maintenance reduction | Any flaky test pain | Maintenance |

## Persona Playbook

### QA Director / Head of QA (Primary - highest reply rate)
- **They care about:** Coverage metrics, team productivity, headcount leverage, tool consolidation
- **Open with:** Challenge question about coverage or maintenance at scale
- **Proof point style:** Specific numbers, peer company stories
- **CTA:** "Would 15 minutes to compare approaches be useful?"

### VP Engineering (Secondary - lower reply rate)
- **They care about:** Release velocity, developer productivity, total cost, platform strategy
- **Open with:** Business outcome question (release speed, team leverage)
- **Proof point style:** ROI-focused, productivity multiplier
- **CTA:** Tie to strategic initiative, not tactical testing
- **Caution:** At 50K+ employee companies, VP Eng is too far from testing decisions. Skip unless Buyer Intent.

### Senior SDET / Automation Lead (Influencer)
- **They care about:** Technical capability, integration with their stack, not losing their job to "no-code"
- **Open with:** Technical curiosity question about their architecture
- **Proof point style:** Technical depth, capability comparison
- **CTA:** "Worth a technical deep-dive?"
- **Caution:** They can champion or block. Don't threaten their role. Position NLP as expanding what they can cover, not replacing them.

## Objection Quick Reference

| They Say | You Say |
|----------|---------|
| "We already have a tool" | "Totally fair. What gap are you seeing with it?" (Let them tell you the pain.) |
| "No budget" | "One company your size cut manual testing 50% and saw ROI in Q1. Worth a quick look?" |
| "Not a priority right now" | "Makes sense. When does it become one? Happy to reconnect at the right time." |
| "We're happy with Selenium/Cypress/Playwright" | See competitor battle cards in `memory/competitors/`. Use tool-specific response. |
| "Security concerns" | "SOC2/ISO certified. On-prem and private cloud options. Several Fortune 500s run us behind their firewall." |
| "Too early, just started this role" | "A lot of QA leaders in their first 90 days use our trial to benchmark what's possible. No commitment, just data." |
| "Send me more info" | "Happy to. What specifically would be most useful? That way I can send something targeted, not a generic deck." |

## Daily Rhythm

1. **Morning (8-9 AM PT):** Check reply queue. Handle replies within 4 hours.
2. **Morning (9-11 AM PT):** Cold calls. Best connect window.
3. **Midday (11 AM-12 PM PT):** Send InMails and emails. Best open window.
4. **Afternoon (12-3 PM PT):** Research new prospects, build sequences.
5. **Afternoon (3-6 PM PT):** Second cold call window. Follow-up calls.
6. **End of day:** Update statuses, log outcomes, prep tomorrow's queue.

## Message Rules (Non-Negotiable)

- Under 100 words for Touch 1 (target 75-95)
- No em dashes. Ever.
- No "I noticed" / "I saw" / "reaching out"
- No feature-led framing (don't lead with AI/self-healing)
- One proof point per message, matched to their pain
- Question mark in the opener AND the close
- No easy-out lines ("no worries if not")
- Different proof point per touch for the same prospect
