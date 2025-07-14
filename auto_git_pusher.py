import os
import subprocess
from dotenv import load_dotenv

load_dotenv('/root/GPT_monitoring/.env')
token = os.getenv('GITHUB_TOKEN')

if not token:
    print("❌ GITHUB_TOKEN не знайдено в .env")
    exit(1)

os.environ['GIT_ASKPASS'] = 'echo'
os.environ['GIT_USERNAME'] = 'oauth2'
os.environ['GIT_PASSWORD'] = token

# Додаємо всі зміни
subprocess.run(['git', 'add', '.'], cwd='/root/GPT_monitoring')

# Коміт з повідомленням
subprocess.run(['git', 'commit', '-m', '🔁 Auto push by GPT Agent'], cwd='/root/GPT_monitoring')

# Пуш
subprocess.run(['git', 'push', 'origin', 'main'], cwd='/root/GPT_monitoring')
