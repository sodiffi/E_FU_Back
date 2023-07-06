from flask import Blueprint, request,Response
from model import moModel
from .util import checkParm, ret, quickRet
from model.db import mongo

moProfile = Blueprint("mo", __name__, url_prefix="/mo")

@moProfile.route("/<user_id>", methods=["GET"])
def get(user_id):
    # print(user_id)
    mo_list = list(mongo.db.user.find({"id": user_id}, {"_id": 0, "friend": 1}))
    friend_ids = []
    for i in mo_list:
        friend_ids.append(i["friend"])
    print(friend_ids)
    try:
        data = moModel.getmofriend(friend_ids[0])
        result = {"success": False, "data": data}
        return ret(result)
    except:
        return "error"
    

