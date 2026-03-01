"""
Memory Audit Log - Tracks every file processed by the ingest pipeline.

Every action is logged to memory/.audit/log.jsonl (append-only).
Original files are archived to memory/.audit/processed/ (never deleted).
Dedup checking prevents the same content from being stored twice.
"""

import hashlib
import json
import os
import shutil
from datetime import datetime
from typing import Optional


MEMORY_ROOT = os.path.join(os.path.dirname(__file__), "../../memory")
AUDIT_DIR = os.path.join(MEMORY_ROOT, ".audit")
LOG_FILE = os.path.join(AUDIT_DIR, "log.jsonl")
PROCESSED_DIR = os.path.join(AUDIT_DIR, "processed")
HASH_INDEX = os.path.join(AUDIT_DIR, "hash_index.json")


def _ensure_dirs():
    """Create audit directories if they don't exist."""
    os.makedirs(AUDIT_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)


def log_action(action: str, source_file: str, dest_file: str = "",
               category: str = "", confidence: float = 0.0,
               metadata: dict = None, details: str = "") -> dict:
    """Append an action to the audit log.

    Args:
        action: What happened (classified, normalized, moved, skipped, duplicate, error)
        source_file: Original file path
        dest_file: Destination file path (if moved)
        category: Classified category
        confidence: Classification confidence
        metadata: Extracted metadata dict
        details: Additional context

    Returns:
        The log entry dict.
    """
    _ensure_dirs()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "source_file": os.path.basename(source_file),
        "source_path": source_file,
        "dest_file": os.path.basename(dest_file) if dest_file else "",
        "dest_path": dest_file,
        "category": category,
        "confidence": confidence,
        "metadata": metadata or {},
        "details": details,
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return entry


def get_log(limit: int = 50, action_filter: str = None) -> list:
    """Read recent audit log entries.

    Args:
        limit: Max entries to return (most recent first).
        action_filter: Optional filter by action type.

    Returns:
        List of log entry dicts.
    """
    if not os.path.exists(LOG_FILE):
        return []

    entries = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entry = json.loads(line)
                    if action_filter is None or entry.get("action") == action_filter:
                        entries.append(entry)
                except json.JSONDecodeError:
                    continue

    # Most recent first, limited
    return entries[-limit:][::-1]


def archive_original(filepath: str) -> str:
    """Copy original file to the processed archive.

    Returns the archive path. Never deletes the original.
    """
    _ensure_dirs()

    basename = os.path.basename(filepath)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_name = f"{timestamp}_{basename}"
    archive_path = os.path.join(PROCESSED_DIR, archive_name)

    shutil.copy2(filepath, archive_path)
    return archive_path


# ─── DEDUP SYSTEM ────────────────────────────────────────────

def compute_content_hash(content: str) -> str:
    """Compute a stable hash of file content for dedup.

    Normalizes whitespace to avoid false negatives from formatting differences.
    """
    # Normalize: lowercase, collapse whitespace, strip
    normalized = " ".join(content.lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def _load_hash_index() -> dict:
    """Load the hash index from disk."""
    if not os.path.exists(HASH_INDEX):
        return {}
    try:
        with open(HASH_INDEX, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def _save_hash_index(index: dict):
    """Save the hash index to disk."""
    _ensure_dirs()
    with open(HASH_INDEX, "w") as f:
        json.dump(index, f, indent=2)


def is_duplicate(content: str) -> Optional[str]:
    """Check if content has already been ingested.

    Args:
        content: File content to check.

    Returns:
        Path to the existing file if duplicate, None if new.
    """
    content_hash = compute_content_hash(content)
    index = _load_hash_index()
    entry = index.get(content_hash)
    if entry:
        return entry.get("dest_path", entry.get("source_file", "unknown"))
    return None


def register_hash(content: str, source_file: str, dest_path: str):
    """Register a content hash in the dedup index.

    Args:
        content: The file content.
        source_file: Original file path.
        dest_path: Where it was stored.
    """
    content_hash = compute_content_hash(content)
    index = _load_hash_index()
    index[content_hash] = {
        "source_file": os.path.basename(source_file),
        "dest_path": dest_path,
        "ingested_at": datetime.now().isoformat(),
    }
    _save_hash_index(index)


def get_stats() -> dict:
    """Get audit statistics.

    Returns:
        Dict with counts by action, category, and date range.
    """
    entries = get_log(limit=10000)
    if not entries:
        return {"total_processed": 0, "by_action": {}, "by_category": {}}

    from collections import Counter
    actions = Counter(e["action"] for e in entries)
    categories = Counter(e["category"] for e in entries if e.get("category"))

    return {
        "total_processed": len(entries),
        "by_action": dict(actions),
        "by_category": dict(categories),
        "last_ingest": entries[0]["timestamp"] if entries else None,
    }
