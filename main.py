import os
import logging
import asyncio
import subprocess
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from openai import OpenAI

# 1. ЗАВАНТАЖЕННЯ ЗМІННИХ
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 2. ЛОГУВАННЯ
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# 3. ІНІЦІАЛІЗАЦІЯ OPENAI
client = OpenAI(api_key=OPENAI_API_KEY)

# 4. МЕНЮ
menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🧠 GPT", callback_data="ask_gpt")],
    [InlineKeyboardButton(text="📊 Аналіз", callback_data="analyze")],
    [InlineKeyboardButton(text="🚀 PUSH", callback_data="show_push")]
])

# 5. ОБРОБНИК /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Надішли мені запит або скористайся кнопками нижче 👇",
        reply_markup=menu_keyboard
    )

# 6. ОБРОБНИК /ask
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

# 7. КНОПКА PUSH
async def handle_push(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📩 Відправляю всі зміни в GitHub...")

    try:
        result = subprocess.run(
            ['python3', '/root/GPT_monitoring/auto_git_pusher.py'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            await query.message.reply_text("✅ PUSH виконано успішно.")
        else:
            await query.message.reply_text(f"❌ Помилка під час PUSH:\n{result.stderr}")
    except Exception as e:
        await query.message.reply_text(f"❗ Виняток:\n{str(e)}")

# 8. ОБРОБНИК КНОПОК
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()
    if data == "ask_gpt":
        await query.message.reply_text("✍️ Надішли запит через /ask <запит>")
    elif data == "analyze":
        await query.message.reply_text("📊 Функція аналізу поки що в розробці.")
    elif data == "show_push":
        await handle_push(update, context)

# 9. ЗАПУСК БОТА
def main():
    pid_file = "/tmp/gpt_bot.pid"
    if os.path.exists(pid_file):
        with open(pid_file, "r") as f:
            pid = int(f.read())
        if os.path.exists(f"/proc/{pid}"):
            print(f"🚫 Захист GPT: бот вже запущений з PID {pid}. Повторний запуск заборонено.")
            exit(1)

    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CallbackQueryHandler(handle_buttons))

    print("✅ Бот запущено. Очікування повідомлень...")
    app.run_polling()

if __name__ == "__main__":
    main()
