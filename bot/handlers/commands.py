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

def start() -> str:
    return "Welcome to LMS Bot! Use /help to see available commands."

def help_cmd() -> str:
    return "/start - Welcome\n/help - This message\n/health - Backend status\n/labs - List labs\n/scores <lab> - Show scores for a lab"

async def health() -> str:
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{LMS_API_URL}/items/", headers={"Authorization": f"Bearer {LMS_API_KEY}"})
            if resp.status_code == 200:
                return f"Backend OK (status {resp.status_code})"
            else:
                return f"Backend returned {resp.status_code}"
    except Exception as e:
        return f"Backend error: {e}"

async def labs() -> str:
    items = await get_items()
    labs_list = [item['title'] for item in items if item['type'] == 'lab']
    if not labs_list:
        return "No labs found"
    return "\n".join(labs_list)

async def scores(lab_id: str) -> str:
    """Get scores for tasks in a lab."""
    items = await get_items()
    lab = next((item for item in items if item['type'] == 'lab' and lab_id.replace('-', ' ') in item['title'].lower()), None) 

    if not lab:
        return f"Lab '{lab_id}' not found"
    
    tasks = [item for item in items if item.get('parent_id') == lab['id'] and item['type'] == 'task']
    if not tasks:
        return f"No tasks found for lab '{lab_id}'"
    
    result = []
    for task in tasks:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{LMS_API_URL}/analytics/pass-rates?lab={lab_id}",
                headers={"Authorization": f"Bearer {LMS_API_KEY}"}
            )
            if resp.status_code == 200:
                data = resp.json()
                for item in data:
                    if item['task'] == task['title']:
                        result.append(f"{task['title']}: {item['avg_score']}% ({item['attempts']} attempts)")
                        break
                else:
                    result.append(f"{task['title']}: no data")
            else:
                result.append(f"{task['title']}: error fetching data")
    
    return "\n".join(result) if result else f"No score data for lab '{lab_id}'"
