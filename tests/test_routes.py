
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_homepage_loads():
    response = client.get("/")

    assert response.status_code == 200
    assert "TruthLens" in response.text
    assert "Analyze content" in response.text


def test_system_status_page_loads():
    response = client.get("/status")

    assert response.status_code == 200
    assert "System Status" in response.text
    assert "/health" in response.text


def test_health_endpoint_returns_json():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["application"] == "TruthLens AI"
    assert data["mode"] in {"demo", "ai"}


def test_api_documentation_is_available():
    response = client.get("/docs")

    assert response.status_code == 200
    assert "swagger" in response.text.lower()


def test_unknown_route_returns_404():
    response = client.get("/this-page-does-not-exist")

    assert response.status_code == 404

