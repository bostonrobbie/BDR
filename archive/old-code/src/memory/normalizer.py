"""
Memory Normalizer - Transforms raw files into structured template format.

Takes classified files and either:
1. Validates they already match the template structure (pass-through)
2. Restructures free-form content into the correct template
3. Parses CSV/JSON rows into individual structured files

Preserves ALL original data. Never discards content.
"""

import csv
import io
import json
import os
import re
from datetime import datetime
from typing import Optional

from .classifier import extract_metadata_from_content


# ─── TEMPLATE SCAFFOLDS ─────────────────────────────────────

def _call_note_scaffold(meta: dict, raw_content: str) -> str:
    """Build a call note from raw content + extracted metadata."""
    person = meta.get("person_name", "[Unknown]")
    company = meta.get("company_name", "[Unknown]")
    date = meta.get("date", datetime.now().strftime("%Y-%m-%d"))
    tools = ", ".join(meta.get("tools_mentioned", [])) or "[not mentioned]"
    pains = ", ".join(meta.get("pain_signals", [])) or "[not identified]"

    return f"""# Call Notes: {person} at {company}

**Date:** {date}
**Call type:** [cold call / follow-up / discovery / meeting]
**Duration:** [X minutes]
**Outcome:** [connected / voicemail / no_answer / meeting_booked / not_interested / callback_requested]

## Quick Summary

{_extract_summary(raw_content)}

## What They Said (Key Quotes)

{_extract_quotes(raw_content)}

## Their Stack

- Current test automation: {tools}
- CI/CD: [if mentioned]
- Languages/frameworks: [if mentioned]
- Other tools: [if mentioned]

## Their Pain

- What they're struggling with: {pains}
- How bad is it: [mild annoyance / real problem / hair on fire]
- Who else feels it: [just them / their team / leadership knows]

## Their Timeline

- Are they evaluating tools now? [yes / no / unclear]
- Any deadline or mandate driving this? [describe]
- Budget cycle: [this quarter / next quarter / unknown]

## Objections Raised

| Objection | My Response | Their Reaction |
|-----------|------------|---------------|
| [fill in] | [fill in] | [fill in] |

## Next Steps

- [ ] [fill in]
- Follow-up date: [YYYY-MM-DD]

## Insights for Future Outreach

- [fill in]

## Tags

- Persona: [qa_director / vp_eng / sdet / etc.]
- Vertical: {meta.get("vertical", "[fill in]").lower()}
- Pain: {pains}
- Competitor mentioned: {_first_competitor(meta) or "[none]"}
- Temperature: [hot / warm / cool / cold]

---
**Original content preserved below:**

{raw_content}
"""


def _win_scaffold(meta: dict, raw_content: str) -> str:
    """Build a win report from raw content + extracted metadata."""
    company = meta.get("company_name", "[Unknown]")
    person = meta.get("person_name", "[Unknown]")
    date = meta.get("date", datetime.now().strftime("%Y-%m-%d"))
    vertical = meta.get("vertical", "[fill in]")

    return f"""# Win Report: {company}

**Date closed:** {date}
**Prospect:** {person}
**Company:** {company}
**Vertical:** {vertical}
**Company size:** [fill in]
**AE:** {meta.get("ae", "[fill in]")}

## How They Found Us

- Source: [outbound / inbound / referral / event]
- First touch channel: [linkedin / email / call]
- Touch that got the reply: [fill in]
- What triggered the reply: [opener / pain_hook / proof_point / timing / referral]

## Their Pain (In Their Words)

{_extract_quotes(raw_content)}

- Primary pain: {", ".join(meta.get("pain_signals", ["[fill in]"]))}
- Current tool(s): {", ".join(meta.get("tools_mentioned", ["[fill in]"]))}
- What they tried before us: [fill in]

## What Resonated

- Proof point that landed: [fill in]
- Capability that mattered most: [fill in]
- ROI angle that clicked: [fill in]

## Objections We Overcame

| Objection | How We Handled It | Did It Work? |
|-----------|-------------------|-------------|
| [fill in] | [fill in] | [fill in] |

## Decision Process

- Decision maker: [fill in]
- Influencer(s): [fill in]
- Timeline from first touch to meeting: [X days]
- Timeline from meeting to closed: [X days]
- What accelerated the deal: [fill in]
- What almost killed it: [fill in]

## Key Takeaways

1. [fill in]
2. [fill in]
3. [fill in]

## Tags

- Pain: {", ".join(meta.get("pain_signals", ["[fill in]"]))}
- Vertical: {vertical.lower()}
- Competitor displaced: {_first_competitor(meta) or "[none]"}
- Deal size: [small / medium / large]
- Cycle length: [fast (<30 days) / medium (30-90) / long (90+)]

---
**Original content preserved below:**

{raw_content}
"""


def _loss_scaffold(meta: dict, raw_content: str) -> str:
    """Build a loss report from raw content + extracted metadata."""
    company = meta.get("company_name", "[Unknown]")
    person = meta.get("person_name", "[Unknown]")
    date = meta.get("date", datetime.now().strftime("%Y-%m-%d"))
    vertical = meta.get("vertical", "[fill in]")

    return f"""# Loss Report: {company}

**Date lost:** {date}
**Prospect:** {person}
**Company:** {company}
**Vertical:** {vertical}
**Company size:** [fill in]
**Stage reached:** [meeting_booked / meeting_held / trial / proposal / negotiation]

## What Happened

{_extract_summary(raw_content)}

## Their Pain Was Real

- Primary pain: {", ".join(meta.get("pain_signals", ["[fill in]"]))}
- Current tool(s): {", ".join(meta.get("tools_mentioned", ["[fill in]"]))}
- Pain was: [confirmed on call / assumed from research / unclear]

## Why We Lost

- **Primary reason:** [chose competitor / no budget / no urgency / champion left / security/compliance blocker / bad timing / poor discovery / other]
- **If chose competitor, which one:** {_first_competitor(meta) or "[fill in]"}
- **What the competitor had that we didn't:** [fill in]

## What We Could Have Done Differently

1. [fill in]
2. [fill in]
3. [fill in]

## Objections We Didn't Overcome

| Objection | Our Response | Why It Didn't Work |
|-----------|-------------|-------------------|
| [fill in] | [fill in] | [fill in] |

## Signals We Missed

- [fill in]

## Re-Engagement Potential

- Can we re-engage later? [yes / no / maybe]
- Best trigger for re-engagement: [contract renewal / new QA hire / product launch / funding]
- Estimated re-engagement window: [unknown]

## Key Takeaways

1. [fill in]
2. [fill in]
3. [fill in]

## Tags

- Lost to: {_first_competitor(meta) or "[fill in]"}
- Vertical: {vertical.lower()}
- Stage: [meeting / trial / proposal / negotiation]
- Recoverable: [yes / no / maybe]

---
**Original content preserved below:**

{raw_content}
"""


# ─── HELPERS ─────────────────────────────────────────────────

def _extract_summary(content: str) -> str:
    """Extract or generate a 1-2 sentence summary from content."""
    lines = [l.strip() for l in content.split("\n") if l.strip()
             and not l.strip().startswith("#")
             and not l.strip().startswith("**")
             and not l.strip().startswith("-")
             and not l.strip().startswith("|")]
    if lines:
        # Take the first non-header, non-metadata line(s)
        summary = " ".join(lines[:2])
        if len(summary) > 300:
            summary = summary[:297] + "..."
        return summary
    return "[Summarize from original content below]"


def _extract_quotes(content: str) -> str:
    """Extract quoted lines from content."""
    quotes = []
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith(">") or stripped.startswith('"'):
            quotes.append(stripped if stripped.startswith(">") else f"> {stripped}")
    if quotes:
        return "\n\n".join(quotes[:5])
    return '> [Extract key quotes from original content below]'


def _first_competitor(meta: dict) -> Optional[str]:
    """Get the first competitor tool from metadata."""
    tools = meta.get("tools_mentioned", [])
    competitors = {"selenium", "cypress", "playwright", "katalon", "tosca",
                   "mabl", "testim", "uft", "appium", "browserstack"}
    for t in tools:
        if t.lower() in competitors:
            return t
    return None


# ─── MAIN NORMALIZER ────────────────────────────────────────

SCAFFOLDS = {
    "call_note": _call_note_scaffold,
    "win": _win_scaffold,
    "loss": _loss_scaffold,
}


def is_already_structured(content: str, category: str) -> bool:
    """Check if content already follows the template structure.

    If it has the right headers and metadata fields, it's already structured
    and doesn't need normalization.
    """
    markers = {
        "call_note": ["## Quick Summary", "## Their Stack", "## Tags"],
        "win": ["## How They Found Us", "## What Resonated", "## Tags"],
        "loss": ["## Why We Lost", "## What We Could Have Done", "## Tags"],
        "competitor": ["## Where", "## Common Objections", "## Talk Track"],
        "market_intel": [],  # Market intel doesn't have a fixed template
    }

    required = markers.get(category, [])
    if not required:
        return True  # No template to match against

    matched = sum(1 for m in required if m.lower() in content.lower())
    return matched >= len(required) - 1  # Allow one missing section


def normalize_file(content: str, category: str, filepath: str = "") -> list:
    """Normalize file content into structured format(s).

    Args:
        content: Raw file content.
        category: Classified category from classifier.
        filepath: Original file path (for format detection).

    Returns:
        List of dicts, each with:
            filename: str - Suggested filename for the normalized file
            content: str - Structured content
            metadata: dict - Extracted metadata
    """
    # Already structured? Pass through
    if is_already_structured(content, category):
        meta = extract_metadata_from_content(content)
        return [{
            "filename": _generate_filename(meta, category, filepath),
            "content": content,
            "metadata": meta,
            "was_restructured": False,
        }]

    # CSV files may contain multiple records
    ext = os.path.splitext(filepath)[1].lower() if filepath else ""
    if ext == ".csv":
        return _normalize_csv(content, category)

    # JSON files may contain multiple records
    if ext == ".json":
        return _normalize_json(content, category)

    # Single markdown/text file
    meta = extract_metadata_from_content(content)
    scaffold_fn = SCAFFOLDS.get(category)

    if scaffold_fn:
        structured = scaffold_fn(meta, content)
    else:
        # For competitor and market_intel, pass through with metadata header
        structured = content

    return [{
        "filename": _generate_filename(meta, category, filepath),
        "content": structured,
        "metadata": meta,
        "was_restructured": True,
    }]


def _normalize_csv(content: str, category: str) -> list:
    """Parse a CSV into multiple structured files."""
    results = []
    reader = csv.DictReader(io.StringIO(content))

    for i, row in enumerate(reader):
        # Build pseudo-content from row
        lines = []
        for key, value in row.items():
            if value and value.strip():
                lines.append(f"**{key}:** {value.strip()}")

        pseudo_content = "\n".join(lines)
        meta = extract_metadata_from_content(pseudo_content)

        # Also pull metadata directly from common CSV column names
        col_map = {
            "name": "person_name", "contact": "person_name", "prospect": "person_name",
            "company": "company_name", "account": "company_name", "organization": "company_name",
            "date": "date", "call_date": "date", "close_date": "date",
            "vertical": "vertical", "industry": "vertical",
        }
        for col, meta_key in col_map.items():
            for csv_key in row:
                if col in csv_key.lower() and row[csv_key] and meta_key not in meta:
                    meta[meta_key] = row[csv_key].strip()

        scaffold_fn = SCAFFOLDS.get(category)
        if scaffold_fn:
            structured = scaffold_fn(meta, pseudo_content)
        else:
            structured = pseudo_content

        results.append({
            "filename": _generate_filename(meta, category, suffix=f"-row{i+1}"),
            "content": structured,
            "metadata": meta,
            "was_restructured": True,
        })

    return results


def _normalize_json(content: str, category: str) -> list:
    """Parse JSON into structured files."""
    results = []
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return [{
            "filename": f"{datetime.now().strftime('%Y-%m-%d')}-unknown.md",
            "content": content,
            "metadata": {},
            "was_restructured": False,
        }]

    # Handle array of records
    records = data if isinstance(data, list) else [data]

    for i, record in enumerate(records):
        pseudo_content = json.dumps(record, indent=2)
        meta = extract_metadata_from_content(pseudo_content)

        # Pull metadata from common JSON keys
        key_map = {
            "name": "person_name", "contact_name": "person_name", "prospect_name": "person_name",
            "company": "company_name", "company_name": "company_name", "account_name": "company_name",
            "date": "date", "call_date": "date",
            "vertical": "vertical", "industry": "vertical",
        }
        for json_key, meta_key in key_map.items():
            if json_key in record and record[json_key] and meta_key not in meta:
                meta[meta_key] = str(record[json_key]).strip()

        scaffold_fn = SCAFFOLDS.get(category)
        if scaffold_fn:
            structured = scaffold_fn(meta, pseudo_content)
        else:
            structured = pseudo_content

        suffix = f"-item{i+1}" if len(records) > 1 else ""
        results.append({
            "filename": _generate_filename(meta, category, suffix=suffix),
            "content": structured,
            "metadata": meta,
            "was_restructured": True,
        })

    return results


def _generate_filename(meta: dict, category: str, filepath: str = "", suffix: str = "") -> str:
    """Generate a standard filename following the naming convention.

    Convention: YYYY-MM-DD-firstname-lastname.md (call notes)
                YYYY-MM-DD-company-name.md (wins, losses)
                tool-name.md (competitors)
                descriptive-name.md (market intel)
    """
    date = meta.get("date", datetime.now().strftime("%Y-%m-%d"))

    if category == "call_note":
        person = meta.get("person_name", "unknown")
        slug = _slugify(person)
        return f"{date}-{slug}{suffix}.md"

    if category in ("win", "loss"):
        company = meta.get("company_name", "unknown")
        slug = _slugify(company)
        return f"{date}-{slug}{suffix}.md"

    if category == "competitor":
        # Try to identify the tool from content
        tools = meta.get("tools_mentioned", [])
        if tools:
            return f"{_slugify(tools[0])}{suffix}.md"
        if filepath:
            return os.path.basename(filepath)
        return f"competitor-update-{date}{suffix}.md"

    if category == "market_intel":
        if filepath:
            base = os.path.splitext(os.path.basename(filepath))[0]
            return f"{_slugify(base)}{suffix}.md"
        return f"intel-{date}{suffix}.md"

    # Unknown
    if filepath:
        return os.path.basename(filepath)
    return f"unclassified-{date}{suffix}.md"


def _slugify(text: str) -> str:
    """Convert text to a filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:50]
