import http.server
import subprocess
import json

class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Логи для налагодження
        print("Received POST request")
        print("Headers:", self.headers)
        print("Body:", post_data.decode())

        # Виконуємо git pull
        subprocess.call(['git', '-C', '/root/GPT_monitoring', 'pull'])

        # Перезапускаємо сервіс бота
        subprocess.call(['systemctl', 'restart', 'telegram_bot.service'])

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

    def do_GET(self):
        self.send_error(501, "Unsupported method (GET)")

if __name__ == "__main__":
    server_address = ("", 8080)
    httpd = http.server.HTTPServer(server_address, WebhookHandler)
    print("Starting webhook receiver on port 8080...")
    httpd.serve_forever()

