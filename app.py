from flask import Flask, render_template, redirect, url_for, request, session
from flask import flash
from flask_socketio import SocketIO



app = Flask(__name__)
app.config['SECRET_KEY'] = 'ssdasdmn,a.fgj.arshklgwewet'
socketio = SocketIO(app)

def custom_render(url):
    if 'username' in session:
        username = session['username']
    else:
        username = ''
    return render_template(url, user=username)

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

@app.route("/login", methods=['POST', 'GET'])
def login():
    username = ''
    if request.method == 'POST':
        username = request.form['username']
        print(username)
        session['username'] = username
        if username == "":
            flash(f'username incorrect')
        else:
            flash(f'{username} eingelogt')
    return custom_render("login.html")

@app.route("/logout")
def logout():
    username = session.pop('username', None)
    flash(f'{username} ausgelogt')
    return redirect('/')
    

@app.route("/kontakt", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        print(request.form)
        name = request.form['name']
        email = request.form['email']
        with open('submissions.txt', 'a') as file:
            file.write(f"Name: {name}, email: {email}\n")
    return custom_render("contact.html")

# generic page
@app.route("/<address>")
def generic(address):
    return render_template("generic.html", title=address)

@app.route("/chat")
def chat():
    return custom_render("chat.html")
    
# Track connection
@socketio.on('connect')
def handle_connect():
    sid = request.sid # session id
    ip = request.remote_addr # IP
    username = session['username']
    print(f"Client connected: {sid} (IP: {ip}) (username: {username})")

# Track disconnection
@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid # session id
    ip = request.remote_addr # IP
    username = session['username']
    print(f'Client disconnected: {sid}  (IP: {ip}) (username: {username})')