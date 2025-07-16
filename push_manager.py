import subprocess
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_git_status():
    try:
        result = subprocess.check_output(["git", "status", "-s"], cwd="/root/GPT_monitoring")
        return result.decode("utf-8") or "Немає змін"
    except Exception as e:
        return f"Помилка: {e}"

def git_push():
    try:
        subprocess.check_call(["git", "add", "."], cwd="/root/GPT_monitoring")
        subprocess.check_call(["git", "commit", "-m", "Manual push from Telegram"], cwd="/root/GPT_monitoring")
        subprocess.check_call(["git", "push"], cwd="/root/GPT_monitoring")
        return "✅ Зміни успішно відправлені в GitHub!"
    except subprocess.CalledProcessError:
        return "⚠️ Помилка при пуші (можливо, нічого не змінено)"
    except Exception as e:
        return f"🚨 Помилка: {e}"

def get_push_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Так, пушити", callback_data="confirm_push")],
        [InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel_push")]
    ])
