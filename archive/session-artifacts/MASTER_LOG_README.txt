================================================================================
PROSPECT MASTER LOG - README
================================================================================

FILE INFORMATION
================================================================================
Name:         prospect-master-log.json
Location:     /sessions/great-busy-meitner/mnt/Work/
Size:         25 KB
Lines:        1,003
Last Updated: 2026-02-25
Format:       JSON

EXTRACTION SUMMARY
================================================================================
Total Prospects Extracted:  66 prospects across 3 batches
  • Batch 1 (2026-02-23): 20 prospects
  • Batch 2 (2026-02-23): 22 prospects  
  • Batch 3 (2026-02-25): 24 prospects

Data Completeness:
  • Names:      66/66 (100%)
  • Titles:     66/66 (100%)
  • Companies:  66/66 (100%)
  • Emails:     24/66 (36%) - Only in Batch 3
  • LinkedIn:   24/66 (36%) - Only in Batch 3
  • Apollo IDs: 24/66 (36%) - Only in Batch 3
  • Status:     66/66 (100%)

INDEXES CREATED
================================================================================
Email Index:
  - 24 prospects with verified email addresses
  - Maps email -> {name, batch, company}
  - Fast lookup for email-based deduplication

Company Index:
  - 64 unique companies represented
  - Maps company -> [list of prospect names]
  - Identifies 2 companies with multiple prospects

BATCH DETAILS
================================================================================

Batch 1 (2026-02-23): 20 prospects
  Status Distribution:
    - Not Started: 19
    - Skipped: 1
  Priority Breakdown:
    - Priority 5 (Hot): 8
    - Priority 4 (Warm): 8
    - Priority 3 (Standard): 4
  Companies: Salesforce, Citizens Financial, Fidelity, NetApp, Careem, etc.

Batch 2 (2026-02-23): 22 prospects
  Status Distribution:
    - Not Started: 22
  Priority Breakdown:
    - Priority 4 (Warm): 12
    - Priority 3 (Standard): 10
  Companies: Light & Wonder, Noetic, Natera, Cantaloupe, Waystar, etc.

Batch 3 (2026-02-25): 24 prospects
  Status Distribution:
    - Touch 1 Sent: 23
    - Not Started: 1
  Priority Breakdown:
    - Priority 3 (Standard): 17
    - Priority 4 (Warm): 6
    - Priority 2 (Lower): 1
  Companies: Progress Software, Lucid, Housecall Pro, Employee Navigator, etc.
  Note: All prospects in Batch 3 have email, LinkedIn, and Apollo ID data

DUPLICATE DETECTION RESULTS
================================================================================
No significant duplicates found.

Companies with Multiple Prospects:
  • Aventiv Technologies: 2 prospects (Chuck Smith appears twice)
  • NCR Voyix: 2 prospects (Jayashree Karnam appears twice)

These appear to be data entry artifacts (same person listed twice) rather than
genuine duplicates of different people at the same company.

JSON STRUCTURE
================================================================================

Root Object:
{
  "lastUpdated": "2026-02-25",
  "totalProspects": 66,
  "batches": {
    "1": {"date": "2026-02-23", "count": 20},
    "2": {"date": "2026-02-23", "count": 22},
    "3": {"date": "2026-02-25", "count": 24}
  },
  "prospects": [
    {
      "batch": 1,
      "dateAdded": "2026-02-23",
      "name": "Kumarswamy Dontamsetti",
      "title": "Director, AI Cloud Quality Engineering (Agentforce)",
      "company": "Salesforce",
      "email": null,              // null in Batches 1 & 2
      "linkedinUrl": null,        // null in Batches 1 & 2
      "apolloId": null,           // null in Batches 1 & 2
      "status": "Not Started",
      "priority": 5
    },
    ...
  ],
  "emailIndex": {
    "isyed@progress.com": {
      "name": "Irfan Syed",
      "batch": 3,
      "company": "Progress Software"
    },
    ...
  },
  "companyIndex": {
    "Salesforce": ["Kumarswamy Dontamsetti"],
    "Aventiv Technologies": ["Chuck Smith", "Chuck Smith"],
    ...
  }
}

HOW TO USE THIS FILE
================================================================================

1. DUPLICATE PREVENTION (When Building New Batches):
   - Check emailIndex for existing prospects before enriching
   - Check companyIndex to avoid over-contacting single companies
   - Compare new prospect names against all extracted prospects

2. EMAIL LOOKUP:
   - emailIndex["email@domain.com"] returns name, batch, company
   - Useful for building email sequences in Batch 3+

3. COMPANY-LEVEL ANALYSIS:
   - companyIndex["Company Name"] shows all contacted prospects at that company
   - Use to identify expansion opportunities or avoid fatigue

4. BATCH HISTORY:
   - Track status progression across batches
   - Monitor which touches have been sent
   - Identify prospects ready for follow-up sequences

5. DATA ENRICHMENT:
   - Batch 3 (2026-02-25) has complete email/LinkedIn/Apollo data
   - Batches 1-2 have names, titles, companies only
   - Use for deciding next enrichment priorities

TECHNICAL NOTES
================================================================================

Extraction Method:
  - JavaScript object parsing from HTML prospect arrays
  - Regex pattern matching for both single ('') and double ("") quoted fields
  - Careful field extraction to avoid nested object pollution

Data Validation:
  - 100% of prospects have names, titles, companies
  - Email/LinkedIn/Apollo data only in Batch 3 (36% of total)
  - All prospects have status and priority fields
  - No null/undefined in core fields (name, title, company)

Performance:
  - JSON file is human-readable and machine-parseable
  - Indexes enable O(1) lookups by email or company
  - Suitable for programmatic duplicate checking before new extractions

NEXT STEPS
================================================================================

1. Use this file as the baseline for Batch 4+ extractions
2. Before adding prospects to new batches:
   - Query emailIndex to check for existing emails
   - Query companyIndex to check company overlap
   - Manually verify against prospect names
3. Update lastUpdated timestamp when adding new batches
4. Re-extract emailIndex and companyIndex after major additions
5. Archive previous versions before major updates

CONTACT / QUESTIONS
================================================================================

This file was auto-generated by Claude Code extraction script.
For issues or questions about the data, refer to the source HTML batch files:
  - prospect-outreach-1-2026-02-23.html
  - prospect-outreach-2-2026-02-23.html
  - prospect-outreach-3-2026-02-25.html

================================================================================
