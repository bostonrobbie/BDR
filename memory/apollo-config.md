# Apollo Configuration & Email SOP

## Apollo Account Status
- **Lead Credits:** ~6,879 remaining / 7,104 effective
- **Direct Dial Credits:** 600 available
- **AI Credits:** 50 million available
- **Email Accounts Linked:** 4

## Rob's Apollo Email Accounts
| Email | ID | Default |
|-------|-----|---------|
| robert.gorham@testsigma.in | 68f65ae5b705750019748b3e | No |
| robert.gorham@testsigma.net | 68f65bdf998c4c0015f3446a | Yes |
| robert.gorham@testsigmatech.in | 68f65c12ce7de000192da2e3 | No |
| robert.gorham@testsigmaweb.com | 68f65c3af5fce700197d4f4c | No |

## Rob's Apollo Owner ID
`68e16f05978e5e000d10a621`

## Active Sequences
| Sequence | ID | Steps | Purpose | Contacts |
|----------|-----|-------|---------|----------|
| LinkedIn Outbound - Q1 Priority Accounts | 69a05801fdd140001d3fc014 | 3 | PRIMARY for ALL outbound. All manual steps. | 311 enrolled (26 added Mar 6 from Q1 QA Outreach migration) |
| Email Outbound - Website Visitor Tier 1 | 69a1b3564fa5fa001152eb66 | 3 | Email-only buyer intent. | 78 active |

### LinkedIn Outbound - Q1 Priority Accounts Step Details (Updated Mar 8, 2026)
- Step 1 (69a05a3883eda10021b7ff0b): LinkedIn InMail (Day 1, High)
- Step 2 (69a05a3883eda10021b7ff0d): **Manual Email** (Day 5, High) ← changed from LinkedIn InMail Follow-up
- Step 3 (69a05a3883eda10021b7ff0f): **LinkedIn Connection Request** (Day 10, Medium) ← changed from LinkedIn send message (Day 30)
- ALL steps are MANUAL. Nothing auto-sends. (Step 2 is "Action item" type in Apollo — no native email step type available.)

**Rationale for change (Mar 8):** T2 InMails cost 1 credit each for 2nd/3rd degree (confirmed via live testing). Credits are scarce and reserved for T1s. Email is free with +37% multi-channel lift (Gong). LI Connection Request as T3 moves prospect to 1st degree — future DMs then free. See `memory/sop-outreach.md` for full sequence policy.

## Retired Sequences (DO NOT USE)
| Sequence | ID | Reason |
|----------|-----|--------|
| Q1 QA Outreach - US | 699f4089628b940011da7fb7 | Fully resolved Mar 6. 26 clean contacts moved to LinkedIn Outbound. 5 deferred (same-company). Sequence archived. |
| Rob Outbound | 68f2723ef174870019958d31 | Legacy. 0.25% reply rate. |
| Eshwar - Rob Outbound | 6915ec4bac6f93000da91dab | Legacy reference only. |

## Which Sequence for Which Prospect
| Type | Sequence |
|------|----------|
| Cold outbound (all batches) | LinkedIn Outbound - Q1 Priority Accounts |
| Intent/transferred accounts | LinkedIn Outbound - Q1 Priority Accounts |
| Website demo / high-intent inbound | Email Outbound - Website Visitor Tier 1 |
| Warm lead reply / meeting booked | Do NOT enroll. Handle manually. |

## Enrollment Rules
- Enroll AFTER Rob approves all messages in batch tracker
- Enroll in batches of 5 (larger batches cause 500 errors)
- Default email: robert.gorham@testsigma.net (68f65bdf998c4c0015f3446a)
- Always use flags: `sequence_no_email: true`, `sequence_active_in_other_campaigns: true`
- For contacts who finished other campaigns: add `sequence_finished_in_other_campaigns: true`
- For contacts with job changes: add `sequence_job_change: true`

## Credit Budget Per Batch (25 prospects)
| Action | Credits |
|--------|---------|
| Person Enrichment | 25 |
| Organization Enrichment | ~15-20 |
| Contact Creation | Free |
| Sequence Enrollment | Free |
| **Total** | **~40-45** |

## 6-Month Dedup Protocol
Before enrolling ANY prospect:
1. Search Apollo contacts by company domain
2. Search previous batch trackers
3. Check Gmail for prior threads
4. If another BDR has activity from Nov 2025 onward: STOP, ask Rob
5. If prior contact >6 months old: safe, note as "Re-engagement"
6. Rob's own sequences are always safe to re-enroll

---

## Email-Only Sequence SOP (Team-Wide)

### Email-Specific Constraints
| # | Constraint |
|---|-----------|
| EC1 | Touch 1 email: max 100w (Standard) or 120w (SMYKM) |
| EC2 | Follow-up emails: max 70w |
| EC3 | Subjects: 5-6 words problem-framed OR SMYKM personal (up to 8 words) |
| EC4 | 1-2 question marks |
| EC5 | No "circling back" or "following up on my last email" |
| EC6 | SMYKM subjects need unique professional detail, not just title |
| EC7 | SMYKM opener must be HC1-compliant |

### 5-Touch 21-Day Email Cadence
| Touch | Day | Type | Words |
|-------|-----|------|-------|
| 1 | Day 1 | Problem Hook | 60-100 |
| 2 | Day 4 | Value Add | 40-70 |
| 3 | Day 9 | Social Proof | 60-100 |
| 4 | Day 14 | Trigger/Timely | 40-70 |
| 5 | Day 21 | Direct Ask | 40-60 |

### SMYKM Framework (Email Channel Only)
Core principle: Subject line and first sentence must prove real research on THIS person. Not company, not industry, THEM.

**SMYKM Subject Lines:**
- GOOD: "Namita's QA coverage at OverDrive"
- GOOD: "The Libby migration testing, Namita"
- BAD: "Regression eating release time?" (problem-framed, not SMYKM)
- BAD: "QA Manager at Acme" (title-only, not unique)

**SMYKM Openers (HC1-compliant):**
- "We have yet to be properly introduced, but I'm Rob with Testsigma."
- Lead directly with challenge observation.
- NEVER: "I noticed," "I saw," "Based on your profile."

**SMYKM Challenge-Narrative:**
Embed proof point inside challenge description: "The challenge [type of team] hits is [problem]. [Customer] was dealing with the same thing and [outcome]."

### Email Subject Line Patterns
| Pattern | Example | Structure |
|---------|---------|-----------|
| Problem-framed | "Regression eating release time?" | Standard |
| Outcome-framed | "3 fewer weeks of regression" | Standard |
| Question format | "What breaks first after the migration?" | Standard |
| Domain-specific | "QA coverage for the payments platform" | Standard |
| SMYKM Personal | "Namita's QA coverage at OverDrive" | SMYKM |
| SMYKM Event | "The Libby migration testing, Namita" | SMYKM |

BANNED: "Quick question", "Following up", >8 words, clickbait, all-caps.

### Email Template IDs (from TEMPLATE_LIBRARY.md v2.0)
| Template | Pain Hook | Touch |
|----------|-----------|-------|
| EM-1 | Test Maintenance | Touch 1 |
| EM-2 | Release Velocity | Touch 1 |
| EM-3 | Coverage/Scale | Touch 1 |
| EM-4 | Tool Migration | Touch 1 |
| EM-5 | Trigger Event | Touch 1 |
| EM-FU-1 | New Proof Point | Touch 2-3 |
| EM-FU-2 | Capability Match | Touch 2-3 |
| EM-FU-3 | Industry Angle | Touch 4 |
| EM-FU-4 | Direct Ask | Touch 5 |
| EM-SMYKM-1 to 4 | SMYKM variants | Touch 1 |
