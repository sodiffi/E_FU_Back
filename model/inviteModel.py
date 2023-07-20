import json
from model.util import group
from model.db import mongo
from datetime import datetime,timedelta

def addinvite(id,name,m_id,friend,time,remark): #新增邀約
    return mongo.db.Invite.insert_one(
        {
            "id": id,
            "name": name,
            "m_id": m_id,
            "friend": friend,
            "time": time,
            "remark": remark,
        }
    )


def editinvite(id,name,m_id,friend,time,remark): #修改邀約
    return mongo.db.Invite.update_one(
        {"id": id, "m_id":m_id},
        {
            "$set": {
                "name": name,
                "friend": friend,
                "time": time,
                "remark": remark
            }
        },
    )

def getacceptList(m_id):
    return list(mongo.db.Invite_detail.aggregate(
        [
            {
                '$match': {
                    'user_id': m_id, 
                    'accept': True
                }
            }, {
                '$project': {
                    'id': '$a_id', '_id': 0
                }
            }
        ]
    ))


def getinviteList(m_id,acceptList): #邀約列表
    return list(mongo.db.Invite.aggregate(
            [
                {
                    '$match': {
                        'm_id': m_id
                    }
                }, {
                    '$project': {
                        'id': 1, 'name': 1, 'time': 1, '_id': 0
                    }
                }, {
                    '$unionWith': {
                        'coll': 'Invite', 
                        'pipeline': [
                            {
                                '$match': {
                                    'id': {'$in': acceptList}
                                }
                            }, {
                                '$project': {
                                    'id': 1, 'name': 1, 'time': 1, '_id': 0
                                }
                            }
                        ]
                    }
                }
            ]
        ))


def getinviteDetail(id,name,m_id,friend,time,remark): #修改活動
    return mongo.db.Invite.update_one(
        {"id": id, "m_id":m_id},
        {
            "$set": {
                "name": name,
                "friend": friend,
                "time": time,
                "remark": remark
            }
        },
    )


# def accept(m_id,a_id,accept):
#     return ''

# def reject():
#     return ''



    """ try:
        mongo.db.inviteid.insert_one(data)
        return ""
    except:
         return "error" """

""" def get():
    return mongo.db.user.insert_one(inviteid) """