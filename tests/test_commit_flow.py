import subprocess
from pathlib import Path

from daily_git_assistant.git_utils import is_git_repo


def test_git_commit_workflow(tmp_path):

    repo = tmp_path / "repo"
    repo.mkdir()

    subprocess.run(["git", "init"], cwd=repo)

    test_file = repo / "test.txt"
    test_file.write_text("hello")

    subprocess.run(["git", "add", "."], cwd=repo)
    subprocess.run(["git", "commit", "-m", "test"], cwd=repo)

    result = subprocess.run(
        ["git", "log", "--oneline"],
        cwd=repo,
        capture_output=True,
        text=True
    )

    assert "test" in result.stdout