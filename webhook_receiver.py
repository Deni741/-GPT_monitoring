from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
from datetime import datetime

LOG_PATH = "/root/GPT_monitoring/webhook_pull.log"

class WebhookHandler(BaseHTTPRequestHandler):
    def log_event(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_PATH, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            payload = json.loads(post_data.decode('utf-8'))
            self.log_event(f"Received webhook payload: {json.dumps(payload)}")

            subprocess.run(["git", "-C", "/root/GPT_monitoring", "pull"], check=True)
            self.log_event("✅ git pull executed successfully.")

            subprocess.run(["systemctl", "restart", "telegram_bot.service"], check=True)
            self.log_event("🔁 telegram_bot.service restarted.")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Webhook received and processed.")

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.log_event(error_msg)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(error_msg.encode())

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Service is running.")

if __name__ == '__main__':
    server_address = ('', 8989)
    httpd = HTTPServer(server_address, WebhookHandler)
    print('Starting webhook listener on port 8989...')
    httpd.serve_forever()
