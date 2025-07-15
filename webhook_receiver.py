from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        payload = self.rfile.read(content_length).decode('utf-8')
        print("Received payload:")
        print(payload)

        # Відповідь GitHub
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Server is running (GET ignored)')

if __name__ == "__main__":
    server_address = ("0.0.0.0", 8989)
    httpd = HTTPServer(server_address, WebhookHandler)
    print("Webhook server running on port 8989...")
    httpd.serve_forever()
