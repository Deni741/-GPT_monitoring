from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route("/read", methods=["GET"])
def read_file():
    filepath = request.args.get("file")
    if not filepath:
        return jsonify({"error": "No file specified"}), 400
    try:
        with open(filepath, "r") as f:
            content = f.read()
        return jsonify({"file": filepath, "content": content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/write", methods=["POST"])
def write_file():
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

@app.route("/delete", methods=["DELETE"])
def delete_file():
    filepath = request.args.get("file")
    if not filepath:
        return jsonify({"error": "No file specified"}), 400
    try:
        os.remove(filepath)
        return jsonify({"status": "deleted", "file": filepath}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/exec", methods=["POST"])
def exec_command():
    data = request.get_json()
    command = data.get("cmd")
    if not command:
        return jsonify({"error": "No command provided"}), 400
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return jsonify({"output": output}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.output}), 500

@app.route("/restart", methods=["POST"])
def restart_service():
    data = request.get_json()
    service = data.get("service")
    if not service:
        return jsonify({"error": "No service specified"}), 400
    try:
        subprocess.run(["systemctl", "restart", service], check=True)
        return jsonify({"status": f"Service {service} restarted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8998)
