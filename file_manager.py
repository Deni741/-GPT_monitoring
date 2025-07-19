import os

def read_file(path):
    if not os.path.exists(path):
        return f"❌ Файл {path} не знайдено."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"✅ Файл {path} оновлено."

def create_file(path, content=""):
    if os.path.exists(path):
        return f"⚠️ Файл {path} вже існує."
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"✅ Файл {path} створено."

def delete_file(path):
    if not os.path.exists(path):
        return f"❌ Файл {path} не існує."
    os.remove(path)
    return f"🗑️ Файл {path} видалено."

def list_files(directory):
    if not os.path.exists(directory):
        return f"❌ Директорія {directory} не знайдена."
    files = os.listdir(directory)
    return "\n".join(files) if files else "📂 Папка порожня."

def edit_file(path, new_content):
    try:
        with open(path, "w", encoding="utf-8") as file:
            file.write(new_content)
        return f"✅ Файл оновлено: {path}"
    except Exception as e:
        return f"❌ Помилка при редагуванні файлу: {str(e)}"
