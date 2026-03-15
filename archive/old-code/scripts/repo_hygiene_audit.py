#!/usr/bin/env python3
"""Lightweight repo hygiene audit.

Scans the repository for likely stale/generated artifacts in top-level folders and
prints a markdown report with safe archive recommendations.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parents[1]
NOW = datetime.now(timezone.utc)

STALE_EXTENSIONS = {".bak", ".zip"}
STALE_NAME_PARTS = (
    "backup",
    "complete",
    "summary",
    "report",
    "ready",
    "deliverables",
    "analysis",
)
EXCLUDE_DIRS = {".git", ".venv", "__pycache__", "node_modules"}


@dataclass
class Finding:
    path: str
    reason: str
    age_days: int


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)


def age_days(path: Path) -> int:
    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return int((NOW - mtime).days)


def collect_findings() -> list[Finding]:
    findings: list[Finding] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file() or is_excluded(path):
            continue
        rel = path.relative_to(REPO_ROOT)

        # Prioritize top-level clutter and obvious generated artifacts.
        top_level = len(rel.parts) == 1
        stem = path.stem.lower()
        suffix = path.suffix.lower()
        age = age_days(path)

        if suffix in STALE_EXTENSIONS:
            findings.append(Finding(str(rel), f"extension={suffix}", age))
            continue

        if top_level and suffix in {".html", ".txt", ".docx", ".md"} and any(
            p in stem for p in STALE_NAME_PARTS
        ):
            findings.append(Finding(str(rel), "top-level artifact-like filename", age))

    findings.sort(key=lambda f: (f.reason, -f.age_days, f.path))
    return findings


def main() -> None:
    findings = collect_findings()
    print("# Repo Hygiene Audit")
    print()
    print(f"Generated: {NOW.isoformat()}")
    print()
    print("## Candidate files to archive (review before moving)")
    if not findings:
        print("- None detected by heuristic scan.")
        return
    for f in findings[:250]:
        print(f"- `{f.path}` — {f.reason}, ~{f.age_days} days old")


if __name__ == "__main__":
    main()
