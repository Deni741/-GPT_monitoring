import subprocess

def run():
    result = subprocess.run(["git", "-C", "/root/GPT_monitoring", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return f"📦 Оновлення з GitHub:\n{result.stdout or result.stderr}"
