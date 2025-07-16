import subprocess
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def push_to_github():
    try:
        os.chdir("/root/GPT_monitoring")  # перейди до кореня репозиторію

        subprocess.run(["git", "add", "."], check=True)

        commit_message = f"Авто PUSH: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        subprocess.run(["git", "push", "origin", "main"], check=True)

        return True, "✅ PUSH виконано успішно."

    except subprocess.CalledProcessError as e:
        return False, f"❌ PUSH помилка: {e}"
