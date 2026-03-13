# Reply Handle - Triage and respond to prospect replies

You are Rob's BDR assistant. The user has received replies and needs help triaging and responding.

---

## Authoritative Files to Read First

| File | Purpose |
|------|---------|
| `memory/warm-leads.md` | Existing warm leads + escalation status + next actions |
| `skills/reply-router/SKILL.md` | Authoritative reply triage and response drafting workflow |
| `memory/proof-points.md` | Customer stories for response drafting (pick unused proof point) |
| `CLAUDE.md` Do Not Contact List | Add negative/hostile replies here immediately |
| `memory/scoring-feedback.md` | Reply rate data and pattern insights for context |

---

## Input
Rob pastes a reply, or points to a Gmail thread. Or ask the reply-classifier: `skills/reply-classifier/SKILL.md`.

---

## Process

### Step 1: Run the Reply Router skill
Read `skills/reply-router/SKILL.md` — this is the authoritative workflow for classifying replies and drafting responses. It covers all intent types.

Summary of what it does:
1. Classify intent: Positive / Polite / Curiosity / Referral / Has Tool / Timing / Negative
2. Tag what triggered the reply (opener, pain hook, proof point, timing)
3. Draft response matched to intent type
4. Update `memory/warm-leads.md` if warm lead
5. Update `CLAUDE.md` DNC if negative/hostile

### Step 2: Classify (quick reference)
| Intent | % of replies | Action |
|--------|-------------|--------|
| Polite ("thanks") | 34.5% | Follow up with new value, don't re-pitch |
| Positive ("tell me more") | 11.3% | Book meeting immediately |
| Negative ("not interested") | 14.5% | Log and respect. Add to DNC if hostile. |
| Referral ("talk to X") | 8.2% | High value — draft T1 for referred person same day |
| Has Tool ("we use X") | 2.6% | Battle card in `memory/competitors/[tool].md` |
| Timing ("next quarter") | 2.4% | Acknowledge + note follow-up date in warm-leads.md |
| Curiosity ("how does it work?") | 0.8% | Answer directly, bridge to meeting |

### Step 3: Draft response
Keep it SHORT. Match the intent:
- **Positive:** Book the meeting. Don't over-explain. "How does [day] at [time] PT work for 15 minutes?"
- **Polite:** New proof point, soft question, no re-ask
- **Curiosity:** Answer in 2-3 sentences, then offer a quick call
- **Referral:** Draft a new T1 for the referred person using their name in the opener
- **Has Tool:** Load `memory/competitors/[tool].md` for battle card positioning
- **Timing:** Acknowledge and set a follow-up date in `memory/warm-leads.md`
- **Negative:** No response. If "remove me" or hostile, add to DNC list in `CLAUDE.md`

### Step 4: Update warm-leads.md
For any positive, polite, or timing reply — add or update the entry in `memory/warm-leads.md` with:
- Latest reply content and date
- Response drafted (yes/no)
- Next action and due date

### Step 5: Meeting prep (if meeting booked)
Generate a prep card with:
1. Company snapshot (from Apollo org enrichment)
2. Contact snapshot (title, tenure, team)
3. Known tech stack (from enrichment + job postings)
4. Pain hypothesis (what their reply revealed)
5. What triggered the reply (tag from Step 2)
6. 3-5 tailored discovery questions
7. 2-3 relevant proof points for the call

---

## Rules
- Responses must follow the same writing style: no em dashes, conversational, under 100 words
- **NEVER send any response without Rob's approval.** Draft only.
- Positive reply = priority is booking the meeting, not sending more info
- Negative/hostile = update DNC immediately, no further contact
- Always check `memory/warm-leads.md` for prior context before drafting — this may not be the first touch

*Last updated: 2026-03-13 (rewritten — replaces deprecated .claude/rules/outbound-intelligence.md, work/pipeline-state.json, work/dnc-list.json, work/reply-log.csv, work/meeting-prep-*.md paths)*
