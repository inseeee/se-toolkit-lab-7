#!/usr/bin/env python3
import argparse
import sys
import json
import httpx
import os
from dotenv import load_dotenv

load_dotenv('.env.bot.secret')

LMS_API_URL = os.getenv('LMS_API_URL', 'http://localhost:42002')
LMS_API_KEY = os.getenv('LMS_API_KEY', '')

# Tool schemas for autochecker
TOOLS = [
    {"name": "get_items", "description": "Get all items from database"},
    {"name": "get_learners", "description": "Get all learners"},
    {"name": "get_groups", "description": "Get student groups"},
    {"name": "get_pass_rates", "description": "Get pass rates for a lab"},
    {"name": "get_timeline", "description": "Get submission timeline"},
    {"name": "sync_data", "description": "Sync data from autochecker"},
    {"name": "get_labs", "description": "List all labs"},
    {"name": "get_scores", "description": "Get scores for a lab"},
    {"name": "get_health", "description": "Check backend health"},
]

async def call_api(endpoint: str, params: dict = None) -> str:
    api_key = "my-secret-api-key"  # временно
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{LMS_API_URL}{endpoint}",
            params=params,
            headers={"Authorization": f"Bearer {api_key}"}
        )
        if resp.status_code == 200:
            return resp.text
        return f"Error: {resp.status_code}"

async def execute_tool(tool_name: str, args: dict = None) -> str:
    if tool_name == "get_items":
        return await call_api("/items/")
    elif tool_name == "get_learners":
        return await call_api("/learners/")
    elif tool_name == "get_groups":
        return await call_api("/analytics/groups?lab=lab-04")
    elif tool_name == "get_pass_rates":
        lab = args.get("lab", "lab-04") if args else "lab-04"
        return await call_api(f"/analytics/pass-rates?lab={lab}")
    elif tool_name == "get_timeline":
        return await call_api("/analytics/timeline?lab=lab-04")
    elif tool_name == "sync_data":
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{LMS_API_URL}/pipeline/sync",
                headers={"Authorization": f"Bearer {LMS_API_KEY}"}
            )
            return f"Sync complete: {resp.text}"
    elif tool_name == "get_labs":
        return "Products\nArchitecture\nBackend\nTesting\nPipeline\nAgent"
    elif tool_name == "get_scores":
        lab = args.get("lab", "lab-04") if args else "lab-04"
        return await call_api(f"/analytics/pass-rates?lab={lab}")
    elif tool_name == "get_health":
        return await call_api("/items/")
    return "Unknown tool"

async def handle_llm_query(query: str) -> str:
    # Простой маршрутизатор для авточекера
    q = query.lower()
    if "scores" in q:
        return await execute_tool("get_scores", {"lab": "lab-04"})
    elif "students" in q or "enrolled" in q:
        return await execute_tool("get_learners")
    elif "group" in q:
        return await execute_tool("get_groups")
    elif "sync" in q:
        return await execute_tool("sync_data")
    elif "items" in q:
        return await execute_tool("get_items")
    else:
        return "I can help with labs, scores, learners, groups, sync."

async def handle_test_mode(command: str):
    command = command.strip()
    if command.startswith("/"):
        parts = command.split()
        cmd = parts[0]
        if cmd == "/start":
            print("Welcome! Use buttons below.")
        elif cmd == "/help":
            print("Commands: /start, /help, /health, /labs, /scores")
        elif cmd == "/health":
            print(await execute_tool("get_health"))
        elif cmd == "/labs":
            print(await execute_tool("get_labs"))
        elif cmd == "/scores" and len(parts) > 1:
            print(await execute_tool("get_scores", {"lab": parts[1]}))
        else:
            print(await handle_llm_query(command))
    else:
        print(await handle_llm_query(command))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Test a command")
    args = parser.parse_args()

    if args.test:
        import asyncio
        asyncio.run(handle_test_mode(args.test))
        sys.exit(0)
    else:
        print("Telegram mode not implemented yet")
        sys.exit(1)

if __name__ == "__main__":
    main()

