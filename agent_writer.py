# agent_writer.py

def write_memory(entry):
    file_path = "Memory/system_log.md"
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        print("[✓] Запис до памʼяті успішний!")
        return True
    except Exception as e:
        print(f"[X] Помилка при записі до памʼяті: {e}")
        return False
