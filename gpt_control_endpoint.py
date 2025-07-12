from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

SERVICE_NAME = "gpt_telegram_bot.service"

def run_command(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode("utf-8")
        return output
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf-8")

@app.route("/exec")
def exec_command():
    cmd = request.args.get("cmd", "")
    if not cmd:
        return jsonify({"error": "Missing command"}), 400
    output = run_command(cmd)
    return jsonify({"output": output})

@app.route("/status")
def status():
    output = run_command(f"systemctl status {SERVICE_NAME}")
    return jsonify({"status": output})

@app.route("/restart")
def restart():
    output = run_command(f"systemctl restart {SERVICE_NAME}")
    return jsonify({"restart": output})

@app.route("/logs")
def logs():
    output = run_command(f"journalctl -u {SERVICE_NAME} --no-pager -n 50")
    return jsonify({"logs": output})

@app.route("/pull")
def git_pull():
    output = run_command("cd /root/GPT_monitoring && git pull")
    return jsonify({"git_pull": output})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8989)