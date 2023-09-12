from flask import Blueprint, request
from model import historyModel
from .util import checkParm, ret, quickRet, get_next_id
from model.db import mongo


historyAPI = Blueprint("history", __name__, url_prefix="/history")


# 歷史運動列表
@historyAPI.route("/list/<id>", methods=["GET"])
def list(m_id):
    cond = ["id"]
    result = {"success": False, "mes": ""}
    check = checkParm(cond, request.json)

    if isinstance(check, dict):
        if type(check) == dict:
            try:
                id = check["id"]
                historyModel.getList(id)
                result["mes"] = "查詢成功"
                result["code"] = 200
                result["success"] = True
                return ret(result)
            except:
                result["mes"] = "資料傳輸發生錯誤"
                result["code"] = 0
                return ret(result)
        else:
            result["mes"] = "資料傳輸發生錯誤"
            result["code"] = 0
            return ret(result)
