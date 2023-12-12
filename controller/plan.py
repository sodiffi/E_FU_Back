from flask import Blueprint, request
from model import planModel
from .util import checkParm, ret

planAPI = Blueprint("plan", __name__, url_prefix="/plan")


@planAPI.route("/<user_id>", methods=["POST"])
def add_plan(user_id):
    cond = ["user_id", "name", "str_date", "end_date","execute"]
    result = {"success": False, "mes": "新增失敗"}
    check = checkParm(cond, request.json)
    print(check['str_date'],check["end_date"])


    if isinstance(check, dict):
        try:
            data=planModel.addPlan(check)
            if isinstance(data,str): result['mes']="新增重複時段的計畫"
            elif data.acknowledged:
                result["mes"]='新增成功'
                result["success"]=True
                # result['data']=data
        except Exception as e:
            print(e)
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
    return ret(result)

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

@planAPI.route("/barchart/<user_id>", methods=["GET"])
def bar_chart(user_id):
    result = {"success": False, "mes": "查詢失敗"}
    try:
        data=planModel.barChart(user_id)
        result["mes"]='查詢成功'
        result["success"]=True
        result['data']=data
        return ret(result)
    except:
        result["mes"]="查詢失敗"
        return ret(result)
    

@planAPI.route("/runchart/<user_id>", methods=["GET"])
def run_chart(user_id):
    result = {"success": False, "mes": "查詢失敗"}
    try:
        data=planModel.runChart(user_id)
        result["mes"]='查詢成功'
        result["success"]=True
        result['data']=data
        return ret(result)
    except:
        result["mes"]="查詢失敗"
        return ret(result)