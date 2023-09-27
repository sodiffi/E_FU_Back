from flask import Blueprint, request,Response
from model import moModel
from .util import checkParm, ret, quickRet
from model.db import mongo

moProfile = Blueprint("mo", __name__, url_prefix="/mo")

@moProfile.route("/<user_id>", methods=["GET"])
def get(user_id):
    mo_list = list(mongo.db.user.find({"id": user_id}, {"_id": 0}))
    friend_ids = []
    hidden_ids = []
    for i in mo_list:
        friend_ids.append(i["friend"])
        hidden_ids.append(i["hide_friend"])
    try:
        data = moModel.getmoFriend(friend_ids[0],hidden_ids[0])
        return quickRet(data)
    except:
        return "error"
    


@moProfile.route("/<user_id>/hide", methods=["GET"])
def gethidden(user_id):
    try:
        hidelist = moModel.getHideFriendid(user_id)
        hidden_ids = []
        for i in hidelist:
            hidden_ids.append(i["hide_friend"])
        if hidden_ids[0] != []:
            data = moModel.getHideFriendData(hidden_ids[0])
            return quickRet(data)
        else:
            result = {"success": False, "mes": "查無資料"}
            return result
    except:
        result = {"success": False, "mes": "error"}
        return result


@moProfile.route("/<user_id>/dohide", methods=["POST"])
def dohidden(user_id):
    cond = ["id"]
    result = {"success": False, "mes": ""}
    check = checkParm(cond,request.json)
    if(isinstance(check, dict)):
        if type(check) == dict:
            data=moModel.doHideFriend(
                user_id,
                check["id"]
            )
            result["mes"] = "已隱藏"
            result["success"] = True
            return ret(result) 
    else:
        return "error"
    

@moProfile.route("/<user_id>/doshow", methods=["POST"])
def doshow(user_id):
    cond = ["id"]
    result = {"success": False, "mes": ""}
    check = checkParm(cond,request.json)
    if(isinstance(check, dict)):
        if type(check) == dict:
            moModel.doShowFriend(
                user_id,
                check["id"]
            )
            result["mes"] = "已取消隱藏"
            result["success"] = True
            return ret(result) 
    else:
        return "error"

@moProfile.route("/search/<keyword>",methods=["GET"])
def search(keyword):
    try:
        data = moModel.search(keyword)
        return quickRet(data)
    except:
        result = {"success":False,"mes":""}
        return ret(result)