# app.py
from flask import Flask,request,make_response,jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as TJSS
import json
from controller import(user,record,people,e,work,mo,invite,history)
from model.db import mongo
from controller.util import checkParm, ret
from model import (userModel)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ABCDEFhijklm'
app.config["MONGO_URI"] = "mongodb+srv://numbone112:i3PO8xrZj1KRwz83@cluster0.5rqnhen.mongodb.net/mcubed"
mongo.init_app(app) # initialize here!
print(type(mongo))
print((mongo.db.name))
app.register_blueprint(user.userAPI)
app.register_blueprint(people.peopleProfile)
app.register_blueprint(record.recordAPI)
app.register_blueprint(e.eAPI)
app.register_blueprint(work.workProfile)
app.register_blueprint(mo.moProfile)
app.register_blueprint(invite.inviteAPI)
app.register_blueprint(history.historyAPI)


@app.route('/', methods=["POST"])
def line():
    return "ok"


@app.route('/get', methods=["GET","OPTIONS"])
def home():
    return 'good from backend'

@app.route("/login", methods=["POST"])
def login():
    content = request.json
    id = content['id']
    password = content["password"]
    data = userModel.login(id, password)
    print((data))
    print("app")
    result = {"success": False, "data": data}
    if len(data) == 1:
        s = TJSS(app.config['SECRET_KEY'], expires_in=3600)
        token = s.dumps({'username': id}).decode('utf-8')
        result["mes"] = "登入成功"
        result["success"] = True
        result['data']={"user":result['data'],"token":token}
        return ret(result)
    elif len(data) == 0:
        result["mes"] = "登入失敗"
    else:
        result["mes"] = "登入異常"
    return ret(result)
    


@app.route("/sign", methods=["POST"])
def sign():
    content = request.json
    cond = ["id", "password", "birthday", "name","phone","sex","role","height"]
    result = {"success": False, "mes": ""}
    t = checkParm(cond, content)
    print(t)
    if(isinstance(t, dict)):
        hasUser = userModel.hasUser(t["id"])
        if len(hasUser) > 0:
            result["mes"] = "重複帳號"
        else:
            data = userModel.sign(t)
            if(data.inserted_id):
                result["mes"] = "註冊成功"
                result["success"] = True
                if t["role"]==2:
                    p_con=["height"]
                    p_t=checkParm(p_con,content)
                    if(isinstance(p_t,dict)):
                        p_t["disease"] = [""]
                        p_t["sets"] = [5,5,5]
                        p_t["p_id"] = t["id"]
                        print(p_t)
                        c = userModel.addpatient(p_t)
                        if(len(c) >0):
                            result["mes"]+=":but something error"
            else:
                result["mes"] = "註冊異常"
    else:
        result["mes"] = "請填畢所有資料"
    return ret(result)
    
