#!/usr/bin/env python3
import sys
import json
import httpx
import asyncio

LLM_API_BASE = "http://localhost:42005/v1"
LLM_API_KEY = "my-secret-qwen-key"
LLM_MODEL = "coder-model"
BACKEND_URL = "http://localhost:42002"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "List of labs and tasks",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Enrolled students and groups",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores",
            "description": "Score distribution for a lab",
            "parameters": {
                "type": "object",
                "properties": {"lab": {"type": "string"}},
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Per-task averages and attempts",
            "parameters": {
                "type": "object",
                "properties": {"lab": {"type": "string"}},
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Submissions per day",
            "parameters": {
                "type": "object",
                "properties": {"lab": {"type": "string"}},
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Group performance and size",
            "parameters": {
                "type": "object",
                "properties": {"lab": {"type": "string"}},
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_learners",
            "description": "Top N learners",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string"},
                    "limit": {"type": "integer"}
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_completion_rate",
            "description": "Completion rate for lab",
            "parameters": {
                "type": "object",
                "properties": {"lab": {"type": "string"}},
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_sync",
            "description": "Refresh data",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

KEYBOARD = [
    [{"text": "What labs are available?", "callback_data": "what labs are available"}],
    [{"text": "Show me scores for lab 04", "callback_data": "show me scores for lab 04"}],
    [{"text": "Top 5 students", "callback_data": "top 5 students"}],
    [{"text": "Lowest pass rate", "callback_data": "which lab has the lowest pass rate"}],
    [{"text": "How many students are enrolled?", "callback_data": "how many students are enrolled"}],
    [{"text": "Sync data", "callback_data": "sync the data"}],
    [{"text": "Which group is best?", "callback_data": "which group is doing best in lab 04"}],
]

async def call_backend(name, args):
    async with httpx.AsyncClient() as client:
        if name == "get_items":
            resp = await client.get(f"{BACKEND_URL}/items/")
            return resp.json()
        elif name == "get_learners":
            resp = await client.get(f"{BACKEND_URL}/learners/")
            return resp.json()
        elif name == "get_scores":
            resp = await client.get(f"{BACKEND_URL}/analytics/scores", params=args)
            return resp.json()
        elif name == "get_pass_rates":
            resp = await client.get(f"{BACKEND_URL}/analytics/pass-rates", params=args)
            return resp.json()
        elif name == "get_timeline":
            resp = await client.get(f"{BACKEND_URL}/analytics/timeline", params=args)
            return resp.json()
        elif name == "get_groups":
            resp = await client.get(f"{BACKEND_URL}/analytics/groups", params=args)
            return resp.json()
        elif name == "get_top_learners":
            resp = await client.get(f"{BACKEND_URL}/analytics/top-learners", params=args)
            return resp.json()
        elif name == "get_completion_rate":
            resp = await client.get(f"{BACKEND_URL}/analytics/completion-rate", params=args)
            return resp.json()
        elif name == "trigger_sync":
            resp = await client.post(f"{BACKEND_URL}/pipeline/sync")
            return resp.json()
        else:
            return {"error": "Unknown tool"}

async def call_llm(messages):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{LLM_API_BASE}/chat/completions",
            headers={"Authorization": f"Bearer {LLM_API_KEY}"},
            json={
                "model": LLM_MODEL,
                "messages": messages,
                "tools": TOOLS,
                "tool_choice": "auto",
            },
            timeout=60,
        )
        return resp.json()

async def process_query(user_input):
    messages = [
        {"role": "system", "content": (
            "You are a strict API assistant. "
            "You MUST use tools to answer ALL data-related questions. "
            "Do NOT answer from knowledge. Always call tools first."
        )},
        {"role": "user", "content": user_input},
    ]

    for _ in range(10):
        resp = await call_llm(messages)

        if "choices" not in resp:
            return f"LLM error: {resp}"

        msg = resp["choices"][0]["message"]

        tool_calls = msg.get("tool_calls", [])

        if not tool_calls:
            content = msg.get("content")
            if content:
                return content
            return "I couldn't process that request."

        messages.append(msg)

        for tc in tool_calls:
            name = tc["function"]["name"]
            args = json.loads(tc["function"]["arguments"])

            print(f"[tool] LLM called: {name}({args})", file=sys.stderr)

            result = await call_backend(name, args)

            print(f"[tool] Result: {str(result)[:100]}", file=sys.stderr)

            messages.append({
                "role": "tool",
                "tool_call_id": tc["id"],
                "content": json.dumps(result),
            })

        print("[summary] Feeding tool results back to LLM", file=sys.stderr)

    return "I couldn't process that request. Try asking about labs, scores, or learners."

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        query = " ".join(sys.argv[2:])
        answer = asyncio.run(process_query(query))
        print(answer)
        sys.exit(0)
    else:
        print(f"tools:{len(TOOLS)} buttons:{len(KEYBOARD)}")
        sys.exit(0)

if __name__ == "__main__":
    main()
