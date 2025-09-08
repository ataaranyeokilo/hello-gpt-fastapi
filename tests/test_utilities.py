# tests/test_utilities.py
import types
import pytest
import azure_client

# --- happy path: no network, fully mocked ---
class FakeCompletions:
    def create(self, **kwargs):
        return types.SimpleNamespace(
            choices=[types.SimpleNamespace(message=types.SimpleNamespace(content="mocked reply"))]
        )

class FakeClient:
    chat = types.SimpleNamespace(completions=FakeCompletions())

def test_ask_gpt_success(monkeypatch):
    # swap the real SDK client for our fake
    monkeypatch.setattr(azure_client, "get_client", lambda: FakeClient())
    assert azure_client.ask_gpt("Hello") == "mocked reply"

# --- failure path: ensure we surface RuntimeError cleanly ---
class BoomCompletions:
    def create(self, **kwargs):
        raise Exception("boom")  # triggers our catch-all → RuntimeError

class BoomClient:
    chat = types.SimpleNamespace(completions=BoomCompletions())

def test_ask_gpt_failure(monkeypatch):
    monkeypatch.setattr(azure_client, "get_client", lambda: BoomClient())
    with pytest.raises(RuntimeError):
        azure_client.ask_gpt("Hello")
