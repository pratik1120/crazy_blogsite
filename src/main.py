from flask import Flask, render_template, redirect, url_for, request, session, jsonify, flash
from werkzeug.exceptions import HTTPException
import random
import json
from datetime import datetime
import os
from .cogs.utils import *
from .cogs import api


app = Flask(__name__)
app.secret_key = os.getenv("secretkey")
app.register_blueprint(api.api)
password=os.getenv("password")


@app.route("/")
def index():
    posts=dict(reversed(getjson().items()))
    return render_template("index.html",posts=posts,total=len(posts))

@app.route("/post/<num>")
def post(num):
    try:
        post = getpost(num)
    except:
        return render_template("404.html")
    return render_template("post.html",name=post["name"],date=post["date"],time=post["time"],content=post["content"])


@app.route("/post")
def onlypost():
    return redirect(url_for("index"))


@app.route("/new",methods=["GET","POST"])
@login_required
def addnew():
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session['logged_in']==True:
        flash("already logged in")
        return redirect(url_for("index"))
    if request.method == 'POST':
        if request.form['password'] != password:
            flash('invalid password.')
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    flash(f"logged in successfully")
    return render_template('login.html')


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


if __name__=="__main__":
    app.run(debug=False)

