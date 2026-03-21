#!/usr/bin/env python3
"""Telegram bot entry point with --test mode."""

import argparse
import sys
import os
from dotenv import load_dotenv

load_dotenv('.env.bot.secret')

LMS_API_URL = os.getenv('LMS_API_URL', 'http://localhost:42002')
LMS_API_KEY = os.getenv('LMS_API_KEY', '')

def handle_start():
    return "Welcome to LMS Bot! Use /help to see available commands."

def handle_help():
    return "/start - Welcome\n/help - This message\n/health - Backend status\n/labs - List labs"

def handle_health():
    return "Backend is healthy (placeholder)"

def handle_labs():
    return "Available labs: lab-04, lab-05, lab-06 (placeholder)"

def handle_test_mode(command):
    command = command.strip().lower()
    if command == "/start":
        print(handle_start())
    elif command == "/help":
        print(handle_help())
    elif command == "/health":
        print(handle_health())
    elif command == "/labs":
        print(handle_labs())
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
