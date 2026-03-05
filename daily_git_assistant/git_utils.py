import os
import subprocess


def run_git_command(cmd, repo_path):
    """
    Execute a git command safely.
    """

    try:

        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True
        )

        return result

    except Exception as e:

        raise RuntimeError(f"Git command failed: {e}")


def is_git_repo(repo_path):
    """
    Validate whether a directory is a git repository.
    """

    if not os.path.exists(repo_path):
        return False

    result = run_git_command(["git", "rev-parse", "--is-inside-work-tree"], repo_path)

    return result.returncode == 0


def get_repo_name(repo_path):
    """
    Get repository folder name.
    """

    return os.path.basename(os.path.abspath(repo_path))


def get_branch(repo_path):
    """
    Get current git branch.
    """

    result = run_git_command(["git", "branch", "--show-current"], repo_path)

    if result.returncode != 0:
        return "unknown"

    return result.stdout.strip()


def get_remote_url(repo_path):
    """
    Retrieve repository remote URL.
    """

    result = run_git_command(
        ["git", "config", "--get", "remote.origin.url"],
        repo_path
    )

    if result.returncode != 0:
        return "unknown"

    return result.stdout.strip()


def get_status(repo_path):
    """
    Show git status.
    """

    result = run_git_command(["git", "status"], repo_path)

    return result.stdout


def add_files(repo_path, files):
    """
    Stage files for commit.
    """

    result = run_git_command(["git", "add", files], repo_path)

    if result.returncode != 0:
        raise RuntimeError("Failed to add files")


def preview_staged_changes(repo_path):
    """
    Preview staged changes before committing.
    """

    result = run_git_command(["git", "diff", "--cached"], repo_path)

    return result.stdout


def has_changes_to_commit(repo_path):
    """
    Detect if there are staged changes.
    """

    result = run_git_command(
        ["git", "diff", "--cached", "--quiet"],
        repo_path
    )

    # returncode 0 means no changes
    return result.returncode != 0


def commit_changes(repo_path, message):
    """
    Commit staged changes.
    """

    result = run_git_command(
        ["git", "commit", "-m", message],
        repo_path
    )

    if result.returncode != 0:
        raise RuntimeError("Commit failed")

    return result.stdout


def push_changes(repo_path):
    """
    Push commit to remote repository.
    """

    result = run_git_command(["git", "push"], repo_path)

    if result.returncode != 0:
        raise RuntimeError("Push failed")

    return result.stdout


def count_staged_files(repo_path):
    """
    Count number of staged files.
    """

    result = run_git_command(
        ["git", "diff", "--name-only", "--cached"],
        repo_path
    )

    if result.returncode != 0:
        return 0

    files = result.stdout.strip().splitlines()

    return len(files)