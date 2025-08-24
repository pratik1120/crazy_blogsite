from flask import Flask, render_template, redirect, url_for, request, session, jsonify, flash
from werkzeug.exceptions import HTTPException
import random
import json
from datetime import datetime
import os
from .cogs.utils import *

app = Flask(__name__)
app.secret_key = os.getenv("secretkey")
password=os.getenv("secretkey")


def check_session():
    if not 'logged_in' in session:
        session["logged_in"]=False
    return session["logged_in"]


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/blog")
def blog():
    posts=dict(reversed(getjson().items()))
    return render_template("blog.html",posts=posts)


@app.route("/blog/post/<num>")
def post(num):
    try:
        post = getpost(num)
    except:
        return render_template("404.html")
    return render_template("post.html",name=post["name"],date=post["date"],time=post["time"],content=post["content"],img=post["img"])



@app.route("/blog/new",methods=["GET","POST"])
def addnew():
    if session['logged_in']==False:
        return redirect(url_for("login"))
    if request.method=="GET":
        return render_template("new.html",session=session)
    name = request.form["title"]
    print(request.form.get("dateField"), request.form.get("timeField"))
    date = request.form['dateField']
    time = request.form['timeField']
    content = request.form["content"]
    img = "https://random.imagecdn.app/400/250"
    num = addpost(name,date,time,content,img)
    return redirect(url_for("index"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session['logged_in']==True:
        # flash("already logged in")
        return redirect(url_for("index",session=session))
    error = None
    if request.method == 'POST':
        if request.form['password'] != password:
            error = 'Invalid.'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    # flash(f"logged in, welcome {request.form['username']}")
    return render_template('login.html', error=error,session=session)


@app.route('/logout')
def logout():
    session.clear()
    # flash("logged out.")
    return redirect(url_for('index'))


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
        if code==404:
            return render_template("404.html",session=session)
    return jsonify(error=str(e)), code

@app.before_request
def b4req():
    check_session()

if __name__=="__main__":
    app.run()

