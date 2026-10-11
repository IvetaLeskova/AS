"""Isolated SQLite test database with reliable Windows cleanup."""
import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Configure the database BEFORE importing app.main (it imports the engine).
_test_dir = tempfile.TemporaryDirectory(prefix="as_test_")
_database_file = Path(_test_dir.name) / "tasks.db"
os.environ["TASK_DB_URL"] = "sqlite:///" + _database_file.as_posix()
os.environ.pop("TASK_BACKEND", None)

from app.main import app  # noqa: E402
from app.database import Base, engine  # noqa: E402


@pytest.fixture
def client():
    # Each test starts with fresh data; API behavior stays unchanged.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client


def pytest_sessionfinish(session, exitstatus):
    # SQLite files cannot be deleted on Windows while the engine has
    # an open connection; dispose of pooled connections before cleanup.
    engine.dispose()
    _test_dir.cleanup()
