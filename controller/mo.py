from flask import Blueprint, request
from model import moModel
from .util import checkParm, ret
from model.db import mongo

moProfile = Blueprint("mo", __name__, url_prefix="/mo")

@moProfile.route("/mo/<user_id>", methods=["GET"])
def get(user_id):
    mo_list = list(mongo.db.user.find({"id": user_id}, {"_id": 0, "friend": 1}))
    friend_ids = []
    for i in mo_list:
        friend_ids.append(i["friend"])
    try:
        data = moModel.getmofriend(friend_ids)
        result = {"success": False, "data": data}
        return ret(result)
    except:
        return "error"
    

