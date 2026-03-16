#!/bin/bash
# Backup the OCC SQLite database with timestamp
# Usage: ./scripts/backup_db.sh [db_path]

DB_PATH="${1:-outreach.db}"
BACKUP_DIR="backups"

if [ ! -f "$DB_PATH" ]; then
    echo "Error: Database file not found at $DB_PATH"
    exit 1
fi

mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="$BACKUP_DIR/outreach-$TIMESTAMP.db"

# Use SQLite backup command for consistency (handles WAL mode)
sqlite3 "$DB_PATH" ".backup '$BACKUP_FILE'"

if [ $? -eq 0 ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "Backup created: $BACKUP_FILE ($SIZE)"

    # Keep only last 10 backups
    ls -t "$BACKUP_DIR"/outreach-*.db 2>/dev/null | tail -n +11 | xargs -r rm
    echo "Retained $(ls "$BACKUP_DIR"/outreach-*.db 2>/dev/null | wc -l) backups"
else
    echo "Error: Backup failed"
    exit 1
fi
