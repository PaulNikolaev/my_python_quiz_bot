import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from database.db import create_table

from handlers.start import router as start_router
from handlers.quiz import router as quiz_router


async def main():
    load_dotenv()

    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    await create_table()

    dp.include_router(start_router)
    dp.include_router(quiz_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
