from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    """Check that /health responds correctly."""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_ask_endpoint_missing_body():
    """POST /ask without question should return 422."""
    r = client.post("/ask", json={})
    assert r.status_code == 422


def test_ask_endpoint_with_mock(monkeypatch):
    """POST /ask with question, mock Azure call to avoid hitting real API."""
    # fake azure_client.ask_llm to always return "mocked response"
    def fake_ask_llm(question: str):
        return "mocked response"

    import azure_client
    monkeypatch.setattr(azure_client, "ask_llm", fake_ask_llm)

    r = client.post("/ask", json={"question": "Hello"})
    assert r.status_code == 200
    body = r.json()
    assert "mocked response" in body["answer"]
