
<<<<<<< HEAD
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
import os
from openai import OpenAI
from dotenv import load_dotenv

# Завантаження .env змінних
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Ініціалізація OpenAI
openai = OpenAI(api_key=OPENAI_API_KEY)

# Обробник команд /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я GPT-бот. Надішли мені запит, і я відповім.")

# Обробник звичайних повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    try:
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )
        response = completion.choices[0].message.content
    except Exception as e:
        response = f"Виникла помилка при зверненні до OpenAI: {e}"

    await update.message.reply_text(response)

# Основна функція запуску бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == '__main__':
=======
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
>>>>>>> 826a837a38227393f7f572d0e5771d47d66ab6da
    main()
