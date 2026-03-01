# Memory Layer - BDR Second Brain

Persistent, structured knowledge that compounds over time. Every file here makes future outreach smarter.

## Structure

```
memory/
├── competitors/       # Battle cards per tool. Used by message_writer when a competitor is detected.
├── wins/              # Structured win reports. What worked, what resonated, why they bought.
├── losses/            # Structured loss reports. Why they didn't convert, what we learn.
├── call-notes/        # Post-call capture. What the prospect said about stack, pain, timeline.
├── market-intel/      # Industry trends, analyst mentions, competitor moves.
└── context/           # Sales playbook, persona guides, evergreen reference material.
```

## How Agents Use This

1. **Researcher agent** checks `competitors/` when a prospect's tech stack is detected. Pulls specific weaknesses and migration stories for that tool.
2. **Message writer** pulls displacement angles from battle cards to craft sharper proof points. Instead of generic "a lot of teams had [tool] too," it says exactly why teams switch from Cypress vs. TOSCA vs. Selenium.
3. **Pre-brief agent** reads `wins/` and `losses/` to identify patterns across deals. Which pain hooks actually close? Which objections kill deals?
4. **Call prep agent** reads `call-notes/` for prior conversations with the same account or similar prospects.

## How to Add Data

### After a call
```
cp memory/call-notes/_template.md memory/call-notes/YYYY-MM-DD-firstname-lastname.md
```
Fill in the template. Takes 2 minutes. Pays dividends forever.

### After a win
```
cp memory/wins/_template.md memory/wins/YYYY-MM-DD-company-name.md
```

### After a loss
```
cp memory/losses/_template.md memory/losses/YYYY-MM-DD-company-name.md
```

### New competitor intel
Edit the relevant file in `memory/competitors/`. Add new data points, update pricing, note product launches.

## Rules

- **Be honest in battle cards.** If a competitor is genuinely good at something, say so. Credibility > cheerleading. Focus on where they fall short for our ICP.
- **Capture raw quotes.** When a prospect says something revealing on a call, write it down verbatim. Raw quotes are more valuable than summaries.
- **Date everything.** Intel decays. A pricing data point from 2024 may be wrong in 2026.
- **No fluff.** These files are for Rob to glance at before dialing. Keep it tight.
