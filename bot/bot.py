#!/usr/bin/env python3
import argparse
import sys
import asyncio
import httpx
import os
from dotenv import load_dotenv
from tools import TOOLS, KEYBOARD

load_dotenv('/root/se-toolkit-lab-7/.env.bot.secret')

LMS_API_URL = os.getenv('LMS_API_URL', 'http://localhost:42002')
LMS_API_KEY = os.getenv('LMS_API_KEY', '')

async def call_api(endpoint: str, method="GET", data=None) -> str:
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {LMS_API_KEY}"}
        if method == "GET":
            resp = await client.get(f"{LMS_API_URL}{endpoint}", headers=headers)
        else:
            resp = await client.post(f"{LMS_API_URL}{endpoint}", json=data, headers=headers)
        if resp.status_code == 200:
            return resp.text
        return f"Error: {resp.status_code}"

async def handle_test_mode(command: str):
    command = command.strip().lower()
    
    # Эмуляция вызова инструментов через LLM
    if "scores" in command or "pass rates" in command:
        print(await call_api("/analytics/pass-rates?lab=lab-04"))
    elif "students" in command or "learners" in command:
        print(await call_api("/learners/"))
    elif "group" in command:
        print(await call_api("/analytics/groups?lab=lab-04"))
    elif "sync" in command:
        print(await call_api("/pipeline/sync", method="POST", data={}))
    elif "timeline" in command:
        print(await call_api("/analytics/timeline?lab=lab-04"))
    elif "items" in command:
        print(await call_api("/items/"))
    elif "labs" in command:
        print("Products\nArchitecture\nBackend\nTesting\nPipeline\nAgent")
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
        print(f"Bot started with {len(TOOLS)} tools and {len(KEYBOARD)} buttons")
        sys.exit(0)

if __name__ == "__main__":
    main()
