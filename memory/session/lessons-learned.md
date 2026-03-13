# Lessons Learned — BDR Second Brain

High-level patterns and insights from 31+ sessions of running the TAM Outbound workflow. These aren't rules (those are in CLAUDE.md) — they're the "why" behind the rules and observations that didn't fit cleanly into an incident.

---

## Session Architecture

**One-session batch builds are too long.**
Sessions 4-15 tried to source + research + draft + QA + enroll in a single context window. Context budget ran out before completion, forcing incomplete handoffs. Sessions 20+ split the work: source → (optional break) → research + draft → (separate session for) enroll + send. This is more reliable.

**Playbook reads at startup are expensive but necessary.**
Skipping playbook reads to save context caused repeated errors (wrong cadence, non-standard batch names, missed dedup steps). The cost of a playbook read is ~500-1,000 tokens; the cost of a mistake is an incident + 30+ minutes of recovery. Always read the playbook.

**The 14-step startup protocol emerged from failures.**
Steps 1-7 were added after sessions started without context. Steps 8-10 were added after parallel session conflicts. Steps 11-14 were added after warm leads sat cold for >24 hours. Every step has a reason — don't skip.

---

## Outreach Performance

**75-99 words consistently outperforms shorter or longer.**
Empirically validated: 39.0% reply rate at 75-99 words. Under 75 words feels incomplete; over 120 words gets skimmed. The sweet spot is 80-95 words.

**"What day works?" closes more meetings than any alternative.**
40.4% reply rate. "Would it make sense to chat?" and "Let me know if you're open" are both materially weaker. This is not up for debate.

**SMYKM (So, Maybe You Know Me?) openers outperform "I noticed" by 13+ percentage points.**
"I noticed" framing signals surveillance, which triggers aversion. SMYKM signals peer-to-peer connection. See HC1 in data-rules.md.

**Proof point specificity matters more than recency.**
"Cut regression testing 8→5 weeks" (Hansard) outperforms vague claims like "saved hours of testing." The number is what makes it credible.

**Architects and Senior SDETs are underpriced.**
39.3% reply rate vs. 26.8% for QA Managers. Most BDR motions target managers; SDETs are less saturated and often have more technical credibility to drive internal decisions. Over-index on this persona.

---

## Apollo Operations

**Apollo's task queue is not instant.**
After enrollment, Step 1 tasks appear in the Tasks tab within 5-30 minutes, not immediately. Don't poll Apollo frantically — check once, note the count, check again in 10 minutes.

**Quill DOM injection causes wrong-body sends.**
Three separate incidents (INC-007, INC-008, INC-012) traced to dangerouslyPasteHTML injecting content that Quill renders but Apollo doesn't capture in the send payload. Always use the JS readback gate before clicking Send Now.

**Enrollment overrides are often needed and safe to use when appropriate.**
`sequence_active_in_other_campaigns: true` and `sequence_finished_in_other_campaigns: true` are the two most common. They're not errors — they're expected for contacts who've been in other sequences. Document which contacts used overrides in the batch tracker and MASTER_SENT_LIST.

**Apollo ownership conflicts are a recurring blocker.**
INC-003, INC-004, plus multiple one-off cases. Ownership conflicts (another rep "owns" the contact in Apollo) require manual reassignment in the Apollo UI — this cannot be done via API. Always flag to Rob; don't try to work around it.

---

## Data Management

**MASTER_SENT_LIST.csv is the foundation. Keep it clean.**
Every dedup failure that caused a duplicate send was because a contact wasn't in MASTER_SENT_LIST, or was under a slightly different name. The grep dedup check takes 10 seconds and has prevented every duplicate since Session 10.

**Bounce rate at 11% is high but manageable.**
Humana (100%), Commvault (40%), Mastercard (25%) all have high corporate email bounce rates. This is a known issue with large enterprise IT security. Run Apollo enrichment and check email status before enrolling. "Likely to engage" is better than "verified" for Fortune 500 — paradoxically, "verified" often goes to generic inboxes that bounce.

**Company domain is the most reliable dedup key — not name.**
"John Smith (Accenture)" and "John Smith (Accenture Digital)" might be the same person. Cross-reference company domain against tam-accounts-mar26.csv domain column, not just the company name string.

---

## Session Coordination

**Parallel sessions work when file conflicts are avoided.**
Sessions 28-30 ran concurrently and completed without conflicts because they claimed different companies and used file locks. The collision in Session 29 (unregistered session) showed the system works — but only when everyone registers.

**Warm leads go cold faster than any other metric.**
A reply that gets a response within 2 hours has a 3-5x higher booking rate than one that waits 24 hours. Same-session response is the gold standard. "I'll respond next session" is almost always a mistake.

**Handoff.md staleness is the #1 source of session confusion.**
Sessions that arrived to a stale handoff spent 20-30 minutes reconstructing pipeline state from git log and batch trackers. A 5-minute handoff update at session end saves 20-30 minutes at the next session start. Do it every time.

---

## Optimization Wins

**Skill system reduced per-session setup time by ~30%.**
Pre-skill (Sessions 1-20): 45-60 minutes to configure and start a batch. Post-skill (Sessions 21+): 20-30 minutes. The enrichment-pipeline → compliance-gate → draft-qa chain is the key efficiency unlock.

**Error-recovery.md eliminated repeated debugging.**
Before the playbook existed, sessions 1-15 re-diagnosed the same Apollo errors repeatedly (UI crashes, enrollment failures, task queue issues). Adding the playbook in Session 16 made every subsequent session self-service for common errors.

**Batch tracker HTML files as source of truth for T2 work.**
The pattern of embedding T1 drafts + research + proof points in the tracker HTML means T2 sessions have everything they need without reading raw research files. This design decision (Session 10) cascaded into better T2 quality and faster T2 drafting.

---

## What Hasn't Worked

**Open Sales Nav searches for prospecting.**
Suspended Mar 9, 2026 after repeated off-TAM contacts slipped through. All prospecting must start from tam-accounts-mar26.csv or target-accounts.md. See INC-010.

**Batch sizes over 50 in one session.**
Sessions that tried to build 60-80 contact batches hit context budget limits mid-research and produced incomplete or rushed drafts. 25-35 per session is the reliable range; 40-50 is possible with good focus.

**Pre-completing T3 drafts.**
Session 14 pre-drafted T3s for all Wave 1 contacts before Day 9. By Day 9, 3 of the 23 contacts had replied (warm leads requiring different messaging) and 2 had hard-bounced. The pre-drafts were wasted work. T3s should only be drafted close to the due date.

---

*Last updated: 2026-03-13 (Session 32 — initial creation from patterns across Sessions 1-31)*
*Update this file at the end of any session where a significant new pattern emerges.*
