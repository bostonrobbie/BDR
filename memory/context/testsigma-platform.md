# Testsigma Platform - Full Reference

## Company Overview
- **Founded:** 2019 by Rukmangada Kandyala + 3 co-founders (all from Freshworks/Zoho background)
- **HQ:** San Francisco; Engineering in Bangalore & Chennai
- **Employees:** ~196 (as of March 2025); 22 engineers, 3 quota-carrying sales reps
- **Funding:** $12.8M total ($4.6M seed Feb 2022 from Accel/STRIVE; $8.2M Series A June 2024 from MassMutual Ventures)
- **Revenue:** ~$10.6M (Oct 2024)
- **Customers:** 68 companies (TheirStack), 1.3M reported users
- **Open source:** Launched Feb 2022 with open-source version + cloud solution

## Platform Capabilities

### Testing Types Supported
- Web application testing (cross-browser, 800+ browser/OS combos)
- Mobile testing (native iOS, Android, mobile browser — 3000+ real devices)
- API testing (RESTful, codeless creation, automated assertions)
- Desktop application testing
- Salesforce testing (Lightning UI, complex element IDs, API)
- SAP testing
- Database testing
- Visual testing (pixel-perfect + lenient modes)
- Accessibility testing (WCAG 2.2 — Level A, AA, AAA)
- Data-driven testing (CSV, JSON, external sources)
- Regression, smoke, sanity, UAT testing

### AI Capabilities (Atto)
**Atto = suite of AI agents ("coworkers"):**
1. Sprint Planner — auto-plans tests when Jira sprint starts
2. Generator — creates tests from NL prompts, Figma, Jira, screenshots, videos, docs
3. Runner — executes tests intelligently at scale
4. Analyzer — root cause analysis on failures
5. Healer — self-healing (intent-based in 2.0, 90% maintenance reduction)
6. Optimizer — optimizes test suites
7. Bug Reporter — real-time failure analysis

**Atto 2.0 (Nov 2025):** Adaptive intelligence, intent-based self-healing, coverage discovery (finds untested paths), risk analysis (connects changes to user flows)

**Copilot:** GenAI assistant that generates complete test cases from multiple input types

### How Test Creation Works
1. Log in → navigate to test editor
2. Write steps in plain English (e.g., "Click on Login Icon")
3. Auto-suggest prompts next logical steps
4. OR use Copilot: prompt like "Create test for user registration with invalid email"
5. Copilot generates full executable test with assertions
6. Can generate from: user stories, Figma designs, screenshots, live apps, docs
7. Manage tests in suites → create test plans → execute

### Deployment Options
1. Public Cloud (fully managed SaaS)
2. Private Cloud
3. On-Premises (self-hosted)
4. Hybrid

### Security
- SSO/SAML support
- IP whitelisting
- Private grid for on-prem execution
- ISO/SOC2 certifications (reference in security-conscious deals)

### Integrations (30+)
**CI/CD:** Jenkins, GitHub Actions, GitLab CI, Azure DevOps, CircleCI, Bamboo, Travis CI
**Bug Tracking:** Jira (two-way), Linear, FreshRelease, YouTrack, Mantis, Backlog
**Cloud/Infra:** AWS, Sauce Labs, BrowserStack
**Collaboration:** Slack
**Design:** Figma (Copilot can generate tests from designs)

### Pricing
- Pro and Enterprise tiers (custom pricing, no public rates)
- Free trial available (no credit card)
- No free tier (community edition status unclear)
- Contact sales for quotes

## Analyst Recognition
- **Forrester:** Recognized in "The Autonomous Testing Platforms Landscape, Q3 2025"
- **G2 Fall 2025:** Leader in Software Testing, Automation Testing, and Test Management
- **G2 Rating:** 4.5/5 stars
- **Gartner Peer Insights:** 4.5/5 stars, 51 reviews
- **Capterra:** 4.2/5 stars

## What Demos Well (from internal research)
**Strengths:** Plain-English test steps, dropdown action selection, mobile testing, local test execution, cross-browser/mobile/API in one tool, responsive support, real customer stories
**Watch-outs:** Recorder/debugger gaps, switching windows for record-playback, competitor UI comparisons (some find others more polished), scalability questions at enterprise scale, reporting limitations

## Competitive Positioning

### vs. Selenium/Cypress/Playwright (Open Source)
- They're "free" but maintenance costs 20+ hrs/week for 55% of teams
- Testsigma: no-code, self-healing, managed cloud, 70% less maintenance
- Bridge: "You can still use custom code — it's not either/or"

### vs. Katalon
- Katalon stronger on API/web services testing
- Testsigma: simpler NLP approach, fully cloud-hosted, broader accessibility
- Katalon has free starter edition (pricing advantage)

### vs. Testim/Tricentis
- Testim specialized in flakiness reduction
- Testsigma: broader scope (mobile, API, desktop, Salesforce), NLP-based

### vs. mabl
- mabl: mature visual workflows, strong DevOps integration
- Testsigma: broader testing scope, NLP approach, stronger mobile/API

### vs. BrowserStack/LambdaTest/Sauce Labs
- They're infrastructure only (bring your own tests)
- Testsigma: complete platform (creation + execution)
