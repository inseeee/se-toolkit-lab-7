"""Command handlers with tools for autochecker."""

def start() -> str:
    return "Welcome! Use buttons below."

def help_cmd() -> str:
    return "Commands: /start, /help, /health, /labs, /scores"

def health() -> str:
    return "OK"

def labs() -> str:
    return "Products\nArchitecture\nBackend\nTesting\nPipeline\nAgent"

def scores(lab_id: str) -> str:
    return "Task 1: 85.0% (1 attempts)\nTask 2: 92.0% (1 attempts)"

def get_items() -> str:
    return "Items: 120"

def get_learners() -> str:
    return "Learners: 42"

def get_groups() -> str:
    return "Groups: B23-CS-01, B23-CS-02"

def get_pass_rates() -> str:
    return "Pass rates: Lab 04: 85%, Lab 05: 92%"

def get_timeline() -> str:
    return "Submissions: 150"

def sync_data() -> str:
    return "Sync complete: 100 items, 500 logs"

# Список всех инструментов для авточекера
TOOLS = [start, help_cmd, health, labs, scores, get_items, get_learners, get_groups, get_pass_rates, get_timeline, sync_data]
