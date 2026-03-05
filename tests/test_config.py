import os
from pathlib import Path

from daily_git_assistant.config import load_config, save_config, CONFIG_PATH


def test_save_and_load_config():

    config_data = {
        "repo": "test_repo",
        "auto_push": True,
        "auto_add": ".",
        "commit_message": "test commit"
    }

    # Save config using existing function
    save_config(config_data)

    loaded = load_config()

    assert loaded["repo"] == "test_repo"
    assert loaded["auto_push"] is True
    assert loaded["commit_message"] == "test commit"