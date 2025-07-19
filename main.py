import os
from dotenv import load_dotenv
load_dotenv(".env.local")
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from file_manager import read_file, write_file, create_file, delete_file, list_files, edit_file

# Завантаження змінних середовища
load_dotenv()

# GPT
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def process_gpt_query(query: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": query}],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Помилка GPT: {str(e)}"

# Команда старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📄 Readfile", callback_data="read_file")],
        [InlineKeyboardButton("✏️ EditFile", callback_data="edit_file")],
        [InlineKeyboardButton("🗂 CreateFile", callback_data="create_file")],
        [InlineKeyboardButton("📁 ListFiles", callback_data="list_files")],
        [InlineKeyboardButton("🚀 PUSH", callback_data="push_code")],
        [InlineKeyboardButton("🧠 GPT", callback_data="ask_gpt")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔽 Вибери опцію ⤵️", reply_markup=reply_markup)

# /ask — GPT запит
async def ask_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Обробка GPT-запиту...")
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("❗️Будь ласка, надішли запит після команди /ask")
        return
    response = process_gpt_query(query)
    await update.message.reply_text(response[:4000])

# Обробка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    context.user_data["mode"] = data

    if data == "read_file":
        await query.message.reply_text("📥 Введи шлях до файлу:")
    elif data == "edit_file":
        context.user_data["step"] = "get_filename"
        await query.message.reply_text("✏️ Введи назву файлу, який хочеш редагувати:")
    elif data == "create_file":
        await query.message.reply_text("📄 Введи шлях і вміст файлу. Приклад:\nMemory/тест.md Це вміст нового файлу")
    elif data == "list_files":
        result = list_files("")
        await query.message.reply_text(result[:4000])
    elif data == "ask_gpt":
        await query.message.reply_text("🧠 Введи запит до GPT:")
    elif data == "push_code":
        os.system("cd /root/GPT_monitoring && git add . && git commit -m 'Автооновлення GPT' && git push")
        await query.message.reply_text("✅ Код запушено на GitHub!")

# Обробка текстових повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode", "")

    if mode == "read_file":
        result = read_file(text)
        await update.message.reply_text(result[:4000])

    elif mode == "edit_file":
        if "step" not in context.user_data:
            context.user_data["step"] = "get_filename"
            await update.message.reply_text("✏️ Введи назву файлу, який хочеш редагувати:")
        elif context.user_data["step"] == "get_filename":
            context.user_data["filename"] = text
            context.user_data["step"] = "get_new_content"
            await update.message.reply_text("📝 Введи новий вміст файлу:")
        elif context.user_data["step"] == "get_new_content":
            filename = context.user_data["filename"]
            new_content = text
            result = edit_file(filename, new_content)
            await update.message.reply_text(result)
            context.user_data.clear()

    elif mode == "create_file":
        parts = text.split(maxsplit=1)
        if len(parts) < 1:
            await update.message.reply_text("❗️ Невірний формат. Приклад:\nMemory/файл.md Написати щось")
            return
        path = parts[0]
        content = parts[1] if len(parts) > 1 else ""
        result = create_file(path, content)
        await update.message.reply_text(result)

    elif mode == "ask_gpt":
        response = process_gpt_query(text)
        await update.message.reply_text(response[:4000])

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask_gpt))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
