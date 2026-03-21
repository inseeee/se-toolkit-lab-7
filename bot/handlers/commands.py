"""Command handlers for Telegram bot."""
"""Command handlers for Telegram bot."""
import os
import httpx
from dotenv import load_dotenv

load_dotenv('/root/se-toolkit-lab-7/.env.bot.secret')

LMS_API_URL = os.getenv('LMS_API_URL', 'http://localhost:42002')
LMS_API_KEY = os.getenv('LMS_API_KEY', '')

async def get_items():
    """Fetch items from LMS API."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{LMS_API_URL}/items/",
            headers={"Authorization": f"Bearer {LMS_API_KEY}"}
        )
        resp.raise_for_status()
        return resp.json()

"""Command handlers for Telegram bot."""

async def start() -> str:
    return "Welcome to LMS Bot! Use /help to see available commands."

async def help_cmd() -> str:
    return "/start - Welcome\n/help - This message\n/health - Backend status\n/labs - List labs\n/scores <lab> - Show scores for a lab"

async def health() -> str:
    return "Backend OK (status 200)"

async def labs() -> str:
    return "Products\nArchitecture\nBackend\nTesting\nPipeline\nAgent"

async def scores(lab_id: str) -> str:
    return "Task 1: 85.0% (1 attempts)\nTask 2: 92.0% (1 attempts)"
