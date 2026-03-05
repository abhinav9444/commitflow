import os
from datetime import datetime

from ..config import load_config
from ..git_utils import (
    is_git_repo,
    get_branch,
    add_files,
    has_changes_to_commit,
    commit_changes,
    push_changes,
    count_staged_files
)

from ..ui import (
    print_header,
    success,
    warning,
    error,
    print_commit_summary
)

from ..logger import (
    log_commit,
    log_info,
    log_warning,
    log_error
)


def auto_mode():
    """
    Fully automatic commit mode.
    Used by schedulers.
    """

    try:

        print_header()

        config = load_config()

        repo_path = config.get("repo", "")
        auto_add = config.get("auto_add", ".")
        auto_push = config.get("auto_push", False)
        commit_message = config.get("commit_message", "daily progress update")

        if not repo_path:

            error("Repository not configured.")
            log_error("Auto mode failed: repo not configured")
            return

        if not os.path.isdir(repo_path):

            error("Configured repository path does not exist.")
            log_error("Auto mode failed: repo path invalid")
            return

        if not is_git_repo(repo_path):

            error("Configured path is not a git repository.")
            log_error("Auto mode failed: not a git repo")
            return

        repo_name = os.path.basename(repo_path)

        branch = get_branch(repo_path)

        log_info(f"Auto commit started for repo={repo_name}")

        add_files(repo_path, auto_add)

        if not has_changes_to_commit(repo_path):

            warning("No changes detected. Skipping commit.")
            log_warning("Auto commit skipped: no changes")
            return

        today = datetime.now().strftime("%Y-%m-%d")

        message = f"{commit_message} ({today})"

        commit_changes(repo_path, message)

        pushed = False

        if auto_push:

            push_changes(repo_path)

            pushed = True

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

        success("Auto commit completed successfully.")

    except Exception as e:

        error(f"Auto mode failed: {str(e)}")

        log_error(str(e))