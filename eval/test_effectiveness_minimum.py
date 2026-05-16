"""Effectiveness score must be at least 0.8."""
import pytest
from app import app

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


def test_effectiveness_at_least_0_8(client):
    res = client.post("/study/effectiveness", json={
        "history": HISTORY,
        "questions": QUESTIONS,
        "topics": TOPICS,
    })
    effectiveness = res.get_json()["effectiveness"]
    assert effectiveness >= 0.8, f"Effectiveness {effectiveness} is below 0.8"
