from flask import Blueprint, request
from model import inviteModel
from .util import checkParm, ret, quickRet
from model.db import mongo

inviteAPI = Blueprint("invite", __name__, url_prefix="/invite")

#新增邀約
@inviteAPI.route("/<m_id>/add", methods=["POST"]) 
def addinvite(m_id):
    cond = ["id", "name", "friend","time","remark"]
    result = {"success": False, "mes": ""}
    check = checkParm(cond, request.json)

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


#修改邀約
@inviteAPI.route("/<m_id>/<id>/edit", methods=["POST"]) 
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

#查看邀約列表
@inviteAPI.route("/<m_id>", methods=["GET"]) 
def getinviteList(m_id):
    acceptList=inviteModel.getacceptList(m_id)
    accept_ids = []
    for i in acceptList:
        accept_ids.append(i["id"])
    if(accept_ids !=[]):
        data = inviteModel.getinviteList(m_id,accept_ids)
        print(data)
        return quickRet(data) 
    else : 
        result = {"success": False, "mes": "查無資料"}
        return ret(result)
    

#查看邀約內容
@inviteAPI.route("/<m_id>/<id>", methods=["GET"]) 
def getinviteDetail(m_id,id):
    try:
        print(123)
        data = inviteModel.getinviteDetail(m_id,int(id))
        print(data)
        return quickRet(data)
    except: 
        result = {"success": False, "mes": "查無資料"}
        return ret(result)
    
    
# @inviteAPI.route("/edit", methods=["POST"]) 
# def edit():
#     check = request.json
#     print(check)
#     m_id = check["m_id"]
#     id = check["id"]
#     data = inviteModel.getinviteDetail(m_id,id)
#     print((data))
#     result = {"success": False, "data": data}
#     return ret(result)

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

    
