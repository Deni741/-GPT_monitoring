from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
import importlib
import os
import urllib.parse

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/':
            length = int(self.headers.get('content-length'))
            data = self.rfile.read(length)
            print("Webhook received:", data.decode())

            # Pull оновлення з GitHub
            result = subprocess.run(['git', '-C', '/root/GPT_monitoring', 'pull'], stdout=subprocess.PIPE)
            print(result.stdout.decode())

            # Перезапуск systemd-сервісу
            subprocess.run(['systemctl', 'restart', 'telegram_bot.service'])
            print("Service restarted")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Updated and restarted')
        else:
            self.send_response(404)
            self.end_headers()

def do_GET(self):
        if self.path.startswith('/cmd'):
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            cmd = query.get('cmd', [None])[0]

            if cmd in ['status', 'restart', 'logs', 'pull']:
                try:
                    module = importlib.import_module(f"actions.{cmd}")
                    output = module.run()
                except Exception as e:
                    output = f"❌ Помилка при виконанні {cmd}: {e}"
            else:
                output = "❌ Невідома команда"

            self.send_response(200)
            self.end_headers()
            self.wfile.write(output.encode())
        else:
            self.send_response(404)
            self.end_headers()
