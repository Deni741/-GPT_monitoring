#!/usr/bin/env python3

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

LOG_FILE = "/root/GPT_monitoring/update_log.txt"
REPO_DIR = "/root/GPT_monitoring"
SERVICE_NAME = "telegram_bot.service"

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{now}] GitHub Webhook received\n"

        try:
            os.chdir(REPO_DIR)
            pull_result = os.popen("git pull origin main").read()
            log_entry += f"[{now}] Git pull:\n{pull_result}\n"
        except Exception as e:
            log_entry += f"[{now}] Git pull error: {e}\n"

        try:
            restart_result = os.popen(f"systemctl restart {SERVICE_NAME}").read()
            log_entry += f"[{now}] Restart:\n{restart_result}\n"
        except Exception as e:
            log_entry += f"[{now}] Restart error: {e}\n"

        with open(LOG_FILE, "a") as f:
            f.write(log_entry + "\n")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Webhook received and processed.\n")

if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, WebhookHandler)
    print("Starting webhook receiver on port 8080...")
    httpd.serve_forever()
