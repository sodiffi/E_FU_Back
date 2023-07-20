from flask import Blueprint, request
from model import inviteModel
from .util import checkParm, ret, quickRet
from model.db import mongo

inviteAPI = Blueprint("invite", __name__, url_prefix="/invite")

@inviteAPI.route("/<m_id>/add", methods=["POST"]) #新增邀約
def addinvite(m_id):
    cond = ["id", "name", "friend","time","remark"]
    result = {"success": False, "mes": ""}
    check = checkParm(cond, request.json)
    print(check)

    if(isinstance(check, dict)):
        if type(check) == dict:
            temp=inviteModel.addinvite(
                check["id"],
                check["name"],
                m_id,
                check["friend"],
                check["time"],
                check["remark"]
            )
            print(temp)
            result["mes"] = "新增邀約成功"
            result["success"] = True
            return ret(result) 
    else : 
        result["mes"] = "新增邀約異常"
        return ret(result)    

  
@inviteAPI.route("/<m_id>/edit/<id>", methods=["POST"]) #修改邀約
def editinvite(m_id,id):
    cond = ["name", "friend", "time", "remark"]
    check = checkParm(cond, request.json)
    print(check)
    result = {"success": False, "mes": ""}
    name = check["name"]
    friend = check["friend"]
    time = check["time"]
    remark = check["remark"]
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

           

    
    """ data = inviteModel.addinviteid(t)
        if(data.inserted_id):
            result["mes"] = "新增邀約成功"
            result["success"] = True

        else:
            result["mes"] = "新增邀約異常"
    else:
        result["mes"] = "請填畢所有資料"
    return ret(result) """

    """ try:
        data = inviteModel.getinviteid(friend_ids)
        result = {"success": False, "data": data}
        return ret(result)
    except:
        return "error" """
    

