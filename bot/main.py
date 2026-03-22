import os
import logging
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from bot import orchestrator
from bot.utils.file_loader import save_uploaded_file, read_project_file

load_dotenv()
logging.basicConfig(level=logging.INFO)

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["✍️ Написать пост", "✏️ Редактировать пост"],
        ["📋 Контент-план", "🔍 Оценить пост"],
        ["📊 Анализ стиля", "📁 Загрузить файл"],
    ],
    resize_keyboard=True,
)

user_state: dict = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет. Я бот-копирайтер.\n\n"
        "Пишу посты в твоём стиле на основе твоих файлов.\n\n"
        "Выбери действие:",
        reply_markup=MAIN_KEYBOARD,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id

    # --- Ожидание ввода от пользователя ---

    if user_state.get(chat_id) == "waiting_topic":
        user_state.pop(chat_id)
        await update.message.reply_text("Генерирую пост... Это займёт около минуты. ⏳")
        result = orchestrator.generate_post(topic=text)
        await update.message.reply_text(f"📝 Готовый пост:\n\n{result['edited']}")
        await update.message.reply_text(f"🔍 Вердикт тестировщика:\n{result['verdict']}")
        return

    if user_state.get(chat_id) == "waiting_edit":
        user_state.pop(chat_id)
        await update.message.reply_text("Редактирую... ⏳")
        result = orchestrator.edit_post(text=text)
        await update.message.reply_text(f"✏️ Отредактированный пост:\n\n{result['edited']}")
        await update.message.reply_text(f"🔍 Вердикт тестировщика:\n{result['verdict']}")
        return

    if user_state.get(chat_id) == "waiting_critique":
        user_state.pop(chat_id)
        await update.message.reply_text("Оцениваю... ⏳")
        from bot.agents import critic
        result = critic.run(text)
        await update.message.reply_text(f"🔍 Оценка критика:\n\n{result}")
        return

    if user_state.get(chat_id) == "waiting_plan_task":
        user_state.pop(chat_id)
        await update.message.reply_text("Работаю с планом... ⏳")
        result = orchestrator.get_plan(text)
        await update.message.reply_text(f"📋 Контент-план:\n\n{result}")
        return

    # --- Кнопки главного меню ---

    if text == "✍️ Написать пост":
        user_state[chat_id] = "waiting_topic"
        await update.message.reply_text(
            "Напиши тему или задачу.\n\n"
            "Например: «Кейс: бот для кафе» или «выбери сам из плана»."
        )

    elif text == "✏️ Редактировать пост":
        user_state[chat_id] = "waiting_edit"
        await update.message.reply_text("Отправь текст поста для редактирования.")

    elif text == "🔍 Оценить пост":
        user_state[chat_id] = "waiting_critique"
        await update.message.reply_text("Отправь текст поста — критик оценит его по шкале и даст советы.")

    elif text == "📋 Контент-план":
        user_state[chat_id] = "waiting_plan_task"
        await update.message.reply_text(
            "Что сделать с планом?\n\n"
            "Например: «покажи следующую тему» или «предложи 3 новые темы про ботов»."
        )

    elif text == "📊 Анализ стиля":
        await update.message.reply_text("Анализирую загруженные файлы... ⏳")
        result = orchestrator.analyze_style()
        await update.message.reply_text(f"📊 Анализ стиля:\n\n{result}")

    elif text == "📁 Загрузить файл":
        await update.message.reply_text(
            "Отправь файл MD или JSON с постами из твоего Telegram-канала.\n\n"
            "Как выгрузить: Telegram Desktop → настройки канала → Экспорт."
        )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc.file_name.endswith((".md", ".json")):
        await update.message.reply_text("Поддерживаются только файлы .md и .json")
        return

    await update.message.reply_text(f"Загружаю {doc.file_name}... ⏳")
    file = await context.bot.get_file(doc.file_id)
    data = await file.download_as_bytearray()
    save_uploaded_file(doc.file_name, bytes(data))
    await update.message.reply_text(
        f"✅ Файл сохранён: {doc.file_name}\n\n"
        "Агенты будут учитывать его при написании постов.\n"
        "Нажми «📊 Анализ стиля» чтобы обновить Tone of Voice."
    )


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN не задан в .env")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен. Ctrl+C для остановки.")
    app.run_polling()


if __name__ == "__main__":
    main()
