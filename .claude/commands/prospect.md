# Prospect - Identify and qualify new prospects

You are Rob's BDR assistant. The user wants to build a prospect list.

## Files to Load
- `.claude/rules/message-structure.md` — prospect mix ratio, priority scoring, qualification checklist
- `work/pipeline-state.json` — current batch number, credit budget
- `work/dnc-list.json` — exclude any DNC contacts
- `config/scoring_weights.json` — priority scoring weights
- `config/vertical_pains.json` — vertical classification

## Process

### Step 1: Check pipeline state
Read `work/pipeline-state.json`:
- How many InMail credits remain? (If <10, PAUSE new sourcing)
- Any unsent batches pending? (Fix those first)
- What's the latest batch number?

### Step 2: Determine sourcing method
Follow the priority waterfall from `.claude/rules/sops.md` (SOP D):
1. **Tier 1: Buyer Intent** — Always check first
2. **Tier 2: Re-Engagement** — If last outreach >60 days ago
3. **Tier 3: Saved Search Backfill** — Standard cold outbound
4. **Tier 4: Specific Account** — Only when Rob directs

If Rob provides a specific source, use that. Otherwise follow the waterfall.

### Step 3: Source prospects
Based on the source:
- **Apollo visitors**: Use Apollo MCP tools to pull high-intent website visitors. Filter: 200+ employees, US, ICP titles.
- **Sales Navigator**: Ask Rob to paste the prospect data or share the search. Extract names, titles, companies, LinkedIn URLs.
- **Manual list**: Accept a pasted list.

### Step 4: Qualify each prospect
Run the qualification checklist:
- [ ] Manager+ seniority
- [ ] ICP title match (QA Manager, Director QA, VP QA, Test Architect, Sr SDET)
- [ ] US-based (unless specified otherwise)
- [ ] Software QA/engineering (NOT pharma manufacturing, biotech lab QA)
- [ ] Company has software products or digital platforms
- [ ] Not on DNC list (check `work/dnc-list.json`)
- [ ] No prior interaction (check with Rob if unsure)

### Step 5: Apply prospect mix ratio
For a 25-prospect batch, aim for:
- 10-12 QA Manager/Lead (26.8% reply rate, best volume+rate)
- 4-6 QA Directors/Heads (26.0% reply rate, has budget)
- 3-5 Architects/Senior ICs (39.3% reply rate, undervalued persona)
- 2-3 Buyer Intent regardless of title
- MAX 2 VP Eng/CTO, only with Buyer Intent or QA scope
- Vertical diversity: no more than 8 from same vertical

### Step 6: Score and enrich
For each qualified prospect:
- Compute priority score (1-5) using `config/scoring_weights.json`
- Enrich with Apollo if available (company + person enrichment)
- Classify vertical using `config/vertical_pains.json`

### Step 7: Save and present
Save to `work/batch-[N]-prospects.csv` with columns:
name, title, company, email, linkedin_url, vertical, employee_count, persona_type, signals, priority_score

Show Rob a summary:
"X prospects qualified out of Y reviewed. Mix: X QA Manager/Lead, Y Director, Z Architect, W Buyer Intent. Ready for /write-batch."

Update `work/pipeline-state.json` with new batch number.

## Key Rules
- Do NOT ask Rob "where should I source from?" — follow the priority waterfall
- Do NOT include prospects from the same company more than twice
- Do NOT include VP Eng at 50K+ companies without Buyer Intent (11.9% reply rate)
- DO prioritize Architects (39.3% reply rate) — most undervalued persona
- Flag Buyer Intent signals prominently
