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

## Batch 9 Bounce Records — Mar 14, 2026

NDRs received Sat Mar 14 from Batch 9 sends (T1 sent Mar 14). All flagged as BOUNCED in Apollo. Stage-monitor logged these Mar 16.

| Contact | Company | Email | Bounce Type | Date |
|---------|---------|-------|-------------|------|
| Rick Bartlett | DraftKings | rick.bartlett@draftkings.com | Address not found (domain-level reject) | Mar 14 |
| Will Hester | DraftKings | will.hester@draftkings.com | Address not found (domain-level reject) | Mar 14 |
| Ankur Arora | DraftKings | ankur.arora@draftkings.com | Address not found (domain-level reject) | Mar 14 |
| Miroslav Kazakov | DraftKings | miroslav.kazakov@draftkings.com | Address not found (domain-level reject) | Mar 14 |
| Felipe Lora | Celonis | felipe.lora@celonis.de | 550 5.1.1 hard bounce | Mar 14 |
| Michael Guntsch | Celonis | michael.guntsch@celonis.de | 550 5.1.1 hard bounce | Mar 14 |
| Jeff Fox | Bungie | jeff.fox@bungie.net | Address not found (.net domain) | Mar 14 |
| Ryan Wagoner | Bungie | ryan.wagoner@bungie.net | Address not found (.net domain) | Mar 14 |
| Keren Sher | Anaplan | keren.sher@anaplan.com | Permanent fatal error | Mar 14 |
| Michael Hart | hims&hers | michael.hart@hims.com | Permanent fatal error | Mar 14 |
| Erik Mabry | Bethesda Softworks | erik.mabry@bethesda.net | Address not found (.net domain) | Mar 14 |
| James Ackermann | Bethesda Softworks | james.ackermann@bethesda.net | Address not found (.net domain) | Mar 14 |
| Vaibhav Shah | Farmers Insurance | vaibhav.shah@farmers.com | 550 5.1.x reject | Mar 14 |
| Siva Ranjani | Farmers Insurance | siva.ranjani@farmers.com | 550 5.1.x reject | Mar 14 |
| Deepa Krishnamoorthy | Farmers Insurance | deepa.krishnamoorthy@farmers.com | 550 5.1.x reject | Mar 14 |

**Pattern notes:** DraftKings (4/4) and Farmers .com domain (3/3) suggest domain-level sending restrictions. Bethesda .net (2/2) same. Rob should manually remove these from Apollo sequence to stop further steps. Apollo enrichment for alternate emails recommended for any contacts Rob wants to re-pursue.

---

## Batch 10 Bounce Records — Mar 16, 2026

NDRs received Mon Mar 16 from Batch 10 sends (T1 sent Mar 16). Logged by reply-classifier Run #3.

| Contact | Company | Email Attempted | Bounce Type | Date |
|---------|---------|-----------------|-------------|------|
| Shikha Jayant | Dun & Bradstreet | jayants@dnb.com | Recipient unknown (Office 365 — jayants not found at dnb.com) | Mar 16 |
| Usman Khan | Citizens Bank | usman.khan@citizensbank.com | Undeliverable (postmaster@citizensbank.com — confidentiality policy bounce) | Mar 16 |

**Pattern notes:** D&B bounce = wrong format or inactive account. Rob should check Apollo for alternate email for Shikha Jayant (try shikha.jayant@dnb.com). Citizens Bank bounce — similar to Zahidh Zubair B9 bounce (Mar 12). Domain may restrict external mail or the email format is wrong. Rob should manually remove both from Apollo sequence.

**Email confirmations (Run #3):** Usman Khan email confirmed as usman.khan@citizensbank.com from batch tracker. Shikha Jayant confirmed as jayants@dnb.com (DNR header).

---

## Batch 11 Bounce Records — Mar 16, 2026

NDRs received Mon Mar 16 (evening) from Mar 16 batch sends. Logged by reply-classifier Run #7 (Mar 17). All 15 contacts bounced — address not found or SMTP 550 hard bounce.

| Contact | Company | Email Attempted | Bounce Type | Date |
|---------|---------|-----------------|-------------|------|
| Jordan Simmons | Kibo Commerce | jordan.simmons@kibocommerce.com | Address not found (domain-level) | Mar 16 |
| Aslam Ather | Kibo Commerce | aslam.ather@kibocommerce.com | Address not found (domain-level) | Mar 16 |
| Dipty Pahal | Kibo Commerce | dipty.pahal@kibocommerce.com | Address not found (domain-level) | Mar 16 |
| Nelly Turton | Kibo Commerce | nelly.turton@kibocommerce.com | Address not found (domain-level) | Mar 16 |
| Bonnie Kaplan | Acadia Healthcare | bonnie.kaplan@acadiahealthcare.com | Address not found | Mar 16 |
| Maja Kilian | Acadia Healthcare | maja.kilian@acadiahealthcare.com | Address not found | Mar 16 |
| Sridhar Bulusu | Replicon | sridhar.bulusu@replicon.com | SMTP 550 hard bounce | Mar 16 |
| Sheethal Kotekar | Replicon | sheethal.kotekar@replicon.com | SMTP 550 hard bounce | Mar 16 |
| Siva Kumar | Replicon | siva.kumar@replicon.com | SMTP 550 hard bounce | Mar 16 |
| Michael Burton | WorkWave | michael.burton@workwave.com | Address not found | Mar 16 |
| Bhanu Sundar | Veradigm | bhanu.sundar@veradigm.com | Address not found | Mar 16 |
| Devendra Choudhary | Open Lending | devendra.choudhary@openlending.com | Address not found | Mar 16 |
| Niveditha Bhuj | LendBuzz | niveditha.bhuj@lendbuzz.com | 550 5.1.1 hard bounce | Mar 16 |
| Sylvia Kuzmak | ManTech | sylvia.kuzmak@mantech-inc.com | Address not found | Mar 16 |
| Emma Newberg | ManTech | emma.newberg@mantech-inc.com | Address not found | Mar 16 |

**Pattern notes:** Kibo Commerce (4/4 bounced) — domain-level block, do not re-enroll without verified alternate emails. Replicon (3/3 SMTP 550) — domain blocks or all emails are invalid format; avoid further enrollments until verified. Acadia Healthcare (2/2) and ManTech (2/2) — likely wrong email format. Rob should manually remove all 15 from Apollo sequence to stop further touches.

---

## Batch 12 Bounce Records — Mar 17, 2026

NDRs received Tue Mar 17 from today's Batch 12 sends (TASK-046 batch: 27 contacts). Logged by reply-classifier Run #11 (Mar 17, 5:00 PM EDT). 19 of 27 contacts confirmed bounced. Zebra (5) and Northern Trust (2) showed no NDRs — may have delivered.

| Contact | Company | Email Attempted | Bounce Type | Date |
|---------|---------|-----------------|-------------|------|
| Padma Srinivasan | Fidelity | padma.srinivasan@fidelity.com | Address not found | Mar 17 |
| Suvajit Chaudhury | Fidelity | suvajit.chaudhury@fidelity.com | Address not found | Mar 17 |
| Richelle Lara | Fidelity | richelle.lara@fidelity.com | Address not found | Mar 17 |
| Chris Petit | Fidelity | chris.petit@fidelity.com | Address not found | Mar 17 |
| Anusha Marlapalli | Epicor | anusha.marlapalli@epicor.com | Address not found | Mar 17 |
| Greg Sysak | Epicor | greg.sysak@epicor.com | Address not found | Mar 17 |
| Kevin McLeod | Infor | kevin.mcleod@infor.com | 550 5.4.1 Recipient address rejected: Access denied | Mar 17 |
| Frank Waters | Infor | frank.waters@infor.com | 550 5.4.1 Recipient address rejected: Access denied | Mar 17 |
| Greg Smith | Infor | greg.smith@infor.com | 550 5.4.1 Recipient address rejected: Access denied | Mar 17 |
| Srijyotsna Bokariya | Infor | srijyotsna.bokariya@infor.com | 550 5.4.1 Recipient address rejected: Access denied | Mar 17 |
| Mirza Hassan | Infor | mirza.hassan@infor.com | 550 5.4.1 Recipient address rejected: Access denied | Mar 17 |
| Sunkara Srinivas | Commvault | sunkara.srinivas@commvault.com | Undeliverable (postmaster@commvault.com) | Mar 17 |
| Prasad Alimineni | Commvault | prasad.alimineni@commvault.com | Undeliverable (postmaster@commvault.com) | Mar 17 |
| Brian Brennan | RSM US | brian.brennan@rsmus.com | Address not found | Mar 17 |
| Philcy Morales | RSM US | philcy.morales@rsmus.com | Address not found | Mar 17 |
| Kristina Pozzi | RSM US | kristina.pozzi@rsmus.com | Address not found | Mar 17 |
| Rupasri Soman | RSM US | rupasri.soman@rsmus.com | Address not found | Mar 17 |
| Christina Jimenez | RSM US | christina.jimenez@rsmus.com | Address not found | Mar 17 |
| Scott Pfeiffer | NETSCOUT | scott.pfeiffer@netscout.com | 550 hard bounce | Mar 17 |

**Pattern notes:** Infor.com (5/5 bounced) — domain firewall "Recipient address rejected: Access denied" (5.4.1). Hard block, do not re-enroll without verified alternate path. RSM US / rsmus.com (5/5) — all "Address not found", likely wrong email format (may use different format like first initial + last name). Fidelity (4 more today, on top of prior run Fidelity bounces) — fidelity.com may block external outreach or email format is incorrect. Commvault (2/2) — postmaster@commvault.com NDR, address not found. Rob should manually remove all 19 contacts from Apollo sequence.

---

## Additional Mar 17 Bounce Records — Non-Batch-12

NDRs from other active sequences (not Batch 12). Logged by reply-classifier Run #11.

| Contact | Company | Email Attempted | Bounce Type | Date |
|---------|---------|-----------------|-------------|------|
| Ashwini Dumbe | Kibo Commerce | ashwini.dumbe@kibocommerce.com | Address not found (domain-level block) | Mar 17 |
| Abhay N | Replicon | abhay.n@replicon.com | SMTP 550 hard bounce | Mar 17 |
| Harita Chandra | Replicon | harita.chandra@replicon.com | SMTP 550 hard bounce | Mar 17 |
| James Nelson | Personalis | james.nelson@personalis.com | 550 5.1.1 hard bounce | Mar 17 |
| Stefan Berner | Personalis | stefan.berner@personalis.com | 550 5.1.1 hard bounce | Mar 17 |
| Shiva Porah | GeoPagos | shiva.porah@geopagos.com | 550 5.1.1 hard bounce | Mar 17 |
| Lori Khan | GeoPagos | lori.khan@geopagos.com | 550 5.1.1 hard bounce | Mar 17 |
| (catchall) | AppSumo | catchall@appsumo.com | Message blocked (enterprise admin) | Mar 17 |
| Shilpa Nayak | FormAssembly | shilpa.nayak@formassembly.com | 550 5.1.1 hard bounce | Mar 17 |
| Massimo Modena | FormAssembly | massimo.modena@formassembly.com | 550 5.1.1 hard bounce | Mar 17 |
| Julieta Abacha | FormAssembly | julieta.abacha@formassembly.com | 550 5.1.1 hard bounce | Mar 17 |
| Brian Oppenheim | Celonis | brian.oppenheim@celonis.de | 550 5.1.1 hard bounce | Mar 17 |
| Bogdan Minciu | Celonis | bogdan.minciu@celonis.de | 550 5.1.1 hard bounce | Mar 17 |
| Tomer Weinberger | Check Point | tomerw@checkpoint.com | Undeliverable (postmaster@checkpoint.com) | Mar 17 |

**Pattern notes:** Kibo Commerce now 5 total bounces (domain block confirmed). Replicon now 5 total bounces (SMTP 550 domain filter confirmed). Celonis now 4 total bounces (brian.oppenheim + bogdan.minciu today, plus Felipe Lora + Michael Guntsch from Batch 9 — celonis.de domain appears unreachable). FormAssembly (3/3) — all 550 5.1.1. AppSumo catchall was blocked — avoid catch-all addresses for AppSumo. Personalis (2/2). GeoPagos (2/2). Check Point (1). Rob should manually remove all 14 contacts from Apollo sequence.

---

## Mar 18 Check Point Bounce Records

NDRs received Wed Mar 18 from postmaster@checkpoint.com. Logged by reply-classifier Run #14 (Mar 18, 3:09 PM EDT). These are the 2nd and 3rd Check Point bounces total (Tomer Weinberger was 1st, logged Mar 17 TASK-049). **checkpoint.com is now a confirmed pattern domain — avoid further enrollments without verified email format.**

| Contact | Company | Email Attempted | Bounce Type | Date |
|---------|---------|-----------------|-------------|------|
| Shlomo Yeret | Check Point | shlomoy@checkpoint.com | Undeliverable — address not found (postmaster@checkpoint.com) | Mar 18 |
| Yogesh Garg | Check Point | yogeshg@checkpoint.com | Undeliverable — address not found (postmaster@checkpoint.com) | Mar 18 |

**Pattern notes:** Check Point now 3 total bounces (Tomer Weinberger tomerw@checkpoint.com + Shlomo Yeret shlomoy@checkpoint.com + Yogesh Garg yogeshg@checkpoint.com). All via postmaster@checkpoint.com NDR. Both new bounces arrived within 4 minutes of each other (~2:32 PM Israel time) suggesting same batch send triggered them. Email format used (firstname.lastname or initials) appears to not match checkpoint.com's actual format, or domain rejects external mail. See TASK-056 to remove from Apollo.

---

## Mar 18 Evening Bounce Record

NDR received Wed Mar 18, 8:57 PM UTC (1:57 PM PDT). Logged by reply-classifier Run #17. This is the 3rd Epicor contact to bounce — email format appears invalid or address not found. Contact was part of B13/B14/B15 sends in TASK-060.

| Contact | Company | Email Attempted | Bounce Type | Date |
|---------|---------|-----------------|-------------|------|
| Alan Spindel | Epicor | alan.spindel@epicor.com | Address not found (mailer-daemon@googlemail.com) | Mar 18, ~9 PM UTC |

**Pattern notes:** Epicor now 3 total bounces (anusha.marlapalli + greg.sysak from TASK-048, + alan.spindel now). All via "Address not found." Epicor email format may be wrong or some contacts are no longer at the company. Verify format with remaining Epicor contacts before any further sends. See TASK-061 to remove from Apollo.

---

## Mar 18–19 Bounce Records (Late Evening / Overnight)

NDRs received Wed Mar 18 evening through Thu Mar 19 morning. Logged by reply-classifier Run #18 (Mar 19). These are from B13/B14/B15 TASK-060 sends.

| Contact | Company | Email Attempted | Bounce Type | Date |
|---------|---------|-----------------|-------------|------|
| Rakesh Rallapalli | Commvault | rrallapalli@commvault.com | Undeliverable — address not found (postmaster@commvault.com) | Mar 18, 7:04 PM EDT |
| Craig Telling | Equiniti | (email from B14) | Undeliverable (postmaster@group.internal) | Mar 18, 6:23 PM UTC |
| Mahesh Tolapu | Equiniti | (email from B14) | Undeliverable (postmaster@group.internal) | Mar 18, 6:40 PM UTC |
| Sheena Ramachandran | Square | sheenar@squareup.com | Address not found (mailer-daemon@googlemail.com) | Mar 18, 2:28 PM PDT |

**Pattern notes:** Commvault now 3 total bounces (Sunkara Srinivas from B12 TASK-048 + Rakesh Rallapalli now, plus possible earlier). Equiniti 2/2 bounced via postmaster@group.internal — new domain, possible domain-level block. squareup.com — first bounce from this domain. All 4 contacts should be removed from Apollo sequences. See TASK-063.

---

## Prospect Reply — Peter Rimshnick @ Yext (P3 Negative)

**Date:** Wed Mar 18, 2026, 6:20 PM EDT
**From:** Peter Rimshnick <primshnick@yext.com>
**Company:** Yext
**Reply content:** "Unsubscribe"
**Touch:** T2 (sent same day, Mar 18, 5:40 PM UTC)
**T1 sent:** Mar 13 (Batch 8)
**Classification:** P3 Negative — explicit unsubscribe request
**Stage update:** T2_REPLIED → recommend DNC
**Action:** Recommend DNC addition to Rob. Remove from Apollo sequence immediately. First prospect reply in 22 runs.

---

## Missed Calls — Unidentified Callers

| Date | Number | Apollo Notification Time | Status |
|------|--------|--------------------------|--------|
| Mar 14, 1:26 PM | +13234808909 | Sat Mar 14 | Unidentified — flagged Run #1 |
| Mar 15, 11:51 AM | +16175199076 | Sun Mar 15 | Unidentified — flagged Run #1 |
| Mar 16, 10:32 AM | +13152756209 | Mon Mar 16, 10:33 AM | NEW — Run #3 |
| Mar 16, 3:39 PM | +13218377968 | Mon Mar 16, 7:40 PM | NEW — Run #7 (first noted Run #6) |
| Mar 17, 2:16 PM | +19319221680 | Tue Mar 17, 2:17 PM | NEW — Run #11. Area code 931 = Tennessee/Clarksville area |
| Mar 17, 4:42 PM | +19319221680 | Tue Mar 17, 4:42 PM | 2nd call same number — Run #12. Two calls in ~2.5 hrs = elevated signal. See TASK-047. |
| Mar 18, 11:02 AM | +17632288324 | Wed Mar 18, 11:02 AM | NEW — Run #14. Area code 763 = NW Twin Cities suburbs (Plymouth/Maple Grove/Brooklyn Park, MN). See TASK-055. |
| Mar 18, 4:55 PM | +16263319807 | Wed Mar 18, 4:55 PM | NEW — Run #17. Area code 626 = San Gabriel Valley / Pasadena / Arcadia, CA. Unidentified. See TASK-062. |

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
