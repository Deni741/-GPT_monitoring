import subprocess

def run():
    try:
        subprocess.check_call(["systemctl", "restart", "telegram_bot.service"])
        return "Bot restarted successfully."
    except subprocess.CalledProcessError as e:
        return f"Restart failed:\n{e}"
