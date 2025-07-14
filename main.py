import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from openai import OpenAI
import asyncio

# =============== 1. ЗАВАНТАЖЕННЯ ЗМІННИХ ====================
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# =============== 2. ЛОГУВАННЯ ===============================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# =============== 3. ІНІЦІАЛІЗАЦІЯ OPENAI ====================
client = OpenAI(api_key=OPENAI_API_KEY)

# =============== 4. ОБРОБНИК КОМАНДИ /start =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Надішли мені запит або скористайся командою /ask")

# =============== 5. ОБРОБНИК КОМАНДИ /ask ===================
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("Будь ласка, введи запит після команди /ask")
        return

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        reply_text = response.choices[0].message.content
        await update.message.reply_text(reply_text)

    except Exception as e:
        await update.message.reply_text(f"❌ Помилка GPT:\n{e}")

# =============== 6. ОБРОБНИК ЗВИЧАЙНОГО ПОВІДОМЛЕННЯ ========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        reply_text = response.choices[0].message.content
        await update.message.reply_text(reply_text)

    except Exception as e:
        await update.message.reply_text(f"❌ Помилка GPT:\n{e}")

# =============== 7. MAIN ====================================
if __name__ == '__main__':
    import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Бот запущено 🚀")
    app.run_polling()
