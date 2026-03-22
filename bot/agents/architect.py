from bot.utils.openrouter import call_agent
from bot.utils.file_loader import read_project_file, load_uploaded_files

MODEL = "anthropic/claude-opus-4-6"
TEMPERATURE = 0.7

SYSTEM_PROMPT = """Ты — архитектор контента. Твоя задача — проанализировать примеры постов автора и спланировать структуру нового поста.

Всегда читай tone-of-voice автора перед работой.

Правила анализа:
- Определи типичную структуру постов автора
- Выдели характерные обороты и слова
- Выбери подходящую тему из контент-плана

Выдай чёткую структуру будущего поста:
1. Крючок (первые 1-2 предложения — результат или провокация)
2. Тело (3-5 коротких блоков)
3. Вывод (1-2 предложения)
4. CTA (вопрос + кодовое слово)"""


def run(task: str) -> str:
    tone = read_project_file("tone-of-voice.md")
    content_plan = read_project_file("content-plan.md")
    examples = load_uploaded_files() or read_project_file("posts-draft.md")

    context = f"""
ГОЛОС АВТОРА:
{tone}

КОНТЕНТ-ПЛАН:
{content_plan}

ПРИМЕРЫ ПОСТОВ АВТОРА:
{examples}

ЗАДАЧА:
{task}
"""
    return call_agent(SYSTEM_PROMPT, context, MODEL, TEMPERATURE)
