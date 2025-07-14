import os
import subprocess
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("GPT_CONTROLLER_TOKEN")
BOT_SERVICE = "telegram_bot.service"

app = Flask(__name__)

def check_token():
    token = request.headers.get("Authorization")
print("Отриманий токен:", token)
print("Правильний токен:", ACCESS_TOKEN)
    if not token or token != ACCESS_TOKEN:
        abort(401, description="Unauthorized")

@app.route("/pull", methods=["POST"])
def pull_code():
    check_token()
    try:
        output = subprocess.check_output(["git", "-C", "/root/GPT_monitoring", "pull"], stderr=subprocess.STDOUT)
        return jsonify({"status": "success", "output": output.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "output": e.output.decode()}), 500

@app.route("/restart", methods=["POST"])
def restart_service():
    check_token()
    try:
        subprocess.run(["systemctl", "restart", BOT_SERVICE], check=True)
        return jsonify({"status": "success", "message": f"{BOT_SERVICE} restarted"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/status", methods=["GET"])
def check_status():
    check_token()
    try:
        output = subprocess.check_output(["systemctl", "status", BOT_SERVICE, "--no-pager"], stderr=subprocess.STDOUT)
        return jsonify({"status": "success", "output": output.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "output": e.output.decode()}), 500

@app.route("/logs", methods=["GET"])
def get_logs():
    check_token()
    try:
        output = subprocess.check_output(["journalctl", "-u", BOT_SERVICE, "-n", "50", "--no-pager"], stderr=subprocess.STDOUT)
        return jsonify({"status": "success", "output": output.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "output": e.output.decode()}), 500

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    check_token()
    try:
        subprocess.run(["systemctl", "restart", BOT_SERVICE], check=True)
        return jsonify({"status": "ok", "message": "Webhook received and bot restarted"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8998)
