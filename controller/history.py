from flask import Blueprint, request
from model import historyModel
from datetime import datetime
from .util import checkParm, ret, quickRet, get_next_id
from model.db import mongo


historyAPI = Blueprint("history", __name__, url_prefix="/history")


# 歷史運動列表
@historyAPI.route("/list/<id>", methods=["GET"])
def list(id):
    result = {"success": False}
    try:
        data = historyModel.getList(id)
        
        # type_id_counts = {}

        # for item in data['done']:
        #     type_id = item['type_id']
        #     type_id_counts[type_id] = type_id_counts.get(type_id, 0) + 1

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
    except:
        result["mes"] = "資料傳輸發生錯誤"
        result["code"] = 0
        return ret(result)
