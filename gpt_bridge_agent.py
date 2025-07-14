from flask import Flask, request, jsonify
import os
import subprocess
import logging

app = Flask(__name__)

# Налаштування логування
logging.basicConfig(
    filename='/root/GPT_monitoring/webhook_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        logging.info("Webhook отримано.")
        os.chdir('/root/GPT_monitoring')

        # Git pull
        logging.info("Виконую git pull...")
        subprocess.run(['git', 'pull'], check=True)

        # Перезапуск telegram bot
        logging.info("Перезапускаю telegram_bot.service...")
        subprocess.run(['systemctl', 'restart', 'telegram_bot.service'], check=True)

        logging.info("Webhook оброблено успішно.")
        return jsonify({'status': 'ok', 'message': 'Бот оновлено та перезапущено'}), 200

    except Exception as e:
        logging.error(f"Помилка під час обробки webhook: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    logging.info("Запускається Flask-сервер на порту 8989...")
    app.run(host='0.0.0.0', port=8989)