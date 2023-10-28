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
        try:
            recordModel.record(check["detail"][0],check["record"])
            result["mes"]="新增成功"
        except:
            result["mes"]="新增異常"
    else:
        result['mes']=check
    return ret(result)
    
    return 




    # token_type, access_token = request.headers.get('Authorization').split(' ')
    # if token_type != 'Bearer' or token_type is None:
    #     # # 驗證token_type是否為Bearer
    #     pass
    #     # return "test"
    
    # if request.is_json:
    #     data = request.get_json()

    #     recordModel.record(data["user_id"], data["i_id"],data["done"], data["raw"])
    #     return "ok"
