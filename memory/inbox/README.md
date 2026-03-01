# Inbox - Drop Zone

Drop any raw file here and run `python -m src.memory.ingest` to auto-process it.

## Supported file types
- `.md` / `.txt` - Call notes, win/loss reports, market intel, competitor updates
- `.csv` - Bulk data (call logs, CRM exports, prospect lists)
- `.json` - Structured data (API exports, enrichment dumps)

## What happens when you process
1. Each file is classified (call note, win, loss, competitor intel, market intel, or unknown)
2. Classified files are parsed into the structured template format
3. Parsed files are moved to the correct `memory/` subdirectory
4. A dedup check prevents duplicate entries
5. Every action is logged in `memory/.audit/log.jsonl`
6. Original files are archived to `memory/.audit/processed/` (never deleted)

## Quick start
```bash
# Drop files in this directory, then:
python -m src.memory.ingest

# Or process a specific file:
python -m src.memory.ingest path/to/file.md

# Dry run (classify without moving):
python -m src.memory.ingest --dry-run

# Process and show verbose log:
python -m src.memory.ingest --verbose
```
