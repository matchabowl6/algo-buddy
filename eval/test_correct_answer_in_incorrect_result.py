"""For incorrect answers, correct_explanation must also be 30–500 chars."""
import pytest
from api.app import app

QUESTIONS = [
    {"type": "short_response", "question": "What is the time complexity of bubble sort?", "answer": "O(n^2)"},
    {"type": "multiple_choice", "question": "Which is true about bubble sort?",
     "options": ["O(n^2) worst case", "O(n log n) worst case", "Not stable", "Recursive only"],
     "answer": "O(n^2) worst case"},
]
ANSWERS = {"0": "O(n)", "1": "O(n log n) worst case"}


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_correct_explanation_present_in_incorrect_result(client):
    res = client.post("/api/quiz/grade", json={
        "algorithm": "bubble sort",
        "questions": QUESTIONS,
        "answers": ANSWERS,
    })
    results = res.get_json()["results"]
    for r in results:
        assert not r.get("correct"), "Expected incorrect answer"
        explanation = r.get("correct_explanation", "")
        assert len(explanation) >= 30, f"correct_explanation too short in incorrect result: {explanation!r}"
        assert len(explanation) <= 500, f"correct_explanation too long in incorrect result: {explanation!r}"
