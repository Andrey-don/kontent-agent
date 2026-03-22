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
        ["📋 Контент-план", "📁 Загрузить файл"],
    ],
    resize_keyboard=True,
)

# Состояние ожидания текста от пользователя
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

    # Ожидаем тему для поста
    if user_state.get(chat_id) == "waiting_topic":
        user_state.pop(chat_id)
        await update.message.reply_text("Генерирую пост... Подожди немного. ⏳")
        result = orchestrator.generate_post(topic=text)
        await update.message.reply_text(f"📝 Готовый пост:\n\n{result['edited']}")
        await update.message.reply_text(f"🔍 Проверка тестировщика:\n{result['verdict']}")
        return

    # Ожидаем текст для редактирования
    if user_state.get(chat_id) == "waiting_edit":
        user_state.pop(chat_id)
        await update.message.reply_text("Редактирую... ⏳")
        result = orchestrator.edit_post(text=text)
        await update.message.reply_text(f"✏️ Отредактированный пост:\n\n{result['edited']}")
        await update.message.reply_text(f"🔍 Проверка тестировщика:\n{result['verdict']}")
        return

    # Кнопки главного меню
    if text == "✍️ Написать пост":
        user_state[chat_id] = "waiting_topic"
        await update.message.reply_text(
            "Напиши тему или задачу для поста.\n\n"
            "Например: «Кейс: бот для кафе» или просто «выбери сам из плана»."
        )

    elif text == "✏️ Редактировать пост":
        user_state[chat_id] = "waiting_edit"
        await update.message.reply_text("Отправь текст поста, который нужно отредактировать.")

    elif text == "📋 Контент-план":
        plan = read_project_file("content-plan.md")
        if plan:
            await update.message.reply_text(f"📋 Контент-план:\n\n{plan[:3000]}")
        else:
            await update.message.reply_text("Файл content-plan.md не найден.")

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

    await update.message.reply_text(f"Загружаю файл {doc.file_name}... ⏳")
    file = await context.bot.get_file(doc.file_id)
    data = await file.download_as_bytearray()
    path = save_uploaded_file(doc.file_name, bytes(data))
    await update.message.reply_text(
        f"✅ Файл сохранён: {doc.file_name}\n\n"
        "Теперь агенты будут учитывать его при написании постов."
    )


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN не задан в .env")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен. Нажми Ctrl+C для остановки.")
    app.run_polling()


if __name__ == "__main__":
    main()
