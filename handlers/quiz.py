import json
from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery

from database.db import get_quiz_state, update_quiz_state
from data.quiz_loader import load_quiz_questions

# Загрузка вопросов
QUIZ_QUESTIONS = load_quiz_questions()

router = Router()


# Функция для генерации Inline-кнопок с вариантами ответов
def generate_options_keyboard(question_index: int, options: list[str]) -> InlineKeyboardBuilder:
    """Генерирует клавиатуру с вариантами ответов для текущего вопроса."""
    builder = InlineKeyboardBuilder()
    for i, option in enumerate(options):
        # Callback-данные будут содержать индекс вопроса и индекс выбранного ответа
        callback_data = f"quiz_{question_index}_{i}"
        builder.add(types.InlineKeyboardButton(text=option, callback_data=callback_data))

    # Кнопки выводим по одной в столбик
    builder.adjust(1)
    return builder.as_markup()


# Функция для отправки вопроса
async def send_question(bot: Bot, chat_id: int, user_id: int, question_index: int):
    """Отправляет вопрос и кнопки с вариантами ответов."""
    if question_index >= len(QUIZ_QUESTIONS):
        # Если вопросов больше нет, завершаем квиз
        state = await get_quiz_state(user_id)
        await bot.send_message(
            chat_id=chat_id,
            text=f"Поздравляю! Вы ответили на все вопросы. 🎉\n"
                 f"Ваш финальный результат: **{state['score']}** из **{len(QUIZ_QUESTIONS)}**.",
            parse_mode="Markdown"
        )
        return

    question_data = QUIZ_QUESTIONS[question_index]
    options = question_data['options']

    # Генерируем клавиатуру
    kb = generate_options_keyboard(question_index, options)

    # Отправляем сообщение с вопросом и прикрепленной клавиатурой
    await bot.send_message(
        chat_id=chat_id,
        text=f"**Вопрос {question_index + 1} из {len(QUIZ_QUESTIONS)}:**\n{question_data['question']}",
        reply_markup=kb,
        parse_mode="Markdown"
    )


# --- Обработчики команд и кнопок ---

@router.message(F.text == "Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message, bot: Bot):
    """
    Обработчик, который запускает квиз, сбрасывает прогресс и отправляет первый вопрос.
    """
    if not QUIZ_QUESTIONS:
        await message.answer("Извините, сейчас нет доступных вопросов для квиза.")
        return

    user_id = message.from_user.id

    # Сбрасываем прогресс пользователя: индекс вопроса 0, счет 0
    await update_quiz_state(user_id, question_index=0, score=0)

    # Отправляем первое сообщение и убираем клавиатуру с кнопкой "Начать игру"
    await message.answer(
        "Давайте начнем квиз! Удачи!",
        reply_markup=types.ReplyKeyboardRemove()
    )

    # Отправляем первый вопрос
    await send_question(bot, message.chat.id, user_id, 0)


@router.callback_query(lambda c: c.data.startswith("quiz_"))
async def process_quiz_answer(callback_query: CallbackQuery, bot: Bot):
    """
    Обработчик нажатий на Inline-кнопки с вариантами ответов.
    """
    user_id = callback_query.from_user.id

    # Получаем текущее состояние квиза из БД
    state = await get_quiz_state(user_id)
    if not state:
        await callback_query.answer()
        return

    current_question_index = state['question_index']
    current_score = state['score']

    parts = callback_query.data.split('_')
    user_answer_index = int(parts[2])

    question_data = QUIZ_QUESTIONS[current_question_index]
    correct_answer_index = question_data["correct_option_index"]

    # Отключаем кнопки после выбора ответа
    await callback_query.message.edit_reply_markup(reply_markup=None)

    # Проверяем ответ
    if user_answer_index == correct_answer_index:
        await callback_query.answer()
        new_score = current_score + 1
        await callback_query.message.answer("✅ **Правильный ответ!**", parse_mode="Markdown")
        await update_quiz_state(user_id, current_question_index + 1, new_score)
    else:
        await callback_query.answer()
        correct_answer_text = question_data['options'][correct_answer_index]
        await callback_query.message.answer(
            f"❌ **Неправильно.**\nПравильный ответ: `{correct_answer_text}`",
            parse_mode="Markdown"
        )
        await update_quiz_state(user_id, current_question_index + 1, current_score)

    # Переходим к следующему вопросу
    next_question_index = current_question_index + 1
    await send_question(bot, callback_query.message.chat.id, user_id, next_question_index)
