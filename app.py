from flask import Flask, render_template, redirect, url_for

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

@app.route("/kontakte")
def contact():
    return render_template("contact.html")

