from bot.agents import architect, writer, editor, tester
from bot.utils.file_loader import read_project_file


def generate_post(topic: str = "") -> dict:
    """Полный цикл генерации поста: Архитектор → Писатель → Редактор → Тестировщик"""

    task = topic if topic else "Выбери подходящую тему из контент-плана и напиши пост."

    # Шаг 1 — Архитектор планирует структуру
    structure = architect.run(task)

    # Шаг 2 — Писатель пишет черновик
    tone = read_project_file("tone-of-voice.md")
    draft = writer.run(structure, tone)

    # Шаг 3 — Редактор правит
    edited = editor.run(draft)

    # Шаг 4 — Тестировщик проверяет
    verdict = tester.run(edited)

    return {
        "structure": structure,
        "draft": draft,
        "edited": edited,
        "verdict": verdict,
    }


def edit_post(text: str) -> dict:
    """Редактирование готового текста: Редактор → Тестировщик"""

    edited = editor.run(text)
    verdict = tester.run(edited)

    return {
        "edited": edited,
        "verdict": verdict,
    }
