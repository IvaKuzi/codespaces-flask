from flask import Flask, render_template, request
from flask_socketio import SocketIO
import time, json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

def getHistory(file_name):
    data = []
    # Open the existing file and read its content
    try:
        with open(file_name, 'r') as json_file:
            # Check if file is empty
            try:
                data = json.load(json_file)  # Load existing data
            except json.JSONDecodeError:
                data = []  # If file is empty or invalid, start with an empty list
    except FileNotFoundError:
        data = []  # If file does not exist, start with an empty list

    if not isinstance(data, list):
        data = [] # If file is empty or invalid, start with an empty list

    return data

# Track connection
@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')
    file_name = 'messages.json'
    data = getHistory(file_name)
    socketio.emit('all-messages', data)

# Track disconnection
@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')

# Track message submission
@socketio.on('message-submit')
def handle_message(payload):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    user = payload['user']
    content = payload['content']
    payload['timestamp'] = timestamp
    print(f'({timestamp}) Message from {user} received: {content}')

    file_name = 'messages.json'
    data = getHistory(file_name)
    data.append(payload)
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)  # Write updated data back to the file
    socketio.emit('all-messages', data)

if __name__ == '__main__':
    print(f"Debug mode: {app.debug}")
    if app.debug:
        socketio.run(app, debug=True)
    else:
        socketio.run(app)
