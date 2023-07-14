import json
from model.util import group
from model.db import mongo
from datetime import datetime,timedelta

def addinvite(id,name,m_id,friend,time,remark):
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


def editinvite(id,name,m_id,friend,time,remark):
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


    """ try:
        mongo.db.inviteid.insert_one(data)
        return ""
    except:
         return "error" """

""" def get():
    return mongo.db.user.insert_one(inviteid) """