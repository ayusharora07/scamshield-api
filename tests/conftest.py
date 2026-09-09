import sys
from unittest.mock import MagicMock

# Prevent network calls from whisper model initialization during local execution
sys.modules["whisper"] = MagicMock()

from fastapi.testclient import TestClient
import fakeredis
import pytest

from app.main import app


@pytest.fixture
def client():
    """Reusable FastAPI TestClient fixture."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def mock_redis(mocker):
    fake_server = fakeredis.FakeStrictRedis()
    mocker.patch("app.services.rate_limit.r", fake_server)
