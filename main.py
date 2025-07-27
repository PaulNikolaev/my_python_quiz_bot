import asyncio
import os
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from aiogram.filters import Command


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Токен бота не найден. Установите переменную окружения BOT_TOKEN.")

# Инициализируем бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


if not BOT_TOKEN:
    raise ValueError("Токен бота не найден. Установите переменную окружения BOT_TOKEN.")

# Инициализируем бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Главная функция для запуска бота
async def main():
    # Запускаем поллинг (получение обновлений)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())