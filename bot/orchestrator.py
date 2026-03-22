from bot.agents import (
    architect, writer, editor, tester,
    dispatcher, decomposer, researcher, critic,
    style_analyst, content_planner,
)
from bot.utils.file_loader import read_project_file


def generate_post(topic: str = "") -> dict:
    """Полный цикл генерации поста: Ресёрчер → Архитектор → Писатель → Критик → Редактор → Тестировщик"""

    task = topic if topic else "Выбери подходящую тему из контент-плана и напиши пост."

    # Шаг 1 — Ресёрчер собирает материал по теме
    research = researcher.run(task)

    # Шаг 2 — Архитектор планирует структуру
    structure = architect.run(f"Тема: {task}\n\nМатериал от ресёрчера:\n{research}")

    # Шаг 3 — Писатель пишет черновик
    tone = read_project_file("tone-of-voice.md")
    draft = writer.run(structure, tone)

    # Шаг 4 — Критик оценивает
    critique = critic.run(draft)

    # Шаг 5 — Редактор правит с учётом критики
    edited = editor.run(f"{draft}\n\n---\nЗамечания критика:\n{critique}")

    # Шаг 6 — Тестировщик финально проверяет
    verdict = tester.run(edited)

    return {
        "research": research,
        "structure": structure,
        "draft": draft,
        "critique": critique,
        "edited": edited,
        "verdict": verdict,
    }


def edit_post(text: str) -> dict:
    """Редактирование готового текста: Критик → Редактор → Тестировщик"""

    critique = critic.run(text)
    edited = editor.run(f"{text}\n\n---\nЗамечания критика:\n{critique}")
    verdict = tester.run(edited)

    return {
        "critique": critique,
        "edited": edited,
        "verdict": verdict,
    }


def analyze_style() -> str:
    """Анализ стиля из загруженных файлов"""
    return style_analyst.run()


def get_plan(task: str = "Покажи актуальные темы и предложи следующую для публикации.") -> str:
    """Работа с контент-планом"""
    return content_planner.run(task)


def route(user_message: str) -> str:
    """Диспетчер определяет тип задачи"""
    return dispatcher.run(user_message)
