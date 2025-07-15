import subprocess

def run():
    result = subprocess.run(["systemctl", "status", "telegram_bot.service"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout[-4000:]
