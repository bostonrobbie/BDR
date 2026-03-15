"""
Memory Inbox File Watcher - Monitors memory/inbox/ for new files.

Runs as a background thread or standalone process. When new files appear,
automatically runs the ingest pipeline to classify, normalize, and sort them.

Usage:
    # As standalone process
    python -m src.memory.watcher

    # As background thread (from app startup)
    from src.memory.watcher import start_watcher
    stop_event = start_watcher()
    # ... later ...
    stop_event.set()  # stops the watcher
"""

import logging
import os
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

logger = logging.getLogger("bdr.memory.watcher")

MEMORY_ROOT = os.path.join(os.path.dirname(__file__), "../../memory")
INBOX_DIR = os.path.join(MEMORY_ROOT, "inbox")
SKIP_FILES = {"README.md", "_template.md", "_index.json", ".gitkeep", ".DS_Store"}

# Default poll interval in seconds
DEFAULT_POLL_INTERVAL = 5


def _get_inbox_files() -> dict:
    """Get current inbox files with their modification times."""
    files = {}
    if not os.path.isdir(INBOX_DIR):
        return files
    for f in os.listdir(INBOX_DIR):
        if f in SKIP_FILES or f.startswith("."):
            continue
        fpath = os.path.join(INBOX_DIR, f)
        if os.path.isfile(fpath):
            files[fpath] = os.path.getmtime(fpath)
    return files


def _process_new_files(new_files: list):
    """Process new files through the ingest pipeline."""
    from src.memory.ingest import process_file

    for fpath in new_files:
        basename = os.path.basename(fpath)
        logger.info("Auto-processing: %s", basename)
        try:
            result = process_file(fpath, verbose=False)
            status = result.get("status", "unknown")
            if status == "processed":
                dest = result.get("destination", "unknown")
                created = len(result.get("files_created", []))
                logger.info("Ingested %s -> %s/ (%d file(s))", basename, dest, created)
            elif status == "duplicate":
                logger.info("Skipped %s (duplicate)", basename)
            elif status == "unclassified":
                logger.info("Left %s in inbox (unclassified)", basename)
            else:
                logger.info("Result for %s: %s", basename, status)
        except Exception as e:
            logger.error("Failed to process %s: %s", basename, e)


def watch_inbox(poll_interval: float = DEFAULT_POLL_INTERVAL,
                stop_event: threading.Event = None):
    """Poll the inbox directory for new files and process them.

    Args:
        poll_interval: Seconds between checks.
        stop_event: Threading event to signal stop.
    """
    stop_event = stop_event or threading.Event()
    known_files = _get_inbox_files()
    logger.info("Watching %s (poll every %ds)", INBOX_DIR, poll_interval)

    while not stop_event.is_set():
        stop_event.wait(poll_interval)
        if stop_event.is_set():
            break

        current_files = _get_inbox_files()
        new_files = []

        for fpath, mtime in current_files.items():
            if fpath not in known_files:
                new_files.append(fpath)
            elif mtime > known_files.get(fpath, 0):
                new_files.append(fpath)

        if new_files:
            logger.info("Detected %d new/modified file(s) in inbox", len(new_files))
            _process_new_files(new_files)

        known_files = _get_inbox_files()

    logger.info("Watcher stopped")


def start_watcher(poll_interval: float = DEFAULT_POLL_INTERVAL) -> threading.Event:
    """Start the inbox watcher as a background daemon thread.

    Returns a stop_event that can be set to stop the watcher.
    """
    os.makedirs(INBOX_DIR, exist_ok=True)
    stop_event = threading.Event()
    thread = threading.Thread(
        target=watch_inbox,
        args=(poll_interval, stop_event),
        daemon=True,
        name="inbox-watcher",
    )
    thread.start()
    logger.info("Inbox watcher started (background thread)")
    return stop_event


# ─── CLI ─────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Watch memory/inbox/ for new files.")
    parser.add_argument("--interval", type=float, default=DEFAULT_POLL_INTERVAL,
                        help=f"Poll interval in seconds (default: {DEFAULT_POLL_INTERVAL})")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    print(f"Watching memory/inbox/ (poll every {args.interval}s, Ctrl+C to stop)")
    try:
        watch_inbox(poll_interval=args.interval)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
