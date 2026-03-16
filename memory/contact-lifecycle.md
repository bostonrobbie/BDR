# Contact Lifecycle Log

## Purpose
Unified contact history tracking every person from first enrichment through final outcome. Maintained by the `skills/lifecycle-tracker/SKILL.md` skill. Append-only for timeline events — stage fields can be updated but history is never deleted.

**Last updated:** 2026-03-12 (initialized)
**Total contacts tracked:** See MASTER_SENT_LIST.csv (495 rows as of Mar 12)

---

## Stage Reference

| Stage | Meaning |
|-------|---------|
| DISCOVERED | Found during prospecting, not yet enriched |
| ENRICHED | Apollo enrichment complete, email obtained |
| COMPLIANCE_CLEAR | Passed all 8 compliance checks |
| DRAFTED | T1 email drafted, pending QA |
| QA_PASS | Draft passed MQS gate |
| ENROLLED | Added to Apollo sequence |
| T1_SENT | First touch sent |
| T1_REPLIED | Replied to first touch |
| T2_SENT | Second touch sent |
| T2_REPLIED | Replied to second touch |
| T3_SENT | Third touch (connection request) sent |
| T3_REPLIED | Accepted or replied to T3 |
| MEETING_BOOKED | Meeting scheduled |
| MEETING_HELD | Meeting completed |
| OPPORTUNITY | Qualified opportunity in pipeline |
| CLOSED_WON | Deal closed |
| CLOSED_LOST | Deal lost |
| DORMANT | No response after full sequence, cooling down |
| DNC | Do Not Contact |
| BOUNCED | Email invalid, no alternate found |

---

## Active Warm Leads (High Priority — track here)

### Namita Jain — OverDrive
| Field | Value |
|-------|-------|
| Company | OverDrive |
| Domain | overdrive.com |
| Title | Software Quality Assurance |
| Email | njain@overdrive.com |
| Apollo Org ID | 54a11f0f69702d8cccc4bf01 |
| Account Type | TAM |
| Current Stage | T1_SENT |
| Lead Type | Warm inbound (webinar engagement x2) |
| Priority | P1 |

**Timeline:**
| Date | Event | Detail | Session |
|------|-------|--------|---------|
| Feb 27 | T1_SENT | Email — coverage angle | — |
| — | MONITORING | Awaiting reply, T2 InMail if no reply by Mar 4 | — |

---

### Stacey Schmidt — Vertafore
| Field | Value |
|-------|-------|
| Company | Vertafore |
| Domain | vertafore.com |
| Title | QA Manager |
| Email | sschmidt@vertafore.com |
| Apollo ID | 664daebc65e77601ebdaa628 |
| Account Type | TAM |
| Current Stage | ENROLLED (hold — re-engage Apr 24+) |
| Lead Type | Outbound T1 |
| Priority | — |
| Call Opt-Out | true |

**Timeline:**
| Date | Event | Detail | Session |
|------|-------|--------|---------|
| Feb 23, 2026 | Prior sequence ended | Campaign `6904f70577baa100190e4858` finished step 2. Sent from robert.gorham@testsigma.net. `inactive_reason: "talked on phone"` | Prior era |
| Mar 15, 2026 | ENROLLED | Added to Batch 10 / TAM Outbound sequence (Apollo override — active_in_other_campaigns) | 40 |
| Mar 15, 2026 | PULLED | Verified prior phone contact Feb 23 (20 days ago). Violates 60-day re-engage minimum. Rob decision: pull. `call_opted_out: true`. Do not send Monday. | 40 |
| Apr 24, 2026+ | RE-ENGAGE WINDOW OPENS | 60 days from Feb 23. Draft new T1. | — |

---

### Pallavi Sheshadri — Origami Risk
| Field | Value |
|-------|-------|
| Company | Origami Risk |
| Domain | origamirisk.com |
| Title | QA (TBD) |
| Current Stage | T1_REPLIED |
| Lead Type | Warm reply (responded to premature T3) |
| Priority | P2 |

**Timeline:**
| Date | Event | Detail | Session |
|------|-------|--------|---------|
| Feb 28 | T3_SENT | Premature Touch 3 email (INC-001 incident) | — |
| Feb 28 | T1_REPLIED | Replied to premature message | — |
| Mar 2 | FOLLOW_UP_SENT | Rob's follow-up reply sent — Hansard proof point, "what day works" CTA | — |
| — | MONITORING | Awaiting reply. If no reply by Mar 7: draft lighter nudge | — |

---

### Evely Perrella — Aetna/CVS Health
| Field | Value |
|-------|-------|
| Company | Aetna/CVS Health |
| Domain | aetna.com |
| Title | Leader Director Quality Assurance |
| Contact ID | 69b1dae03e09b90001402481 |
| Sequence | Inbound Leads - Rob Gorham (69b2ae589d6bd10017d4be89) |
| Current Stage | T1_SENT (error — INC-012) |
| Lead Type | Inbound — Google Ads branded search |
| Priority | P0 |

**Timeline:**
| Date | Event | Detail | Session |
|------|-------|--------|---------|
| Mar 12 | T1_SENT | WRONG BODY delivered (INC-012) — old template sent instead of approved V-C draft | — |
| Mar 12 | MANUAL_FOLLOW_UP | Rob sent correction/follow-up directly via Gmail | — |
| Mar 16 | T2_SKIP | Touch 2 due Mar 16 — SKIP. Rob already sent own follow-up | — |
| Mar 19 | T3_ELIGIBLE | First eligible re-contact. Personalize before sending. Needs Rob approval | — |

---

---

### Krystal Jackson-Lennon — TELUS
| Field | Value |
|-------|-------|
| Company | TELUS |
| Domain | telus.com |
| Title | Manager, Technology Strategy / SRE / Performance Engineering |
| Email | krystal.jackson-lennon@telus.com |
| Phone | +1 416-906-2317 |
| Apollo Contact ID | 699ca3b22f3aa6001115c940 |
| Current Stage | T1_REPLIED (inbound call ×4) |
| Lead Type | Inbound missed calls — called Rob back via Apollo dialer |
| Priority | P0 |

**Timeline:**
| Date | Event | Detail |
|------|-------|--------|
| Feb 23 | ENROLLED | TAM Outbound sequence |
| Mar 12 | INBOUND_CALL ×4 | Called Rob's Apollo dialer at 3:55-3:56 PM — MISSED. Sequence auto-finished with reason "talked on phone" |

---

### Mike Brown — TELUS
| Field | Value |
|-------|-------|
| Company | TELUS |
| Domain | telus.com |
| Title | Quality Assurance Manager |
| Email | mike.brown@telus.com |
| Phone | +1 604-999-8592 |
| Apollo Contact ID | 698e0fb3f82c890015cc6d36 |
| Current Stage | T1_REPLIED (inbound call ×2) |
| Lead Type | Inbound missed calls |
| Priority | P0 |

**Timeline:**
| Date | Event | Detail |
|------|-------|--------|
| Feb 12 | ENROLLED | TAM Outbound sequence |
| Mar 11 | INBOUND_CALL ×2 | Called at 3:25 PM and 3:40 PM — MISSED. Sequence finished "Completed last step" |

---

### Rajesh Ranjan — TELUS
| Field | Value |
|-------|-------|
| Company | TELUS |
| Domain | telusagcg.com (subdomain) |
| Title | Engineering Manager, Data Engineering & Analytics |
| Email | rajesh.ranjan@telusagcg.com |
| Phone | +1 647-936-7954 |
| Apollo Contact ID | 699ca29b9d3516001deb1e82 |
| Current Stage | T1_REPLIED (inbound call ×1) |
| Lead Type | Inbound missed call |
| Priority | P0 |

**Timeline:**
| Date | Event | Detail |
|------|-------|--------|
| Feb 23 | ENROLLED | TAM Outbound sequence |
| Mar 11 | INBOUND_CALL ×1 | Called at 3:00 PM — MISSED. Sequence still active at step 4 |

---

### Elias E. del Real — Anewgo
| Field | Value |
|-------|-------|
| Company | Anewgo |
| Domain | anewgo.com |
| Email | elias@anewgo.com |
| Current Stage | MEETING_BOOKED |
| Lead Type | Outbound → converted |
| Priority | P1 |

**Timeline:**
| Date | Event | Detail |
|------|-------|--------|
| Mar 12 | MEETING_BOOKED | Accepted calendar invite for Apr 13, 2026 12:00-12:15 PM EDT |
| Note | Bounce for elias@anugo.com was wrong domain typo — correct email is elias@anewgo.com |

---

### Zahidh Zubair — Citizens Bank
| Field | Value |
|-------|-------|
| Company | Citizens Bank |
| Email | zahidh.zubair@citizensaccess.com |
| Title | QA Lead |
| Apollo Contact ID | 69b2ef9378c0040011c67f3e |
| Current Stage | BOUNCED |

**Timeline:**
| Date | Event | Detail |
|------|-------|--------|
| Mar 12 | ENROLLED | TAM Outbound via robert.gorham@testsigma.com |
| Mar 12 | BOUNCED | Apollo marked failed/bounced — email to citizensbank.com domain undeliverable |
| Note | Apollo has citizensaccess.com as email domain — bounce suggests wrong domain was attempted |

---

### Sabrina Perry — EverBank
| Field | Value |
|-------|-------|
| Company | EverBank |
| Email | sabrina.perry@everbank.com |
| Title | Vice President Quality Assurance |
| Apollo Contact ID | 69b2f340c168d60015b5811a |
| Current Stage | BOUNCED (spam_blocked) |

**Timeline:**
| Date | Event | Detail |
|------|-------|--------|
| Mar 12 | ENROLLED | TAM Outbound via robert.gorham@testsigma.com |
| Mar 12 | BLOCKED | EverBank security policy (550 5.7.129) — restricted senders. Not a bad email, just blocked. |

---

### David Schraff — Cleveland Clinic
| Field | Value |
|-------|-------|
| Company | Cleveland Clinic |
| Email | schraffd@ccf.org |
| Title | Manager, Testing & QA Center of Excellence |
| Apollo Contact ID | 68cc65ca295c7b0001f11445 |
| Current Stage | BOUNCED |

**Timeline:**
| Date | Event | Detail |
|------|-------|--------|
| Mar 11 | ENROLLED | TAM Outbound via robert.gorham@testsigma.com |
| Mar 12 | BOUNCED | Cleveland Clinic messaging system returned delivery failure for schraffd@ccf.org |

---

## Bulk Contact Records

> **Note:** Full individual records for the 495 contacts in MASTER_SENT_LIST.csv are stored at the batch level. Run `skills/lifecycle-tracker/SKILL.md` to generate full per-contact records. The following represents a summary by batch.

### Batch Summary

| Batch | Contacts | Date | Channel | Stage | Notes |
|-------|----------|------|---------|-------|-------|
| Batch 1 | ~50 | Feb 23 | LinkedIn Connection | T3_SENT | From outreach-sent-feb13-batch1-v2.html |
| Batches 2-5B | ~200 | Feb-Mar | Mixed | T1/T2/T3 | Multiple waves |
| TAM Outbound Mar 12 | ~40 | Mar 12 | Email | ENROLLED/T1_SENT | tamob-batch files |
| Inbound Leads (bulk) | ~15 | Mar 12 | Email | ENROLLED | Salesforce inbound leads |

*Run the lifecycle-tracker skill to expand this into full contact-level records.*

---

## DNC Contacts (from CLAUDE.md)

| Name | Company | Stage | Reason | Date Added |
|------|---------|-------|--------|------------|
| Sanjay Singh | ServiceTitan | DNC | Hostile reply (2022 mabl era) | Feb 27, 2026 |
| Lance Silverman | Batch 5B | DNC | Polite decline. Re-engage 60+ days with new trigger | Mar 1, 2026 |
| Clyde Faulkner | CAMP Systems | DNC | mabl-era customer (2022). Skip permanently | Mar 3, 2026 |
| Ashok Prasad | ZL Technologies | DNC | mabl-era contact, 2 messages sent, no reply. Skip permanently | Mar 3, 2026 |
| Abe Blanco | Kapitus | DNC | Replied "not interested" Mar 4 | Mar 4, 2026 |
| Chuck Smith | Aventiv Technologies | DNC | Double-send (B1 + B5B). Rob decision | Mar 4, 2026 |
| Jitesh Biswal | JPMorgan Chase | DNC | Declined InMail Nov 4 | Mar 6, 2026 |

---

## Maintenance Notes

- This file is APPEND-ONLY for timeline events
- Stage fields may be updated as contacts progress
- Run `skills/lifecycle-tracker/SKILL.md` to sync from batch trackers + Gmail
- DNC entries here mirror CLAUDE.md — if they diverge, CLAUDE.md is authoritative
- For contacts not listed individually, check their batch tracker HTML file
