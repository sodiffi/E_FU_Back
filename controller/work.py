from flask import Blueprint, request, Response
from model import workModel
import json
import uuid
# from coder import MyEncoder
from flask import app
from model.db import mongo


from .util import checkParm, ret,quickRet

workProfile = Blueprint("work", __name__, url_prefix="/work")

@workProfile.route("/<t_id>", methods=["GET"])
def getwork(t_id):
    return quickRet(workModel.getWork(t_id))


@workProfile.route("/<t_id>/add", methods=["POST"])
def addwork(t_id):
    cond = ["start_date", "work"]
    check = checkParm(cond, request.json)
    if type(check) == dict:
        temp=workModel.addWork(
                t_id,
                check["start_date"],
                check["work"]
            )
        print(temp.inserted_id)
        return quickRet("add success")
    else : 
        return quickRet(check)
