from flask import Blueprint, request, Response
from model import eModel
import json
import uuid

# from coder import MyEncoder
from flask import app
from model.db import mongo
from datetime import datetime

from .util import checkParm, ret, quickRet

eAPI = Blueprint("therapist", __name__, url_prefix="/therapist")


@eAPI.route("/<t_id>", methods=["GET"])
def getProfile(t_id):
    return quickRet(eModel.getProfile(t_id))


@eAPI.route("/<t_id>", methods=["POST"])
def updateProfile(t_id):
    cond = ["phone", "sex", "name", "birthday"]
    check = checkParm(cond, request.json)
    if type(check) == dict:
        temp=eModel.editProfile(
                t_id,
                check["name"],
                check["sex"],
                check["birthday"],
                check["phone"],
            )
        print(temp.raw_result)
        return quickRet("good")
    else:
        return quickRet(check)


@eAPI.route("/p/<t_id>", methods=["GET"])
def get(t_id):
    return quickRet(eModel.getEpeople(t_id))


@eAPI.route("/a/<t_id>", methods=["GET"])
def getAppoint(t_id):
    return quickRet(eModel.getAppoint(t_id))


@eAPI.route("/a/d", methods=["GET"])
def getAppointDetail():
    cond = ["start_date", "time", "t_id"]
    check = checkParm(cond, request.args)
    result = {
        "success": False,
    }
    if type(check) == dict:
        result["success"] = True
        result["data"] = eModel.getAppointDetail(
            check["t_id"], check["start_date"], check["time"]
        )
    else:
        result["mes"] = check

    return ret(result)

@eAPI.route('/appointment',methods=["POST"])
def editAppoint():
    cond=["a_id","done"]
    check=checkParm(cond,request.json)
    result = {
        "success": False,
    }
    if type(check)==dict:
        result["success"]=True
        eModel.edit_appointment(check["a_id"],check['done'])
    else:
        result['msg']=check
    return ret(result)
    
