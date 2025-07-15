from http.server import BaseHTTPRequestHandler, HTTPServer

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

server_address = ('', 8089)
httpd = HTTPServer(server_address, WebhookHandler)
print("Webhook receiver running on port 8089...")
httpd.serve_forever()
