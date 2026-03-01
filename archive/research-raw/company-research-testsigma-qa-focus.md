# Testsigma BDR Research: Company Deep Dives

**Date:** February 23, 2026
**Research Focus:** QA/Testing tech stacks, pain points, and AI test automation opportunities

---

## 1. FIDELITY INVESTMENTS

### Company Overview
- **Employees:** 35,000+
- **Headquarters:** Boston, MA
- **Business:** Leading global financial services company; operates wealth management, brokerage, asset management, retirement solutions, and payment services

### Big Data Platforms Division (Key Focus)
Fidelity is building a "next-generation data pipeline" to make data available across the entire enterprise and ecosystem. Mihir Shah leads this as enterprise head of data architecture and engineering. Focus on democratizing data access across roles for better decision-making.

### Tech Stack & Data Infrastructure
- **Big Data:** Hadoop 3.4.2+ (with enhanced S3A support), Apache Spark 4.0.1+
- **Data Pipeline:** Next-generation ETL/data integration
- **Cloud:** AWS services (S3, EC2, database services)
- **Data Tools:** Google Drive, data warehousing solutions

### QA & Test Automation Tech Stack (from job postings)
- **UI Automation:** Selenium, Playwright (actively recruiting)
- **Testing Frameworks:** TestNG, Cucumber, JUnit
- **CI/CD Pipeline:** Jenkins (primary), Git/GitHub
- **Testing Roles:** Senior Software Engineer (QA Automation), Software Engineer in Test (Selenium/Playwright), Senior Software Engineer in Test, Principal Software Engineer in Test
- **Current Hiring:** Multiple open positions across Westlake TX, Merrimack NH, Jersey City NJ, Durham NC, Smithfield RI, Galway Ireland

### Testing Pain Points (Inferred)
1. **Data Pipeline Testing Complexity** - Testing ETL pipelines, data transformations, and large-scale data processing across distributed systems
2. **Test Framework Maintenance** - Java-based test suites require constant upkeep; Selenium and Playwright maintenance across multiple platforms
3. **CI/CD Test Bottlenecks** - Jenkins pipeline scaling and parallel test execution across distributed teams
4. **Coverage Gaps** - Multiple job postings indicate aggressive hiring for test automation, suggesting coverage scale challenges
5. **Cross-Platform Testing** - Need to test across multiple data sources, platforms, and integrations (Hadoop, Spark, cloud services)

### Recent Developments (2025-2026)
- Heavy investment in data pipeline modernization
- Migration toward cloud-first architecture (AWS)
- Active hiring for QA/testing roles suggests aggressive automation expansion

### Prospect Fit for Testsigma
**HIGH** - Fidelity faces scale and maintenance challenges in test automation with legacy Selenium/Playwright frameworks. AI self-healing would reduce brittle tests in complex data pipeline testing. NLP could simplify test creation for non-technical roles in data teams.

---

## 2. CITIZENS FINANCIAL GROUP

### Company Overview
- **Employees:** ~20,000+
- **Headquarters:** Providence, RI
- **Business:** Multi-national bank providing consumer and commercial banking, wealth management, and digital financial services
- **Recent Recognition:** Named "Bank of the Year" by The Banker (December 2025)

### Digital Transformation & Platform Engineering (Key Focus)
Citizens is undergoing massive digital transformation and cloud migration to modernize banking infrastructure. In mid-2024, crossed 50% cloud migration milestone; targeting 100% by end of 2025. Partnered with Cognizant to open Hyderabad hub for enhanced digital resilience and testing capabilities.

### Engineering Initiatives (2025-2026)
- **Hiring Plan:** Close to 750 engineers hired over past 4 years; planning expansion to 1,000+ engineers (shift from outsourced to in-house engineering)
- **AI Adoption:** Pilot with Microsoft Copilot showed 20% productivity boost; rolling out to 1,000 engineers
- **Operating Model:** Agile, DevSecOps-focused with modern CI/CD pipelines, test automation, APIs, and cloud services

### Tech Stack & Infrastructure
- **Cloud Platforms:** Amazon Web Services (AWS), Microsoft Azure (hybrid cloud strategy)
- **DevSecOps:** Modern CI/CD pipelines, automated test automation, API-first architecture
- **Mobile/Digital:** New payment methods, direct deposit features (with Mastercard partnership)
- **Master Data Management:** Informatica (for cloud master data management)
- **Data Management:** Cloud data management and governance

### QA & Test Automation Tech Stack (from job postings)
- **UI Automation:** Selenium (explicitly mentioned in Senior QA Engineer role)
- **Testing Tools:** Cucumber, Test Complete, EggPlant, Appium (mobile), Perfecto, ReadyAPI (API testing)
- **Salary Range:** $63,760-$95,640 for Senior QA Engineer roles
- **Current Hiring:** Senior QA Engineer - Automation (Selenium) in Johnston, RI
- **Focus Areas:** Shortening test cycles, lowering testing costs, test-driven development

### Testing Pain Points (Inferred)
1. **Cloud Migration Testing Complexity** - Testing hybrid cloud environments (AWS/Azure) simultaneously
2. **Multi-Service Integration Testing** - New digital products require extensive cross-system testing
3. **DevSecOps Testing Requirements** - Security testing, compliance testing, API security testing at scale
4. **Test Automation Scaling** - Rapid engineering team growth (750→1000+) requires distributed, scalable testing
5. **Legacy-to-Cloud Test Translation** - Testing flaky legacy tests during migration while ensuring new cloud tests are reliable
6. **Mobile App Testing** - Testing new mobile payment capabilities across devices/platforms

### Recent Developments (2025-2026)
- Opening India hub with Cognizant for "digital resilience and testing" (explicit outsourcing of testing to ramp quickly)
- Launched new mobile capabilities (Mastercard partnership)
- Microsoft Copilot rollout to 1,000 engineers (AI-assisted coding/testing)
- Active build-out of in-house engineering capability

### Prospect Fit for Testsigma
**VERY HIGH** - Citizens is mid-transformation with aggressive timeline (100% cloud by end of 2025), scaling engineering from 750→1000+ people, and explicitly investing in testing outsourcing. Current Selenium-based approach won't scale. AI self-healing and NLP-based test creation are perfect for reducing test maintenance during cloud migration. "Digital resilience" mandate = testing pain point.

---

## 3. SALESFORCE

### Company Overview
- **Employees:** 80,000+
- **Headquarters:** San Francisco, CA
- **Business:** Global CRM and enterprise cloud software leader; now major AI platform player with Agentforce
- **Recent Focus:** AI agents, Einstein AI, Agentforce platform (major 2025 initiative)

### Agentforce AI Cloud & Internal QA Challenges (Key Focus)
Salesforce is building Agentforce - an autonomous AI agent platform that fundamentally changes how testing works. Testing AI agents is exponentially harder than testing traditional software. Unlike chatbots, Agentforce agents handle multi-turn conversations, take actions across Salesforce (create records, trigger flows, update data), and escalate to humans.

### Tech Stack & Platform Architecture
- **Core Language:** Apex (proprietary), Lightning Web Components (LWC) with Jest testing
- **Testing Requirements:** 75% code coverage minimum for deployments; best practice is 90%+
- **APIs:** REST, SOAP, Platform Events, Change Data Capture (CDC) streams
- **Flow Automation:** Flow-heavy orgs require new testing approaches
- **AI/ML Stack:** Einstein AI foundation; new Agentforce agents built on proprietary AI

### QA & Test Automation Practices (from industry research)
- **Apex Testing:** Unit tests with TestNG-style assertions; 75% coverage enforced by platform
- **LWC Testing:** Jest framework for Lightning Web Components
- **API Testing:** Comprehensive REST/SOAP/Platform Event validation; data transformation validation
- **Agentforce Testing Center:** New tool (2025) that tests agents against thousands of AI-generated scenarios before deployment
- **Test Approach:** Functional + Performance + Security + Bias/Fairness testing + Ethical Red Teaming
- **Guardrails Testing:** Edge-case prompts, malformed inputs, policy-violating inputs to verify guardrails work

### AI/LLM Testing Challenges (Critical Pain Point)
1. **Conversational Accuracy Testing** - Validating multi-turn conversations with context retention
2. **Bias & Fairness Testing** - AI agents must pass ethical red teaming; hallucination mitigation
3. **Guardrail Validation** - Testing Einstein Trust Layer (toxicity detection, dynamic grounding, zero data retention)
4. **Business Logic + AI** - Agents must correctly execute Salesforce actions (create records, flows) while handling natural language
5. **Scale & Volume** - Agentforce Testing Center tests agents against thousands of AI-generated scenarios (not traditional test cases)
6. **Hallucination Detection** - Testing to prevent incorrect information dissemination
7. **Escalation Logic** - Ensuring smooth handoffs between AI and human agents, preserving context

### Adoption Trends (2025)
- AI-based testing adoption: **7% (2023) → 16% (2025)** - doubling in two years
- AI-assisted test creation & data generation: **50%+ adoption** among leading QA teams (already surpassing traditional test creation)
- Shift to "Cognitive DevOps" where quality becomes embedded, intelligent capability
- New skill requirements: Jest, Flow-heavy org testing, quality gates, modern Salesforce delivery

### Recent Developments (2025-2026)
- Agentforce launched as core platform capability
- Agentforce Testing Center released (synthetic scenario generation)
- Einstein Trust Layer enhancements (bias, fairness, toxicity guardrails)
- Responsible AI guidelines and red-teaming requirements
- Test automation landscape moving toward AI-driven testing (not just Selenium)

### Prospect Fit for Testsigma
**VERY HIGH + STRATEGIC** - Salesforce is THE company struggling with AI agent testing at scale. Traditional Selenium-based approaches don't work for multi-turn conversation validation, guardrail testing, and bias detection. Testsigma's AI-powered test creation and self-healing are perfect for Agentforce testing. Testsigma could own "Agentforce QA" as a specialization. Salesforce internal QA teams AND customers building Agentforce agents both have acute pain.

---

## 4. NETAPP

### Company Overview
- **Employees:** 10,000+
- **Headquarters:** San Jose, CA
- **Business:** Enterprise storage, data management, and cloud infrastructure leader; building AI data infrastructure
- **Recent Focus:** Kubernetes storage orchestration, AI data management, ONTAP disaggregation

### Software Engineering & Storage Platform Testing (Key Focus)
NetApp maintains extremely complex storage platforms (ONTAP, Trident, CloudVolumes) that require rigorous testing across:
- Multiple storage protocols (NFS, SMB, FC, NVMe/TCP)
- Kubernetes environments (Trident for container orchestration)
- Distributed systems (HA, failover, replication)
- Performance-sensitive workloads (AI/ML, databases, analytics)

### Tech Stack & Infrastructure
- **Kubernetes Orchestration:** Trident 25.10 (latest), open-source storage orchestrator
- **Storage Protocols:** NFS, SMB, FC, NVMe/TCP, iSCSI
- **Container Runtime:** Red Hat OpenShift, Kubernetes
- **Cloud Platforms:** AWS, GCP, Azure integrations
- **ONTAP Features:** FlexClone (rapid cloning for testing), SnapShot, replication, compression
- **AI Data Platform:** New "NetApp AI Data Engine" (2025) - orchestration layer for AI data pipelines

### Testing Infrastructure & Practices
- **Development Environment:** Now running on Red Hat OpenShift Virtualization (enables faster provisioning, reduced complexity)
- **Clone for Testing:** DevOps engineers use FlexClone for fast, space-efficient test clones to speed up time-to-market
- **Release Cycle:** Rapid - 4 releases per year (like Kubernetes)
- **Complex Testing:** Multi-protocol support, HA/failover scenarios, performance testing, security testing

### QA & Software Testing Roles (from job postings)
- **QA Automation Engineer** roles listed at NetApp
- **Responsibilities:** Develop, modify, review test plans; identify improvements in software development processes, tools, methodologies
- **Requirements:** Participation in all phases of product development cycle (requirement → design → implementation → test design)

### Testing Pain Points (Inferred)
1. **Storage Stack Complexity** - Testing ONTAP across multiple protocols, configurations, and failover scenarios
2. **Kubernetes Integration Testing** - Trident testing requires Kubernetes cluster validation, container orchestration edge cases
3. **Protocol Diversity** - Testing NFS, SMB, FC, NVMe/TCP simultaneously; protocol-specific bug discovery
4. **Performance Testing at Scale** - AI/ML workloads require performance characterization; small-file handling edge cases reported
5. **Rapid Release Cycles** - 4 releases/year requires fast test automation; traditional manual/Selenium approaches bottleneck
6. **Distributed System Testing** - HA, replication, node failover require complex state validation
7. **AI Data Pipeline Testing** - New AI Data Engine (2025) requires end-to-end testing of data transformation, governance, metadata management

### Recent Developments (2025-2026)
- **Trident 25.10 Release:** Enhanced scalability, node/controller parallelism improvements
- **ONTAP AI (AFX):** Disaggregated AI storage platform, new testing requirements
- **AI Data Engine:** New orchestration layer for AI workloads (testing liability)
- **OpenShift Virtualization:** Modernized test infrastructure reduces complexity
- **NVIDIA Integration:** Building AI infrastructure on NVIDIA AI Data Platform

### Prospect Fit for Testsigma
**HIGH** - NetApp's complex distributed storage systems and rapid 4-release/year cycle create test maintenance nightmares. AI self-healing would reduce flaky test failures across protocol edge cases. Testsigma's parallel execution and cross-browser/multi-environment support maps to NetApp's multi-protocol testing needs. New AI Data Engine (2025) is a testing liability.

---

## 5. CAREEM

### Company Overview
- **Employees:** 2,000+ (estimates vary)
- **Headquarters:** Dubai, UAE
- **Business:** Ride-sharing and super-app platform; operates in 70+ cities across Middle East and South Asia
- **Valuation:** Last valued at $3.1 billion (exit target ~$5B+)
- **Business Model Shift:** Moving from ride-sharing-only to super-app (ride, food delivery, payments, financial services, lending)

### Super-App Architecture & Testing Complexity (Key Focus)
Careem's big strategic bet is the "Super App" - evolving from ride-sharing to unified platform offering 5+ services. This creates massive testing complexity: multiple interdependent services, cross-service state management, unified user experience requirements, new payment flows, financial services integration.

Challenge explicitly stated: "Making Careem feel like one unified app, not just multiple services bolted together."

### Tech Stack & Infrastructure
- **Backend:** Java, AWS services (S3, EC2), Google Cloud
- **In-Memory Cache:** Redis (for location tracking, real-time ride updates, data caching)
- **Data Storage:** Amazon S3, Google BigQuery
- **Cloud Provider:** AWS primary, with Google Cloud secondary
- **Architecture:** Microservices (modular, independently scalable)
- **Development:** Agile methodologies, DevOps, CI/CD pipelines

### QA & Test Automation Tech Stack (from job postings)
- **Mobile Testing:** Sofy, Maestro (next-gen mobile testing)
- **API Testing:** Postman, REST-assured (Java REST client), JMeter (load/performance testing), K6
- **BDD Framework:** Cucumber
- **UI Automation:** Selenium
- **Mobile Automation:** Appium
- **CI/CD Tools:** Jenkins, Bitrise (iOS/mobile CI)
- **Current Hiring:** QA Engineer I, QA Engineer II, Director of Quality Engineering (Automation & QA)
- **Benefits:** 4-day office week, remote work flexibility (30 days/year), unlimited vacation

### Testing Pain Points (Inferred)
1. **Cross-Service Integration Testing** - Super-app requires testing that rides, food, payments, financial services work together seamlessly
2. **Unified State Management** - Testing that user context/session persists across service boundaries
3. **Payment Flow Complexity** - Multiple payment methods, financial services integration, security testing
4. **Mobile-First Testing** - iOS/Android apps are primary interface; Maestro/Sofy adoption suggests issues with traditional mobile automation
5. **Real-Time Data Consistency** - Redis caching, location tracking, ride matching requires real-time validation
6. **Microservices Interdependencies** - Testing failures in one service (payment) can cascade; contract testing gaps
7. **Global Scale Testing** - 70+ cities, multi-language, multi-currency, regional regulations
8. **Modern Framework Adoption** - Job postings show Maestro/Sofy (newer tools), suggesting dissatisfaction with traditional Appium/Selenium

### Recent Developments (2025-2026)
- Super-app strategy acceleration (major engineering push)
- Oracle AI integration for invoice process automation (70% reduction; suggests data/finance testing pain)
- Aggressive feature releases (payment methods, direct deposits, new services)
- Team expansion for super-app unification

### Prospect Fit for Testsigma
**HIGH** - Careem's super-app strategy requires cross-service integration testing at scale. Microservices + payment/financial flows = brittle, flaky tests. AI self-healing would reduce test maintenance as services evolve. Testsigma's ability to test across mobile, API, and cross-service workflows maps perfectly. Director of QA hiring signals testing infrastructure overhaul.

---

## 6. O9 SOLUTIONS

### Company Overview
- **Employees:** 500+ (estimates)
- **Headquarters:** Dallas, TX
- **Business:** AI-powered enterprise planning and supply chain optimization platform
- **Valuation:** Privately held; recent funding rounds suggest $1B+ valuation target
- **Market Recognition:** Gartner Customers' Choice 2025 - Supply Chain Planning Solutions (only vendor with this honor)

### AI Supply Chain Platform & Testing at Scale (Key Focus)
o9 Solutions sells "Digital Brain" - an enterprise AI planning platform based on proprietary Enterprise Knowledge Graph (EKG) technology. Platform handles integrated business planning, demand forecasting, supply chain master planning, production scheduling, allocation, revenue growth management. Supports Fortune 500 customers (Walmart, Nike, Estée Lauder, Starbucks, Nestlé, Google, Sony, Samsung, Caterpillar, Bridgestone).

### Tech Stack & Architecture
- **Core Technology:** Enterprise Knowledge Graph (EKG) - proprietary data modeling layer
- **In-Memory Store:** Graph-Cube (in-memory graph database for fast querying)
- **Data Ingestion:** Batch ETL + Real-time APIs
- **AI Agent Stack:** Generative AI + Agentic AI + Neurosymbolic reasoning
- **APIs:** UI APIs, Reference Model APIs (GraphCube access), planning APIs
- **Integration:** Connects to SAP, Salesforce, Oracle, JD Edwards, NetSuite ERP systems

### 2025 AI Enhancements (Major Pain Point)
- **GenAI-Powered Agents:** New composite agents for cross-functional planning (demand, supply, revenue, allocation)
- **Neurosymbolic AI:** Combines symbolic reasoning with neural networks for planning optimization
- **Real-Time Decision Making:** Agents continuously sense changes, simulate outcomes, recommend actions
- **Autonomous Planning:** Agents execute complex, multi-step planning tasks without human intervention
- **Learning Models:** Self-learning models that improve over time with new data

### QA & Test Automation Tech Stack (from job postings)
- **API Testing:** JMeter (performance/load), Postman
- **UI Automation:** Selenium, Robot Framework
- **SDET Roles:** Senior QA Engineer II (SDET) with 6-10 years experience, SaaS microservices focus
- **Microservices Testing:** API testing emphasis; JMeter for performance testing at scale
- **Current Hiring:** Associate QA Engineer, QA Engineer II, Senior QA Engineer, Senior QA Engineer II (SDET)

### Testing Pain Points (Inferred)
1. **AI Agent Testing Complexity** - Testing autonomous agents that make multi-step planning decisions requires validating decision logic, not just API responses
2. **Graph Database Testing** - EKG/GraphCube testing requires validating graph traversals, relationships, query correctness
3. **Real-Time Data Pipeline Testing** - Batch ETL + real-time APIs must maintain data consistency in graph structure
4. **Neurosymbolic AI Validation** - Testing combination of symbolic reasoning + neural networks is non-trivial; edge cases in planning logic
5. **Integration Testing at Scale** - Connecting to 5+ ERP systems (SAP, Salesforce, Oracle, JD Edwards, NetSuite) with bi-directional sync
6. **Performance Testing for Decision Engines** - Graph queries over massive enterprise datasets must perform sub-second
7. **Multi-Tenant Data Isolation** - Fortune 500 customers require strict data separation; testing cross-tenant leaks
8. **Machine Learning Model Testing** - Self-learning models require continuous monitoring; detecting model drift, bias

### Recent Business Growth (2025-2026)
- **Go-Lives:** 30+ customer implementations in 2025 alone
- **ARR Growth:** Mid-double-digit growth 2022-2025 with acceleration
- **New Logos:** +60% YoY new customer acquisition (Q1 2025)
- **Feature Expansion:** Revenue Growth Management suite added to platform
- **Neurosymbolic AI:** Major new capability released (2025)

### Prospect Fit for Testsigma
**VERY HIGH** - o9's rapid growth (+60% YoY new logos, 30+ go-lives in 2025) combined with complex AI agent + graph database + ERP integrations = testing bottleneck. Traditional Selenium/JMeter can't validate planning agent logic. Testsigma's NLP test creation ideal for non-technical planning domain experts to create "what-if" test scenarios. Self-healing crucial as ERP integrations evolve. AI testing is o9's bleeding edge pain.

---

## SUMMARY: QA/Testing Pain Points by Company

| Company | Primary Pain | Secondary Pain | Tech Stack Debt | Testsigma Fit |
|---------|--------------|-----------------|-----------------|---------------|
| **Fidelity** | Data pipeline testing scale | Selenium/Playwright maintenance | Java test framework legacy | HIGH - NLP for data teams, parallel execution |
| **Citizens** | Cloud migration testing (hybrid AWS/Azure) | Test scaling (750→1000 engineers) | Selenium + legacy-to-cloud test translation | VERY HIGH - cloud testing + scaling |
| **Salesforce** | AI agent testing (Agentforce) guardrails/bias | Multi-turn conversation validation | Apex + Jest test coverage (75% mandate) | VERY HIGH - AI testing specialization |
| **NetApp** | Distributed storage complexity + rapid releases | Multi-protocol testing (NFS/SMB/FC/NVMe) | ONTAP/Trident test maintenance | HIGH - parallel execution, complex workflows |
| **Careem** | Super-app cross-service integration | Mobile testing (Maestro/Sofy adoption) | Microservices state management | HIGH - mobile + API + cross-service |
| **o9** | AI agent + ERP integration testing | Graph database query validation | Neurosymbolic AI testing | VERY HIGH - AI agent + integration testing |

---

## Key Insights for Rob's Outreach

1. **AI Testing is the Bleeding Edge** - Salesforce (Agentforce), o9 (Neurosymbolic agents), and Careem (super-app scale) all face new testing challenges that Selenium/Cypress/Playwright can't solve. "AI agents require AI test automation."

2. **Cloud Migration = Immediate Pain** - Citizens (50%→100% cloud migration), Fidelity (data pipeline modernization), and NetApp (infrastructure on OpenShift) all have 6-12 month windows where testing is on fire.

3. **Microservices Testing is Hard** - Careem (super-app), o9 (ERP integrations), and NetApp (Trident/Kubernetes) all struggle with testing interdependent services. Contract testing, cross-service state validation, cascading failures.

4. **Self-Healing is Gold** - All six companies use Selenium or similar brittle tools. Rapid releases (NetApp 4x/year, Careem weekly, o9 with 30+ go-lives in 2025) mean test flakiness is costing them velocity.

5. **NLP Test Creation Resonates** - Fidelity's data teams, Careem's super-app product managers, and o9's planning domain experts all need to write tests but aren't developers. "Write tests in English" is a huge unlock.

6. **Platform-Specific Testing** - Salesforce needs Agentforce-specific QA (guardrails, bias, hallucination testing), NetApp needs storage protocol testing, o9 needs planning agent testing. Testsigma could own verticals.

---

## Sources Consulted

- Fidelity Careers: [Senior Software Engineer (QA Automation)](https://www.fidelitytalentsource.com/job-details/20023016/senior-software-engineer-qa-automation-/)
- Citizens Financial Group: [Senior QA Engineer - Automation (Selenium)](https://jobs.citizensbank.com/job/johnston/senior-qa-engineer-automation-selenium/288/53494385792)
- Citizens Digital Transformation: [Article on digital banking and cloud migration](https://tearsheet.co/banking/how-citizens-is-rebuilding-a-modern-bank-from-the-inside-out/)
- Salesforce Agentforce: [Platform documentation](https://www.salesforce.com/agentforce/)
- Salesforce Testing Landscape 2025: [SalesforceDevops.net Report](https://salesforcedevops.net/index.php/2025/10/09/salesforce-test-automation-landscape-2025-report/)
- NetApp Trident: [25.10 Release](https://www.netapp.com/blog/trident-25-10-advanced-kubernetes-storage-solutions/)
- NetApp AI Data Engine: [Blog announcement](https://blocksandfiles.com/2025/10/14/netapp-disaggregates-ontap-storage-and-provides-an-ai-data-engine/)
- Careem Tech Stack: [Appscrip blog article](https://appscrip.com/blog/careem-tech-stack-and-infrastructure/)
- Careem Super-App: [CIO.com article on CISO strategy](https://www.cio.com/article/190909/careems-ciso-explains-strategy-for-the-companys-big-bet-super-app.html)
- o9 Solutions: [Digital Brain platform overview](https://o9solutions.com/digital-brain)
- o9 2025 Achievements: [Q2 2025 results and go-live success](https://o9solutions.com/news/o9-q2-2025-results/)
- o9 Gartner Recognition: [Customers' Choice 2025 for Supply Chain Planning](https://o9solutions.com/)
