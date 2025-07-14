from flask import Flask, request
import subprocess
import logging

app = Flask(__name__)

logging.basicConfig(
    filename='/root/GPT_monitoring/webhook.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        logging.info("Webhook received.")

        # Перезапуск бота
        restart_result = subprocess.run(
            ["systemctl", "restart", "telegram_bot.service"],
            capture_output=True,
            text=True
        )
        logging.info(f"Restart service output:\n{restart_result.stdout}\nErrors:\n{restart_result.stderr}")

        return "Webhook received and processed.", 200

    except Exception as e:
        logging.error(f"Error handling webhook: {e}")
        return "Error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
