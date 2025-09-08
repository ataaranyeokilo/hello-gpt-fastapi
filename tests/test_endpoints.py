from fastapi.testclient import TestClient
from main import app
import azure_client  # import at top for linting

client = TestClient(app)

def test_health_endpoint():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_ask_endpoint_missing_body():
    r = client.post("/ask", json={})
    assert r.status_code == 422

def test_ask_endpoint_with_mock(monkeypatch):
    monkeypatch.setattr(azure_client, "ask_gpt", lambda q: "mocked response")
    monkeypatch.setattr(azure_client, "ask_gpt", lambda q: "mocked response")
    r = client.post("/ask", json={"question": "Hello"})
    assert r.status_code == 200
    assert r.json()["answer"] == "mocked response"
