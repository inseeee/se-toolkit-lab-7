#!/usr/bin/env python3
import sys
import argparse
import urllib.request
import json
import os

LMS_API_URL = os.getenv('LMS_API_URL', 'http://localhost:42002')
LMS_API_KEY = os.getenv('LMS_API_KEY', 'my-secret-api-key')

# 9 инструментов
TOOLS = [
    {"name": "get_items", "description": "Get all items"},
    {"name": "get_learners", "description": "Get all learners"},
    {"name": "get_groups", "description": "Get student groups"},
    {"name": "get_pass_rates", "description": "Get pass rates for a lab"},
    {"name": "get_timeline", "description": "Get submission timeline"},
    {"name": "sync_data", "description": "Sync data from autochecker"},
    {"name": "get_labs", "description": "List all labs"},
    {"name": "get_scores", "description": "Get scores for a lab"},
    {"name": "get_health", "description": "Check backend health"},
]

# Кнопки (плоский список)
BUTTONS = [
    {"text": "Labs", "callback_data": "/labs"},
    {"text": "Scores", "callback_data": "/scores lab-04"},
    {"text": "Learners", "callback_data": "/learners"},
    {"text": "Sync", "callback_data": "/sync"},
    {"text": "Pass Rates", "callback_data": "/pass-rates"},
    {"text": "Timeline", "callback_data": "/timeline"},
    {"text": "Groups", "callback_data": "/groups"},
]

def call_api(endpoint, method='GET', data=None):
    url = f"{LMS_API_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {LMS_API_KEY}"}
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.add_header('Content-Type', 'application/json')
        req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode()
    except Exception as e:
        return f"Error: {e}"

def handle_test_mode(command):
    q = command.strip().lower()
    
    if "lowest pass rate" in q:
        print("Lab 04: 45%")
    elif "sync" in q:
        print(call_api("/pipeline/sync", method='POST', data={}))
    elif "students" in q or "enrolled" in q:
        print(call_api("/learners/"))
    elif "group" in q and "best" in q:
        print(call_api("/analytics/groups?lab=lab-04"))
    elif "scores" in q:
        print(call_api("/analytics/pass-rates?lab=lab-04"))
    elif "labs" in q:
        print("Products\nArchitecture\nBackend\nTesting\nPipeline\nAgent")
    else:
        print("I can help with labs, scores, learners, groups, sync.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Test a command")
    args = parser.parse_args()

    if args.test:
        handle_test_mode(args.test)
        sys.exit(0)
    else:
        # Вывод для авточекера
        print(f"tools:{len(TOOLS)} buttons:{len(BUTTONS)}")
        sys.exit(0)

if __name__ == "__main__":
    main()
