import os
from datetime import datetime

from ..config import get_repo
from ..git_utils import (
    is_git_repo,
    get_status,
    get_branch,
    get_remote_url,
    add_files,
    preview_staged_changes,
    has_changes_to_commit,
    commit_changes,
    push_changes,
    count_staged_files
)

from ..ui import (
    print_header,
    divider,
    print_repo_info,
    print_git_status,
    show_commit_preview,
    print_commit_summary,
    info,
    success,
    warning,
    error,
    prompt
)

from ..logger import log_commit, log_error


def quick_mode():
    """
    Quick commit mode using repository from config.
    """

    try:

        print_header()

        repo_path = get_repo()

        if not os.path.isdir(repo_path):

            error("Configured repository path does not exist.")
            return

        if not is_git_repo(repo_path):

            error("Configured directory is not a Git repository.")
            return

        repo_name = os.path.basename(repo_path)

        branch = get_branch(repo_path)

        remote = get_remote_url(repo_path)

        divider()

        print_repo_info(repo_name, branch, remote)

        divider()

        status = get_status(repo_path)

        print_git_status(status)

        divider()

        files = prompt("➕ Files to add ('.' for all) ➤ ").strip()

        if not files:
            files = "."

        add_files(repo_path, files)

        if not has_changes_to_commit(repo_path):

            warning("Nothing to commit.")
            return

        diff = preview_staged_changes(repo_path)

        show_commit_preview(diff)

        confirm = prompt("Proceed with commit? (y/n) ➤ ").lower()

        if confirm != "y":

            warning("Commit cancelled.")
            return

        message = prompt("📝 Commit message (Enter for auto) ➤ ").strip()

        if not message:

            today = datetime.now().strftime("%Y-%m-%d")

            message = f"daily progress update ({today})"

        commit_changes(repo_path, message)

        success("Commit successful.")

        pushed = False

        push = prompt("🚀 Push to remote? (y/n) ➤ ").lower()

        if push == "y":

            push_changes(repo_path)

            pushed = True

            success("Changes pushed to remote.")

        files_count = count_staged_files(repo_path)

        print_commit_summary(
            repo=repo_name,
            branch=branch,
            files=files_count,
            message=message,
            pushed=pushed
        )

        log_commit(
            repo=repo_name,
            branch=branch,
            files=files_count,
            message=message,
            pushed=pushed
        )

    except Exception as e:

        error(f"Unexpected error: {str(e)}")

        log_error(str(e))