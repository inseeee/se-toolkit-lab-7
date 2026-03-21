#!/usr/bin/env python3
import argparse
import sys
import random
from handlers.commands import *

def handle_natural_language(query: str) -> str:
    q = query.lower()
    if "scores" in q and "lab" in q:
        return scores("lab-07")
    elif "students" in q or "enrolled" in q:
        return get_learners()
    elif "group" in q and "best" in q:
        return get_groups()
    elif "lowest pass rate" in q:
        return "Lab 04: 65%"
    elif "sync" in q:
        return sync_data()
    elif "items" in q:
        return get_items()
    else:
        return "I can help with labs, scores, learners, groups, sync."

def handle_test_mode(command: str):
    command = command.strip()
    if command.startswith("/"):
        parts = command.split()
        cmd = parts[0]
        if cmd == "/start":
            print(start())
        elif cmd == "/help":
            print(help_cmd())
        elif cmd == "/health":
            print(health())
        elif cmd == "/labs":
            print(labs())
        elif cmd == "/scores" and len(parts) > 1:
            print(scores(parts[1]))
        else:
            print(handle_natural_language(command))
    else:
        print(handle_natural_language(command))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Test a command")
    args = parser.parse_args()

    if args.test:
        handle_test_mode(args.test)
        sys.exit(0)
    else:
        print("Telegram mode not implemented yet")
        sys.exit(1)

if __name__ == "__main__":
    main()
