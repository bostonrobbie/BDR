# Batch JSON Builder — Skill

## Description
After Rob approves a batch (Gate 1 — APPROVE SEND), this skill reads the approved batch tracker HTML file and extracts all contacts + their approved subjects + bodies into a `batch{N}_sends.json` file. The output is the content source for `skills/apollo-send/SKILL.md`. Eliminates the manual JSON-construction step that previously happened ad hoc.

## Trigger
Run immediately after Rob says **APPROVE SEND** for a batch, before starting any Apollo send session.

Inputs needed:
- The batch tracker HTML file path (e.g., `mnt/Work/tamob-batch-20260313-2.html`)
- The batch number (e.g., `9`)
- Confirmation that all "Draft Ready" cards in the tracker have finalized subjects + bodies

## Prerequisites
- Batch tracker HTML file exists with all contacts and approved content
- All contacts have status "Draft Ready" (not "Draft WIP" or blank)
- Rob has reviewed and approved all content (Gate 1 — APPROVE SEND granted)

---

## Process

### Step 1: Read the Tracker HTML

```python
from pathlib import Path
import re, json

tracker_path = "mnt/Work/{tracker_filename}.html"
content = Path(tracker_path).read_text(encoding='utf-8')
print(f"Tracker loaded: {len(content)} chars")
```

### Step 2: Parse Contact Cards

The tracker HTML uses a consistent card structure. Each contact card contains:
- An `id` attribute or data attribute (numeric ID)
- The contact's first and last name
- Their email address
- Approved subject line (in a `subject-line` or similar labeled span/div)
- Approved email body (in a `email-body` or pre-formatted div)

Parse using regex or BeautifulSoup depending on the tracker format:

```python
# Example regex pattern — adjust to match actual tracker HTML structure
# Look for cards with class "contact-card" or "prospect-card"
# Each card has data-id, name, email, subject, body

# Pattern for extracting card sections:
cards = re.findall(r'<div[^>]+class="[^"]*contact-card[^"]*"[^>]*>(.*?)</div>\s*</div>', content, re.DOTALL)

contacts = []
for i, card in enumerate(cards, 1):
    # Extract fields — adjust selectors to match your tracker's actual HTML
    name_match = re.search(r'class="[^"]*contact-name[^"]*"[^>]*>([^<]+)<', card)
    email_match = re.search(r'class="[^"]*contact-email[^"]*"[^>]*>([^<]+)<', card)
    subject_match = re.search(r'class="[^"]*subject-line[^"]*"[^>]*>([^<]+)<', card)
    body_match = re.search(r'class="[^"]*email-body[^"]*"[^>]*>(.*?)</div>', card, re.DOTALL)

    if not all([name_match, email_match, subject_match, body_match]):
        print(f"  ⚠️  Card {i}: missing fields — manual review needed")
        continue

    full_name = name_match.group(1).strip()
    first_name = full_name.split()[0]

    contacts.append({
        "id": i,
        "name": full_name,
        "first": first_name,
        "email": email_match.group(1).strip(),
        "subject": subject_match.group(1).strip(),
        "body": body_match.group(1).strip()
        # strip any HTML tags from body if needed:
        # "body": re.sub(r'<[^>]+>', '', body_match.group(1)).strip()
    })

print(f"Parsed {len(contacts)} contacts")
```

**Note:** The exact CSS class names vary between tracker versions. If the regex doesn't match, inspect the actual HTML structure and adjust the selectors. The key fields to extract are: numeric ID, full name, first name, email, approved subject, approved body.

### Step 3: Validation Pass

Before writing the JSON, validate every contact:

```python
errors = []
warnings = []

for c in contacts:
    # Required fields check
    if not c['email'] or '@' not in c['email']:
        errors.append(f"ID {c['id']} ({c['name']}): invalid email")
    if not c['subject'] or len(c['subject']) < 5:
        errors.append(f"ID {c['id']} ({c['name']}): subject too short or missing")
    if not c['body'] or len(c['body']) < 50:
        errors.append(f"ID {c['id']} ({c['name']}): body too short or missing")

    # Placeholder check
    for placeholder in ['[COMPANY]', '{name}', '[NAME]', 'FIRSTNAME', 'INSERT']:
        if placeholder.lower() in c['body'].lower() or placeholder.lower() in c['subject'].lower():
            errors.append(f"ID {c['id']} ({c['name']}): placeholder text found: {placeholder}")

    # Word count check (T1: 75-99)
    word_count = len(c['body'].split())
    if word_count < 60 or word_count > 110:
        warnings.append(f"ID {c['id']} ({c['name']}): word count {word_count} (expected 75-99)")

    # First name in subject check
    if c['first'].lower() not in c['subject'].lower():
        warnings.append(f"ID {c['id']} ({c['name']}): first name not in subject")

if errors:
    print("❌ ERRORS (must fix before proceeding):")
    for e in errors: print(f"  {e}")
else:
    print("✅ No errors")

if warnings:
    print("⚠️ WARNINGS (review recommended):")
    for w in warnings: print(f"  {w}")
```

Stop and present errors to Rob if any validation errors exist. Warnings can proceed with Rob's acknowledgment.

### Step 4: Write the JSON

```python
output_path = f"batch{N}_sends.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(contacts, f, indent=2, ensure_ascii=False)

print(f"✅ Written to {output_path}: {len(contacts)} contacts")
print(f"   Fields per record: id, name, first, email, subject, body")
```

### Step 5: Spot-Check 3 Random Contacts

Print 3 random entries (first, middle, last) for Rob to eyeball:
```python
import random
samples = [contacts[0], contacts[len(contacts)//2], contacts[-1]]
for s in samples:
    print(f"\n--- ID {s['id']}: {s['name']} ({s['email']}) ---")
    print(f"SUBJECT: {s['subject']}")
    print(f"BODY ({len(s['body'].split())} words): {s['body'][:200]}...")
```

Ask Rob: "Spot-check looks good? Ready to proceed with sends?"

### Step 6: Confirm for Apollo Send Skill

Once Rob confirms:
1. State the output file path: `/sessions/epic-laughing-ptolemy/batch{N}_sends.json`
2. State the count: "N contacts ready to send"
3. Hand off to `skills/apollo-send/SKILL.md`

---

## Output File Format

```json
[
  {
    "id": 1,
    "name": "Jane Smith",
    "first": "Jane",
    "email": "jane.smith@company.com",
    "subject": "Jane's regression coverage at Company",
    "body": "Hi Jane,\n\nSaw that Company is scaling..."
  },
  ...
]
```

The `id` field is the numeric position in the tracker (1-indexed). It's used by the apollo-send skill's Python lookup command.

---

## When the Tracker HTML Doesn't Have Clean CSS Classes

Some tracker versions use inline styles or different class conventions. If the regex parsing fails:

1. Open the tracker HTML in a text editor and search for the first contact's email address
2. Identify the surrounding HTML structure (what tags/classes wrap the subject and body)
3. Update the regex patterns to match
4. Or: manually copy the approved content into a JSON template and validate step-by-step

This is a one-time fix per tracker version — once you've adjusted the parser for a tracker format, it works for all contacts in that tracker.

---

## Tracker Formats Known

| Tracker Version | Subject Selector | Body Selector | Notes |
|----------------|-----------------|---------------|-------|
| tamob-batch-20260313-2.html | TBD | TBD | First tracker to use this skill — update this table after first run |

---

*Created: 2026-03-14 (Session 37). Designed to replace the ad-hoc batch_sends.json construction that was done manually before Batch 9 sends. Prerequisite for `skills/apollo-send/SKILL.md`. Update the "Tracker Formats Known" table with verified selectors after first production run.*

---

## Self-Improvement Loop

This skill maintains its own run log and learned-patterns file. Full protocol: `skills/_shared/learning-loop.md`

### Before Each Run
1. Read `skills/batch-json-builder/learned-patterns.md` if it exists — apply any documented calibration adjustments
2. Count entries in `skills/batch-json-builder/run-log.md` to determine current run number

### After Every Run — Append to run-log.md
```
### Run #[N] — [YYYY-MM-DD HH:MM]
- **Result:** [1-2 sentence summary]
- **Key metrics:** [skill-specific counts per _shared/learning-loop.md]
- **Anomalies:** [anything unexpected]
- **Adjustments made this run:** [any deviations from SKILL.md]
- **Output quality:** [Accurate / Mostly accurate / Needs calibration / Failed]
```

### Every 5th Run — Pattern Review
1. Read last 5 run-log.md entries
2. Extract recurring patterns, consistent edge cases, metric drift
3. Overwrite `skills/batch-json-builder/learned-patterns.md` with updated findings
4. If a pattern appears in 4+ of 5 runs: write a `## SKILL UPDATE PROPOSAL — batch-json-builder` entry to `memory/session/messages.md` for Rob's review

**Hard rule:** Never modify SKILL.md directly. Only propose updates via messages.md and wait for Rob's explicit approval.
