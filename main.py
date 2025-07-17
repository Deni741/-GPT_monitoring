import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
)
from file_manager import read_file, write_file, create_file, delete_file, list_files

BOT_TOKEN = open("bot_token.txt", "r").read().strip()

keyboard = [
    [InlineKeyboardButton("🧠 Запитай у GPT", callback_data="ask_gpt")],
    [InlineKeyboardButton("📂 Прочитати файл", callback_data="read_file")],
    [InlineKeyboardButton("✏️ Редагувати файл GPT", callback_data="edit_file")],
    [InlineKeyboardButton("📤 PUSH до GitHub", callback_data="push_code")],
    [InlineKeyboardButton("📝 Створити файл", callback_data="create_file")],
    [InlineKeyboardButton("📁 Список файлів", callback_data="list_files")]
]
reply_markup = InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Вибери опцію 👇", reply_markup=reply_markup)

# GPT-запит
async def handle_gpt_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✍️ Напиши запит для GPT:")
    context.user_data["mode"] = "gpt_prompt"

# Прочитати файл
async def readfile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📄 Введи шлях до файлу, який хочеш прочитати:")
    context.user_data["mode"] = "read_file"

# Редагування GPT
async def handle_edit_gpt_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛠️ Введи шлях до файлу для редагування GPT:")
    context.user_data["mode"] = "gpt_edit_step1"

# Обробка натискання кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "ask_gpt":
        await query.message.reply_text("✍️ Напиши запит для GPT:")
        context.user_data["mode"] = "gpt_prompt"

    elif data == "read_file":
        await query.message.reply_text("📄 Введи шлях до файлу:")
        context.user_data["mode"] = "read_file"

    elif data == "edit_file":
        await query.message.reply_text("🛠️ Введи шлях до файлу для редагування:")
        context.user_data["mode"] = "gpt_edit_step1"

    elif data == "push_code":
        await query.message.reply_text("🚀 Виконую PUSH до GitHub...")
        os.system("cd /root/GPT_monitoring && git add . && git commit -m 'Auto push' && git push")
        await query.message.reply_text("✅ Зміни запушено до GitHub.")

    elif data == "create_file":
        await query.message.reply_text("📝 Введи шлях і вміст файлу через пробіл:\nНаприклад: `Memory/test.txt Це тестовий файл`")
        context.user_data["mode"] = "create_file"

    elif data == "list_files":
        await query.message.reply_text("📁 Введи назву папки або залиш порожнім для поточної:")
        context.user_data["mode"] = "list_files"
		
		# Обробка текстових повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode", "none")

    if mode == "gpt_prompt":
        context.user_data["mode"] = "none"
        await update.message.reply_text(f"🤖 GPT відповідає: {text[::-1]}")  # Тестова відповідь, заміниш на GPT

    elif mode == "read_file":
        result = read_file(text)
        await update.message.reply_text(result[:4000])

    elif mode == "create_file":
        try:
            parts = text.split(maxsplit=1)
            if len(parts) < 1:
                await update.message.reply_text("❗️Формат: шлях і вміст через пробіл.")
                return
            path = parts[0]
            content = parts[1] if len(parts) > 1 else ""
            result = create_file(path, content)
            await update.message.reply_text(result)
        except Exception as e:
            await update.message.reply_text(f"❌ Помилка: {e}")

    elif mode == "list_files":
        try:
            directory = text.strip() if text.strip() else "."
            result = list_files(directory)
            await update.message.reply_text(result[:4000])
        except Exception as e:
            await update.message.reply_text(f"❌ Помилка: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
