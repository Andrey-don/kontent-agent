from bot.utils.openrouter import call_agent
from bot.utils.file_loader import read_project_file

MODEL = "anthropic/claude-sonnet-4-6"
TEMPERATURE = 0.7

SYSTEM_PROMPT = """Ты — копирайтер, который пишет строго в стиле конкретного автора-вайбкодера.

Голос автора важнее структуры — всегда читай tone-of-voice.md.

Жёсткие правила:
- Результат ПЕРВЫМ — пост начинается с итога, не с раскачки
- Пост про клиента, не про инструмент
- Короткие предложения — один смысл, одно предложение
- Длина: 150–300 слов
- 3–5 эмодзи только там где усиливают смысл
- Провокационный вопрос перед CTA
- Кодовое слово в CTA (одно слово, заглавными)

Технические термины пиши естественно, без объяснений в скобках."""


def run(structure: str, tone: str) -> str:
    context = f"""
ГОЛОС АВТОРА:
{tone}

СТРУКТУРА ПОСТА (от Архитектора):
{structure}

Напиши готовый пост строго по этой структуре и в голосе автора.
"""
    return call_agent(SYSTEM_PROMPT, context, MODEL, TEMPERATURE)
