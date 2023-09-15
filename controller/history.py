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
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = historyModel.getList(id,now_time)
        
        # type_id_counts = {}

        # for item in data['done']:
        #     type_id = item['type_id']
        #     type_id_counts[type_id] = type_id_counts.get(type_id, 0) + 1

        result["data"] = data
        result["mes"] = "查詢成功"
        result["code"] = 200
        result["success"] = True
        return ret(result)
    except:
        result["mes"] = "資料傳輸發生錯誤"
        result["code"] = 0
        return ret(result)
