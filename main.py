# main.py — 100% рабочая версия для aiogram 3.13+
import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import dp  # ← импортируем готовый dp из handlers.py

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Ошибка: BOT_TOKEN не найден в файле .env!")

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    print("Я проектирую своё благополучие — бот запущен и готов к работе!")
    print("Открой Telegram → найди своего бота → нажми /start")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())