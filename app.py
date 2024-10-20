from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_socketio import SocketIO

from utils.chat_lib import getHistory, appendMessage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet') # * Not Recommended for Production

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Dictionary to store active connections
active_connections = {}

def custom_render(url):
    if 'username' in session:
        username = session['username']
    else:
        username = ''
    return render_template(url, template_name=url, username=username)

@app.route("/")
def index():
    return custom_render("index.html")

@app.route("/home")
def home():
    return redirect( url_for("index") )

@app.route("/ueber-uns")
def about():
    return custom_render("about.html")

@app.route("/preise")
def preise():
    return custom_render("prices.html")

@app.route("/kontakt", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        print(request.form)
        print(f"Name: {request.form['name']}")
        print(f"E-Mail: {request.form['email']}")
    return custom_render("contact.html")

@app.route("/chat")
def chat():
    return custom_render("chat.html")
    
# Track connection
@socketio.on('connect')
def handle_connect():
    data = getHistory('messages.json')
    socketio.emit('all-messages', data)
    
    sid = request.sid # Get the session ID of the connected client
    ip = request.remote_addr
    username = session['username']
    active_connections[sid] = { "ip" : ip, "username" : username }

    # Update a list of usernames
    usernames = [entry['username'] for entry in active_connections.values()]
    socketio.emit('update-users', usernames)

    print(f"Client connected: {sid} (IP: {ip}) (username: {username})")
    
    
# Track disconnection
@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid  # Get the session ID of the disconnected client
    connection = active_connections.pop(sid, None)  # Remove the client from the active connections list
    ip = connection['ip']
    username = connection['username']

    # Update a list of usernames
    usernames = [entry['username'] for entry in active_connections.values()]
    socketio.emit('update-users', usernames)

    print(f'Client disconnected: {sid}  (IP: {ip}) (username: {username})')

# Track message submission
@socketio.on('message-submit')
def handle_message(payload):
    data = appendMessage(payload)
    socketio.emit('all-messages', data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        flash(f"User {username} logged in")
        return redirect('/')
    else:
        return custom_render('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    username = session.pop('username', None)
    flash(f"User {username} logged out")
    return redirect(request.referrer or '/')

# Generic page
@app.route("/<address>")
def generic(address):
    if 'username' in session:
        username = session['username']
    else:
        username = ''
    return render_template("generic.html", title=address, template_name="generic.html", username=username)
