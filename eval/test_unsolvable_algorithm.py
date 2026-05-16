"""Unsolvable algorithms (e.g. halting problem) must return a refusal, not code."""
import ast
import pytest
from app import app

REFUSAL = "# I don't know how to implement this, as a well-known solution has not been discovered yet"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_halting_problem_returns_refusal(client):
    res = client.post("/generate", json={"algorithm": "halting problem"})
    code = res.get_json()["code"].strip()
    assert code == REFUSAL


def test_halting_problem_is_not_runnable_code(client):
    res = client.post("/generate", json={"algorithm": "halting problem"})
    code = res.get_json()["code"].strip()
    # Must not be parseable as a callable implementation (no function definitions)
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return  # also acceptable — not valid Python code
    has_function = any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in ast.walk(tree))
    assert not has_function
