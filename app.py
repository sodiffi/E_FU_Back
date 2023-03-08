# app.py
from flask import Flask,request
from itsdangerous import TimedJSONWebSignatureSerializer as TJSS

from controller import(user,record,people)
from model.db import mongo
from controller.util import checkParm, ret
from model import (userModel)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ABCDEFhijklm'
app.config["MONGO_URI"] = "mongodb+srv://numbone112:i3PO8xrZj1KRwz83@cluster0.5rqnhen.mongodb.net/efu"
mongo.init_app(app) # initialize here!
print(type(mongo))
print((mongo.db.name))
app.register_blueprint(user.userAPI)
app.register_blueprint(people.peopleProfile)
app.register_blueprint(record.recordAPI)


@app.route('/', methods=["POST"])
def line():
    return "ok"


@app.route('/get', methods=["GET","OPTIONS"])
def home():
    return 'good from backend'

@app.route("/login", methods=["POST"])
def login():
    content = request.json
    account = content['account']
    password = content["password"]
    data = userModel.login(account, password)
    print((data))
    result = {"success": False, "data": data}
    if len(data) == 1:
        s = TJSS(app.config['SECRET_KEY'], expires_in=3600)
        token = s.dumps({'username': account}).decode('utf-8')
        result["mes"] = "登入成功"
        
        result["success"] = True
        response = jsonify({
            'access_token': token,
            'token_type': 'Bearer',
            'expires_in': 3600
        })
        response.headers['Cache-Control'] = 'no-store'
        response.headers['Pragma'] = 'no-cache'

        return response
    elif len(data) == 0:
        result["mes"] = "登入失敗"
    else:
        result["mes"] = "登入異常"
    return ret(result)
    


@app.route("/sign", methods=["POST"])
def sign():
    content = request.json
    cond = ["account", "password", "age", "sex","name"]
    result = {"success": False, "mes": ""}
    t = checkParm(cond, content)
    print(t)
    if(isinstance(t, dict)):
        hasUser = userModel.hasUser(t["account"])
        if len(hasUser) > 0:
            result["mes"] = "重複帳號"
        else:
            data = userModel.sign(t)

            if(data.inserted_id):
                result["mes"] = "註冊成功"
                result["success"] = True
            else:
                    result["mes"] = "註冊異常"

    else:
        result["mes"] = "請填畢所有資料"
    return ret(result)
    return ret(result)
