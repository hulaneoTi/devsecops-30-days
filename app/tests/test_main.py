import pytest

from app.main import ITEMS, app


@pytest.fixture
def client():
    ITEMS.clear()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_security_headers(client):
    r = client.get("/health")
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["X-Frame-Options"] == "DENY"
    assert "Content-Security-Policy" in r.headers


def test_create_and_list_items(client):
    r = client.post("/items", json={"name": "jump-server"})
    assert r.status_code == 201
    assert client.get("/items").get_json() == {"items": [{"id": 1, "name": "jump-server"}]}


def test_rejects_invalid_item(client):
    assert client.post("/items", json={}).status_code == 400
    assert client.post("/items", json={"name": "x" * 101}).status_code == 400
