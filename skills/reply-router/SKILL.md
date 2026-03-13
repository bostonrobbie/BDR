# Reply Router — Draft Response Based on Reply Type

## Description
When a reply comes in (from `skills/reply-classifier/SKILL.md` or Rob directly), routes to the correct Google Drive objection doc, pulls the relevant talk track, and drafts a response using the right framework. All drafts go to Rob for review. Nothing is ever sent without APPROVE SEND.

## Trigger
- Called by `skills/reply-classifier/SKILL.md` when a reply is classified
- Run on-demand: "draft reply for [name]", "how should I respond to [reply]", "handle this objection"
- Rob pastes a reply and says "help me respond to this"

## Note on Playbooks
> **Index-first rule:** Before loading objection docs or playbooks, check `memory/playbooks/_index.md` to confirm which file handles your specific reply type.

## ⛔ APPROVE SEND RULE
This skill DRAFTS ONLY. It does NOT send anything. Rob reviews every draft and sends manually via Apollo UI or Gmail. "APPROVE SEND ≠ APPROVE CLICK" — content approval and sending are two separate steps. NEVER use Gmail MCP to send.

---

## Route 1: Positive Reply (interested, wants meeting)

**Google Drive doc:** Simple Talk Tracks (`1lZhfvmxGfI12F64PCtejpHSdWOX_dI0gwr5MV3mGFgA`)

**Draft framework (under 60 words):**
1. Mirror their language — acknowledge specifically what they said
2. One proof point matched to their stated interest (different from T1 if possible)
3. Meeting ask: "What day works this week?" or propose 2-3 specific times

**Rules:**
- Respond within 2 hours of Rob seeing it (per `memory/warm-leads.md` SLA)
- No feature dumping — they're already interested, don't overwhelm
- Generate meeting prep card after meeting is booked (per `memory/scoring-feedback.md` template)
- Update `memory/warm-leads.md` with the reply details

---

## Route 2: Curiosity Reply (asking product questions)

**Google Drive doc:** Product Objections (`1EDmrZO9ZK1rpYTMlZD1oL2DxtZIYrJY3UO9B_MRQkJU`)

**Draft framework (under 80 words):**
1. Answer their specific question directly first (2-3 sentences) — don't redirect without answering
2. One proof point that demonstrates the answer with numbers
3. Bridge to meeting: "Easier to show you in 15 minutes. What day works?"

**Special case — pricing question:**
"Depends on your team size and scope. Quick call would help me give you accurate numbers."

---

## Route 3: Referral Reply (pointing to someone else)

**Google Drive doc:** Persona Battle Cards (`1dqNe_q1RXuzXs4OD0TIEJwkplHk1UwabNQGIL3vpEOg`)

**Two separate drafts needed:**

**Draft A — Thank referrer (1-2 lines, send via Gmail):**
"Thanks for pointing me to [referred name], [first name]. Really appreciate it."

**Draft B — Outreach to referred person:**
1. Research the referred person first: `apollo_contacts_search` q_keywords="{name} {company}"
2. Run compliance gate on referred person (check DNC, MASTER_SENT_LIST, TAM domain)
3. Match to persona battle card based on their title
4. Draft: "Hi [name], [referrer] suggested I reach out. [Your company] [concrete company fact]..."
5. Softer CTA: "Would a quick call make sense?" (NOT "What day works" — too forward for cold referral)

**APPROVE SEND required for both drafts separately.**

Real example: If Seth Drummond at Fidelity refers us to Chris Pendergast, Draft A goes back to Seth, Draft B goes to Chris. Both need Rob's approval.

---

## Route 4: Timing Objection ("not now", "next quarter")

**Google Drive doc:** Full-Funnel BDR Scripts (`1yXGKZvy-7o78BxawYjng9H-F7DCBiQaudCZssgMlbjo`)

**Draft framework:**
1. Acknowledge timing: "Totally makes sense."
2. One brief insight or stat (plant a seed, don't pitch)
3. Set expectation: "I'll check back in [timeframe]. In the meantime, [light value offer — relevant article or case study]."

**Actions:** Log re-engagement date in `memory/warm-leads.md`. Add task to work-queue.md.

---

## Route 5: Has a Tool ("we use Selenium/Cypress/etc.")

**Google Drive doc:** Competitor Comparisons (`1yFYzrb1FdCOzI9FoVcN2MyfI_vfLOqGy-79SLgjJ0Kc`)

Identify the tool, then pull the comparison angle:

| Tool | Key comparison angle |
|------|---------------------|
| Selenium | Maintenance burden, brittle locators, high upkeep cost |
| Cypress | Cross-browser gaps, component-only focus, no mobile |
| Playwright | Maintenance at scale, non-coder accessibility gap |
| Katalon | AI capabilities, enterprise scale |
| TestComplete | Cost, modernization |
| Tricentis | Cost, complexity, AI coverage discovery |
| BrowserStack / Sauce Labs | Infrastructure only, not automation — Testsigma does both |
| mabl | (Rob's former company — handle with care, don't disparage) |

**Draft framework:**
1. Acknowledge the tool: "[Tool] is solid for [what it's genuinely good at]."
2. Name the gap: "Where teams usually hit a wall is [specific pain point tied to their company]."
3. Social proof: "[Customer] was using [similar approach] before."
4. Low-pressure ask: "If [gap] ever becomes a pain point, what day works for a quick look at how [customer] solved it?"

---

## Route 6: Negative Reply ("not interested")

**No external doc needed.**

**If polite decline:**
Draft: "Appreciate you letting me know, [first name]. If anything changes on the testing front, I'm around."

**If explicit removal request:**
Do NOT draft a response. Flag to Rob: "Recommend DNC addition for [name]. Awaiting your approval."
Rob must explicitly approve before modifying `CLAUDE.md` DNC list.

**If hostile:**
No response. Flag to Rob. Recommend DNC.

Real examples:
- Abe Blanco (Kapitus) replied "not interested" Mar 4 — DNC added
- Sanjay Singh (ServiceTitan) — hostile reply in mabl era — DNC permanent

---

## Route 7: OOO / Auto-reply

No response needed. Actions:
1. Extract return date if stated ("returning [date]")
2. Log: "OOO: [Name] returning [date]. Next touch after return + 2 business days."
3. Update `contact-lifecycle.md` if the contact has a record

---

## Route 8: Bounce / Delivery Failure

No response needed. Actions:
1. Flag email as invalid in the batch tracker HTML and `contact-lifecycle.md`
2. Search Apollo for alternate: `apollo_contacts_search` q_keywords="{name} {company}"
3. If alternate found: Present to Rob — "Found alternate email [email] for [Name]. Proceed with re-send?"
4. If no alternate: Move to backlog. Note in MASTER_SENT_LIST if possible.
5. If hard bounce (SMTP 550) and in Apollo sequence: Tell Rob to manually remove from sequence

---

## Output Format

```
REPLY ROUTER: Pallavi Sheshadri @ Origami Risk
Classification: Positive (replied to premature T3 — INC-001)
Route: Positive → Schedule meeting
Doc: Simple Talk Tracks (1lZhfvmxGfI12F64PCtejpHSdWOX_dI0gwr5MV3mGFgA)

CONTEXT:
  Original outreach: Premature Touch 3 email (Feb 28 — INC-001 incident)
  Her reply: [content from warm-leads.md]
  Rob's follow-up: Sent Mar 2 — Hansard proof point, "what day works" CTA
  Status: Awaiting reply to Rob's Mar 2 follow-up

DRAFT RESPONSE (if no reply by Mar 7):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Subject: Re: [original subject]

Hi Pallavi,

[lighter nudge — shorter, references Mar 2 note]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
47 words | 1 question mark | Conversational

⛔ AWAITING ROB'S APPROVE SEND BEFORE ANY ACTION

RECOMMENDED ACTIONS:
  □ Update warm-leads.md: Stage = monitoring, next check Mar 9
  □ Do not draft T3 — still in active monitoring
```

---

## Integration Points
- Called by: `skills/reply-classifier/SKILL.md` (after classification)
- Reads: Google Drive docs via MCP, `memory/proof-points.md`, `memory/warm-leads.md`, `memory/data-rules.md`
- Outputs: Draft response for Rob's review (NEVER auto-sends)
- Updates: `memory/warm-leads.md`, `memory/contact-lifecycle.md`

**Google Drive doc IDs:**
- Product objections: `1EDmrZO9ZK1rpYTMlZD1oL2DxtZIYrJY3UO9B_MRQkJU`
- Competitor comparisons: `1yFYzrb1FdCOzI9FoVcN2MyfI_vfLOqGy-79SLgjJ0Kc`
- Persona battle cards: `1dqNe_q1RXuzXs4OD0TIEJwkplHk1UwabNQGIL3vpEOg`
- Simple talk tracks: `1lZhfvmxGfI12F64PCtejpHSdWOX_dI0gwr5MV3mGFgA`
- Trigger event playbook: `1e9DDmuOFtd9MgB1ol3MOJklzrq3vZn5oyevM6FAj_7I`
- AI objections: `1kGN-3bfmrFUclqIKCPky-eJ6ikqJYEBTApldxKiwCw4`
- Security objections: `1NAZqKAYKKLvJSo11kGxflqhvORW0BWXp0f7xGP1h0YQ`
- Full-funnel BDR scripts: `1yXGKZvy-7o78BxawYjng9H-F7DCBiQaudCZssgMlbjo`

*Source: `memory/warm-leads.md` + `memory/sop-email.md` + `CLAUDE.md` (Google Drive Knowledge Base)*
*Last updated: 2026-03-12 (Session 30)*
