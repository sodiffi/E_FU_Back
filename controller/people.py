from flask import Blueprint, request, Response
from model import peopleModel
import json
import uuid
# from coder import MyEncoder
from flask import app
from model.db import mongo
from datetime import datetime

from .util import checkParm, ret,quickRet

peopleProfile = Blueprint("people", __name__, url_prefix="/people")

@peopleProfile.route("/", methods=["GET"])
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

@peopleProfile.route("/", methods=["POST"])
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

# @peopleProfile.route("/arrange", methods=["POST"])
# def arrange():
#     content = request.json
#     print(content)
#     uid = uuid.uuid4()
#     arrange_id=str(uid)
#     e_id = content["e_id"]
#     project_id = content["project_id"]
#     need_times = content["need_times"]
#     finish_group = content["finish_group"]
#     recovery_time = content["recovery_time"]
#     order = content["order"]
#     account = content["account"]
#     access = peopleModel.finduid(e_id)
#     print(access)
#     data = peopleModel.arrange(e_id, project_id, need_times, finish_group, recovery_time,order,account)
#     print((data))
#     result = {"success": False, "data": data}
#     return ret(result)



@peopleProfile.route("/tfind", methods=["GET"])
def findt():
    data = peopleModel.findTherapist()
    print((data))
    result = {"success": False, "data": data}
    return ret(result)


@peopleProfile.route("/twork/<t_id>", methods=["GET"])
def findtwork(t_id):
    data = peopleModel.findTherapist(t_id)
    result = {"success": False, "data": data}
    return ret(result)

@peopleProfile.route("/appointment/<t_id>", methods=["POST"])
def appointment(t_id):
    cond = ["id","start_date", "time","item","p_id","done","remark"]
    check = checkParm(cond, request.json)
    if type(check) == dict:
        temp=peopleModel.appointment(
                t_id,
                check["id"],
                check["start_date"],
                check["time"],
                check["item"],
                check["p_id"],
                check["done"],
                check["remark"]
            )
        print(temp.inserted_id)
        return quickRet("Appointment successful")
    else : 
        return quickRet(check)

@peopleProfile.route("/appointment/find", methods=["POST"])
def findappointment():
    content = request.json
    p_id = content["p_id"]
    data = peopleModel.findappointment(p_id)
    result = {"success": False, "data": data}
    return ret(result)