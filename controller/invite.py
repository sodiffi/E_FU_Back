from flask import Blueprint, request
from model import inviteModel
from .util import checkParm, ret, quickRet
from model.db import mongo

inviteAPI = Blueprint("invite", __name__, url_prefix="/invite")

@inviteAPI.route("/<m_id>/add", methods=["POST"])
def addinvite(m_id):
    cond = ["id", "name", "friend","time","remark"]
    result = {"success": False, "mes": ""}
    check = checkParm(cond, request.json)
    print(check)

    if(isinstance(check, dict)):
        # hasInvite = inviteModel.hasInvite(check["id"])
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
        
        
@inviteAPI.route("/<m_id>/edit", methods=["POST"])
def editinvite():
    check = request.json
    print(check)
    result = {"success": False, "mes": ""}
    id=check["id"],
    name=check["name"],
    m_id=check["m_id"],
    friend=check["friend"],
    time=check["time"],
    remark=check["remark"]
    if(result["mes"] == ""):
        data = inviteModel.editinvite(id, name, m_id, friend, time, remark)
        print((data))
        result["mes"] = "編輯成功"
        result["success"] = True
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
    

