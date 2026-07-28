import pytest
from fastapi.testclient import TestClient
from main import app, reset_users


@pytest.fixture()
def client() -> TestClient:
    reset_users()
    return TestClient(app)


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_users(client: TestClient) -> None:
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Alice", "role": "frontend"}]


def test_create_user(client: TestClient) -> None:
    response = client.post("/users", json={"name": "Bob", "role": "backend"})

    assert response.status_code == 200
    assert response.json() == {"id": 2, "name": "Bob", "role": "backend"}


def test_get_missing_user_returns_404(client: TestClient) -> None:
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_user_with_invalid_payload_returns_422(client: TestClient) -> None:
    response = client.post("/users", json={"name": "", "role": "backend"})

    assert response.status_code == 422
