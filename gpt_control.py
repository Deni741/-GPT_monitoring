from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import importlib
import os

ACTIONS_DIR = os.path.join(os.path.dirname(__file__), "actions")

class CommandHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/cmd":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return

        params = urllib.parse.parse_qs(parsed.query)
        action = params.get("do", [None])[0]

        if not action:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing 'do' parameter")
            return

        try:
            module = importlib.import_module(f"actions.{action}")
            result = module.run()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(result.encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode("utf-8"))

def run(server_class=HTTPServer, handler_class=CommandHandler):
    server_address = ("", 8989)
    httpd = server_class(server_address, handler_class)
    print("GPT Control Server running on port 8989")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
