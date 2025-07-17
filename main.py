from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from file_manager import read_file, write_file, create_file, delete_file, list_files

# КНОПКИ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📄 ReadFile", callback_data="read_file")],
        [InlineKeyboardButton("✏️ EditFile", callback_data="edit_file")],
        [InlineKeyboardButton("📁 CreateFile", callback_data="create_file")],
        [InlineKeyboardButton("📂 ListFiles", callback_data="list_files")],
        [InlineKeyboardButton("🚀 PUSH", callback_data="push_code")],
        [InlineKeyboardButton("🧠 GPT", callback_data="ask_gpt")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Вибери опцію 👇", reply_markup=reply_markup)

# Обробка натискання кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "read_file":
        await query.message.reply_text("📄 Введи шлях до файлу:")
        context.user_data["mode"] = "read_file"

    elif data == "edit_file":
        await query.message.reply_text("✏️ Введи шлях до файлу для редагування:")
        context.user_data["mode"] = "edit_file"

    elif data == "create_file":
        await query.message.reply_text("📁 Введи шлях до файлу і його вміст через пробіл:")
        context.user_data["mode"] = "create_file"

    elif data == "list_files":
        await query.message.reply_text("📂 Введи назву папки або залиш порожнім:")
        context.user_data["mode"] = "list_files"

    elif data == "push_code":
        await query.message.reply_text("🚀 Виконую PUSH до GitHub...")
        import os
        os.system("cd /root/GPT_monitoring && git add . && git commit -m 'Auto push' && git push")
        await query.message.reply_text("✅ Зміни запушено до GitHub.")

    elif data == "ask_gpt":
        await query.message.reply_text("🧠 Напиши запит для GPT:")
        context.user_data["mode"] = "gpt_prompt"

# Обробка текстових повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode", "none")

    if mode == "read_file":
        result = read_file(text)
        await update.message.reply_text(result[:4000])

    elif mode == "edit_file":
        await update.message.reply_text("✏️ Введи новий вміст файлу:")
        context.user_data["edit_path"] = text
        context.user_data["mode"] = "edit_file_step2"

    elif mode == "edit_file_step2":
        path = context.user_data.get("edit_path", "")
        content = text
        result = write_file(path, content)
        await update.message.reply_text(result)

    elif mode == "create_file":
        parts = text.split(maxsplit=1)
        if len(parts) < 1:
            await update.message.reply_text("❗️ Невірний формат. Приклад:\nMemory/ідеї.md Написати файл")
            return
        path = parts[0]
        content = parts[1] if len(parts) > 1 else ""
        result = create_file(path, content)
        await update.message.reply_text(result)

    elif mode == "list_files":
        result = list_files(text)
        await update.message.reply_text(result[:4000])

    elif mode == "gpt_prompt":
        from openai import OpenAI
        # Псевдозапит — підставляй свій GPT-запит або обробку
        await update.message.reply_text("⏳ Обробка GPT-запиту (заглушка)...")

# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token("ТУТ_ТВОЙ_ТОКЕН").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
