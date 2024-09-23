from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def hello_world():
    #return render_template("index.html", title="Hello")
    print("/")
    return render_template("hello_world.html")

@app.route("/home")
def home():
    print("/home")
    return redirect( url_for("hello_world") )

@app.route("/about")
def about():
    return "About Us"

@app.route("/preise")
def preise():
    return "<h1>Unsere Tarife</h1>"

#impressum
#preise
#kontakte
#teilen
#galerie