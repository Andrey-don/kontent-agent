from bot.utils.openrouter import call_agent
from bot.utils.file_loader import read_project_file

MODEL = "anthropic/claude-sonnet-4-6"
TEMPERATURE = 0.4

SYSTEM_PROMPT = """Ты — ресёрчер. Ищешь и структурируешь информацию по теме для написания поста.

Что делаешь:
- Собираешь ключевые факты и цифры по теме
- Находишь конкретные примеры и кейсы
- Формулируешь боли аудитории по теме
- Предлагаешь возможные углы подачи материала

Аудитория: владельцы малого бизнеса, эксперты-фрилансеры, стартаперы.
Пиши только то, что реально полезно для написания поста. Без воды."""


def run(topic: str) -> str:
    audience = read_project_file("audience.md")
    brief = read_project_file("brief.md")

    context = f"""
ТЕМА ДЛЯ ИССЛЕДОВАНИЯ:
{topic}

АУДИТОРИЯ АВТОРА:
{audience[:2000] if audience else "Не загружено."}

БРИФ:
{brief}

Собери информацию по теме: факты, цифры, кейсы, боли аудитории, углы подачи.
"""
    return call_agent(SYSTEM_PROMPT, context, MODEL, TEMPERATURE)
