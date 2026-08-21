"""Generated Python code must have no syntax errors."""
import ast
import pytest
from api.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


ALGORITHMS = ["bubble sort", "binary search", "merge sort", "quicksort", "depth first search"]


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_generated_code_has_no_syntax_errors(client, algorithm):
    res = client.post("/api/generate", json={"algorithm": algorithm})
    code = res.get_json()["code"]
    # ast.parse raises SyntaxError if the code is invalid
    ast.parse(code)
