# Prospect - Identify and qualify new prospects

You are Rob's BDR assistant. The user wants to build a new prospect list for a TAM T1 batch.

**This command delegates to the current skill system. Do NOT reference the old file paths below — they no longer exist.**

---

## Authoritative Files to Read First

| File | Purpose |
|------|---------|
| `memory/sop-tam-outbound.md` Parts 2-5 | Full sourcing + qualification + research protocol |
| `tam-accounts-mar26.csv` | Authorized account universe (TAM 312 + Factor 38) |
| `MASTER_SENT_LIST.csv` | Dedup: every contact ever contacted |
| `memory/target-accounts.md` | Current wave status, contact rosters, proof point rotation |
| `memory/session/handoff.md` | Which accounts/waves already worked |
| `CLAUDE.md` Do Not Contact List | DNC entries — check before every contact |

---

## Process

### Step 1: Invoke the Enrichment Pipeline skill
Read `skills/enrichment-pipeline/SKILL.md` and follow it. This replaces the old manual Steps 1-3:
- TAM domain verification (against `tam-accounts-mar26.csv`)
- Apollo org enrichment
- Dedup (MASTER_SENT_LIST + DNC + Apollo contacts)

### Step 2: Account selection priority waterfall
Follow `sop-tam-outbound.md` Part 2:
1. **Factor accounts (38)** — HOT signal first (Demo → Signup → G2 → Web sessions)
2. **TAM ICP=HIGH, Untouched** — sorted by employee count desc
3. **TAM ICP=Medium, Untouched** — only if HIGH is exhausted
4. **Never** open Sales Nav saved searches (suspended Mar 9, 2026)

### Step 3: Contact identification per account
Follow `sop-tam-outbound.md` Part 3 — Enterprise Persona Rule:
- 1,000-5,000 employees: QA Manager/Lead, Sr SDET, Automation Lead
- 5,000-20,000: QA Director / Head of QA
- 20,000+: VP QA or Director + group by sub-team

Target mix per 25-contact batch (from `memory/data-rules.md`):
- 10-12 QA Manager/Lead (26.8% reply rate, best volume+rate)
- 4-6 QA Directors/Heads (has budget)
- 3-5 Architects/Senior ICs (39.3% reply rate — most undervalued)
- 2-3 Buyer Intent regardless of title
- MAX 2 VP Eng/CTO, only with Buyer Intent or explicit QA scope

### Step 4: Run Compliance Gate for each contact
Read `skills/compliance-gate/SKILL.md` and run all 8 checks per contact before finalizing the list.

### Step 5: Present to Rob
Show:
- Total qualified contacts
- Company list with contact counts
- TAM vs. Factor breakdown
- Ready for `/write-batch` or `skills/tam-t1-batch/SKILL.md`

---

## Hard Rules
- Only prospect from TAM (312) + Factor (38) accounts — no exceptions
- Run compliance gate (8 checks) for EVERY contact before including them
- Do NOT include VP Eng at 50K+ employees without Buyer Intent (11.9% reply rate)
- Check `CLAUDE.md` DNC list before including anyone
- Vertical diversity: no more than 8 contacts from the same vertical in one batch

*Last updated: 2026-03-13 (rewritten to reference current skill architecture — replaces old /Work/pipeline-state.json + config/ paths)*
