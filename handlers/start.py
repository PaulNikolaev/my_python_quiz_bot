from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """
    Этот обработчик срабатывает на команду /start.
    """
    await message.answer(
        "Привет! Я — бот для квизов по Python. Готов проверить свои знания? "
        "Напиши /quiz, чтобы начать."
    )