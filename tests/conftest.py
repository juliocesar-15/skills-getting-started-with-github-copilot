import importlib

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    # Reload the app module before each test to restore initial in-memory state
    importlib.reload(app_module)
    yield
