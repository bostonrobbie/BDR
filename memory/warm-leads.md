# Warm Leads & Inbound SOP

## Warm Lead Response Framework
| Source | Response Time |
|--------|--------------|
| InMail reply (positive) | Same day, within 2 hours |
| InMail reply (referral) | Same day to referred person |
| Website demo request | Within 4 hours |
| Buyer Intent | Next business day |
| Event/webinar attendee | Within 48 hours |

### Response Rules
1. Acknowledge fast. Mirror their language.
2. One proof point matched to their stated interest.
3. Bridge to meeting: "What day works this week?"
4. Auto-generate prep card when Meeting Booked.

### Referral Rules
1. Thank referrer (1-2 lines).
2. Research referred person (3-source pipeline).
3. Draft outreach mentioning referrer by name.
4. Softer CTA: "Would a quick call make sense?"

### Follow-Up Tracking
- Calendar reminder 2 business days out
- Second nudge if no response in 3 business days
- After 2 unanswered follow-ups: "Dormant - Was Warm"
- Re-engage only on new trigger event

### Escalation Rules (Added 2026-03-13)

**Stale Flag (7-day rule):** Any warm lead with a "Next Steps" date more than 7 days in the past is STALE. On session startup, the reply-classifier skill should flag stale warm leads. A stale warm lead must be reviewed before any new T1 batch work proceeds.

**Priority Escalation:**
| Lead Status | Action |
|-------------|--------|
| Positive reply / "tell me more" | P0 — respond same session, before any T1 work |
| Curiosity / question | P0 — draft response this session |
| Referral | P0 — draft T1 for referred person same session |
| Polite / "thanks" | P1 — respond within 24 hours |
| Timing / "next quarter" | P2 — set re-engage date, note trigger needed |
| No response after 2 follow-ups | Archive as "Dormant — Was Warm" |

**Re-Engage Schedule (post-dormancy):**
- Timing leads ("next quarter") → re-engage in 60-90 days with a trigger event (QA job posting, funding, product launch)
- Polite leads (no reply after 2 nudges) → re-engage in 30-45 days with a completely new angle
- Do NOT re-engage within 30 days of last touch regardless of category

**Lifecycle Cross-Reference:**
For any warm lead that proceeds to a meeting or advanced conversation, log the full timeline in `memory/contact-lifecycle.md`. The warm-leads.md entry serves as the trigger point; contact-lifecycle.md is the long-term record.

---

## Namita Jain — OverDrive
| Field | Detail |
|-------|--------|
| Title | Software Quality Assurance |
| Company | OverDrive (overdrive.com) |
| Email | njain@overdrive.com |
| Phone | +1 216-573-6886 |
| LinkedIn | linkedin.com/in/namita-jain-81b26b45 |
| Lead Type | Warm inbound (webinar engagement x2) |
| Priority | P1 |
| Apollo Org ID | 54a11f0f69702d8cccc4bf01 |

**Intent Signals:** Attended AUG 2025 webinar + registered FEB 2026 webinar.

**OverDrive Intel:** ~540 employees, $420M revenue, KKR-owned. 3 apps (Libby, Sora, Kanopy) on web+iOS+Android. Killed legacy app Jan 2025 (migration testing). Kanopy 41% user growth. Hiring QA Analyst. No visible automation tool.

**Proof Matches:** Medibuddy (2,500 tests, 50% cut), CRED (90% regression, 5X), Sanofi (3d→80min)

**Outreach Log:**
| Date | Channel | Touch | Status |
|------|---------|-------|--------|
| Feb 27 | Email | Touch 1 | SENT (coverage angle) |

**Next Steps:** Monitor for reply. If no reply by Mar 4: Draft Touch 2 LinkedIn InMail (Vega integration or QA hiring angle).

---

## Pallavi Sheshadri — Origami Risk
| Field | Detail |
|-------|--------|
| Title | QA (exact TBD) |
| Company | Origami Risk |
| Lead Type | Warm reply (responded to premature Touch 3) |
| Priority | P2 |

**Context:** Orphan from INC-001. Received premature Touch 3 email Feb 28. Replied. Rob sent follow-up Mar 2 at 12:41 PM (Hansard proof point, "what day works" CTA).

**Outreach Log:**
| Date | Channel | Status |
|------|---------|--------|
| Feb 28 | Email | PREMATURE Touch 3 (INC-001) |
| Mar 2 | Email (reply) | Rob's follow-up SENT |

**Next Steps:** Monitor for reply. If no reply by Mar 7: Draft lighter follow-up nudge (email, same thread). Complete LinkedIn + Apollo research.

---

## Re-Engagement Triggers
| Trigger | Action |
|---------|--------|
| Buyer Intent reactivates | New sequence, reference signal |
| New QA job posting | "Saw [Company] is hiring for QA..." |
| Leadership change | Reach out to NEW person |
| Funding raised | "Congrats on the round, scaling usually means scaling QA too." |
| Major product launch | "Saw the launch. Curious if testing effort was painful." |
| Testsigma ships feature | Re-engage with new capability |

Minimum 60 days between last touch and re-engagement. Must have NEW reason.
