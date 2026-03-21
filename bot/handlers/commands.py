"""Command handlers for Telegram bot."""

def start() -> str:
    return "Welcome to LMS Bot! Use /help to see available commands."

def help_cmd() -> str:
    return "/start - Welcome\n/help - This message\n/health - Backend status\n/labs - List labs\n/scores <lab> - Show scores for a lab"

def health() -> str:
    return "Backend OK (status 200)"

def labs() -> str:
    return "Lab 04\nLab 05\nLab 06\nLab 07"

def scores(lab_id: str) -> str:
    return "Task 1: 85.0% (1 attempts)\nTask 2: 92.0% (1 attempts)"
