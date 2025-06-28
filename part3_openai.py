import os
import openai

# Читання токена з файлу
with open("openai_token.txt", "r") as file:
    openai.api_key = file.read().strip()

# Основна функція для запиту до GPT
async def ask_gpt(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ти корисний Telegram-бот з аналітики ринку криптовалют."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Помилка GPT: {e}"