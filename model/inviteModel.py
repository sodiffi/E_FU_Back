import json
from model.util import group
from model.db import mongo
from datetime import datetime, timedelta
import numpy as np


def addinvite(id, name, m_id, friend, time, remark):  # 新增邀約
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


def addinvitedetail(data):
    return mongo.db.Invite_detail.insert_many(data)


def editinvite(id, name, m_id, friend, time, remark):  # 修改邀約
    return mongo.db.Invite.update_one(
        {"id": id, "m_id": m_id},
        {"$set": {"name": name, "friend": friend, "time": time, "remark": remark}},
    )


def getinviteDetail( i_id):  # 邀約詳細資料
    return list(
        mongo.db.Invite_detail.aggregate(
            [
                {"$match": {"i_id": i_id}},
                {
                    "$lookup": {
                        "from": "user",
                        "localField": "user_id",
                        "foreignField": "id",
                        "as": "result",
                    }
                },
                {"$unwind": {"path": "$result"}},
                {
                    "$addFields": {
                        "userName": "$result.name",
                        "targetSets": "$result.target_sets",
                    }
                },{
                    "$unset":["result","_id"]
                }
            ]
        )
    )


def invitelist(user_id, accept):
    # 0全部; 1接受; 2不接受; 3未回應;
    modePipline = {
        "user_id": user_id,
    }
    if accept != 0:
        modePipline["accept"] = accept
    return list(
        mongo.db.Invite_detail.aggregate(
            [
                {"$match": modePipline},
                {
                    "$lookup": {
                        "from": "Invite",
                        "localField": "i_id",
                        "foreignField": "id",
                        "as": "invite",
                    }
                },
                {"$unwind": {"path": "$invite"}},
                {
                    "$addFields": {
                        "name": "$invite.name",
                        "m_id": "$invite.m_id",
                        "remark": "$invite.remark",
                        "time": "$invite.time",
                        "friend": "$invite.friend",
                    }
                },
                {
                    "$lookup": {
                        "from": "user",
                        "localField": "m_id",
                        "foreignField": "id",
                        "as": "user",
                    }
                },
                {
                    "$unwind": {
                        "path": "$user",
                    }
                },
                {"$addFields": {"m_name": "$user.name"}},
                {"$unset": ["user", "invite", "_id"]},
            ]
        )
    )


def replyinvite(m_id, i_id, accept):
    return mongo.db.Invite_detail.update_one(
        {"i_id": i_id, "user_id": m_id},
        {
            "$set": {
                "accept": accept,
            }
        },
    )
