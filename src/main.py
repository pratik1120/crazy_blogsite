from flask import Flask, render_template, redirect, url_for, request, session, jsonify, flash
from werkzeug.exceptions import HTTPException
import random
import json
from datetime import datetime
import os
from .cogs.utils import *
from .cogs import api


app = Flask(__name__)
app.secret_key = os.urandom()
app.register_blueprint(api.api)
username=os.getenv("username")
password=os.getenv("password")


@app.route("/")
def index():
    posts=dict(reversed(getjson().items()))
    try:
        return render_template("index.html",posts=posts,total=len(posts))
    except:
        return render_template("index.html",posts=posts,total=len(posts))


@app.route("/docs")
def docs():
    return render_template("docs.html")

@app.route("/post/<num>")
def post(num):
    try:
        post = getpost(num)
    except:
        return render_template("404.html")
    return render_template("post.html",name=post["name"],date=post["date"],time=post["time"],content=post["content"],img=post["img"])


@app.route("/post")
def onlypost():
    return redirect(url_for("rand"))


@app.route("/new",methods=["GET","POST"])
def addnew():
    if session['logged_in']==False:
        return redirect(url_for("login"))
    if request.method=="GET":
        return render_template("new.html")
    name = request.form["title"]
    print(request.form.get("dateField"), request.form.get("timeField"))
    date = request.form['dateField']
    time = request.form['timeField']
    content = request.form["content"]
    img = "https://random.imagecdn.app/400/250"
    num = addpost(name,date,time,content,img)
    return redirect(url_for("index"))


@app.route("/random")
def rand():
    postcnt = len(getjson())
    return redirect(f"/post/{random.choice(range(1,postcnt+1))}")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session['logged_in']==True:
        flash("already logged in")
        return redirect(url_for("index"))
    error = None
    if request.method == 'POST':
        if request.form['username'] != username or request.form['password'] != password:
            error = 'Invalid.'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    flash(f"logged in, welcome {request.form['username']}")
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    flash("logged out.")
    return redirect(url_for('index'))


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
        if code==404:
            return render_template("404.html")
    return jsonify(error=str(e)), code

@app.before_request
def b4req():
    check_session() #creates session['logged_in'] if doesnt exist

if __name__=="__main__":
    app.run("0.0.0.0")

