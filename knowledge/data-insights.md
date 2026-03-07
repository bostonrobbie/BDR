# Outbound Intelligence System

Data-driven rules derived from analysis of 1,330 LinkedIn conversations (384 replies, 946 no-replies, 6,210 messages). These rules override generic best practices. When data conflicts with intuition, the data wins.

Source data: `data/analysis_output.json` and `data/linkedin-outreach-analysis.docx`

## Hard Constraints (MUST NEVER be violated)

Any draft message violating these is automatically rejected and rewritten.

| # | Constraint | Data Basis |
|---|-----------|------------|
| HC1 | No "reaching out" / "wanted to connect" / "I saw" / "I noticed" phrasing | -13.3 pp diff (14.7% reply vs 28.0% no-reply). Strongest negative signal. |
| HC2 | No role-at-company as the primary opener hook ("Seeing that you're the [Title] at [Company]") | -12.7 pp diff (86.1% vs 98.8%). Present in 98.8% of failures. |
| HC3 | No feature-led framing (AI, self-healing, automation as the headline) | ai_mention -8.0 pp, self_healing -6.8 pp. Features as headlines lose. |
| HC4 | No messages over 120 words | Reply avg 98.7 words vs no-reply 107.7 words. Shorter wins. |
| HC5 | No evening sends (after 6 PM) | Evening: 10.8% of replies vs 19.4% of no-replies. -8.6 pp swing. |
| HC6 | No bullet-point feature lists | Bullet-format messages dominate no-reply samples. 0 high-performers use bullets. |
| HC7 | No permission-based CTAs ("would it be unreasonable", "happy to share if helpful") | permission_ask CTA: 23.5% rate (below 27.5% baseline). |

## Strong Preferences (optimize for)

| # | Preference | Data Basis |
|---|-----------|------------|
| SP1 | Under 100 words (~580 chars) | Reply avg: 578 chars / 98.7 words |
| SP2 | Afternoon send window (12-5 PM) | 88.7% of replies sent in afternoon vs 80.4% no-reply |
| SP3 | Question-led openers grounded in research | question_opener: +2.6 pp diff |
| SP4 | Exactly one outcome-based proof point | Relevance matters, not volume |
| SP5 | Direct, confident CTA with time/action | meeting_ask: 75.0% rate (directional, small n) |
| SP6 | Vary message angle across touches | High-performer threads: 4.7 avg msgs with diverse angles |
| SP7 | Commit to at least 3 touches before expecting reply | 28.2% of replies came after 2 msgs, 31.3% after 3+ |
