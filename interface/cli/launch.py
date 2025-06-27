# phantomroll/interface/cli/launch.py

import argparse
import asyncio
import sys
import os

# Ensure the controller path is accessible
sys.path.append(os.path.expanduser('~/phantomroll/phantomroll/controller/python'))

from main_controller import main as controller_main


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="🎲 PhantomRoll - Telegram Dice Control CLI Interface"
    )

    parser.add_argument(
        "--chat", "-c", type=str, help="Target Telegram chat username or ID (e.g., @groupname)"
    )
    parser.add_argument(
        "--sums", "-s", type=str,
        help="Comma-separated list of valid target sums (e.g., 10,12,15)"
    )
    parser.add_argument(
        "--stealth", action="store_true", help="Enable stealth auto-delete booster"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Only simulate logic without sending messages"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    return parser.parse_args()


async def run_main(args):
    # Prompt for missing inputs
    chat = args.chat or input("Enter target chat username or ID: ").strip()
    sum_input = args.sums or input("Enter target sums (comma-separated): ").strip()

    # Inject runtime context if needed later
    os.environ["PHANTOM_STEALTH"] = "1" if args.stealth else "0"
    os.environ["PHANTOM_DRYRUN"] = "1" if args.dry_run else "0"
    os.environ["PHANTOM_VERBOSE"] = "1" if args.verbose else "0"

    # Inject into global namespace for main_controller
    sys.argv = ["main_controller", chat, sum_input]
    await controller_main()


if __name__ == "__main__":
    args = parse_arguments()
    try:
        asyncio.run(run_main(args))
    except KeyboardInterrupt:
        print("\n[!] Exiting PhantomRoll...")
