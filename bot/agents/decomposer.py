from bot.utils.openrouter import call_agent

MODEL = "anthropic/claude-sonnet-4-6"
TEMPERATURE = 0.3

SYSTEM_PROMPT = """Ты — декомпозитор. Получаешь сложную задачу и разбиваешь её на конкретные мелкие шаги.

Правила:
- Каждый шаг — одно конкретное действие
- Шаги идут в логическом порядке
- Каждый шаг понятен без дополнительных объяснений
- Не более 7 шагов

Формат ответа:
1. [конкретное действие]
2. [конкретное действие]
...

Только список. Без вступлений и комментариев."""


def run(task: str) -> str:
    return call_agent(SYSTEM_PROMPT, task, MODEL, TEMPERATURE)
