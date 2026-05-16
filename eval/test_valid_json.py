"""Every endpoint response body must be strictly valid JSON."""
import json
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


REQUESTS = [
    ("/generate",          {"algorithm": "bubble sort"}),
    ("/study",             {"algorithm": "bubble sort", "question": "how does it work?", "history": []}),
    ("/study/quiz",        {"algorithm": "bubble sort", "history": [
        {"role": "user",      "content": "how does it work?"},
        {"role": "assistant", "content": "It repeatedly swaps adjacent elements."},
    ]}),
    ("/quiz",              {"algorithm": "bubble sort"}),
    ("/quiz/grade",        {"algorithm": "bubble sort",
                            "questions": [{"type": "short_response", "question": "What is the time complexity?", "answer": "O(n^2)"}],
                            "answers": {"0": "O(n)"}}),
    ("/study/effectiveness", {
        "history": [
            {"role": "user",      "content": "explain time complexity"},
            {"role": "assistant", "content": "Bubble sort is O(n^2)."},
        ],
        "questions": [{"type": "short_response", "question": "What is the time complexity?", "answer": "O(n^2)", "topic": "time complexity"}],
        "topics": ["time complexity"],
    }),
]


@pytest.mark.parametrize("url,body", REQUESTS)
def test_response_is_valid_json(client, url, body):
    res = client.post(url, json=body)
    # Flask's test client returns bytes; ensure it parses without error
    parsed = json.loads(res.data)
    assert isinstance(parsed, dict)
