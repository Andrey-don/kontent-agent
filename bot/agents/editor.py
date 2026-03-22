from bot.utils.openrouter import call_agent
from bot.utils.file_loader import read_project_file

MODEL = "anthropic/claude-haiku-4-5"
TEMPERATURE = 0.4

SYSTEM_PROMPT = """Ты — строгий редактор. Получаешь черновик поста и делаешь его лучше.

Что делаешь:
- Убираешь воду и лишние слова
- Режешь длинные предложения на короткие
- Усиливаешь крючок — первые 1-2 предложения должны останавливать скроллинг
- Проверяешь: есть ли результат в первой строке
- Проверяешь: есть ли провокационный вопрос перед CTA
- Проверяешь: есть ли кодовое слово в CTA

Чего НЕ делаешь:
- Не меняешь смысл
- Не меняешь голос автора
- Не добавляешь канцелярит и официоз

Верни только отредактированный пост, без комментариев."""


def run(draft: str) -> str:
    tone = read_project_file("tone-of-voice.md")
    context = f"""
ГОЛОС АВТОРА (не нарушай):
{tone}

ЧЕРНОВИК ПОСТА:
{draft}

Отредактируй. Верни только готовый текст поста.
"""
    return call_agent(SYSTEM_PROMPT, context, MODEL, TEMPERATURE)
