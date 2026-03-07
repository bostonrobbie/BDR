# mabl Battle Card

**Last updated:** 2026-02-28
**Threat level:** Medium (closest AI positioning)
**Category:** AI-native commercial

## What It Is

AI-powered test automation platform. Low-code test creation with auto-healing, visual regression, and performance testing. Cloud-native SaaS. Founded 2017 by ex-Google engineers. Raised $40M total. Acquired by Tricentis in 2024.

## Who Uses It

Mid-market SaaS and e-commerce companies. Teams that want AI-powered testing without heavy coding. Popular with teams that have limited QA headcount. Now part of the Tricentis portfolio (cross-sell and up-sell from TOSCA).

## Where mabl Is Genuinely Strong

- Good auto-healing (locator fallbacks, visual healing)
- Low-code test creation (trainer/recorder based)
- Built-in visual regression testing
- Built-in API testing
- Performance testing included
- Good CI/CD integration
- Clean, modern UI

## Where mabl Falls Short (Our Angle)

### 1. Web-only
- mabl does not support native mobile testing. Web and API only.
- **Testsigma angle:** Unified platform: web + native mobile + API + desktop + SAP + Salesforce.

### 2. Limited test logic
- mabl's low-code approach struggles with complex conditional flows, data-driven testing, and custom assertions.
- Teams hit a ceiling when tests get sophisticated.
- **Testsigma angle:** NLP handles complex scenarios naturally. "If the cart total exceeds $500, apply the enterprise discount" just works.

### 3. No plain English
- mabl uses a visual trainer/recorder, not natural language. Still requires understanding the tool's UI paradigm.
- **Testsigma angle:** Write tests in actual plain English sentences. No tool-specific paradigm to learn.

### 4. Tricentis acquisition uncertainty
- Acquired by Tricentis in 2024. Product roadmap may shift toward Tricentis enterprise priorities.
- Pricing may increase as Tricentis integrates it into their enterprise bundle.
- **Testsigma angle:** Independent, focused platform. Product roadmap driven by testing practitioners, not enterprise portfolio strategy.

### 5. Self-healing is good but not agentic
- mabl's auto-healing is locator-based fallback. Good for simple changes.
- Doesn't understand test intent. Can't handle major UI restructuring.
- **Testsigma angle:** Atto's intent-based healing understands WHAT the test is trying to do, not just WHERE the element was.

### 6. Limited scale proof points
- mabl's customer base is mostly mid-market. Fewer enterprise reference customers.
- **Testsigma angle:** Cisco, Samsung, Honeywell, Bosch, Nokia, Nestle at scale. Enterprise-proven.

## Displacement Proof Points

| Proof Point | Context |
|-------------|---------|
| Medibuddy: 2,500 tests, 50% maintenance cut | Mid-market scaling story, mabl's core market. |
| CRED: 90% regression automation, 5x faster | High-velocity team needing more than low-code. |
| Spendflo: 50% manual testing cut | SaaS quick-win, competes directly with mabl's pitch. |

## Common Objections When Displacing

| Objection | Response |
|-----------|----------|
| "mabl has AI too, what's different?" | "mabl's AI is great for auto-healing simple locator changes. Where it stops is test generation and intent understanding. Testsigma's Atto agents can generate tests from a Jira ticket, plan sprint coverage, and heal tests by understanding what they're trying to accomplish, not just where elements are on the page." |
| "We like the visual regression feature" | "Visual regression is genuinely useful. Testsigma supports visual testing too. The difference is Testsigma also handles the 90% of testing that isn't visual: functional flows, API validation, mobile apps, data-driven scenarios." |
| "mabl was easier to get started with" | "mabl's recorder makes the first 10 tests easy. The question is the next 500. When you need complex data flows, conditional logic, and cross-platform coverage, that's where NLP scales better than a visual trainer." |

## Talk Track

- mabl is the most direct competitor in AI positioning. Differentiate on **depth of AI** and **platform breadth**.
- Lead with **mobile gap**: if they have mobile apps, mabl can't help.
- Lead with **scale ceiling**: mabl's low-code hits limits. NLP doesn't.
- The **Tricentis acquisition** is a useful wedge. "How's the mabl roadmap looking post-acquisition?" Plants doubt without trashing.
- Don't compete on auto-healing alone. mabl's is decent. Win on the full AI agent story (Atto).

## Pricing Context

- mabl: Starts ~$200/mo. Enterprise tiers are higher, pricing may shift under Tricentis.
- Testsigma: Competitive at every tier. Broader platform coverage for similar price point.
