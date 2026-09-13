from fastapi.testclient import TestClient

from app.main import app


def test_missing_api_key():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict",
            json={
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        )

    assert response.status_code == 401


def test_invalid_api_key():
    with TestClient(app) as client:
        client.headers.update({
            "X-API-Key": "wrong-key"
        })

        response = client.post(
            "/api/v1/predict",
            json={
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        )

    assert response.status_code == 401


def test_unexpected_extra_field(client):
    response = client.post(
        "/api/v1/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
            "unexpected_field": "test"
        }
    )

    assert response.status_code == 422