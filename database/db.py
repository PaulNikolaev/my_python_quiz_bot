import aiosqlite
import datetime

DB_NAME = "quiz_bot.db"


async def create_table():
    """
    Инициализация базы данных, сли она еще не существует
    """
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_state (
                user_id INTEGER PRIMARY KEY,
                question_index INTEGER DEFAULT 0,
                score INTEGER DEFAULT 0
            )
        ''')

        # Таблица для результатов
        await db.execute('''
                    CREATE TABLE IF NOT EXISTS quiz_results (
                        user_id INTEGER PRIMARY KEY,
                        score INTEGER,
                        total_questions INTEGER,
                        timestamp TEXT
                    )
                ''')
        await db.commit()


async def update_quiz_state(user_id: int, question_index: int, score: int):
    """
    Вставляет или обновляет состояние квиза для пользователя.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT OR REPLACE INTO quiz_state (user_id, question_index, score) VALUES (?, ?, ?)',
            (user_id, question_index, score)
        )
        await db.commit()


async def get_quiz_state(user_id: int):
    """
    Получает текущее состояние квиза для заданного пользователя.
    Возвращает словарь с данными или None, если пользователь не найден.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute('SELECT * FROM quiz_state WHERE user_id = ?', (user_id,))
        results = await cursor.fetchone()

        return dict(results) if results else None


async def save_quiz_result(user_id: int, score: int, total_questions: int):
    """
    Сохраняет или обновляет последний результат квиза для пользователя.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT OR REPLACE INTO quiz_results (user_id, score, total_questions, timestamp) VALUES (?, ?, ?, ?)',
            (user_id, score, total_questions, datetime.datetime.now().isoformat())
        )
        await db.commit()


async def get_top_scores():
    """
    Возвращает 5 лучших результатов всех игроков.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            'SELECT user_id, score, total_questions, timestamp FROM quiz_results ORDER BY score DESC LIMIT 5'
        )
        return await cursor.fetchall()
