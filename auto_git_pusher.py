import os
import subprocess
from dotenv import load_dotenv

# Завантаження .env-файлу
load_dotenv('/root/GPT_monitoring/.env')
token = os.getenv('GITHUB_TOKEN')

# Перевірка, чи є токен
if not token:
    print("❌ GITHUB_TOKEN не знайдено в .env")
    exit(1)

# Додаємо всі зміни до Git
subprocess.run(['git', 'add', '.'], cwd='/root/GPT_monitoring')

# Коміт з повідомленням
subprocess.run(['git', 'commit', '-m', '🤖 Auto push by GPT Agent'], cwd='/root/GPT_monitoring')

# Пуш з токеном у URL
subprocess.run([
    'git', 'push',
    f'https://oauth2:{token}@github.com/Deni741/-GPT_monitoring.git',
    'main'
], cwd='/root/GPT_monitoring')
