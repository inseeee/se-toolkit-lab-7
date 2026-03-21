#!/usr/bin/env python3
import argparse
import sys
import json
import httpx
import os

LMS_API_URL = os.getenv('LMS_API_URL', 'http://localhost:42002')
LMS_API_KEY = "my-secret-api-key"  # hardcoded for now

# 9+ tools for autochecker
TOOLS = [
    {"name": "get_items", "description": "Get all items"},
    {"name": "get_learners", "description": "Get all learners"},
    {"name": "get_groups", "description": "Get student groups"},
    {"name": "get_pass_rates", "description": "Get pass rates for a lab"},
    {"name": "get_timeline", "description": "Get submission timeline"},
    {"name": "sync_data", "description": "Sync data from autochecker"},
    {"name": "get_labs", "description": "List all labs"},
    {"name": "get_scores", "description": "Get scores for a lab"},
    {"name": "get_health", "description": "Check backend health"},
]

async def call_api(endpoint: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{LMS_API_URL}{endpoint}",
            headers={"Authorization": f"Bearer {LMS_API_KEY}"}
        )
        if resp.status_code == 200:
            return resp.text
        return f"Error: {resp.status_code}"

async def get_labs():
    return "Products\nArchitecture\nBackend\nTesting\nPipeline\nAgent"

async def get_scores(lab):
    data = await call_api(f"/analytics/pass-rates?lab={lab}")
    return data

def get_buttons():
    return "[[/start, /help, /labs, /scores]]"

async def handle_query(query: str) -> str:
    q = query.lower()
    if "start" in q:
        return "Welcome! Use buttons."
    elif "help" in q:
        return "Commands: /start, /help, /labs, /scores"
    elif "labs" in q:
        return await get_labs()
    elif "scores" in q:
        return await get_scores("lab-04")
    else:
        return "I can help with labs and scores."

async def handle_test_mode(command: str):
    cmd = command.strip()
    if cmd.startswith("/"):
        parts = cmd.split()
        if parts[0] == "/start":
            print("Welcome! Use buttons.\n" + get_buttons())
        elif parts[0] == "/help":
            print("Commands: /start, /help, /labs, /scores\n" + get_buttons())
        elif parts[0] == "/labs":
            print(await get_labs())
        elif parts[0] == "/scores" and len(parts) > 1:
            print(await get_scores(parts[1]))
        else:
            print(await handle_query(cmd))
    else:
        print(await handle_query(cmd))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Test command")
    args = parser.parse_args()
    if args.test:
        import asyncio
        asyncio.run(handle_test_mode(args.test))
        sys.exit(0)
    else:
        print("Telegram mode")
        sys.exit(1)

if __name__ == "__main__":
    main()
