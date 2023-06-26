from flask import Blueprint, request
from model import recordModel
from .util import checkParm, ret

recordAPI = Blueprint("record", __name__, url_prefix="/record")


@recordAPI.route("", methods=["POST"])
def add_record():
    # token_type, access_token = request.headers.get('Authorization').split(' ')
    # if token_type != 'Bearer' or token_type is None:
    #     # 驗證token_type是否為Bearer
    #     pass
    # return "test"
    if request.is_json:
        data = request.get_json()

        recordModel.record(data["a_id"], data["done"], data["raw"])

    return "ok"
