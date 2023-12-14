from flask import Blueprint, request
from model import homeModel

from .util import quickRet
from model.db import mongo


homeAPI = Blueprint("home", __name__, url_prefix="/home")
@homeAPI.route("/<int:user_id>", methods=["GET"])
def home(user_id):
    try:
        return quickRet(homeModel.getHome(user_id))
    except Exception as e:
        print(e)
