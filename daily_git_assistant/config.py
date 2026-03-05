import os
import json
from pathlib import Path

# Default config file location
CONFIG_PATH = os.path.join(Path.home(), ".commitflow_config.json")

# Default configuration values
DEFAULT_CONFIG = {
    "repo": "",
    "auto_push": False,
    "auto_add": ".",
    "commit_message": "Daily progress update",
    "schedule_time": "21:00"
}


def create_default_config():
    """
    Create a config file with default values if it does not exist.
    """
    if not os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "w") as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)

            return DEFAULT_CONFIG

        except Exception as e:
            raise RuntimeError(f"Failed to create config file: {e}")

    return load_config()


def load_config():
    """
    Load configuration from config file.
    """
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)

        return config

    except FileNotFoundError:

        return create_default_config()

    except json.JSONDecodeError:

        raise RuntimeError(
            "Config file corrupted. Delete ~/.commitflow_config.json and run setup again."
        )


def save_config(config_data):
    """
    Save updated configuration.
    """

    try:

        with open(CONFIG_PATH, "w") as f:
            json.dump(config_data, f, indent=4)

    except Exception as e:

        raise RuntimeError(f"Failed to save config: {e}")


def update_config(key, value):
    """
    Update a single configuration field.
    """

    config = load_config()

    config[key] = value

    save_config(config)


def validate_repo_path(repo_path):
    """
    Ensure repository path exists and is valid.
    """

    if not repo_path:
        raise ValueError("Repository path not set in config")

    if not os.path.exists(repo_path):
        raise ValueError(f"Repository path does not exist: {repo_path}")

    return True


def get_repo():
    """
    Retrieve repository path from config.
    """

    config = load_config()

    repo = config.get("repo", "")

    validate_repo_path(repo)

    return repo


def reset_config():
    """
    Reset configuration to default values.
    """

    try:

        with open(CONFIG_PATH, "w") as f:

            json.dump(DEFAULT_CONFIG, f, indent=4)

        return True

    except Exception as e:

        raise RuntimeError(f"Failed to reset config: {e}")