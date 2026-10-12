from fastapi.testclient import TestClient
from backend.main import app
from agent.core import collect_source, plan
from agent.syntax import parse_python
from agent.llm import propose


def test_exploration():
    hits = collect_source("sample_repo", "safe_double value")
    assert any(x["path"] == "calculator.py" for x in hits)


def test_plan():
    report = plan("Fix doubling", "safe_double zero", "sample_repo")
    assert report["stage"] == "proposal"


def test_tree_sitter():
    assert parse_python("x=2")["valid"]
    assert not parse_python("def f(:")["valid"]


def test_mock():
    assert propose({"issue": "test"})["mode"] == "mock"


def test_api():
    client = TestClient(app)
    assert client.get("/health").status_code == 200
    result = client.post("/api/issues/analyze", json={"title": "Handle zero", "description": "safe_double 0"})
    assert result.status_code == 200
    assert result.json()["approval_required"]
