from bot.utils.openrouter import call_agent
from bot.utils.file_loader import read_project_file

MODEL = "anthropic/claude-sonnet-4-6"
TEMPERATURE = 0.4

SYSTEM_PROMPT = """Ты — критик контента. Оцениваешь пост и даёшь честную ревизию.

Оцениваешь по шкале от 1 до 10 по каждому критерию:
- Крючок: насколько цепляет первое предложение
- Голос: соответствие стилю автора
- Польза: реальная ценность для читателя
- CTA: насколько понятен и мотивирует к действию
- Общая оценка

После оценок — 3 конкретных совета что улучшить.
Будь честным и конкретным. Не хвали просто так."""


def run(post: str) -> str:
    tone = read_project_file("tone-of-voice.md")

    context = f"""
ГОЛОС АВТОРА (эталон):
{tone}

ПОСТ ДЛЯ ОЦЕНКИ:
{post}

Оцени пост по критериям. Дай конкретные советы по улучшению.
"""
    return call_agent(SYSTEM_PROMPT, context, MODEL, TEMPERATURE)
