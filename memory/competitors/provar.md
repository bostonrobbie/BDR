# Provar Battle Card

**Last updated:** 2026-03-03
**Threat level:** Medium (Salesforce-specific niche)
**Category:** Commercial, Salesforce-focused

## What It Is

Provar Automation (formerly Provar Testing) is a Salesforce-native test automation tool. Built specifically for testing Salesforce applications including Lightning, Classic, Visualforce, and CPQ. Uses a Java-based framework under the hood.

## Who Uses It

Salesforce-heavy enterprises and ISVs. Common in financial services, healthcare, and insurance companies with deep Salesforce CRM/CPQ deployments. Typically adopted by teams that have tried Selenium for Salesforce and hit the Shadow DOM wall.

## Where Provar Is Genuinely Strong

- Purpose-built for Salesforce: handles Lightning Web Components, Shadow DOM, dynamic IDs natively
- Strong metadata awareness: understands Salesforce object model, not just DOM elements
- Good Salesforce DevOps integration (Copado, Gearset, AutoRABIT)
- Established Salesforce ecosystem presence (AppExchange, Dreamforce)
- Decent regression suite management for Salesforce-only testing

## Where Provar Falls Short (Our Angle)

### 1. Java-heavy, slow to set up
- Provar requires Java IDE (Eclipse-based) for test creation and maintenance.
- Setup takes weeks, not days. Learning curve is steep for non-developers.
- **Testsigma angle:** 1-day setup vs weeks. Plain English test authoring, no Java knowledge needed.

### 2. No self-healing
- When Salesforce UI changes (every release cycle), Provar tests break and need manual fixes.
- Salesforce ships 3 major releases per year, each one can break locators.
- **Testsigma angle:** AI self-healing auto-fixes broken locators. 90% maintenance reduction.

### 3. Salesforce-only
- Provar only tests Salesforce. If the team also needs to test web apps, mobile, APIs, or other platforms, they need a second tool.
- **Testsigma angle:** Unified platform: web, mobile, API, desktop, Salesforce, SAP. One tool for everything.

### 4. Limited CI/CD integration
- Provar's CI/CD story is weaker than modern tools. Jenkins plugin exists but setup is manual.
- **Testsigma angle:** Native CI/CD integration with Jenkins, CircleCI, GitHub Actions, Azure DevOps. Cloud execution built in.

### 5. Expensive for what you get
- Provar pricing is per-seat, and the Salesforce-only limitation means you're paying full price for partial coverage.
- **Testsigma angle:** More coverage (cross-platform) at comparable or lower cost.

## Displacement Proof Points

| Proof Point | Context |
|-------------|---------|
| 90% maintenance reduction with self-healing | Direct counter to Provar's manual fix burden after SF releases |
| Hansard: regression 8 weeks to 5 weeks | Insurance/financial services context where Provar is common |
| Fortune 100: 3X productivity increase | Enterprise context, Provar's primary market |

## Common Objections When Displacing

| Objection | Response |
|-----------|----------|
| "Provar understands Salesforce metadata" | "We do too. Testsigma has native Salesforce support including Lightning, Shadow DOM, and CPQ. The difference is we also cover your non-Salesforce apps." |
| "We've built our test suite in Provar already" | "Totally fair. Most teams keep Provar for existing Salesforce tests and use Testsigma for new tests and non-SF coverage. Over time, teams find it easier to consolidate." |
| "Our Salesforce team is comfortable with Provar" | "That makes sense. The question is whether the Java dependency and manual maintenance after every SF release is sustainable. Our plain English approach means anyone on the team can contribute." |

## Talk Track (What to Emphasize)

- Lead with **setup speed**: 1 day vs weeks. Provar's Eclipse-based IDE is a barrier.
- Emphasize **cross-platform coverage**: Provar locks you into Salesforce-only. What about the rest of the stack?
- Highlight **Salesforce release cycle pain**: 3 major releases per year = 3 test maintenance sprints per year with Provar. Self-healing eliminates this.
- Don't trash Provar's Salesforce knowledge. Acknowledge it, then expand the conversation to the full test surface.

## Pricing Context

- Provar: Per-seat licensing, Salesforce-only coverage
- Testsigma: Platform pricing, covers web + mobile + API + desktop + Salesforce + SAP
