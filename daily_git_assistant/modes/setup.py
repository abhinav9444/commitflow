import os

from ..config import save_config, DEFAULT_CONFIG
from ..git_utils import is_git_repo
from ..scheduler import schedule_interactive
from ..ui import (
    print_header,
    divider,
    success,
    error,
    info,
    prompt
)

from ..logger import log_info


def setup_mode():
    """
    CommitFlow setup wizard.
    """

    try:

        print_header()

        divider()
        info("CommitFlow Setup Wizard")
        divider()

        # Ask repository path
        repo_path = prompt("📁 Repository path ➤ ").strip()

        if not repo_path:
            error("Repository path cannot be empty.")
            return

        if not os.path.isdir(repo_path):
            error("Directory does not exist.")
            return

        if not is_git_repo(repo_path):
            error("Selected directory is not a Git repository.")
            return

        # Auto push option
        push_choice = prompt("🚀 Push automatically after commit? (y/n) ➤ ").lower()
        auto_push = push_choice == "y"

        # Default commit message
        commit_message = prompt(
            "📝 Default commit message (press Enter for default) ➤ "
        ).strip()

        if not commit_message:
            commit_message = DEFAULT_CONFIG["commit_message"]

        # Schedule time
        schedule_time = prompt(
            "⏰ Daily commit time (HH:MM) ➤ "
        ).strip()

        # Create configuration
        config = {
            "repo": repo_path,
            "auto_push": auto_push,
            "auto_add": ".",
            "commit_message": commit_message,
            "schedule_time": schedule_time
        }

        save_config(config)

        success("Configuration saved successfully.")

        divider()

        # Ask scheduler creation
        schedule_choice = prompt("⚙ Setup automatic scheduler now? (y/n) ➤ ").lower()

        if schedule_choice == "y":
            schedule_interactive()

        success("CommitFlow setup completed successfully.")

        log_info("CommitFlow setup completed")

    except Exception as e:

        error(f"Setup failed: {str(e)}")