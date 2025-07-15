from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            payload = json.loads(post_data.decode('utf-8'))
            print("Received webhook payload:", payload)

            # Запуск git pull та перезапуск бота
            subprocess.run(["git", "-C", "/root/GPT_monitoring", "pull"])
            subprocess.run(["systemctl", "restart", "telegram_bot.service"])

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Webhook received and processed.')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Service is running.')

if __name__ == '__main__':
    server_address = ('', 8989)
    httpd = HTTPServer(server_address, WebhookHandler)
    print('Starting webhook listener on port 8989...')
    httpd.serve_forever()
