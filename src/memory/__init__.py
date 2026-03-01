# Memory Layer - BDR Second Brain
# Provides structured access to competitor intel, win/loss data, call notes, and market context.
#
# Key modules:
#   loader.py     - Read API for agents (battle cards, objection responses, prospect context)
#   classifier.py - Auto-classifies raw files into memory categories
#   normalizer.py - Transforms raw content into structured template format
#   audit.py      - Tracks every file processed, dedup checking, archive
#   ingest.py     - CLI pipeline that ties everything together
