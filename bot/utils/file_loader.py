import os
import json

UPLOADS_DIR = os.getenv("UPLOADS_DIR", "data/uploads")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def read_project_file(filename: str) -> str:
    path = os.path.join(PROJECT_ROOT, filename)
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_uploaded_files() -> str:
    uploads_path = os.path.join(PROJECT_ROOT, UPLOADS_DIR)
    if not os.path.exists(uploads_path):
        return ""

    content = []
    for filename in os.listdir(uploads_path):
        filepath = os.path.join(uploads_path, filename)
        if filename.endswith(".md"):
            with open(filepath, "r", encoding="utf-8") as f:
                content.append(f"--- {filename} ---\n{f.read()}")
        elif filename.endswith(".json"):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Извлекаем текст сообщений из JSON-выгрузки Telegram
                if isinstance(data, dict) and "messages" in data:
                    messages = [
                        m.get("text", "") for m in data["messages"]
                        if isinstance(m.get("text"), str) and len(m.get("text", "")) > 50
                    ]
                    content.append(f"--- {filename} (posts) ---\n" + "\n\n".join(messages))
                else:
                    content.append(f"--- {filename} ---\n{json.dumps(data, ensure_ascii=False)}")

    return "\n\n".join(content)


def save_uploaded_file(filename: str, data: bytes) -> str:
    uploads_path = os.path.join(PROJECT_ROOT, UPLOADS_DIR)
    os.makedirs(uploads_path, exist_ok=True)
    filepath = os.path.join(uploads_path, filename)
    with open(filepath, "wb") as f:
        f.write(data)
    return filepath
