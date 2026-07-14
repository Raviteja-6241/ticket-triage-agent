import os
from src.schema import Issue


def test_sample_issues_exist():
    assert os.path.exists("data/issues.json")


def test_sample_issues_load():
    issues = Issue.load_from_file("data/issues.json")
    assert len(issues) > 0
    assert all(issue.issue_id for issue in issues)


def test_project_structure():
    assert os.path.exists("src/agents.py")
    assert os.path.exists("src/tasks.py")
    assert os.path.exists("src/crew.py")
    assert os.path.exists("src/tools.py")
    assert os.path.exists("src/schema.py")
    assert os.path.exists("main.py")
