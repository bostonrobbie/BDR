"""
Shared pytest fixtures for OCC test suite.
"""

import os
import pytest
import tempfile

from src.db.init_db import init_db
from src.db.migrate_v2 import run_migration as run_v2_migration
from src.db.migrate_v3 import run_migration as run_v3_migration


@pytest.fixture
def test_db(tmp_path):
    """Create a fresh test database with all migrations applied."""
    db_path = str(tmp_path / "test.db")
    os.environ["OCC_DB_PATH"] = db_path
    os.environ["OCC_JOURNAL_MODE"] = "DELETE"

    # Reload models module to pick up new DB_PATH
    import src.db.models as models
    models.DB_PATH = db_path

    init_db(db_path)
    run_v2_migration(db_path)
    run_v3_migration(db_path)

    yield db_path

    os.environ.pop("OCC_DB_PATH", None)
    os.environ.pop("OCC_JOURNAL_MODE", None)


@pytest.fixture
def sample_account(test_db):
    """Create a sample account for testing."""
    import src.db.models as models
    return models.create_account({
        "name": "Test Corp",
        "domain": "testcorp.com",
        "industry": "SaaS",
        "employee_count": 500,
    })


@pytest.fixture
def sample_contact(test_db, sample_account):
    """Create a sample contact for testing."""
    import src.db.models as models
    return models.create_contact({
        "account_id": sample_account["id"],
        "first_name": "Jane",
        "last_name": "Doe",
        "title": "QA Manager",
        "email": "jane@testcorp.com",
        "persona_type": "qa_leader",
    })
