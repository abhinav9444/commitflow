import os
from pathlib import Path
from .git_utils import is_git_repo


def scan_for_git_repos(base_directory=None, max_depth=3):
    """
    Scan a directory recursively to find Git repositories.
    """

    repos = []

    if base_directory is None:
        base_directory = Path.home()

    base_directory = os.path.expanduser(base_directory)

    for root, dirs, files in os.walk(base_directory):

        # limit search depth
        depth = root[len(base_directory):].count(os.sep)
        if depth > max_depth:
            dirs[:] = []
            continue

        if ".git" in dirs:

            if is_git_repo(root):
                repos.append(root)

            dirs.remove(".git")

    return repos


def scan_common_dev_directories():
    """
    Scan common development directories automatically.
    """

    common_dirs = [
        os.path.join(Path.home(), "projects"),
        os.path.join(Path.home(), "Projects"),
        os.path.join(Path.home(), "Documents"),
        os.path.join(Path.home(), "workspace"),
        os.path.join(Path.home(), "dev"),
    ]

    repos = []

    for directory in common_dirs:

        if os.path.exists(directory):

            repos.extend(scan_for_git_repos(directory))

    # remove duplicates
    repos = list(set(repos))

    return repos


def display_repos(repos):
    """
    Display detected repositories.
    """

    if not repos:

        print("No Git repositories found.")
        return

    print("\nDetected Git Repositories:\n")

    for index, repo in enumerate(repos, start=1):

        name = os.path.basename(repo)

        print(f"{index}. {name}  ({repo})")


def select_repo(repos):
    """
    Allow user to choose repository interactively.
    """

    if not repos:
        return None

    display_repos(repos)

    while True:

        try:

            choice = input("\nSelect repository number ➤ ").strip()

            index = int(choice) - 1

            if 0 <= index < len(repos):

                return repos[index]

            else:
                print("Invalid selection. Try again.")

        except ValueError:

            print("Enter a valid number.")


def auto_detect_repo():
    """
    Auto detect repositories and allow selection.
    """

    print("Scanning for Git repositories...")

    repos = scan_common_dev_directories()

    if not repos:

        print("No repositories detected.")

        return None

    return select_repo(repos)