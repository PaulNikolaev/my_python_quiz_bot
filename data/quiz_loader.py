import json
import os

QUIZ_FILE_PATH = os.path.join(os.path.dirname(__file__), 'quiz_questions.json')

def load_quiz_questions():
    """
    Загружает вопросы для квиза из JSON-файла.
    """
    try:
        with open(QUIZ_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: файл {QUIZ_FILE_PATH} не найден. Убедитесь, что он существует.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: некорректный формат JSON в файле {QUIZ_FILE_PATH}.")
        return []