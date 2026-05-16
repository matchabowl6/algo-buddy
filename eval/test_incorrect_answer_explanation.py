"""For incorrect answers, incorrect_explanation must be 30–500 chars."""
import pytest
from app import app

QUESTIONS = [
    {"type": "short_response", "question": "What is the time complexity of bubble sort?", "answer": "O(n^2)"},
    {"type": "multiple_choice", "question": "Which is true about bubble sort?",
     "options": ["O(n^2) worst case", "O(n log n) worst case", "Not stable", "Recursive only"],
     "answer": "O(n^2) worst case"},
]
# Both answers are wrong
ANSWERS = {"0": "O(n)", "1": "O(n log n) worst case"}


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_incorrect_explanation_length(client):
    res = client.post("/quiz/grade", json={
        "algorithm": "bubble sort",
        "questions": QUESTIONS,
        "answers": ANSWERS,
    })
    results = res.get_json()["results"]
    for r in results:
        assert not r.get("correct"), "Expected incorrect answer"
        explanation = r.get("incorrect_explanation", "")
        assert len(explanation) >= 30, f"incorrect_explanation too short: {explanation!r}"
        assert len(explanation) <= 500, f"incorrect_explanation too long: {explanation!r}"
