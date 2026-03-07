# Weekly Prep Brief — Week of March 2, 2026

## Week Overview
- **1 external call this week** — Lexia Learning trial kickoff on Monday at 3:00 PM ET. This is a high-priority meeting: it's a trial kickoff with two QA leaders (Sr. Director QA + QA Manager) at a $380M EdTech company serving 6.8M students.
- **Key signal:** Lexia is part of Cambium Learning Group and runs multiple student-facing products (Core5, PowerUp, Lexia English) across web and mobile. Their QA team owns test coverage for products used by 23,000+ schools in 100+ countries.
- **Estimated time commitment:** 1 hour (3:00–4:00 PM ET Monday)

---

## Monday, March 2

### Lexia Learning — 3:00 PM ET
**Attendees:** Joe Casale (Sr. Director, Quality Assurance), Megan Morris (Software QA Manager — Student Products), Tyler Kapeller (Testsigma), Zac Taylor (Testsigma), Sridhar (Testsigma), Rob Gorham (Testsigma)
**Meeting type:** Trial Kickoff

**Company Snapshot**
- Lexia Learning is a K-12 literacy and language EdTech company, part of Cambium Learning Group (formerly Rosetta Stone). Founded 1984, HQ Concord MA, ~870 employees, ~$380M estimated revenue.
- Core products: **Core5** (K-5 reading), **PowerUp** (6-12+ literacy), **Lexia English** (English learners), **LETRS** (teacher training). All student-facing products run on web + mobile.
- Serves **6.8 million students** and **620,000+ educators** across **23,000 schools** in 100+ countries. That scale means a massive cross-platform test matrix.
- Tech stack includes Salesforce, Atlassian Cloud, Docker, Kubernetes, React Redux, New Relic, Terraform, and Figma. No visible dedicated test automation tool detected, which suggests they may be relying on manual testing or homegrown frameworks.
- Actively hiring QA roles, which signals capacity pressure on the testing team.

**Attendee Profiles**
- **Joe Casale** (Sr. Director, Quality Assurance): Based in Framingham, MA. At Lexia since 2014, promoted to Sr. Director in 2018 — 12 years leading QA there. Previously at IBM (Software Group) and Unica. Deep institutional knowledge of Lexia's product suite and test infrastructure. As Sr. Director, he likely owns the QA strategy, tooling decisions, and budget. His longevity means he's seen every iteration of their testing approach and knows where the gaps are.
- **Megan Morris** (Software QA Manager — Student Products): Based in Cleveland, OH (remote). At Lexia since May 2022, managing QA specifically for student-facing products (Core5, PowerUp, Lexia English). Previously at Dakota Software, AXS, and Sherwin-Williams. She owns the day-to-day testing execution for the products that 6.8M students use. Her focus on "Student Products" means she feels the pain of cross-platform coverage, release cadence, and regression testing most directly.

**Top Signals This Week**
- **Trial kickoff = active evaluation.** They've committed time and resources to exploring Testsigma. Joe (budget holder) and Megan (execution lead) are both attending, which signals this is being taken seriously at multiple levels.
- **No visible test automation tool** in their tech stack. They're likely evaluating Testsigma because their current approach (manual or homegrown) isn't scaling with 3 major product lines + mobile.
- **Active QA hiring** suggests the team is under capacity pressure. Automation could relieve that without requiring additional headcount.

**This Week's News**
- Lexia announced **2026 Science of Reading Week** and continues to win industry recognition (CODiE Awards for Core5 and PowerUp).
- **Core5 product updates** include Retake Placement and accessibility enhancements, which expand the test surface (new features = new test cases needed).
- **19% growth in state department renewals** and ~2,000 schools now on Lexia English — growing footprint means growing testing demands.

**Recommended Objectives**
Understand their current testing setup (tools, frameworks, pain points) across the student product suite, and establish clear success criteria for the trial. Since Joe owns strategy and Megan owns execution, tailor the conversation: help Joe see how Testsigma fits into the QA roadmap, and help Megan envision how her team's daily workflow improves. Anchor to the scale challenge — 3 product lines, web + mobile, 6.8M students means zero tolerance for regression bugs reaching production.

**Relevant Proof Points**
- **Medibuddy** (2,500 tests automated, 50% maintenance cut) — similar consumer-facing platform at scale
- **CRED** (90% regression automation, 5X faster execution) — high-velocity product team with broad test coverage needs
- **Sanofi** (regression from 3 days to 80 minutes) — if regression cycle time is a bottleneck for their release cadence

**Suggested Discovery Questions**
1. "Walk me through how your team currently tests Core5 and the student products across web and mobile — what does a typical release cycle look like?"
2. "What's your current automation coverage like? Are you using any frameworks today, or is it mostly manual?"
3. "Where does regression testing hit hardest — is it the cross-platform matrix, the sheer number of test cases, or something else?"
4. "With the Core5 accessibility updates and Lexia English expansion, how is the team keeping test coverage ahead of new feature releases?"
5. "What does success look like for this trial? What would need to be true for Testsigma to become your go-to automation platform?"

**Predicted Objection**
*"We're still assessing / too early to commit"* — Joe has been leading QA for 12 years at Lexia. He's methodical. Likely wants to see proof before committing.
**Pre-loaded response:** "Makes total sense. A lot of QA leaders use the trial period to benchmark what's possible against their current approach. We can set up a focused test suite on one product (like Core5) so you see real results before making any broader decision."
