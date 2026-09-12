import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from handlers.answer import router as router_answer
from handlers.keyboard import router as router_keyboard

load_dotenv()
TOKEN = (getenv("TOKEN"))

dp = Dispatcher()
dp.include_router(router_answer)
dp.include_router(router_keyboard)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, stream=sys.stdout)
    asyncio.run(main())