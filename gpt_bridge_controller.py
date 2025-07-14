import os
import subprocess
from flask import Flask, request, jsonify, abort

from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.getenv("GPT_CONTROLLER_TOKEN")

app = Flask(__name__)

# 🔒 Токен-захист усіх запитів
def check_token():
    token = request.headers.get("Authorization")
    if not token or token != ACCESS_TOKEN:
        abort(401, description="Unauthorized")

# 📥 Pull із GitHub
@app.route("/pull", methods=["POST"])
def pull_code():
    check_token()
    try:
        os.chdir("/root/GPT_monitoring")
        subprocess.run(["git", "pull"], check=True)
        subprocess.run(["systemctl", "restart", "telegram_bot.service"], check=True)
        return jsonify({"status": "ok", "message": "Код оновлено й бот перезапущено"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 📖 Читання файлу
@app.route("/read", methods=["GET"])
def read_file():
    check_token()
    filepath = request.args.get("file")
    if not filepath:
        return jsonify({"error": "No file specified"}), 400
    try:
        with open(filepath, "r") as f:
            content = f.read()
        return jsonify({"file": filepath, "content": content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 📝 Запис у файл
@app.route("/write", methods=["POST"])
def write_file():
    check_token()
    data = request.get_json()
    filepath = data.get("file")
    content = data.get("content")
    if not filepath or content is None:
        return jsonify({"error": "Missing file or content"}), 400
    try:
        with open(filepath, "w") as f:
            f.write(content)
        return jsonify({"status": "success", "message": f"File {filepath} updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🗑️ Видалення файлу
@app.route("/delete", methods=["DELETE"])
def delete_file():
    check_token()
    filepath = request.args.get("file")
    if not filepath:
        return jsonify({"error": "No file specified"}), 400
    try:
        os.remove(filepath)
        return jsonify({"status": "success", "message": f"File {filepath} deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ▶️ Запуск сервера
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8998, debug=True)
