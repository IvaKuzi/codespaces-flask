from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO

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
    # You can log or take action when a client connects
    #emit('message', {'data': 'Connected to server!'})
    socketio.emit('hello')

# Track disconnection
@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')
    # Log or take action when a client disconnects

if __name__ == '__main__':
    socketio.run(app, debug=True)