from telegram import Update
from telegram.ext import ContextTypes
import subprocess

async def handle_push(query, context: ContextTypes.DEFAULT_TYPE):
    await query.message.reply_text("📤 Відправляю всі зміни в GitHub...")
    try:
        result = subprocess.run(
            ["python3", "/root/GPT_monitoring/auto_git_pusher.py"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            await query.message.reply_text("✅ PUSH виконано успішно.")
        else:
            await query.message.reply_text(f"❌ ПОМИЛКА:\n{result.stderr}")
    except Exception as e:
        await query.message.reply_text(f"❌ Виняток:\n{e}")
