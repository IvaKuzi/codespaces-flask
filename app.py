from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("hello.html",name="world")

@app.route("/<title>")
def index(title):
    return render_template("hello.html",name=title)


