import subprocess

def run():
    try:
        output = subprocess.check_output(["journalctl", "-u", "telegram_bot.service", "-n", "50", "--no-pager"])
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"Log read failed:\n{e.output.decode('utf-8')}"
