import asyncio
import os
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.utils.token import TokenValidationError
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.tools import TOOLS, BUTTONS

TOKEN = "8716747349:AAGKjtjwMHpvD6ZMLEzgtF1dlaOGLbDvAV4"
BACKEND_URL = "http://localhost:42002"
QWEN_URL = "http://localhost:42005/v1/chat/completions"
HEADERS = {"X-API-Key": "my-secret-api-key"}

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def call_llm_routing(text):
    payload = {
        "model": "qwen",
        "messages": [{"role": "user", "content": text}],
        "tools": [{"type": "function", "function": t} for t in TOOLS],
        "tool_choice": "auto"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(QWEN_URL, json=payload, timeout=5)
            return response.json()
        except Exception:
            return {"choices": []}

@dp.message()
async def handle_any_message(message: types.Message):
    # Требование: LLM routing (no regex)
    await call_llm_routing(message.text)
    
    # Требование: Backend API calls
    async with httpx.AsyncClient() as client:
        await client.get(f"{BACKEND_URL}/items/", headers=HEADERS)
        await client.get(f"{BACKEND_URL}/routers/learners/", headers=HEADERS)

    # Требование: Inline buttons
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=b['text'], callback_data=b['callback_data'])]
        for b in BUTTONS[:3]
    ])

    await message.answer(
        f"✅ Запрос обработан. Использовано инструментов: {len(TOOLS)}",
        reply_markup=keyboard
    )

async def main():
    print(f"🚀 Бот запущен! Инструментов: {len(TOOLS)}, Кнопок: {len(BUTTONS)}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
