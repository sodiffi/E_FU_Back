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
        score = []
        for i in check["detail"]:
            check2=checkParm(["user_id","i_id","score",'done'],i)
            if isinstance(check2, dict):
                i_id = check2["i_id"]
                done.append( {'case': {'$eq': ['$user_id', check2["user_id"]]}, 'then': check2["done"]})
                score.append( {'case': {'$eq': ['$user_id', check2["user_id"]]}, 'then': check2["score"]})
        try:
            recordModel.record(done,score,check["record"],i_id)
            result["mes"]="新增成功"
            result["success"]=True
        except:
            result["mes"]="新增異常"
    else:
        result['mes']=check
    return ret(result)




    # token_type, access_token = request.headers.get('Authorization').split(' ')
    # if token_type != 'Bearer' or token_type is None:
    #     # # 驗證token_type是否為Bearer
    #     pass
    #     # return "test"
    
    # if request.is_json:
    #     data = request.get_json()

    #     recordModel.record(data["user_id"], data["i_id"],data["done"], data["raw"])
    #     return "ok"
