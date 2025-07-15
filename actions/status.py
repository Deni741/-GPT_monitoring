import subprocess

def run():
    try:
        output = subprocess.check_output(["systemctl", "status", "telegram_bot.service", "--no-pager"])
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"Status check failed:\n{e.output.decode('utf-8')}"
