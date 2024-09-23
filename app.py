from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return redirect( url_for("index") )

@app.route("/ueber-uns")
def about():
    return render_template("about.html")

@app.route("/preise")
def preise():
    return render_template("prices.html")

@app.route("/kontakt", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        print(request.form)
        print(f"Name: {request.form['name']}")
        print(f"E-Mail: {request.form['email']}")
    return render_template("contact.html")

# generic page
@app.route("/<address>")
def generic(address):
    return render_template("generic.html", title=address)
    