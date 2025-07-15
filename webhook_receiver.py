from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        # Логування отриманого payload (для відладки)
        try:
            data = json.loads(post_data)
            print("Received Webhook Payload:")
            print(json.dumps(data, indent=4))
        except json.JSONDecodeError:
            print("Invalid JSON received")

        # Автоматичне оновлення з GitHub
        try:
            subprocess.run(["git", "-C", "/root/GPT_monitoring", "pull"], check=True)
            subprocess.run(["systemctl", "restart", "telegram_bot.service"], check=True)
            print("🔄 Репозиторій оновлено і бот перезапущено.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Помилка при оновленні або перезапуску: {e}")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Webhook received and processed.')

def run():
    server_address = ('', 8989)
    httpd = HTTPServer(server_address, WebhookHandler)
    print("✅ Webhook server running on port 8989...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
