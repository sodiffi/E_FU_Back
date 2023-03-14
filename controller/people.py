from flask import Blueprint, request, Response
from model import peopleModel
import json
import uuid
# from coder import MyEncoder
from flask import app
from model.db import mongo
from datetime import datetime

from .util import checkParm, ret

peopleProfile = Blueprint("people", __name__, url_prefix="/people")

@peopleProfile.route("/show", methods=["GET"])
def get():
    data = peopleModel.getpeople()
    print((data))
    print(type(data))
    result = {"success": False, "data": data}
    return ret(result)



# @peopleProfile.route("/add", methods=["POST"])
# def add(name,gender,birth,height,weight):
#     data = {"name":name,"gender":gender,"birth":birth,"height":height,"weight":weight}
#     print((data))
#     result = {"success": False, "data": data}
#     peopleModel.addpeople(data)

@peopleProfile.route("/add", methods=["POST"])
def add():
    content = request.json
    print(content)
    uid = uuid.uuid4()
    uid=str(uid)
    print(uid)
    name = content["name"]
    gender = content["gender"]
    birth = content["birth"]
    # birth = datetime.strptime(content["birth"],'%Y-%m-%d').date()
    height = content["height"]
    weight = content["weight"]
    disease_id = content["disease_id"]
    data = peopleModel.addpeople(uid,name, gender, birth, height, weight,disease_id)
    print((data))
    result = {"success": False, "data": data}
    return ret(result)


@peopleProfile.route("/search", methods=["POST"])
def findname():
    content = request.json
    print(content)
    name = content["name"]
    data = peopleModel.findname(name)
    print((data))
    result = {"success": False, "data": data}
    return ret(result)


@peopleProfile.route("/edit", methods=["POST"])
def edit():
    content = request.json
    print(content)
    uid = content["uid"]
    data = peopleModel.finduid(uid)
    print((data))
    result = {"success": False, "data": data}
    return ret(result)


@peopleProfile.route("/edit/id", methods=["POST"])
def editpeople():
    content = request.json
    print(content)
    result = {"success": False, "mes": ""}
    uid = content["uuid"]
    name = content["name"]
    gender = content["gender"]
    birth = content["birth"]
    height = content["height"]
    weight = content["weight"]
    disease_id = content["disease_id"]
    if(result["mes"] == ""):
        data = peopleModel.editpeople(uid,name, gender, birth, height, weight,disease_id)
        print((data))
        result["mes"] = "編輯成功"
        result["success"] = True
    return ret(result)