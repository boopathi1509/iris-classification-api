import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.config import settings


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        test_client.headers.update({
            "X-API-Key": settings.API_KEY
        })
        yield test_client