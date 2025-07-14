from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/exec')
def exec_cmd():
    cmd = request.args.get('cmd')
    if not cmd:
        return jsonify({"error": "No command provided"}), 400
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
        return jsonify({"output": output.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.output.decode()}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        repo_dir = "/root/GPT_monitoring"
        # Перехід у директорію з ботом
        os.chdir(repo_dir)
        # Оновлення коду
        pull = subprocess.check_output("git pull", shell=True).decode()
        # Перезапуск бота
        subprocess.check_output("systemctl restart telegram_bot.service", shell=True)
        return jsonify({"status": "ok", "git": pull}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.output.decode()}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)