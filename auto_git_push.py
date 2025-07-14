import os
import time
import subprocess
from datetime import datetime

WATCH_DIR = '/root/GPT_monitoring'
LOG_FILE = '/root/GPT_monitoring/auto_git.log'
DEBOUNCE_SECONDS = 180  # 3 хвилини без змін

def log(msg):
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def has_changes():
    result = subprocess.run(['git', 'status', '--porcelain'], cwd=WATCH_DIR, stdout=subprocess.PIPE)
    return bool(result.stdout)

def push_changes():
    try:
        subprocess.run(['git', 'add', '.'], cwd=WATCH_DIR)
        subprocess.run(['git', 'commit', '-m', 'Auto-sync: local change by GPT'], cwd=WATCH_DIR)
        subprocess.run(['git', 'push'], cwd=WATCH_DIR)
        log("✅ Push успішний")
    except Exception as e:
        log(f"❌ Помилка при пуші: {e}")

def main():
    log("🔍 Авто Git Watchdog запущено")
    last_mtime = 0

    while True:
        try:
            current_mtime = max(
                os.path.getmtime(os.path.join(root, f))
                for root, _, files in os.walk(WATCH_DIR)
                for f in files if not f.startswith('.') and not f.endswith('.log')
            )
            if current_mtime != last_mtime:
                last_mtime = current_mtime
                log("📁 Виявлено зміну. Очікуємо тишу для debounce...")
                time.sleep(DEBOUNCE_SECONDS)
                if has_changes():
                    push_changes()
            time.sleep(5)
        except Exception as e:
            log(f"❗ Помилка: {e}")
            time.sleep(10)

if __name__ == '__main__':
    main()