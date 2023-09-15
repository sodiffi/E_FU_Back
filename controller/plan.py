from flask import Blueprint, request
from model import planModel
from .util import checkParm, ret

planAPI = Blueprint("plan", __name__, url_prefix="/plan")


@planAPI.route("/<user_id>", methods=["POST"])
def add_plan(user_id):
    cond = ["user_id", "name", "str_date", "end_date","execute"]
    result = {"success": False, "mes": "新增失敗"}
    check = checkParm(cond, request.json)

    if isinstance(check, dict):
        try:
            data=planModel.addPlan(check).acknowledged
            result["mes"]='新增成功'
            result["success"]=True
            result['data']=data
        except:
            result["mes"]="新增異常"
    else:
        result['mes']=check
    return ret(result)


@planAPI.route("/<user_id>", methods=["GET"])
def get_plan(user_id):
    result = {"success": False, "mes": "查詢失敗"}
    try:
        data=planModel.getPlan(user_id)
        result["mes"]='查詢成功'
        result["success"]=True
        result['data']=data
    except:
        result["mes"]="查詢異常"

@planAPI.route("/<user_id>", methods=["PUT"])
def edit_plan(user_id):
    cond = [ "name", "str_date", "end_date","execute"]
    result = {"success": False, "mes": "修改失敗"}
    check = checkParm(cond, request.json)

    if isinstance(check, dict):
        try:
            data=planModel.editPlan(check,user_id)
            result["mes"]='修改成功'
            result["success"]=True
            result['data']=data
        except:
            result["mes"]="修改異常"
    else:
        result['mes']=check
    return ret(result)



   
