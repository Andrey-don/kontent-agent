from bot.utils.openrouter import call_agent
from bot.utils.file_loader import read_project_file, load_uploaded_files

MODEL = "anthropic/claude-sonnet-4-6"
TEMPERATURE = 0.5

SYSTEM_PROMPT = """Ты — аналитик стиля. Анализируешь тексты автора и извлекаешь его Tone of Voice.

Что анализируешь:
- Характерные слова и обороты
- Длину предложений
- Способ объяснять (через примеры, цифры, истории)
- Эмоциональный тонус
- Как обращается к читателю
- Типичная структура постов

Результат — краткое описание стиля + список конкретных правил.
Пиши конкретно, с примерами из текстов."""


def run() -> str:
    uploaded = load_uploaded_files()
    existing_tone = read_project_file("tone-of-voice.md")

    context = f"""
ЗАГРУЖЕННЫЕ ПОСТЫ АВТОРА:
{uploaded if uploaded else "Файлы не загружены."}

ТЕКУЩИЙ TONE OF VOICE (для сравнения):
{existing_tone}

Проанализируй загруженные посты. Дополни или скорректируй описание стиля автора.
"""
    return call_agent(SYSTEM_PROMPT, context, MODEL, TEMPERATURE)
