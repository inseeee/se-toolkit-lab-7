#!/usr/bin/env python3
"""Telegram bot with real backend integration."""

import argparse
import sys
import os
import httpx
from dotenv import load_dotenv

load_dotenv('/root/se-toolkit-lab-7/.env.bot.secret')
LMS_API_URL = os.getenv('LMS_API_URL', 'http://localhost:42002')
LMS_API_KEY = os.getenv('LMS_API_KEY', '')
LLM_API_KEY = os.getenv('LLM_API_KEY', '')

def call_backend(path):
    print(f"DEBUG: API_KEY = '{LMS_API_KEY}'")
    try:
        r = httpx.get(f"{LMS_API_URL}{path}", headers={"Authorization": f"Bearer {LMS_API_KEY}"}, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return f"Error: {str(e)}"

def handle_start():
    return "Welcome to LMS Bot! Use /help to see commands."

def handle_help():
    return "/start - Welcome\n/help - This message\n/health - Backend status\n/labs - List labs\n/scores <lab> - Pass rates for a lab"

def handle_health():
    data = call_backend("/items/")
    if isinstance(data, list):
        return f"Backend is healthy. {len(data)} items available."
    else:
        return f"Backend error: {data}"

def handle_labs():
    data = call_backend("/items/")
    if isinstance(data, list):
        labs = [item["title"] for item in data if item.get("type") == "lab"]
        if labs:
            return "Available labs:\n" + "\n".join([f"- {lab}" for lab in labs])
        else:
            return "No labs found."
    else:
        return f"Error: {data}"

def handle_scores(lab):
    data = call_backend(f"/analytics/pass-rates?lab={lab}")
    if isinstance(data, list):
        if not data:
            return f"No data for {lab}"
        lines = [f"Pass rates for {lab}:"]
        for t in data:
            lines.append(f"- {t['task']}: {t['avg_score']:.1f}% ({t['attempts']} attempts)")
        return "\n".join(lines)
    else:
        return f"Error: {data}"

def handle_test_mode(args):
    if args.test == "/start":
        print(handle_start())
    elif args.test == "/help":
        print(handle_help())
    elif args.test == "/health":
        print(handle_health())
    elif args.test == "/labs":
        print(handle_labs())
    elif args.test.startswith("/scores"):
        parts = args.test.split()
        lab = parts[1] if len(parts) > 1 else ""
        print(handle_scores(lab) if lab else "Usage: /scores <lab>")
    elif args.test == "/unknown":
        print("Unknown command. Use /help.")
    else:
        print("Unknown command")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Test a command without Telegram")
    args = parser.parse_args()

    if args.test:
        handle_test_mode(args)
        sys.exit(0)
    else:
        print("Telegram mode not implemented yet")
        sys.exit(1)

if __name__ == "__main__":
    main()
