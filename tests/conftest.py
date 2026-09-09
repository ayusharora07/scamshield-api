import sys
from unittest.mock import MagicMock

# Prevent network calls from whisper model initialization during local execution
sys.modules["whisper"] = MagicMock()

import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Reusable FastAPI TestClient fixture."""
    with TestClient(app) as test_client:
        yield test_client
