
import json
import pytest

from backend.services.ai_service import classify_ticket


class MockResponse:

    def __init__(self, content):
        self.content = content

    def raise_for_status(self):
        pass

    def json(self):
        return {
            "message": {
                "content": self.content
            }
        }


def mock_ollama(monkeypatch, ai_result):

    def fake_post(*args, **kwargs):
        return MockResponse(json.dumps(ai_result))

    monkeypatch.setattr(
        "backend.services.ai_service.httpx.post",
        fake_post,
    )


def test_valid_ai_classification(monkeypatch):

    mock_ollama(
        monkeypatch,
        {
            "category": "Payment",
            "priority": "High",
            "recommended_action": "Escalate to Support",
            "reason": "Payment was deducted but order was not confirmed."
        },
    )

    result = classify_ticket(
        "Payment deducted but order not confirmed."
    )

    assert result["category"] == "Payment"
    assert result["priority"] == "High"
    assert result["recommended_action"] == "Escalate to Support"
    assert result["reason"]


def test_invalid_category(monkeypatch):

    mock_ollama(
        monkeypatch,
        {
            "category": "Urgent",
            "priority": "High",
            "recommended_action": "Escalate to Support",
            "reason": "Test explanation."
        },
    )

    with pytest.raises(ValueError):
        classify_ticket("Test complaint")


def test_invalid_priority(monkeypatch):

    mock_ollama(
        monkeypatch,
        {
            "category": "Payment",
            "priority": "Critical",
            "recommended_action": "Escalate to Support",
            "reason": "Test explanation."
        },
    )

    with pytest.raises(ValueError):
        classify_ticket("Test complaint")


def test_invalid_recommended_action(monkeypatch):

    mock_ollama(
        monkeypatch,
        {
            "category": "Payment",
            "priority": "High",
            "recommended_action": "Issue Free Money",
            "reason": "Test explanation."
        },
    )

    with pytest.raises(ValueError):
        classify_ticket("Test complaint")


def test_missing_recommended_action(monkeypatch):

    mock_ollama(
        monkeypatch,
        {
            "category": "Payment",
            "priority": "High",
            "reason": "Test explanation."
        },
    )

    with pytest.raises(ValueError):
        classify_ticket("Test complaint")


def test_missing_reason(monkeypatch):

    mock_ollama(
        monkeypatch,
        {
            "category": "Payment",
            "priority": "High",
            "recommended_action": "Escalate to Support",
            "reason": ""
        },
    )

    with pytest.raises(ValueError):
        classify_ticket("Test complaint")


def test_empty_complaint():

    with pytest.raises(ValueError):
        classify_ticket("   ")
