import os
import subprocess
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
commit_message = f"Auto push from Telegram at {now}"

commands = [
    "cd /root/GPT_monitoring",
    "git add .",
    f'git commit -m "{commit_message}"',
    "git push origin main"
]

for cmd in commands:
    subprocess.run(cmd, shell=True, check=True)
