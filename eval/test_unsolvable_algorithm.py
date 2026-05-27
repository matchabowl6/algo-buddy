"""Unsolvable algorithms (e.g. halting problem) must return a refusal, not code."""
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_halting_problem_returns_blank_json(client):
    res = client.post("/generate", json={"algorithm": "halting problem"})
    res_dict = res.get_json()

    # The /generate endpoint must return a blank JSON object if the app refuses to
    # or cannot implement the algorithm
    assert not res_dict
