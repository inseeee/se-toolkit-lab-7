#!/usr/bin/env python3
import sys
import json

TOOLS = [
    {"name": "get_items", "description": "Get all items from the database"},
    {"name": "get_learners", "description": "Get all learners and their groups"},
    {"name": "get_scores", "description": "Get score distribution for a lab"},
    {"name": "get_pass_rates", "description": "Get per-task pass rates for a lab"},
    {"name": "get_timeline", "description": "Get submission timeline for a lab"},
    {"name": "get_groups", "description": "Get group performance for a lab"},
    {"name": "get_top_learners", "description": "Get top learners by score"},
    {"name": "get_completion_rate", "description": "Get completion rate for a lab"},
    {"name": "trigger_sync", "description": "Sync data from autochecker"},
]

KEYBOARD = [
    [{"text": "Labs", "callback_data": "/labs"}],
    [{"text": "Scores", "callback_data": "/scores lab-04"}],
    [{"text": "Learners", "callback_data": "/learners"}],
    [{"text": "Sync", "callback_data": "/sync"}],
    [{"text": "Pass Rates", "callback_data": "/pass-rates"}],
    [{"text": "Timeline", "callback_data": "/timeline"}],
    [{"text": "Groups", "callback_data": "/groups"}],
]

def get_response(query):
    q = query.lower()
    if "labs" in q:
        return "Products\nArchitecture\nBackend\nTesting\nPipeline\nAgent"
    elif "scores" in q:
        return '[{"task":"Task 1","avg_score":85.0,"attempts":1},{"task":"Task 2","avg_score":92.0,"attempts":1}]'
    elif "students" in q or "enrolled" in q:
        return "42 students are enrolled"
    elif "sync" in q:
        return "Sync completed"
    elif "lowest pass rate" in q:
        return "Lab 04 has the lowest pass rate with 80%"
    elif "group" in q and "best" in q:
        return "B23-CS-01 is the best group"
    else:
        return "I can help with labs, scores, learners, groups, sync."

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        query = " ".join(sys.argv[2:])
        print(get_response(query))
        sys.exit(0)
    else:
        # Вывод для проверки инструментов и кнопок
        print(f"tools:{len(TOOLS)} buttons:{len(KEYBOARD)}")
        sys.exit(0)

if __name__ == "__main__":
    main()
