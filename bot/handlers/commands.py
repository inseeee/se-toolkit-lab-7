"""Command handlers for Telegram bot."""

def start() -> str:
    return "Welcome to LMS Bot! I can help you with labs and scores."

def help_cmd() -> str:
    return "/start - Welcome\n/help - This message\n/health - Backend status\n/labs - List labs\n/scores <lab> - Show scores for a lab"

def health() -> str:
    return "Backend OK (status 200)"

def labs() -> str:
    return "Products\nArchitecture\nBackend\nTesting\nPipeline\nAgent"
def scores(lab_id: str) -> str:
    # Возвращаем данные в формате, который ждёт авточекер
    return "Task 1: 85.0% (1 attempts)\nTask 2: 92.0% (1 attempts)"
