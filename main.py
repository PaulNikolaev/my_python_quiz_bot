import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

# Импортируем наши обработчики
from handlers import start


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    # Регистрируем роутеры с обработчиками
    dp.include_router(start.router)
    #dp.include_router(quiz.router)

    # Запускаем поллинг
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())