from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()

@router.message(CommandStart())
async def cmd_start_with_button(message: types.Message):
    """
    Обработчик команды /start с кнопкой "Начать игру".
    """
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))

    await message.answer(
        "Добро пожаловать в квиз по Python! Нажмите 'Начать игру', чтобы проверить свои знания.",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )