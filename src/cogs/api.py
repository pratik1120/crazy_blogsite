from flask import Blueprint
from flask import request, render_template, redirect, url_for, session, jsonify
from .utils import addpost, getpost, getjson, delpost
from datetime import datetime
import os

api = Blueprint('api', __name__, url_prefix="/api")


@api.route("/")
def apindex():
    return redirect(url_for("docs"))


@api.route("/new",methods=["POST"])
def new():
    if session["logged_in"]==False:
        user = request.json.get("username")
        passwd = request.json.get("password")
        if user is None or passwd is None:
            return jsonify(error="not logged in. username and pasword required")
        elif user != os.getenv("username") or passwd != os.getenv("password"):
            return jsonify(error="not logged in. username or password invalid")
        else:
            session["logged_in"]=True
    post = request.get_json(force=True)
    name=post.get("name")
    date=post.get("date") or datetime.now().strftime("%B %d, %Y").lower()
    time=post.get("time") or datetime.now().strftime("%H.%M %p").lower()
    content=post.get("content")
    img=post.get("img") or "https://random.imagecdn.app/400/250"
    if name is None:
        return {"error":"name field is required"}
    if content is None:
        return {"error":"content field is required"}
    num = addpost(name, date, time, content, img)
    return {"id":num}


@api.route("/get")
def get():
    num = request.args.get("id")
    if num is None:
        return getjson()
    return getpost(num)


@api.route("/del")
def _del():
    num = request.args.get("id")
    if num is None:
        return jsonify(error="`id` is required")
    con = delpost(num)
    if isinstance(con,bool):
        return jsonify(error=f"no such `id={num}` exists")
    return jsonify(message=f"This entry of `id={num}` has been deleted", con=con)
    