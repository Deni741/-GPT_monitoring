
import os
import openai
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Завантаження токенів із файлів
with open("bot_token.txt", "r") as f:
    TELEGRAM_TOKEN = f.read().strip()

with open("openai_token.txt", "r") as f:
    OPENAI_API_KEY = f.read().strip()

openai.api_key = OPENAI_API_KEY

# Налаштування логування
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я GPT-бот. Напиши запит або натисни кнопку.")

# Основна обробка повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ти корисний Telegram-бот, що відповідає українською мовою."},
                {"role": "user", "content": user_message},
            ],
        )
        bot_reply = response.choices[0].message.content.strip()
    except Exception as e:
        bot_reply = f"Помилка GPT:\n{str(e)}"

    await update.message.reply_text(bot_reply)

# Запуск бота
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
