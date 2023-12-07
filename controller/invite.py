from flask import Blueprint, request
from model import inviteModel
from .util import checkParm, ret, quickRet, get_next_id
from model.db import mongo


inviteAPI = Blueprint("invite", __name__, url_prefix="/invite")


# 新增邀約
@inviteAPI.route("/<m_id>", methods=["POST"])
def addinvite(m_id):
    cond = ["name", "friend", "time", "remark"]
    result = {"success": False, "mes": ""}
    check = checkParm(cond, request.json)

    if isinstance(check, dict):
        if type(check) == dict:
            # id = check["id"]
            name = check["name"]
            friend = check["friend"]
            time = check["time"]
            remark = check["remark"]
            id = get_next_id("Invite")
            data = inviteModel.addinvite(id, name, m_id, friend, time, remark)
            
            if data == "0" :
                result["mes"] = "新增邀約失敗，附近時段已有其他運動邀約"
                result["success"] = False
                return ret(result)
            else:
                friend = []
                for i in check["friend"]:
                    friend.append(i)
                if friend != []:
                    try:
                        
                        insert_data = []
                        for i in range(0, len(friend)):
                            insert_data.append(
                                {
                                    "i_id": id,
                                    "user_id": friend[i],
                                    "accept": 3 if friend[i] != m_id else 1,
                                    "done": [],
                                }
                            )
                            # {"sets_no": 0, "item_id": 0, "times": 0, "level": 0}
                        inviteModel.addinvitedetail(insert_data)
                        result["mes"] = "新增邀約成功"
                        result["success"] = True
                        return ret(result)
                    except:
                        result["mes"] = "好友邀約失敗"
                        return ret(result)
                else:
                    result["mes"] = "新增邀約成功，您暫無邀請任何好友"
                    result["success"] = True
                    return ret(result)
    else:
        result["mes"] = "新增邀約異常"
        return ret(result)


# 修改邀約
@inviteAPI.route("/<m_id>/<id>", methods=["PUT"])
def editinvite(m_id, id):
    cond = ["name", "friend", "time", "remark","m_id"]
    check = checkParm(cond, request.json)
    result = {"success": False, "mes": ""}
    name = check["name"]
    friend = check["friend"]
    time = check["time"]
    remark = check["remark"]
    if isinstance(check, dict):
        if type(check) == dict:
            data = inviteModel.editinvite(id, name, m_id, friend, time, remark)
            if not isinstance(data,str):
                
                result["mes"] = "編輯成功"
                result["success"] = True
            return ret(result)
    else:
        result["mes"] = "修改失敗"
        return ret(result)


# 邀請列表使用另外的MQL
@inviteAPI.route("/list2/<user_id>/<int:mode>", methods=["GET"])
def inviteList(user_id, mode):
    data = inviteModel.invitelist(user_id, mode)
    
    return quickRet(data)



# 查看邀約內容
@inviteAPI.route("/<m_id>/<id>", methods=["GET"])
def getinviteDetail(m_id, id):
    try:
        data = inviteModel.getinviteDetail(int(id))
        return quickRet(data)
    except:
        result = {"success": False, "mes": "查無資料"}
        return ret(result)


# 使用者回復邀約
@inviteAPI.route("/<m_id>/<id>", methods=["POST"])
def replyinvite(m_id, id):
    cond = ["accept"]
    check = checkParm(cond, request.json)
    result = {"success": False, "mes": ""}
    if isinstance(check, dict):
        if type(check) == dict:
            try:
                accept = check["accept"]
                data = inviteModel.replyinvite(m_id, int(id), accept)
                if data == "0" :
                    result["mes"] = "該時段已有其他運動"
                    result["success"] = False
                else:    
                    if accept==1:
                        result["mes"] = "已接受邀約"
                    elif accept==2:
                        result["mes"] = "已拒絕邀約"
                    result["success"] = True
                return ret(result)
            except:
                return ret(result)
    else:
        result["mes"] = "資料傳遞錯誤"
        return ret(result)


@inviteAPI.route("/search/<m_id>/<time>", methods=["GET"])
def searchInvite(m_id, time):
    args = request.args
    
    result = {"success": False, "mes": ""}
    try:
        data = inviteModel.searchInvite(m_id, time,id=args.get("id"))
        
        return quickRet(data)
    except Exception as e:
        print("except",e)
        return ret(result)
