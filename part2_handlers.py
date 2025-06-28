from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes
from part3_openai import ask_gpt

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я GPT-бот. Напиши запит або натисни кнопку.")

async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = " ".join(context.args)
    if not question:
        await update.message.reply_text("Використання: /ask [запит]")
        return
    response = await ask_gpt(question)
    await update.message.reply_text(response)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    response = await ask_gpt(question)
    await update.message.reply_text(response)

def add_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ask", ask_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))