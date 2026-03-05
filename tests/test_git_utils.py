import os
import subprocess
from pathlib import Path

from daily_git_assistant.git_utils import is_git_repo


def test_is_git_repo(tmp_path):

    repo = tmp_path / "repo"
    repo.mkdir()

    subprocess.run(["git", "init"], cwd=repo)

    assert is_git_repo(str(repo)) is True


def test_not_git_repo(tmp_path):

    repo = tmp_path / "repo"
    repo.mkdir()

    assert is_git_repo(str(repo)) is False