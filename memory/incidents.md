# Incidents & Draft Safety Rules

## INC-001: Premature Touch 3 Emails (2026-02-28)
**Severity:** HIGH

### What Happened
6 Touch 3 emails sent Feb 28 at 6:30-6:33 AM ET, 7-8 days early, skipping Touch 2 entirely.

### Affected Prospects
| Name | Company | Batch | Touch 1 Sent | Days Early |
|------|---------|-------|-------------|------------|
| Irfan Syed | Progress Software | Batch 3 | Feb 25 | 7 |
| Katie Barlow Hotard | Lucid Software | Batch 3 | Feb 25 | 7 |
| Rachana Jagetia | Housecall Pro | Batch 3 | Feb 26 | 8 |
| Giang Hoang | Employee Navigator | Batch 3 | Feb 26 | 8 |
| Pallavi Sheshadri | Origami Risk | ORPHAN | Unknown | N/A |
| Gunasekaran Chandrasekaran | FloQast | ORPHAN | Unknown | N/A |

### Root Cause (3 stacked failures)
1. Gmail drafts created WITHOUT date-gating logic
2. Drafts used old pre-C2 templates with HC1 violations
3. Two prospects not in any batch tracker (orphans)

### Remediation
- 4 Batch 3: Treat premature email as extra touch. Skip official Touch 3. Continue Touch 2 on schedule.
- 2 orphans: Add retroactively. Research + proper follow-ups.

---

---

## INC-002: Five Double-Sends Across Batches (Discovered 2026-03-04)
**Severity:** HIGH

### What Happened
Five prospects were sent LinkedIn InMails twice — once in an early batch and once in Batch 8 (Mar 3). All five sends already occurred and cannot be unsent. Discovered during full Sales Nav inbox audit (220 conversations).

### Affected Prospects
| Name | First Send | Second Send | Gap |
|------|-----------|------------|-----|
| Chuck Smith | Batch 1, Feb 23 (connection msg) | Batch 5B, Feb 27 | 4 days |
| Abe Blanco | Batch 3, Feb 26 | Batch 8, Mar 3 | 5 days |
| Rick Kowaleski | Batch 3, Feb 26 | Batch 8, Mar 3 | 5 days |
| Christie Howard | Batch 5B, Feb 27 | Batch 8, Mar 3 | 4 days |
| Mohan Gummadi | Batch 5B, Feb 27 | Batch 8, Mar 3 | 4 days |

Note: Abe Blanco also replied "not interested" Mar 4. Added to DNC. Double-send is moot for him but logged for accuracy.

### Root Cause
No cross-batch dedup check performed before Batch 8 was built. Batch 8 pull from Apollo Q1 Priority Accounts sequence included prospects already messaged in Batches 1/3/5B without any name-level verification against prior send history.

### Remediation (applied 2026-03-04)
- All 5 double-sends logged in pipeline-state.md under "Double-sends (cannot unsend)"
- MASTER_SENT_LIST.csv created: single deduplicated CSV of all sends across all batches
- Pre-batch dedup check added to sop-send.md as mandatory Step A/B before any batch is built
- For Touch 2: treat double-send people as normal Touch 2 candidates. Note the extra prior touch. Abe Blanco = DNC, skip entirely.
- For Chuck Smith: first send was a connection request (not InMail, no Sales Nav thread). Touch 2 still due on normal timeline.

---

## INC-003: Batch 9 Untracked Sends (2026-03-03)
**Severity:** MEDIUM

### What Happened
6 Batch 9 InMails sent on Mar 3 in a session that ended without logging. Discovered via Sales Nav audit the following day. 5-credit discrepancy between tracker (28) and actual (23) also traced to same-session logging gap.

### Affected Prospects
Mohan Guruswamy, Jeremy Cira, Chandana Ray, Lueanne Fitzhugh, Martha Horns, Kylie Summer.

### Root Cause
Send session ended mid-batch without updating pipeline-state.md. Credits not decremented. No same-session logging discipline.

### Remediation (applied 2026-03-04)
- All 6 logged retroactively in pipeline-state.md Batch 9 True State table
- Credits corrected to 23
- Same-session logging rule added to sop-send.md Step 9

---

## INC-004: Wrong Company in Subject Lines — Mar 7 WV Emails (Discovered 2026-03-09)
**Severity:** MEDIUM

### What Happened
Two WV (Website Visitor) emails sent Mar 7 contained the wrong company name in the subject line. Template variables were not properly substituted before send.

### Affected Prospects
| Name | Company | Subject Sent | Wrong Company Referenced |
|------|---------|-------------|--------------------------|
| Chris Bell | Crestron | "Regression test coverage during Xero's platform expansion, Chris" | Xero (not Crestron) |
| Davor Milosevic | IQVIA | "QE load coverage as Vimeo moves beyond B2B, Davor" | Vimeo (not IQVIA) |

### Root Cause
Subject line templates for WV batch were not checked for wrong-company variable substitution before send. Previous prospect's company name carried over into subject.

### Remediation
- Cannot unsend. Both contacts are live outreach and may not notice or respond.
- No corrective email sent — would draw more attention to the error.
- Monitor for replies. If either responds, handle naturally without referencing the error.
- Pre-send QA rule: subject line company name must match recipient's company before any email send.

---

## INC-005: Cross-Channel Double-Sends — LinkedIn InMail + WV Email (Discovered 2026-03-09)
**Severity:** LOW-MEDIUM

### What Happened
Four prospects received both a LinkedIn InMail (cold outreach) AND a WV email (Website Visitor sequence) — two separate first-touch cold contacts. Dedup check was not run across channels before WV email batch was built.

### Affected Prospects
| Name | Company | LinkedIn InMail | WV Email | Gap |
|------|---------|----------------|----------|-----|
| Jason Schwichtenberg | WebMD | Batch 8, Mar 3 | WV Email Mar 3 | Same day |
| Jamie Kurt | Vertafore | Batch 5B, Feb 27 | WV Email Mar 3 | 4 days |
| Kerri McGee | Sapiens | Batch 5A, Feb 27 | WV Email Mar 3 | 4 days |
| Lyle Landry | Availity | Batch 5B, Feb 27 | WV Email Mar 3 | 4 days |

### Root Cause
Pre-batch dedup check (sop-send.md Step 0) was applied within LinkedIn batches but not cross-referenced against the WV email build. WV email batch was built against Apollo Website Visitor list without checking MASTER_SENT_LIST for prior LinkedIn InMail sends.

### Remediation
- Cannot unsend. All four have received both touches.
- Treat as having consumed T1 and T2 in both channels. Do not send any further follow-ups — they've been contacted twice.
- Add all four to DNC for future batches.
- Pre-batch rule update: MASTER_SENT_LIST dedup must apply to ALL channels, not just same-channel, before any batch (LinkedIn or email) is built.

---

## INC-006: Feb 27 WV Email Batch — 11 Contacts Never Added to MASTER_SENT_LIST (Discovered 2026-03-09)
**Severity:** LOW

### What Happened
11 contacts emailed Feb 27-28 via WV (Website Visitor) email batch were never logged in MASTER_SENT_LIST. Discovered via Gmail sent audit Mar 9.

### Affected Contacts
Tom Yang (Versant Media), Jeff Barnes (Digi), Jose Moreno (Flywire), Eyal Luxenburg (Island), Todd Willms (Bynder), Jason Ruan (Binance), Namita Jain (OverDrive), Pallavi Sheshadri (Origami Risk), Gunasekaran Chandrasekaran (FloQast), Andy Nelson (Rightworks — T1 only, T2 Mar 6 was tracked), Eduardo Menezes (Fulgent Genetics — T1 only, T2 Mar 6 was tracked).

### Remediation
All 11 added to MASTER_SENT_LIST Mar 9 under "WV Email Batch Feb27" / "WV Email Batch Feb28" with "Gmail audit Mar9 (was missing)" notation.

---

## INC-007: Mass Placeholder Send — TAM Outbound Wave 1 + Wave 2 (2026-03-10)
**Severity:** HIGH

### What Happened
All TAM Outbound T1 emails sent via Apollo task queue (both Wave 1, ~22 contacts, and Wave 2 first 2 contacts) went out with Apollo's default placeholder body: "Placeholder - replace with personalized email before sending. Robert Gorham - BDR Robert.gorham@testsigma.com www.testsigma.com" — instead of the real personalized content. Confirmed via Gmail sent folder.

### Root Cause
The Quill API injection (`quill.setText(...)`) visually updated the compose panel and returned "done" — but Apollo's internal send payload was NOT updated. Apollo was reading from its own sequence template state, not the Quill editor DOM. The body looked correct in the preview but the wrong content was sent.

### Affected Contacts (confirmed via Gmail sent)
Wave 1 (Session 11): Sucheth, Richelle, Padma, Nithya, Des, Eric, Maurice, Sourabh, Seth, Prasad, Brahmaiah, Arun, Christopher, Chamath, Maggie, Neeraj, Jennifer (TruStage), Snezhana, Rick, Jennifer W., John, Hrishi — ~22 contacts
Wave 2 (this session): Shyamendra Singh (HashiCorp), Saeyed Shamlou (OneMain) — 2 confirmed

### Remediation — ✅ COMPLETE (2026-03-10, Sessions 12-13)

Recovery emails sent as personalized reply threads — honest "oops" opener + real intended message — via Gmail Chrome automation. All sends screenshot-verified before sending.

**Recovery send summary: 24/25 sent. 1 hard bounce.**

| # | Name | Company | Result |
|---|------|---------|--------|
| 0 | Rick Brandt | Cboe | ✅ Sent |
| 1 | Maurice Saunders | Cboe | ✅ Sent |
| 2 | Snezhana Ruseva | Cboe | ✅ Sent |
| 3 | Seth Drummond | Fidelity | ✅ Sent |
| 4 | Bipin Bhoite | Mindbody | ✅ Sent |
| 5 | Christopher Bilcz | Fidelity | ✅ Sent |
| 6 | Eric Pearson | Fidelity | ✅ Sent |
| 7 | Nithya Arunkumar | Fidelity | ✅ Sent |
| 8 | Richelle Lacamera | Fidelity | ✅ Sent |
| 9 | Sourabh Roy | Fidelity | ✅ Sent |
| 10 | Padma Srikanth | Fidelity | ✅ Sent |
| 11 | Neeraj Tati | JPMorgan Chase | ✅ Sent |
| 12 | Brahmaiah Vallabhaneni | Commvault | ✅ Sent |
| 13 | Jennifer Wang | Commvault | ✅ Sent |
| 14 | Prasad Alapati | Commvault | ✅ Sent |
| 15 | Sucheth Ramgiri | Commvault | ⚠️ HARD BOUNCE — sramgiri@commvault.com not found (SMTP 550 5.1.10). Recovery NOT sent. Remove from sequence + re-enrich. |
| 16 | Arun Amarendran | Commvault | ✅ Sent |
| 17 | Chamath Guneratne | TruStage | ✅ Sent |
| 18 | Maggie Redden | TruStage | ✅ Sent |
| 19 | Jennifer Drangstveit | TruStage | ✅ Sent |
| 20 | John Harding | YouTube | ✅ Sent |
| 21 | Des Keane | YouTube | ✅ Sent |
| 22 | Hrishikesh Aradhye | YouTube | ✅ Sent |
| 23 | Saeyed Shamlou | OneMain | ✅ Sent |
| 24 | Shyamendra Singh | HashiCorp | ✅ Sent |

**Action item:** Remove Sucheth Ramgiri from TAM Outbound sequence. Re-enrich email via Apollo or LinkedIn before any future outreach to Commvault.

**Ongoing rules (permanent):**
- DO NOT use Quill setText() for Apollo task sends
- Pre-send body verification: read back `.ql-editor` innerText + screenshot before every Send Now click
- If placeholder still present: STOP. Do not send.

### Rule Added to SOP
After every body injection and before every Send Now click:
1. Read back `document.querySelector('.ql-editor').innerText` — confirm real content, not placeholder
2. Screenshot the compose panel — visually verify subject AND body
3. If placeholder still present: STOP. Do not send.

---

---

## INC-008: Two Placeholder Sends — TAM Outbound Wave 3 (2026-03-11)
**Severity:** HIGH

### What Happened
Two Wave 3 T1 emails were sent with Apollo's default placeholder body ("Placeholder - replace with personalized email before sending...") instead of real personalized content. Confirmed via Gmail sent folder. Both show real subjects but empty/placeholder bodies.

### Affected Contacts
| # | Name | Company | Email | Correct Subject |
|---|------|---------|-------|-----------------|
| 1 | Michael Cahill | L3Harris | michael.cahill@l3harris.com | Michael's regression coverage at L3Harris |
| 2 | Manpreet Burmi | Veradigm | manpreet.burmi@allscripts.com | Manpreet's regression coverage at Veradigm |

### Root Cause (two failure modes)
1. **Silent clipboard paste failure:** After triple-clicking the subject field and typing a new subject, clicking the body area at the wrong coordinate fails to focus the Quill editor. `Ctrl+A → Ctrl+V` executes but targets the wrong element (browser UI, not Quill). The editor still shows "Placeholder" text. No error is visible.
2. **False-positive verification:** The "Changes saved" toast fires when the subject is saved — NOT when the body is saved. A screenshot of the compose panel can look plausible if the zoom is insufficient. The mandatory JS body readback (`document.querySelector('.ql-editor').innerText`) was NOT executed before Send Now, allowing the placeholder to be sent.

### Remediation
- Recovery emails sent via Gmail as reply threads (same approach as INC-007). Honest "oops" opener + real intended content.
- Both contacts remain in the TAM Outbound sequence. Recovery email counts as the real T1. T2 due Day 5 from recovery send.
- Recovery drafts: see `tamob-batch-20260311-1.html` notes for Michael Cahill (L03) and Manpreet Burmi (V06).

### Permanent Rule Changes (effective immediately)
**Rule A — Mandatory JS body verification before every Send Now click (TAM Outbound task queue):**
```javascript
// Run this BEFORE clicking Send Now. Paste result in session log.
document.querySelector('.ql-editor').innerText.trim().slice(0, 80)
```
Expected result starts with: `Hi [FirstName],` — NOT "Placeholder"
If result contains "Placeholder": STOP. Re-paste body. Verify again. Do not click Send Now.

**Rule B — Zoom screenshot of body area required:**
After pasting, take a `zoom` screenshot of the body area (approximately [860, 380] to [1215, 500]) to visually confirm real content before proceeding to Send Now.

**Rule C — "Changes saved" toast does NOT confirm body was set:**
The toast fires on subject save only. Do not treat it as body confirmation. Body verification (Rule A + Rule B) is always required separately.

**Rule D — Body paste focus recovery:**
After editing the subject field, click the body at coordinate (1035, 540) — center of the Quill editor — not (514, 407) or (528, 407). Then wait 0.5s before Ctrl+A. If paste fails, try clicking (1035, 480) and repeating.

---

## INC-009: Wave 4 Email Bounce + Invalid Email Flag (2026-03-11)
**Severity:** LOW

### What Happened
During TAM Outbound Wave 4 enrollment and task execution (Mar 11), two contacts surfaced with problematic email addresses:

1. **Ksenia Shchelkonogova (Mastercard)** — Apollo email `kshchelkonogova@mastercard.com` triggered a bounce/failure. Apollo showed contact in TAM Outbound sequence with `status: failed` / `inactive_reason: email_invalid`. Email was not successfully delivered.

2. **Divya Sathish (EA / Electronic Arts)** — Apollo contact record contained custom field `"678901dcd836ab01b09a6110": "invalid"` — the same "email_invalid" flag marker seen on Ksenia's record before her bounce. Apollo custom field `678901dcd836ab01b09a6110` = email quality flag = "invalid" when set.

### Root Cause
Apollo marks email addresses as invalid when bounce signals or verification checks flag them. The custom field `678901dcd836ab01b09a6110 = "invalid"` is Apollo's internal email quality indicator. Contacts with this flag are at high risk of bounce. This flag was not checked during Wave 4 enrichment/enrollment.

### Affected Contacts
| Name | Company | Email | Status | Action |
|------|---------|-------|--------|--------|
| Ksenia Shchelkonogova | Mastercard | kshchelkonogova@mastercard.com | ⛔ Bounced/Failed | Re-enrich. Try LinkedIn InMail when credits available. |
| Divya Sathish | EA | divya.sathish@ea.com | ⚠️ Invalid flag — T1 task pending | Check if task sends. If bounce, re-enrich via LinkedIn. |

### Remediation
- Ksenia: Remove from TAM Outbound sequence. Do not attempt email follow-up until re-enriched with a valid address. Use LinkedIn InMail when credits available.
- Divya: Monitor Wave 4 pending tasks. If Step 1 task sends and bounces, remove from sequence + re-enrich.
- Both contacts still in tamob-batch-20260311-2.html as "Ready" (pending T1 tasks).

### Permanent Rule Added
Before enrolling any contact in TAM Outbound (or any Apollo email sequence), check for Apollo custom field `678901dcd836ab01b09a6110 = "invalid"`. If present, skip email enrollment and use LinkedIn InMail instead. This field is an Apollo email quality flag and reliably predicts hard bounces.

---

## Draft Safety & Cadence Enforcement Rules

### Rule 1: Date-Gating
- Touch 2 drafts: NOT before Day 4
- Touch 3 drafts: NOT before Day 9
- Premature drafts saved as `[DRAFT-HOLD]` with date gate, NOT in Gmail.

### Rule 2: TOUCH_ELIGIBLE_DATE Fields
Every tracker must have: touch1_sent_date, touch2_eligible_date (+4d), touch2_send_date (+5d), touch3_eligible_date (+9d), touch3_send_date (+10d). **Check today's date before creating ANY draft.**

### Rule 3: No Orphan Prospects
Every prospect must exist in a tracker BEFORE any draft is created.

### Rule 4: Template Version Enforcement
All drafts must use C2 structure. MQS >= 9/12. No C1 or pre-C2 templates.

### Rule 5: Draft Naming Convention
- `[READY] [Name] @ [Company] - Touch [N] - Send on [date]`
- `[HOLD] [Name] @ [Company] - Touch [N] - NOT BEFORE [date]`
- `[SENT] [Name] @ [Company] - Touch [N] - Sent [date]`

### Rule 6: Daily Gmail Draft Audit
Every daily session: search drafts, cross-reference eligible dates, flag orphans/premature/old-template/unscored. Delete or hold-tag flagged drafts.

### Rule 7: Batch 7+ Tracker Requirements
Must include: touch1_sent_date, touch2/3_eligible_date, current_touch, cadence_status (ON_TRACK/AHEAD/BEHIND/COMPLETE).
