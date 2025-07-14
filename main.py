
import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
import openai

# Завантаження .env змінних
load_dotenv('/root/GPT_monitoring/.env')
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Ініціалізація OpenAI
openai.api_key = OPENAI_API_KEY

# GPT-відповідь
async def ask_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ти — корисний Telegram-бот, помічник користувача."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Помилка GPT: {e}"

# Обробник повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logging.info(f"📩 Отримано повідомлення: {user_message}")
    reply = await ask_gpt(user_message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="👋 Привіт! Я GPT-помічник. Надішли мені повідомлення, і я відповім.")

# Головна функція
def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
