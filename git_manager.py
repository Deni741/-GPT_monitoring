import os

def read_file(file_path):
    try:
        full_path = os.path.join(os.getcwd(), file_path)
        if not os.path.exists(full_path):
            return f"[❌] Файл не знайдено: {file_path}"
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"[❌] Помилка при читанні {file_path}:\n{str(e)}"
