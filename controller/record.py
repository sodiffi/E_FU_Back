from flask import Blueprint, request
from model import recordModel
from .util import checkParm, ret

recordAPI = Blueprint("record", __name__, url_prefix="/record")


@recordAPI.route("", methods=["POST"])
def add_record():
    cond = ["record","detail"]
    check = checkParm(cond, request.json)
    result = {"success": False, "mes": "新增失敗"}
    if isinstance(check, dict):
        done = []
        each_score = []
        total_score=[]
        for i in check["detail"]:
            check2=checkParm(["user_id","i_id",'done','each_score','total_score'],i)
            if isinstance(check2, dict):
                i_id = check2["i_id"]
                user_id = check2["user_id"]
                done.append( {'case': {'$eq': ['$user_id', check2["user_id"]]}, 'then': check2["done"]})
                each_score.append( {'case': {'$eq': ['$user_id', check2["user_id"]]}, 'then': check2["each_score"]})
                total_score.append( {'case': {'$eq': ['$user_id', check2["user_id"]]}, 'then': check2["total_score"]})
        
        try:
            recordModel.record(done,each_score,total_score,check["record"],i_id,user_id)
            result["mes"]="新增成功"
            result["success"]=True
        except:
            result["mes"]="新增異常"
    else:
        result['mes']=check
    return ret(result)

@recordAPI.route("/update/<user_id>", methods=["GET"])
def update_record(user_id):
    try:
        recordModel.avg_score(user_id)
        return "更新成功"
    except:
        return "更新失敗"
    