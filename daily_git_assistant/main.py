import argparse
import sys

from . import __version__
from .ui import print_header, error
from .scheduler import schedule_interactive

# modes
from .modes.interactive import interactive_mode
from .modes.quick import quick_mode
from .modes.auto import auto_mode
from .modes.setup import setup_mode


VERSION = f"CommitFlow {__version__}"


def main():
    """
    Main CLI entrypoint.
    """

    parser = argparse.ArgumentParser(
        prog="commitflow",
        description="CommitFlow - Daily Git consistency assistant"
    )

    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick commit mode using configured repository"
    )

    parser.add_argument(
        "--auto",
        action="store_true",
        help="Automatic commit mode (used by scheduler)"
    )

    parser.add_argument(
        "--setup",
        action="store_true",
        help="Run setup wizard"
    )

    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Create scheduled automation task"
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show CommitFlow version"
    )

    args = parser.parse_args()

    try:

        # version command
        if args.version:

            print(VERSION)
            return

        # setup wizard
        if args.setup:

            setup_mode()
            return

        # scheduler setup
        if args.schedule:

            print_header(VERSION)
            schedule_interactive()
            return

        # auto mode
        if args.auto:

            auto_mode()
            return

        # quick mode
        if args.quick:

            quick_mode()
            return

        # default interactive mode
        interactive_mode()

    except KeyboardInterrupt:

        print("\nOperation cancelled by user.")
        sys.exit(0)

    except Exception as e:

        error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()