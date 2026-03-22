from bot.utils.openrouter import call_agent
from bot.utils.file_loader import read_project_file

MODEL = "anthropic/claude-sonnet-4-6"
TEMPERATURE = 0.5

SYSTEM_PROMPT = """Ты — контент-планер. Работаешь с контент-планом автора.

Умеешь:
- Показывать актуальные темы из плана
- Предлагать следующую тему для публикации
- Добавлять новые темы на основе болей аудитории
- Отмечать опубликованные темы

Аудитория: владельцы малого бизнеса, эксперты-фрилансеры, стартаперы.
Отвечай конкретно. Без лишних слов."""


def run(task: str) -> str:
    plan = read_project_file("content-plan.md")
    audience = read_project_file("audience.md")

    context = f"""
ТЕКУЩИЙ КОНТЕНТ-ПЛАН:
{plan}

БОЛИ И ВОПРОСЫ АУДИТОРИИ (для новых тем):
{audience[:1500] if audience else "Не загружено."}

ЗАДАЧА:
{task}
"""
    return call_agent(SYSTEM_PROMPT, context, MODEL, TEMPERATURE)
