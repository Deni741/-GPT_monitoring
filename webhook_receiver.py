from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import urllib.parse

class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)
        action = query.get('do', [None])[0]

        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        if action == "pull":
            output = subprocess.getoutput("cd /root/GPT_monitoring && git pull")
            self.wfile.write(output.encode("utf-8"))

        elif action == "restart":
            output = subprocess.getoutput("systemctl restart telegram_bot.service")
            self.wfile.write(b"Telegram bot restarted.\n")
            self.wfile.write(output.encode("utf-8"))

        elif action == "status":
            output = subprocess.getoutput("systemctl status telegram_bot.service --no-pager")
            self.wfile.write(output.encode("utf-8"))

        elif action == "logs":
            output = subprocess.getoutput("tail -n 50 /root/GPT_monitoring/update_log.txt")
            self.wfile.write(output.encode("utf-8"))

        else:
            self.wfile.write(b"Invalid or missing 'do' parameter.\n")

def run(server_class=HTTPServer, handler_class=WebhookHandler, port=8989):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting webhook server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
