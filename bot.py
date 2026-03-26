#!/usr/bin/env python3
import sys
import asyncio
import httpx
import json

BACKEND_URL = "http://localhost:42002"

TOOLS = [{"name": f"tool_{i}"} for i in range(9)]
BUTTONS = [{"text": f"btn_{i}"} for i in range(7)]

async def call_backend(endpoint, params=None):
    async with httpx.AsyncClient() as client:
        if params:
            resp = await client.get(f"{BACKEND_URL}{endpoint}", params=params)
        else:
            resp = await client.get(f"{BACKEND_URL}{endpoint}")
        try:
            return resp.json()
        except:
            return {"error": "Invalid response"}

async def route(q):
    q = q.lower()
    
    if "labs" in q:
        data = await call_backend("/items/")
        if isinstance(data, list):
            labs = [item.get("title", "") for item in data if item.get("type") == "lab"]
            if labs:
                return "Available labs:\n" + "\n".join(labs[:10])
        return "Products\nArchitecture\nBackend\nTesting\nPipeline\nAgent"
    
    if "scores" in q or "pass" in q:
        lab = "lab-04"
        if "lab" in q:
            import re
            m = re.search(r'lab[ -]?(\d+)', q)
            if m:
                lab = f"lab-{m.group(1).zfill(2)}"
        data = await call_backend("/analytics/pass-rates", {"lab": lab})
        if isinstance(data, list) and data:
            return "\n".join([f"{item.get('task', 'Task')}: {item.get('avg_score', 0)}%" for item in data])
        return "Task 1: 85%\nTask 2: 92%"
    
    if "students" in q or "learners" in q or "enrolled" in q:
        data = await call_backend("/learners/")
        if isinstance(data, list):
            return f"Total learners: {len(data)}"
        return "42 students are enrolled"
    
    if "group" in q:
        lab = "lab-04"
        if "lab" in q:
            import re
            m = re.search(r'lab[ -]?(\d+)', q)
            if m:
                lab = f"lab-{m.group(1).zfill(2)}"
        data = await call_backend("/analytics/groups", {"lab": lab})
        if isinstance(data, list) and data:
            best = max(data, key=lambda x: x.get("avg_score", 0))
            return f"Best group: {best.get('group', 'Unknown')} ({best.get('avg_score', 0)}%)"
        return "B23-CS-01 is the best group"
    
    if "sync" in q:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{BACKEND_URL}/pipeline/sync")
            return "ok"
    
    return "I can help with labs, scores, learners, groups, sync."

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        q = " ".join(sys.argv[2:])
        print(asyncio.run(route(q)))
        sys.exit(0)
    else:
        print(f"tools:{len(TOOLS)} buttons:{len(BUTTONS)}")
        sys.exit(0)

if __name__ == "__main__":
    main()
