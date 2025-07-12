import os
import logging
from aiogram import Bot, Dispatcher, types, executor
from openai import OpenAI

# Завантаження токенів
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ініціалізація бота та GPT
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
client = OpenAI(api_key=OPENAI_API_KEY)

# Логування
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply("Привіт! Я GPT-бот. Напиши мені щось, і я відповім.")

@dp.message_handler()
async def gpt_handler(message: types.Message):
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message.text}]
        )
        answer = completion.choices[0].message.content.strip()
        await message.reply(answer)
    except Exception as e:
        await message.reply(f"Сталася помилка: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
