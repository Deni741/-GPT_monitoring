import hmac
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

PORT = 8080
GITHUB_SECRET = b''  # За бажанням можна задати секрет

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Перевірка шляху
        if self.path != "/webhook":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return

        # Зчитуємо вхідні дані
        content_length = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_length)

        # Перевірка HMAC (опціонально)
        signature = self.headers.get('X-Hub-Signature-256')
        if GITHUB_SECRET and signature:
            hash_object = hmac.new(GITHUB_SECRET, post_body, hashlib.sha256)
            expected_signature = f"sha256={hash_object.hexdigest()}"
            if not hmac.compare_digest(expected_signature, signature):
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Invalid signature")
                return

        # Якщо все ок – оновлюємо код і перезапускаємо бот
        try:
            subprocess.run(["git", "-C", "/root/GPT_monitoring", "pull"], check=True)
            subprocess.run(["systemctl", "restart", "telegram_bot.service"], check=True)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Updated and restarted")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), WebhookHandler)
    print(f"Listening on port {PORT}...")
    server.serve_forever()
