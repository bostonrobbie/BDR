"""
Memory Ingest Pipeline - Auto-processes files into the memory layer.

Ties together: classifier, normalizer, dedup, and audit log.

Usage:
    # Process everything in memory/inbox/
    python -m src.memory.ingest

    # Process a specific file
    python -m src.memory.ingest path/to/file.md

    # Dry run (classify only, don't move)
    python -m src.memory.ingest --dry-run

    # Verbose output
    python -m src.memory.ingest --verbose

    # Show processing stats
    python -m src.memory.ingest --stats

    # Validate existing memory files are in the right place
    python -m src.memory.ingest --validate
"""

import argparse
import os
import shutil
import sys
from glob import glob

# Ensure project root is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.memory.classifier import classify_file, classify_content_type
from src.memory.normalizer import normalize_file, is_already_structured
from src.memory.audit import (
    log_action, archive_original, is_duplicate, register_hash,
    get_stats, get_log,
)


MEMORY_ROOT = os.path.join(os.path.dirname(__file__), "../../memory")
INBOX_DIR = os.path.join(MEMORY_ROOT, "inbox")

# Files to skip during processing
SKIP_FILES = {"README.md", "_template.md", "_index.json", ".gitkeep", ".DS_Store"}
SKIP_DIRS = {".audit", "__pycache__"}


def process_file(filepath: str, dry_run: bool = False, verbose: bool = False,
                 force: bool = False) -> dict:
    """Process a single file through the ingest pipeline.

    Args:
        filepath: Path to the file.
        dry_run: If True, classify but don't move anything.
        verbose: Print detailed output.
        force: Skip dedup check.

    Returns:
        Result dict with status, category, destination, etc.
    """
    basename = os.path.basename(filepath)
    result = {
        "file": basename,
        "path": filepath,
        "status": "pending",
        "category": None,
        "destination": None,
        "files_created": [],
    }

    # Skip special files
    if basename in SKIP_FILES or basename.startswith("."):
        result["status"] = "skipped"
        result["reason"] = "system file"
        if verbose:
            print(f"  SKIP {basename} (system file)")
        return result

    # Read content
    try:
        with open(filepath, "r", errors="replace") as f:
            content = f.read()
    except Exception as e:
        result["status"] = "error"
        result["reason"] = str(e)
        log_action("error", filepath, details=str(e))
        if verbose:
            print(f"  ERROR reading {basename}: {e}")
        return result

    if not content.strip():
        result["status"] = "skipped"
        result["reason"] = "empty file"
        if verbose:
            print(f"  SKIP {basename} (empty)")
        return result

    # Dedup check
    if not force:
        existing = is_duplicate(content)
        if existing:
            result["status"] = "duplicate"
            result["reason"] = f"already exists at {existing}"
            log_action("duplicate", filepath, details=f"matches {existing}")
            if verbose:
                print(f"  DUP  {basename} -> already at {existing}")
            return result

    # Classify
    classification = classify_file(filepath, content)
    category = classification["category"]
    confidence = classification["confidence"]
    result["category"] = category
    result["confidence"] = confidence

    if verbose:
        print(f"  CLASSIFY {basename} -> {category} (confidence: {confidence:.0%})")
        if classification.get("scores"):
            top_scores = sorted(classification["scores"].items(),
                                key=lambda x: x[1], reverse=True)[:3]
            for cat, score in top_scores:
                print(f"    {cat}: {score}")

    if category == "unknown":
        result["status"] = "unclassified"
        result["reason"] = "could not determine category"
        log_action("unclassified", filepath,
                   category=category, confidence=confidence,
                   details="scores: " + str(classification.get("scores", {})))
        if verbose:
            print(f"  UNKNOWN - left in inbox for manual review")
        return result

    # Normalize
    content_type = classify_content_type(filepath)
    normalized_files = normalize_file(content, category, filepath)

    if verbose and normalized_files:
        n = len(normalized_files)
        restructured = sum(1 for f in normalized_files if f.get("was_restructured"))
        print(f"  NORMALIZE -> {n} file(s), {restructured} restructured")

    if dry_run:
        result["status"] = "dry_run"
        result["would_create"] = [nf["filename"] for nf in normalized_files]
        result["destination"] = classification["destination"]
        log_action("dry_run", filepath, category=category, confidence=confidence)
        return result

    # Move files to destination
    dest_dir = os.path.join(MEMORY_ROOT, classification["destination"])
    os.makedirs(dest_dir, exist_ok=True)

    for nf in normalized_files:
        dest_filename = nf["filename"]
        dest_path = os.path.join(dest_dir, dest_filename)

        # Handle filename collisions
        dest_path = _resolve_collision(dest_path)
        dest_filename = os.path.basename(dest_path)

        # Write the normalized file
        with open(dest_path, "w") as f:
            f.write(nf["content"])

        # Register in dedup index
        register_hash(nf["content"], filepath, dest_path)

        # Log the action
        log_action(
            "ingested", filepath, dest_path,
            category=category, confidence=confidence,
            metadata=nf.get("metadata", {}),
            details=f"restructured={nf.get('was_restructured', False)}"
        )

        result["files_created"].append(dest_path)
        if verbose:
            print(f"  WRITE {dest_filename} -> {classification['destination']}/")

    # Archive original and remove from inbox
    archive_path = archive_original(filepath)
    if verbose:
        print(f"  ARCHIVE {basename} -> .audit/processed/")

    # Remove from inbox (safe since we archived)
    if os.path.dirname(os.path.abspath(filepath)) == os.path.abspath(INBOX_DIR):
        os.remove(filepath)
        if verbose:
            print(f"  REMOVE {basename} from inbox/")

    result["status"] = "processed"
    result["destination"] = classification["destination"]
    return result


def _resolve_collision(dest_path: str) -> str:
    """If dest_path already exists, append a counter."""
    if not os.path.exists(dest_path):
        return dest_path

    base, ext = os.path.splitext(dest_path)
    counter = 2
    while os.path.exists(f"{base}-{counter}{ext}"):
        counter += 1
    return f"{base}-{counter}{ext}"


def process_inbox(dry_run: bool = False, verbose: bool = False,
                  force: bool = False) -> list:
    """Process all files in memory/inbox/.

    Returns:
        List of result dicts from process_file().
    """
    if not os.path.isdir(INBOX_DIR):
        print("No inbox directory found. Creating memory/inbox/")
        os.makedirs(INBOX_DIR, exist_ok=True)
        return []

    files = []
    for f in sorted(os.listdir(INBOX_DIR)):
        fpath = os.path.join(INBOX_DIR, f)
        if os.path.isfile(fpath) and f not in SKIP_FILES and not f.startswith("."):
            files.append(fpath)

    if not files:
        print("Inbox is empty. Drop files into memory/inbox/ and run again.")
        return []

    print(f"Processing {len(files)} file(s) from inbox...")
    if dry_run:
        print("(DRY RUN - no files will be moved)\n")
    else:
        print()

    results = []
    for filepath in files:
        basename = os.path.basename(filepath)
        print(f"[{len(results)+1}/{len(files)}] {basename}")
        result = process_file(filepath, dry_run=dry_run, verbose=verbose, force=force)
        results.append(result)
        print()

    # Summary
    _print_summary(results)
    return results


def process_path(filepath: str, dry_run: bool = False, verbose: bool = False,
                 force: bool = False) -> list:
    """Process a specific file or directory.

    Args:
        filepath: Path to a file or directory.

    Returns:
        List of result dicts.
    """
    if os.path.isdir(filepath):
        files = []
        for f in sorted(os.listdir(filepath)):
            fpath = os.path.join(filepath, f)
            if os.path.isfile(fpath) and f not in SKIP_FILES and not f.startswith("."):
                files.append(fpath)
    else:
        files = [filepath]

    print(f"Processing {len(files)} file(s)...")
    if dry_run:
        print("(DRY RUN - no files will be moved)\n")
    else:
        print()

    results = []
    for fpath in files:
        basename = os.path.basename(fpath)
        print(f"[{len(results)+1}/{len(files)}] {basename}")
        result = process_file(fpath, dry_run=dry_run, verbose=verbose, force=force)
        results.append(result)
        print()

    _print_summary(results)
    return results


def validate_memory(verbose: bool = False) -> list:
    """Validate that existing memory files are in the correct directories.

    Scans all files in memory/ subdirectories and checks if they'd be
    classified into the directory they're currently in. Reports mismatches.

    Returns:
        List of mismatch dicts.
    """
    print("Validating memory files...\n")
    mismatches = []

    dirs_to_check = {
        "call-notes": "call_note",
        "wins": "win",
        "losses": "loss",
        "competitors": "competitor",
        "market-intel": "market_intel",
    }

    for subdir, expected_category in dirs_to_check.items():
        dir_path = os.path.join(MEMORY_ROOT, subdir)
        if not os.path.isdir(dir_path):
            continue

        for f in sorted(os.listdir(dir_path)):
            if f in SKIP_FILES or f.startswith(".") or f.startswith("_"):
                continue
            fpath = os.path.join(dir_path, f)
            if not os.path.isfile(fpath):
                continue

            classification = classify_file(fpath)
            actual = classification["category"]

            if actual != expected_category and actual != "unknown":
                mismatches.append({
                    "file": f,
                    "path": fpath,
                    "current_dir": subdir,
                    "expected_category": expected_category,
                    "detected_category": actual,
                    "confidence": classification["confidence"],
                })
                print(f"  MISMATCH {subdir}/{f}")
                print(f"    Expected: {expected_category}, Detected: {actual} "
                      f"(confidence: {classification['confidence']:.0%})")
            elif verbose:
                print(f"  OK {subdir}/{f}")

    if not mismatches:
        print("All files are in the correct directories.")
    else:
        print(f"\n{len(mismatches)} file(s) may be misplaced.")

    return mismatches


def show_stats():
    """Print audit statistics."""
    stats = get_stats()
    print("Memory Layer Statistics")
    print("=" * 40)
    print(f"Total files processed: {stats['total_processed']}")
    if stats.get("last_ingest"):
        print(f"Last ingest: {stats['last_ingest']}")

    if stats.get("by_action"):
        print("\nBy action:")
        for action, count in sorted(stats["by_action"].items()):
            print(f"  {action}: {count}")

    if stats.get("by_category"):
        print("\nBy category:")
        for cat, count in sorted(stats["by_category"].items()):
            print(f"  {cat}: {count}")

    # Count files in each memory directory
    print("\nFiles in memory/:")
    for subdir in ["call-notes", "wins", "losses", "competitors", "market-intel", "context"]:
        dir_path = os.path.join(MEMORY_ROOT, subdir)
        if os.path.isdir(dir_path):
            count = sum(1 for f in os.listdir(dir_path)
                        if not f.startswith("_") and not f.startswith(".")
                        and os.path.isfile(os.path.join(dir_path, f)))
            print(f"  {subdir}/: {count}")

    # Count inbox
    inbox_count = sum(1 for f in os.listdir(INBOX_DIR)
                      if f not in SKIP_FILES and not f.startswith(".")
                      and os.path.isfile(os.path.join(INBOX_DIR, f)))
    if inbox_count:
        print(f"  inbox/ (pending): {inbox_count}")


def show_recent(limit: int = 10):
    """Print recent audit log entries."""
    entries = get_log(limit=limit)
    if not entries:
        print("No audit log entries yet.")
        return

    print(f"Last {min(limit, len(entries))} ingest actions:")
    print("-" * 60)
    for entry in entries:
        ts = entry["timestamp"][:19]
        action = entry["action"].upper()
        source = entry["source_file"]
        dest = entry.get("dest_file", "")
        cat = entry.get("category", "")
        print(f"  {ts} {action:12s} {source}")
        if dest:
            print(f"{'':33s} -> {cat}/{dest}")


def _print_summary(results: list):
    """Print a summary of processing results."""
    print("=" * 40)
    print("Summary:")

    by_status = {}
    for r in results:
        s = r["status"]
        by_status[s] = by_status.get(s, 0) + 1

    for status, count in sorted(by_status.items()):
        label = {
            "processed": "Processed",
            "skipped": "Skipped",
            "duplicate": "Duplicate (already exists)",
            "unclassified": "Unclassified (left in inbox)",
            "error": "Errors",
            "dry_run": "Would process",
        }.get(status, status)
        print(f"  {label}: {count}")

    total_created = sum(len(r.get("files_created", [])) for r in results)
    if total_created:
        print(f"  Total files created: {total_created}")


# ─── CLI ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Memory Layer Ingest Pipeline - Auto-sort files into the BDR second brain.",
        epilog="Drop files in memory/inbox/ and run without arguments to process them.",
    )
    parser.add_argument("path", nargs="?", default=None,
                        help="Specific file or directory to process (default: memory/inbox/)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Classify files without moving them")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed processing output")
    parser.add_argument("--force", action="store_true",
                        help="Skip dedup check and process anyway")
    parser.add_argument("--validate", action="store_true",
                        help="Validate existing memory files are in the right place")
    parser.add_argument("--stats", action="store_true",
                        help="Show processing statistics")
    parser.add_argument("--recent", type=int, nargs="?", const=10,
                        help="Show recent audit log entries (default: 10)")

    args = parser.parse_args()

    if args.stats:
        show_stats()
        return

    if args.recent is not None:
        show_recent(args.recent)
        return

    if args.validate:
        validate_memory(verbose=args.verbose)
        return

    if args.path:
        process_path(args.path, dry_run=args.dry_run, verbose=args.verbose,
                     force=args.force)
    else:
        process_inbox(dry_run=args.dry_run, verbose=args.verbose, force=args.force)


if __name__ == "__main__":
    main()
