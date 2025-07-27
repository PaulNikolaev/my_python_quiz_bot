from aiogram import Router, types
from aiogram.filters import Command
from database.db import get_top_scores
from datetime import datetime

router = Router()


@router.message(Command("stats"))
async def show_stats(message: types.Message):
    """
    Обработчик для команды /stats, который выводит статистику игроков.
    """
    top_players = await get_top_scores()

    if not top_players:
        await message.answer("Пока никто не прошёл квиз. Статистика пуста.")
        return

    # Формируем сообщение со статистикой
    stats_message = "**🏆 Топ-5 игроков:**\n\n"
    for i, player in enumerate(top_players):
        timestamp_obj = datetime.fromisoformat(player['timestamp'])
        formatted_timestamp = timestamp_obj.strftime("%d.%m.%Y в %H:%M")
        stats_message += (
            f"**{i + 1}.** Игрок: `{player['user_id']}`\n"
            f"   - Результат: **{player['score']}** из **{player['total_questions']}**\n"
            f"   - Дата: {formatted_timestamp}\n\n"
        )

    await message.answer(stats_message, parse_mode="Markdown")
