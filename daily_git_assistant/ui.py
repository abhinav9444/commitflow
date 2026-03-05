from colorama import Fore, Style, init

init(autoreset=True)


def print_header(version="CommitFlow v1.0"):
    """
    Display tool header.
    """

    print(Fore.CYAN + Style.BRIGHT)
    print("═══════════════════════════════════════")
    print(f"           {version}")
    print("     Daily Git Consistency Assistant")
    print("═══════════════════════════════════════")
    print(Style.RESET_ALL)


def divider():
    """
    Print a visual divider.
    """

    print(Fore.CYAN + "────────────────────────────────────────" + Style.RESET_ALL)


def print_section(title):
    """
    Display a section heading.
    """

    divider()
    print(Fore.YELLOW + Style.BRIGHT + title)
    divider()


def info(message):
    """
    Display informational message.
    """

    print(Fore.CYAN + f"[INFO] {message}")


def success(message):
    """
    Display success message.
    """

    print(Fore.GREEN + f"[SUCCESS] {message}")


def warning(message):
    """
    Display warning message.
    """

    print(Fore.YELLOW + f"[WARNING] {message}")


def error(message):
    """
    Display error message.
    """

    print(Fore.RED + f"[ERROR] {message}")


def print_repo_info(repo, branch, remote):
    """
    Display repository details.
    """

    print(Fore.CYAN + Style.BRIGHT)
    print(f"📦 Repository : {repo}")
    print(f"🌿 Branch     : {branch}")
    print(f"🔗 Remote     : {remote}")
    print(Style.RESET_ALL)


def print_git_status(status_output):
    """
    Print git status output.
    """

    print(Fore.YELLOW + "\n📄 Git Status:\n" + Style.RESET_ALL)
    print(status_output)


def show_commit_preview(diff_output):
    """
    Display staged changes preview.
    """

    print_section("Preview Staged Changes")

    if not diff_output.strip():

        warning("No staged changes detected.")

    else:

        print(diff_output)


def print_commit_summary(repo, branch, files, message, pushed):
    """
    Display commit summary after operation.
    """

    pushed_text = "Yes" if pushed else "No"

    print("\n" + Fore.CYAN + Style.BRIGHT)
    print("══════════════════════════")
    print("Commit Summary")
    print("══════════════════════════")

    print(f"Repo      : {repo}")
    print(f"Branch    : {branch}")
    print(f"Files     : {files}")
    print(f"Message   : {message}")
    print(f"Pushed    : {pushed_text}")

    print("══════════════════════════")
    print(Style.RESET_ALL)


def prompt(message):
    """
    Input prompt helper.
    """

    return input(Fore.CYAN + message + Style.RESET_ALL)


def restart_message():
    """
    Display restart message for repeated commits.
    """

    print(Fore.CYAN + "\n♻ Restarting session...\n")


def exit_message():
    """
    Display exit message.
    """

    print(Fore.GREEN + "\n👋 Exiting CommitFlow. Stay consistent!")