from flask import Flask, request, jsonify
import os
import subprocess
import logging

app = Flask(__name__)

# ????????? ? ????
logging.basicConfig(filename='/root/GPT_monitoring/webhook_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        logging.info("Webhook triggered.")

        # ??????? ?? ?????????? ???????
        os.chdir('/root/GPT_monitoring')

        # Git pull
        logging.info("Running git pull...")
        subprocess.run(['git', 'pull'], check=True)

        # ?????????? ??????? telegram_bot
        logging.info("Restarting telegram_bot.service...")
        subprocess.run(['systemctl', 'restart', 'telegram_bot.service'], check=True)

        logging.info("Webhook processing complete.")
        return jsonify({'status': 'ok', 'message': 'Bot updated and restarted'}), 200

    except Exception as e:
        logging.error(f"Error during webhook execution: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)