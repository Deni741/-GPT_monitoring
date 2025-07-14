# agent_reader.py

def read_memory():
    file_path = "Memory/system_log.md"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print("[✓] Вміст памʼяті прочитано успішно:")
        print(content)
        return content
    except FileNotFoundError:
        print("[X] Файл памʼяті не знайдено.")
        return ""
    except Exception as e:
        print(f"[X] Помилка при читанні памʼяті: {e}")
        return ""

if __name__ == "__main__":
    read_memory()

