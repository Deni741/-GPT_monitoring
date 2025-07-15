import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_message(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Failed to send message: {e}")

class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        action = query.get('do', [None])[0]

        if not action:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing 'do' parameter")
            return

        if action == "status":
            output = subprocess.getoutput("systemctl status telegram_bot.service --no-pager")
            send_message("🔍 STATUS:\n" + output[:4000])
        elif action == "pull":
            output = subprocess.getoutput("cd /root/GPT_monitoring && git pull")
            send_message("📥 PULL:\n" + output[:4000])
        elif action == "restart":
            output = subprocess.getoutput("systemctl restart telegram_bot.service")
            send_message("♻️ Бот перезапущено.")
        elif action == "logs":
            output = subprocess.getoutput("tail -n 40 /root/GPT_monitoring/update_log.txt")
            send_message("🧾 Логи:\n" + output[:4000])
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

if __name__ == "__main__":
    server_address = ("", 8989)
    httpd = HTTPServer(server_address, WebhookHandler)
    print("✅ Webhook server is running on port 8989...")
    httpd.serve_forever()
