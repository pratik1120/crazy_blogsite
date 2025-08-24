import requests as r
import json
import os

jsfile=os.getenv("jsfile")
url="https://api.github.com/gists/"
gist=os.getenv("gist")
token=os.getenv("token")
headers={'Authorization':'token {}'.format(token)}
params={'scope':'gist'}
fn="data.json"


def getjson():
    con = r.get(f"{jsfile}/raw/{fn}")
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
        "content":content,
        "img": img
        }
    })
    payload={
            "description":f"yap dump - {num}",
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
            "description":f"yap dump - {int(num)-1}",
            "public":False,
            "files":{
                fn:{"content": json.dumps(data,indent=4)}
                }
        }
    res=r.patch(url+gist, headers=headers, params=params, data=json.dumps(payload,indent=4))
    return con


def getjoke():
    con = r.get("https://api.chucknorris.io/jokes/random").json()
    joke = con['value']
    return joke

def check_session():
    if not 'logged_in' in session:
        session["logged_in"]=False
    return session["logged_in"]
