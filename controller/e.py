from flask import Blueprint, request, Response
from model import eModel
import json
import uuid
# from coder import MyEncoder
from flask import app
from model.db import mongo
from datetime import datetime

from .util import checkParm, ret,quickRet

eAPI = Blueprint("e", __name__, url_prefix="/e")

@eAPI.route("/p/<e_id>", methods=["GET"])
def get(e_id):
    return quickRet(eModel.getEpeople(e_id))

@eAPI.route("/a/<e_id>",methods=["GET"])
def getAppoint(e_id):
    return quickRet(eModel.getAppoint(e_id))

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

