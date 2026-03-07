# Work Directory

This is the active working directory for daily Cowork sessions. Everything Claude needs to read and write during a session lives here.

## Structure

```
work/
├── reply-log.csv              # All replies tracked (the learning loop)
├── results.json               # Aggregated metrics across batches
├── batch-N-prospects.csv      # Prospect list for batch N (from /prospect)
├── batch-N-outreach.md        # Written touches for batch N (from /write-batch)
├── pre-brief-batch-N.md       # Pre-brief for batch N (from /pre-brief)
├── meeting-prep/              # Meeting prep cards (from /reply-handle)
│   └── meeting-prep-name.md
└── README.md                  # This file
```

## How to use

1. `/prospect` creates `batch-N-prospects.csv`
2. `/write-batch` reads prospects and creates `batch-N-outreach.md`
3. `/follow-up` checks what's due and drafts follow-ups
4. `/reply-handle` triages replies and updates `reply-log.csv`
5. `/pre-brief` reads all data and generates insights for next batch
6. `/score-message` QA-checks any message draft

## Reply log format

The `reply-log.csv` is the most important file in this directory. Every reply Rob gets should be logged here. This is what makes each batch smarter than the last.
