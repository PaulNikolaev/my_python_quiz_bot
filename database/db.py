import aiosqlite

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
