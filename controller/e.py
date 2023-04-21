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

