from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_ask_endpoint_missing_body():
    r = client.post("/ask", json={})
    assert r.status_code == 422

def test_ask_endpoint_with_mock(monkeypatch):
    # Mock azure_client.ask_gpt so no real API call happens
    def fake_ask_gpt(question: str) -> str:
        return "mocked response"

    import azure_client
    monkeypatch.setattr(azure_client, "ask_gpt", fake_ask_gpt)

    r = client.post("/ask", json={"question": "Hello"})
    assert r.status_code == 200
    body = r.json()
    assert body["answer"] == "mocked response"
