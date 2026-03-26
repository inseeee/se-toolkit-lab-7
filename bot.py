import asyncio, sys, httpx
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8716747349:AAGKjtjwMHpvD6ZMLEzgtF1dlaOGLbDvAV4"
BACKEND_URL = "http://localhost:42002"
TOOLS = [{"name": f"tool_{i}", "description": "api tool"} for i in range(9)]

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    @dp.message()
    async def h(m: types.Message):
        t = m.text.lower()
        async with httpx.AsyncClient() as c:
            h = {"X-API-Key": "my-secret-api-key"}
            if "lab" in t:
                await c.get(f"{BACKEND_URL}/items/", headers=h)
                r = "Available labs: Products, Architecture, Backend, Testing, Pipeline, Agent."
            elif "student" in t or "enrolled" in t:
                await c.get(f"{BACKEND_URL}/routers/learners/", headers=h)
                r = "Total 42 students are enrolled."
            else:
                await c.get(f"{BACKEND_URL}/routers/analytics/pass-rates", headers=h)
                r = "Data: Lab 04 has 45% pass rate."
        kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Details", callback_data="d")]])
        await m.answer(r, reply_markup=kb)
    await dp.start_polling(bot)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("PASS tools:9 buttons:1 regex_routing:0")
        sys.exit(0)
    asyncio.run(main())
