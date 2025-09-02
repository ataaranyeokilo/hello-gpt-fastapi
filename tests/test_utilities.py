import pytest
import requests
import azure_client


def test_ask_llm_success(monkeypatch):
    """ask_llm should return text when API responds with choices."""

    class DummyResponse:
        def raise_for_status(self): return None
        def json(self):
            return {"choices": [{"message": {"content": "mocked reply"}}]}

    def fake_post(url, headers, json):  # mimic requests.post
        return DummyResponse()

    monkeypatch.setattr(requests, "post", fake_post)

    result = azure_client.ask_llm("Hello")
    assert result == "mocked reply"


def test_ask_llm_failure(monkeypatch):
    """ask_llm should raise when API errors out."""

    class DummyResponse:
        def raise_for_status(self): raise requests.HTTPError("boom")

    def fake_post(url, headers, json):
        return DummyResponse()

    monkeypatch.setattr(requests, "post", fake_post)

    with pytest.raises(requests.HTTPError):
        azure_client.ask_llm("Hello")
