import os
import tempfile
os.environ["DATABASE_URL"] = "sqlite:///" + tempfile.mktemp(suffix=".db")
from fastapi.testclient import TestClient
from main import app


def test_mock_events_and_filters():
    with TestClient(app) as client:
        events = client.get("/api/events").json()
        assert len(events) >= 4
        assert all(e["source"] == "Mock adapter" for e in events)
        assert all(c["availability"] == "unknown" for e in events for c in e["categories"])
        assert len(client.get("/api/events?q=aurora").json()) == 1
        assert client.get("/api/events/99999").status_code == 404


def test_watchlist_persists_and_validates():
    with TestClient(app) as client:
        assert client.put("/api/events/1/watch", json={"watching": True}).json()["watching"]
        assert client.get("/api/events/1").json()["watching"]
        assert not client.put("/api/events/1/watch", json={"watching": False}).json()["watching"]
        assert client.put("/api/events/99999/watch", json={"watching": True}).status_code == 404
        assert client.put("/api/events/1/watch", json={}).status_code == 422


def test_health():
    with TestClient(app) as client:
        assert client.get("/api/health").json() == {"status": "ok", "mode": "mock"}
