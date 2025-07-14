from flask import Flask, request
import subprocess
import logging
import os

app = Flask(__name__)

# Налаштування логування
logging.basicConfig(filename='/root/GPT_monitoring/webhook_log.txt', level=logging.INFO)

@app.route("/", methods=["POST"])
def webhook():
    try:
        data = request.json
        logging.info(f"Received webhook event: {data}")

        # Виконуємо git pull
        repo_path = "/root/GPT_monitoring"
        pull_result = subprocess.run(
            ["git", "-C", repo_path, "pull"],
            capture_output=True,
            text=True
        )
        logging.info(f"Git pull output:\n{pull_result.stdout}\nErrors:\n{pull_result.stderr}")

        # Перезапускаємо telegram_bot.service
        restart_result = subprocess.run(
            ["systemctl", "restart", "telegram_bot.service"],
            capture_output=True,
            text=True
        )
        logging.info(f"Restart service output:\n{restart_result.stdout}\nErrors:\n{restart_result.stderr}")

        return "Webhook received and processed.", 200

    except Exception as e:
        logging.error(f"Error handling webhook: {e}")
        return "Error processing webhook", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
