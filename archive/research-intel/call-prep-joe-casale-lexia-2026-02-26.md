# Call Prep: Joe Casale — Lexia Learning

**Meeting:** Intro Call — Thu Feb 26, 11:30 AM EST (15 min)
**Link:** [Join via RevenueHero](https://testsigma.revenuehero.io/meetings/43d77572-8e84-4228-a4b0-46f12369882d/conference)
**Lead Source:** INBOUND (Joe booked this himself)

---

## Account Snapshot

| Field | Value |
|-------|-------|
| **Company** | Lexia Learning |
| **Parent** | Cambium Learning Group (owned by Rosetta Stone, acquired 2013) |
| **Industry** | EdTech / E-Learning |
| **HQ** | Concord, MA |
| **Employees** | ~870 |
| **Revenue** | ~$380M |
| **Engineering Headcount** | ~74 |
| **Key Products** | Core5 Reading (K-5), PowerUp Literacy (6-12), Lexia English (ELL), LETRS (teacher PD), Aspire Professional Learning |
| **Scale** | 6.8M students, 620K educators, 23K+ schools |

### What They Do
Lexia builds literacy software used in 1 out of every 3 US school districts. Their products deliver personalized, adaptive reading instruction for students pre-K through grade 12, plus professional development for educators. Everything is web-based and data-driven, with real-time student progress dashboards.

### Tech Stack (QA-Relevant)
| Category | Tools |
|----------|-------|
| **Frontend** | React Redux |
| **Mobile** | Android |
| **Infrastructure** | Docker, Kubernetes, Terraform, AWS |
| **Monitoring** | New Relic |
| **Design** | Figma |
| **Project Mgmt** | Atlassian Cloud (Jira) |
| **CRM/Internal** | Salesforce, Salesforce Service Cloud |

**Testing implications:** Multi-product web platform built on React + mobile (Android). Docker/K8s infrastructure means CI/CD pipeline is likely mature. Multiple products = large test surface. No visible test automation tool in their tech stack (no Selenium, Cypress, Playwright detected in Apollo).

---

## Who You're Meeting

### Joe Casale — Sr. Director, Quality Assurance

| Field | Detail |
|-------|--------|
| **Location** | Framingham, MA (EST) |
| **At Lexia Since** | 2014 (~12 years) |
| **Promoted** | Director QA → Sr. Director QA (2018) |
| **Email** | joe.casale@lexialearning.com (verified) |
| **Phone** | +1 508-330-7228 |
| **LinkedIn** | [Profile](http://www.linkedin.com/in/joe-casale-6938ba7) |
| **Education** | Masters, IT Management — Brandeis University (2006-2009) |

**Career Path (28+ years in QA):**
- Sybase → Sr. QA Engineer (1998-2007, ~9 years)
- Unica → Principal QA Engineer (2007-2010)
- IBM → QA Manager → Sr. QA Manager (2010-2013)
- Lexia → Director QA → Sr. Director QA (2014-present)

**Skills on record:** Perforce, Test Planning, QA, Software QA, Agile Methodologies

**Side venture:** CEO of "Vodka Vault" since 2021 (personal project, don't bring up unless he does)

**What this tells you:** Joe is a deeply experienced QA veteran, not a newcomer. He's been doing this for nearly three decades. He'll know his stuff technically. Don't oversimplify or over-explain basics. He's been at Lexia long enough to have built whatever QA infrastructure exists there, so any pain he's feeling is pain with HIS OWN system. Be respectful of what he's built while exploring where it's hitting limits.

---

## Context & Key Signals

### Why This Meeting Matters
**This is inbound.** Joe went to the Testsigma website and booked this call himself. That means:
- He has active pain or curiosity
- He's already past the "awareness" stage
- He's evaluating options (or at least window-shopping)
- Your job is to understand WHY he came to you, not to pitch

### QA Pressure Points to Explore
1. **Multi-product test surface:** 5+ distinct products (Core5, PowerUp, English, LETRS, Aspire), each with different user types (students K-5 vs 6-12 vs teachers vs admins). That's a massive test matrix.
2. **Seasonal pressure:** EdTech companies face intense "back to school" deadlines. Lexia just announced 2025-2026 product updates (accessibility upgrades, new content modules, Spanish language support). All of that needs testing before school year launch.
3. **Cross-platform coverage:** Web + Android + adaptive learning algorithms. The personalization engine means testing isn't just UI, it's logic-driven outcomes per student.
4. **Salesforce in-house:** They use Salesforce CRM and Service Cloud internally. If they test Salesforce workflows, that's a direct Testsigma strength.
5. **No visible automation tool in stack:** Apollo doesn't show Selenium, Cypress, or Playwright. Could mean they're using something unlisted, or there's a gap in automation coverage.
6. **React Redux frontend:** Dynamic, component-heavy UI. Locators change frequently. Self-healing would be highly relevant.

### Recent Company Activity
- Lexia was named a 2025 CODiE Award winner
- Parent company Cambium named to GSV 150 list (6th consecutive year)
- 19% increase in state departments acquiring Lexia LETRS/Aspire in 2025
- Product updates for 2025-2026: accessibility improvements, Spanish language support in Lexia English, new teacher training content

---

## Suggested Agenda (15 min is tight)

1. **Open (1 min)** — Quick intro, thank him for booking. Then go straight to: *"What prompted you to take a look at Testsigma?"* — This is the most important question. His answer tells you everything about his pain and intent.

2. **Discovery (7-8 min)** — Based on his answer, dig into the details. See questions below.

3. **Bridge / Proof Point (3-4 min)** — Share ONE relevant customer story matched to whatever pain he describes. Keep it tight.

4. **Next Steps (2-3 min)** — If interested: propose a deeper technical demo with his team. If early stage: offer a free trial or POC.

---

## Discovery Questions (pick 4-5 based on his opening)

**Start here (most important):**
> "What prompted you to take a look at Testsigma?"

**Then explore based on his answer:**

| If he mentions... | Ask... |
|-------------------|--------|
| Test maintenance / flaky tests | "How much of your team's time is going to test upkeep vs. writing new coverage?" |
| Scaling coverage | "How many of your products does the QA team cover today? Where are the gaps?" |
| Tool evaluation / replacing a tool | "What are you using today, and where is it falling short?" |
| Speed / release pressure | "How does the school-year cycle affect your release cadence? Is back-to-school a crunch?" |
| General curiosity | "Walk me through how your team tests Core5 and PowerUp today. Manual, automated, or a mix?" |

**Additional discovery questions:**
- "How big is your QA team, and how is it structured across the products?"
- "Are you testing the adaptive/personalization logic, or is that more on the data science side?"
- "Is mobile (Android) testing a separate effort, or same team?"
- "What does your CI/CD pipeline look like for test execution?"

---

## Proof Points Ready to Deploy

| If pain is... | Use this story |
|---------------|---------------|
| **Test maintenance / flaky tests** | Hansard cut regression from 8 weeks to 5 weeks using AI self-healing. 90% reduction in test maintenance. |
| **Scaling across multiple products** | Medibuddy automated 2,500 tests across their platform and cut maintenance by 50%. |
| **Speed / release velocity** | Sanofi went from 3-day regression cycles to 80 minutes. |
| **Multi-platform (web + mobile)** | Testsigma covers web, mobile, API, and desktop from one platform. Plain English test creation, no code switching between frameworks. |
| **Selenium/manual testing limits** | Teams moving off Selenium see 70% maintenance reduction with Testsigma's self-healing. |

---

## Potential Objections

| Objection | Response |
|-----------|----------|
| **"We already have a tool/process"** | "Totally fair. Most QA leaders who come to us do. The question is usually whether it's keeping up with the test surface. What's working well today, and where are you hitting limits?" |
| **"We're just exploring, no timeline"** | "Makes sense. A lot of QA directors in their first look use our free trial to benchmark what's possible before building a business case. Would that be helpful?" |
| **"Security / data privacy (EdTech = COPPA/FERPA)"** | "We're SOC2 Type II, ISO 27001, and GDPR compliant. We also offer on-prem and private cloud deployment. Happy to walk through the specifics with your security team." |
| **"Need to involve my team"** | "Totally. The best next step would be a technical walkthrough with a couple of your leads so they can validate the fit. What day works to set that up?" |

---

## Tone Reminders

- **He came to YOU.** Don't pitch. Discover.
- **He's a 28-year QA veteran.** Talk peer-to-peer, not top-down. He'll respect technical depth and hate feature dumps.
- **15 minutes is short.** Get to "why are you here" in the first 60 seconds. Don't waste time on company intros.
- **Goal of this call:** Understand his pain, earn a second meeting with his team. That's it.
- **If he asks "what do you do?"** — Keep it to 30 seconds: "We're an AI-powered test automation platform. Teams write tests in plain English, our AI creates and runs them, and when the UI changes, our self-healing fixes the tests automatically. We cover web, mobile, API, all from one platform."
