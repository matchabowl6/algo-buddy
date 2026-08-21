"""Effectiveness > 1.0 must not be hidden — the raw value must be returned as-is."""
import pytest
from api.app import app

# Craft a scenario where correctly_classified > total_questions is impossible via the
# formula, but we can verify the server does not clamp the value by injecting a
# mock that returns a score > 1 and checking it passes through unchanged.
# Since we cannot call the LLM, we test the arithmetic in the route directly by
# monkey-patching chat_json to return a controlled result.

from unittest.mock import patch


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_effectiveness_above_1_not_clamped(client):
    # 4 correctly_classified, 0 off_topic, 2 total questions → effectiveness = 4/2 = 2.0
    mock_result = {
        "questions": [
            {"on_topic": True, "correctly_classified": True},
            {"on_topic": True, "correctly_classified": True},
            {"on_topic": True, "correctly_classified": True},
            {"on_topic": True, "correctly_classified": True},
        ]
    }
    with patch("app.chat_json", return_value=mock_result):
        res = client.post("/api/study/effectiveness", json={
            "history": [{"role": "user", "content": "x"}],
            "questions": [
                {"question": "Q1", "topic": "t"},
                {"question": "Q2", "topic": "t"},
            ],
            "topics": ["t"],
        })
    effectiveness = res.get_json()["effectiveness"]
    assert effectiveness > 1.0, f"Expected effectiveness > 1.0 but got {effectiveness}"
