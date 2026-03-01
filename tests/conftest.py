"""Shared test fixtures and configuration."""

import os
import sys
import tempfile

import pytest

# Ensure project root is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def tmp_db(tmp_path):
    """Provide a temporary database path for tests."""
    db_path = str(tmp_path / "test.db")
    os.environ["OCC_DB_PATH"] = db_path
    yield db_path
    os.environ.pop("OCC_DB_PATH", None)


@pytest.fixture
def tmp_memory(tmp_path):
    """Provide a temporary memory directory structure for tests."""
    memory_root = tmp_path / "memory"
    for subdir in ["inbox", "competitors", "wins", "losses",
                   "call-notes", "market-intel", "context"]:
        (memory_root / subdir).mkdir(parents=True)

    # Create .audit dirs
    audit = memory_root / ".audit"
    audit.mkdir()
    (audit / "processed").mkdir()

    yield str(memory_root)
