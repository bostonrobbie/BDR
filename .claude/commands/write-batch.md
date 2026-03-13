# Write Batch - Research prospects and draft all outreach touches

You are Rob's BDR assistant. The user wants to research prospects and write personalized T1 email outreach.

**This command delegates to the current skill system. Do NOT reference the old file paths below — they no longer exist.**

---

## Authoritative Files to Read First

| File | Purpose |
|------|---------|
| `memory/sop-tam-outbound.md` Parts 5-8 | Research protocol, T1 draft formula, QA gate, T2 formula |
| `memory/playbooks/qa-gate.md` | 12-point MQS scoring rubric |
| `memory/playbooks/batch-tracker-html.md` | HTML tracker format for the deliverable |
| `memory/proof-points.md` | Customer stories + stats by vertical |
| `memory/data-rules.md` | Hard Constraints (HC1-HC10) + Strong Preferences |
| `CLAUDE.md` Do Not Contact List | DNC check before writing anyone |
| `memory/target-accounts.md` | Proof point rotation — which stories already used per account |

---

## Process

### Step 1: Run the full TAM T1 Batch skill
Read `skills/tam-t1-batch/SKILL.md` — this is the authoritative end-to-end workflow. It orchestrates:
- `skills/enrichment-pipeline/SKILL.md` — sourcing + dedup + enrichment
- `skills/compliance-gate/SKILL.md` — 8-point pre-enrollment safety check
- `skills/draft-qa/SKILL.md` — automated MQS scoring

### Step 2: Research (per prospect)
Per `sop-tam-outbound.md` Part 5:
1. Apollo org enrichment — employee count, industry, tech stack, revenue
2. LinkedIn scan — team structure, QA job postings, tenure of target contact
3. Job posting analysis — signals about QA pain (manual testing, hiring automation, Selenium migration)
4. News scan — funding rounds, reorgs, product launches

Tag each research bullet with which message element it feeds (opener/proof point/CTA angle).

### Step 3: Draft T1 emails
Per `memory/sop-tam-outbound.md` Part 6 and `memory/data-rules.md`:
- **Subject (SMYKM):** Situation-based question, 5-8 words, no company name
- **Structure:** Opener (QA situation hook) → Context (why it matters) → Proof point (1, matched to vertical) → Close ("What day works" tied to proof point outcome)
- **Word count:** 75-99 words (39.0% reply rate sweet spot)
- **Exactly 2 question marks** in the body
- **Hard rules:** No em dashes. No "I noticed/I saw/reaching out/wanted to connect". No feature-led framing. No bullet lists.

### Step 4: QA Gate (HARD GATE — no exceptions)
Read `skills/draft-qa/SKILL.md` and score every T1 before including it.
- **Pass:** MQS ≥ 9/12 → include
- **Rewrite:** MQS 7-8 → fix flagged dimensions, re-score
- **Reject:** MQS < 7 → start over with a new angle
- **Any HC violation (HC1-HC10)** → auto-fail regardless of score

Do NOT skip automated scoring. If in doubt, use the 4-dimension rubric in `memory/playbooks/qa-gate.md`.

### Step 5: Build batch tracker HTML
Per `memory/playbooks/batch-tracker-html.md`:
- File naming: `tamob-batch-{YYYYMMDD}-{N}.html`
- One section per contact with T1 draft, proof point used, research summary, T2 placeholder
- Add to `batch-trackers-index.csv` after saving

### Step 6: Present BATCH SUMMARY to Rob
Wait for **APPROVE SEND** before any enrollment or sending.

Show:
- Total contacts, company list, vertical mix
- Proof points used (rotation check — no same proof point twice in batch)
- QA Gate scores
- Batch file name and row count for MASTER_SENT_LIST

---

## Writing Rules (NON-NEGOTIABLE)
- NO em dashes (—). Use commas.
- NO "I noticed" / "I saw" / "reaching out" / "wanted to connect"
- NO role-at-company opener ("Seeing that you're the...")
- NO feature-led framing (don't open with AI/self-healing/NLP)
- NO bullet-point feature lists
- NO permission-based CTAs ("happy to share if helpful")
- Under 120 words for T1 (sweet spot 75-99)
- Exactly 2 question marks in T1
- Different proof point per touch for same prospect
- Must sound like Rob wrote it, not AI
- "What day works" CTA tied to proof point outcome

*Last updated: 2026-03-13 (rewritten to reference current skill + SOP architecture — replaces old config/vertical_pains.json, config/product_config.json, work/pipeline-state.json paths)*
