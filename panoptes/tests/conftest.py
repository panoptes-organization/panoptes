"""Shared pytest fixtures for the panoptes test suite.

Must set ``PANOPTES_DB_URL`` *before* anything imports :mod:`panoptes`, since
``panoptes.database`` reads the env var at module-import time and binds an
engine to it.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

_TMP_DIR = Path(tempfile.mkdtemp(prefix="panoptes-tests-"))
_DB_PATH = _TMP_DIR / "test.db"
# PANOPTES_TEST_DB_URL lets the same suite run against another database (CI
# runs it against a PostgreSQL service container, see #203); by default the
# tests use an isolated throwaway SQLite file.
os.environ["PANOPTES_DB_URL"] = (
    os.environ.get("PANOPTES_TEST_DB_URL")
    or f"sqlite:///{_DB_PATH}?check_same_thread=False"
)

# Imports must come after the env var is set.
from panoptes.app import app as flask_app  # noqa: E402
from panoptes.database import Base, db_session, engine  # noqa: E402


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "e2e: end-to-end test that runs real Snakemake against a live panoptes server",
    )


@pytest.fixture
def client():
    """Flask test client backed by an isolated, freshly-truncated SQLite DB."""
    # Make sure the schema exists, then clear every table so each test starts
    # from a clean slate without paying for a full create/drop cycle.
    Base.metadata.create_all(bind=engine)
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()

    flask_app.config["TESTING"] = True
    with flask_app.test_client() as test_client:
        yield test_client
