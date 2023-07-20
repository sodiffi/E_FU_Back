from flask import Blueprint, request
from model import inviteModel
from .util import checkParm, ret, quickRet
from model.db import mongo

inviteAPI = Blueprint("invite", __name__, url_prefix="/invite")


@inviteAPI.route("/<m_id>/add", methods=["POST"]) #新增活動
def addinvite(m_id):
    cond = ["id", "name", "friend","time","remark"]
    result = {"success": False, "mes": ""}
    check = checkParm(cond, request.json)
    print(check)

    if(isinstance(check, dict)):
        if type(check) == dict:
            data=inviteModel.addinvite(
                check["id"],
                check["name"],
                m_id,
                check["friend"],
                check["time"],
                check["remark"]
            )
            print(data)
            result["mes"] = "新增邀約成功"
            result["success"] = True
            return ret(result) 
    else : 
        result["mes"] = "新增邀約異常"
        return ret(result)    

        
@inviteAPI.route("/<m_id>/edit/<id>", methods=["POST"]) #修改活動
def editinvite(m_id,id):
    cond = ["name", "friend","time","remark"]
    check = checkParm(cond, request.json)
    print(check)
    result = {"success": False, "mes": ""}
    name=check["name"]
    friend=check["friend"]
    time=check["time"]
    remark=check["remark"]
    if(isinstance(check, dict)):
        if type(check) == dict:
            data = inviteModel.editinvite(id, name, m_id, friend, time, remark)
            print((data))
            result["mes"] = "編輯成功"
            result["success"] = True
            return ret(result)
    else:
        result["mes"] = "修改失敗"
        return ret(result)  


@inviteAPI.route("/edit", methods=["POST"]) 
def edit():
    check = request.json
    print(check)
    m_id = check["m_id"]
    id = check["id"]
    data = inviteModel.findmid(m_id,id)
    print((data))
    result = {"success": False, "data": data}
    return ret(result)



@inviteAPI.route("/<m_id>/invite", methods=["GET"]) #查看活動列表
def getinviteList(m_id):
    data=inviteModel.getinviteList(m_id)
    if(data[0] !=[]):
        print(data)
        return quickRet(data) 
    else : 
        result = {"success": False, "mes": "查無資料"}
        return ret(result)
    
    
@inviteAPI.route("/<m_id>/invite/<a_id>", methods=["GET"]) #查看活動內容
def getinviteDetail(m_id):
    data=inviteModel.getinviteDetail(m_id)
    if(data[0] !=[]):
        print(data)
        return quickRet(data) 
    else : 
        result = {"success": False, "mes": "查無資料"}
        return ret(result)

# @inviteAPI.route("/<m_id>/<a_id>", methods=["POST"]) #使用者回復邀約
# def replyinvite():
#     check = request.json
#     print(check)
#     result = {"success": False, "mes": ""}
#     id=check["id"],
#     name=check["name"],
#     # m_id=check["m_id"],
#     friend=check["friend"],
#     time=check["time"],
#     remark=check["remark"]
#     if(result["mes"] == ""):
#         data = inviteModel.editinvite(id, name, m_id, friend, time, remark)
#         print((data))
#         result["mes"] = "編輯成功"
#         result["success"] = True
#     return ret(result)

    

