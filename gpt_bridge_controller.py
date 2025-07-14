import os
import subprocess
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv

# Завантаження .env
load_dotenv(dotenv_path="/root/GPT_monitoring/.env")

ACCESS_TOKEN = os.getenv("GPT_CONTROLLER_TOKEN")
BOT_SERVICE = "telegram_bot.service"

app = Flask(__name__)

# Авторизація
def check_token():
    raw_token = request.headers.get("Authorization")
    if raw_token and raw_token.startswith("Bearer "):
        token = raw_token[len("Bearer "):]  # Видаляє "Bearer "
    else:
        token = raw_token

    if not token or token != ACCESS_TOKEN:
        abort(401, description="Unauthorized")

# /pull
@app.route("/pull", methods=["POST"])
def pull_code():
    check_token()
    try:
        output = subprocess.check_output(["git", "-C", "/root/GPT_monitoring", "pull"], stderr=subprocess.STDOUT)
        return jsonify({"status": "success", "output": output.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "output": e.output.decode()}), 500

# /restart
@app.route("/restart", methods=["POST"])
def restart_service():
    check_token()
    try:
        subprocess.run(["systemctl", "restart", BOT_SERVICE], check=True)
        return jsonify({"status": "success", "message": f"{BOT_SERVICE} restarted"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# /status
@app.route("/status", methods=["GET"])
def check_status():
    check_token()
    try:
        output = subprocess.check_output(["systemctl", "status", BOT_SERVICE, "--no-pager"], stderr=subprocess.STDOUT)
        return jsonify({"status": "success", "output": output.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "output": e.output.decode()}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8998, debug=True)
