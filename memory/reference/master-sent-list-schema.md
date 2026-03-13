# MASTER_SENT_LIST.csv — Schema Reference

**File location:** `/Work/MASTER_SENT_LIST.csv`
**Current row count:** 496 (as of 2026-03-12 Session 31)
**Purpose:** Single source of truth for every contact ever sent outreach. Used for dedup, compliance gate, and TAM coverage audits.

---

## Column Schema

| Column | Type | Example | Required | Notes |
|--------|------|---------|----------|-------|
| `name` | string | `Jason Lieberman` | Yes | Full name. Normalized to "First Last" — no middle initials, no suffixes. Used for grep dedup. |
| `batch` | string | `TAM Outbound Batch 7 Mar12` | Yes | **Must follow standard format** (see Batch Name Format below). Used for wave/batch lookup. |
| `send_date` | date | `2026-03-12` | Yes | ISO 8601 (YYYY-MM-DD). Date T1 email was sent. |
| `channel` | string | `EMAIL` | Yes | `EMAIL` (Apollo email) or `INMAIL` (LinkedIn InMail). |
| `credits` | integer | `1` | Yes | Credits consumed. `1` for email, `1` for InMail. `0` if bounced before send. |
| `file` | string | `tamob-batch-20260312-7.html` | Yes | Batch tracker HTML file containing this contact's draft and research. |
| `norm` | string | `jason lieberman` | Yes | Lowercase normalized name for case-insensitive grep. Auto-generated: `echo "Jason Lieberman" | tr '[:upper:]' '[:lower:]'` |

---

## Batch Name Format (MANDATORY)

Standard format: `TAM Outbound Batch {N} {MonDD}`

Examples:
- `TAM Outbound Batch 7 Mar12` ✅
- `TAM Outbound Batch 7 T2 Mar17` ✅ (for T2 sends)
- `B7` ❌ non-standard
- `W6B1` ❌ non-standard
- `Wave5B` ❌ non-standard

**Legacy names (pre-Mar 10, 2026):** Some rows use old formats (`Feb27 Batch 5A`, `linkedin-batch-1`, etc.). These are grandfathered — do not modify. All new rows must use standard format.

---

## Adding Rows

Append one row per contact sent. **Never modify existing rows.**

Template:
```
{Full Name},{TAM Outbound Batch N MonDD},{YYYY-MM-DD},EMAIL,1,{tracker-filename.html},{lowercase full name}
```

Example:
```
Jason Lieberman,TAM Outbound Batch 7 Mar12,2026-03-12,EMAIL,1,tamob-batch-20260312-7.html,jason lieberman
```

---

## Dedup Grep Commands

```bash
# By full name (case-insensitive)
grep -i "jason lieberman" /Work/MASTER_SENT_LIST.csv

# By company (use with caution — partial matches possible)
grep -i "epicor" /Work/MASTER_SENT_LIST.csv

# Count rows (verify after every session)
wc -l /Work/MASTER_SENT_LIST.csv

# Check for duplicate names
sort /Work/MASTER_SENT_LIST.csv | cut -d',' -f1 | uniq -d
```

---

## Row Count Verification

After every enrollment session, run `wc -l MASTER_SENT_LIST.csv` and report:
`MASTER_SENT_LIST.csv verified: N rows (was M + X new contacts)`

If count doesn't match expected, STOP and investigate before proceeding.

---

## Known Data Issues

| Issue | Rows Affected | Status |
|-------|--------------|--------|
| Hard bounces: 12 contacts marked in batch column as "HARD BOUNCE" | ~12 rows | Documented, do not re-contact |
| Non-standard batch names in pre-Mar 10 rows | ~50 rows | Grandfathered — do not modify |
| Missing `company_domain` column | All rows | Known gap — TAM compliance requires manual cross-check against tam-accounts-mar26.csv |

---

*Created: 2026-03-13 (Session 32 optimization pass)*
*When the schema changes: update this file, increment version, note date.*
