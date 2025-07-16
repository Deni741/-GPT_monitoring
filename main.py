import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from openai import OpenAI
from push_handler import handle_push

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧠 GPT", callback_data="ask_gpt")],
        [InlineKeyboardButton("📊 Аналіз", callback_data="analyze")],
        [InlineKeyboardButton("🚀 PUSH", callback_data="show_push")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            "Привіт! Надішли мені запит або скористайся кнопками нижче:",
            reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            "Привіт! Надішли мені запит або скористайся кнопками нижче:",
            reply_markup=reply_markup
        )

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    if not query:
        await update.message.reply_text("Напиши текст для запиту.")
        return

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": query}]
    )
    await update.message.reply_text(response.choices[0].message.content)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask))
    app.add_handler(CallbackQueryHandler(handle_push, pattern="^show_push$"))

    print("🤖 Бот запущено!")
    app.run_polling()

if __name__ == "__main__":
    main()
from push_handler import handle_push

# У функції start_handler
keyboard = [
    [InlineKeyboardButton("🤖 GPT", callback_data='gpt')],
    [InlineKeyboardButton("📈 Аналіз", callback_data='analyze')],
    [InlineKeyboardButton("📤 PUSH", callback_data='push')]
]
reply_markup = InlineKeyboardMarkup(keyboard)
await update.message.reply_text("Привіт! Надішли мені запит або скористайся командою /ask", reply_markup=reply_markup)

# У функції callback_handler
if query.data == "push":
    await handle_push(query, context)
