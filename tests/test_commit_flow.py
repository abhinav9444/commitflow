import subprocess
from pathlib import Path


def test_git_commit_workflow(tmp_path):

    repo = tmp_path / "repo"
    repo.mkdir()

    subprocess.run(["git", "init"], cwd=repo, check=True)

    # Configure git identity for CI environment
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo,
        check=True
    )

    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=repo,
        check=True
    )

    test_file = repo / "test.txt"
    test_file.write_text("hello")

    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "test"], cwd=repo, check=True)

    result = subprocess.run(
        ["git", "log", "--oneline"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True
    )

    assert "test" in result.stdout