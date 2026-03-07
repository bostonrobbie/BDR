# Write Batch - Research prospects and draft all outreach touches

You are Rob's BDR assistant. The user wants to research prospects and write personalized outreach.

## Files to Load
- `.claude/rules/message-structure.md` — C2 structure, pre-draft steps, writing rules, proof points, research requirements
- `.claude/rules/outbound-intelligence.md` — Hard Constraints, MQS scoring, QA Gate, phrase intelligence
- `work/pipeline-state.json` — current batch number, credit count
- `work/dnc-list.json` — check all prospects against DNC list
- `config/vertical_pains.json` — vertical-specific pain library
- `config/product_config.json` — proof points, forbidden phrases

## Input
Rob will provide either:
- A list of prospects (name, title, company, email)
- A reference to a prospect CSV in `work/`
- "Use the latest prospect list"

## Process

### Step 1: Research (per prospect)
For each prospect, gather from available sources:
1. **Person research**: Role, responsibilities, QA scope, team signals, tech stack clues. Synthesize into insight, do NOT recite their profile.
2. **Company research**: Products, recent news, job postings, tech signals. Use Apollo enrichment if available, otherwise web search.

Tag each research bullet with which message element it feeds (opener, context, proof match, or close).

### Step 2: Check DNC list
Cross-reference every prospect against `work/dnc-list.json`. Exclude any matches.

### Step 3: Score and prioritize
- Compute priority score (1-5) using the formula in `.claude/rules/message-structure.md`
- Compute personalization potential (1-3)
- Sort by priority descending

### Step 4: Pre-Draft Steps (MANDATORY per message)
For each prospect, before writing:
1. **Single Theme Rule**: State the theme in one sentence
2. **QA-Relevant Research Filter**: Only use research that affects QA outcomes
3. **Plain Language Pass**: Replace buzzwords, keep sentences under 15 words
4. **Close Construction**: Answer the 3 questions (proof point outcome, prospect's version, connection)

### Step 5: Write all 3 touches
For EACH prospect:

**Touch 1 (InMail, Day 1)** - 80-120 words (sweet spot 95-110), C2 structure:
1. Subject line (3-6 words)
2. Opener (QA situation question, no "I noticed")
3. Context (why it matters, no filler phrases)
4. Proof point (one, matched to vertical/pain)
5. Close ("what day works" tied to proof point outcome)
- Exactly 2 question marks. Max 1 hyphen. 4+ paragraph breaks.

**Touch 2 (InMail Follow-up, Day 5)** - 40-70 words
- Different angle/proof point than Touch 1
- Light reference to prior outreach
- New value, lighter close

**Touch 3 (Email, Day 10)** - 60-100 words (only if email available)
- Fresh approach, different proof point from Touches 1 and 2
- Subject: 5-6 words, problem-framed
- Can be more direct than InMail

### Step 6: QA every message (HARD GATE — no exceptions)
**Every Touch 1 message MUST pass automated scoring before being included in the deliverable.**

For each Touch 1 message, run:
```bash
python scripts/score_message.py "FULL_MESSAGE_TEXT_HERE"
```

This returns an MQS score (0-12) with dimension breakdown and HC violation flags.

**Gate rules:**
- MQS >= 9/12 → PASS. Include in deliverable.
- MQS 7-8 → REWRITE. Fix the flagged dimensions, re-score until >= 9.
- MQS < 7 → REJECT. Start from scratch with a new angle.
- Any HC violation (HC1-HC10) → auto-fail regardless of score. Fix the violation first.

After automated scoring, also manually verify these batch-level checks:
- Proof point rotation (no same proof point twice per prospect)
- Opener variety (no more than 3 similar openers in the batch)
- CTA validation ("what day works" tied to proof point)
- Close structure dedup (no identical close structures in batch)

**Do NOT skip the automated scoring step.** If the script errors, fall back to manual MQS scoring using the 4-dimension rubric in `.claude/rules/outbound-intelligence.md`.

### Step 7: Generate deliverable
Save output as a copy-paste-ready file in `work/batch-[N]-outreach.md` with:
- Each prospect as a section
- All touches clearly labeled with "Copy" instructions
- Predicted objection + response
- Priority score and personalization score

Update `work/pipeline-state.json` with new batch number.

## Writing Rules (NON-NEGOTIABLE)
- NO em dashes (—). Use commas or short hyphens.
- NO "I noticed" / "I saw" / "reaching out" / "wanted to connect"
- NO role-at-company opener ("Seeing that you're the...")
- NO feature-led framing (don't lead with AI/self-healing)
- NO bullet-point feature lists
- NO permission-based CTAs ("happy to share if helpful")
- Under 120 words for Touch 1 (sweet spot 80-99)
- Exactly 2 question marks in Touch 1
- Different proof point per touch for same prospect
- Must sound like Rob wrote it, not AI
- "What day works" CTA tied to proof point outcome

## Reference files
- `memory/context/sales-playbook.md` - Pain hooks and proof points
- `memory/competitors/` - Battle cards for objection handling
