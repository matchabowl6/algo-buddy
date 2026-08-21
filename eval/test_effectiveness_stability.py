"""Back-to-back effectiveness scores must differ by no more than 0.005."""
import pytest
from api.app import app

HISTORY = [
    {"role": "user",      "content": "explain time complexity"},
    {"role": "assistant", "content": "Bubble sort has O(n^2) time complexity in the worst case."},
    {"role": "user",      "content": "explain space complexity"},
    {"role": "assistant", "content": "Bubble sort uses O(1) extra space — it sorts in place."},
]
TOPICS = ["time complexity", "space complexity"]
QUESTIONS = [
    {"type": "short_response", "question": "What is the worst-case time complexity?", "answer": "O(n^2)", "topic": "time complexity"},
    {"type": "short_response", "question": "What is the best-case time complexity?",  "answer": "O(n)",   "topic": "time complexity"},
    {"type": "short_response", "question": "How much extra space does bubble sort use?", "answer": "O(1)", "topic": "space complexity"},
    {"type": "short_response", "question": "Is bubble sort in-place?", "answer": "Yes", "topic": "space complexity"},
]


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def _get_effectiveness(client):
    res = client.post("/api/study/effectiveness", json={
        "history": HISTORY,
        "questions": QUESTIONS,
        "topics": TOPICS,
    })
    return res.get_json()["effectiveness"]


def test_back_to_back_effectiveness_stability(client):
    score1 = _get_effectiveness(client)
    score2 = _get_effectiveness(client)
    assert abs(score1 - score2) <= 0.005, (
        f"Effectiveness scores differ by more than 0.005: {score1} vs {score2}"
    )
