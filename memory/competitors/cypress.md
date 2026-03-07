# Cypress Battle Card

**Last updated:** 2026-02-28
**Threat level:** High (popular with modern dev teams)
**Category:** Open-source (with paid cloud)

## What It Is

JavaScript-based end-to-end testing framework. Runs directly in the browser. Known for developer-friendly API, fast feedback loop, and built-in time travel debugging. Cypress Cloud (paid) adds parallelization, analytics, and CI integration.

## Who Uses It

Modern JavaScript/TypeScript teams. Especially popular with React, Vue, and Next.js shops. Developer-led testing (vs. QA-led). Common in SaaS, startups, and mid-market tech companies.

## Where Cypress Is Genuinely Strong

- Excellent developer experience. Fast, intuitive, great error messages.
- Time travel debugging (snapshots of each step)
- Automatic waiting (reduces flakiness vs. Selenium)
- Strong TypeScript support
- Active community, well-maintained
- Good CI/CD integration

## Where Cypress Falls Short (Our Angle)

### 1. JavaScript only
- Teams must know JS/TS. Non-technical QA can't contribute.
- If the engineering team is Python or Java, Cypress doesn't fit.
- **Testsigma angle:** Plain English NLP. Any team member can write tests regardless of language background.

### 2. Browser limitations
- Historically Chrome-first. Safari support is experimental. Multi-browser testing is still a weak spot.
- Can't test across browsers as reliably as Selenium or Testsigma.
- **Testsigma angle:** True cross-browser, cross-device testing from day one. Web, mobile, API, desktop.

### 3. No mobile testing
- Cypress doesn't support native mobile testing at all. Teams need a separate tool (Appium, Detox) for mobile.
- **Testsigma angle:** Unified platform for web + mobile + API + desktop. One tool, one language.

### 4. Single-tab limitation
- Can't test multi-tab or multi-window scenarios natively. Workarounds exist but they're hacky.
- **Testsigma angle:** No architectural limitations on multi-tab, multi-window, or iframe testing.

### 5. No self-healing
- When the UI changes, Cypress tests break just like Selenium tests. Manual locator updates required.
- **Testsigma angle:** AI self-healing auto-fixes broken locators. 90% reduction in maintenance.

### 6. Scaling costs
- Cypress Cloud parallelization is paid. Costs grow with test volume.
- **Testsigma angle:** Parallel execution included. No per-test-run pricing surprises.

## Displacement Proof Points

| Proof Point | Context |
|-------------|---------|
| 70% maintenance reduction vs Selenium | Applies to Cypress too, same locator fragility problem. |
| CRED: 90% regression automation, 5x faster | FinTech velocity story. Cypress teams relate to speed needs. |
| Medibuddy: 2,500 tests, 50% maintenance cut | Scaling story for teams outgrowing Cypress. |

## Common Objections When Displacing

| Objection | Response |
|-----------|----------|
| "Our devs love Cypress, they won't switch" | "Developers should keep using Cypress for component tests if they love it. The gap is usually at the E2E and integration level, where QA needs to own coverage without waiting on dev bandwidth. Testsigma handles that layer." |
| "Cypress is fast enough for us" | "Speed is one of Cypress's real strengths. The question is whether the team can scale coverage fast enough. When you're shipping weekly and coverage is flat, plain English test creation is the unlock." |
| "We just migrated to Cypress from Selenium" | "Makes sense, that's a common path. Most teams who come to us from Cypress aren't replacing it, they're adding Testsigma for the use cases Cypress can't cover: mobile, cross-browser, API, and letting non-dev team members write tests." |

## Talk Track

- Don't position against the developer experience. Cypress DX is genuinely good. Acknowledge it.
- Lead with the **coverage gap**: Cypress does web well, but what about mobile? API? Cross-browser?
- Emphasize **team leverage**: Cypress requires JS developers. Testsigma lets the whole QA team contribute.
- The "complement" angle works better than "replace" for Cypress shops.

## Pricing Context

- Cypress: Free (open source). Cypress Cloud starts ~$75/mo, scales with parallelization and test volume.
- Testsigma: Competitive at the platform level, especially when replacing Cypress Cloud + Appium + API tool.
