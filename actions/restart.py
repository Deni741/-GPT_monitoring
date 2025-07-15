import subprocess

def run():
    subprocess.run(["systemctl", "restart", "telegram_bot.service"])
    return "🔄 Сервіс Telegram-бота перезапущено!"
