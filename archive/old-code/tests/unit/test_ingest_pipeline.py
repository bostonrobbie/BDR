"""Tests for the memory ingest pipeline: classifier, normalizer, audit, and end-to-end."""

import json
import os
import shutil
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.memory.classifier import classify_file, classify_content_type, extract_metadata_from_content
from src.memory.normalizer import normalize_file, is_already_structured, _slugify
from src.memory.audit import (
    compute_content_hash, is_duplicate, register_hash, log_action,
    get_log, get_stats, _load_hash_index,
)
from src.memory.ingest import process_file, process_inbox, _resolve_collision


# ─── FIXTURES ────────────────────────────────────────────────

@pytest.fixture
def tmp_memory(tmp_path):
    """Create a temporary memory directory with proper structure."""
    dirs = ["inbox", "call-notes", "wins", "losses", "competitors",
            "market-intel", "context", ".audit", ".audit/processed"]
    for d in dirs:
        (tmp_path / d).mkdir(parents=True, exist_ok=True)
    return tmp_path


@pytest.fixture(autouse=True)
def patch_memory_root(tmp_memory, monkeypatch):
    """Patch MEMORY_ROOT in all modules to use temp directory."""
    root = str(tmp_memory)
    monkeypatch.setattr("src.memory.audit.MEMORY_ROOT", root)
    monkeypatch.setattr("src.memory.audit.AUDIT_DIR", os.path.join(root, ".audit"))
    monkeypatch.setattr("src.memory.audit.LOG_FILE", os.path.join(root, ".audit", "log.jsonl"))
    monkeypatch.setattr("src.memory.audit.PROCESSED_DIR", os.path.join(root, ".audit", "processed"))
    monkeypatch.setattr("src.memory.audit.HASH_INDEX", os.path.join(root, ".audit", "hash_index.json"))
    monkeypatch.setattr("src.memory.ingest.MEMORY_ROOT", root)
    monkeypatch.setattr("src.memory.ingest.INBOX_DIR", os.path.join(root, "inbox"))


# ─── SAMPLE CONTENT ─────────────────────────────────────────

SAMPLE_CALL_NOTE = """# Call Notes: Sarah Chen at Acme Corp

**Date:** 2026-02-15
**Call type:** cold call
**Duration:** 8 minutes
**Outcome:** connected

## Quick Summary

Spoke with Sarah, she's the Director of QA. They're using Selenium with a custom
framework built over 3 years. Maintenance is killing them.

## What They Said (Key Quotes)

> "We spend 60% of our time fixing broken tests, not writing new ones"

> "Every time the UI team ships a redesign, half our suite breaks"

## Their Stack

- Current test automation: Selenium, custom Java framework
- CI/CD: Jenkins
- Other tools: Jira, TestRail

## Their Pain

- What they're struggling with: Test maintenance after UI changes
- How bad is it: real problem
- Who else feels it: leadership knows

## Their Timeline

- Are they evaluating tools now? yes
- Budget cycle: next quarter

## Objections Raised

| Objection | My Response | Their Reaction |
|-----------|------------|---------------|
| "We've invested 3 years in our Selenium framework" | "Most teams keep Selenium for edge cases and use Testsigma for the 80%" | Seemed open to it |

## Next Steps

- [ ] Send comparison deck
- Follow-up date: 2026-02-22

## Tags

- Persona: qa_director
- Vertical: saas
- Pain: maintenance
- Competitor mentioned: selenium
- Temperature: warm
"""

SAMPLE_WIN_REPORT = """# Win Report: Acme Corp

**Date closed:** 2026-01-15
**Prospect:** Sarah Chen, Director of QA
**Company:** Acme Corp
**Vertical:** SaaS
**Company size:** 500
**AE:** Mike Johnson

## How They Found Us

- Source: outbound
- First touch channel: linkedin
- Touch that got the reply: Touch 3, email
- What triggered the reply: pain_hook

## Their Pain (In Their Words)

> "We were spending 60% of QA time on maintenance"

## What Resonated

- Proof point that landed: Spendflo 50% manual cut
- Capability that mattered most: self-healing
- ROI angle that clicked: time saved

## Tags

- Pain: maintenance
- Vertical: saas
- Competitor displaced: selenium
- Deal size: medium
- Cycle length: medium (30-90)
"""

SAMPLE_LOSS_REPORT = """# Loss Report: Beta Inc

**Date lost:** 2026-01-20
**Prospect:** John Smith, VP Engineering
**Company:** Beta Inc
**Vertical:** FinTech

## What Happened

They chose Playwright. Their SDET team was deeply invested in TypeScript and
didn't want to learn a new paradigm.

## Why We Lost

- **Primary reason:** chose competitor
- **If chose competitor, which one:** Playwright
- **What the competitor had that we didn't:** Free, their team already knew TypeScript

## What We Could Have Done Differently

1. Should have engaged the SDET team earlier
2. Should have led with the "complement, don't replace" angle

## Tags

- Lost to: playwright
- Vertical: fintech
- Stage: trial
- Recoverable: maybe
"""

SAMPLE_RAW_NOTES = """Called Dave Martinez at TechFlow Inc today. He's the QA Manager.

They use Cypress for their web app testing but have no mobile coverage.
He mentioned they're shipping a React Native app next quarter and are
worried about how to test it.

"We don't have anyone who knows Appium and we can't afford to hire"

He seemed interested when I mentioned Medibuddy's 2,500 tests story.
Asked me to send more info. Following up Thursday.
"""

SAMPLE_COMPETITOR_INTEL = """# Playwright Battle Card Update

## Where Playwright Falls Short (Our Angle)

### 7. New limitation discovered
- Playwright's trace viewer doesn't support collaborative debugging.
- Teams can't easily share test failure analysis.
- **Testsigma angle:** Built-in collaborative debugging with shared traces.

## Common Objections When Displacing

| Objection | Response |
|-----------|----------|
| "Playwright traces are amazing" | "They are. The gap is when 3 people need to debug the same failure. Testsigma's collaborative view is built for that." |
"""

SAMPLE_MARKET_INTEL = """# Market Trends Update - Q1 2026

## Competitor Moves (Recent)

| Date | Competitor | Move | Impact |
|------|-----------|------|--------|
| 2026-01 | Playwright | v1.50 with AI assist | Growing threat, need updated messaging |
| 2026-02 | Katalon | Launched AI test generation | More competitive on AI claims |

## Industry Trends

The shift toward AI-native testing tools is accelerating. Gartner now lists
"AI-augmented testing" as entering the "Slope of Enlightenment."
"""

SAMPLE_CSV = """name,company,date,call_type,outcome,notes
Sarah Chen,Acme Corp,2026-02-15,cold call,connected,Uses Selenium. Maintenance pain.
Dave Martinez,TechFlow,2026-02-16,cold call,voicemail,Left VM about Cypress mobile gap.
"""

SAMPLE_JSON = """[
  {
    "name": "Sarah Chen",
    "company": "Acme Corp",
    "date": "2026-02-15",
    "outcome": "connected",
    "notes": "Uses Selenium. Maintenance is their biggest pain."
  },
  {
    "name": "Dave Martinez",
    "company_name": "TechFlow",
    "date": "2026-02-16",
    "outcome": "voicemail",
    "notes": "Uses Cypress. No mobile testing."
  }
]
"""


# ─── CLASSIFIER TESTS ───────────────────────────────────────

class TestClassifier:
    def test_classify_call_note_structured(self, tmp_memory):
        path = str(tmp_memory / "inbox" / "call.md")
        with open(path, "w") as f:
            f.write(SAMPLE_CALL_NOTE)
        result = classify_file(path)
        assert result["category"] == "call_note"
        assert result["confidence"] > 0.3

    def test_classify_call_note_raw(self, tmp_memory):
        path = str(tmp_memory / "inbox" / "notes.txt")
        with open(path, "w") as f:
            f.write(SAMPLE_RAW_NOTES)
        result = classify_file(path)
        assert result["category"] == "call_note"

    def test_classify_win(self, tmp_memory):
        path = str(tmp_memory / "inbox" / "win.md")
        with open(path, "w") as f:
            f.write(SAMPLE_WIN_REPORT)
        result = classify_file(path)
        assert result["category"] == "win"

    def test_classify_loss(self, tmp_memory):
        path = str(tmp_memory / "inbox" / "loss.md")
        with open(path, "w") as f:
            f.write(SAMPLE_LOSS_REPORT)
        result = classify_file(path)
        assert result["category"] == "loss"

    def test_classify_competitor(self, tmp_memory):
        path = str(tmp_memory / "inbox" / "competitor.md")
        with open(path, "w") as f:
            f.write(SAMPLE_COMPETITOR_INTEL)
        result = classify_file(path)
        assert result["category"] == "competitor"

    def test_classify_market_intel(self, tmp_memory):
        path = str(tmp_memory / "inbox" / "market.md")
        with open(path, "w") as f:
            f.write(SAMPLE_MARKET_INTEL)
        result = classify_file(path)
        assert result["category"] == "market_intel"

    def test_classify_unknown(self, tmp_memory):
        path = str(tmp_memory / "inbox" / "random.md")
        with open(path, "w") as f:
            f.write("Just some random text that doesn't match anything specific.")
        result = classify_file(path)
        assert result["category"] == "unknown"

    def test_classify_from_content(self):
        result = classify_file("fake.md", content=SAMPLE_CALL_NOTE)
        assert result["category"] == "call_note"

    def test_scores_present(self, tmp_memory):
        path = str(tmp_memory / "inbox" / "call.md")
        with open(path, "w") as f:
            f.write(SAMPLE_CALL_NOTE)
        result = classify_file(path)
        assert "scores" in result
        assert "call_note" in result["scores"]

    def test_content_type_detection(self):
        assert classify_content_type("file.md") == "markdown"
        assert classify_content_type("file.csv") == "csv"
        assert classify_content_type("file.json") == "json"
        assert classify_content_type("file.txt") == "text"
        assert classify_content_type("file.xyz") == "unknown"


class TestMetadataExtraction:
    def test_extract_date(self):
        meta = extract_metadata_from_content("**Date:** 2026-02-15\nSome content")
        assert meta["date"] == "2026-02-15"

    def test_extract_tools(self):
        meta = extract_metadata_from_content("They use Selenium and Cypress for testing")
        assert "selenium" in meta["tools_mentioned"]
        assert "cypress" in meta["tools_mentioned"]

    def test_extract_pain(self):
        meta = extract_metadata_from_content("Test maintenance is their biggest problem. Flaky tests everywhere.")
        assert "maintenance" in meta["pain_signals"]

    def test_extract_company(self):
        meta = extract_metadata_from_content("**Company:** Acme Corp")
        assert meta["company_name"] == "Acme Corp"


# ─── NORMALIZER TESTS ───────────────────────────────────────

class TestNormalizer:
    def test_structured_passthrough(self):
        """Already-structured files should pass through without restructuring."""
        results = normalize_file(SAMPLE_CALL_NOTE, "call_note", "call.md")
        assert len(results) == 1
        assert results[0]["was_restructured"] is False
        assert results[0]["content"] == SAMPLE_CALL_NOTE

    def test_raw_text_restructured(self):
        """Raw text should be restructured into the template."""
        results = normalize_file(SAMPLE_RAW_NOTES, "call_note", "notes.txt")
        assert len(results) == 1
        assert results[0]["was_restructured"] is True
        assert "## Quick Summary" in results[0]["content"]
        assert "## Their Stack" in results[0]["content"]
        assert "## Tags" in results[0]["content"]
        # Original content should be preserved
        assert "Dave Martinez" in results[0]["content"]
        assert "TechFlow" in results[0]["content"]

    def test_csv_produces_multiple_files(self):
        """CSV with multiple rows should produce multiple files."""
        results = normalize_file(SAMPLE_CSV, "call_note", "calls.csv")
        assert len(results) == 2
        assert "Sarah Chen" in results[0]["content"] or "Sarah Chen" in results[1]["content"]
        assert "Dave Martinez" in results[0]["content"] or "Dave Martinez" in results[1]["content"]

    def test_json_produces_multiple_files(self):
        """JSON array should produce multiple files."""
        results = normalize_file(SAMPLE_JSON, "call_note", "calls.json")
        assert len(results) == 2

    def test_win_scaffold(self):
        """Raw win content should be restructured."""
        raw = "Closed Acme Corp! Sarah Chen signed after seeing the Spendflo demo."
        results = normalize_file(raw, "win", "win-acme.md")
        assert len(results) == 1
        assert "## How They Found Us" in results[0]["content"]

    def test_loss_scaffold(self):
        """Raw loss content should be restructured."""
        raw = "Lost Beta Inc. They chose Playwright because their team knows TypeScript."
        results = normalize_file(raw, "loss", "loss-beta.md")
        assert len(results) == 1
        assert "## Why We Lost" in results[0]["content"]
        assert "playwright" in results[0]["content"].lower()

    def test_original_preserved(self):
        """Original content must always be preserved in normalized output."""
        results = normalize_file(SAMPLE_RAW_NOTES, "call_note", "notes.txt")
        assert "Original content preserved below" in results[0]["content"]
        assert "Dave Martinez" in results[0]["content"]
        assert "Cypress" in results[0]["content"]

    def test_slugify(self):
        assert _slugify("Sarah Chen") == "sarah-chen"
        assert _slugify("Acme Corp Inc.") == "acme-corp-inc"
        assert _slugify("  spaces  and   stuff  ") == "spaces-and-stuff"


class TestStructureDetection:
    def test_structured_call_note(self):
        assert is_already_structured(SAMPLE_CALL_NOTE, "call_note") is True

    def test_structured_win(self):
        assert is_already_structured(SAMPLE_WIN_REPORT, "win") is True

    def test_structured_loss(self):
        assert is_already_structured(SAMPLE_LOSS_REPORT, "loss") is True

    def test_raw_not_structured(self):
        assert is_already_structured(SAMPLE_RAW_NOTES, "call_note") is False

    def test_market_intel_always_structured(self):
        """Market intel has no fixed template, always returns True."""
        assert is_already_structured("anything", "market_intel") is True


# ─── AUDIT & DEDUP TESTS ────────────────────────────────────

class TestAudit:
    def test_log_action(self):
        entry = log_action("test", "/fake/file.md", category="call_note")
        assert entry["action"] == "test"
        assert entry["source_file"] == "file.md"

    def test_get_log(self):
        log_action("test1", "/file1.md")
        log_action("test2", "/file2.md")
        entries = get_log(limit=10)
        assert len(entries) == 2
        # Most recent first
        assert entries[0]["source_file"] == "file2.md"

    def test_get_log_filter(self):
        log_action("ingested", "/file1.md")
        log_action("skipped", "/file2.md")
        entries = get_log(action_filter="ingested")
        assert len(entries) == 1
        assert entries[0]["action"] == "ingested"

    def test_get_stats(self):
        log_action("ingested", "/f1.md", category="call_note")
        log_action("ingested", "/f2.md", category="win")
        log_action("duplicate", "/f3.md", category="call_note")
        stats = get_stats()
        assert stats["total_processed"] == 3
        assert stats["by_action"]["ingested"] == 2
        assert stats["by_category"]["call_note"] == 2


class TestDedup:
    def test_hash_deterministic(self):
        h1 = compute_content_hash("hello world")
        h2 = compute_content_hash("hello world")
        assert h1 == h2

    def test_hash_whitespace_normalized(self):
        h1 = compute_content_hash("hello   world\n\n")
        h2 = compute_content_hash("  hello world  ")
        assert h1 == h2

    def test_hash_different_content(self):
        h1 = compute_content_hash("content A")
        h2 = compute_content_hash("content B")
        assert h1 != h2

    def test_register_and_detect_duplicate(self):
        content = "unique test content for dedup"
        assert is_duplicate(content) is None
        register_hash(content, "/src/file.md", "/dest/file.md")
        dup = is_duplicate(content)
        assert dup is not None
        assert "dest/file.md" in dup

    def test_no_false_positive(self):
        register_hash("content A", "/a.md", "/dest/a.md")
        assert is_duplicate("content B") is None


# ─── END-TO-END PIPELINE TESTS ──────────────────────────────

class TestPipelineE2E:
    def test_process_call_note(self, tmp_memory):
        """Full pipeline: structured call note in inbox -> call-notes/."""
        inbox_file = str(tmp_memory / "inbox" / "sarah-call.md")
        with open(inbox_file, "w") as f:
            f.write(SAMPLE_CALL_NOTE)

        result = process_file(inbox_file)
        assert result["status"] == "processed"
        assert result["category"] == "call_note"
        assert len(result["files_created"]) == 1

        # File should be in call-notes/
        dest = result["files_created"][0]
        assert "/call-notes/" in dest
        assert os.path.exists(dest)

        # Original should be archived
        assert not os.path.exists(inbox_file)
        processed = list((tmp_memory / ".audit" / "processed").iterdir())
        assert len(processed) == 1

    def test_process_raw_notes(self, tmp_memory):
        """Full pipeline: raw text -> restructured call note."""
        inbox_file = str(tmp_memory / "inbox" / "dave-notes.txt")
        with open(inbox_file, "w") as f:
            f.write(SAMPLE_RAW_NOTES)

        result = process_file(inbox_file, verbose=True)
        assert result["status"] == "processed"
        assert len(result["files_created"]) == 1

        # Read the created file, verify structure
        with open(result["files_created"][0]) as f:
            content = f.read()
        assert "## Quick Summary" in content
        assert "## Tags" in content
        assert "Dave Martinez" in content

    def test_process_win(self, tmp_memory):
        inbox_file = str(tmp_memory / "inbox" / "win-acme.md")
        with open(inbox_file, "w") as f:
            f.write(SAMPLE_WIN_REPORT)

        result = process_file(inbox_file)
        assert result["status"] == "processed"
        assert result["category"] == "win"
        dest = result["files_created"][0]
        assert "/wins/" in dest

    def test_process_loss(self, tmp_memory):
        inbox_file = str(tmp_memory / "inbox" / "loss-beta.md")
        with open(inbox_file, "w") as f:
            f.write(SAMPLE_LOSS_REPORT)

        result = process_file(inbox_file)
        assert result["status"] == "processed"
        assert result["category"] == "loss"
        dest = result["files_created"][0]
        assert "/losses/" in dest

    def test_dedup_blocks_second_ingest(self, tmp_memory):
        """Same file processed twice should be blocked as duplicate."""
        inbox_file = str(tmp_memory / "inbox" / "call.md")
        with open(inbox_file, "w") as f:
            f.write(SAMPLE_CALL_NOTE)

        result1 = process_file(inbox_file)
        assert result1["status"] == "processed"

        # Drop the same content again
        inbox_file2 = str(tmp_memory / "inbox" / "call-copy.md")
        with open(inbox_file2, "w") as f:
            f.write(SAMPLE_CALL_NOTE)

        result2 = process_file(inbox_file2)
        assert result2["status"] == "duplicate"

    def test_force_bypasses_dedup(self, tmp_memory):
        """Force flag should bypass dedup check."""
        inbox_file = str(tmp_memory / "inbox" / "call.md")
        with open(inbox_file, "w") as f:
            f.write(SAMPLE_CALL_NOTE)
        process_file(inbox_file)

        inbox_file2 = str(tmp_memory / "inbox" / "call2.md")
        with open(inbox_file2, "w") as f:
            f.write(SAMPLE_CALL_NOTE)

        result = process_file(inbox_file2, force=True)
        assert result["status"] == "processed"

    def test_dry_run(self, tmp_memory):
        """Dry run should classify but not move."""
        inbox_file = str(tmp_memory / "inbox" / "call.md")
        with open(inbox_file, "w") as f:
            f.write(SAMPLE_CALL_NOTE)

        result = process_file(inbox_file, dry_run=True)
        assert result["status"] == "dry_run"
        assert os.path.exists(inbox_file)  # Not moved

    def test_skip_system_files(self, tmp_memory):
        inbox_file = str(tmp_memory / "inbox" / "README.md")
        with open(inbox_file, "w") as f:
            f.write("Inbox readme")

        result = process_file(inbox_file)
        assert result["status"] == "skipped"

    def test_skip_empty_files(self, tmp_memory):
        inbox_file = str(tmp_memory / "inbox" / "empty.md")
        with open(inbox_file, "w") as f:
            f.write("")

        result = process_file(inbox_file)
        assert result["status"] == "skipped"

    def test_csv_multi_record(self, tmp_memory):
        """CSV with multiple rows should create multiple files."""
        inbox_file = str(tmp_memory / "inbox" / "calls.csv")
        with open(inbox_file, "w") as f:
            f.write(SAMPLE_CSV)

        result = process_file(inbox_file)
        assert result["status"] == "processed"
        assert len(result["files_created"]) == 2

    def test_process_inbox_batch(self, tmp_memory):
        """Process entire inbox in one go."""
        # Drop multiple files
        files = [
            ("call.md", SAMPLE_CALL_NOTE),
            ("win.md", SAMPLE_WIN_REPORT),
            ("loss.md", SAMPLE_LOSS_REPORT),
        ]
        for name, content in files:
            with open(str(tmp_memory / "inbox" / name), "w") as f:
                f.write(content)

        results = process_inbox()
        processed = [r for r in results if r["status"] == "processed"]
        assert len(processed) == 3

    def test_filename_collision_resolution(self, tmp_memory):
        """Two files producing the same destination name should both be saved."""
        dest = str(tmp_memory / "call-notes" / "test.md")
        with open(dest, "w") as f:
            f.write("existing")

        resolved = _resolve_collision(dest)
        assert resolved != dest
        assert "-2" in resolved

    def test_audit_trail_complete(self, tmp_memory):
        """Every processed file should have an audit log entry."""
        inbox_file = str(tmp_memory / "inbox" / "call.md")
        with open(inbox_file, "w") as f:
            f.write(SAMPLE_CALL_NOTE)

        process_file(inbox_file)

        entries = get_log()
        ingested = [e for e in entries if e["action"] == "ingested"]
        assert len(ingested) >= 1
        assert ingested[0]["category"] == "call_note"
