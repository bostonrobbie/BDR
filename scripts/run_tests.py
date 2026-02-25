#!/usr/bin/env python3
"""
Unified test runner for the BDR Outreach Command Center.

Runs all test suites, reports results, and exits with non-zero on failure.

Usage:
    python scripts/run_tests.py              # Run all tests
    python scripts/run_tests.py researcher   # Run only researcher tests
    python scripts/run_tests.py scorer       # Run only scorer tests
    python scripts/run_tests.py messages     # Run only message writer tests
    python scripts/run_tests.py feedback     # Run only feedback tests
    python scripts/run_tests.py quality      # Run only quality gate tests
"""

import subprocess
import sys
import os
import time

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")

# Test suites organized by module (consolidated layout)
TEST_SUITES = {
    "researcher": [
        "tests/unit/test_research_artifact.py",
    ],
    "scorer": [
        "tests/unit/test_scorer.py",
    ],
    "messages": [
        "tests/unit/test_message_writer.py",
        "tests/unit/test_channels.py",
    ],
    "feedback": [
        "tests/unit/test_feedback.py",
        "tests/unit/test_wiring_enhancements.py",
        "tests/unit/test_intelligence_enhancements.py",
    ],
    "quality": [
        "tests/unit/test_quality_gate.py",
    ],
    "sequences": [
        "tests/unit/test_sequence_generator.py",
    ],
    "other": [
        "tests/unit/test_signal_enrichment.py",
        "tests/unit/test_llm_polish.py",
    ],
}


def run_suite(path):
    """Run a single test file and return (passed, output)."""
    full = os.path.join(PROJECT_ROOT, path)
    if not os.path.exists(full):
        return False, f"  SKIP: {path} (file not found)"
    try:
        result = subprocess.run(
            [sys.executable, full],
            capture_output=True, text=True, timeout=120,
            cwd=PROJECT_ROOT,
        )
        last_line = result.stdout.strip().split("\n")[-1] if result.stdout.strip() else ""
        if result.returncode == 0:
            return True, f"  PASS: {path} -- {last_line}"
        else:
            error = result.stderr.strip().split("\n")[-1] if result.stderr.strip() else "unknown error"
            return False, f"  FAIL: {path} -- {error}"
    except subprocess.TimeoutExpired:
        return False, f"  TIMEOUT: {path}"


def main():
    groups = list(TEST_SUITES.keys())

    # Filter to specific group if requested
    if len(sys.argv) > 1:
        requested = sys.argv[1].lower()
        if requested in TEST_SUITES:
            groups = [requested]
        else:
            print(f"Unknown group '{requested}'. Available: {', '.join(TEST_SUITES.keys())}")
            sys.exit(1)

    print("=" * 60)
    print("BDR TEST RUNNER")
    print("=" * 60)

    start = time.time()
    total_passed = 0
    total_failed = 0
    failures = []

    for group in groups:
        files = TEST_SUITES[group]
        print(f"\n--- {group.upper()} ---")
        for f in files:
            passed, msg = run_suite(f)
            print(msg)
            if passed:
                total_passed += 1
            else:
                total_failed += 1
                failures.append(f)

    elapsed = time.time() - start
    print(f"\n{'=' * 60}")
    print(f"RESULTS: {total_passed} passed, {total_failed} failed ({elapsed:.1f}s)")
    if failures:
        print(f"FAILURES:")
        for f in failures:
            print(f"  - {f}")
    print("=" * 60)

    sys.exit(1 if total_failed > 0 else 0)


if __name__ == "__main__":
    main()
