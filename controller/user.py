from flask import Blueprint, request
from model import userModel
from .util import checkParm, ret

userAPI = Blueprint("user", __name__, url_prefix="/user")

@userAPI.route("/test",methods=["GET"])
def test():
    token_type, access_token = request.headers.get('Authorization').split(' ')
    if token_type != 'Bearer' or token_type is None:
        # 驗證token_type是否為Bearer
        pass
    return "test"


@userAPI.route("/<u_id>", methods=["GET"])
def getUser(u_id):
    return ret(userModel.user(u_id))


@userAPI.route("/", methods=["POST"])
def user():
    content = request.json
    return ret(userModel.user(content["user_id"]))


@userAPI.route("/psw", methods=["POST"])
def edit():
    content = request.json
    print(content)
    cond = ["account", "oldPassword", "password", "passwordConfire"]
    result = {"success": False, "mes": ""}
    t = checkParm(cond, content)

    if(isinstance(t, dict)):
        oldPasswordFromDB = userModel.login(
            content["account"], content["oldPassword"])
        print(oldPasswordFromDB)
        print("ok")
        if(len(oldPasswordFromDB) > 0):
            if(content["password"] != content["passwordConfire"]):
                result["mes"] += "密碼和確認密碼不同\n"
            if(result["mes"] == ""):
                data = userModel.changePassword(
                    content["account"], content["password"])
                print(data)
                result["mes"] = "更換密碼成功"
                result["success"] = True
                # result["data"] = data
        elif(len(oldPasswordFromDB) == 0):
            result["mes"] = "輸入舊密碼錯誤"
        else:
            result["mes"] = "帳號異常"
    return ret(result)


@userAPI.route("/", methods=["PATCH"])
def changeProfile():
    content = request.json
    account = content["account"]
    cond = ["area_id", "name"]
    data = {}
    for i in cond:
        if(i in content.keys()):
            data[i] = content[i]
    data = userModel.changeProfile(data, account)
    result = {"success": False, "mes": "修改異常", "data": data}
    if(data["success"]):
        result["success"] = True
        result["mes"] = "修改成功"
    return ret(result)



    