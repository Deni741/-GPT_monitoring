from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return 'GPT Bridge Agent is active.'

@app.route('/exec', methods=['GET'])
def exec_cmd():
    cmd = request.args.get('cmd')
    if not cmd:
        return '? No command provided', 400
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"? Error:\n{e.output.decode('utf-8')}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)