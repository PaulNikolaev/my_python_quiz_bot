from aiogram import Router, types
from aiogram.filters import Command
from database.db import get_top_scores, get_user_latest_result
from datetime import datetime

router = Router()


@router.message(Command("stats"))
async def show_stats(message: types.Message):
    """
    Обработчик для команды /stats, который выводит статистику игроков.
    """
    # Получаем топ-5 игроков
    top_players = await get_top_scores(limit=5)
    # Получаем последний результат текущего пользователя
    user_result = await get_user_latest_result(message.from_user.id)

    # Формируем сообщение для топа игроков
    stats_message = "**🏆 Топ-5 игроков:**\n\n"
    if not top_players:
        stats_message += "Пока никто не прошёл квиз. Статистика пуста.\n\n"
    else:
        for i, player in enumerate(top_players):
            timestamp_obj = datetime.fromisoformat(player['timestamp'])
            formatted_timestamp = timestamp_obj.strftime("%H:%M %d.%m.%Y")

            stats_message += (
                f"**{i + 1}.** Игрок: `{player['user_id']}`\n"
                f"   - Результат: **{player['score']}** из **{player['total_questions']}**\n"
                f"   - Дата: {formatted_timestamp}\n\n"
            )

    stats_message += "---\n\n"

    # Персональный результат пользователя
    if user_result:
        timestamp_obj = datetime.fromisoformat(user_result['timestamp'])
        formatted_timestamp = timestamp_obj.strftime("%H:%M %d.%m.%Y")
        stats_message += (
            f"**Твой последний результат:**\n"
            f"   - **{user_result['score']}** из **{user_result['total_questions']}**\n"
            f"   - Дата: {formatted_timestamp}"
        )
    else:
        stats_message += "Ты ещё не прошёл ни одного квиза. Запусти /quiz, чтобы начать!"

    await message.answer(stats_message, parse_mode="Markdown")
