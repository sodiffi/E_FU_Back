# app.py
from flask import Flask, request, make_response, jsonify, abort
import requests
from itsdangerous import TimedJSONWebSignatureSerializer as TJSS
import json
from controller import user, record, people, e, work, mo, invite, history, plan, home
from model.db import mongo
from controller.util import checkParm, ret
from model import userModel
from model.lineModule import lineModule

#  -----------------------
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage


app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCDEFhijklm"
app.config[
    "MONGO_URI"
] = "mongodb+srv://numbone112:i3PO8xrZj1KRwz83@cluster0.5rqnhen.mongodb.net/mcubed"
mongo.init_app(app)  # initialize here!
print(type(mongo))
print((mongo.db.name))
app.register_blueprint(home.homeAPI)
app.register_blueprint(user.userAPI)
app.register_blueprint(people.peopleProfile)
app.register_blueprint(record.recordAPI)
app.register_blueprint(e.eAPI)
app.register_blueprint(work.workProfile)
app.register_blueprint(mo.moProfile)
app.register_blueprint(invite.inviteAPI)
app.register_blueprint(history.historyAPI)
app.register_blueprint(plan.planAPI)

line_bot_api = LineBotApi(
    "8rkciRRjGhrEa+SAabMXVm9OslLiA6QE5wkd5RpGu9iYdrNerBZVynJQXqR+i4jfMuAzo7YBy/4NGC8jFN6oaGSnh+y1R6UVLVOSuF/jebICvPy0+UWQZqzcEG1to8MFYef/7gdvJI+uSeNdZGfkGwdB04t89/1O/w1cDnyilFU="
)
handler = WebhookHandler("dd50fb19fc5fbf0df7f2d6caa5ee6f7f")


@app.route("/", methods=["POST"])
def line():
    return "ok"


@app.route("/get", methods=["GET", "OPTIONS"])
def test():
    return "good from backend"


@app.route("/login", methods=["POST"])
def login():
    content = request.json
    id = content["id"]
    password = content["password"]
    data = userModel.login(id, password)
    print((data))
    print("app")
    result = {"success": False, "data": data}
    if len(data) == 1:
        s = TJSS(app.config["SECRET_KEY"], expires_in=3600)
        token = s.dumps({"username": id}).decode("utf-8")
        result["mes"] = "登入成功"
        result["success"] = True
        result["data"] = {"user": result["data"], "token": token}
        return ret(result)
    elif len(data) == 0:
        result["mes"] = "登入失敗"
    else:
        result["mes"] = "登入異常"
    return ret(result)


@app.route("/sign", methods=["POST"])
def sign():
    content = request.json
    cond = ["id", "password", "birthday", "name", "phone", "sex", "role", "height"]
    result = {"success": False, "mes": ""}
    t = checkParm(cond, content)
    print(t)
    if isinstance(t, dict):
        hasUser = userModel.hasUser(t["id"])
        if len(hasUser) > 0:
            result["mes"] = "重複帳號"
        else:
            data = userModel.sign(t)
            if data.inserted_id:
                result["mes"] = "註冊成功"
                result["success"] = True
                if t["role"] == 2:
                    p_con = ["height"]
                    p_t = checkParm(p_con, content)
                    if isinstance(p_t, dict):
                        p_t["disease"] = [""]
                        p_t["sets"] = [5, 5, 5]
                        p_t["p_id"] = t["id"]
                        print(p_t)
                        c = userModel.addpatient(p_t)
                        if len(c) > 0:
                            result["mes"] += ":but something error"
            else:
                result["mes"] = "註冊異常"
    else:
        result["mes"] = "請填畢所有資料"
    return ret(result)


#  -----------------------
@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)
    print(request.headers["X-Line-Signature"])
    # print(body.events.source.userId)
    print(body)

    
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        return "invalid singature"
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    data = lineModule.handle_messenge(event)
    line_bot_api.reply_message(event.reply_token, data)


