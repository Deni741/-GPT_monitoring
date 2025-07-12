import configparser
import openai

# Зчитування токенів із config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Отримання шляху до файлу з OpenAI API токеном
api_key_file = config.get("openai", "api_key_file")

# Зчитування токена з файлу
with open(api_key_file, "r") as f:
    openai.api_key = f.read().strip()

# Основна функція взаємодії з GPT
def ask_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ти асистент для Telegram-бота GPT Monitoring."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Помилка GPT:\n{str(e)}"