"""Study quiz must have exactly 2 questions per topic discussed in the session."""
import pytest
from collections import Counter
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_two_questions_per_topic(client):
    res = client.post("/study/quiz", json={
        "algorithm": "bubble sort",
        "history": [
            {"role": "user",      "content": "explain time complexity"},
            {"role": "assistant", "content": "Bubble sort is O(n^2) in the worst case."},
            {"role": "user",      "content": "explain space complexity"},
            {"role": "assistant", "content": "Bubble sort uses O(1) extra space."},
        ],
    })
    data = res.get_json()
    topics = data["topics"]
    questions = data["questions"]

    assert len(questions) == len(topics) * 2, (
        f"Expected {len(topics) * 2} questions for {len(topics)} topics, got {len(questions)}"
    )

    counts = Counter(q["topic"] for q in questions)
    for topic in topics:
        assert counts[topic] == 2, (
            f"Topic '{topic}' has {counts[topic]} question(s), expected 2"
        )
