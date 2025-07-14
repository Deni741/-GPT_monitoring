import http.server
import json
import subprocess
import telegram
import os
from dotenv import load_dotenv

# Завантажуємо токен Telegram та ID
load_dotenv('/root/GPT_monitoring/.env')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


bot = telegram.Bot(token="8108237988:AAEa3aj8WOuLMwk11DPmRc_eqFt-WKP1NY8")

class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        try:
            payload = json.loads(body)
            commits = payload.get("commits", [])
            repo_name = payload.get("repository", {}).get("name", "невідомо")

            if commits:
                for commit in commits:
                    message = commit.get("message", "без повідомлення")
                    author = commit.get("committer", {}).get("name", "невідомий")
                    commit_url = commit.get("url", "")
                    sha = commit.get("id", "")[:7]

                    text = f"🔄 <b>Оновлення в GitHub ({repo_name})</b>\n" \
                           f"👤 Автор: <code>{author}</code>\n" \
                           f"💬 Повідомлення: <code>{message}</code>\n" \
                           f"🔗 <a href='{commit_url}'>{sha}</a>"

                    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, parse_mode=telegram.constants.ParseMode.HTML)
            else:
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="⚠️ Отримано Webhook без комітів.")

        except Exception as e:
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"❌ Помилка обробки Webhook: {e}")

        self.send_response(200)
        self.end_headers()

if __name__ == '__main__':
    server_address = ('', 8080)
    httpd = http.server.HTTPServer(server_address, WebhookHandler)
    print('Слухаємо порт 8080...')
    httpd.serve_forever()
