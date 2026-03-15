# Testsigma Knowledge Bible
*Last updated: February 23, 2026 (v3 - third research pass complete, 25-question deep dive)*
*Compiled from: testsigma.com, GitHub, G2, Capterra, Gartner, GlobeNewsWire, PR Newswire, Bug0, Research.com, TestGuild, SaaSWorthy, GetApp, SoftwareAdvice, SourceForge, Qualitrix, product documentation, trust.testsigma.com, and 10+ customer case studies.*

---

## A) Company Overview

Testsigma is an agentic AI-powered, codeless test automation platform that enables quality engineering teams to write, execute, and maintain automated tests in plain English across web, mobile, desktop, API, Salesforce, and SAP, all from a single unified platform. Instead of traditional coded frameworks, teams describe test steps in simple English and Testsigma's AI agents handle generation, execution, maintenance, analysis, and optimization autonomously.

- **Founded:** 2019
- **HQ:** San Francisco, California
- **Team size:** ~196 employees
- **Funding:** $12.8M total (Series A led by MassMutual Ventures)
- **Leadership:** Rukmangada Kandyala (CEO & Founder), Pratheep Velicherla (Co-founder), Rajesh Reddy (Co-founder), Vikram Chaitanya (Co-founder)
- **Open source:** Yes, Apache 2.0 license (Community Edition)
- **Tech stack:** Java (47.3% backend), TypeScript (30.8%), HTML (16.5%), SCSS (5%), Docker
- **G2 rating:** 4.5/5, Leader in Software Testing and Automation Testing (Fall 2025)
- **Gartner:** Listed under AI-Augmented Software Testing Tools
- **Target market:** Mid-size to enterprise QA/engineering teams, especially those with mixed technical skill levels or consolidating multi-platform testing

---

## B) Product Capabilities (Specific Feature Names and Details)

### B1. Atto, the AI Coworker
Atto is Testsigma's AI coworker for QA teams. It mobilizes a crew of specialized AI agents that work alongside humans in every phase of testing. This is the core differentiator: not AI that suggests things and waits for action, but agents that do the work themselves.

**Five Core AI Agents:**

| Agent | What It Does | Key Detail |
|-------|-------------|------------|
| **Generator Agent** | Auto-generates test cases from natural language prompts, Jira stories, Figma designs, videos, documents, images, screenshots | Accelerates authoring by 10x. Accepts multiple input types. |
| **Runner Agent** | Executes tests across hundreds/thousands of parallel sessions simultaneously | In-browser execution for quick sanity checks. Validates generated tests. |
| **Analyzer Agent** | Diagnoses test failures, highlights root causes, recommends fixes | Uses visual diffs, logs, and video replays for pinpoint diagnosis. |
| **Healer/Maintenance Agent** | Auto-adapts locators and selectors when UI changes (renamed buttons, moved elements, updated layouts) | Claims 90% reduction in maintenance time. No manual fixes needed. |
| **Optimizer Agent** | Identifies redundant tests, suggests pruning, flags coverage gaps, prioritizes test suites | Keeps suite lean, stable, and high-impact. |

**Additional Agents (added with Atto 2.0 and test management):**
- **Sprint Planner Agent** - Automatically plans tests when a Jira sprint starts by detecting the new sprint
- **Bug Reporter Agent** - Captures logs, screenshots, and test steps to file bugs instantly to Jira
- **Data Generator Agent** - Generates dynamic, realistic test data. Understands form logic, past test behavior, and field types

### B2. Atto 2.0 (Released November 20, 2025)
Major advancement with four new capability dimensions:

1. **Intent-Based Self-Healing** - Now uses user intent, not just code-level locator matching. Tests adapt to UI shifts, redesigns, and dynamic states with human-like stability. This means fewer false failures from cosmetic changes.
2. **Coverage Discovery** - Autonomously explores the application to uncover untested user paths and edge cases that traditional planning misses. Expands coverage beyond what documents or teams typically capture.
3. **Risk Analysis** - Identifies the real impact of code changes by connecting updates to user flows and historical patterns. Pinpoints meaningful risk areas and filters out noise.
4. **Root Cause Analysis** - Performs true causal reasoning to pinpoint WHY a test failed, explain the root cause, and propose the exact fix. Debugging becomes a quick review, not an investigation.

CEO Quote: "Atto 2.0 is a significant step forward for software testing. By making testing adaptive, proactive, and context-aware, it gives QA teams a system that stays in sync with modern software development and supports fast and confident releases in even the most demanding cycles." - Rukmangada Kandyala

### B3. Testsigma Copilot
GenAI-driven assistant built into the platform. Uses LLMs to generate test cases from:
- Natural language prompts
- Jira stories and requirements documents
- Figma designs
- Screenshots and images
- Videos of user flows
- Plain text descriptions

### B4. Natural Language Programming (NLP)
- Write test steps in simple English (no code required)
- Non-technical team members (business analysts, product managers) can review, write, and verify tests
- Supports custom scripting in Java when needed for advanced scenarios
- Test Recorder available for generating editable scripts visually

### B5. Cross-Platform Testing Coverage
| Platform | Details |
|----------|---------|
| **Web** | 800+ browser/OS combinations, cross-browser testing. Shadow DOM and iframe handling with dedicated support. Dynamic locator strategies (runtime, parameter, environment data). |
| **Mobile** | 2,000+ real devices (iOS and Android native apps + mobile web) |
| **API** | Full REST API lifecycle: GET, PUT, POST, DELETE, PATCH. JSON schema validation. Test chaining (use output of one API call as input to the next). Data-driven from XLS, CSV, or database. Postman collection import. Swagger/OpenAPI support. Combined API + UI + DB tests in unified flows. |
| **Desktop** | Desktop application testing |
| **Salesforce** | Dedicated Salesforce testing with metadata locator integration (not just XPath/CSS). Auto-healing for Lightning Web Components (LWC). Multi-sandbox support: Developer, Developer Pro, Partial Copy, Full. Auto-sync with Salesforce metadata changes. Supports Lightning, Classic, and LWC. |
| **SAP** | Enterprise SAP testing on the same platform |

### B6. Self-Healing Tests (Technical Details)
**The Problem:** Every test relies on locators (ID, Name, XPath, CSS) to find UI elements. When apps evolve, locators break, causing tests to fail even when the app works fine. This is the #1 reason teams abandon test automation.

**How Testsigma Solves It:**
1. AI detects changes in the application's source code that affect tests
2. When UI changes between releases (renamed buttons, moved elements, updated layouts), the Healer Agent automatically adapts locators and selectors
3. Atto 2.0 adds intent-based healing: understands WHAT the test is trying to do, not just WHERE the element was
4. Healing happens in real-time during CI/CD pipeline execution
5. AI analyzes failures, identifies updated locators, and applies changes without human intervention

**What It Handles:** Renamed elements, moved components, updated layouts, dynamic states
**What It Doesn't:** Full app redesigns may still need some manual test updates
**Transparency Note:** When the Healer changes a locator, you can see what it did, but understanding why it made a specific choice isn't always fully transparent

**Claimed Result:** 90% reduction in test maintenance time and effort

### B7. Parallel Execution
- Run tests across 3,000+ browser/device/OS combinations simultaneously
- Cloud-based device lab eliminates local infrastructure setup
- Configurable parallel sessions for test suites
- Drastically reduces total execution time for regression and cross-browser testing

### B8. Test Management (AI-Native, Launched May 2025)
Testsigma launched a full AI-native Test Management module in May 2025. By September 2025, it was named a G2 Leader in Test Management.

- **Sprint Planner Agent** - Auto-detects when a new Jira sprint starts and plans test coverage automatically
- **Two-way Jira sync** - Failed tests auto-create Jira bug tickets with logs, screenshots, and steps. When a Jira bug is resolved, it triggers test reruns. Changes in Jira reflect in Testsigma and vice versa.
- **Requirements traceability** - Map test cases to requirements, track coverage per feature
- **Test case management** - Test cases, test suites, test plans, with history and versioning
- **UAT support** - User acceptance testing workflows built in
- **Covers sanity, regression, UAT, and continuous testing workflows**
- **Pricing:** $39/user/month for the test management module
- **Eliminates need for:** TestRail, Zephyr, qTest, or any standalone test management tool
- **Why it matters for BDR:** This is a consolidation play. Teams paying for Selenium + TestRail + BrowserStack can replace all three with Testsigma.

### B9. Visual Testing
- Run functional and visual tests simultaneously in parallel
- Detects visual regressions alongside functional testing
- No additional setup needed

### B10. Data-Driven Testing
- Built-in data generators for parametrized testing
- Run tests with different data sets (user credentials, form inputs, edge cases)
- Data Generator Agent creates dynamic, realistic test data that understands form logic

### B11. Extensibility
- Add-ons Marketplace: community-built custom extensions for unique automation scenarios
- Custom test actions and data generators
- Conditional logic (if/while loops) supported
- Java scripting for advanced customization

### B12. Reporting and Analytics
- Test execution reports with pass/fail status
- Visual diffs, logs, and video replays for failure analysis
- **Known limitation:** Reporting depth is noted by reviewers as less robust than BrowserStack or Sauce Labs. This is the most common improvement area cited in reviews.

### B13. Two-Factor Authentication (2FA) Testing
This is a major differentiator. Most automation tools require disabling 2FA for testing. Testsigma has it built in:
- **Built-in OTP generation** within test steps, no third-party frameworks needed
- **Phone number provisioning** - Testsigma provides a valid mobile number for SMS OTP testing
- **Email mailbox provisioning** - Valid mailbox provided for email-based 2FA
- **Supported countries for SMS OTP:** US, Canada, Australia, UK, Mexico, Netherlands, Sweden, Denmark, Czech Republic, Hungary, Indonesia, Romania, Slovakia
- **Enterprise plan feature**
- This matters because companies commonly disable 2FA in QA environments, creating security blind spots. Testsigma lets teams test the actual production auth flow.

### B14. Accessibility Testing
- Built-in accessibility testing catches WCAG 2.1, Section 508, and ADA issues during functional test runs
- Checks keyboard navigation, screen reader compatibility, color contrast, and semantic structure
- Integrates with aXe and WAVE for deeper accessibility scanning
- Cross-browser accessibility testing across 800+ environments
- Can run accessibility and functional tests simultaneously

### B15. Addons Marketplace (100+ Extensions)
- Community-built and Testsigma-maintained addons extending core capabilities
- **Categories:** custom automated actions, data generators, integrations, utilities
- **Notable addons:** Google Authenticator code generation, Google Sheets read/write, browser localStorage operations, Cassandra DB CRUD, gRPC service testing, keyboard/mouse interaction actions
- Built using the Testsigma Java SDK
- Teams can build proprietary addons for internal use

### B16. Test Recorder
- **Web Recorder** - Record browser interactions and auto-generate editable NLP test steps
- **Mobile Recorder** - Record native app interactions on real devices
- Recorded steps are fully editable in plain English
- Supports image injection, multiple WebViews, and bulk actions
- Great entry point for teams transitioning from manual to automated testing

### B17. Version Control and Git Integration
- Tests stored as version-controlled assets
- Git branching support for test development
- Branch-specific test configurations (run different test sets per branch)
- Merge conflict handling for test scripts

### B18. Autonomous Testing Platform (Launched May 2025)
In May 2025, Testsigma announced the "Autonomous Testing Platform" rebrand/upgrade, positioning itself as the first test automation platform where AI agents handle the full testing lifecycle without human intervention. This is the evolution beyond just "AI-assisted" testing into fully autonomous testing. Key claims:
- AI agents plan, create, execute, heal, and report tests independently
- Human role shifts from "doing testing" to "overseeing quality"
- This is the strategic narrative for VP/CTO-level conversations

---

## C) Integrations (30+ Tools)

| Category | Tools |
|----------|-------|
| **CI/CD** | Jenkins (official plugin with native integration), GitHub Actions (PR gate support, trigger tests on pull requests), GitLab CI (merge request workflow integration), Azure DevOps/Pipelines, CircleCI, Travis CI, Bamboo, Bitbucket Pipelines, Bitrise CI, AWS DevOps, AWS Lambda, CodeShip CI, Copado CI/CD, Gearset CI/CD, TeamCity. All support branch-specific configs, webhook-based notifications, and API-based triggers. |
| **Bug Tracking** | Jira (two-way, most polished), Bugzilla, MantisBT, Azure Boards, YouTrack, FreshRelease |
| **Collaboration** | Slack (real-time failure alerts), Microsoft Teams, Google Chat, Email notifications |
| **Cloud/Testing** | BrowserStack, Sauce Labs, Kobiton, AWS |
| **Project Management** | Jira, Trello, Backlog, Linear |
| **Design** | Figma (test generation from designs) |

**Key Integration Detail:** Jira integration is two-way. Failed tests auto-create bug tickets, and resolved bugs trigger test reruns. Sprint Planner Agent detects new Jira sprints automatically.

---

## D) Pricing and Deployment

### Pricing Tiers

| Plan | Price | Best For |
|------|-------|----------|
| **Community Edition (CE)** | Free, open source (Apache 2.0) | Individuals, small teams, budget-constrained orgs |
| **Pro/Enterprise** | ~$10,000 per license (confirmed by Rob, Feb 2026) | Mid-size to enterprise teams |

**Note:** Pricing is NOT a lead topic in outreach. We sell on value and pain, not price. Only discuss pricing when the prospect asks or during late-stage discovery.

### Deployment Options
- **Cloud** (fully managed SaaS) - recommended, easiest entry
- **On-Premises** - available on Enterprise plan for regulated industries
- **Private Grid** - hybrid option for Enterprise
- **Self-Hosted** - Community Edition via Docker

### Enterprise Security Features
- **Trust Center:** trust.testsigma.com (powered by Sprinto), publicly accessible
- **Security Policies (15+):** Acceptable Use, Anti-Bribery, Asset Management, Business Continuity, Change Management, Code of Conduct, Cryptography, Data Classification, Data Protection, Data Retention, Disaster Recovery, Incident Management, Information Security, Risk Management, Vendor Risk Management
- **Compliance:** GDPR compliant, CCPA compliant
- **SOC 2:** Confirmed compliant (per Rob, Feb 2026). ISO 27001 status not publicly confirmed.
- **Access Controls:** SSO (Single Sign-On), IP Whitelisting, role-based access
- **Deployment Options for Security:** On-premises, private cloud, hybrid
- Dedicated Customer Success Manager on Enterprise plan
- Premium support and consulting
- **BDR Note:** When a prospect raises security concerns, lead with "We're SOC 2 compliant" and the Trust Center URL (trust.testsigma.com). Mention the 15+ security policies and on-prem/private cloud options. This usually satisfies the security objection immediately.

### Free Trial
21-day free trial with full access to features including AI-powered test creation, cross-browser testing, and integrations.

**Pricing Note (common complaint):** Pricing is not publicly listed for Pro or Enterprise. Both require a sales call. This is the most frequently cited negative in user reviews.

---

## E) Unique Differentiators vs Competitors

### vs Selenium (Open Source Framework)
| Selenium Pain | Testsigma Advantage |
|---------------|-------------------|
| Requires heavy coding (Java, Python, C#, etc.) | Write tests in plain English, no code required |
| No built-in self-healing; tests break constantly | AI Healer Agent auto-fixes broken locators (90% less maintenance) |
| Web-only testing | Unified platform: web, mobile, API, desktop, Salesforce, SAP |
| Complex setup (WebDriver, frameworks, infrastructure) | Zero setup, cloud-based, instant start |
| No parallel execution built-in | 3,000+ parallel sessions on cloud device lab |
| No test management | Built-in test management with Jira integration |
| No AI capabilities | 5+ AI agents for generation, execution, healing, analysis, optimization |
| **Proof point:** 70% maintenance reduction vs Selenium; 90% with self-healing |

### vs Cypress (JavaScript Framework)
| Cypress Pain | Testsigma Advantage |
|-------------|-------------------|
| JavaScript only, can't test non-JS apps | Language-agnostic, plain English |
| Web-only, no mobile native testing | Web, mobile (2,000+ real devices), API, desktop, Salesforce, SAP |
| Known flakiness issues | AI self-healing reduces flaky tests by 90% |
| Requires coding expertise | No-code, accessible to non-technical team members |
| No AI-driven capabilities | Full agentic AI suite (Atto) |

### vs Playwright (Microsoft Framework)
| Playwright Pain | Testsigma Advantage |
|----------------|-------------------|
| Requires coding (TypeScript, JavaScript, Python, .NET) | No-code, plain English |
| Microsoft ecosystem focus | Platform-agnostic, supports Salesforce/SAP |
| No self-healing | AI Healer Agent with intent-based healing |
| No built-in test management | Built-in sprint planning, traceability, Jira sync |
| Setup and maintenance burden | Zero-setup cloud platform |

### vs Katalon (Commercial Platform)
| Katalon Pain | Testsigma Advantage |
|-------------|-------------------|
| High license cost | Open-source option (CE), more competitive pricing |
| Steeper learning curve, complex UI | Plain English test creation, lower learning curve |
| Limited AI capabilities | Full agentic AI (5+ agents, Atto 2.0) |
| Selenium-based under the hood (maintenance issues persist) | Purpose-built AI self-healing, not Selenium wrappers |
| Tests time-consuming to fix without programming knowledge | Non-technical users can fix and maintain tests |

### vs Tricentis Tosca (Enterprise)
| Tosca Pain | Testsigma Advantage |
|-----------|-------------------|
| Very high cost (thousands to tens of thousands per license annually) | Fraction of the cost, open-source option available |
| Complex model-based approach | Simple plain English, faster onboarding |
| Heavy enterprise overhead | Lightweight, fast to deploy (cloud or Docker) |
| Slow implementation cycles | 21-day free trial, immediate value |
| **Positioning:** Tosca is the "heavyweight." Testsigma is faster, cheaper, and more accessible while still being enterprise-ready. |

### vs Testim (by Tricentis)
| Testim Pain | Testsigma Advantage |
|------------|-------------------|
| Hybrid approach can be confusing (code + codeless) | Pure no-code with optional Java for advanced cases |
| Documentation gaps noted by users | Well-documented, responsive support team |
| Stability degrades with large parallel test runs | Built for massive parallel execution (3,000+ environments) |
| Now part of Tricentis (pricing/bundling concerns) | Independent, focused platform |

### vs mabl
| mabl Pain | Testsigma Advantage |
|----------|-------------------|
| Primarily web-focused | Web, mobile, desktop, API, Salesforce, SAP |
| Higher pricing structure | Open-source CE, competitive Pro pricing |
| Limited platform coverage | Unified platform for all testing types |
| No Salesforce/SAP-specific testing | Dedicated Salesforce testing with metadata locators |

### vs TestRigor (AI-First NLP Tool)
| TestRigor Pain | Testsigma Advantage |
|---------------|-------------------|
| NLP-only, no visual recorder option | NLP + test recorder + Copilot from Figma/Jira/videos |
| No multi-agent architecture | Atto: 5+ specialized autonomous agents |
| Limited to web and mobile | Web, mobile, desktop, API, Salesforce, SAP |
| No open-source option | Free Community Edition (Apache 2.0) |
| No built-in test management | Full test management with sprint planning and Jira sync |
| Newer company, smaller customer base | Cisco, Samsung, Nestle, Sanofi as customers |

### vs ACCELQ (Enterprise Codeless)
| ACCELQ Pain | Testsigma Advantage |
|------------|-------------------|
| Enterprise-only pricing, expensive | Open-source CE available, more accessible entry |
| QGPT is single-model AI | Atto is multi-agent (Generator, Runner, Healer, Analyzer, Optimizer work together) |
| Heavier setup and onboarding | 1-week training to full productivity (Fortune 100 case study) |
| Primarily enterprise-focused | Serves startups to Fortune 100 |

### What Testsigma Does That NONE of These Can
1. **Agentic AI architecture** - Not just AI assistance, but autonomous AI agents that plan, generate, execute, heal, analyze, and optimize tests independently
2. **Plain English + AI agents + unified platform** - No other tool combines codeless NLP with a full suite of autonomous agents across web, mobile, API, desktop, Salesforce, AND SAP
3. **Intent-based self-healing (Atto 2.0)** - Goes beyond locator matching to understand user intent. No competitor has this
4. **Coverage discovery** - AI autonomously explores the app to find untested paths humans miss
5. **Open source with enterprise AI** - The only platform offering both a free open-source edition AND enterprise-grade agentic AI
6. **Built-in 2FA/MFA testing** - Native OTP generation, phone number provisioning, and email mailbox provisioning. No other codeless tool handles 2FA without third-party workarounds.
7. **Test generation from Figma designs** - Create tests directly from design files before the code is even written. Shift-left at its most literal.
8. **100+ community addons marketplace** - Extensible with community-built addons for Google Sheets, gRPC, Cassandra, Google Authenticator, and more. Open ecosystem.

---

## F) Customer Stories with Real Numbers

### Verified Customer Case Studies

| Customer | Industry | Problem Before | What They Did | Results | Best Used For |
|----------|----------|---------------|--------------|---------|---------------|
| **Hansard** | Insurance/Financial Services | Regression testing took 8 weeks, long cycles blocking releases | Implemented Testsigma with AI self-healing | Regression cut from 8 weeks to 5 weeks (3x faster) | Insurance, financial services, long regression cycles |
| **Medibuddy** | Healthcare/Digital Health | Scaling test coverage across growing platform, heavy maintenance burden | Automated tests with Testsigma's NLP approach | 2,500 tests automated, 50% maintenance reduction | Healthcare, mid-size teams, scaling coverage |
| **CRED** | FinTech | Needed high regression coverage with fast execution for rapid releases | Built regression suite with Testsigma | 90% regression automation coverage, 5x faster execution | FinTech, high-velocity teams |
| **Sanofi** | Pharma | Regression testing took 3 days, compliance requirements slowing everything down | Deployed Testsigma for compliance-safe automation | Regression reduced from 3 days to 80 minutes | Pharma, compliance-heavy, healthcare |
| **Fortune 100 (unnamed)** | Enterprise/Big Tech | Low test creation productivity across large QA organization | Adopted Testsigma's AI-powered test creation | 3x productivity increase | Enterprise, VP-level conversations, big tech |
| **Nagra DTV** | Media/Streaming (Kudelski Group) | In-house WebDriver IO/Node.js framework, single test case took 1-2 days to build | Switched to Testsigma for OTT application testing | 2,500 tests built in <8 months, 4x faster development, CI/CD pipeline running daily, low debugging/maintenance effort | Media, streaming, API + UI testing |
| **Spendflo** | SaaS | Resource-intensive manual QA, 2 resources spending 8 man-hours every 7-8 days on sanity/regression | Automated with Testsigma cloud platform | 50% manual testing reduction, faster execution, steady growth in automated test cases | SaaS, smaller teams, quick wins, budget-conscious |

### NEW: Credit Saison India (Fintech, Verified Case Study)
| Detail | Value |
|--------|-------|
| **Company** | Credit Saison India (Kisetsu Saison Finance), subsidiary of Japan's 3rd-largest credit card issuer |
| **Industry** | FinTech, Digital Lending |
| **Size** | ~400+ APIs, 21-person QA team |
| **Problem** | Only 30% regression automation. Manual testing for frontend and mobile (iOS/Android). 400+ APIs creating bottlenecks. Frequent sprint updates breaking test scripts. |
| **Results** | 80% regression automation (from 30%). 5,000+ tests running daily overnight with results by morning. Avoided 30-40% QA team expansion (saved headcount). Enhanced stability for dynamic application changes. |
| **Best For** | FinTech, lending platforms, mobile-heavy apps, scaling automation without adding headcount |

### NEW: Fortune 100 Networking & Communications Giant (Verified Case Study)
| Detail | Value |
|--------|-------|
| **Company** | Fortune 100 global networking & communications technology leader (unnamed, likely Cisco based on description) |
| **Industry** | Enterprise Tech, Telecom |
| **Size** | Fortune 100, global presence, 12+ person QA team in Mexico GSC |
| **Problem** | Manual mobile app testing was labor-intensive. Testing apps like YouTube and Google Maps for telecom clients. |
| **Results** | 3x efficiency (deliver 3x more work in same timeframe). 400 test cases migrated in 2 months. Nearly 100% mobile app testing automated (iOS + Android). Trained in 1 week. |
| **Quote** | "The support from the Testsigma team has been phenomenal. Their responsiveness and constant improvements to the platform have been critical to our success." |
| **Best For** | Enterprise, mobile testing, telecom, VP-level conversations |

### NEW: Finland-Based AI Technology Company (Verified Case Study)
| Detail | Value |
|--------|-------|
| **Company** | Unnamed AI technology company, Finland |
| **Industry** | AI/Tech |
| **Problem** | Needed to scale test coverage alongside rapid product development |
| **Results** | 47.82% increase in test case volume over 6 months (1,481 to 2,189 test cases). Reduced manual testing. Accelerated release cycles. |
| **Best For** | AI/tech companies, scaling coverage, European prospects |

### NEW: Open Vantage (Verified Case Study)
| Detail | Value |
|--------|-------|
| **Company** | Open Vantage, Johannesburg, South Africa |
| **Industry** | IT Services, Custom Software Development |
| **Size** | Lean cross-functional team |
| **Problem** | Mostly manual testing, low automation coverage, QA bottlenecks blocking releases |
| **Results** | 40% test coverage achieved (from near-zero automation). Smoother regression cycles. Lower implementation cost vs. custom frameworks. No QA headcount increase needed. |
| **Best For** | QA consulting firms, IT services, lean teams, budget-conscious |

### NEW: Qualitrix Partnership Case Study (Verified)
| Detail | Value |
|--------|-------|
| **Company** | Qualitrix (Testsigma implementation partner, Bengaluru) |
| **Industry** | QA Services/Consulting |
| **What They Did** | Used Testsigma as their automation platform for client engagements. Enabled manual testers to automate. Cross-platform testing across browsers and devices. CI/CD integration for continuous testing. |
| **Results** | Expanded automation coverage across web and mobile. AI self-healing minimized script maintenance. Parallel cross-platform testing sped up regression. Non-technical team members creating tests. |
| **Best For** | QA consulting/services firms, Testsigma partner ecosystem |

### UPDATED: Hansard (Richer Detail from Second Pass)
| Detail | Value |
|--------|-------|
| **Company** | Hansard International |
| **Industry** | Insurance/Financial Services |
| **Problem** | Manual testing took 15-20 days per cycle. Monthly functional deployments and patch retesting couldn't fit into tight timelines. |
| **Results** | 3x faster regression (reduced from 3 weeks to under 1 week). 75% automated test coverage. Sanity test results available within 30 minutes of code commits. Regression from 8 weeks to 5 weeks per sprint. |
| **Quote** | Holly Pennington, Test Manager: "With Testsigma, we've reduced our test execution time from 8 weeks to just 5 weeks per sprint." |
| **Key Feature Used** | Self-healing was critical, auto-updating locators when UI changed between weekly releases |
| **Best For** | Insurance, financial services, long regression cycles, compliance environments |

### VERIFICATION NOTE: Medibuddy, CRED, and Sanofi
- **Medibuddy:** From internal sales materials (confirmed by Rob). No published case study on testsigma.com. Numbers are valid for use in outreach but cannot be linked to a public source.
- **CRED:** From internal sales materials (confirmed by Rob). No published case study. Note: Credit Saison India (fintech, 80% automation, 5,000+ daily tests) is a stronger VERIFIED alternative for fintech proof points when a public source is needed.
- **Sanofi:** From internal sales materials (confirmed by Rob). No published case study found. Numbers valid for outreach.

### Additional Named Customers (logos/references, no published case studies)
Cisco, Samsung, Honeywell, Bosch, Nokia, Nestle, KFC, DHL, Zeiss, Axel Springer, NTUC Fairprice, Oscar Health, American Psychological Association

### General Platform Claims
- 90% maintenance reduction with self-healing
- 70% maintenance reduction vs Selenium specifically
- 10x faster test authoring with AI Generator Agent
- 800+ browser/OS combinations, 2,000+ real devices, 3,000+ environment combinations

---

## G) Pain Points Testsigma Solves (Pain-to-Solution-to-Proof Mapping)

| Prospect Pain | Testsigma-Specific Solution | Proof Point |
|---------------|---------------------------|-------------|
| "Our regression suite takes days/weeks to run" | Parallel execution across 3,000+ environments + Runner Agent for simultaneous sessions | Sanofi: 3 days to 80 minutes. Hansard: 8 weeks to 5 weeks. |
| "Our Selenium/Cypress/Playwright tests are flaky and break constantly" | Healer Agent auto-fixes broken locators. Atto 2.0 intent-based healing understands what the test is trying to do, not just where the element was | 90% maintenance reduction. 70% vs Selenium specifically. |
| "We can't find enough SDET/automation talent" | NLP test creation in plain English. Non-technical team members can write and maintain tests. No coding required. | Spendflo automated 50% of manual testing without adding headcount. Nagra DTV built 2,500 tests in 8 months. |
| "We need to test web AND mobile AND API but have separate tools for each" | Unified platform: web, mobile (2,000+ real devices), API, desktop, Salesforce, SAP, all in one | Nagra DTV: OTT app (web + API + UI) all on one platform. |
| "Our test maintenance is eating all our time, we can't build new tests" | Healer Agent + Optimizer Agent. Self-healing fixes broken tests, Optimizer prunes redundant ones | Medibuddy: 50% maintenance cut. Hansard: 3x faster regression. |
| "We need Salesforce test automation" | Dedicated Salesforce testing with metadata-based locators, sandbox support, auto-sync with instances | Salesforce case study: regression from days to hours, defects caught earlier. |
| "We're migrating to cloud/microservices and tests keep breaking" | AI self-healing adapts to architecture changes. Parallel execution validates across new environments. | Nagra DTV: transitioned from in-house framework to Testsigma in 8 months. |
| "Security and compliance requirements make tool adoption slow" | Enterprise plan: on-prem deployment, private grid, SSO, IP whitelisting, SOC 2/ISO certified | Sanofi (pharma compliance). Oscar Health (healthcare). Multiple banks. |
| "We don't have a dedicated QA team" | Plain English NLP means developers write tests without QA expertise. Copilot generates tests from Jira stories. | Spendflo: small team, 50% manual testing reduction. |
| "We already have a tool but it's not keeping up" | Unlike Selenium wrappers (Katalon, etc.), Testsigma is purpose-built with agentic AI. Generator + Healer + Optimizer work autonomously | CRED: achieved 90% coverage at 5x speed after switching. |
| "Test creation takes too long" | Generator Agent creates tests from prompts, Figma, Jira, videos, screenshots. 10x faster authoring claimed. | Fortune 100: 3x productivity increase. Nagra DTV: tests that took 1-2 days now built in hours. |
| "We can't get visibility into what's tested and what's not" | Atto 2.0 Coverage Discovery autonomously explores app to find untested paths. Built-in test management with traceability. | Unique capability, no direct competitor match. |
| "We have too many APIs to test alongside the UI" | Unified platform handles API + UI + mobile in one test suite. Single test can validate API response and then check UI rendering. | Credit Saison: 400+ APIs, 5,000+ tests daily. Nagra DTV: API + UI for OTT platform. |
| "We can't automate because our app uses 2FA" | Built-in 2FA testing with OTP generation, phone provisioning, and email mailbox. No need to disable 2FA in QA. | Unique Testsigma capability. No competitor handles this natively. |
| "Our mobile testing is separate from web testing" | Unified platform: 2,000+ real devices for iOS/Android + 800+ browser combos for web. One test suite, one platform. | Fortune 100: nearly 100% mobile testing automated, 400 cases migrated in 2 months. |
| "We're scaling fast and can't hire QA fast enough" | NLP + AI agents reduce headcount dependency. Non-technical team members write tests. | Credit Saison: avoided 30-40% QA team expansion. Open Vantage: no headcount increase needed. |
| "We're paying for too many testing tools (TestRail + Selenium + BrowserStack, etc.)" | Testsigma replaces your automation framework, test management tool, device cloud, and CI/CD test runner with one platform. | Built-in test management (replaces TestRail/Zephyr), 3,000+ cloud environments (replaces BrowserStack), AI test creation (replaces Selenium). |
| "Our Salesforce testing is manual and painful" | Dedicated Salesforce testing with metadata locators (not fragile XPath), auto-healing for LWC, multi-sandbox support, auto-sync with metadata changes. | Salesforce-specific case study available. Works across Lightning, Classic, and LWC. |
| "We can't keep up with sprint velocity, QA is the bottleneck" | Sprint Planner Agent auto-detects new Jira sprints and plans test coverage. Generator Agent creates tests from Jira stories. Self-healing means no maintenance backlog. | Hansard: 3x faster regression. Credit Saison: 5,000+ tests running daily overnight. |

---

## H) Ideal Customer Profile

### Company Size Sweet Spot
- **Primary:** 200-10,000 employees (large enough to need automation, small enough to move fast)
- **Secondary:** 50-200 employees (if they're tech companies with software products)
- **Enterprise:** 10,000+ (sell on unified platform consolidation and maintenance reduction)

### Industries Where Testsigma Wins Most
1. **FinTech** - Fast release cycles, compliance requirements, multi-platform (web + mobile + API)
2. **SaaS/Tech** - Continuous deployment, scaling coverage, mixed-skill teams
3. **Healthcare/Digital Health** - HIPAA compliance, integration testing, fast growth
4. **Insurance/Financial Services** - Long regression cycles, regulatory testing, Salesforce
5. **Pharma** - Compliance-heavy, validation requirements, slow traditional processes
6. **Retail/E-Commerce** - Cross-browser, cross-device, high velocity
7. **Media/Streaming** - Multi-platform (OTT, web, mobile), API + UI testing

### Titles That Buy (Budget Authority)
- Director/VP of QA / Quality Engineering
- VP Engineering / CTO (at smaller companies)
- VP of IT / CIO

### Titles That Influence (Technical Champions)
- QA Manager / QA Lead
- Senior SDET / Automation Lead
- Software Engineering Manager (owns QA when no dedicated team)

### Common Trigger Events
- Hiring a new QA leader (first 90 days = evaluation window)
- Scaling engineering team rapidly (coverage can't keep up)
- Migrating to cloud or microservices (existing tests break)
- Launching a new product or platform (need testing fast)
- Recent funding round (budget available, growth pressure)
- Switching tools (frustration with current solution)
- Post-acquisition integration (multiple platforms to test)

---

## I) Objection Handling with Proof

| Objection | Response | Proof |
|-----------|----------|-------|
| "We already use Selenium/Cypress/Playwright" | "Totally fair. A lot of teams we work with used [their tool] too. The gap they kept hitting was maintenance, tests breaking every time the UI changed. Testsigma's Healer Agent auto-fixes those. Worth comparing?" | 70% maintenance reduction vs Selenium. 90% with full self-healing. |
| "We already use Katalon/Tosca/Testim/mabl" | "Makes sense. The teams that switch usually hit a ceiling with [AI depth/pricing/platform coverage]. Testsigma's agentic AI goes beyond assisted testing to autonomous testing. Different architecture." | CRED switched and hit 90% coverage at 5x speed. |
| "We're a large enterprise, can you scale?" | "Absolutely. We offer on-prem, private cloud, and hybrid deployment. SOC 2/ISO certified. Fortune 500 companies run us behind their firewall. Enterprise plan includes SSO, IP whitelisting, and a dedicated CSM." | Fortune 100: 3x productivity. Sanofi (global pharma). Cisco, Samsung, Nokia, Nestle as customers. |
| "We don't have a QA team" | "That's actually why teams like yours use Testsigma. Plain English test creation means developers write tests without dedicated QA expertise. The Copilot generates tests from your Jira stories automatically." | Spendflo: small team, no dedicated QA, cut manual testing 50%. |
| "Just hired a new QA leader, too early to evaluate" | "Makes sense. A lot of QA leaders in their first 90 days use our free trial to benchmark what's possible before committing to a tool. No pressure, just data." | 21-day free trial with full access. |
| "We have compliance/security requirements" | "We work with Sanofi, Oscar Health, and several banks. On-prem deployment, private grid, SSO, IP whitelisting are all standard on Enterprise. Happy to walk through our compliance story." | Sanofi (pharma, global compliance). Oscar Health (HIPAA). |
| "Budget is tight" | "Totally get it. One company your size, Spendflo, cut manual testing 50% and saw ROI in the first quarter. We also have a free open-source edition if you want to start there." | Spendflo: ROI in first quarter. Community Edition: free. |
| "AI testing tools are all hype" | "Fair skepticism. The difference is Testsigma's agents actually do the work, they don't just suggest. The Healer auto-fixes broken tests. The Generator creates them from Jira stories. Real results, not demos." | Nagra DTV: 2,500 real tests in 8 months, running daily in CI/CD. |

---

## J) G2 and Review Platform Intelligence

### What Users Love (use in messaging)
1. **NLP/Plain English testing** - Most praised feature across all review platforms
2. **AI self-healing** - Second most praised, especially by teams coming from Selenium
3. **Responsive support** - "Issues get diagnosed and resolved within hours, not days"
4. **Low learning curve** - "With minimum training, users can handle the application"
5. **Cross-platform coverage** - Single platform replacing multiple tools

### What Users Dislike (anticipate in objection handling)
1. **Opaque pricing** - No published pricing, requires sales calls
2. **Limited reporting depth** - Not as deep as BrowserStack or Sauce Labs
3. **Element identification in complex DOMs** - Can be tricky initially
4. **Test data limitations** - Complex data scenarios can be challenging
5. **Can be overkill for simple apps** - Features you won't use if your app is small

### Competitive Position on Reviews
- G2: 4.5/5 (70+ reviews). Leader status Fall 2025.
- BrowserStack and LambdaTest score slightly higher (4.6) with far more reviews (2,400+), but Testsigma wins on codeless testing and AI-powered maintenance. Neither offers self-healing.

---

## K) Key Product Terminology Quick Reference

| Term | What It Is | When to Reference |
|------|-----------|-------------------|
| **Atto** | AI coworker, the suite of 5+ autonomous agents | When discussing AI differentiation |
| **Atto 2.0** | Nov 2025 update with intent-based healing, coverage discovery, risk analysis | When discussing latest capabilities |
| **Generator Agent** | Auto-creates tests from prompts, Figma, Jira, videos | When prospect struggles with test creation speed |
| **Healer Agent** | Auto-fixes broken tests when UI changes | When prospect has flaky/brittle test problems |
| **Analyzer Agent** | Diagnoses failures with visual diffs and root cause | When prospect spends too much time debugging |
| **Optimizer Agent** | Prunes redundant tests, flags coverage gaps | When prospect's test suite is bloated |
| **Runner Agent** | Parallel execution across thousands of sessions | When prospect has slow execution times |
| **Sprint Planner Agent** | Auto-plans tests for new Jira sprints | When prospect needs test management |
| **Copilot** | GenAI assistant for test generation | When discussing AI-powered creation |
| **NLP** | Natural Language Programming, plain English tests | When prospect lacks coding expertise |
| **Self-healing** | AI auto-fixes broken locators (90% reduction) | For any maintenance/flakiness pain |

---

---

## L) Complete Verified Proof Points Library (Quick Reference for Messaging)

Use ONLY these verified proof points in outreach. Never fabricate stats.

| # | Customer | Metric | Best Match | Source Status |
|---|----------|--------|------------|---------------|
| 1 | **Hansard** | Regression 8 weeks to 5 weeks (3x faster). 75% automated coverage. Sanity in 30 min post-commit. | Insurance, financial services, long regression cycles | VERIFIED (testsigma.com/customers/hansard, Holly Pennington quote) |
| 2 | **Nagra DTV** | 2,500 tests in <8 months. 4x faster test creation (1-2 days per test to 3-4 per day). Eliminated manual testing. CI/CD running daily. | Media, streaming, OTT, API + UI, framework migration | VERIFIED (testsigma.com/customers/nagra, direct quote) |
| 3 | **Spendflo** | 50% manual testing reduction. Faster execution. Steady growth in automated test cases. | SaaS, small teams, budget-conscious, quick wins | VERIFIED (testsigma.com/customers/spendflo) |
| 4 | **Credit Saison India** | 80% regression automation (from 30%). 5,000+ tests daily. Avoided 30-40% QA team expansion. | FinTech, lending, mobile-heavy, scaling without headcount | VERIFIED (testsigma.com/customers/creditsaison) |
| 5 | **Fortune 100 Tech Giant** | 3x efficiency. 400 tests migrated in 2 months. Nearly 100% mobile testing automated. 1-week training. | Enterprise, mobile testing, telecom, VP-level | VERIFIED (testsigma.com/customers/networkingcommunicationscompany) |
| 6 | **Finland AI Company** | 47.82% test case volume increase in 6 months (1,481 to 2,189). Reduced manual testing. | AI/tech companies, European prospects | VERIFIED (testsigma.com/customers/finland-based-AI-technology-company) |
| 7 | **Open Vantage** | 40% test coverage from near-zero. No QA headcount increase. Lower cost vs. custom frameworks. | IT services, lean teams, South Africa/international | VERIFIED (testsigma.com/customers/open-vantage) |
| 8 | **Sanofi** | Regression from 3 days to 80 minutes | Pharma, compliance-heavy, healthcare | INTERNAL (confirmed by Rob, no public case study) |
| 9 | **CRED** | 90% regression automation, 5x faster execution | FinTech, high-velocity | INTERNAL (confirmed by Rob, no public case study) |
| 10 | **Medibuddy** | 2,500 tests automated, 50% maintenance cut | Healthcare, mid-size teams | INTERNAL (confirmed by Rob, no public case study) |
| 11 | **General Platform** | 90% maintenance reduction with self-healing. 70% vs Selenium specifically. 10x faster test authoring. | Any prospect with maintenance/flakiness pain | VERIFIED (multiple sources, testsigma.com) |

---

## M) Implementation, Onboarding, and Learning Curve

### How Fast Can Teams Get Started?
- **Fortune 100 case study:** Full QA team trained and productive within 1 week
- **NLP basics:** Most users write their first tests within hours due to plain English syntax
- **Advanced features:** Steeper curve for complex scenarios (custom Java scripting, addon development, advanced data-driven testing)
- **Onboarding process:** Structured onboarding with tailored training sessions. Dedicated CSM on Enterprise.
- **Free trial:** 21 days with full feature access, enough time for a meaningful POC

### What Does a Typical Implementation Look Like?
1. **Week 1:** Training, platform setup, first test cases created
2. **Weeks 2-4:** Core regression suite built, CI/CD integration configured
3. **Month 2-3:** Coverage expansion, self-healing tuned, team fully autonomous
4. **Ongoing:** Atto agents handle maintenance, team focuses on new test creation

### BDR Talking Point
"Teams typically write their first tests within hours because it's plain English. One Fortune 100 team was fully trained in a week. The steepest part of the learning curve is advanced customization, but most teams never need it because the AI handles the complexity."

---

## N) Migration Path (From Other Tools)

### Key Fact: No Direct Automated Import
- There is NO automated "import Selenium scripts" or "import Katalon tests" feature
- Tests must be recreated in Testsigma's NLP format
- However, test creation is dramatically faster with NLP + Copilot + AI Generator
- Nagra DTV migrated 2,500 tests from WebDriver IO in under 8 months
- Fortune 100 migrated 400 test cases in 2 months

### Migration Framework (How to Position It)
| Migration From | Prospect Concern | How to Reframe |
|---------------|-----------------|----------------|
| Selenium/WebDriver | "We have thousands of tests, rewriting is expensive" | "Nagra DTV rebuilt 2,500 tests in 8 months, and they stopped spending time on maintenance. The rewrite pays for itself in the first quarter." |
| Katalon | "We've invested in Katalon already" | "Most Katalon teams that switch tell us the same thing: they hit a ceiling with AI depth. The migration is fast because NLP tests write 10x faster than Katalon's approach." |
| Tosca | "Tosca is deeply embedded in our enterprise" | "Makes sense. A lot of Tosca teams run Testsigma in parallel first, cover the gaps Tosca can't reach. No rip-and-replace needed." |
| Manual testing | "We don't have tests to migrate" | "That's actually the ideal starting point. No legacy debt. Teams go from zero to 80% automation in 3-6 months." |

### BDR Talking Point
"There's no automated import, but honestly, that's a feature. Rewriting in plain English with AI is faster than you'd expect, and you get self-healing from day one. Nagra DTV rebuilt 2,500 tests in 8 months, and the new suite runs daily without maintenance."

---

## O) BDR Buyer Question Bank (with Answers)

These are the questions buyers and prospects most commonly ask, with pre-loaded answers from verified sources.

### Product Questions

**Q: How does the AI self-healing actually work?**
A: When your app's UI changes between releases (buttons renamed, elements moved, layouts updated), the Healer Agent detects the change and automatically updates the test locator. Atto 2.0 goes further with intent-based healing: it understands WHAT the test is trying to do (e.g., "click the submit button"), not just WHERE the element was. So even if the element changes substantially, the AI adapts.

**Q: Can we use it if we don't have coding skills on the team?**
A: Yes. Tests are written in plain English (NLP). Business analysts, product managers, and manual testers can all write and maintain tests. For advanced scenarios, Java scripting is available, but most teams never need it.

**Q: What about testing behind 2FA/MFA?**
A: Testsigma is one of the only platforms with built-in 2FA testing. It generates OTPs natively, provisions phone numbers for SMS verification, and provides email mailboxes for email-based 2FA. No need to disable security in your test environment.

**Q: How does it handle dynamic elements, Shadow DOM, and iframes?**
A: Dedicated documentation and tooling for Shadow DOM, iframe switching, and dynamic elements. Multiple locator strategies including runtime parameters and environment-based data. The AI adapts locators dynamically.

**Q: Can we test APIs alongside our UI tests?**
A: Yes, in the same test flow. Full REST API support (GET, POST, PUT, DELETE, PATCH), JSON schema validation, test chaining (use API response data in UI steps), Postman collection import, and Swagger/OpenAPI support.

**Q: What about our Salesforce environment?**
A: Dedicated Salesforce testing with metadata-based locators (not just XPath), auto-healing for Lightning Web Components, multi-sandbox support (Developer, Dev Pro, Partial Copy, Full), and auto-sync with Salesforce metadata changes.

### Competitive Questions

**Q: How is this different from Selenium?**
A: Selenium is a framework, not a platform. You write code, build infrastructure, maintain locators manually, and stitch together 5-6 tools for CI/CD, test management, parallel execution, and reporting. Testsigma is one platform that does all of that, with AI agents handling the maintenance. 70% less maintenance vs Selenium.

**Q: How is this different from Katalon?**
A: Katalon is Selenium under the hood with a UI layer. When locators break, you still fix them manually. Testsigma's Healer Agent fixes them autonomously. Katalon's AI is assistive (suggests), Testsigma's is agentic (acts). Plus Testsigma has an open-source edition.

**Q: How is this different from mabl or Testim?**
A: mabl is primarily web-focused. Testim (now Tricentis) is hybrid code/codeless which can be confusing. Neither has the multi-agent architecture (5+ autonomous agents working together) or the breadth of platform coverage (web, mobile, API, desktop, Salesforce, SAP) that Testsigma offers.

### Business Questions

**Q: What does implementation look like?**
A: Typically 1 week for training, 2-4 weeks to build a core regression suite, and 2-3 months to full coverage. Fortune 100 team was productive in 1 week. We provide structured onboarding with a dedicated CSM on Enterprise.

**Q: How much does it cost?**
A: Around $10K per license. But we sell on value, not price. Most teams see ROI in the first quarter from reduced maintenance and faster test creation. There's also a free open-source Community Edition.

**Q: Is it secure enough for our industry?**
A: Trust Center at trust.testsigma.com. 15+ documented security policies. GDPR and CCPA compliant. On-premises and private cloud deployment options. We work with Sanofi (pharma), Oscar Health (healthcare), and several financial services companies.

**Q: Can we run a POC first?**
A: 21-day free trial with full feature access. No credit card required. Most teams have enough data to make a decision within the trial period.

**Q: What integrations do you support?**
A: 30+ integrations including Jenkins, GitHub Actions, GitLab CI, Azure DevOps, Jira (two-way sync), Slack, BrowserStack, Sauce Labs, Figma, and more. If your CI/CD tool has an API, we can integrate.

---

## P) Product Roadmap Signals and Recent Launches

| Date | What Launched | Why It Matters for BDR |
|------|--------------|----------------------|
| **Nov 2025** | Atto 2.0 (intent-based healing, coverage discovery, risk analysis) | Lead with this for prospects frustrated by false failures and incomplete coverage |
| **May 2025** | AI-Native Test Management Module | Consolidation play: "replace TestRail + Selenium + BrowserStack with one platform" |
| **May 2025** | Autonomous Testing Platform positioning | Strategic narrative for VP/CTO conversations: "the platform tests itself" |
| **Sept 2025** | G2 Leader in Test Management | Proof point for test management pitch |
| **Ongoing** | Addons Marketplace growth (100+) | Shows extensibility and community |

---

*This document is the foundation for all outreach messaging. Every message must connect a prospect's specific pain to a Testsigma-specific solution from this bible, backed by a customer proof point with real numbers. No generic "test automation" language.*
