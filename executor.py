import json
import os
import subprocess

def run_instruction():
    with open("instruction.json", "r") as f:
        instruction = json.load(f)

    action = instruction.get("action")
    path = instruction.get("path")
    content = instruction.get("content")

    if action == "read_file":
        try:
            with open(path, "r") as file:
                data = file.read()
            print("✅ Вміст файлу", path + ":\n" + data)
        except Exception as e:
            print("❌ Помилка при зчитуванні файлу:", e)

    elif action == "create_file":
        try:
            with open(path, "w") as file:
                file.write(content)
            print("✅ Файл створено:", path)
        except Exception as e:
            print("❌ Помилка при створенні файлу:", e)

    elif action == "edit_file":
        try:
            with open(path, "w") as file:
                file.write(content)
            print("✅ Файл оновлено:", path)
        except Exception as e:
            print("❌ Помилка при оновленні файлу:", e)

    elif action == "autopush":
        print("🔍 Запускаємо тести через pytest...")
        try:
            result = subprocess.run(["pytest"], capture_output=True, text=True)
            print(result.stdout)

            if result.returncode == 0:
                print("✅ Тести пройдено. Виконуємо git push...")
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", "Автоматичний пуш після успішного тесту"], check=True)
                subprocess.run(["git", "push"], check=True)
                print("✅ Git push виконано успішно.")
            else:
                print("❌ Тести не пройдено. PUSH не виконано.")
        except Exception as e:
            print("❌ Помилка при запуску тестів або пушу:", e)

if __name__ == "__main__":
    run_instruction()
