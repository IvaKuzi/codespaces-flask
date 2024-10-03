# uncommen next two line for production 
#import eventlet
#eventlet.monkey_patch()

from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

# Track connection
@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')

# Track disconnection
@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')
    # Log or take action when a client disconnects

@socketio.on('message-submit')
def handle_message(payload):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    user = payload['user']
    content = payload['content']
    payload['timestamp'] = timestamp
    print(f'({timestamp}) Message from {user} received: {content}')
    socketio.emit('new-message', payload)
    with open('messages.txt', 'a') as file:
        file.write(f"{payload},\n")
    

if __name__ == '__main__':
    socketio.run(app, debug=True)