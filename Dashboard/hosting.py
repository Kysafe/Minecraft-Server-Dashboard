from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://Enter domain"}})

current_server = None
server_screens = {'serwermc': 'serwermc', 'serwermc2': 'serwermc2'}

def is_server_running(server_name):
    screen_name = server_screens.get(server_name, None)
    if screen_name:
        try:
            output = subprocess.check_output(f"screen -ls | grep {screen_name}", shell=True)
            if screen_name in output.decode():
                return True
        except subprocess.CalledProcessError:
            return False
    return False

@app.route('/server-status', methods=['GET'])
def server_status():
    status_serwermc = 'online' if is_server_running('serwermc') else 'offline'
    status_serwermc2 = 'online' if is_server_running('serwermc2') else 'offline'

    return jsonify({
        "serwermc": status_serwermc,
        "serwermc2": status_serwermc2
    })

def are_players_online(server_name):
    if server_name == 'serwermc':
        log_file = 'Enter minecraft location/logs/latest.log'
    elif server_name == 'serwermc2':
        log_file = 'Enter minecraft location/logs/latest.log'

    with open(log_file, 'r') as f:
        lines = f.readlines()
        for line in reversed(lines):
            if 'logged in' in line or 'joined the game' in line:
                return True
            if 'logged out' in line or 'left the game' in line:
                return False
    return False

@app.route('/start-server/<server_name>')
def start_server(server_name):
    global current_server

    if current_server and is_server_running(current_server):
        return jsonify({'error': 'Inny serwer jest już uruchomiony!'}), 400

    if server_name == 'serwermc':
        command = 'screen -dmS serwermc bash -c "cd Enter minecraft location && ./start.sh"'
    elif server_name == 'serwermc2':
        command = 'screen -dmS serwermc2 bash -c "cd Enter minecraft location && ./start.sh"'
    else:
        return jsonify({'error': 'Nieznany serwer'}), 400

    subprocess.call(command, shell=True)
    current_server = server_name

    return jsonify({'message': f'{server_name} został uruchomiony'}), 200

def stop_minecraft_server(server_name):
    if server_name == 'serwermc':
        command = 'screen -S serwermc -X stuff "stop\n"'
    elif server_name == 'serwermc2':
        command = 'screen -S serwermc2 -X stuff "stop\n"'
    else:
        return False

    subprocess.call(command, shell=True)
    time.sleep(5)
    subprocess.call(f'screen -S {server_name} -X quit', shell=True)

    return True

@app.route('/stop-server')
def stop_server():
    global current_server

    if current_server and is_server_running(current_server):
        if are_players_online(current_server):
            return jsonify({'error': 'Nie można wyłączyć serwera, gracze są zalogowani!'}), 400

        stop_minecraft_server(current_server)
        current_server = None
        return jsonify({'message': 'Serwer został wyłączony'}), 200
    else:
        return jsonify({'error': 'Żaden serwer nie jest uruchomiony!'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
