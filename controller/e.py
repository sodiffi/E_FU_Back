from flask import Blueprint, request, Response
from model import eModel
import json
import uuid
# from coder import MyEncoder
from flask import app
from model.db import mongo
from datetime import datetime

from .util import checkParm, ret

eAPI = Blueprint("e", __name__, url_prefix="/e")

@eAPI.route("/p/<e_id>", methods=["GET"])
def get(e_id):
    data = eModel.getEpeople(e_id)
    print((data))
    print(type(data))
    result = {"success": True, "data": data}
    return ret(result)

@eAPI.route("/a/<e_id>",methods=["GET"])
def getAppoint(e_id):
    result = {"success": True, "data": eModel.getAppoint(e_id)}
    return ret(result)

@eAPI.route('a/d',methods=["GET"])
def getAppointDetail():
    cond=["start_date","time","e_id"]
    check=checkParm(cond,request.args)
    result = {"success": False, }
    if(type(check)==dict):
        result["success"]=True
        result['data']=eModel.getAppointDetail(check["e_id"],check["start_date"],check["time"])
    else:
        result['mes']=check

    return ret(result)

