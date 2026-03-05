import os
from pathlib import Path
from datetime import datetime


# Log file location
LOG_PATH = os.path.join(Path.home(), ".commitflow.log")

# Ensure log directory exists (future-proof safety)
try:
    log_dir = os.path.dirname(LOG_PATH)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
except Exception:
    # Logging should never break the application
    pass


def _write_log(level, message):
    """
    Internal function to write log messages.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] [{level}] {message}\n"

    try:
        with open(LOG_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)

    except Exception:
        # Logging should never crash the application
        pass


def log_info(message):
    """
    Log informational message.
    """

    _write_log("INFO", message)


def log_warning(message):
    """
    Log warning message.
    """

    _write_log("WARNING", message)


def log_error(message):
    """
    Log error message.
    """

    _write_log("ERROR", message)


def log_commit(repo, branch, files, message, pushed):
    """
    Specialized log for commit operations.
    """

    commit_log = (
        f"repo={repo} "
        f"branch={branch} "
        f"files={files} "
        f"message='{message}' "
        f"pushed={pushed}"
    )

    _write_log("COMMIT", commit_log)


def read_logs(lines=20):
    """
    Read last N log entries.
    """

    if not os.path.exists(LOG_PATH):
        return []

    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            logs = f.readlines()

        return logs[-lines:]

    except Exception:
        return []


def clear_logs():
    """
    Clear log file.
    """

    try:
        if os.path.exists(LOG_PATH):
            open(LOG_PATH, "w").close()

    except Exception:
        pass