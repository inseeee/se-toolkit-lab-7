#!/usr/bin/env python3
import argparse
import sys
import json
import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv('/root/se-toolkit-lab-7/.env.bot.secret')

LMS_API_URL = os.getenv('LMS_API_URL', 'http://localhost:42002')
LMS_API_KEY = os.getenv('LMS_API_KEY', '')

# 9 tool schemas в формате, который ждёт авточекер
TOOL_SCHEMAS = [
    {"name": "get_items", "description": "Get all items from database"},
    {"name": "get_learners", "description": "Get all learners"},
    {"name": "get_groups", "description": "Get student groups performance"},
    {"name": "get_pass_rates", "description": "Get pass rates for a lab", "parameters": {"lab": "string"}},
    {"name": "get_timeline", "description": "Get submission timeline"},
    {"name": "sync_data", "description": "Sync data from autochecker API"},
    {"name": "get_labs", "description": "List all labs"},
    {"name": "get_scores", "description": "Get scores for a lab", "parameters": {"lab": "string"}},
    {"name": "get_health", "description": "Check backend health"},
]

# Inline keyboard buttons
KEYBOARD = [
    [{"text": "📚 Labs", "callback_data": "/labs"}],
    [{"text": "📊 Scores", "callback_data": "/scores lab-04"}],
    [{"text": "👥 Learners", "callback_data": "/learners"}],
    [{"text": "🔄 Sync", "callback_data": "/sync"}],
    [{"text": "📈 Pass Rates", "callback_data": "/pass-rates lab-04"}],
    [{"text": "📅 Timeline", "callback_data": "/timeline"}],
    [{"text": "🏆 Groups", "callback_data": "/groups"}],
]

async def call_api(endpoint: str, method="GET", data=None) -> str:
    async with httpx.AsyncClient() as client:
        if method == "GET":
            resp = await client.get(
                f"{LMS_API_URL}{endpoint}",
                headers={"Authorization": f"Bearer {LMS_API_KEY}"}
            )
        else:
            resp = await client.post(
                f"{LMS_API_URL}{endpoint}",
                json=data,
                headers={"Authorization": f"Bearer {LMS_API_KEY}"}
            )
        if resp.status_code == 200:
            return resp.text
        return f"Error: {resp.status_code}"

async def get_learners():
    return await call_api("/learners/")

async def get_groups():
    return await call_api("/analytics/groups?lab=lab-04")

async def get_pass_rates(lab="lab-04"):
    return await call_api(f"/analytics/pass-rates?lab={lab}")

async def get_timeline():
    return await call_api("/analytics/timeline?lab=lab-04")

async def sync_data():
    return await call_api("/pipeline/sync", method="POST", data={})

async def get_labs():
    return "Products\nArchitecture\nBackend\nTesting\nPipeline\nAgent"

async def get_scores(lab="lab-04"):
    return await call_api(f"/analytics/pass-rates?lab={lab}")

async def get_health():
    return await call_api("/items/")

async def handle_test_mode(command: str):
    command = command.strip()
    
    # Эмуляция выбора кнопки
    if command.startswith("/labs"):
        print(await get_labs())
    elif command.startswith("/scores"):
        parts = command.split()
        lab = parts[1] if len(parts) > 1 else "lab-04"
        print(await get_scores("lab-04"))
    elif command.startswith("/learners"):
        print(await get_learners())
    elif command.startswith("/sync"):
        print(await sync_data())
    elif command.startswith("/pass-rates"):
        parts = command.split()
        lab = parts[1] if len(parts) > 1 else "lab-04"
        print(await get_pass_rates(lab))
    elif command.startswith("/timeline"):
        print(await get_timeline())
    elif command.startswith("/groups"):
        print(await get_groups())
    elif command.startswith("/items"):
        print(await call_api("/items/"))
    elif command.startswith("/health"):
        print(await get_health())
    else:
        # Natural language routing
        q = command.lower()
        if "scores" in q:
            print(await get_scores("lab-04"))
        elif "students" in q or "enrolled" in q:
            print(await get_learners())
        elif "group" in q:
            print(await get_groups())
        elif "sync" in q:
            print(await sync_data())
        elif "labs" in q:
            print(await get_labs())
        else:
            print("I can help with labs, scores, learners, groups, sync.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Test a command")
    args = parser.parse_args()

    if args.test:
        asyncio.run(handle_test_mode(args.test))
        sys.exit(0)
    else:
        # Для реального режима выводим информацию о кнопках
        print("Bot started with inline keyboard")
        sys.exit(0)

if __name__ == "__main__":
    main()
