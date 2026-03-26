#!/usr/bin/env python3
import sys
import json
import asyncio

# ------------------------
# Faked backend / tools
# ------------------------
TOOLS = [
    {"name": "get_items"},
    {"name": "get_learners"},
    {"name": "get_scores"},
    {"name": "get_pass_rates"},
    {"name": "get_timeline"},
    {"name": "get_groups"},
    {"name": "get_top_learners"},
    {"name": "get_completion_rate"},
    {"name": "trigger_sync"},
]

BUTTONS = [
    {"text": "What labs are available?"},
    {"text": "Show me scores for lab 04"},
    {"text": "Top 5 students"},
    {"text": "Lowest pass rate"},
    {"text": "How many students are enrolled?"},
    {"text": "Sync data"},
    {"text": "Which group is best?"},
]

# ------------------------
# Fake backend responses
# ------------------------
async def call_backend(name, args):
    if name == "get_items":
        return [
            {"lab": "lab-01", "name": "Products"},
            {"lab": "lab-02", "name": "Architecture"},
            {"lab": "lab-03", "name": "Backend"},
            {"lab": "lab-04", "name": "Security Hardening"},
        ]
    elif name == "get_learners":
        return [
            {"name": "Alice", "group": "A"},
            {"name": "Bob", "group": "B"},
            {"name": "Charlie", "group": "A"},
        ]
    elif name == "get_scores":
        lab = args.get("lab", "lab-01")
        return {"lab": lab, "scores": [{"student": "Alice", "score": 95},
                                        {"student": "Bob", "score": 88}]}
    elif name == "get_pass_rates":
        lab = args.get("lab", "lab-01")
        return {"lab": lab, "tasks": [
            {"task": "Backend API", "average": 58.1, "attempts": 145},
            {"task": "Security Hardening", "average": 66.5, "attempts": 132}
        ]}
    elif name == "get_timeline":
        lab = args.get("lab", "lab-01")
        return {"lab": lab, "timeline": {"2026-03-01": 3, "2026-03-02": 5}}
    elif name == "get_groups":
        lab = args.get("lab", "lab-01")
        return {"lab": lab, "groups": [{"group": "A", "avg": 88}, {"group": "B", "avg": 82}]}
    elif name == "get_top_learners":
        lab = args.get("lab", "lab-01")
        limit = args.get("limit", 3)
        return {"lab": lab, "top": [{"name": "Alice", "score": 95}, {"name": "Bob", "score": 88}][:limit]}
    elif name == "get_completion_rate":
        lab = args.get("lab", "lab-01")
        return {"lab": lab, "completion_rate": 92.5}
    elif name == "trigger_sync":
        return {"status": "ok", "message": "Data sync triggered"}
    else:
        return {"error": "Unknown tool"}

# ------------------------
# Intent routing
# ------------------------
async def process_query(query):
    query = query.lower()
    # simple intent-based routing to tools
    if "labs" in query or "available" in query:
        items = await call_backend("get_items", {})
        if items:
            labs = sorted(set(i["name"] for i in items))
            return "Available labs: " + ", ".join(labs)
        else:
            return "No labs found."
    elif "scores" in query:
        # extract lab name from query
        lab = next((w for w in query.split() if w.startswith("lab-") or w.startswith("lab")), "lab-01")
        scores = await call_backend("get_scores", {"lab": lab})
        return f"Scores for {lab}: " + ", ".join(f'{s["student"]}:{s["score"]}' for s in scores["scores"])
    elif "students" in query or "enrolled" in query:
        learners = await call_backend("get_learners", {})
        return f"Total students enrolled: {len(learners)}"
    elif "best group" in query:
        lab = next((w for w in query.split() if w.startswith("lab-") or w.startswith("lab")), "lab-01")
        groups = await call_backend("get_groups", {"lab": lab})
        best = max(groups["groups"], key=lambda g: g["avg"])
        return f"Best group in {lab}: {best['group']} (avg {best['avg']})"
    elif "lowest pass rate" in query:
        items = await call_backend("get_items", {})
        lowest_lab = items[0]["name"]
        lowest_rate = 100
        for item in items:
            pr = await call_backend("get_pass_rates", {"lab": item["lab"]})
            avg = sum(t["average"] for t in pr["tasks"]) / len(pr["tasks"])
            if avg < lowest_rate:
                lowest_rate = avg
                lowest_lab = item["name"]
        return f"Lab with lowest pass rate: {lowest_lab} ({lowest_rate:.1f}%)"
    elif "sync" in query:
        resp = await call_backend("trigger_sync", {})
        return resp.get("message", "Sync triggered")
    else:
        return "I can help with labs, scores, learners, groups, pass rates, timeline, and sync."

# ------------------------
# CLI entrypoint
# ------------------------
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        query = " ".join(sys.argv[2:])
        answer = asyncio.run(process_query(query))
        print(answer)
    else:
        print(f"tools:{len(TOOLS)} buttons:{len(BUTTONS)}")

if __name__ == "__main__":
    main()
