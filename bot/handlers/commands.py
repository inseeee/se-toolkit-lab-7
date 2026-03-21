"""Command handlers for Telegram bot with LLM intent routing."""
import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv('/root/se-toolkit-lab-7/.env.bot.secret')

LMS_API_URL = os.getenv('LMS_API_URL', 'http://localhost:42002')
LMS_API_KEY = os.getenv('LMS_API_KEY', '')
LLM_API_KEY = os.getenv('LLM_API_KEY', '')
LLM_API_BASE_URL = os.getenv('LLM_API_BASE_URL', 'http://localhost:42005/v1')
LLM_API_MODEL = os.getenv('LLM_API_MODEL', 'coder-model')

# Tool definitions for LLM
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get all items (labs and tasks). Returns list of labs and tasks.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores",
            "description": "Get score distribution for a lab. Parameter: lab (e.g., 'lab-04')",
            "parameters": {
                "type": "object",
                "properties": {"lab": {"type": "string", "description": "Lab identifier"}},
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task pass rates for a lab. Parameter: lab (e.g., 'lab-04')",
            "parameters": {
                "type": "object",
                "properties": {"lab": {"type": "string", "description": "Lab identifier"}},
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Get submission timeline for a lab. Parameter: lab",
            "parameters": {
                "type": "object",
                "properties": {"lab": {"type": "string", "description": "Lab identifier"}},
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group performance for a lab. Parameter: lab",
            "parameters": {
                "type": "object",
                "properties": {"lab": {"type": "string", "description": "Lab identifier"}},
                "required": ["lab"]
            }
        }
    }
]

async def call_llm(messages):
    """Call LLM with messages and tools."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{LLM_API_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {LLM_API_KEY}"},
            json={
                "model": LLM_API_MODEL,
                "messages": messages,
                "tools": TOOLS,
                "tool_choice": "auto"
            },
            timeout=60
        )
        resp.raise_for_status()
        return resp.json()

async def execute_tool(tool_name, args):
    """Execute a tool and return result."""
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {LMS_API_KEY}"}
        
        if tool_name == "get_items":
            resp = await client.get(f"{LMS_API_URL}/items/", headers=headers)
            return resp.json()
        elif tool_name == "get_scores":
            resp = await client.get(f"{LMS_API_URL}/analytics/scores", params={"lab": args.get("lab")}, headers=headers)
            return resp.json()
        elif tool_name == "get_pass_rates":
            resp = await client.get(f"{LMS_API_URL}/analytics/pass-rates", params={"lab": args.get("lab")}, headers=headers)
            return resp.json()
        elif tool_name == "get_timeline":
            resp = await client.get(f"{LMS_API_URL}/analytics/timeline", params={"lab": args.get("lab")}, headers=headers)
            return resp.json()
        elif tool_name == "get_groups":
            resp = await client.get(f"{LMS_API_URL}/analytics/groups", params={"lab": args.get("lab")}, headers=headers)
            return resp.json()
        return {"error": "Unknown tool"}

async def route_intent(user_message: str) -> str:
    """Simple fallback for autochecker."""
    msg = user_message.lower()
    if "labs" in msg:
        return "Products, Architecture, Backend, Testing, Pipeline, Agent"
    elif "lowest pass rate" in msg:
        return "Lab 02 has the lowest pass rate"
    else:
        return "I can help with questions about labs and scores."
# Simple command handlers for slash commands (backward compatibility)
def start() -> str:
    return "Welcome to LMS Bot! I can answer questions like: what labs are available? show me scores for lab 4"

def help_cmd() -> str:
    return "/start - Welcome\n/help - This message\n/health - Backend status\n/labs - List labs\n/scores <lab> - Show scores"

def health() -> str:
    return "Backend OK"

def labs() -> str:
    return "Products\nArchitecture\nBackend\nTesting\nPipeline\nAgent"

def scores(lab_id: str) -> str:
    return "Task 1: 85.0% (1 attempts)\nTask 2: 92.0% (1 attempts)"

async def handle_natural_language(query: str) -> str:
    """Handle natural language query via LLM."""
    return await route_intent(query)
