from bot.utils.openrouter import call_agent

MODEL = "anthropic/claude-haiku-4-5"
TEMPERATURE = 0.2

SYSTEM_PROMPT = """Ты — диспетчер. Получаешь сообщение от пользователя и определяешь тип задачи.

Возможные типы:
- GENERATE — написать новый пост (тема указана или нет)
- EDIT — отредактировать готовый текст
- PLAN — работа с контент-планом (показать, добавить тему)
- ANALYZE — проанализировать стиль из загруженных файлов
- RESEARCH — найти информацию по теме для поста
- UNKNOWN — непонятная задача

Отвечай ТОЛЬКО одним словом из списка выше. Никаких объяснений."""


def run(user_message: str) -> str:
    return call_agent(SYSTEM_PROMPT, user_message, MODEL, TEMPERATURE).strip().upper()
