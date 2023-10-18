from flask import Blueprint, request
from model import recordModel
from .util import checkParm, ret

recordAPI = Blueprint("record", __name__, url_prefix="/record")


@recordAPI.route("", methods=["POST"])
def add_record():
    cond = ["i_id","user_id","done"]
    check = checkParm(cond, request.json)
    if isinstance(check):
        if type(check) == dict:
            # female = [
            #     [
            #         [11,15,18,20,23],
            #         [10,14,17,20,22],
            #         [10,13,16,19,21],
            #         [9,13,16,18,20],
            #         [5,11,14,17],
            #         [0,9,13,16]
            #     ], #左右
            #     []  #椅子坐立
            # ]
            # male = [
            #     [[12,16,18,21,24]], #左右
            #     []  #椅子坐立
            # ]
            insert_data = []
            for data in check["done"]:
                set_data = {}
                set_data["type_id"] = data["type_id"]
                set_data["times"] = data["times"]
                print(set_data)
                insert_data.append(set_data)



    # token_type, access_token = request.headers.get('Authorization').split(' ')
    # if token_type != 'Bearer' or token_type is None:
    #     # 驗證token_type是否為Bearer
    #     pass
    # return "test"
    if request.is_json:
        data = request.get_json()

        recordModel.record(data["i_id"], data["done"], data["raw"])

    return "ok"
