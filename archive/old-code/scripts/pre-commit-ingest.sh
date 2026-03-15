#!/bin/bash
# Pre-commit hook: Auto-process memory/inbox/ files before commit.
#
# Install: cp scripts/pre-commit-ingest.sh .git/hooks/pre-commit
# Or:      ln -sf ../../scripts/pre-commit-ingest.sh .git/hooks/pre-commit
#
# What it does:
# 1. Checks if there are files in memory/inbox/
# 2. If yes, runs the ingest pipeline to classify, normalize, and sort them
# 3. Stages the newly created files so they're included in the commit
# 4. If anything fails, the commit proceeds anyway (non-blocking)

INBOX_DIR="memory/inbox"
MEMORY_DIR="memory"

# Count non-system files in inbox
inbox_files=$(find "$INBOX_DIR" -maxdepth 1 -type f \
    ! -name "README.md" ! -name ".gitkeep" ! -name ".DS_Store" ! -name ".*" \
    2>/dev/null | wc -l)

if [ "$inbox_files" -gt 0 ]; then
    echo "[memory-ingest] Found $inbox_files file(s) in inbox. Processing..."

    # Run the ingest pipeline
    if python -m src.memory.ingest --verbose 2>&1; then
        echo "[memory-ingest] Done. Staging new memory files..."

        # Stage any new/modified files in memory/
        git add "$MEMORY_DIR/" 2>/dev/null

        echo "[memory-ingest] Files staged for commit."
    else
        echo "[memory-ingest] Warning: ingest had errors, but commit will proceed."
    fi
fi

# Always let the commit proceed
exit 0
