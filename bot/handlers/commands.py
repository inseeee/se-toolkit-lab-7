"""Command handlers for Telegram bot."""

def start() -> str:
    return "Welcome to LMS Bot! Use /help to see available commands."

def help_cmd() -> str:
    return "/start - Welcome\n/help - This message\n/health - Backend status\n/labs - List labs"

def health() -> str:
    return "Backend is healthy (placeholder)"

def labs() -> str:
    return "Available labs: lab-04, lab-05, lab-06"
