import requests as r
import json
import os
from functools import wraps
from flask import session, request, jsonify, flash, redirect, url_for


url="https://api.github.com/gists/"
gist=os.getenv("gist")
token=os.getenv("token")
headers={'Authorization':'token {}'.format(token)}
params={'scope':'gist'}
fn="data.json"


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "message": "Login required"}), 401
            else:
                flash(f"Login required", "danger")
                return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def getjson():
    con = r.get(f"{url+gist}/raw/{fn}")
    return con.json()

def getpost(num:str):
    con = getjson()
    post = con[num]
    return post

def addpost(name, date, time, content, img):
    con = getjson()
    num = str(len(con)+1)
    con.update({num:
        {
        "num":num,
        "name":name,
        "date":date,
        "time":time,
        "content":content
        }
    })
    payload={
        "description":f"update - {num}",
        "public":False,
        "files":{
            fn:{"content": json.dumps(con,indent=4)}
        }
    }
    res=r.patch(url+gist, headers=headers, params=params, data=json.dumps(payload,indent=4))
    return str(num)


def delpost(num):
    num = str(num)
    data = getjson()
    try:
        con = data.pop(num)
    except KeyError:
        return False
    payload={
            "description":f"update - {int(num)-1}",
            "public":False,
            "files":{
                fn:{"content": json.dumps(data,indent=4)}
                }
        }
    res=r.patch(url+gist, headers=headers, params=params, data=json.dumps(payload,indent=4))
    return con

def check_session():
    if not 'logged_in' in session:
        session["logged_in"]=False
    return session["logged_in"]
