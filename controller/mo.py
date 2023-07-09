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
        data = moModel.getmofriend(friend_ids[0],hidden_ids[0])
        return quickRet(data)
    except:
        return "error"
    


@moProfile.route("/<user_id>/hide", methods=["GET"])
def gethidden(user_id):
    try:
        data = moModel.getHideFriend(user_id)
        return quickRet(data)
    except:
        return "error"


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
            print(data)
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
            data=moModel.doShowFriend(
                user_id,
                check["id"]
            )
            print(data)
            result["mes"] = "已取消隱藏"
            result["success"] = True
            return ret(result) 
    else:
        return "error"

