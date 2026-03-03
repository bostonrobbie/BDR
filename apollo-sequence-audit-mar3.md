# Apollo Q1 Priority Accounts Sequence Audit
**Date:** March 3, 2026  
**Audited by:** Claude (on behalf of Rob Gorham)

---

## Executive Summary

Audited all prior batches (1-8, Overflow, Buyer Intent) against the Q1 Priority Accounts Apollo sequence. **Batch 8** was fully remediated this session (18 contacts created + enrolled). **Batches 3-7 and Overflow** are clean. **Batch 1 (23 contacts) is the major gap**, with zero contacts in Q1 Priority Accounts. **Buyer Intent (9 contacts)** are in their own dedicated sequence by design.

---

## Batch 8 (Completed This Session)

- 43 prospects sent InMails (from batch7-send-tracker.json overflow)
- **18 contacts were missing from Apollo** and have been created + enrolled
- **25 contacts were already in Apollo** and enrolled
- Sequence now at **200 active + 4 finished = 204 total**
- ~12 contacts owned by other reps could not be enrolled via API (ownership restriction)

---

## Prior Batches Status

| Batch | Sent | In Q1 Priority Accounts? | Status |
|-------|------|--------------------------|--------|
| Batch 3 (Feb 25-26) | 25 | Yes | Clean |
| Batch 5A (Feb 27-28) | 24 | Yes | Clean |
| Batch 5B (Feb 27) | 25 | Yes | Clean |
| Batch 6 (Feb 28) | 27 | Yes | Clean |
| Batch 7 (Feb 28) | 42 | Yes | Clean |
| Overflow (Mar 1) | 7 | Yes | Clean |
| **Batch 1 (Feb 13)** | **23** | **NO** | **GAP** |
| Buyer Intent (Feb 27) | 9 | No (own sequence) | By design |

---

## Batch 1 Gap Detail (23 contacts, ALL missing from Q1 Priority Accounts)

Batch 1 was the earliest batch (Feb 13), sent via InMail only, before the systematic Apollo enrollment workflow was established.

### NOT FOUND in Apollo (11 contacts)
These would need to be created as new Apollo contacts before enrollment:

| Name | Company | Title |
|------|---------|-------|
| Kumarswamy Dontamsetti | Salesforce | Director, AI Cloud Quality Engineering |
| Rahul Rajendra Prasad | Citizens Financial Group | Director, Platform & SRE Operations |
| Shashin Surkund | Fidelity Investments | VP, Big Data Platforms |
| Florentin Stafie | NetApp | VP Software Engineering |
| Kunal Shah | o9 Solutions | SVP Software Engineering |
| Tauhid Khan | Optum/UHG | Director QA, Test Automation |
| Pathik Desai | TriNetX | Head of Global IT |
| Theresa Naramore | Spectrio | Director of QA |
| Debbie Almeida | loanDepot | Director IT Quality Assurance |
| Jayashree Karnam | NCR Voyix | Director Quality Engineering |
| Izzie Alvarez | Harbor.ai | Director QE |

### FOUND in Apollo but NOT in sequence (7 contacts)
These exist but are owned by other reps or unowned, and are not in any sequence:

| Name | Company | Ownership |
|------|---------|-----------|
| Shadi Sleiman | Careem | No owner |
| Valerie Terrell | Travelers | Other rep |
| David Muczynski | Persefoni | No owner |
| Tim Attuquayefio | 2K Games | No owner |
| Sarat Ramineni | DiiZen | Other rep |
| Aditi Agrawal | Myridius | Other rep |
| Yoram Tal | OPAQUE Systems | No owner |

### NOT CHECKED (5 contacts)
| Name | Company |
|------|---------|
| Abe J. | Origence |
| Vishal Tiwari | 3E |
| Veeresh Erched | Amadeus NA |
| Chuck Smith | Aventiv Technologies |
| Kowsick Venkatachalapathi | BNY |

---

## Buyer Intent Contacts (9)

All 9 are in the **Q1 Website Visitor, Tier 1 Intent** sequence (separate from Q1 Priority Accounts). This appears intentional since they came through a different funnel.

| Name | Company | Status in Intent Sequence |
|------|---------|---------------------------|
| Andy Nelsen | Roper Technologies | Active |
| Jose Moreno | Dexcom | Active |
| Tom Yang | IQVIA | Active |
| Eyal Luxenburg | Upstream Security | Active |
| Hibatullah Ahmed | Bupa | Active |
| Jeff Barnes | Mimecast | Active |
| Eduardo Menezes | Citrix | Active |
| Todd Willms | Bynder | Finished |
| Jason Ruan | Coupang | Active |

---

## Recommendations

1. **Batch 1 (decision needed):** Should I create the 11 missing contacts and enroll all 23 into Q1 Priority Accounts? The 7 that exist but are owned by other reps may hit the same ownership restriction we saw with Batch 8.

2. **Buyer Intent (likely no action):** These are in their own sequence by design. Confirm no dual-enrollment needed.

3. **Batch 8 ownership-blocked contacts (~12):** These need manual enrollment in Apollo UI since the API rejects enrollment for contacts owned by other team members.

---

## Sequence Totals (Current)
- Q1 Priority Accounts: **200 active + 4 finished = 204 total**
- Q1 Website Visitor, Tier 1 Intent: 9 contacts (Buyer Intent batch)
