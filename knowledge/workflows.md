# Workflows

## Sales Navigator Workflow
1. Use Rob's saved searches in Sales Navigator.
2. Click "Show X new results" to filter to fresh, never-contacted prospects only.
3. Manager level and above only. Must fit ICP titles (see `icp.md`).
4. **MUST check interaction status** on each profile. If "Messaged:" or "Viewed:" shows prior activity, EXCLUDE and replace.
5. Filter out: pharma/biotech manufacturing QA (not software), non-US, titles that don't own software testing decisions.
6. Extract data using bulk JavaScript DOM extraction from search pages, then visit individual profiles for deep research.
7. Use `get_page_text` for profile data extraction (more reliable than screenshots).
8. Launch parallel Task subagents for company research to save time.

## Research Requirements (TWO sources per prospect)
1. **LinkedIn profile** - Read headline, about section, role description, responsibilities, recent activity. Capture and log the Sales Navigator profile URL.
2. **Company research** - From credible external sources (company website, product pages, news, engineering blog, job postings, press releases). NOT just the LinkedIn company page.

## A/B Testing Within Batches

Split each 25-prospect batch into 2-3 sub-groups to test ONE variable at a time. Label each prospect with their A/B group.

**What to A/B test (one per batch, rotate across batches):**
1. **Pain hook** - Group A: "maintenance/flaky tests" angle, Group B: "release velocity/speed" angle
2. **Proof point style** - Group A: named customer, Group B: anonymous
3. **Opener style** - Group A: career-reference openers, Group B: company-metric openers
4. **Ask intensity** - Group A: "Would 15 minutes make sense?", Group B: "Happy to share more if helpful"
5. **Message length** - Group A: 70-80 words (tight), Group B: 100-120 words (fuller)

**Rules:**
- Only test ONE variable per batch. Keep everything else constant.
- Split groups evenly by persona type and vertical so results aren't skewed.
- Need 3+ batches testing the same variable to draw conclusions.

## Feedback Loop & Batch Learning

- Each deliverable HTML includes status tracker, reply tags, A/B group labels, and personalization scores.
- Rob updates these as he sends messages and gets replies.
- Before building the NEXT batch, Claude reads ALL previous batch files and generates a Pre-Brief.
- Adjustments based on accumulated data: which proof points get replies, which opener styles work, which personas convert, which verticals are responsive, which A/B variants win, whether higher personalization scores correlate with replies.

## Pre-Brief (generated before each new batch)

5-line "What's Working" summary:
1. **Best persona** - Which title/level is replying most?
2. **Best proof point** - Which customer story is in the most replied-to messages?
3. **Best vertical** - Which industry is warmest?
4. **Best pattern** - Any opener/ask/length pattern standing out?
5. **Stop doing** - One thing to drop or change.

## Meeting Booked Handoff

When a prospect says yes, the deliverable includes a Prep card:
1. **Company snapshot** - What they do, how big, key products, recent news.
2. **Prospect snapshot** - Title, tenure, responsibilities, career background.
3. **Known/likely tech stack** - From profile, job postings, engineering blog.
4. **Pain hypothesis** - The specific testing problem from our outreach.
5. **What triggered the reply** - From the reply tag.
6. **Suggested discovery questions** (3-5, tailored).
7. **Relevant proof points** - 2-3 matched to their vertical and pain.
8. **Predicted objections** - Pre-mapped objection + response.

Keep to one screen. Rob should read it in 2 minutes before the call.
