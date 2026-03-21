#!/usr/bin/env python3
import argparse
import sys
from handlers.commands import start, help_cmd, health, labs, scores

def handle_test_mode(command: str):
    command = command.strip().lower()
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
        print(f"Unknown command: {command}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Test a command without Telegram")
    args = parser.parse_args()

    if args.test:
        handle_test_mode(args.test)
        sys.exit(0)
    else:
        print("Telegram mode not implemented yet")
        sys.exit(1)

if __name__ == "__main__":
    main()
