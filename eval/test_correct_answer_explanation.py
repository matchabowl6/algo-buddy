"""correct_explanation must be present and between 25 and 250 characters for every result."""
import pytest
from app import app

QUESTIONS = [
    {"type": "short_response", "question": "What is the time complexity of bubble sort?", "answer": "O(n^2)"},
    {"type": "multiple_choice", "question": "Which is true about bubble sort?",
     "options": ["O(n^2) worst case", "O(1) space always", "Not stable", "Recursive only"],
     "answer": "O(n^2) worst case"},
]
# All answers correct so every result is a "correct" result
ANSWERS = {"0": "O(n^2)", "1": "O(n^2) worst case"}


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_correct_explanation_length(client):
    res = client.post("/quiz/grade", json={
        "algorithm": "bubble sort",
        "questions": QUESTIONS,
        "answers": ANSWERS,
    })
    results = res.get_json()["results"]
    for r in results:
        explanation = r.get("correct_explanation", "")
        assert len(explanation) >= 25, f"correct_explanation too short: {explanation!r}"
        assert len(explanation) <= 250, f"correct_explanation too long: {explanation!r}"
