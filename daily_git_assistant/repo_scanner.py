import os
import sys
import json
import threading
import itertools
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from .git_utils import is_git_repo


# --------------------------------------------------
# Repo index file
# --------------------------------------------------

INDEX_FILE = os.path.join(Path.home(), ".commitflow_repo_index.json")


# --------------------------------------------------
# Directories to skip during scanning
# --------------------------------------------------

SKIP_DIRS = {
    # Windows system
    "Windows",
    "Program Files",
    "Program Files (x86)",
    "ProgramData",
    "$Recycle.Bin",
    "System Volume Information",
    "Recovery",
    "PerfLogs",

    # Windows user cache
    "AppData",
    "Temp",

    # Development dependencies
    "node_modules",
    "__pycache__",
    ".cache",
    ".npm",
    ".yarn",
    ".venv",
    "venv",
    "env",
    ".tox",
    "dist",
    "build",
    ".mypy_cache",
    ".pytest_cache",
    ".gradle",

    # IDE folders
    ".idea",
    ".vscode",

    # Linux system
    "proc",
    "sys",
    "dev",
    "run",
    "boot",
    "lib",
    "lib64",
    "snap",
    "var",
    "lost+found",
}


# --------------------------------------------------
# Known developer directories
# --------------------------------------------------

def get_dev_directories():

    home = Path.home()

    candidates = [
        home / "projects",
        home / "Projects",
        home / "dev",
        home / "workspace",
        home / "code",
        home / "src",
        home / "repos",
        home / "Documents",
        home / "Downloads",
        home / "Pictures",
        home / "Videos",
        home / "Music",
    ]

    dev_dirs = []

    for d in candidates:

        if d.exists():
            dev_dirs.append(str(d))

    return dev_dirs


# --------------------------------------------------
# Save repo index
# --------------------------------------------------

def save_repo_index(repos):

    try:
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(repos, f, indent=2)

    except Exception:
        pass


# --------------------------------------------------
# Load repo index
# --------------------------------------------------

def load_repo_index():

    if not os.path.exists(INDEX_FILE):
        return []

    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return []


# --------------------------------------------------
# Validate stored repo paths
# --------------------------------------------------

def validate_repo_index(repos):

    valid = []

    for repo in repos:

        if os.path.exists(repo) and is_git_repo(repo):
            valid.append(repo)

    return valid


# --------------------------------------------------
# Detect system roots
# --------------------------------------------------

def get_system_roots():

    roots = []

    if os.name == "nt":

        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

            drive = f"{letter}:\\"

            if os.path.exists(drive):
                roots.append(drive)

    else:
        roots.append("/")

    return roots


# --------------------------------------------------
# Spinner progress
# --------------------------------------------------

def spinner_progress(counter, repos_found, stop_event):

    spinner = itertools.cycle([
        "⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"
    ])

    while not stop_event.is_set():

        spin = next(spinner)

        sys.stdout.write(
            f"\rScanning system {spin} folders: {counter[0]} repos: {repos_found[0]}"
        )

        sys.stdout.flush()

        time.sleep(0.1)

    print()


# --------------------------------------------------
# Scan a directory with adaptive depth
# --------------------------------------------------

def scan_directory(base_directory, counter, repos_found):

    repos = []

    base_depth = base_directory.count(os.sep)

    for root, dirs, files in os.walk(base_directory):

        counter[0] += 1

        # Directory pruning
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        depth = root.count(os.sep) - base_depth

        # Adaptive depth
        if base_directory == str(Path.home()):
            max_depth = 5
        else:
            max_depth = 3

        if depth > max_depth:
            dirs[:] = []
            continue

        # Early git detection
        if ".git" in dirs:

            if is_git_repo(root):

                repos.append(root)
                repos_found[0] += 1

            dirs.remove(".git")

    return repos


# --------------------------------------------------
# Scan entire filesystem (parallel)
# --------------------------------------------------

def scan_entire_system():

    roots = get_system_roots()
    dev_dirs = get_dev_directories()

    repos = []

    counter = [0]
    repos_found = [0]

    stop_event = threading.Event()

    spinner_thread = threading.Thread(
        target=spinner_progress,
        args=(counter, repos_found, stop_event),
        daemon=True
    )

    spinner_thread.start()

    try:

        # 1️⃣ Scan developer directories first
        for dev_dir in dev_dirs:

            repos.extend(scan_directory(dev_dir, counter, repos_found))

        # 2️⃣ Parallel scan system roots
        with ThreadPoolExecutor(max_workers=4) as executor:

            futures = []

            for root in roots:
                futures.append(
                    executor.submit(scan_directory, root, counter, repos_found)
                )

            for f in futures:
                repos.extend(f.result())

    except Exception:
        pass

    stop_event.set()
    spinner_thread.join()

    return repos


# --------------------------------------------------
# Display repositories
# --------------------------------------------------

def display_repos(repos):

    if not repos:

        print("\nNo Git repositories found.")
        return

    print("\nDetected Git Repositories:\n")

    for index, repo in enumerate(repos, start=1):

        name = os.path.basename(repo)

        print(f"{index}. {name}  ({repo})")


# --------------------------------------------------
# Repo selection
# --------------------------------------------------

def select_repo(repos):

    if not repos:
        return None

    display_repos(repos)

    while True:

        choice = input("\nSelect repository number (or 'r' to rescan) ➤ ").strip()

        if choice.lower() == "r":
            return "rescan"

        try:

            index = int(choice) - 1

            if 0 <= index < len(repos):
                return repos[index]

            else:
                print("Invalid selection.")

        except ValueError:

            print("Enter a valid number or 'r'.")


# --------------------------------------------------
# Main repo detection workflow
# --------------------------------------------------

def auto_detect_repo():

    print("Scanning system for Git repositories...\n")

    repos = load_repo_index()

    repos = validate_repo_index(repos)

    if not repos:

        repos = scan_entire_system()

        repos = list(set(repos))

        save_repo_index(repos)

    while True:

        repo = select_repo(repos)

        if repo == "rescan":

            print("\nRescanning entire system...\n")

            repos = scan_entire_system()

            repos = list(set(repos))

            save_repo_index(repos)

            continue

        return repo