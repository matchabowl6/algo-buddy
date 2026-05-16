"""
Calls the real OpenAI API via /eval/valid-json and asserts that
response.choices[0].message.content is strictly valid JSON by simulating calls to
generate() and study() server-side.
JSONDecodeError is caught server-side; the test fails if pass is False.
"""
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_openai_returns_valid_json(client):
    res = client.post("/eval/valid-json")
    data = res.get_json()
    assert data["pass"], f"OpenAI returned invalid JSON: {data.get('error')}"
