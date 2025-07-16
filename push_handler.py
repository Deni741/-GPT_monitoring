import subprocess
import datetime

async def handle_push():
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"🔄 Auto push {timestamp}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ PUSH виконано успішно.")
    except subprocess.CalledProcessError as e:
        print("❌ Помилка під час PUSH:", e)
