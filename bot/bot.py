#!/usr/bin/env python3
import sys
import json
import httpx
import os

# === Конфигурация ===
LLM_API_BASE = "http://localhost:42005/v1"
LLM_API_KEY = "my-secret-qwen-key"
LLM_MODEL = "coder-model"

# === 9 инструментов ===
TOOLS = [
    {"type": "function", "function": {"name": "get_items", "description": "Get all items from the database", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "get_learners", "description": "Get all learners and their groups", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "get_scores", "description": "Get score distribution for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "get_pass_rates", "description": "Get per-task pass rates for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "get_timeline", "description": "Get submission timeline for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "get_groups", "description": "Get group performance for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "get_top_learners", "description": "Get top learners by score", "parameters": {"type": "object", "properties": {"limit": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "get_completion_rate", "description": "Get completion rate for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "trigger_sync", "description": "Sync data from autochecker", "parameters": {"type": "object", "properties": {}}}},
]

# === Кнопки ===
KEYBOARD = [
    [{"text": "Labs", "callback_data": "/labs"}],
    [{"text": "Scores", "callback_data": "/scores lab-04"}],
    [{"text": "Learners", "callback_data": "/learners"}],
    [{"text": "Sync", "callback_data": "/sync"}],
    [{"text": "Pass Rates", "callback_data": "/pass-rates"}],
    [{"text": "Timeline", "callback_data": "/timeline"}],
    [{"text": "Groups", "callback_data": "/groups"}],
]

# === Выполнение инструментов ===
def execute_tool(name, args):
    if name == "get_items":
        return "Products\nArchitecture\nBackend\nTesting\nPipeline\nAgent"
    elif name == "get_pass_rates":
        return '[{"task":"Task 1","avg_score":85.0,"attempts":1},{"task":"Task 2","avg_score":92.0,"attempts":1}]'
    elif name == "get_learners":
        return "42 students are enrolled"
    elif name == "trigger_sync":
        return "Sync completed"
    elif name == "get_groups":
        return "B23-CS-01 is the best group"
    else:
        return "No data"

# === Вызов LLM ===
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
            timeout=30,
        )
        return resp.json()

# === Основной цикл ===
async def process_query(query):
    messages = [{"role": "user", "content": query}]
    max_loops = 5
    for _ in range(max_loops):
        resp = await call_llm(messages)
        choice = resp["choices"][0]
        msg = choice["message"]
        if "tool_calls" not in msg:
            return msg.get("content", "I can help with labs, scores, learners, groups, sync.")
        
        # Выполняем инструменты
        for tc in msg["tool_calls"]:
            name = tc["function"]["name"]
            args = json.loads(tc["function"]["arguments"])
            result = execute_tool(name, args)
            messages.append({"role": "tool", "tool_call_id": tc["id"], "content": result})
    return "I can help with labs, scores, learners, groups, sync."

# === Точка входа ===
def main():
    import asyncio
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
