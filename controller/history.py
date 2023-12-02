from flask import Blueprint, request
from model import historyModel

from .util import checkParm, ret, quickRet, get_next_id
from model.db import mongo


historyAPI = Blueprint("history", __name__, url_prefix="/history")


# 歷史運動列表
@historyAPI.route("/list/<id>", methods=["GET"])
def list(id):
    result = {"success": False}
    i_id = request.args.get('i_id')

    try:
        data = historyModel.getList(id,i_id=i_id)
        result["data"] = data
        result["mes"] = "查詢成功"
        result["code"] = 200
        result["success"] = True
        return ret(result)
    except Exception as e:
        print(e)
        result["mes"] = "資料傳輸發生錯誤"
        result["code"] = 0
        return ret(result)
    

@historyAPI.route("/<h_id>", methods=["GET"])
def getHistory(h_id):
    result = {"success": False}
    try:
        data = historyModel.getHistory(h_id)
        print(data)
        result["data"] = data
        result["mes"] = "查詢成功"
        result["code"] = 200
        result["success"] = True
        return ret(result)
    except Exception as err:
        print(f"Unexpected {err}, {type(err)}")

        result["mes"] = "資料傳輸發生錯誤"
        result["code"] = 0
        return ret(result)
    
@historyAPI.route("detail/<h_id>/<user_id>")
def getCommand(h_id,user_id):
    result = {"success": False}
    try:
        data = historyModel.getCommend(user_id,h_id)
        
        result["data"] = data
        result["mes"] = "查詢成功"
        result["code"] = 200
        result["success"] = True
        return ret(result)
    except Exception as err:
        print(f"Unexpected {err}, {type(err)}")

        result["mes"] = "資料傳輸發生錯誤"
        result["code"] = 0
        return ret(result)
    

