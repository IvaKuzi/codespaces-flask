from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        print(session)
        return redirect('/')
    else:
        return custom_render('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(request.referrer or '/')

# generic page
@app.route("/<address>")
def generic(address):
    return custom_render("generic.html", title=address)
    